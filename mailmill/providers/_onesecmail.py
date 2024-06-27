from .._client import SyncAPIClient


class OneSecMail(SyncAPIClient):
    _base_url = "https://www.1secmail.com/api/v1"

    def __init__(self) -> None:
        super().__init__(base_url=self._base_url)

    def _request(self, params: dict[str, object]) -> dict[str, str]:
        return self.get("/", params=params).json()

    def get_random_email(self, *, count: int = 1) -> list[str]:
        return self._request({"action": "getRandomMailbox", "count": count})

    def get_domains(self) -> list[str]:
        return self._request({"action": "getDomainList"})

    def get_mailbox(self, login: str, domain: str) -> list[str]:
        return self._request({"action": "getMessages", "login": login, "domain": domain})

    def get_message(
        self, login: str, domain: str, *, message_id: int
    ) -> list[dict[str, object]]:
        return self._request({
            "action": "readMessage",
            "login": login,
            "domain": domain,
            "id": message_id
        })

    def download_attachment(
        self, login: str, domain: str, *, message_id: int, file: str
    ) -> object:
        return self._request({
            "action": "download",
            "login": login,
            "domain": domain,
            "id": message_id,
            "file": file
        })

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            **super().default_headers,
            "X-Requested-With": "XMLHttpRequest",
            **self._custom_headers
        }
