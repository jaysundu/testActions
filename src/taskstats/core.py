from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, TypeAlias

PriorityCounts: TypeAlias = dict[str, int]


@dataclass(frozen=True)
class Task:
    title: str
    completed: bool = False
    due: date | None = None
    priority: str = "normal"


@dataclass(frozen=True)
class TaskStats:
    total: int
    completed: int
    open: int
    overdue: int
    by_priority: PriorityCounts


def load_tasks(path: Path) -> list[Task]:
    """Load tasks from a JSON or CSV file."""
    suffix = path.suffix.lower()
    if suffix == ".json":
        return _load_json(path)
    if suffix == ".csv":
        return _load_csv(path)
    msg = f"Unsupported task file type: {path.suffix or '<none>'}. Use .json or .csv."
    raise ValueError(msg)


def summarize_tasks(tasks: Iterable[Task], *, today: date | None = None) -> TaskStats:
    current_day = today or date.today()
    task_list = list(tasks)
    completed = sum(1 for task in task_list if task.completed)
    overdue = sum(
        1
        for task in task_list
        if not task.completed and task.due is not None and task.due < current_day
    )

    by_priority: PriorityCounts = {}
    for task in task_list:
        by_priority[task.priority] = by_priority.get(task.priority, 0) + 1

    return TaskStats(
        total=len(task_list),
        completed=completed,
        open=len(task_list) - completed,
        overdue=overdue,
        by_priority=dict(sorted(by_priority.items())),
    )


def _load_json(path: Path) -> list[Task]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("JSON task file must contain an array of objects.")
    return [
        _task_from_mapping(item, source=f"{path}:{index + 1}") for index, item in enumerate(data)
    ]


def _load_csv(path: Path) -> list[Task]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [
            _task_from_mapping(row, source=f"{path}:{index + 2}")
            for index, row in enumerate(reader)
        ]


def _task_from_mapping(raw: object, *, source: str) -> Task:
    if not isinstance(raw, dict):
        raise ValueError(f"Task at {source} must be an object.")

    item: dict[str, Any] = raw
    title = _required_text(item, "title", source=source)
    priority = _optional_text(item, "priority", default="normal")

    return Task(
        title=title,
        completed=_parse_bool(item.get("completed", False), source=source),
        due=_parse_due(item.get("due"), source=source),
        priority=priority.lower(),
    )


def _required_text(item: dict[str, Any], key: str, *, source: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Task at {source} must include a non-empty {key!r} field.")
    return value.strip()


def _optional_text(item: dict[str, Any], key: str, *, default: str) -> str:
    value = item.get(key, default)
    if value is None or value == "":
        return default
    if not isinstance(value, str):
        msg = f"Optional field {key!r} must be text when provided."
        raise ValueError(msg)
    return value.strip()


def _parse_bool(value: object, *, source: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "t", "yes", "y", "1"}:
            return True
        if normalized in {"false", "f", "no", "n", "0", ""}:
            return False
    raise ValueError(f"Task at {source} has invalid completed value: {value!r}.")


def _parse_due(value: object, *, source: str) -> date | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError(f"Task at {source} has invalid due date: {value!r}.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Task at {source} has invalid due date: {value!r}.") from exc
