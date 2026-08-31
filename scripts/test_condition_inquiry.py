#!/usr/bin/env python3
"""Contract and semantic tests for quantitative condition inquiries."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from inspect_condition_inquiry import semantic_errors, validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = "examples/condition_inquiry.synthetic_measurement.json"
SCHEMA = "schemas/condition_inquiry.schema.json"


def load(relative_path: str) -> dict[str, Any]:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must contain an object")
    return value


def assert_semantic_failure(document: dict[str, Any], expected_fragment: str) -> None:
    errors = semantic_errors(document)
    if not any(expected_fragment in error for error in errors):
        raise AssertionError(
            f"Expected semantic failure containing {expected_fragment!r}; observed {errors!r}"
        )


def main() -> int:
    example = load(EXAMPLE)
    schema = load(SCHEMA)
    errors = validate(example, schema)
    if errors:
        raise AssertionError("Committed condition-inquiry fixture is invalid:\n- " + "\n- ".join(errors))

    assessment = example["measurement_assessment"]
    if assessment["label_share_alone_validates_instrument"] is not False:
        raise AssertionError("Label prevalence was mistaken for instrument validation")
    if assessment["targets_reused_in_construction"] is not False:
        raise AssertionError("Measurement assessment reuses its own construction targets")
    contract = example["interpretation_contract"]
    required_truths = [value for key, value in contract.items() if key != "note"]
    if not all(required_truths):
        raise AssertionError("Interpretation contract lost a required boundary")

    discovered = copy.deepcopy(example)
    condition = discovered["candidate_conditions"][0]
    condition["origin"] = "DATA_DISCOVERED"
    condition["new_hypothesis_required"] = False
    errors = validate(discovered, schema)
    if not any("True was expected" in error for error in errors):
        raise AssertionError("Data-discovered condition could silently rewrite the source strategy")

    fake_plan_result = copy.deepcopy(example)
    fake_plan_result["candidate_conditions"][0]["status"] = "RECURRING"
    assert_semantic_failure(fake_plan_result, "PLAN inquiry cannot report")

    command = [sys.executable, str(ROOT / "scripts" / "inspect_condition_inquiry.py"), EXAMPLE]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(
            f"Inspector failed with {completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
        )
    if "did not execute a market test or backtest" not in completed.stdout:
        raise AssertionError("Inspector output lost its non-execution boundary")

    print(
        "Condition-inquiry tests passed: measurement, discovery and interpretation boundaries hold."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
