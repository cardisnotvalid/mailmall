from typing import Union, List, Dict, Any
from urllib.parse import unquote
from .._client import SyncAPIClient


class EmailNator(SyncAPIClient):
    _base_url = "https://www.emailnator.com"
    _xsrf_token = ""

    def __init__(self) -> None:
        super().__init__(base_url=self._base_url)
        self._xsrf_token = self.get("/").cookies.get("XSRF-TOKEN")

    def get_email(
        self,
        *,
        use_domain: bool = True,
        use_plus_gmail: bool = True,
        use_dot_gmail: bool = True,
        use_google_mail: bool = True,
    ) -> str:
        """
        Generate email address.

        Args
        ----
        use_domain : bool
            pass
        use_plus_gmail : bool
            pass
        use_dot_gmail : bool
            ...
        use_google_mail : bool
            ...

        Returns
        -------
        str
        """
        data = self.post(
            "/generate-email",
            json={"email": [use_domain, use_plus_gmail, use_dot_gmail, use_google_mail]}
        ).json()
        return data.get("email", []).pop()

    def get_mailbox(self, address: str) -> List[Dict[str, Any]]:
        """
        Check your mailbox.

        An example of response:

        ```json
        [{
            "messageID": "ADSVPN",
            "from": "AI TOOLS",
            "subject": "Unleash the power of AI with our ultimate directory of online tools!",
            "time": "Just Now"
        }]
        ```

        Returns
        -------
        List[Dict[str, str]]
        """
        return self.post("/message-list", json={"email": address}).json()["messageData"]

    def get_message(self, address: str, message_id: str) -> str:
        """
        Fetch single message.

        Args
        ----
        address : str
            Email address
        message_id : str
            Message id

        Returns
        -------
        str
        """
        return self.post(
            "/message-list", json={"email": address, "messageID": message_id}
        ).json()

    @property
    def auth_headers(self) -> Dict[str, str]:
        token = unquote(self._xsrf_token)
        return {"X-Xsrf-Token": token}

    @property
    def default_headers(self) -> Dict[str, str]:
        return {
            **super().default_headers,
            "X-Requested-With": "XMLHttpRequest",
            **self._custom_headers,
        }
