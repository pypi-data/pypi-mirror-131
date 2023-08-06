import posixpath

from cloud_sdk.api_client import BaseApiClient
from cloud_sdk.api_client.utils import parse_date, datetime_to_str
from cloud_sdk.api_client.auxiliary import DEFAULT, make_params


class Resource:
    id_field = "id"
    TIME_FIELDS = None
    SKIP_SET = tuple()

    def __init__(self, crud, info):
        self._crud = crud
        self._update_fields(info)

    def _update_fields(self, fields):
        self._info = fields
        if self.TIME_FIELDS:
            for field in self.TIME_FIELDS:
                v = fields.get(field)
                if v is not None:
                    fields[field] = parse_date(v)

        for k, v in fields.items():
            if k not in self.SKIP_SET:
                setattr(self, k, v)

    def __str__(self):
        return "<{} {}>".format(self.__class__.__name__, self._info)

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self._info == other._info

    def update(self, **kwargs):
        """Update resource fields"""
        updated = self._crud.update(self.id, **kwargs)
        self._update_fields(updated._info)

    def delete(self, **params):
        """Delete resources"""
        result = self._crud.delete(self.id, **params)
        return result

    def reload(self):
        """Reload resource info"""
        updated = self._crud.get(self.id)
        self._update_fields(updated._info)
        return self

    get = reload  # TODO do we need this?

    @property
    def id(self):
        return self._info[self.id_field]


class WrapIterator:
    def __init__(self, items, wrap):
        self._items = items
        self._wrap = wrap

    def __iter__(self):
        for item in self._items:
            yield self._wrap(item)


class ResourceList:

    def __init__(self, crud, info, original_filters):
        self._crud = crud
        self._info = info
        self._original_filters = original_filters

    @property
    def total(self):
        """Total number of items. Only at the moment of first query"""
        return self._info["meta"]["total_count"]

    def __getitem__(self, index):
        return self._wrap(self._info["list"][index])

    def __len__(self):
        return self.total

    def __bool__(self):
        return bool(self.total)

    def __str__(self):
        return "<List %s. Total: %s>" % (self._crud.resource_class.__name__, self.total)

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, ResourceList):
            return False

        if other.total != self.total:
            return False
        for it, it2 in zip(self, other):
            if it != it2:
                return False
        return True

    # TODO more robust pagination handling
    def __iter__(self):
        global_index = 0
        index = 0
        info = self._info
        meta = info["meta"]
        page = meta["page"]

        while global_index < self.total:
            if index < len(info["list"]):
                yield self._wrap(info["list"][index])
                index += 1
                global_index += 1
            else:
                index = 0
                page += 1
                kwargs = self._original_filters
                kwargs["page"] = page
                info = self._crud.list(dont_wrap=True, **kwargs)

    def _wrap(self, item):
        return self._crud.resource_class(self._crud, item)

    @property
    def page_size(self):
        return len(self._info["list"])

    @property
    def page_items(self):
        return WrapIterator(self._info["list"], self._wrap)


class ResourceListDjango(ResourceList):
    list_field_name = "list"

    def __init__(self, crud, info, original_filters):
        self._crud = crud
        self._info = info
        self._original_filters = original_filters

    def __iter__(self):
        global_index = 0
        index = 0
        info = self._info
        page = 1

        while global_index < self.total:
            items = info[self.list_field_name]
            if not items:
                break
            if index < len(items):
                yield self._wrap(items[index])
                index += 1
                global_index += 1
            else:
                index = 0
                page += 1
                kwargs = self._original_filters
                kwargs["page"] = page
                info = self._crud.list(dont_wrap=True, **kwargs)


class CRUD:
    resource_info = None
    resource_list = None
    resource_url = None
    resource_class = Resource
    resource_list_class = ResourceList
    json = False
    tail_slash = False

    def __init__(self, client: BaseApiClient):
        assert self.resource_url is not None, "please specify resource_url for %s" % self
        self.client = client

    def url(self, resource_id=None, *parts):
        url = self.resource_url
        if resource_id:
            if url[-1] != "/":
                url += "/"
            url += str(resource_id)
        if parts:
            if url[-1] != "/":
                url += "/"
            url += "/".join(parts)
        if self.tail_slash and url[-1] != "/":
            url += "/"
        return url

    def create(self, **kwargs):
        data = None
        json = None
        if self.json:
            json = kwargs
        else:
            data = kwargs
        res = self.client.post(self.url(), data=data, json=json)
        resource = self.resource_class(self, res[self.resource_info])
        return resource

    def list(self, dont_wrap=False, per_page=DEFAULT, page=DEFAULT, **kwargs):
        params = make_params(page=page, per_page=per_page)
        kwargs.update(params)
        res = self.client.get(self.url(), query_params=kwargs)
        if self.resource_list:
            res = res[self.resource_list]
        if not dont_wrap:
            res = self.resource_list_class(self, res, kwargs)
        return res

    def get(self, resource_id):
        res = self.client.get(self.url(self.client.get_id(resource_id)))
        return self.resource_class(self, res[self.resource_info])

    def delete(self, resource_id, **kwargs):
        return self.client.delete(self.url(resource_id), query_params=kwargs)

    def update(self, resource_id, **kwargs):
        data = None
        json = None

        for field in self.resource_class.TIME_FIELDS or tuple():
            if field in kwargs:
                kwargs[field] = datetime_to_str(kwargs[field])

        if self.json:
            json = kwargs
        else:
            data = kwargs

        res = self.client.put(self.url(resource_id), json=json, data=data)
        if self.resource_info:
            resource = self.resource_class(self, res[self.resource_info])
            return resource
        return res


class SubResourceCRUD(CRUD):
    def __init__(self, client, main_crud, resource_id, sub_parts=None):
        super().__init__(client)
        self.main_crud = main_crud
        self.main_resource_id = resource_id
        self.sub_parts = sub_parts or tuple()

    def url(self, resource_id=None, *parts):
        url = self.main_crud.url(self.main_resource_id)
        url = posixpath.join(url, self.resource_url, *self.sub_parts) + "/"
        if resource_id:
            url += str(resource_id) + "/"
        if parts:
            url += "/".join(parts) + "/"
        return url


class ResourceService:
    service_name = None

    def __init__(self, resource):
        self.resource = resource
        self.client = resource._crud.client

    def url(self, *parts):
        return self.resource._crud.url(self.resource.id, self.service_name, *parts)
