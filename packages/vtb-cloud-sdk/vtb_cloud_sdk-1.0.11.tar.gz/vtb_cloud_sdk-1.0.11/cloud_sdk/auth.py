from cloud_sdk.api_client.auth import BearTokenBaseAuthorization


class SDKAuthorizationToken(BearTokenBaseAuthorization):
    def __init__(self, token):
        self._token = token

    def authorize(self, client, headers, **kwargs):
        token = kwargs.pop("token", None)
        if token:
            self._token = token
        super().authorize(client, headers, **kwargs)

    def get_token(self):
        return self._token
