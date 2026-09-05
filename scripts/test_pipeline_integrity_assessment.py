#!/usr/bin/env python3
"""Regression tests for synthetic and surrogate pipeline controls."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path
from typing import Any

from validate_pipeline_integrity_assessment import (
    schema_errors,
    semantic_errors,
    validate_assessment,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "pipeline_integrity_assessment.synthetic_controls.json"


def load_fixture() -> dict[str, Any]:
    with FIXTURE.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError("Pipeline-integrity fixture must be an object.")
    return value


def planned_version(assessed: dict[str, Any]) -> dict[str, Any]:
    planned = copy.deepcopy(assessed)
    planned["status"] = "PLANNED"
    planned.pop("execution_evidence", None)
    planned["updated_at"] = "2026-09-01T10:15:00Z"
    planned["first_run_at"] = None
    planned["overall_gate"] = "NOT_ASSESSED"
    planned["plain_language_conclusion"] = (
        "The control plan is locked, but no control result exists yet."
    )
    for control in planned["controls"]:
        control["actual_runs"] = 0
        control["result"] = {
            "status": "NOT_ASSESSED",
            "uncertainty_record": None,
            "evidence_refs": [],
            "monte_carlo_uncertainty": "Not assessed before the first run.",
            "plain_language_interpretation": "No result exists yet.",
        }
    return planned


def assert_contains(errors: list[str], fragment: str) -> None:
    if not any(fragment in error for error in errors):
        raise AssertionError(
            f"Expected an error containing {fragment!r}, observed:\n- "
            + "\n- ".join(errors)
        )


def main() -> int:
    from test_execution_controls import prepare_plan
    from pipeline_execution import run
    temporary = tempfile.TemporaryDirectory()
    directory = Path(temporary.name)
    prepare_plan(directory)
    assessed = run(directory / 'plan.json', directory / 'run')
    errors = validate_assessment(assessed)
    if errors:
        raise AssertionError("Valid assessed controls were rejected:\n- " + "\n- ".join(errors))

    planned = planned_version(assessed)
    errors = validate_assessment(planned)
    if errors:
        raise AssertionError("Valid planned controls were rejected:\n- " + "\n- ".join(errors))

    evidence_promotion = copy.deepcopy(assessed)
    evidence_promotion["claim_limits"]["supports_forward_prediction"] = True
    if not schema_errors(evidence_promotion):
        raise AssertionError("Synthetic controls were allowed to become prediction evidence.")

    random_walk_only = copy.deepcopy(assessed)
    random_walk_only["controls"][0]["basis"] = "SYNTHETIC_MODEL"
    random_walk_only["controls"][0]["empirical_data_role"] = "NOT_APPLICABLE"
    random_walk_only["controls"][0]["empirical_dataset_ref"] = None
    random_walk_only["controls"][0]["model"]["family"] = "RANDOM_WALK"
    assert_contains(
        semantic_errors(random_walk_only),
        "RANDOM_WALK cannot be the only required negative control",
    )

    inadequate_pass = copy.deepcopy(assessed)
    inadequate_pass["controls"][0]["model"]["structure_adequacy"] = "INADEQUATE"
    assert_contains(
        semantic_errors(inadequate_pass),
        "cannot PASS a required gate",
    )

    late_lock = copy.deepcopy(assessed)
    late_lock["plan_locked_at"] = late_lock["first_run_at"]
    assert_contains(
        semantic_errors(late_lock),
        "plan_locked_at must be earlier",
    )

    wrong_gate = copy.deepcopy(assessed)
    wrong_gate["controls"][0]["result"]["status"] = "FAIL"
    assert_contains(semantic_errors(wrong_gate), "overall_gate must be FAIL")

    causal_without_sentinel = copy.deepcopy(assessed)
    causal_without_sentinel["causal_tooling_required"] = True
    assert_contains(
        semantic_errors(causal_without_sentinel),
        "needs a required CAUSAL_TOOL_SENTINEL",
    )

    optional_control_promoted = copy.deepcopy(assessed)
    optional_control_promoted["controls"][2]["required_for_gate"] = True
    if not schema_errors(optional_control_promoted):
        raise AssertionError("An optional synthetic challenge was allowed to become a gate silently.")

    post_result_plan = planned_version(assessed)
    post_result_plan["controls"][0]["result"]["status"] = "PASS"
    if not schema_errors(post_result_plan):
        raise AssertionError("A planned control artifact was allowed to contain a result.")

    print(
        "Pipeline-integrity tests passed: full-pipeline null controls, positive sentinels, "
        "structure adequacy, pre-run locking, claim limits, and fail-closed gate mapping."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
