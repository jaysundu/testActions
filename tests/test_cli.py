from __future__ import annotations

import json
from pathlib import Path

from pytest import CaptureFixture

from taskstats.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_prints_text_summary(capsys: CaptureFixture[str]) -> None:
    exit_code = main([str(FIXTURES / "tasks.json")])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Total tasks: 4" in captured.out
    assert "Completed: 1" in captured.out
    assert "By priority:" in captured.out


def test_cli_prints_json_summary(capsys: CaptureFixture[str]) -> None:
    exit_code = main([str(FIXTURES / "tasks.json"), "--format", "json"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["total"] == 4
    assert data["completed"] == 1
    assert data["by_priority"] == {"high": 2, "low": 1, "medium": 1}
