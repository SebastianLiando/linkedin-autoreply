from dataclasses import dataclass
from typing import List
from .message import Message


@dataclass
class Thread:
    id: str
    history_id: str
    messages: List[Message]

    @staticmethod
    def from_json(json: dict):
        return Thread(
            id=json['id'],
            history_id=json['historyId'],
            messages=[Message.from_json(m) for m in json['messages']],
        )

    def is_replied(self, user_email: str) -> bool:
        num_of_messages = len(self.messages)

        if num_of_messages > 1:
            # If there are multiple messages, check if one of them is sent by the user
            for thread_message in self.messages:
                sender = thread_message.from_address
                if user_email in sender:
                    return True

        # If only 1 message, confirm not replied
        return False
