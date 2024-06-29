from typing import List, Dict, Any
from .._client import SyncAPIClient


class DisposableMail(SyncAPIClient):
    _base_url = "https://www.disposablemail.com"

    def __init__(self) -> None:
        super().__init__(base_url=self._base_url)

    def get_email(self) -> Dict[str, str]:
        """
        Generate email address.

        An example of response:

        ```json
        {
            "email": "jediael.finian@dockleafs.com",
            "heslo": "nbhpn9Z@"
        }
        ```

        Returns
        -------
        Dict[str, str]
        """
        return self.get("/index/index").json()

    def get_mailbox(self) -> List[Dict[str, Any]]:
        """
        Checking your mailbox.

        An example of response:

        ```json
        [{
            "predmetZkraceny": "Welcome to DisposableMail...",
            "predmet": "Welcome to DisposableMail:)",
            "od": "Disposable Mail Address <Admin@DisposableMail.com>",
            "id": 1,
            "kdy": "2 sec. ago",
            "akce": "Some message body",
            "precteno": "new"
        }]
        ```

        Returns
        -------
        List[Dict[str, Any]]
        """
        return self.get("/index/refresh").json()

    def get_message(self, message_id: int) -> str:
        """
        Fetching single message body.

        Args
        ----
        message_id : Union[int, str]
            Message id

        Returns
        -------
        str
        """
        return self.get(f"/email/id/{message_id}").text

    @property
    def default_headers(self) -> Dict[str, str]:
        return {
            **super().default_headers,
            "X-Requested-With": "XMLHttpRequest",
            **self._custom_headers
        }
