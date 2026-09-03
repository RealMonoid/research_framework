#!/usr/bin/env python3
"""Contract and semantic tests for the bounded framework-control reviewer."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - environment failure.
    raise SystemExit(
        "Missing development dependency 'jsonschema'. "
        "Install with: python -m pip install -r requirements-dev.txt"
    ) from exc

from validate_framework_control_review import semantic_errors


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "framework_control_review.synthetic.json"
SCHEMA = ROOT / "schemas" / "framework_control_review.schema.json"


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


def assert_schema_valid(document: dict[str, Any]) -> None:
    validator = Draft202012Validator(load(SCHEMA), format_checker=FormatChecker())
    errors = list(validator.iter_errors(document))
    if errors:
        raise AssertionError(
            "Expected valid framework-control review was rejected:\n- "
            + "\n- ".join(f"{error.json_path}: {error.message}" for error in errors)
        )


def assert_invalid(document: dict[str, Any], label: str) -> None:
    validator = Draft202012Validator(load(SCHEMA), format_checker=FormatChecker())
    if validator.is_valid(document) and not semantic_errors(document):
        raise AssertionError(f"Expected invalid review was accepted: {label}")


def main() -> int:
    baseline = load(EXAMPLE)
    assert_schema_valid(baseline)
    if semantic_errors(baseline):
        raise AssertionError(f"Expected no semantic errors: {semantic_errors(baseline)}")

    private_reasoning = copy.deepcopy(baseline)
    private_reasoning["no_private_chain_of_thought"] = False
    assert_invalid(private_reasoning, "private chain-of-thought disclosure")

    applied_without_regression = copy.deepcopy(baseline)
    applied_without_regression["corrective_action"]["status"] = "APPLIED"
    assert_invalid(applied_without_regression, "applied correction without regression")

    closed_without_regression = copy.deepcopy(baseline)
    closed_without_regression["disposition"] = "CLOSED"
    assert_invalid(closed_without_regression, "closed review without regression")

    strategy_without_identity = copy.deepcopy(baseline)
    strategy_without_identity["mode"] = "STRATEGY_LAUNDERING"
    strategy_without_identity["finding"]["equivalent_attempt_count"] = 1
    assert_invalid(strategy_without_identity, "strategy laundering without identity")

    print(
        "Framework-control review tests passed: schema validity, no-private-reasoning, "
        "bounded correction, closure, and strategy-identity safeguards."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
