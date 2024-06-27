from typing import TypeVar, Generic, Mapping

import httpx

from ._constants import DEFAULT_TIMEOUT

HttpxClientT = TypeVar("HttpxClientT", bound=[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[HttpxClientT]):
    _client: HttpxClientT
    _base_url: httpx.URL

    _timeout: float | httpx.Timeout
    _custom_headers: Mapping[str, str]

    def __init__(
        self,
        *,
        base_url: str | httpx.URL,
        timeout: float | httpx.Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
    ) -> None:
        self._base_url = httpx.URL(base_url)
        self._timeout = timeout or DEFAULT_TIMEOUT
        self._custom_headers = custom_headers or {}

    def _enforce_trailing_slash(self, url: httpx.URL) -> httpx.URL:
        if url.raw_path.endswith(b"/"):
            return url
        return url.copy_with(raw_path=url.raw_path + b"/")

    def _prepare_url(self, url: str | httpx.URL) -> httpx.URL:
        merge_url = httpx.URL(url)
        if merge_url.is_relative_url:
            merge_raw_path = self.base_url.raw_path + merge_url.raw_path.lstrip(b"/")
            return self.base_url.copy_with(raw_path=merge_raw_path)
        return merge_url

    def _prepare_headers(
        self,
        headers: Mapping[str, str] | None = None
    ) -> dict[str, str]:
        pre_headers = headers or {}
        pre_headers.update({**self.default_headers, **self._custom_headers})
        return httpx.Headers(pre_headers)

    def _build_request(
        self,
        method: str,
        url: str | httpx.URL,
        **kwargs,
    ) -> httpx.Request:
        headers = self._prepare_headers(kwargs.get("headers"))
        return self._client.build_request(
            method=method,
            url=self._prepare_url(url),
            headers=headers,
            timeout=self._timeout,
            **kwargs,
        )

    @property
    def base_url(self) -> httpx.URL:
        return self._base_url

    @base_url.setter
    def base_url(self, url: str | httpx.URL) -> None:
        self._base_url = self._enforce_trailing_slash(
            url if isinstance(url, httpx.URL) else httpx.URL(url)
        )

    @property
    def auth_headers(self) -> dict[str, str]:
        return {}

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json,text/html;q=0.9",
            "Content-Type": "application/json",
            **self.auth_headers,
            **self._custom_headers,
        }


class SyncAPIClient(BaseClient[httpx.Client]):
    _client: httpx.Client

    def __init__(
        self,
        *,
        base_url: str | httpx.URL,
        timeout: float | httpx.Timeout | None = None,
        custom_headers: Mapping[str, str] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            custom_headers=custom_headers,
        )
        self._client = http_client or httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=custom_headers,
        )

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self) -> "SyncAPIClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self._client.send(self._build_request("GET", path, **kwargs))

    def post(self, path: str, **kwargs) -> httpx.Response:
        return self._client.send(self._build_request("POST", path, **kwargs))


