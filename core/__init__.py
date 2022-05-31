import os
from typing import Iterable, Callable, Any

WIT_ACCESS_TOKEN = os.environ['WIT_ACCESS_TOKEN']
CONF_THRESHOLD = 0.7
SCOPES = [
    # All read/write operations except immediate, permanent deletion of threads and messages, bypassing Trash
    "https://www.googleapis.com/auth/gmail.modify",
]
INMAIL_ADDR = 'inmail-hit-reply@linkedin.com'


def first_where(items: Iterable, test: Callable[[Any], bool], fallback=None):
    for item in items:
        if test(item):
            return item

    return fallback
