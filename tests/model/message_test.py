from ..import get_asset
from model.message import Message
import pytest


@pytest.fixture()
def read_message():
    data = get_asset('message.json')
    yield Message.from_json(data)


def test_correct_id(read_message):
    assert read_message.id == '18109121e5b7a4a7'


def test_correct_thread_id(read_message):
    assert read_message.thread_id == '18109121e5b7a4a7'


def test_correct_subject(read_message):
    assert read_message.subject == 'Fantastic IOS Roles in Singapore'


def test_correct_from_address(read_message):
    assert read_message.from_address == 'Neil McCormick <inmail-hit-reply@linkedin.com>'


def test_correct_message_id(read_message):
    assert read_message.message_id == '<1261984904.6670095.1653714591174@ltx1-app46141.prod.linkedin.com>'
