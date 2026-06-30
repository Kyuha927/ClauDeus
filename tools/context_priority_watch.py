#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from pathlib import Path

from cladeus_core import build_context_pack
from context_priority import DEFAULT_PRIORITY_PATH, init_priority


def mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return 0.0


def run(*, interval: float, output: str, task: str, project: str, once: bool = False) -> int:
    init_priority()
    last = -1.0
    while True:
        current = mtime(DEFAULT_PRIORITY_PATH)
        if current != last:
            build_context_pack(task=task, project=project, output=output)
            print(f"CONTEXT_PRIORITY_APPLIED {DEFAULT_PRIORITY_PATH} -> {output}", flush=True)
            last = current
        if once:
            return 0
        time.sleep(max(0.25, interval))


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch context priority and rebuild context pack on change")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--output", default="CONTEXT_PACK.md")
    parser.add_argument("--task", default="continue current work")
    parser.add_argument("--project", default="default")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    return run(interval=args.interval, output=args.output, task=args.task, project=args.project, once=bool(args.once))


if __name__ == "__main__":
    raise SystemExit(main())
