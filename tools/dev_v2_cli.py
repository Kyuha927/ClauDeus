from __future__ import annotations

import argparse
import sys

from cladeus_core import (
    build_context_pack,
    build_handoff_plan,
    mobile_inbox_check,
    portfolio_status,
    provider_check,
    skill_approve,
    skill_suggest,
)
from context_priority import export_markdown, init_priority, load_priority, move_item, set_enabled
from context_priority_watch import run as watch_context_priority


def main() -> int:
    parser = argparse.ArgumentParser(description="ClauDeus v2 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    cp = sub.add_parser("context-pack", help="Build CONTEXT_PACK.md")
    cp.add_argument("task", nargs="*", help="Task text")
    cp.add_argument("--project", default="default")
    cp.add_argument("--output", default="CONTEXT_PACK.md")

    hp = sub.add_parser("handoff-plan", help="Create a handoff packet")
    hp.add_argument("summary", nargs="*", help="Summary text")
    hp.add_argument("--source", default="user")
    hp.add_argument("--target", default="executor")
    hp.add_argument("--project", default="default")

    sub.add_parser("provider-check", help="Check local provider adapter entrypoints")
    sub.add_parser("mobile-inbox-check", help="Check mobile inbox readiness")
    sub.add_parser("portfolio-status", help="Write PORTFOLIO_STATUS.md")

    pr = sub.add_parser("context-priority", help="Manage context priority order")
    pr_sub = pr.add_subparsers(dest="priority_command", required=True)
    pr_sub.add_parser("init", help="Create context priority file")
    pr_sub.add_parser("list", help="Print current priority order")
    move = pr_sub.add_parser("move", help="Move item to zero-based position")
    move.add_argument("item_id")
    move.add_argument("index", type=int)
    enable = pr_sub.add_parser("enable", help="Enable a context item")
    enable.add_argument("item_id")
    disable = pr_sub.add_parser("disable", help="Disable a context item")
    disable.add_argument("item_id")
    watch = pr_sub.add_parser("watch", help="Watch priority file and rebuild context pack")
    watch.add_argument("--interval", type=float, default=1.0)
    watch.add_argument("--output", default="CONTEXT_PACK.md")
    watch.add_argument("--task", default="continue current work")
    watch.add_argument("--project", default="default")
    watch.add_argument("--once", action="store_true")
    pr_sub.add_parser("export", help="Write context/CONTEXT_PRIORITY.md")

    ss = sub.add_parser("skill-suggest", help="Create a skill candidate")
    ss.add_argument("name", nargs="?", default="candidate")
    ss.add_argument("--source-dir", default=".logs")

    sa = sub.add_parser("skill-approve", help="Promote a skill candidate")
    sa.add_argument("candidate")

    args = parser.parse_args()

    if args.command == "context-pack":
        init_priority()
        path = build_context_pack(task=" ".join(args.task), project=args.project, output=args.output)
        print(f"CONTEXT_PACK_READY {path}")
        return 0
    if args.command == "handoff-plan":
        path = build_handoff_plan(
            source=args.source,
            target=args.target,
            project=args.project,
            summary=" ".join(args.summary),
        )
        print(f"HANDOFF_PACKET_READY {path}")
        return 0
    if args.command == "provider-check":
        provider_check()
        return 0
    if args.command == "mobile-inbox-check":
        mobile_inbox_check()
        return 0
    if args.command == "portfolio-status":
        path = portfolio_status()
        print(f"PORTFOLIO_STATUS_READY {path}")
        return 0
    if args.command == "context-priority":
        if args.priority_command == "init":
            path = init_priority()
            print(f"CONTEXT_PRIORITY_READY {path}")
            return 0
        if args.priority_command == "list":
            data = load_priority()
            for item in sorted(data.get("items", []), key=lambda x: int(x.get("priority", 9999))):
                print(f"{item.get('priority')}\t{item.get('enabled', True)}\t{item.get('id')}\t{item.get('path')}")
            return 0
        if args.priority_command == "move":
            path = move_item(args.item_id, args.index)
            print(f"CONTEXT_PRIORITY_MOVED {path}")
            return 0
        if args.priority_command == "enable":
            path = set_enabled(args.item_id, True)
            print(f"CONTEXT_PRIORITY_ENABLED {path}")
            return 0
        if args.priority_command == "disable":
            path = set_enabled(args.item_id, False)
            print(f"CONTEXT_PRIORITY_DISABLED {path}")
            return 0
        if args.priority_command == "watch":
            return watch_context_priority(
                interval=args.interval,
                output=args.output,
                task=args.task,
                project=args.project,
                once=bool(args.once),
            )
        if args.priority_command == "export":
            path = export_markdown()
            print(f"CONTEXT_PRIORITY_EXPORTED {path}")
            return 0
    if args.command == "skill-suggest":
        path = skill_suggest(name=args.name, source_dir=args.source_dir)
        print(f"SKILL_CANDIDATE_READY {path}")
        return 0
    if args.command == "skill-approve":
        path = skill_approve(args.candidate)
        print(f"SKILL_APPROVED {path}")
        return 0

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
