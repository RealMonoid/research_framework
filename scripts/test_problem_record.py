#!/usr/bin/env python3
"""Semantic regression tests for separately stored workflow problem records."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from validate_problem_record import validate_problem_record


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "problem_record.missing_source_pages.json"
FRAMEWORK_PROBLEM = ROOT / "problems" / "2026-09-04-specialist-capability-discovery-bypass.json"


def load_fixture() -> dict[str, object]:
    with FIXTURE.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError("problem-record fixture must contain an object")
    return value


def assert_invalid(document: dict[str, object], expected_fragment: str) -> None:
    errors = validate_problem_record(document)
    if not any(expected_fragment in error for error in errors):
        raise AssertionError(
            f"Expected problem-record failure containing {expected_fragment!r}; got {errors!r}"
        )


def main() -> int:
    example = load_fixture()
    errors = validate_problem_record(example)
    if errors:
        raise AssertionError(f"Synthetic problem record is invalid: {errors}")
    with FRAMEWORK_PROBLEM.open("r", encoding="utf-8") as handle:
        framework_problem = json.load(handle)
    if not isinstance(framework_problem, dict):
        raise AssertionError("framework problem record must contain an object")
    errors = validate_problem_record(framework_problem)
    if errors:
        raise AssertionError(f"Framework problem record is invalid: {errors}")

    earlier_record = copy.deepcopy(example)
    earlier_record["recorded_at"] = "2026-09-04T09:29:00+02:00"
    assert_invalid(earlier_record, "recorded_at cannot precede occurred_at")

    mismatched_recommendation = copy.deepcopy(example)
    mismatched_recommendation["recommended_option_id"] = "resolution:close-unreconstructable-case"
    assert_invalid(mismatched_recommendation, "must identify the RECOMMENDED option")

    duplicate_option = copy.deepcopy(example)
    options = duplicate_option["resolution_options"]
    if not isinstance(options, list) or not isinstance(options[1], dict):
        raise AssertionError("fixture resolution options have unexpected shape")
    options[1]["option_id"] = "resolution:provide-source-pages"
    assert_invalid(duplicate_option, "must use unique option_id values")

    print("Problem-record tests passed: model identity, timestamp order, and weighted recovery options.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
