import heapq
import json
import os
from typing import Any


class PersistentPriorityQueue:
    def __init__(self, file_path: str = "queue.json"):
        self.file_path = file_path
        self._items: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r", encoding="utf-8") as file:
            self._items = json.load(file)

    def _save(self) -> None:
        temp_path = f"{self.file_path}.tmp"

        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(self._items, file, indent=2)

        os.replace(temp_path, self.file_path)

    def insert(self, item_id: str, value: Any, priority: int) -> None:
        if item_id in self._items:
            raise ValueError(f"Item already exists: {item_id}")

        self._items[item_id] = {
            "value": value,
            "priority": priority,
        }
        self._save()

    def _ordered_items(self):
        return sorted(
            self._items.items(),
            key=lambda item: (item[1]["priority"], item[0]),
        )

    def extract_min(self) -> dict[str, Any]:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        item_id, item = self._ordered_items()[0]
        del self._items[item_id]
        self._save()

        return {
            "id": item_id,
            **item,
        }

    def extract_max(self) -> dict[str, Any]:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        item_id, item = self._ordered_items()[-1]
        del self._items[item_id]
        self._save()

        return {
            "id": item_id,
            **item,
        }

    def peek(self) -> dict[str, Any]:
        if self.is_empty():
            raise IndexError("Priority queue is empty")

        item_id, item = self._ordered_items()[0]

        return {
            "id": item_id,
            **item,
        }

    def update(self, item_id: str, priority: int) -> None:
        if item_id not in self._items:
            raise KeyError(f"Item not found: {item_id}")

        self._items[item_id]["priority"] = priority
        self._save()

    def delete(self, item_id: str) -> None:
        if item_id not in self._items:
            raise KeyError(f"Item not found: {item_id}")

        del self._items[item_id]
        self._save()

    def is_empty(self) -> bool:
        return len(self._items) == 0


if __name__ == "__main__":
    queue = PersistentPriorityQueue()

    queue.insert("task-1", "process payment", 10)
    queue.insert("task-2", "send email", 5)

    print(queue.peek())
    print(queue.extract_min())