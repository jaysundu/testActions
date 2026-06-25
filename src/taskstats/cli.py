from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from taskstats.core import load_tasks, summarize_tasks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize tasks from a JSON or CSV file.")
    parser.add_argument("task_file", type=Path, help="Path to a .json or .csv task file.")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format. Defaults to text.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        stats = summarize_tasks(load_tasks(args.task_file))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    if args.format == "json":
        print(json.dumps(asdict(stats), indent=2, sort_keys=True))
        return 0

    print(f"Total tasks: {stats.total}")
    print(f"Completed: {stats.completed}")
    print(f"Open: {stats.open}")
    print(f"Overdue: {stats.overdue}")
    print("By priority:")
    for priority, count in stats.by_priority.items():
        print(f"  {priority}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
