import functools
import os
import attrdict
from typing import Dict
from cloud_sdk.calculator_client import CalculatorClient
from cloud_sdk.authorizer_client import AuthorizerClient
from cloud_sdk.order_service import OrderServiceClient
from cloud_sdk.portal import PortalClient
from cloud_sdk.references import ReferencesClient
from cloud_sdk.state_service_client import StateServiceClient
from cloud_sdk.product_catalog import ProductCatalogClient
from cloud_sdk.api_client.pool import ClientPool
from cloud_sdk.keycloak_token import KeyCloakToken


class SdkServiceError(Exception):
    pass


class CloudSdk:
    def __init__(self, config):
        self.config = config

    def __str__(self):
        return "<CloudSDK>"

    @classmethod
    def get_default_config(cls):
        return {
                "ssl_verify": False,
                "timeout": 10,
                "url": ""
        }

    @classmethod
    def get_env_config(cls, config=None) -> Dict[str, str]:
        services = ("calculator", "authorizer", "keycloak", "state_service", "product_catalog", "portal")
        prefixes = tuple(service.upper() + "_" for service in services)
        default_config = cls.get_default_config()

        config = config or {}
        for service_name in services:
            cfg = config.get(service_name)
            if cfg is None:
                config[service_name] = default_config.copy()
            else:
                for k, v in default_config.items():
                    cfg.setdefault(k, v)

        for name, value in os.environ.items():
            for service_prefix, service_name in zip(prefixes, services):
                if name.startswith(service_prefix):
                    parameter = name[len(service_prefix):].lower()
                    config[service_name][parameter] = value

        return attrdict.AttrDict(config)

    def _get_calculator_client_pool(self):
        config = self.config.calculator
        url = config.url
        auth_token = self.config.calculator.token
        client_type = functools.partial(CalculatorClient, url, auth_token,
                                        ssl_verify=config.ssl_verify,
                                        timeout=config.timeout)
        return ClientPool(client_type)

    def _get_authorizer_client_pool(self):
        config = self.config.authorizer
        client_type = functools.partial(AuthorizerClient, config.url,
                                        ssl_verify=config.ssl_verify,
                                        timeout=config.timeout)

        return ClientPool(client_type)

    def _get_state_service_client_pool(self):
        config = self.config.state_service
        url = config.url
        auth_token = config.token
        client_type = functools.partial(StateServiceClient, url, auth_token,
                                        ssl_verify=config.ssl_verify,
                                        timeout=config.timeout)

        return ClientPool(client_type)

    def _get_product_catalog_client_pool(self):
        config = self.config.product_catalog
        url = config.url
        auth_token = config.token
        client_type = functools.partial(ProductCatalogClient, url, auth_token,
                                        ssl_verify=config.ssl_verify,
                                        timeout=config.timeout)

        return ClientPool(client_type)

    def _get_order_service_client_pool(self):
        config = self.config.order_service
        url = config.url
        client_type = functools.partial(OrderServiceClient, url, "",
                                        ssl_verify=config.ssl_verify,
                                        timeout=config.timeout)

        return ClientPool(client_type)

    def _get_portal_client_pool(self):
        config = self.config.portal
        url = config.url
        client_type = functools.partial(PortalClient, url, "",
                                        ssl_verify=config.ssl_verify,
                                        timeout=config.timeout)

        return ClientPool(client_type)

    def _get_references_client_pool(self):
        config = self.config.references
        url = config.url
        client_type = functools.partial(ReferencesClient, url, "",
                                        ssl_verify=config.ssl_verify,
                                        timeout=config.timeout)

        return ClientPool(client_type)

    @functools.cached_property
    def pool_calculator(self):
        return self._get_calculator_client_pool()

    @functools.cached_property
    def keycloak(self):
        return KeyCloakToken(self.config.keycloak)

    @functools.cached_property
    def pool_authorizer(self):
        return self._get_authorizer_client_pool()

    @functools.cached_property
    def pool_state_service(self):
        return self._get_state_service_client_pool()

    @functools.cached_property
    def pool_product_catalog(self):
        return self._get_product_catalog_client_pool()

    @functools.cached_property
    def pool_order_service(self):
        return self._get_order_service_client_pool()

    @functools.cached_property
    def pool_portal_service(self):
        return self._get_portal_client_pool()

    @functools.cached_property
    def pool_references_service(self):
        return self._get_references_client_pool()
