#!/usr/bin/env python3
"""Contract and routing tests for the research conductor."""

from __future__ import annotations

import copy
import json
import subprocess
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

from check_research_fingerprint import (
    build_fingerprint_check,
    calculate_fingerprint_sha256,
)
from route_research_task import route_state


ROOT = Path(__file__).resolve().parents[1]
STATE_FIXTURE = "examples/orchestration_state.prose_strategy.json"
DECISION_FIXTURE = "examples/routing_decision.pre_operationalization.json"
FINGERPRINT_FIXTURE = "examples/research_fingerprint.prose_strategy.json"
FINGERPRINT_CHECK_FIXTURE = "examples/research_fingerprint_check.unchanged.json"


def load(relative_path: str) -> dict[str, Any]:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must contain an object")
    return value


def validator(relative_path: str) -> Draft202012Validator:
    schema = load(relative_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


STATE_VALIDATOR = validator("schemas/orchestration_state.schema.json")
DECISION_VALIDATOR = validator("schemas/routing_decision.schema.json")
FINGERPRINT_CHECK_VALIDATOR = validator("schemas/research_fingerprint_check.schema.json")


def assert_route(state: dict[str, Any], expected: str) -> dict[str, Any]:
    state_errors = list(STATE_VALIDATOR.iter_errors(state))
    if state_errors:
        raise AssertionError(
            "Test state is invalid:\n- "
            + "\n- ".join(f"{error.json_path}: {error.message}" for error in state_errors)
        )
    decision = route_state(state)
    decision_errors = list(DECISION_VALIDATOR.iter_errors(decision))
    if decision_errors:
        raise AssertionError(
            "Router produced an invalid decision:\n- "
            + "\n- ".join(
                f"{error.json_path}: {error.message}" for error in decision_errors
            )
        )
    if decision["route"] != expected:
        raise AssertionError(f"Expected route {expected}, observed {decision['route']}")
    return decision


def complete_audit(state: dict[str, Any]) -> None:
    state["artifacts"]["strategy_concept_audit"] = {
        "status": "COMPLETE",
        "artifact_ref": "concept-audit:synthetic-prose-strategy:v1",
    }


def neutral_state() -> dict[str, Any]:
    state = load(STATE_FIXTURE)
    state["research_context"].update(
        {
            "source_kind": "EXISTING_RESEARCH",
            "source_completeness": "NOT_APPLICABLE",
            "stage": "RESEARCH_CASE",
            "concept_audit_required": "NO",
            "operationalization_status": "NOT_APPLICABLE",
            "frozen_result_status": "NONE",
        }
    )
    state["artifacts"] = {
        name: {"status": "NOT_APPLICABLE", "artifact_ref": None}
        for name in state["artifacts"]
    }
    state["completed_steps"] = []
    state["routing_history"] = []
    return state


def main() -> int:
    base = load(STATE_FIXTURE)

    expected_fixture = load(DECISION_FIXTURE)
    actual_fixture = assert_route(
        copy.deepcopy(base), "SCIENTIFIC_PHILOSOPHY_PRE_OPERATIONALIZATION"
    )
    if actual_fixture != expected_fixture:
        raise AssertionError("Committed routing fixture differs from deterministic output")

    baseline_fingerprint = load(FINGERPRINT_FIXTURE)
    unchanged_report = build_fingerprint_check(
        expected_fixture,
        baseline_fingerprint,
        copy.deepcopy(baseline_fingerprint),
        checked_at="2026-08-31T18:05:00+02:00",
    )
    report_errors = list(FINGERPRINT_CHECK_VALIDATOR.iter_errors(unchanged_report))
    if report_errors:
        raise AssertionError(
            "Fingerprint checker produced an invalid unchanged report:\n- "
            + "\n- ".join(
                f"{error.json_path}: {error.message}" for error in report_errors
            )
        )
    if unchanged_report != load(FINGERPRINT_CHECK_FIXTURE):
        raise AssertionError("Committed fingerprint-check fixture differs from deterministic output")

    hidden_filter_change = copy.deepcopy(baseline_fingerprint)
    hidden_filter_change["fingerprint_id"] = "fingerprint:synthetic-prose-strategy:candidate"
    hidden_filter_change["material_specification"]["conditions_filters_and_exclusions"]["content"]["exclusions"] = [
        "Exclude crisis months"
    ]
    hidden_filter_change["fingerprint_sha256"] = calculate_fingerprint_sha256(hidden_filter_change)
    change_report = build_fingerprint_check(
        expected_fixture,
        baseline_fingerprint,
        hidden_filter_change,
        checked_at="2026-08-31T18:06:00+02:00",
    )
    if change_report["overall_status"] != "CHANGE_PROPOSED":
        raise AssertionError("A hidden exclusion was not converted to a visible proposal")
    if not any("conditions_filters_and_exclusions" in path for path in change_report["proposal"]["changed_paths"]):
        raise AssertionError("The proposal did not identify the hidden exclusion")
    if change_report["candidate_may_become_effective"]:
        raise AssertionError("A changed fingerprint was incorrectly allowed to become effective")
    if change_report["proposal"]["effect_if_accepted"] != "CREATE_NEW_RESEARCH_VERSION":
        raise AssertionError("Accepted changes could overwrite the existing research version")

    awaiting_check = copy.deepcopy(base)
    awaiting_check["change_control"] = {
        "status": "AWAITING_COMPARISON",
        "routing_decision_ref": expected_fixture["decision_id"],
        "check_ref": None,
        "proposal_ref": None,
        "changed_paths": [],
        "plain_language_summary": None,
    }
    assert_route(awaiting_check, "BLOCKED")

    change_proposed = copy.deepcopy(base)
    change_proposed["change_control"] = {
        "status": "CHANGE_PROPOSED",
        "routing_decision_ref": expected_fixture["decision_id"],
        "check_ref": change_report["check_id"],
        "proposal_ref": change_report["proposal"]["proposal_id"],
        "changed_paths": change_report["proposal"]["changed_paths"],
        "plain_language_summary": change_report["plain_language_summary"],
    }
    proposal_decision = assert_route(change_proposed, "USER_DECISION_REQUIRED")
    if proposal_decision["user_interaction"]["status"] != "REQUIRED":
        raise AssertionError("A research change proposal did not become a user-visible decision")

    missing_reconstruction = copy.deepcopy(base)
    missing_reconstruction["artifacts"]["strategy_reconstruction"] = {
        "status": "MISSING",
        "artifact_ref": None,
    }
    decision = assert_route(missing_reconstruction, "RECONSTRUCT_SOURCE_STRATEGY")
    if decision["next_required_route"] != "SCIENTIFIC_PHILOSOPHY_PRE_OPERATIONALIZATION":
        raise AssertionError("Prose reconstruction lost its mandatory concept-audit successor")

    condition_needs_definition = copy.deepcopy(base)
    condition_needs_definition["request"]["intent"] = "ASSESS_MEASUREMENT"
    complete_audit(condition_needs_definition)
    decision = assert_route(condition_needs_definition, "OPERATIONALIZE_SOURCE_STRATEGY")
    if decision["next_required_route"] != "CONDITION_INQUIRY":
        raise AssertionError("Condition inquiry may be lost after provisional operationalization")

    condition_ready = copy.deepcopy(condition_needs_definition)
    condition_ready["research_context"]["operationalization_status"] = "PROVISIONAL"
    decision = assert_route(condition_ready, "CONDITION_INQUIRY")
    if decision["selected_agent"] != "condition-inquiry-analyst":
        raise AssertionError("Condition inquiry did not select its specialist")

    quantitative_request = neutral_state()
    quantitative_request["request"]["intent"] = "QUANTITATIVE_ANALYSIS"
    quantitative_request["request"]["requested_claim_level"] = "ASSOCIATIONAL_PREDICTIVE"
    decision = assert_route(quantitative_request, "DATA_ANALYSIS")
    if decision["selected_agent"] != "data-analyst":
        raise AssertionError("Quantitative request did not select the data specialist")
    if decision["specialist_mode"] != "SCOPED_QUANTITATIVE_ANALYSIS":
        raise AssertionError("Data route did not use its bounded specialist mode")
    if decision["work_order"]["required_output_type"] != "data_analysis_report":
        raise AssertionError("Data route did not require a data-analysis report")
    if "Do not make a trading" not in " ".join(decision["work_order"]["excluded_actions"]):
        raise AssertionError("Data route did not exclude trading decisions")

    quantitative_repeat = copy.deepcopy(quantitative_request)
    quantitative_repeat["artifacts"]["data_analysis"] = {
        "status": "COMPLETE",
        "artifact_ref": "data-report:synthetic-intraday-summary:v1",
    }
    assert_route(quantitative_repeat, "BLOCKED")

    quantitative_causal = copy.deepcopy(quantitative_request)
    quantitative_causal["request"]["requested_claim_level"] = "INTERVENTIONAL"
    decision = assert_route(quantitative_causal, "CAUSAL_IDENTIFICATION_REVIEW")
    if decision["selected_agent"] != "causal-identification-critic":
        raise AssertionError("Causal quantitative request bypassed identification review")

    causal_request = neutral_state()
    causal_request["request"]["intent"] = "ASSESS_CAUSAL_CLAIM"
    causal_request["request"]["requested_claim_level"] = "INTERVENTIONAL"
    causal_request["artifacts"]["causal_identification_assessment"] = {
        "status": "MISSING",
        "artifact_ref": None,
    }
    decision = assert_route(causal_request, "CAUSAL_IDENTIFICATION_REVIEW")
    if decision["selected_agent"] != "causal-identification-critic":
        raise AssertionError("Causal claim did not select the identification specialist")
    if decision["work_order"]["required_output_type"] != "causal_identification_assessment":
        raise AssertionError("Causal route did not require its identification artifact")

    predictive_request = neutral_state()
    predictive_request["request"]["intent"] = "START_OR_CONTINUE_RESEARCH"
    predictive_request["request"]["requested_claim_level"] = "ASSOCIATIONAL_PREDICTIVE"
    decision = assert_route(predictive_request, "DEFINE_OUTCOME_EVIDENCE_CONTRACT")
    if decision["work_order"]["required_output_type"] != "outcome_evidence_contract":
        raise AssertionError("Research-case routing did not require the outcome contract.")

    predictive_ready = copy.deepcopy(predictive_request)
    predictive_ready["artifacts"]["outcome_evidence_contract"] = {
        "status": "COMPLETE",
        "artifact_ref": "outcome-contract:synthetic-predictive:v1",
    }
    decision = assert_route(predictive_ready, "ASSESS_PIPELINE_INTEGRITY")
    if decision["work_order"]["required_output_type"] != "pipeline_integrity_assessment":
        raise AssertionError("Pre-freeze routing did not require pipeline controls.")
    if "Q-Fin" not in " ".join(decision["work_order"]["excluded_actions"]):
        raise AssertionError("The pipeline-control route did not reject unvalidated model code.")

    pipeline_ready = copy.deepcopy(predictive_ready)
    pipeline_ready["artifacts"]["pipeline_integrity_assessment"] = {
        "status": "COMPLETE",
        "artifact_ref": "pipeline-integrity:synthetic-predictor:v1",
    }
    assert_route(pipeline_ready, "CONDUCT_RESEARCH")

    pipeline_invalid = copy.deepcopy(predictive_ready)
    pipeline_invalid["artifacts"]["pipeline_integrity_assessment"] = {
        "status": "INVALID",
        "artifact_ref": "pipeline-integrity:synthetic-predictor:failed",
    }
    assert_route(pipeline_invalid, "BLOCKED")

    frozen_without_contract = neutral_state()
    frozen_without_contract["request"]["intent"] = "START_OR_CONTINUE_RESEARCH"
    frozen_without_contract["research_context"]["stage"] = "FROZEN_TEST"
    decision = assert_route(frozen_without_contract, "BLOCKED")
    if "Do not reconstruct" not in " ".join(decision["work_order"]["excluded_actions"]):
        raise AssertionError("Missing pre-test contract did not fail closed after freeze.")

    frozen_without_pipeline_controls = copy.deepcopy(predictive_ready)
    frozen_without_pipeline_controls["research_context"]["stage"] = "FROZEN_TEST"
    decision = assert_route(frozen_without_pipeline_controls, "BLOCKED")
    if "synthetic-control success" not in " ".join(
        decision["work_order"]["excluded_actions"]
    ):
        raise AssertionError("Missing pre-freeze pipeline controls did not fail closed.")

    identified_request = copy.deepcopy(causal_request)
    identified_request["artifacts"]["causal_identification_assessment"] = {
        "status": "COMPLETE",
        "artifact_ref": "causal-assessment:synthetic-hfi:v1",
    }
    assert_route(identified_request, "CONDUCT_RESEARCH")

    post_result = neutral_state()
    post_result["request"]["intent"] = "REVISE_AFTER_RESULT"
    post_result["research_context"]["stage"] = "POST_RESULT"
    post_result["research_context"]["frozen_result_status"] = "FALSIFIED"
    post_result["artifacts"]["scientific_philosophy_review"] = {
        "status": "MISSING",
        "artifact_ref": None,
    }
    decision = assert_route(post_result, "SCIENTIFIC_PHILOSOPHY_POST_RESULT")
    if decision["specialist_mode"] != "POST_RESULT":
        raise AssertionError("Post-result philosophy mode was not explicit")

    explain_only = copy.deepcopy(post_result)
    explain_only["request"]["intent"] = "INTERPRET_RESULT"
    assert_route(explain_only, "CONDUCT_RESEARCH")

    generation = neutral_state()
    generation["request"]["intent"] = "GENERATE_IDEAS"
    generation["research_context"].update(
        {"source_kind": "NONE", "stage": "NO_IDEA", "research_id": None, "research_version": None}
    )
    decision = assert_route(generation, "GENERATE_INTRADAY_IDEAS")
    if decision["fingerprint_guard"]["mode"] != "NEW_RESEARCH_CREATION":
        raise AssertionError("Idea generation did not declare intentional research creation")

    raw_idea = neutral_state()
    raw_idea["research_context"].update(
        {"source_kind": "RAW_IDEA", "stage": "INBOX"}
    )
    assert_route(raw_idea, "RESEARCH_INTAKE")

    material_choice = neutral_state()
    material_choice["request"]["material_user_choice"] = {
        "status": "REQUIRED",
        "question": "Should the reconstructed variant preserve the source's discretionary entry or become a simplified mechanical variant?",
        "options": [
            "Preserve the discretionary protocol.",
            "Create a separately labelled simplified variant.",
        ],
        "recommendation": "Preserve the source protocol unless the goal is explicitly to study a different simplified strategy.",
    }
    assert_route(material_choice, "USER_DECISION_REQUIRED")

    blocked = neutral_state()
    blocked["blocking_issues"] = [
        {
            "issue_id": "issue:missing-source-pages",
            "statement": "The source pages containing the entry definition are missing.",
            "affected_next_action": "Source reconstruction cannot be completed.",
            "user_action_required": True,
        }
    ]
    assert_route(blocked, "BLOCKED")

    formal_strategy = neutral_state()
    formal_strategy["request"]["intent"] = "OPERATIONALIZE_SOURCE_STRATEGY"
    formal_strategy["research_context"].update(
        {
            "source_kind": "FORMAL_STRATEGY",
            "source_completeness": "COMPLETE",
            "stage": "OPERATIONALIZATION",
            "concept_audit_required": "NO",
            "operationalization_status": "DRAFT",
        }
    )
    decision = assert_route(formal_strategy, "OPERATIONALIZE_SOURCE_STRATEGY")
    if decision["fingerprint_guard"]["mode"] != "PRESERVE_EFFECTIVE":
        raise AssertionError("A conductor-only material route bypassed fingerprint protection")

    command = [
        sys.executable,
        str(ROOT / "scripts" / "route_research_task.py"),
        STATE_FIXTURE,
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(
            f"Router CLI failed with {completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
        )
    if json.loads(completed.stdout) != expected_fixture:
        raise AssertionError("Router CLI output differs from committed fixture")

    print(
        "Research-orchestration tests passed: mandatory philosophy handoffs, "
        "causal-identification routing, predictive bypass, full-fingerprint "
        "continuity, visible change proposals, outcome-contract freeze gating, "
        "pipeline-integrity freeze gating, prerequisite ordering, user pause, "
        "and blocker behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
