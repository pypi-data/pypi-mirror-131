from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode, ResourceListDjango, make_params, DEFAULT
from cloud_sdk.api_client.auth import BearTokenBaseAuthorization
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.api_client.service import Service, ListService


class OrderServiceClientError(ApiClientError):
    @property
    def error_code(self):
        json = self.json
        if not json:
            return None
        if not isinstance(json, dict):
            return None

        error = json.get("error", {})
        code = error.get("code")
        return code


class OrderServiceAuthorization(BearTokenBaseAuthorization):
    def __init__(self, token):
        self._token = token

    def authorize(self, client, headers, **kwargs):
        token = kwargs.pop("token", None)
        if token:
            self._token = token
        super().authorize(client, headers, **kwargs)

    def get_token(self):
        return self._token


class ServiceResourceList(ResourceListDjango):
    def _wrap(self, item):
        return item


class DataCenters(ListService):
    service_name = "api/v1/data_centers"


class NetSegments(ListService):
    service_name = "api/v1/net_segments"


class Platforms(ListService):
    service_name = "api/v1/platforms"


class Domains(ListService):
    service_name = "api/v1/domains"


class ResourcePools(ListService):
    service_name = "api/v1/products/resource_pools"

    def quota_flat(self, quota: dict):
        def rec(d, prefix):
            for name, value in d.items():
                if isinstance(value, dict):
                    yield from rec(value, prefix=f"{prefix}[{name}]")
                else:
                    yield f"{prefix}[{name}]", value

        return dict(rec(quota, "quota"))

    # noinspection PyMethodOverriding
    def list(self, project_name, category, data_center=DEFAULT, quota: dict=DEFAULT):
        params = make_params(project_name=project_name, category=category, data_center=data_center)
        if quota is not DEFAULT:
            quota = self.quota_flat(quota)
            params.update(quota)
        return self.client.get(self.url(), query_params=params)["list"]


class OrderServiceClient(BaseApiClient):
    name = 'order_service'
    ClientError = OrderServiceClientError

    def __init__(self, url, token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=OrderServiceAuthorization(token), mode=mode)
        self.datacenters = DataCenters(self)
        self.net_segments = NetSegments(self)
        self.platforms = Platforms(self)
        self.domains = Domains(self)
        self.resource_pools = ResourcePools(self)

    def check_unique(self, field_name, field_value, project_name=DEFAULT, product_id=DEFAULT):
        params = make_params(field_name=field_name, field_value=field_value,
                             project_name=project_name, product_id=product_id)
        try:
            self.get("api/v1/orders/check_field_uniqueness", query_params=params)
            return True
        except OrderServiceClientError as e:
            print(e, e.status_code, e.error_code)
            if e.status_code == 422 and e.error_code == "field_value_already_used":
                return False
            raise
