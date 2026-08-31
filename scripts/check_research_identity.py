#!/usr/bin/env python3
"""Compare the six-part research identity around one routed handoff."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


DIMENSIONS = (
    "research_question",
    "strategy",
    "market",
    "time_horizon",
    "trigger",
    "target",
)


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _check_id(decision_id: str) -> str:
    candidate = f"identity-check:{decision_id}"
    if len(candidate) > 199:
        raise ValueError("derived identity-check id exceeds 199 characters")
    return candidate


def build_identity_check(
    decision: Mapping[str, Any],
    after_state: Mapping[str, Any],
    *,
    checked_at: str,
) -> dict[str, Any]:
    """Build one deterministic comparison report from a route and candidate state."""

    decision_id = decision.get("decision_id")
    if not isinstance(decision_id, str):
        raise ValueError("decision_id must be a string")
    guard = _mapping(decision.get("identity_guard"), "identity_guard")
    mode = guard.get("mode")
    if mode not in {"PRESERVE_EXISTING", "NEW_IDENTITY_CREATION", "NOT_APPLICABLE"}:
        raise ValueError("identity_guard.mode is unsupported")

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "check_id": _check_id(decision_id),
        "checked_at": checked_at,
        "routing_decision_ref": decision_id,
        "guard_mode": mode,
        "before_identity": None,
        "after_identity": None,
        "comparisons": [],
        "overall_status": "NOT_APPLICABLE",
        "changed_dimensions": [],
        "plain_language_summary": (
            "This route does not hand an existing research identity to a specialist."
        ),
        "handoff_may_be_accepted": True,
    }

    if mode == "NEW_IDENTITY_CREATION":
        report.update(
            {
                "overall_status": "NOT_COMPARABLE_NEW_IDENTITY",
                "plain_language_summary": (
                    "No existing research identity was available for a before-and-after comparison; "
                    "each generated idea must receive its own identity at intake."
                ),
            }
        )
        return report

    if mode == "NOT_APPLICABLE":
        return report

    before = _mapping(guard.get("baseline_identity"), "identity_guard.baseline_identity")
    after = _mapping(after_state.get("research_identity"), "research_identity")
    expected_dimensions = guard.get("compared_dimensions")
    if expected_dimensions != list(DIMENSIONS):
        raise ValueError("identity guard must compare the six dimensions in canonical order")

    comparisons: list[dict[str, Any]] = []
    changed: list[str] = []
    for dimension in DIMENSIONS:
        before_value = _mapping(before.get(dimension), f"before.{dimension}")
        after_value = _mapping(after.get(dimension), f"after.{dimension}")
        status = "UNCHANGED" if before_value == after_value else "CHANGED"
        comparisons.append(
            {
                "dimension": dimension,
                "before": dict(before_value),
                "after": dict(after_value),
                "status": status,
            }
        )
        if status == "CHANGED":
            changed.append(dimension)

    report.update(
        {
            "before_identity": dict(before),
            "after_identity": dict(after),
            "comparisons": comparisons,
            "overall_status": "DRIFT_DETECTED" if changed else "UNCHANGED",
            "changed_dimensions": changed,
            "plain_language_summary": (
                "The handoff changed these parts of the research: "
                + ", ".join(changed)
                + ". The returned work must not be accepted until the user decides whether the change is intended."
                if changed
                else "The handoff preserved the research question, strategy, market, time horizon, trigger, and target."
            ),
            "handoff_may_be_accepted": not changed,
        }
    )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare research identity before and after one routed handoff."
    )
    parser.add_argument("decision", type=Path, help="routing-decision JSON file")
    parser.add_argument("after_state", type=Path, help="candidate post-handoff orchestration state")
    parser.add_argument("--output", type=Path, help="optional identity-check JSON file")
    parser.add_argument(
        "--checked-at",
        default=None,
        help="optional ISO timestamp; defaults to current UTC time",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    checked_at = args.checked_at or datetime.now(timezone.utc).isoformat()
    try:
        report = build_identity_check(
            _load(args.decision),
            _load(args.after_state),
            checked_at=checked_at,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Identity check failed: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 1 if report["overall_status"] == "DRIFT_DETECTED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
