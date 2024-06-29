from typing import Union, List, Dict, Any
from .._client import SyncAPIClient


class OneSecMail(SyncAPIClient):
    """
    Provider: https://www.1secmail.com/
    API Documentation: https://www.1secmail.com/api/
    """

    _base_url = "https://www.1secmail.com"

    def __init__(self) -> None:
        super().__init__(base_url=self._base_url)

    def _request(self, params: Dict[str, Any]) -> Dict[str, str]:
        return self.get("/api/v1/", params=params).json()

    def generate_random_emails(self, count: Union[int, None] = None) -> List[str]:
        """
        Generating random email addresses.

        This is NOT required.
        You can use any email address with our domains without generating it before.

        An example of response:

        ```json
        ["514adm2s0c@wwjmp.com"]
        ```

        Args
        ----
        count : Union[int, None]
            The number of random email adresses to generate. Defaults to 1.

        Returns
        -------
        List[str]
        """
        return self._request({"action": "genRandomMailbox", **self._build_payload(locals())})

    def get_domains(self) -> List[str]:
        """
        Getting list of active domains.

        This function generate list of currently active domains on which our system is handling incoming emails at the moment.

        An example of response:

        ```json
        ["1secmail.com"]
        ```

        Returns
        -------
        List[str]
        """
        return self._request({"action": "getDomainList"})

    def get_mailbox(self, login: str, domain: str) -> List[str]:
        """
        Checking your mailbox.

        An example of response:

        ```json
        [{
            "id": 639,
            "from": "someone@example.com",
            "subject": "Some subject",
            "date": "2018-06-08 14:33:55"
        }]
        ```

        Args
        ----
        login : str
            Email login
        domain : str
            Email domain

        Returns
        -------
        List[Dict[str, Any]]
        """
        return self._request({"action": "getMessages", **self._build_payload(locals())})

    def get_message(self, login: str, domain: str, message_id: Union[int, str]) -> Dict[str, Any]:
        """
        Fetching single message.

        An example of response:

        ```json
        {
            "id": 639,
            "from": "someone@example.com",
            "subject": "Some subject",
            "date": "2018-06-08 14:33:55",
            "attachments": [{
                "filename": "iometer.pdf",
                "contentType": "application\/pdf",
                "size": 47412
            }],
            "body": "Some message body",
            "textBody": "Some message body",
            "htmlBody": ""
        }
        ```

        Args
        ----
        login : str
            Email login
        domain : str
            Email domain
        message_id : Union[int, str]
            Message id

        Returns
        -------
        Dict[str, Any]
        """
        params = {"action": "readMessage", **self._build_payload(locals())}
        params["id"] = params.pop("message_id")
        return self._request(params)

    def download_attachment(self, login: str, domain: str, message_id: Union[int, str], file: str) -> Any:
        """
        Attachment download.

        Args
        ----
        login : str
            Email login
        domain : str
            Email domain
        message_id : Union[int, str]
            Message id
        file : str
            Filename of attachment
        """
        params = {"action": "download", **self._build_payload(locals())}
        params["id"] = params.pop("message_id")
        return self._request(params)
