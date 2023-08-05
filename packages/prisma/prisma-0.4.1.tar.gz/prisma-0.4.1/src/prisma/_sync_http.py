from typing import Any

import httpx

from ._types import Method
from .http_abstract import AbstractResponse, AbstractHTTP


__all__ = ('HTTP', 'Response', 'client')


class HTTP(AbstractHTTP[httpx.Client, httpx.Response]):
    # pylint: disable=invalid-overridden-method,attribute-defined-outside-init

    session: httpx.Client

    def download(self, url: str, dest: str) -> None:
        with self.session.stream('GET', url, timeout=None) as resp:
            resp.raise_for_status()
            with open(dest, 'wb') as fd:
                for chunk in resp.iter_bytes():
                    fd.write(chunk)

    def request(self, method: Method, url: str, **kwargs: Any) -> 'Response':
        return Response(self.session.request(method, url, **kwargs))

    def open(self) -> None:
        self.session = httpx.Client()

    def close(self) -> None:
        if not self.closed:
            self.session.close()
            self.session = None  # type: ignore[assignment]

    def __del__(self) -> None:
        self.close()


client: HTTP = HTTP()


class Response(AbstractResponse[httpx.Response]):
    # pylint: disable=invalid-overridden-method

    @property
    def status(self) -> int:
        return self.original.status_code

    def json(self, **kwargs: Any) -> Any:
        return self.original.json(**kwargs)

    def text(self, **kwargs: Any) -> str:
        return self.original.content.decode(**kwargs)
