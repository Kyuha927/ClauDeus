from __future__ import annotations

import json
import os
import re
import shutil
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]

PORTFOLIO_COMPONENTS = [
    {"repo": "Kyuha927/copilot", "role": "runtime", "label": "ClauDeus Runtime / Bridge Hub"},
    {"repo": "Kyuha927/daily", "role": "mobile_inbox", "label": "Mobile Inbox Connector"},
    {"repo": "Kyuha927/obsidian_dashboard_os", "role": "dashboard", "label": "User Dashboard"},
    {"repo": "Kyuha927/studio-agent", "role": "skills", "label": "Skills Pack"},
    {"repo": "Kyuha927/agency-runtime", "role": "playbooks", "label": "Playbook Runtime"},
    {"repo": "Kyuha927/codex-global-config", "role": "profiles", "label": "Profile Pack"},
    {"repo": "Kyuha927/codexskills", "role": "skill_archive", "label": "Skill Archive"},
    {"repo": "Kyuha927/knowledge-feeder-vault", "role": "knowledge", "label": "Knowledge Feeder"},
]

@dataclass(slots=True)
class HandoffPacket:
    source: str
    target: str
    project_slug: str
    session_id: str
    turn_id: str
    summary: str
    next_actions: list[str]
    title_hint: str
    created_at: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


def _read_text(path: Path, max_chars: int = 12000) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[: max_chars - 20].rstrip() + "\n...[trimmed]"
    return text


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _slug(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9가-힣_.-]+", "-", text.strip()).strip("-")
    return value[:80] or "task"


def build_context_pack(task: str = "", project: str = "default", output: str = "CONTEXT_PACK.md") -> Path:
    """Create a compact, file-backed prompt handoff packet."""
    project_slug = _slug(project)
    sections: list[str] = [
        "# ClauDeus Context Pack",
        "",
        f"- generated_at: `{time.strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- project: `{project_slug}`",
        f"- task: `{task.strip() or 'continue current work'}`",
        "",
        "## Operating contract",
        "",
        "Return only `PATCH LIST`, `READY-TO-PASTE CONTENT`, and `CHECKS` unless the task explicitly asks for analysis.",
        "Default to propose-only for risky or destructive changes.",
        "",
    ]

    for rel in ["README.md", "AGENTS.md", "DEVELOPMENT_START.md", "ROADMAP.md"]:
        text = _read_text(REPO_ROOT / rel, max_chars=6000)
        if text:
            sections.extend([f"## {rel}", "", text, ""])

    skill_root = REPO_ROOT / "skills"
    if skill_root.exists():
        skills = sorted(skill_root.glob("*/SKILL.md"))[:8]
        if skills:
            sections.extend(["## Candidate skills", ""])
            for skill in skills:
                sections.extend([f"### {skill.parent.name}", "", _read_text(skill, max_chars=2500), ""])

    return _write(REPO_ROOT / output, "\n".join(sections).rstrip() + "\n")


def build_handoff_plan(source: str = "user", target: str = "executor", project: str = "default", summary: str = "") -> Path:
    packet = HandoffPacket(
        source=source,
        target=target,
        project_slug=_slug(project),
        session_id=f"manual-{int(time.time())}",
        turn_id=f"turn-{int(time.time())}",
        summary=summary or "Continue the current ClauDeus work from the attached context pack.",
        next_actions=[
            "Read CONTEXT_PACK.md",
            "Select the lowest-risk provider adapter",
            "Return patch package with checks",
        ],
        title_hint=f"{_slug(project)} handoff",
        created_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
    )
    out = REPO_ROOT / "handoffs" / f"{packet.session_id}.json"
    return _write(out, packet.to_json() + "\n")


def provider_check() -> dict[str, object]:
    checks = {
        "codex_cli": shutil.which("codex") is not None,
        "git": shutil.which("git") is not None,
        "python": shutil.which("python") is not None or shutil.which("python3") is not None,
        "antigravity_cli": shutil.which("antigravity") is not None or shutil.which("ag") is not None,
    }
    result = {"ok": any(checks.values()), "checks": checks}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def mobile_inbox_check() -> dict[str, object]:
    candidates = [
        REPO_ROOT / "connectors" / "google_drive" / "google_drive_poll_ingest.py",
        REPO_ROOT / "Docs" / "MOBILE_INBOX_CONNECTOR.md",
        REPO_ROOT / "DEVELOPMENT_START.md",
    ]
    result = {
        "ok": any(p.exists() for p in candidates),
        "candidates": {str(p.relative_to(REPO_ROOT)): p.exists() for p in candidates},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def portfolio_status() -> Path:
    lines = ["# ClauDeus Portfolio Status", "", f"Generated: `{time.strftime('%Y-%m-%d %H:%M:%S')}`", ""]
    for item in PORTFOLIO_COMPONENTS:
        lines.append(f"- **{item['role']}**: `{item['repo']}` — {item['label']}")
    return _write(REPO_ROOT / "PORTFOLIO_STATUS.md", "\n".join(lines) + "\n")


def _iter_log_texts(paths: Iterable[Path]) -> Iterable[str]:
    for path in paths:
        if path.is_file():
            yield _read_text(path, max_chars=8000)


def skill_suggest(name: str = "candidate", source_dir: str = ".logs") -> Path:
    root = REPO_ROOT / source_dir
    corpus = "\n".join(_iter_log_texts(root.glob("*.log") if root.exists() else []))
    if not corpus:
        corpus = "No logs found. Candidate created from manual request."
    candidate_id = _slug(name)
    out_dir = REPO_ROOT / "skills" / "_candidates" / candidate_id
    content = f"""# Skill Candidate: {candidate_id}

## Trigger

Use this candidate when a similar task repeats and the output contract is stable.

## Evidence

```text
{corpus[:3000]}
```

## Proposed output contract

- PATCH LIST
- READY-TO-PASTE CONTENT
- CHECKS

## Approval

Status: needs human approval.
"""
    return _write(out_dir / "SKILL.md", content)


def skill_approve(candidate: str) -> Path:
    candidate_id = _slug(candidate)
    src = REPO_ROOT / "skills" / "_candidates" / candidate_id
    dst = REPO_ROOT / "skills" / candidate_id
    if not src.exists():
        raise FileNotFoundError(f"candidate not found: {src}")
    if dst.exists():
        raise FileExistsError(f"active skill already exists: {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    return dst / "SKILL.md"
