# Persistent Priority Queue

A persistent priority queue implementation in Python.

The queue supports:

- `insert`
- `extract_min`
- `extract_max`
- `peek`
- `update`
- `delete`
- `is_empty`

## Implementation

The queue stores its state in a JSON file.

Each item contains:

- `id`
- `value`
- `priority`

Lower priority numbers are returned first by `extract_min`.
Higher priority numbers are returned first by `extract_max`.

Updates and deletions are persisted immediately.

A temporary file is used during writes and then atomically replaced
to avoid leaving a partially written queue file.

## Real-world use cases

Priority queues are useful for:

- Job scheduling
- Network packet prioritization
- Task processing systems
- Event scheduling
- Background worker queues

## Requirements

Python 3.10+

Install test dependency:

```bash
pip install pytest