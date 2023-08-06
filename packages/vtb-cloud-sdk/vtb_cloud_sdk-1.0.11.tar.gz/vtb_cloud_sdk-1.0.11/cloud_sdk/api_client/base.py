import requests
import contextlib
import uuid
from typing import Union
from cloud_sdk.logger import log
from .auxiliary import response_pretty
from .error import ApiClientError
from .http_client import BaseHttpClient
from .auth import BaseAuthorization


_default_stub = object()


def _replacement(current, new):
    return current if new is _default_stub else new


class _ExpectStatus:
    text = None

    def check(self, status_code):
        return False


class ExpectStatus20X(_ExpectStatus):
    text = "20X"

    def check(self, status_code):
        return 200 <= status_code < 300


class ExpectStatus(_ExpectStatus):
    def __init__(self, expected):
        self._expected = expected

    @property
    def text(self):
        return str(self._expected)

    def check(self, status_code):
        return status_code == self._expected


class ExpectStatusOneOf(_ExpectStatus):
    def __init__(self, expected):
        self._expected = expected

    @property
    def text(self):
        return f"one of {self._expected}"

    def check(self, status_code):
        return status_code in self._expected


class ApiClientMode:
    __slots__ = ["raw_response", "timeout", "json_response", "expect_status", "log_level", "warning_log_level",
                 "auth_required"]

    def __init__(self, raw_response=False, timeout=None, json_response=True, expect_status_code=ExpectStatus20X(),
                 log_level="INFO", warning_log_level="WARNING", auth_required=True):
        self.raw_response = raw_response
        self.timeout = timeout
        self.json_response = json_response
        self.expect_status = expect_status_code
        self.log_level = log_level
        self.warning_log_level = warning_log_level
        self.auth_required = auth_required

    def __str__(self):
        return f"<Mode: timeout: {self.timeout}, auth_required: {self.auth_required}, log_level: {self.log_level}>"

    def replace(self, raw_response=_default_stub, timeout=_default_stub, json_response=_default_stub,
                expect_status_code=_default_stub, log_level=_default_stub, auth_required=_default_stub):
        new_mode = ApiClientMode(
            raw_response=_replacement(self.raw_response, raw_response),
            timeout=_replacement(self.timeout, timeout),
            json_response=_replacement(self.json_response, json_response),
            expect_status_code=_replacement(self.expect_status, expect_status_code),
            log_level=_replacement(self.log_level, log_level),
            auth_required=_replacement(self.auth_required, auth_required)
        )
        return new_mode


class BaseApiClient:
    name = None
    ClientError = ApiClientError

    def __init__(self, raw_http_client: BaseHttpClient, authorizer: BaseAuthorization, mode: ApiClientMode = None):
        self._session_authorized = False
        self._raw_http_client = raw_http_client
        self._authorizer = authorizer
        self._mode = mode or ApiClientMode()
        self._last_response = None
        self._request_headers = {}
        log.info("Created client: {} with auth: {}", self, authorizer)

    def __str__(self):
        return f"<{self._get_name()} {self._raw_http_client.base_url}>"

    def make_error(self, err, response):
        err_message = str(err) if err else None
        return self.ClientError(message=err_message, response=response)

    def _auth_request(self, method, url, query_params, data, json, headers):
        if self._mode.auth_required:
            self._authorizer.authorize_request(self, headers)

    def _get_name(self):
        return self.name or self.__class__.__name__

    def _pre_request(self, method, url, query_params, data, json, headers):
        self._auth_request(method, url, query_params, data, json, headers)

    def _request_(self, method, url, query_params, data, json, headers):
        try:
            return method(url, data=data, json=json, headers=headers, params=query_params, timeout=self._mode.timeout)
        except requests.exceptions.RequestException as err:
            log.warning("Failed request to {} {} {}: {}", self._get_name(), url, data, err)
            raise self.make_error(err, None)
        finally:
            self._request_headers = {}

    def _request(self, method, url, *, query_params=None, data=None, json=None, headers=None):
        assert url
        if not headers:
            headers = {}
        self._pre_request(method, url, query_params, data, json, headers)

        response = self._request_(method, url, query_params, data, json, headers, )

        method_name = response.request.method.upper()
        status_code = response.status_code

        def _log(log_level, message, log_response, **kwargs):
            query_str = " query: {query_params} " if query_params else ""
            data_str = " data: {data}" if data else ""
            response_fmt = "{method} {url}%s%s: [{status}] {response}" % (query_str, data_str)
            message = message.replace("#", response_fmt)
            logger = getattr(log, log_level.lower())
            logger(message, method=method_name, url=url, query_params=query_params, data=data or json,
                   status=status_code, response=log_response, **kwargs)

        if not self._mode.expect_status.check(status_code):
            _log("warning", "Wrong status of #. expected: {expected}", response_pretty(response.text),
                 expected=self._mode.expect_status.text)
            raise self.make_error(f"Wrong status code [{status_code}]", response=response)

        self._last_response = response

        try:
            _log(self._mode.log_level, "Response #", response.text)
            if self._mode.json_response:
                return_response = {} if response.status_code == 204 else response.json()
            elif self._mode.raw_response:
                return_response = response
            else:
                return_response = response.text

            return return_response
        except (ValueError, TypeError) as err:
            _log(self._mode.warning_log_level, "Failed json of the response #. Error: {error}",
                 response_pretty(response.text), error=err)
            raise self.make_error(f"Wrong response '{err}'", response=response)

    def get(self, url, query_params=None, headers=None):
        return self._request(self._raw_http_client.get, url, query_params=query_params, headers=headers)

    def post(self, url, data=None, query_params=None, json=None, headers=None):
        return self._request(self._raw_http_client.post, url, query_params=query_params,
                             data=data, json=json, headers=headers)

    def put(self, url, data=None, query_params=None, json=None, headers=None):
        return self._request(self._raw_http_client.put, url, query_params=query_params,
                             data=data, json=json, headers=headers)

    def delete(self, url, query_params=None, headers=None):
        return self._request(self._raw_http_client.delete, url, query_params=query_params, headers=headers)

    def auth(self, **kwargs):
        return self._authorizer.authorize(self, headers={}, **kwargs)

    @contextlib.contextmanager
    def replace_mode(self, raw_response=_default_stub, timeout=_default_stub, json_response=_default_stub,
                     expect_status_code=_default_stub, mode: ApiClientMode = None, auth_required=None):
        current = self._mode
        if mode:
            self._mode = mode
        else:
            self._mode = self._mode.replace(raw_response=raw_response, timeout=timeout, json_response=json_response,
                                            expect_status_code=expect_status_code, auth_required=auth_required)
        try:
            yield
        finally:
            self._mode = current

    @property
    def last_response(self):
        return self._last_response

    def get_id(self, resource, id_name=None) -> Union[int, None, uuid.UUID]:
        from .resource import Resource

        if resource is None:
            return None
        if isinstance(resource, int):
            return resource
        if isinstance(resource, uuid.UUID):
            return resource
        if isinstance(resource, Resource):
            return resource.id
        if isinstance(resource, dict):
            if id_name:
                return resource[id_name]
            ids = [key for key in resource.keys() if key.endswith("_id") or key.endswith("_uid")]
            if len(ids) == 1:
                return resource[ids[0]]
            assert False, "can't determinate id field in dict %s" % resource

        return resource

    def close(self):
        self._raw_http_client.close()
