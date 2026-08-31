#!/usr/bin/env python3
"""Contract and semantic tests for pre-operationalization concept audits."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from inspect_strategy_concept_audit import semantic_errors, validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = "examples/strategy_concept_audit.synthetic.json"
SCHEMA = "schemas/strategy_concept_audit.schema.json"


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
        raise AssertionError("Committed concept-audit fixture is invalid:\n- " + "\n- ".join(errors))

    classifications = {item["classification"] for item in example["condition_map"]}
    expected = {
        "STRATEGY_DEFINING",
        "SOURCE_STATED_APPLICATION",
        "SUSPECTED_PERFORMANCE_MODIFIER",
        "UNKNOWN_SUCCESS_CONDITION",
    }
    if classifications != expected:
        raise AssertionError("Concept audit does not keep the four condition classes separate")
    if any(item["causal_evidence"] for item in example["construction_dependencies"]):
        raise AssertionError("Construction dependency was mislabelled as causal evidence")
    if any(
        item["predictive_separation_establishes_real_state"]
        or item["predictive_separation_establishes_cause"]
        for item in example["measurement_instruments"]
    ):
        raise AssertionError("Measurement instrument overclaims state reality or causation")

    unknown_construct = copy.deepcopy(example)
    unknown_construct["measurement_instruments"][0]["construct_ref"] = "construct:not-listed"
    assert_semantic_failure(unknown_construct, "references unknown construct")

    missing_unknown = copy.deepcopy(example)
    missing_unknown["condition_map"] = [
        item
        for item in missing_unknown["condition_map"]
        if item["classification"] != "UNKNOWN_SUCCESS_CONDITION"
    ]
    assert_semantic_failure(missing_unknown, "must preserve an UNKNOWN_SUCCESS_CONDITION")

    command = [sys.executable, str(ROOT / "scripts" / "inspect_strategy_concept_audit.py"), EXAMPLE]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(
            f"Inspector failed with {completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
        )
    if "no market test or backtest was run" not in completed.stdout:
        raise AssertionError("Inspector output lost its non-testing boundary")

    print(
        "Strategy concept-audit tests passed: four condition classes remain separate, "
        "unknown conditions remain explicit, and construction/measurement claims stay bounded."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
