import datetime

from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode
from cloud_sdk.api_client.auth import TokenBaseAuthorization
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.api_client.service import Service


class CalculatorClientError(ApiClientError):
    pass


def dt_format_minute(dt: datetime.datetime):
    return dt.strftime("%Y-%m-%dT%H:%M")


class OrderService(Service):
    service_name = "orders"

    def get_order(self, order_id):
        return self.client.get(self.url(order_id))

    def list_orders(self, from_: datetime.datetime, to: datetime.datetime, account_id=None):
        query_params = {"to": dt_format_minute(to), "from": dt_format_minute(from_)}
        if account_id:
            query_params["account_id"] = account_id
        return self.client.get(self.url(), query_params=query_params)

    def get_total(self, from_: datetime.datetime, to: datetime.datetime, account_id=None):
        query_params = {"to": dt_format_minute(to), "from": dt_format_minute(from_)}
        if account_id:
            query_params["account_id"] = account_id
        return self.client.get(self.url("total"), query_params=query_params)["total"]

    def cost(self, account_id):
        query_params = {"account_id": account_id}
        return self.client.get(self.url("cost"), query_params=query_params)["cost"]


class CalculatorAuthorization(TokenBaseAuthorization):
    TOKEN_PREFIX = "Token "

    def __init__(self, token):
        super().__init__()
        self._token = token

    def get_token(self):
        return self._token


class CalculatorClient(BaseApiClient):
    name = 'calc_client'
    ClientError = CalculatorClientError

    def __init__(self, url, token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=CalculatorAuthorization(token), mode=mode)
        self.orders = OrderService(self)
