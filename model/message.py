from dataclasses import dataclass
from typing import Dict, List
from core import first_where


@dataclass
class MessagePayload:
    part_id: str
    mime_type: str
    filename: str
    headers: List[Dict[str, str]]

    @staticmethod
    def from_json(json: dict):
        return MessagePayload(
            part_id=json['partId'],
            mime_type=json['mimeType'],
            filename=json['filename'],
            headers=json['headers']
        )

    def __getitem__(self, key):
        return first_where(self.headers, lambda h: h['name'] == key)['value']


@dataclass
class Message:
    id: str
    thread_id: str
    payload: MessagePayload

    @staticmethod
    def from_json(json: dict):
        return Message(
            id=json['id'],
            thread_id=json['threadId'],
            payload=MessagePayload.from_json(json['payload'])
        )

    @property
    def subject(self):
        return self.payload['Subject']

    @property
    def message_id(self):
        # Used in "In-Reply-To" header
        return self.payload['Message-ID']

    @property
    def from_address(self):
        return self.payload['From']
