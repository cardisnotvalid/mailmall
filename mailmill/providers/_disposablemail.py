from .._client import SyncAPIClient
from ..models.disposablemail import Email, Message, Mailbox


class DisposableMail(SyncAPIClient):
    _base_url = "https://www.disposablemail.com"

    def __init__(self) -> None:
        super().__init__(base_url=self._base_url)

    def get_email(self) -> Email:
        data = self.get("/index/index").json()
        return Email.from_dict(data)

    def get_mailbox(self) -> Mailbox:
        data = self.get("/index/refresh").json()
        return Mailbox.from_list(data)

    def get_message(self, message_id: int) -> str:
        return self.get(f"/email/id/{message_id}").text

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            **super().default_headers,
            "X-Requested-With": "XMLHttpRequest",
            **self._custom_headers
        }
