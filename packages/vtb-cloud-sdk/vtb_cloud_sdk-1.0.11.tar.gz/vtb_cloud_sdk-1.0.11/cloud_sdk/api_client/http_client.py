import posixpath
import requests


class BaseHttpClient:
    def __init__(self, url, ssl_verify):
        self.base_url = url
        self.ssl_verify = ssl_verify

    def make_url(self, url):
        return posixpath.join(self.base_url, url)

    def get(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        raise NotImplementedError()

    def post(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        raise NotImplementedError()

    def put(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        raise NotImplementedError()

    def patch(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        raise NotImplementedError()

    def delete(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        raise NotImplementedError()

    def close(self):
        pass


class RequestHttpClient(BaseHttpClient):
    def __init__(self, url, ssl_verify):
        super().__init__(url, ssl_verify=ssl_verify)
        self.session = requests.Session()
        self.session.verify = ssl_verify

    def get(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        return self.session.get(url=self.make_url(url), data=data, json=json,
                                headers=headers, params=params, timeout=timeout)

    def post(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        return self.session.post(url=self.make_url(url), data=data, json=json,
                                 headers=headers, params=params, timeout=timeout)

    def put(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        return self.session.put(url=self.make_url(url), data=data, json=json,
                                headers=headers, params=params, timeout=timeout)

    def patch(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        return self.session.patch(url=self.make_url(url), data=data, json=json,
                                  headers=headers, params=params, timeout=timeout)

    def delete(self, url, data=None, json=None, headers=None, params=None, timeout=None):
        return self.session.delete(url=self.make_url(url), data=data, json=json,
                                   headers=headers, params=params, timeout=timeout)

    @property
    def headers(self):
        return self.session.headers

    def close(self):
        self.session.close()
