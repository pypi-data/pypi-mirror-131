import time
from keycloak import KeycloakOpenID, KeycloakGetError
from cloud_sdk.logger import log


class KeyCloakToken:
    def __init__(self, config):
        self._client = None
        self._config = config

        self._token = None
        self._access_token = None
        self._access_token_expired_at = 0
        self._refresh_token = None
        self._refresh_token_expired_at = 0
        self.expiration_gap = 10

    def get_client(self):
        if not self._client:
            self._client = KeycloakOpenID(server_url=self._config.url,
                                          client_id=self._config.client_id,
                                          realm_name=self._config.realm_name,
                                          client_secret_key=self._config.client_secret_key)

        return self._client

    def _update_token(self):
        now = time.time()

        token = None
        if self._refresh_token_expired_at > now:
            try:
                token = self.get_client().refresh_token(self._refresh_token)
                log.debug("Keycloak token is refreshed")
            except KeycloakGetError as e:
                log.warning("Failed to refresh token: {}", e)

        if not token:
            token = self.get_client().token(grant_type="client_credentials")
            log.debug("New keycloak token is returned")

        now = time.time()
        self._access_token = token["access_token"]
        self._access_token_expired_at = now + token["expires_in"] - self.expiration_gap
        self._refresh_token = token["refresh_token"]
        self._refresh_token_expired_at = now + token["refresh_expires_in"] - self.expiration_gap
        return token

    def get_access_token(self):
        now = time.time()
        if self._access_token_expired_at > now:
            return self._access_token

        self._update_token()
        return self._access_token
