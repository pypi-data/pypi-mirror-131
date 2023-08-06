import posixpath
import uuid

from cloud_sdk.api_client.resource import Resource, CRUD, ResourceList
from cloud_sdk.api_client import ApiClientError, BaseApiClient, Service, ApiClientMode
from cloud_sdk.api_client.auth import BearTokenBaseAuthorization
from cloud_sdk.api_client.http_client import RequestHttpClient
from typing import Union


class AccountManagerClientError(ApiClientError):
    pass


class UtilityService(Service):
    service_name = "api/v1/"

    def force_delete(self):
        return self.client.delete("_force_delete")["deleted"]

    def version(self):
        return self.client.get("/api/version")["deleted"]

    def check_exception(self):
        return self.client.get("/api/v1/check_exception")

    def health(self):
        return self.client.get("/api/v1/health")

    def currencies(self):
        return self.client.get("/api/v1/currencies")["currencies"]


class Account(Resource):
    id_field = "account_id"
    account_id = None

    def _update_fields(self, fields):
        super()._update_fields(fields)
        self.account_id = uuid.UUID(self.account_id)

    def list_transfers(self, transferred_at_le=None, transferred_at_lte=None,
                       transferred_at_ge=None, transferred_at_gte=None):
        crud = self._crud
        params = {"transferred_at_le": transferred_at_le,
                  "transferred_at_lte": transferred_at_lte,
                  "transferred_at_ge": transferred_at_ge,
                  "transferred_at_gte": transferred_at_gte,
                  }
        url = crud.url(self.id, "/transfers")
        res = self._crud.client.get(url, query_params=params)
        return ResourceList(TransferService, res, params)

    def tree_list(self):
        tree = self._crud.client.get(self._crud.url(self.id, "tree"))["tree"]
        for child in tree:
            child["account"] = Account(self._crud, child["account"])
        return tree

    def link(self, folder_uid):
        base_url, tail = posixpath.split(self._crud.base_resource_url)
        if not tail:
            base_url, tail = posixpath.split(base_url)

        url = posixpath.join(base_url, "folders", folder_uid, "accounts", self.id)
        self._crud.client.post(url)

    def unlink(self, folder_uid):
        base_url, tail = posixpath.split(self._crud.base_resource_url)
        if not tail:
            base_url, tail = posixpath.split(base_url)

        url = posixpath.join(base_url, "folders", folder_uid, "accounts", self.id)
        self._crud.client.delete(url)



class AccountCrud(CRUD):
    resource_class = Account
    resource_url = "api/v1/accounts/"
    resource_info = "account"
    json = True

    def get_bank_account(self, currency):
        account = self.client.get(self.url("bank", currency))["account"]
        return Account(self, account)

    def get_infrastructure_account(self, currency):
        account = self.client.get(self.url("infrastructure", currency))["account"]
        return Account(self, account)


class OrganizationAccountCrud(CRUD):
    resource_class = Account
    resource_url = "api/v1/organizations/"
    resource_info = "account"
    json = True

    def __init__(self, client: BaseApiClient, organization_uid):
        super().__init__(client)
        self.organization_uid = organization_uid
        self.base_resource_url = self.resource_url
        self.resource_url = posixpath.join(OrganizationAccountCrud.resource_url, organization_uid, "accounts")

    def create(self, name, parent, limit=0):
        json = {"name": name, "limit": limit, "parent_id": self.client.get_id(parent)}
        res = self.client.post(self.url(), json=json)
        resource = self.resource_class(self, res[self.resource_info])
        return resource

    def create_root(self, name, currency, limit=0):
        json = {"name": name, "limit": limit, "currency": currency}
        res = self.client.post(self.url("root"), json=json)
        resource = self.resource_class(self, res[self.resource_info])
        return resource

    def list_root(self):
        accounts = self.client.get(self.url("root"))["accounts"]
        accounts = [self.resource_class(self, account) for account in accounts]
        return accounts


class Transfer(Resource):
    pass


def format_money(money: Union[int, float, str]) -> str:
    if isinstance(money, int):
        return f"{money}.00"
    if isinstance(money, float):
        return f"{money:.2}"
    if isinstance(money, str):
        return money
    assert "Incorrect type for money"


class TransferService(Service):
    service_name = "/api/v1/organizations"
    resource_class = Transfer
    json = True

    def __init__(self, client: BaseApiClient, organization_uid):
        super().__init__(client)
        self.organization_uid = organization_uid
        self.service_name = posixpath.join(TransferService.service_name, organization_uid, "accounts")

    def make_transfer(self, from_account: Union[Account, str], to_account: Union[Account, str],
                      amount: Union[str, int, float], reason: str):
        json = {"from_account_id": self.get_id(from_account),
                "to_account_id": self.get_id(to_account),
                "amount": format_money(amount),
                "reason": reason}
        res = self.client.post(self.url("transfers"), json=json)
        resource = Transfer(self, res["transfer"])
        return resource


class FolderLinkService(Service):
    service_name = "/api/v1/folders"
    json = True

    def _make_account(self, info):
        account = info["account"]
        return Account(self.client.accounts(account["organization_uid"]), account)

    def link(self, folder_uid, account):
        account_uid = self.client.get_id(account, "account_id")
        info = self.client.post(self.url(folder_uid, "accounts", account_uid))
        return self._make_account(info)

    def unlink(self, folder_uid, account):
        account_uid = self.client.get_id(account, "account_id")
        info = self.client.delete(self.url(folder_uid, "accounts", account_uid))
        return self._make_account(info)

    def get(self, folder_uid):
        info = self.client.get(self.url(folder_uid, "accounts"))
        return self._make_account(info)


class FabricSubCRUD:
    def __init__(self, client, crud):
        self.client = client
        self._crud = crud

    def __call__(self, organization_uid):
        return self._crud(self.client, organization_uid)


class AccountManagerAuthorization(BearTokenBaseAuthorization):
    def __init__(self, token):
        super().__init__()
        self._token = token

    def get_token(self):
        return self._token



class AccountManagerClient(BaseApiClient):
    name = 'am_client'
    ClientError = AccountManagerClientError

    def __init__(self, url, *, auth_token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=AccountManagerAuthorization(auth_token),
                         mode=mode)
        self.accounts = FabricSubCRUD(self, OrganizationAccountCrud)
        self.admin_accounts = AccountCrud(self)
        self.folders = FolderLinkService(self)
        self.utility = UtilityService(self)
        self.transfers = FabricSubCRUD(self, TransferService)
