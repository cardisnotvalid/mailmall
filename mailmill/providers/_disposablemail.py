from .._client import SyncAPIClient


class DisposableMail(SyncAPIClient):
    _base_url = "https://www.disposablemail.com"

    def __init__(self) -> None:
        super().__init__(base_url=self._base_url)

    def get_email(self) -> dict[str, str]:
        return self.get("/index/index").json()

    def get_mailbox(self) -> list[dict[str, object]]:
        return self.get("/index/refresh").json()

    def get_message(self, message_id: int) -> str:
        return self.get(f"/email/id/{message_id}").text

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            **super().default_headers,
            "X-Requested-With": "XMLHttpRequest",
            **self._custom_headers
        }
