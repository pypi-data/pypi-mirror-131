from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode, DEFAULT, CRUD, Resource, \
    ResourceListDjango, make_params
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.auth import SDKAuthorizationToken


class ReferenceClientError(ApiClientError):
    pass


class Page(Resource):
    id_field = "name"
    id = None
    name = None
    data = None
    directory = None


class PagesCRUD(CRUD):
    resource_url = "api/v1/pages/"
    resource_list_class = ResourceListDjango
    resource_class = Page

    def list(self, tags=DEFAULT, directory__name=DEFAULT, **kwargs):
        params = make_params(tags=tags, directory__name=directory__name)
        params.update(kwargs)
        res = self.client.get(self.url(), query_params=params)
        res = [Page(self, page) for page in res]
        return res


class ReferencesClient(BaseApiClient):
    name = 'portal'
    ClientError = ReferenceClientError

    def __init__(self, url, token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=SDKAuthorizationToken(token), mode=mode)
        self.pages = PagesCRUD(self)

    def health(self):
        return self.get("api/v1/health")

