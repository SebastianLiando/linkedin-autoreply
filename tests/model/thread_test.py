import pytest
from model.thread import Thread
from ..import get_asset


@pytest.fixture()
def read_thread():
    data = get_asset('thread.json')
    yield Thread.from_json(data)


def test_correct_id(read_thread):
    assert read_thread.id == '1811531be3d51725'


def test_correct_history_id(read_thread):
    assert read_thread.history_id == '3808969'


def test_correct_messages(read_thread):
    messages = read_thread.messages

    assert len(messages) == 2
    assert messages[0].id == '1811531be3d51725'
    assert messages[1].id == '18115365822c6ef1'


def test_correct_is_replied(read_thread):
    assert read_thread.is_replied('sebastianliando@gmail.com')
    assert not read_thread.is_replied('random@gmail.com')
