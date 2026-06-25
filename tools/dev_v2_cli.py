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

    ss = sub.add_parser("skill-suggest", help="Create a skill candidate")
    ss.add_argument("name", nargs="?", default="candidate")
    ss.add_argument("--source-dir", default=".logs")

    sa = sub.add_parser("skill-approve", help="Promote a skill candidate")
    sa.add_argument("candidate")

    args = parser.parse_args()

    if args.command == "context-pack":
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
