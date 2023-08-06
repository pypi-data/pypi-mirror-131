import datetime
from typing import Optional
from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode, make_params, CRUD, \
    Resource, ResourceListDjango
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.api_client.service import Service
from cloud_sdk.api_client.utils import datetime_to_str
from cloud_sdk.auth import SDKAuthorizationToken


class StateServiceClientError(ApiClientError):
    pass


class ActionService(Service):
    service_name = "actions"

    def change_folders_account(self, event_dt: datetime.datetime, account_id, folders):
        json = make_params(event_dt=event_dt.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                           account_id=account_id, folders=folders)
        return self.client.post(self.url("change_folders_account/"), json=json)


class Event(Resource):
    TIME_FIELDS = ("created_row_dt", "create_dt")
    created_row_dt = None
    create_dt = None
    order_id = None
    action_id = None
    graph_id = None
    type = None
    vm = None
    subtype = None
    config = None
    status = None
    data = None
    item_id = None
    update_data = None


class EventCrud(CRUD):
    resource_class = Event
    resource_url = "events/"
    resource_info = "event"
    resource_list_class = ResourceListDjango
    json = True

    def create(self, order_id, item_id, action_id, graph_id, type, subtype, **kwargs):
        json = make_params(order_id=str(order_id),
                           item_id=str(item_id),
                           action_id=str(action_id),
                           graph_id=str(graph_id),
                           type=type,
                           subtype=subtype)
        json.update(kwargs)
        res = self.client.post(self.url(), json=json)
        resource = Event(self, res)
        return resource

    def update_config(self, item_id, order_id, updates, external_event=None,
                      create_dt: Optional[datetime.datetime] = None):
        json = make_params(item_id=str(item_id), order_id=str(order_id), updates=updates,
                           create_dt=datetime_to_str(create_dt, microseconds=True) if create_dt else None,
                           external_event=external_event)

        return self.client.post(self.url("update-config/"), json=json)


class StateServiceClient(BaseApiClient):
    name = 'state_service_client'
    ClientError = StateServiceClientError

    def __init__(self, url, token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=SDKAuthorizationToken(token), mode=mode)
        self.actions = ActionService(self)
        self.events = EventCrud(self)
