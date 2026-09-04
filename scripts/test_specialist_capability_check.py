#!/usr/bin/env python3
"""Semantic regressions for specialist capability discovery."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from validate_specialist_capability_check import validate_specialist_capability_check


ROOT = Path(__file__).resolve().parents[1]
CHECK_FIXTURE = ROOT / "examples" / "specialist_capability_check.internal_agent.json"
DECISION_FIXTURE = ROOT / "examples" / "routing_decision.pre_operationalization.json"


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


def assert_invalid(document: dict[str, Any], expected: str) -> None:
    errors = validate_specialist_capability_check(document)
    if not any(expected in error for error in errors):
        raise AssertionError(f"Expected failure containing {expected!r}; got {errors!r}")


def main() -> int:
    baseline = load(CHECK_FIXTURE)
    decision = load(DECISION_FIXTURE)
    errors = validate_specialist_capability_check(baseline, decision)
    if errors:
        raise AssertionError(f"Expected valid internal-agent capability check: {errors}")

    false_unavailable = copy.deepcopy(baseline)
    false_unavailable["status"] = "UNAVAILABLE"
    false_unavailable["selected_interface_id"] = None
    false_unavailable["next_action"] = "RECORD_UNAVAILABILITY_BLOCKER"
    assert_invalid(false_unavailable, "status must be AVAILABLE")

    ignored_interface = copy.deepcopy(baseline)
    ignored_interface["selected_interface_id"] = "interface:missing-adapter"
    assert_invalid(ignored_interface, "must identify an available interface")

    incomplete_unavailable = copy.deepcopy(baseline)
    incomplete_unavailable["interfaces"] = []
    incomplete_unavailable["status"] = "UNAVAILABLE"
    incomplete_unavailable["selected_interface_id"] = None
    incomplete_unavailable["next_action"] = "RECORD_UNAVAILABILITY_BLOCKER"
    incomplete_unavailable["discovery"]["search_complete"] = False
    assert_invalid(incomplete_unavailable, "requires a complete capability search")

    skipped_tool_search = copy.deepcopy(baseline)
    skipped_tool_search["discovery"]["tool_search_surface"] = "AVAILABLE"
    assert_invalid(skipped_tool_search, "True was expected")

    completed_unknown = copy.deepcopy(baseline)
    completed_unknown["interfaces"] = []
    completed_unknown["status"] = "UNKNOWN"
    completed_unknown["selected_interface_id"] = None
    completed_unknown["next_action"] = "RETRY_DISCOVERY"
    assert_invalid(completed_unknown, "requires an incomplete capability search")

    mismatched_route = copy.deepcopy(decision)
    mismatched_route["selected_agent"] = "condition-inquiry-analyst"
    errors = validate_specialist_capability_check(baseline, mismatched_route)
    if not any("does not match the routed specialist" in error for error in errors):
        raise AssertionError(f"A mismatched specialist route was accepted: {errors!r}")

    print(
        "Specialist capability-check tests passed: internal invocation is preferred, "
        "incomplete discovery cannot claim unavailability, and route binding is enforced."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
