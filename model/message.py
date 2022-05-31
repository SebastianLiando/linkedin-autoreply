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

    def get_header(self, name: str) -> str:
        return first_where(self.headers, lambda h: h['name'] == name)['value']


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
        return self.payload.get_header('Subject')

    @property
    def from_address(self):
        from_str = self.payload.get_header('From')
        from_parts = from_str.split(' ')
        from_email = from_parts[len(from_parts) - 1]
        return from_email[1:len(from_email) - 1]
