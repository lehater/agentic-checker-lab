#!/usr/bin/env python3
"""Stdlib-only checks for the lab foundation and the documentation navigation."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "docs/README.md",
    "docs/project/strategy.md",
    "docs/project/success-criteria.md",
    "docs/project/roadmap.md",
    "docs/project/governance.md",
    "docs/project/experiment-design.md",
    "docs/project/current-state.yaml",
    "docs/scenario/README.md",
    "docs/research/README.md",
    "docs/research/source-ledger.md",
    "docs/research/legacy-checker.md",
    "docs/research/tooling.md",
    "docs/integration/README.md",
    "docs/evaluation/README.md",
    "docs/evaluation/oracle-plan.md",
    "docs/decisions/README.md",
    "docs/decisions/0001-independent-lab.md",
    "tooling/README.md",
    "tooling/versions.yaml",
    "experiments/README.md",
    ".github/pull_request_template.md",
    ".github/workflows/repository.yml",
)
LINK = re.compile(r"(?<!!)[[][^]]+[]][(]([^ )]+)[)]")
SCHEMES = ("http:", "https:", "mailto:", "data:", "sandbox:")


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append("missing: " + rel)

    agents = ROOT / "AGENTS.md"
    if agents.is_file() and agents.stat().st_size > 1800:
        errors.append("AGENTS.md must stay a compact documentation map")

    docs = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        *sorted((ROOT / "docs").rglob("*.md")),
        ROOT / "tooling" / "README.md",
        ROOT / "experiments" / "README.md",
    ]
    for doc in docs:
        if not doc.is_file():
            continue
        body = doc.read_text(encoding="utf-8")
        for raw in LINK.findall(body):
            if raw.startswith(SCHEMES) or raw.startswith("#") or "://" in raw:
                continue
            name = unquote(raw.split("#", 1)[0].split("?", 1)[0])
            if not name:
                continue
            target = (doc.parent / name).resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f"{doc.relative_to(ROOT)}: link outside repository: {raw}")
            elif not target.exists():
                errors.append(f"{doc.relative_to(ROOT)}: broken relative link: {raw}")

    state = ROOT / "docs/project/current-state.yaml"
    if state.is_file():
        content = state.read_text(encoding="utf-8")
        for key in ("status:", "phase:", "next_task:", "toolchain:"):
            if key not in content:
                errors.append("current-state.yaml missing: " + key)

    if errors:
        print("Repository check FAILED:")
        for issue in errors:
            print(" -", issue)
        return 1
    print(f"Repository check PASS: {len(docs)} Markdown files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
