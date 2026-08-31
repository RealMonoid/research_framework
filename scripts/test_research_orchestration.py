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

from route_research_task import route_state


ROOT = Path(__file__).resolve().parents[1]
STATE_FIXTURE = "examples/orchestration_state.prose_strategy.json"
DECISION_FIXTURE = "examples/routing_decision.pre_operationalization.json"


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
    assert_route(generation, "GENERATE_INTRADAY_IDEAS")

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
    assert_route(formal_strategy, "OPERATIONALIZE_SOURCE_STRATEGY")

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
        "Research-orchestration tests passed: 10 routes, mandatory philosophy "
        "handoffs, prerequisite ordering, user pause, and blocker behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
