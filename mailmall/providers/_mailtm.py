import json
from .._client import SyncAPIClient


class MailTM(SyncAPIClient):
    _base_url = "https://api.mail.tm"
    _custom_headers = {}

    def __init__(self) -> None:
        super().__init__(base_url=self._base_url)

    def create_account(self, address: str, password: str):
        payload = {"address": address, "password": password}
        return self.post("/accounts", json=payload).json()

    def get_account_token(self, address: str, password: str):
        payload = {"address": address, "password": password}
        data = self.post("/token", json=payload).json()
        self._custom_headers["Authorization"] = f"Bearer {data['token']}"
        return data

    def get_domains(self):
        return self.get("/domains").json()

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            **super().default_headers,
            "X-Requested-With": "XMLHttpRequest",
            **self._custom_headers
        }
