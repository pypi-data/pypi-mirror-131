import functools


class ApiClientError(IOError):
    def __init__(self, *, response=None, message=None, **kwargs):
        super().__init__()

        self._response = response
        self._message = message
        self.status_code = response.status_code if response is not None else None
        self.kwargs = kwargs

    def __str__(self):
        return f"<ResponseError {self.status_code} - {self.code or ''}: {self.message} {self.json}>"

    @functools.cached_property
    def json(self):
        if self.content_type != "application/json":
            return None
        return self._response.json()

    @property
    def content_type(self):
        if self._response is not None:
            return self._response.headers["content-type"]
        else:
            return None

    @property
    def url(self):
        return self._response.url

    @property
    def code(self):
        json = self.json
        return json.get("code") if json else None

    @property
    def response(self):
        return self._response

    @property
    def message(self):
        if self._message:
            return self._message
        json = self.json
        if not json:
            return None

        return json.get("message") or json.get("detail")
