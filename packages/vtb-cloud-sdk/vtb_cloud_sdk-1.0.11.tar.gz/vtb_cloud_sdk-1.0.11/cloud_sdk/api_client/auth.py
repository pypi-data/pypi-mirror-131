import datetime
import jwt
from cloud_sdk.logger import log


class BaseAuthorization:
    def __init__(self, **kwargs):
        self._authorized = False

    def __str__(self):
        return f"<{self.__class__.__name__}>"

    def authorize(self, client, headers, **kwargs):
        pass

    def authorize_request(self, client, headers):
        if not self.is_authorized():
            self.authorize(client, headers)

    def is_authorized(self):
        return self._authorized

    def update_credential(self, **credential):
        pass


class WithoutAuthorization(BaseAuthorization):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._authorized = True


class BasicAuthorization(BaseAuthorization):
    def __init__(self, login, password):
        self.login = login
        self.password = password
        super().__init__()


class CredentialAuth(BaseAuthorization):
    def __init__(self, **credential):
        self._credential = credential
        self._auth_response = None
        super().__init__()

    def authorize(self, client, **kwargs):
        if kwargs:
            self.update_credential(**kwargs)
        response = client.post(self.auth_url(client), json=self._credential)
        self._authorized = True
        self._auth_response = response

    def auth_url(self, client):
        raise NotImplementedError()

    def update_credential(self, **credential):
        for key, value in credential.items():
            if value is not None:
                self._credential[key] = value
        self._authorized = False


class TokenBaseAuthorization(BaseAuthorization):
    HEADER = "Authorization"
    TOKEN_PREFIX = ""

    def __init__(self):
        super().__init__()

    def authorize(self, client, headers, **kwargs):
        super().authorize(client, headers, **kwargs)
        token = self.get_token()
        headers[self.HEADER] = f"{self.TOKEN_PREFIX}{token}"

    def authorize_request(self, client, headers):
        self.authorize(client, headers)

    def get_token(self):
        raise NotImplementedError()


class BearTokenBaseAuthorization(TokenBaseAuthorization):
    TOKEN_PREFIX = "Bearer "


class JwtBearTokenAuthorization(BearTokenBaseAuthorization):
    def __init__(self, private_key, algorithm='RS256', ttl=None, **payload):
        super().__init__()
        self.private_key = private_key
        self.payload = payload
        self.ttl = ttl
        self.algorithm = algorithm
        self.jwt_token = None
        self.jwt_token_expired = None

    def get_payload(self):
        now = datetime.datetime.utcnow()
        payload = self.payload.copy()
        payload["nbf"] = now
        payload["exp"] = now
        if self.ttl:
            payload["exp"] = now + datetime.timedelta(seconds=self.ttl)
        return payload

    def get_token(self):
        now = datetime.datetime.utcnow()
        if self.jwt_token and self.jwt_token_expired and self.jwt_token_expired > now:
            return self.jwt_token
        payload = self.get_payload()
        log.debug("Auth payload {}", payload)
        encoded = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        self.jwt_token = encoded.decode("ascii")
        self.jwt_token_expired = now + datetime.timedelta(seconds=self.ttl * 5 // 6 - 1)
        return self.jwt_token
