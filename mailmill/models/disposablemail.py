from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any

from ._model import ListModel


__all__ = ["Email", "Message", "Mailbox"]


@dataclass
class Email:
    address: str
    password: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Email":
        return Email(address=data["email"], password=data["heslo"])


@dataclass
class Message:
    id: int
    from_: str
    subject: str
    subject_short: str
    body: str
    status: str
    elapsed_time: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Message":
        return Message(
            id=data["id"],
            from_=data["od"],
            subject=data["predmet"],
            subject_short=data["predmetZkraceny"],
            body=data["akce"],
            status=data["precteno"],
            elapsed_time=data["kdy"],
        )


class Mailbox(ListModel[Message]):
    @staticmethod
    def from_list(data: List[Dict[str, Any]]) -> "Mailbox":
        return Mailbox([Message.from_dict(x) for x in data])
