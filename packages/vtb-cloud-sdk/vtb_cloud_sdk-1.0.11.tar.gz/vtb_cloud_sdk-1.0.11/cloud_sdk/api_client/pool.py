import contextlib
from collections import deque
from functools import partial
from .base import BaseApiClient
from typing import Union, Type


class ClientPool:
    def __init__(self, client_type: Type[BaseApiClient]):
        self._pool = deque()
        self._active = 0
        self._client_type = client_type

    def __str__(self):
        return f"<Pool {self._client_type} size: {len(self._pool)}, in_use: {self._active}>"

    def _get_client(self) -> BaseApiClient:
        if self._pool:
            return self._pool.pop()
        return self._client_type()

    @contextlib.contextmanager
    def get(self):
        connection = self._get_client()
        self._active += 1
        try:
            yield connection
        finally:
            self._active -= 1
            self._pool.append(connection)

    def close(self):
        while self._pool:
            client = self._pool.pop()
            client.close()
