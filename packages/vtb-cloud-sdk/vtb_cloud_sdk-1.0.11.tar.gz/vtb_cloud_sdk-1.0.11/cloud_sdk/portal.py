from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode, DEFAULT, CRUD, Resource, \
    ResourceListDjango
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.auth import SDKAuthorizationToken
from cloud_sdk.api_client.service import ListService, ServiceResourceListWithoutTotal


class PortalClientError(ApiClientError):
    pass


class Users(ListService):
    service_name = "api/v1/users"
    resource_list = ServiceResourceListWithoutTotal

    def list(self, q=DEFAULT, username=DEFAULT, project_environment_id=DEFAULT,
             domain=DEFAULT, project_name=DEFAULT,
             page=1, per_page=25, **kwargs):
        return super().list(page=page, per_page=per_page,
                            q=q, username=username, include=DEFAULT,
                            project_environment_id=project_environment_id, domain=domain,
                            project_name=project_name, **kwargs)


class AccessGroup(Resource):
    id_field = "id"
    id = None
    created_at = None
    updated_at = None
    name = None
    project_name = None
    description = None
    creator = None
    is_deleted = None
    domain = None
    group_dn = None


class AccessGroupCRUD(CRUD):
    resource_url = "_"
    resource_list_class = ResourceListDjango
    resource_class = AccessGroup


class Projects:
    def __init__(self, client, project_name):
        self.client = client
        self.project_name = project_name
        self.access_groups = AccessGroupCRUD(self.client)
        self.access_groups.resource_url = f"api/v1/projects/{self.project_name}/access_groups"


class PortalClient(BaseApiClient):
    name = 'portal'
    ClientError = PortalClientError

    def __init__(self, url, token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=SDKAuthorizationToken(token), mode=mode)
        self.users = Users(self)

    def version(self):
        return self.get("api/v1/version")["version"]

    def health(self):
        return self.get("api/v1/health")

    def logo(self):
        return self.get("api/v1/logo")

    def projects(self, project_name):
        return Projects(self, project_name)


