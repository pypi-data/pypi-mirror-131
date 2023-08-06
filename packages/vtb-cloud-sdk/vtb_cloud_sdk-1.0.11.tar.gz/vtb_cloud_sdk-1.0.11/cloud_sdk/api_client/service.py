from cloud_sdk.api_client import ResourceListDjango, make_params, DEFAULT


class Service:
    service_name = None

    def __init__(self, client):
        self.client = client
        assert self.service_name, "Service name should be initialized for each service"

    def url(self, *parts):
        url = self.service_name
        if parts:
            url += "/"
            url += "/".join(str(p) for p in parts)
        return url

    def get_id(self, resource, id_name=None):
        return self.client.get_id(resource, id_name=id_name)


class ServiceResourceList(ResourceListDjango):
    def __str__(self):
        return f"<List total items: {self.total}>"

    def _wrap(self, item):
        return item

    @property
    def total(self):
        return self._info["meta"]["total_count"]


class ServiceResourceListWithoutTotal(ServiceResourceList):
    def __str__(self):
        return f"<List {self.total}>"

    @property
    def total(self):
        return len(self._info)


class ListService(Service):
    service_name = None
    resource_list = ServiceResourceList

    def list(self, include="total_count", page=1, per_page=25, **kwargs):
        params = make_params(include=include, page=page, per_page=per_page)
        params.update((k, v) for k, v in kwargs.items() if v is not DEFAULT)
        res = self.client.get(self.url(), query_params=params)
        res = self.resource_list(self, res, params)
        return res
