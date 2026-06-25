from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from taskstats.core import Task, load_tasks, summarize_tasks

FIXTURES = Path(__file__).parent / "fixtures"


def test_summarize_tasks_counts_completed_open_overdue_and_priority() -> None:
    tasks = [
        Task("done", completed=True, due=date(2026, 6, 1), priority="high"),
        Task("late", completed=False, due=date(2026, 6, 10), priority="high"),
        Task("later", completed=False, due=date(2026, 7, 1), priority="low"),
        Task("unscheduled", completed=False, priority="normal"),
    ]

    stats = summarize_tasks(tasks, today=date(2026, 6, 25))

    assert stats.total == 4
    assert stats.completed == 1
    assert stats.open == 3
    assert stats.overdue == 1
    assert stats.by_priority == {"high": 2, "low": 1, "normal": 1}


@pytest.mark.parametrize("filename", ["tasks.json", "tasks.csv"])
def test_load_tasks_from_supported_files(filename: str) -> None:
    tasks = load_tasks(FIXTURES / filename)

    assert [task.title for task in tasks] == [
        "Write tests",
        "Wire GitHub Actions",
        "Publish package",
        "Triage ideas",
    ]
    assert tasks[0].completed is True
    assert tasks[1].due == date(2026, 6, 24)
    assert tasks[3].due is None


def test_load_tasks_rejects_unsupported_extensions(tmp_path: Path) -> None:
    task_file = tmp_path / "tasks.txt"
    task_file.write_text("nope", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported task file type"):
        load_tasks(task_file)


def test_load_tasks_rejects_bad_json_shape(tmp_path: Path) -> None:
    task_file = tmp_path / "tasks.json"
    task_file.write_text('{"title": "not a list"}', encoding="utf-8")

    with pytest.raises(ValueError, match="array of objects"):
        load_tasks(task_file)
