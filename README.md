# taskstats-demo

A small Python CLI project for trying out GitHub Actions with `uv`.

`taskstats` reads a JSON or CSV file of tasks and prints simple project stats:

- total tasks
- completed and open tasks
- overdue open tasks
- counts by priority

## Task Format

JSON input is an array of objects:

```json
[
  {"title": "Write tests", "completed": true, "due": "2026-06-20", "priority": "high"},
  {"title": "Ship release", "completed": false, "due": "2026-06-30", "priority": "medium"}
]
```

CSV input uses the same fields:

```csv
title,completed,due,priority
Write tests,true,2026-06-20,high
Ship release,false,2026-06-30,medium
```

## Usage

```bash
uv sync
uv run taskstats tests/fixtures/tasks.json
uv run taskstats tests/fixtures/tasks.json --format json
```

## Development

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest
uv run python -m build
```

Refresh the lockfile after dependency changes:

```bash
uv lock
```

## GitHub Actions

The included CI workflow uses `astral-sh/setup-uv`, installs from `uv.lock`, then runs linting,
formatting checks, type checks, tests across multiple Python versions, a CLI smoke test, and a
package build.
