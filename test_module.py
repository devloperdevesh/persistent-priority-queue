import json

import pytest

from module import PersistentPriorityQueue


def test_insert_and_peek(tmp_path):
    queue = PersistentPriorityQueue(tmp_path / "queue.json")

    queue.insert("a", "task-a", 10)

    assert queue.peek() == {
        "id": "a",
        "value": "task-a",
        "priority": 10,
    }


def test_extract_min(tmp_path):
    queue = PersistentPriorityQueue(tmp_path / "queue.json")

    queue.insert("a", "low priority", 10)
    queue.insert("b", "high priority", 1)

    result = queue.extract_min()

    assert result["id"] == "b"
    assert queue.peek()["id"] == "a"


def test_extract_max(tmp_path):
    queue = PersistentPriorityQueue(tmp_path / "queue.json")

    queue.insert("a", "low", 1)
    queue.insert("b", "high", 10)

    result = queue.extract_max()

    assert result["id"] == "b"


def test_update(tmp_path):
    queue = PersistentPriorityQueue(tmp_path / "queue.json")

    queue.insert("a", "task", 10)
    queue.update("a", 1)

    assert queue.peek()["priority"] == 1


def test_delete(tmp_path):
    queue = PersistentPriorityQueue(tmp_path / "queue.json")

    queue.insert("a", "task", 10)
    queue.delete("a")

    assert queue.is_empty()


def test_persistence(tmp_path):
    path = tmp_path / "queue.json"

    queue = PersistentPriorityQueue(path)
    queue.insert("a", "persistent task", 5)

    new_queue = PersistentPriorityQueue(path)

    assert new_queue.peek() == {
        "id": "a",
        "value": "persistent task",
        "priority": 5,
    }


def test_empty_queue(tmp_path):
    queue = PersistentPriorityQueue(tmp_path / "queue.json")

    assert queue.is_empty()

    with pytest.raises(IndexError):
        queue.peek()