import sys
import ruamel.yaml
import attrdict
import logbook

from keycloak import KeycloakOpenID
from collections import Counter
from ruamel.yaml import CommentedMap, RoundTripDumper
from cloud_sdk.keycloak_token import KeyCloakToken
from cloud_sdk.product_catalog import ProductCatalogClient
from pprint import pprint


def scan_ui_schema(schema: dict, path=""):
    if path == "":
        print("")
        print("")
        print("")
        # pprint(schema, width=160)
        print("")
    for field, data in schema.items():
        if not field.startswith("ui:") and isinstance(data, dict):
            ui_field = data.get("ui:field")
            if ui_field:
                yield path + field, ui_field, None
            else:
                ui_widget = data.get("ui:widget")
                if ui_widget:
                    yield path + field, None, ui_widget
                else:
                    yield from scan_ui_schema(data, path + field + ".")
        else:
            if field not in ("ui:readonly", "ui:options", "ui:order", "ui:autofocus", "ui:help"):
                print("!!!!", field, data)


def get_user_token(login, password):
    client = KeycloakOpenID(server_url="http://dev-keycloak.apps.d0-oscp.corp.dev.vtb/auth/",
                            client_id="portal-cli ",
                            realm_name="Portal",
                            verify=False)

    token = client.token(login, password, scope="offline_access")
    return token["access_token"]


def get_service_token():
    keycloak_config = attrdict.AttrDict({
        "url": "http://dev-keycloak.apps.d0-oscp.corp.dev.vtb/auth/",
        "client_id": "cloud_accountmanager",
        "realm_name": "Portal",
        "client_secret_key": "84fa8393-aa8f-42b1-898c-1d17b68bb8e2"
    })
    keycloak_token = KeyCloakToken(keycloak_config)
    return keycloak_token.get_access_token()


class RefResolutionError(Exception):
    pass


nodefault = object()


class Field:
    def __init__(self, name, data, document):
        self.name = name
        ref = data.pop("$ref", None)
        if ref:
            data.update(resolve_fragment(document, ref))

        self._data = data
        self.title = data.get("title")
        self.default = data.get("default", nodefault)
        self.enum = None
        enum_ = data.get("enum")
        if enum_:
            data.setdefault("type", "enum")
            self.enum = enum_

        self.type = data["type"]
        if self.type not in ("number", "string", "boolean", "object", "integer", "enum", "array"):
            print("## type", self.name, self.type)
            xxxx
            # pprint(data)
        self.ui_ext = None
        self.required = False
        self.readonly = False
        self.widget = None
        self.ui_field = None
        self.subfields = None
        if self.type == "object":
            self.subfields = self._object(data, document)
        elif self.type == "array":
            self._array(data, document)

    def _object(self, data, document):
        ref = data.pop("$ref", None)
        if ref:
            data.update(resolve_fragment(document, ref))
        required = set(data.get("required", []))
        properties = data.get("properties")
        fields = []
        if not properties:
            print("!!!!", data)
        for name, data in properties.items():
            f = Field(name, data, {})
            if f.name in required:
                f.required = True
            fields.append(f)

        return fields

    def _array(self, data, document):
        print("Array", self.name)
        pprint(data)
        items = data["items"]
        if isinstance(items, dict):
            ref = items.pop("$ref", None)
            if ref:
                items.update(resolve_fragment(document, ref))
            if items["type"] == "object":
                fields = self._object(items, document)
                self.subfields = fields

        # maxitems minitems

    def __str__(self):
        default = self.default if self.default is not nodefault else "nodefault"
        return f"<{self.name} ({self.title}) type: {self.type}, default: {default}>"

    __repr__ = __str__

    def update_ext(self, ui_ext):
        self.ui_ext = ui_ext

        readonly = ui_ext.pop("ui:readonly",  None)
        if readonly is not None:
            self.readonly = readonly

        widget = ui_ext.pop("ui:widget", None)
        if widget is not None:
            self.widget = widget

        ui_field = ui_ext.pop("ui:field", None)
        if ui_field is not None:
            self.ui_field = ui_field

        if self.type == "object":
            for field in self.subfields:
                ext = ui_ext.pop(field.name, None)
                if ext:
                    field.update_ext(ext)

        if ui_ext:
            print("!!!!!!!!!!", self.name, ui_ext)
            #  pprint(self._data)
            print("=---------================================")

    def to_template(self):
        pass

    def convert_to_yaml_struct(self, dumper):
        if self.default is not nodefault:
            if self.type in ("number", "integer"):
                node = dumper.represent_int(self.default)
            elif self.type == "string":
                node = dumper.represent_str(self.default)
            elif self.type == "boolean":
                node = dumper.represent_bool(self.default)
            elif self.type in ("array", ""):
                node = dumper.represent_none(None)
            else:
                node = dumper.represent_none(None)

            return node

        if self.required:
            return dumper.represent_str("<required>")
        return dumper.represent_str("")

    @staticmethod
    def yaml_representer(dumper, data, flow_style=False):
        assert isinstance(dumper, ruamel.yaml.RoundTripDumper)
        return data.convert_to_yaml_struct(dumper)

    def get_yaml_comment(self):
        if self.type == "object":
            return ""

        title = self.title + " " if self.title else ""
        if self.readonly or (self.enum and len(self.enum) == 1):
            comment = f"{title}"
        else:
            t = "one of: " + ", ".join(str(e) for e in self.enum) if self.enum else f"type: {self.type}"
            comment = f"{title}\n{t}"
            mini = self._data.get("minimum")
            if mini is not None:
                comment += f"\nminimum: {mini}"
            maxi = self._data.get("maximum")
            if maxi is not None:
                comment += f"\nmaximum: {maxi}"

            max_length = self._data.get("maxLength")
            min_length = self._data.get("minLength")
            if max_length is not None and min_length:
                comment += f"\nlength between {min_length} and {max_length}"
            elif min_length:
                comment += f"\nlength should be more than {min_length}"
            elif max_length is not None:
                comment += f"\nlength should be less that {max_length}"
            pattern = self._data.get("pattern")
            if pattern is not None:
                comment += f"\npattern: {pattern}"

            if self.ui_ext:
                comment += f"\nExt: {self.ui_ext}"

        return comment + f"\n!!!{self._data}"


