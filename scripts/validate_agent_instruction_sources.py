#!/usr/bin/env python3
"""Fail closed when agent bootstrap files duplicate or redefine project rules."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BOOTSTRAP = """# Agent bootstrap

`AGENTS.md` is the sole authoritative source of repository instructions for all
AI agents. Read `AGENTS.md` in full before doing any work, then inspect the
recent entries in `AGENT_CHANGELOG.md`.

If either file cannot be read, stop. Do not duplicate, reinterpret, or add
project rules in this bootstrap file.
"""

CHANGELOG_PREAMBLE = """# Agent Collaboration Changelog

This file records completed work by AI agents. It is a historical record, not
an instruction source. All binding repository rules and changelog requirements
are defined only in `AGENTS.md`. Read `AGENTS.md` in full before using this log.

## Log entries
"""


def main() -> int:
    canonical = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    required_statements = (
        (
            "This file is the sole authoritative source of repository instructions "
            "for every\nAI agent.",
            "AGENTS.md does not declare itself as the sole instruction source.",
        ),
        (
            "`PLANNED_FEATURES.md` is the single authoritative roadmap and priority "
            "order for\nCodex, Claude, Gemini, and every other agent.",
            "AGENTS.md does not declare PLANNED_FEATURES.md as the shared agent roadmap.",
        ),
    )
    for statement, error in required_statements:
        if statement not in canonical:
            raise SystemExit(error)

    roadmap = (ROOT / "PLANNED_FEATURES.md").read_text(encoding="utf-8")
    roadmap_statement = (
        "This file is the single authoritative feature backlog and implementation\n"
        "priority for Codex, Claude, Gemini, and every other agent"
    )
    if roadmap_statement not in roadmap:
        raise SystemExit("PLANNED_FEATURES.md does not declare itself as the shared roadmap.")

    for filename in ("CLAUDE.md", "GEMINI.md"):
        actual = (ROOT / filename).read_text(encoding="utf-8")
        if actual != BOOTSTRAP:
            raise SystemExit(
                f"{filename} must remain the exact minimal bootstrap to AGENTS.md; "
                "project rules may not be duplicated there."
            )

    changelog = (ROOT / "AGENT_CHANGELOG.md").read_text(encoding="utf-8")
    if not changelog.startswith(CHANGELOG_PREAMBLE):
        raise SystemExit(
            "AGENT_CHANGELOG.md must keep the canonical non-normative preamble and "
            "must not become a second instruction source."
        )

    print("Agent instruction-source validation passed: one canonical policy and two minimal bootstraps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
