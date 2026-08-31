#!/usr/bin/env python3
"""Deterministic hard-rule router for the research conductor.

The router does not call a model, inspect market data, choose an
operationalization, or run a test.  It turns an already classified checkpoint
into one bounded next work order.  Semantic classification remains the
conductor's responsibility and is recorded in the checkpoint.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


NON_POSITIVE_RESULTS = {
    "FALSIFIED",
    "PRECISE_NULL",
    "INCONCLUSIVE",
    "INVALID_TEST",
}
POST_RESULT_INTENTS = {
    "ATTRIBUTE_RESULT",
    "REVISE_AFTER_RESULT",
    "CONTINUE_AFTER_RESULT",
}
CONDITION_INTENTS = {
    "ASSESS_MEASUREMENT",
    "DISCOVER_CONDITIONS",
    "CHECK_DEFINITION_SENSITIVITY",
}


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _artifact_ref(state: Mapping[str, Any], name: str) -> str | None:
    artifacts = _mapping(state.get("artifacts"), "artifacts")
    record = _mapping(artifacts.get(name), f"artifacts.{name}")
    ref = record.get("artifact_ref")
    return ref if isinstance(ref, str) else None


def _artifact_status(state: Mapping[str, Any], name: str) -> str:
    artifacts = _mapping(state.get("artifacts"), "artifacts")
    record = _mapping(artifacts.get(name), f"artifacts.{name}")
    status = record.get("status")
    if not isinstance(status, str):
        raise ValueError(f"artifacts.{name}.status must be a string")
    return status


def _input_refs(state: Mapping[str, Any]) -> list[str]:
    refs: list[str] = []
    artifacts = _mapping(state.get("artifacts"), "artifacts")
    for value in artifacts.values():
        record = _mapping(value, "artifact status")
        ref = record.get("artifact_ref")
        if isinstance(ref, str) and ref not in refs:
            refs.append(ref)
    return refs


def _work_order(
    objective: str,
    required_output_type: str,
    allowed_inputs: list[str],
    excluded_actions: list[str],
    acceptance_checks: list[str],
    stop_condition: str,
) -> dict[str, Any]:
    return {
        "objective": objective,
        "allowed_inputs": allowed_inputs,
        "excluded_actions": excluded_actions,
        "required_output_type": required_output_type,
        "acceptance_checks": acceptance_checks,
        "stop_condition": stop_condition,
        "max_attempts": 1,
    }


def _no_user_interaction() -> dict[str, Any]:
    return {
        "status": "NOT_REQUIRED",
        "question": None,
        "options": [],
        "recommendation": None,
    }


def _decision(
    state: Mapping[str, Any],
    *,
    route: str,
    execution_mode: str,
    selected_agent: str | None,
    specialist_mode: str | None,
    decision_basis: list[str],
    work_order: dict[str, Any],
    next_required_route: str | None = None,
    user_interaction: dict[str, Any] | None = None,
) -> dict[str, Any]:
    orchestration_id = state.get("orchestration_id")
    sequence = state.get("next_decision_sequence")
    updated_at = state.get("updated_at")
    conductor_version = state.get("conductor_version")
    if not isinstance(orchestration_id, str):
        raise ValueError("orchestration_id must be a string")
    if not isinstance(sequence, int) or sequence < 1:
        raise ValueError("next_decision_sequence must be a positive integer")
    if not isinstance(updated_at, str):
        raise ValueError("updated_at must be a timestamp string")
    if conductor_version != "1.0.0":
        raise ValueError("unsupported conductor_version")

    return {
        "schema_version": "1.0.0",
        "decision_id": f"routing:{orchestration_id}:{sequence}",
        "created_at": updated_at,
        "orchestration_ref": orchestration_id,
        "conductor_version": conductor_version,
        "route": route,
        "execution_mode": execution_mode,
        "selected_agent": selected_agent,
        "specialist_mode": specialist_mode,
        "decision_basis": decision_basis,
        "input_artifact_refs": _input_refs(state),
        "work_order": work_order,
        "next_required_route": next_required_route,
        "user_interaction": user_interaction or _no_user_interaction(),
        "control": {
            "coordinator_retains_control": True,
            "specialist_may_address_user": False,
            "sequential_execution": True,
            "checkpoint_required": True,
            "specialist_output_requires_validation": True,
        },
    }


def route_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """Return exactly one next route from an orchestration checkpoint."""

    request = _mapping(state.get("request"), "request")
    context = _mapping(state.get("research_context"), "research_context")
    intent = request.get("intent")
    if not isinstance(intent, str):
        raise ValueError("request.intent must be a string")

    material_choice = _mapping(
        request.get("material_user_choice"), "request.material_user_choice"
    )
    if material_choice.get("status") == "REQUIRED":
        return _decision(
            state,
            route="USER_DECISION_REQUIRED",
            execution_mode="PAUSE_FOR_USER",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "The unresolved choice changes the research question or the meaning of the source strategy."
            ],
            work_order=_work_order(
                "Explain the material choice in ordinary language and wait for the user's decision.",
                "plain-language decision request",
                ["current orchestration checkpoint"],
                ["Do not choose on the user's behalf.", "Do not start a specialist or empirical task."],
                ["The alternatives and their practical consequences are stated.", "A recommendation is provided."],
                "Stop after asking the one material question.",
            ),
            user_interaction={
                "status": "REQUIRED",
                "question": material_choice.get("question"),
                "options": material_choice.get("options", []),
                "recommendation": material_choice.get("recommendation"),
            },
        )

    blocking_issues = state.get("blocking_issues")
    if not isinstance(blocking_issues, list):
        raise ValueError("blocking_issues must be an array")
    invalid_artifacts = [
        name
        for name in _mapping(state.get("artifacts"), "artifacts")
        if _artifact_status(state, name) in {"BLOCKED", "INVALID"}
    ]
    if blocking_issues or invalid_artifacts:
        reasons = [
            issue.get("statement", "An unnamed blocking issue exists.")
            for issue in blocking_issues
            if isinstance(issue, Mapping)
        ]
        if invalid_artifacts:
            reasons.append(
                "Required artifacts are blocked or invalid: " + ", ".join(invalid_artifacts)
            )
        return _decision(
            state,
            route="BLOCKED",
            execution_mode="BLOCKED",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=reasons or ["A required input is blocked or invalid."],
            work_order=_work_order(
                "Report what is missing, what remains reliable, and the smallest action that can remove the blocker.",
                "plain-language blocker report",
                ["current orchestration checkpoint"],
                ["Do not skip the blocked prerequisite.", "Do not invent missing source content or evidence."],
                ["The practical consequence of the blocker is explicit."],
                "Stop without advancing the research phase.",
            ),
        )

    frozen_result = context.get("frozen_result_status")
    if frozen_result in NON_POSITIVE_RESULTS and intent in POST_RESULT_INTENTS:
        return _decision(
            state,
            route="SCIENTIFIC_PHILOSOPHY_POST_RESULT",
            execution_mode="SPECIALIST_AS_TOOL",
            selected_agent="scientific-philosophy-critic",
            specialist_mode="POST_RESULT",
            decision_basis=[
                "A non-positive frozen result exists and attribution, revision, or empirical continuation is being considered."
            ],
            work_order=_work_order(
                "Map the tested bundle, preserve the frozen result, and judge whether any proposed continuation adds a genuinely new testable prediction.",
                "scientific_philosophy_review",
                _input_refs(state),
                ["Do not relabel the frozen result.", "Do not run or request a backtest.", "Do not choose a favorable replacement definition."],
                ["The review passes its schema and semantic inspector.", "Any empirical continuation uses a new Research-ID and an independent future test."],
                "Stop after the review has classified the proposed continuation or documented why it remains unresolved.",
            ),
        )

    if intent == "GENERATE_IDEAS":
        return _decision(
            state,
            route="GENERATE_INTRADAY_IDEAS",
            execution_mode="SPECIALIST_AS_TOOL",
            selected_agent="intraday-hypothesis-generator",
            specialist_mode="SHORT_HORIZON_IDEA_GENERATION",
            decision_basis=["The user explicitly requested new intraday or short-swing research ideas."],
            work_order=_work_order(
                "Generate unscreened short-horizon research candidates from the mechanism catalog.",
                "INBOX hypothesis candidates",
                ["generation/mechanism_catalog.v1.json", "the user's stated market and horizon"],
                ["Do not backtest, rank, screen, promote, or claim evidence."],
                ["Every candidate remains INBOX.", "The requested horizon is no longer than five trading days."],
                "Stop after candidate generation; do not enter research intake automatically.",
            ),
        )

    source_kind = context.get("source_kind")
    source_completeness = context.get("source_completeness")
    audit_required = context.get("concept_audit_required")
    reconstruction_status = _artifact_status(state, "strategy_reconstruction")
    audit_status = _artifact_status(state, "strategy_concept_audit")

    prose_reconstruction_needed = (
        source_kind == "PROSE_STRATEGY"
        and reconstruction_status != "COMPLETE"
        and intent
        in {
            "RECONSTRUCT_SOURCE_STRATEGY",
            "OPERATIONALIZE_SOURCE_STRATEGY",
            "ASSESS_MEASUREMENT",
            "DISCOVER_CONDITIONS",
            "CHECK_DEFINITION_SENSITIVITY",
            "START_OR_CONTINUE_RESEARCH",
        }
    )
    if prose_reconstruction_needed:
        return _decision(
            state,
            route="RECONSTRUCT_SOURCE_STRATEGY",
            execution_mode="CONDUCTOR_ONLY",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "The source describes a prose strategy, but no complete source reconstruction exists."
            ],
            work_order=_work_order(
                "Extract only the reviewed source strategy, distinguish rules from examples and discretion, and leave open definitions undecided.",
                "strategy_reconstruction",
                ["reviewed source excerpts and their locators"],
                ["Do not operationalize open constructs.", "Do not invent missing prerequisites.", "Do not run a market test or backtest."],
                ["Source scope and locators are recorded.", "Open definitions remain visibly undecided."],
                "Stop when source extraction is complete enough for the pre-operationalization concept audit.",
            ),
            next_required_route="SCIENTIFIC_PHILOSOPHY_PRE_OPERATIONALIZATION",
        )

    audit_mandatory = (
        source_kind == "PROSE_STRATEGY"
        and (
            source_completeness == "INCOMPLETE"
            or audit_required == "YES"
        )
    )
    if audit_mandatory and reconstruction_status == "COMPLETE" and audit_status != "COMPLETE":
        reconstruction_ref = _artifact_ref(state, "strategy_reconstruction")
        return _decision(
            state,
            route="SCIENTIFIC_PHILOSOPHY_PRE_OPERATIONALIZATION",
            execution_mode="SPECIALIST_AS_TOOL",
            selected_agent="scientific-philosophy-critic",
            specialist_mode="PRE_OPERATIONALIZATION",
            decision_basis=[
                "The prose strategy is incomplete or contains implicit conditions, and its mandatory concept audit is not complete."
            ],
            work_order=_work_order(
                "Separate source conditions, source advice, suspected modifiers, and unknown success conditions before any definition is chosen.",
                "strategy_concept_audit",
                [reconstruction_ref] if reconstruction_ref else [],
                ["Do not choose an operationalization.", "Do not turn suspected or unknown conditions into strategy rules.", "Do not run a market test or backtest."],
                ["The audit passes its schema and semantic inspector.", "Unknown success conditions remain explicitly unknown."],
                "Stop when the concept audit is complete or a missing source fact makes it blocked.",
            ),
            next_required_route="OPERATIONALIZE_SOURCE_STRATEGY",
        )

    if intent in CONDITION_INTENTS:
        operationalization_status = context.get("operationalization_status")
        if operationalization_status not in {"PROVISIONAL", "FROZEN"}:
            return _decision(
                state,
                route="OPERATIONALIZE_SOURCE_STRATEGY",
                execution_mode="CONDUCTOR_ONLY",
                selected_agent=None,
                specialist_mode=None,
                decision_basis=[
                    "A condition or measurement inquiry requires a fixed provisional operationalization, which does not yet exist."
                ],
                work_order=_work_order(
                    "Turn the already audited open constructs into a documented provisional definition without treating it as source fact.",
                    "documented provisional operationalization",
                    _input_refs(state),
                    ["Do not select a definition from outcome data.", "Do not claim the chosen definition was supplied by the source unless it was."],
                    ["Every choice has an origin and rationale.", "The source strategy and the reconstructed variant remain distinguishable."],
                    "Stop after the provisional definition is fixed and before any quantitative inquiry.",
                ),
                next_required_route="CONDITION_INQUIRY",
            )
        return _decision(
            state,
            route="CONDITION_INQUIRY",
            execution_mode="SPECIALIST_AS_TOOL",
            selected_agent="condition-inquiry-analyst",
            specialist_mode=intent,
            decision_basis=[
                "A provisional operationalization exists and the request concerns measurement usefulness, definition sensitivity, or observable success conditions."
            ],
            work_order=_work_order(
                "Formulate the smallest quantitative condition inquiry that answers the stated question without rewriting the source strategy.",
                "condition_inquiry",
                _input_refs(state),
                ["Do not silently alter the source strategy.", "Do not interpret predictive separation as causal proof.", "Do not claim all success conditions are known."],
                ["The inquiry passes its schema and semantic inspector.", "Discovery and independent recurrence are kept separate."],
                "Stop after producing the inquiry plan or the requested bounded interpretation.",
            ),
        )

    if source_kind == "RAW_IDEA" or context.get("stage") == "INBOX":
        return _decision(
            state,
            route="RESEARCH_INTAKE",
            execution_mode="CONDUCTOR_ONLY",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=["A concrete raw idea exists and has not yet completed research intake."],
            work_order=_work_order(
                "Record the raw idea and apply only the intake requirements appropriate to its current status.",
                "hypothesis_candidate",
                ["the raw idea and its provenance"],
                ["Do not call the idea generator.", "Do not promote the idea merely because it is plausible."],
                ["The candidate remains INBOX unless the promotion requirements are actually met."],
                "Stop at the honest intake status.",
            ),
        )

    if intent == "OPERATIONALIZE_SOURCE_STRATEGY":
        return _decision(
            state,
            route="OPERATIONALIZE_SOURCE_STRATEGY",
            execution_mode="CONDUCTOR_ONLY",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=["The request is to document a usable definition after applicable source and concept work."],
            work_order=_work_order(
                "Document the chosen operationalization and its origin while preserving the difference between source strategy and researcher choice.",
                "documented provisional operationalization",
                _input_refs(state),
                ["Do not use outcome data to choose the definition.", "Do not present a reconstructed choice as a source rule."],
                ["All material choices and unresolved points are visible."],
                "Stop before any empirical test unless the user separately requests it and the research path authorizes it.",
            ),
        )

    return _decision(
        state,
        route="CONDUCT_RESEARCH",
        execution_mode="CONDUCTOR_ONLY",
        selected_agent=None,
        specialist_mode=None,
        decision_basis=[
            "No mandatory specialist trigger applies to the classified request and current research state."
        ],
        work_order=_work_order(
            "Continue the currently authorized research step and re-route before the next material transition.",
            "next applicable research artifact or plain-language answer",
            _input_refs(state),
            ["Do not skip a gate or silently change the research question."],
            ["The next step is allowed by the current framework state."],
            "Stop at the next material transition, blocker, or user decision.",
        ),
    )


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("input must contain one JSON object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Route one research orchestration checkpoint to its next bounded task."
    )
    parser.add_argument("state", type=Path, help="orchestration-state JSON file")
    parser.add_argument("--output", type=Path, help="optional routing-decision JSON file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        decision = route_state(load_object(args.state))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Routing failed: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(decision, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