def resolve_fragment(document, fragment):
    """
    Resolve a ``fragment`` within the referenced ``document``.
    Arguments:
        document:
            The referent document
        fragment (str):
            a URI fragment to resolve within it
    """
    from urllib.parse import unquote
    from collections import Sequence

    fragment = fragment.lstrip("#")
    fragment = fragment.lstrip("/")
    parts = unquote(fragment).split("/") if fragment else []

    for part in parts:
        part = part.replace("~1", "/").replace("~0", "~")

        if isinstance(document, Sequence):
            # Array indexes should be turned into integers
            try:
                part = int(part)
            except ValueError:
                pass
        try:
            document = document[part]
        except (TypeError, LookupError):
            raise RefResolutionError(
                "Unresolvable JSON pointer: %r" % fragment
            )

    return document


class Form:
    def __init__(self, json_schema, ui_schema):
        self.json_schema = json_schema
        self.ui_schema = ui_schema
        self.title = self.json_schema["title"]
        self.fields = []

    def process_scheme(self):
        self.fields = self.get_fields(self.json_schema, self.ui_schema)
        return self.fields

    def get_fields(self, json_schema, ui_schema):
        properties = json_schema.get("properties")
        assert json_schema["type"] == "object"
        required = set(json_schema.get("required", []))
        order = ui_schema.get("ui:order", [])
        order = {name: i for i, name in enumerate(order)}
        fields = []
        for field, data in properties.items():
            f = Field(field, data, json_schema)
            fields.append(f)
            if f.name in required:
                f.required = True

            ui_ext = ui_schema.get(f.name)
            if ui_ext:
                f.update_ext(ui_ext)

        fields.sort(key=lambda f: order.get(f.name, 10000))
        diff = set(order.keys()) - {f.name for f in fields}
        print("++++++++++++++++++++++++++++++++++++++++++++++++++", self.title, len(order), len(fields), diff)
        return fields

    def _rec_yaml(self, fields):
        x = CommentedMap()
        x.yaml_set_start_comment(f'{self.title}\n------------------------------------------')
        for f in fields:
            if f.type == "object":
                d = self._rec_yaml(f.subfields)
                print("##", f.name, f.subfields, d)
                x[f.name] = d
                d.yaml_set_start_comment("zzzzzzzzzzzzzzzzzz")
                pass
            else:
                x[f.name] = f
                comment = f.get_yaml_comment()
                if comment:
                    x.yaml_set_comment_before_after_key(f.name, before=comment)
                    # x.yaml_add_eol_comment(comment, f.name, column=15)
        return x

    def convert_to_yaml_struct(self):
        return self._rec_yaml(self.fields)

    @staticmethod
    def yaml_representer(dumper, data, flow_style=False):
        assert isinstance(dumper, ruamel.yaml.RoundTripDumper)
        return dumper.represent_dict(data.convert_to_yaml_struct())


def main():
    ruamel.yaml.RoundTripDumper.add_representer(Field, Field.yaml_representer)
    ruamel.yaml.RoundTripDumper.add_representer(Form, Form.yaml_representer)

    with logbook.FileHandler("productlist.log"):
        token = get_user_token("portal_admin", "portal_admin")
        client = ProductCatalogClient("http://dev-kong-service.apps.d0-oscp.corp.dev.vtb/product-catalog", token)
        widgets = Counter()
        fields = Counter()
        for p in client.products.list(is_open='true'):
            graph = client.graphs.get(p.creating_graph_id)
            from pprint import pprint

            print("============================", graph.json_schema["title"])
            pprint(graph.json_schema)
            print("-----------------------------------------------")
            pprint(graph.ui_schema)


            # print("##################", graph.json_schema["title"])
            # form = Form(graph.json_schema, graph.ui_schema)
            # fields = form.process_scheme()
            # for field in fields:
            #     print(field)

            # dumper = RoundTripDumper
            # dumper.comment_handling = None
            # ruamel.yaml.round_trip_dump(form, sys.stdout, Dumper=dumper)
            #
            # asdfasdf
            # ui_schema = graph.ui_schema
            # for name, field, widget in scan_ui_schema(ui_schema):
            #     if widget:
            #         widgets[widget] += 1
            #     if field:
            #         fields[field] += 1





# http://dev-kong-service.apps.d0-oscp.corp.dev.vtb/product-catalog/graphs/4735c177-a66c-4184-9bc4-cafec0a69de6/?version=1.0.14



if __name__ == "__main__":
    main()

