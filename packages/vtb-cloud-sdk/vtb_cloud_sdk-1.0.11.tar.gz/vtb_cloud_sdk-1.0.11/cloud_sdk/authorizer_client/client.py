import enum

from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode, CRUD, Resource, DEFAULT, \
    ResourceListDjango
from cloud_sdk.api_client.auth import TokenBaseAuthorization
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.api_client.service import Service


class AuthorizerClientError(ApiClientError):
    pass


class Folder(Resource):
    id_field = "name"
    name = None
    title = None
    type = None
    parent = None
    kind = None
    children_count = None

    def ancestors(self):
        folders = self._crud.client.get(self._crud.url(self.id, "ancestors"))["data"]
        return [Folder(self._crud, folder) for folder in folders]

    def get_children(self):
        folders = self._crud.client.get(self._crud.url(self.id, "children"))["data"]
        return [Folder(self._crud, folder) for folder in folders]

    def get_policy(self):
        return self._crud.client.get(self._crud.url(self.id, "policy"))["data"]

    def get_projects(self):
        projects = self._crud.client.get(self._crud.url(self.id, "projects"))["data"]
        return [Project(ProjectsCRUD(self._crud.client), project) for project in projects]


class Organization(Resource):
    id_field = "name"
    name = None
    title = None
    description = None
    created_at = None
    updated_at = None
    TIME_FIELDS = frozenset(("created_at", "updated_at"))

    def get_children(self):
        folders = self._crud.client.get(self._crud.url(self.id, "children"))["data"]
        return [Folder(FolderCRUD(self._crud.client), folder) for folder in folders]

    def get_policy(self):
        return self._crud.client.get(self._crud.url(self.id, "policy"))["data"]


class ResourceListData(ResourceListDjango):
    list_field_name = "data"


class OrganizationCRUD(CRUD):
    resource_url = "api/v1/organizations"
    resource_list_class = ResourceListData
    resource_class = Organization
    resource_info = "data"

    def list(self,  per_page=DEFAULT, page=DEFAULT, include=DEFAULT, **kwargs):
        return super().list(per_page=per_page, page=page, include="total_count" if include is DEFAULT else include)


class FolderCRUD(CRUD):
    resource_url = "api/v1/folders"
    resource_info = "data"

    def available_types(self, parent_type):
        return self.client.get(self.url("available_types"), query_params={"parent_type": parent_type})


class Project(Resource):
    id_field = "name"
    name = None
    title = None
    description = None
    disable_rollback = None
    organization = None
    folder = None
    information_system_id = None
    project_environment_id = None
    environment_prefix_id = None
    created_at = None
    updated_at = None
    TIME_FIELDS = frozenset(("created_at", "updated_at"))

    def get_policy(self):
        return self._crud.client.get(self._crud.url(self.id, "policy"))["data"]

    def ancestors(self):
        folders = self._crud.client.get(self._crud.url(self.id, "ancestors"))["data"]
        return [Folder(self._crud, folder) for folder in folders]


class ProjectsCRUD(CRUD):
    resource_url = "api/v1/projects"
    resource_info = "data"


class Permission(enum.Enum):
    folder_create = "authorizer:folders:create"
    folder_get = "authorizer:folders:get"
    organization_create = "authorizer:organizations:create"


class PermissionService(Service):
    service_name = "api/v1/permissions"

    def test(self, resource, permission):
        if isinstance(permission, Permission):
            permission = permission.value
        json = {"permissions": [permission],
                "resource": resource}
        allowed_permissions = self.client.post(self.url("test"), json=json)["data"]["permissions"]
        return permission in allowed_permissions


class AuthorizerAuthorization(TokenBaseAuthorization):
    TOKEN_PREFIX = "bearer "

    def __init__(self, token=None):
        super().__init__()
        self._token = token

    def authorize(self, client, headers, token=None, **kwargs):
        if token:
            self._token = token
        super().authorize(client, headers, **kwargs)
        token = self.get_token()
        headers[self.HEADER] = f"{self.TOKEN_PREFIX}{token}"

    def get_token(self):
        assert self._token
        return self._token


class AuthorizerClient(BaseApiClient):
    name = 'auth_client'
    ClientError = AuthorizerClientError

    def __init__(self, url, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=AuthorizerAuthorization(), mode=mode)
        self.organizations = OrganizationCRUD(self)
        self.folders = FolderCRUD(self)
        self.projects = ProjectsCRUD(self)
        self.permissions = PermissionService(self)

    def get_version(self):
        return self.get("api/v1/version")
