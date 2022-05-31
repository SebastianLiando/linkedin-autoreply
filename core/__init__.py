import os
from typing import Iterable, Callable, Any

WIT_ACCESS_TOKEN = os.environ['WIT_ACCESS_TOKEN']
CONF_THRESHOLD = 0.8
SCOPES = [
    # All read/write operations except immediate, permanent deletion of threads and messages, bypassing Trash
    "https://www.googleapis.com/auth/gmail.modify",
]
INMAIL_ADDR = 'inmail-hit-reply@linkedin.com'


def first_where(items: Iterable, test: Callable[[Any], bool], fallback=None):
    """Find the first item in [items] that passes the test function.

    Args:
        items (Iterable): The collection to search.
        test (Callable[[Any], bool]): The test function. This function takes in an item as argument and should return a Boolean value.
        fallback (_type_, optional): The fallback value if none of the items pass the test function. Defaults to None.

    Returns:
        The first item that passes the test function.
    """
    for item in items:
        if test(item):
            return item

    return fallback
