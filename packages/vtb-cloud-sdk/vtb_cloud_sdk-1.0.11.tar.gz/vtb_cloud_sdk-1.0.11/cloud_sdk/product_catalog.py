from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode, Resource, ResourceListDjango
from cloud_sdk.api_client import CRUD as _CRUD
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.auth import SDKAuthorizationToken


class ProductCatalogClientError(ApiClientError):
    pass


class CRUD(_CRUD):
    def url(self, resource_id=None, *parts):
        url = super().url(resource_id=resource_id, *parts)
        if not url.endswith("/"):
            url += "/"
        return url

    def get(self, resource_id):
        res = self.client.get(self.url(self.client.get_id(resource_id)))
        return self.resource_class(self, res)


class Product(Resource):
    id_field = "id"
    id = None


class ProductCrud(CRUD):
    resource_class = Product
    resource_url = "products/"
    resource_info = "product"
    json = True
    resource_list_class = ResourceListDjango


class Graph(Resource):
    id_field = "id"
    id = None


class GraphCrud(CRUD):
    resource_class = Graph
    resource_url = "graphs/"
    resource_info = "graph"
    json = True
    resource_list_class = ResourceListDjango


class ProductCatalogClient(BaseApiClient):
    name = 'pc_client'
    ClientError = ProductCatalogClientError

    def __init__(self, url, token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=SDKAuthorizationToken(token), mode=mode)
        self.products = ProductCrud(self)
        self.graphs = GraphCrud(self)
