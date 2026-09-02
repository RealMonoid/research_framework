#!/usr/bin/env python3
"""Regression tests for outcome roles and evidence-stage separation."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from validate_outcome_evidence_contract import schema_errors, semantic_errors, validate_contract


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "outcome_evidence_contract.predictor_without_mechanism.json"


def load_fixture() -> dict[str, Any]:
    with FIXTURE.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError("Outcome evidence fixture must be an object.")
    return value


def frozen_version(assessed: dict[str, Any]) -> dict[str, Any]:
    frozen = copy.deepcopy(assessed)
    frozen["status"] = "FROZEN"
    frozen["updated_at"] = "2026-09-01T09:30:00Z"
    for outcome in frozen["outcomes"]:
        outcome["assessment"] = {
            "result": "NOT_ASSESSED",
            "evidence_refs": [],
            "plain_language_interpretation": "No result exists because the contract is frozen before testing.",
        }
    for item in frozen["transportability_by_target"]:
        item["status"] = "NOT_ASSESSED"
        item["evidence_refs"] = []
        item["plain_language_scope"] = "The environments and stability rule are frozen, but no result exists yet."
    for stage in frozen["stage_conclusions"].values():
        stage["status"] = "UNKNOWN"
        stage["evidence_refs"] = []
        stage["rationale"] = "No conclusion is allowed before the frozen test is assessed."
    return frozen


def assert_contains(errors: list[str], fragment: str) -> None:
    if not any(fragment in error for error in errors):
        raise AssertionError(
            f"Expected an error containing {fragment!r}, observed:\n- "
            + "\n- ".join(errors)
        )


def main() -> int:
    assessed = load_fixture()
    errors = validate_contract(assessed)
    if errors:
        raise AssertionError("Valid assessed contract was rejected:\n- " + "\n- ".join(errors))

    if assessed["stage_conclusions"]["forward_predictive_oos"]["status"] != "SUPPORTED":
        raise AssertionError("The positive fixture lost predictive support.")
    if assessed["stage_conclusions"]["mechanism_supported"]["status"] != "NOT_SUPPORTED":
        raise AssertionError("The positive fixture did not reject the contradicted mechanism story.")

    frozen = frozen_version(assessed)
    errors = validate_contract(frozen)
    if errors:
        raise AssertionError("Valid frozen contract was rejected:\n- " + "\n- ".join(errors))

    story_rescue = copy.deepcopy(assessed)
    story_rescue["stage_conclusions"]["mechanism_supported"] = {
        "status": "SUPPORTED",
        "evidence_refs": ["evidence:decorative-mechanism-story"],
        "rationale": "The predictor worked, so the original story is retained.",
    }
    assert_contains(
        semantic_errors(story_rescue),
        "mechanism_supported must be NOT_SUPPORTED",
    )

    unknown_coupling = copy.deepcopy(frozen)
    unknown_coupling["outcomes"][0]["mechanical_coupling"]["status"] = "UNKNOWN"
    assert_contains(
        semantic_errors(unknown_coupling),
        "cannot retain UNKNOWN mechanical coupling",
    )

    missing_transport = copy.deepcopy(frozen)
    missing_transport["transportability_by_target"] = missing_transport[
        "transportability_by_target"
    ][:1]
    assert_contains(
        semantic_errors(missing_transport),
        "missing: MECHANISM_SUPPORTED",
    )

    duplicate_id = copy.deepcopy(frozen)
    duplicate_id["outcomes"][1]["outcome_id"] = duplicate_id["outcomes"][0][
        "outcome_id"
    ]
    assert_contains(semantic_errors(duplicate_id), "outcome_id values must be unique")

    exploratory_promoted = copy.deepcopy(frozen)
    exploratory_promoted["outcomes"][1]["role"] = "EXPLORATORY"
    if not schema_errors(exploratory_promoted):
        raise AssertionError("An exploratory outcome was allowed to change a material evidence stage.")

    valid_forward = copy.deepcopy(frozen)
    valid_forward["forward_testing_protocol"] = {
        "stopping_rule": {
            "horizon_type": "FIXED_OBSERVATIONS",
            "threshold_value": "500",
            "unit": "trades",
        },
        "peeking_policy": "NO_INTERIM_STOPPING",
        "early_termination_allowed": False,
        "justification": "Fixed 500 trades horizon without optional stopping.",
    }
    errors = validate_contract(valid_forward)
    if errors:
        raise AssertionError("Valid forward testing protocol was rejected:\n- " + "\n- ".join(errors))

    invalid_forward = copy.deepcopy(valid_forward)
    invalid_forward["forward_testing_protocol"]["early_termination_allowed"] = True
    assert_contains(
        semantic_errors(invalid_forward),
        "forward_testing_protocol cannot permit early_termination_allowed when peeking_policy is NO_INTERIM_STOPPING",
    )

    print(
        "Outcome evidence contract tests passed: predictor/mechanism separation, "
        "freeze discipline, coupling disclosure, transportability coverage, role limits, and forward stopping rules."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
