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
CAUSAL_CLAIM_LEVELS = {"INTERVENTIONAL", "COUNTERFACTUAL"}
ROUTER_VERSION = "1.10.0"


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


def _weighted_options(value: Any, label: str) -> list[Mapping[str, Any]]:
    """Require decision-ready alternatives rather than an unweighted list."""

    if not isinstance(value, list) or len(value) < 2:
        raise ValueError(f"{label} requires at least two options")
    options = [_mapping(option, f"{label} option") for option in value]
    option_ids = [option.get("option_id") for option in options]
    if len(option_ids) != len(set(option_ids)):
        raise ValueError(f"{label} options must have unique option_id values")
    recommended = [
        option for option in options if option.get("assessment") == "RECOMMENDED"
    ]
    if len(recommended) != 1:
        raise ValueError(f"{label} requires exactly one RECOMMENDED option")
    return options


def _base_user_interaction(
    decision_basis: list[str], execution_mode: str
) -> dict[str, Any]:
    """Return the user-facing progress brief required for every route."""

    if execution_mode == "SPECIALIST_AS_TOOL":
        next_agent_action = (
            "The framework will inspect and record the active runtime's specialist-invocation capabilities, then use a suitable internal interface to complete the required focused review."
        )
        after_agent_action = (
            "It will check the result, preserve any remaining limit, and then state the next required step."
        )
    elif execution_mode == "CONDUCTOR_ONLY":
        next_agent_action = (
            "The framework will complete the selected research step without changing the accepted research version."
        )
        after_agent_action = (
            "It will check the completed work and then state the next required step."
        )
    elif execution_mode == "PAUSE_FOR_USER":
        next_agent_action = (
            "The framework will keep the current research version unchanged while it waits for your decision."
        )
        after_agent_action = (
            "After your decision is recorded, it will state the next permitted step."
        )
    elif execution_mode == "BLOCKED":
        next_agent_action = (
            "The framework will not work around the problem or advance the research while the prerequisite is unresolved."
        )
        after_agent_action = (
            "After a documented solution is available, it will resume from this same point and state the next step."
        )
    else:  # pragma: no cover - the routing schema constrains this value.
        raise ValueError(f"unsupported execution mode: {execution_mode}")

    return {
        "status": "NOT_REQUIRED",
        "current_position": decision_basis[0],
        "next_agent_action": next_agent_action,
        "after_agent_action": after_agent_action,
        "user_next_action": "No decision or material is required from you now.",
        "question": None,
        "options": [],
        "recommendation": None,
        "problems": [],
    }


def _documented_problems(state: Mapping[str, Any]) -> dict[str, Any]:
    """Build transparent recovery guidance from separately recorded problems."""

    issues = state.get("blocking_issues")
    if not isinstance(issues, list) or not issues:
        raise ValueError(
            "a BLOCKED route requires at least one separately documented blocking issue"
        )

    problems: list[dict[str, Any]] = []
    user_options: list[dict[str, Any]] = []
    recommendations: list[str] = []
    for raw_issue in issues:
        issue = _mapping(raw_issue, "blocking issue")
        required_fields = {
            "issue_id",
            "problem_record_ref",
            "statement",
            "affected_next_action",
            "resolution_options",
            "recommendation",
            "user_action_required",
        }
        if not required_fields.issubset(issue):
            raise ValueError("blocking issue is missing problem-record or recovery guidance")
        options = _weighted_options(
            issue["resolution_options"], "blocking issue recovery guidance"
        )
        problem = {
            "issue_id": issue["issue_id"],
            "problem_record_ref": issue["problem_record_ref"],
            "statement": issue["statement"],
            "impact": issue["affected_next_action"],
            "resolution_options": options,
            "recommendation": issue["recommendation"],
        }
        problems.append(problem)
        recommendations.append(issue["recommendation"])
        if issue["user_action_required"] is True:
            user_options.extend(options)

    if user_options:
        return {
            "status": "REQUIRED",
            "user_next_action": "Choose a resolution for every problem that requires your decision.",
            "question": "Which documented resolution should be used for each open problem?",
            "options": user_options,
            "recommendation": " ".join(recommendations),
            "problems": problems,
        }
    return {
        "problems": problems,
    }


def _validate_specialist_unavailability(state: Mapping[str, Any]) -> None:
    """Reject an availability blocker unless complete discovery proved it."""

    issues = state.get("blocking_issues")
    if not isinstance(issues, list):
        raise ValueError("blocking_issues must be an array")
    unavailable_issues = [
        issue
        for issue in issues
        if isinstance(issue, Mapping)
        and issue.get("category") == "SPECIALIST_UNAVAILABLE"
    ]
    if not unavailable_issues:
        return

    capability = _mapping(
        state.get("specialist_capability"), "specialist_capability"
    )
    status = capability.get("status")
    if status == "AVAILABLE":
        raise ValueError(
            "a specialist cannot be blocked as unavailable when the capability check found a suitable invocation interface"
        )
    if status != "UNAVAILABLE":
        raise ValueError(
            "specialist unavailability requires a completed capability check with status UNAVAILABLE"
        )
    check_ref = capability.get("capability_check_ref")
    if not isinstance(check_ref, str):
        raise ValueError("specialist unavailability requires a capability-check reference")
    routing_ref = capability.get("routing_decision_ref")
    routing_history = state.get("routing_history")
    if (
        not isinstance(routing_ref, str)
        or not isinstance(routing_history, list)
        or not routing_history
        or routing_history[-1] != routing_ref
    ):
        raise ValueError(
            "specialist unavailability requires a capability check for the latest routed decision"
        )
    for issue in unavailable_issues:
        if issue.get("capability_check_ref") != check_ref:
            raise ValueError(
                "specialist unavailability blocker must reference the checkpoint's capability check"
            )
        if issue.get("required_specialist") != capability.get("required_specialist"):
            raise ValueError(
                "specialist unavailability blocker must name the capability check's required specialist"
            )


def _user_interaction(
    state: Mapping[str, Any],
    decision_basis: list[str],
    execution_mode: str,
    supplied: dict[str, Any] | None,
) -> dict[str, Any]:
    """Merge a route's decision prompt with its mandatory progress brief."""

    interaction = _base_user_interaction(decision_basis, execution_mode)
    if execution_mode == "BLOCKED":
        interaction.update(_documented_problems(state))
    elif supplied is not None:
        interaction.update(supplied)

    if interaction["status"] == "REQUIRED" and interaction[
        "user_next_action"
    ] == "No decision or material is required from you now.":
        interaction["user_next_action"] = "Choose one of the weighted options below."
    return interaction


def _fingerprint_guard(
    state: Mapping[str, Any], execution_mode: str, route: str
) -> dict[str, Any]:
    if execution_mode in {"PAUSE_FOR_USER", "BLOCKED"}:
        return {
            "mode": "NOT_APPLICABLE",
            "baseline_fingerprint_ref": None,
            "baseline_fingerprint_sha256": None,
            "comparison_scope": "NONE",
            "difference_disposition": "NOT_APPLICABLE",
        }
    if route == "GENERATE_INTRADAY_IDEAS":
        return {
            "mode": "NEW_RESEARCH_CREATION",
            "baseline_fingerprint_ref": None,
            "baseline_fingerprint_sha256": None,
            "comparison_scope": "NONE",
            "difference_disposition": "RECORD_NEW_FINGERPRINT",
        }
    fingerprint = _mapping(
        state.get("effective_research_fingerprint"),
        "effective_research_fingerprint",
    )
    fingerprint_ref = fingerprint.get("fingerprint_ref")
    fingerprint_hash = fingerprint.get("fingerprint_sha256")
    if not isinstance(fingerprint_ref, str) or not isinstance(fingerprint_hash, str):
        raise ValueError("an effective research fingerprint is required for this route")
    return {
        "mode": "PRESERVE_EFFECTIVE",
        "baseline_fingerprint_ref": fingerprint_ref,
        "baseline_fingerprint_sha256": fingerprint_hash,
        "comparison_scope": "FULL_MATERIAL_RESEARCH_STATE",
        "difference_disposition": "CREATE_VISIBLE_PROPOSAL_AND_PAUSE",
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
    if conductor_version != ROUTER_VERSION:
        raise ValueError("unsupported conductor_version")

    fingerprint_guard = _fingerprint_guard(state, execution_mode, route)
    guarded_work_order = {
        **work_order,
        "excluded_actions": list(work_order["excluded_actions"]),
        "acceptance_checks": list(work_order["acceptance_checks"]),
    }
    if fingerprint_guard["mode"] == "PRESERVE_EFFECTIVE":
        guarded_work_order["excluded_actions"].append(
            "Do not silently replace any effective research commitment, definition, parameter, filter, data choice, inference rule, execution assumption, result, or protected artifact."
        )
        guarded_work_order["acceptance_checks"].append(
            "Before acceptance, the deterministic full-fingerprint check reports UNCHANGED; every difference remains a visible proposal and the baseline stays effective."
        )

    return {
        "schema_version": ROUTER_VERSION,
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
        "work_order": guarded_work_order,
        "fingerprint_guard": fingerprint_guard,
        "next_required_route": next_required_route,
        "user_interaction": _user_interaction(
            state, decision_basis, execution_mode, user_interaction
        ),
        "control": {
            "coordinator_retains_control": True,
            "specialist_may_address_user": False,
            "specialist_may_make_research_decision": False,
            "specialist_may_change_research_state": False,
            "sequential_execution": True,
            "checkpoint_required": True,
            "specialist_capability_check_required_before_invocation": True,
            "specialist_unavailability_requires_complete_discovery": True,
            "specialist_output_requires_validation": True,
            "fingerprint_check_required_before_acceptance": True,
            "scope_locked_to_request": True,
            "delegation_max_depth": 1,
            "conclusions_require_evidence": True,
            "repeat_requires_changed_evidence": True,
            "completion_requires_validated_evidence": True,
        },
    }


def route_state(state: Mapping[str, Any], *, base_dir: Path = Path(__file__).resolve().parents[1]) -> dict[str, Any]:
    """Return exactly one next route from an orchestration checkpoint."""

    from validation_artifact_gate import check_completed_artifacts
    check_completed_artifacts(state, base_dir)
    request = _mapping(state.get("request"), "request")
    context = _mapping(state.get("research_context"), "research_context")
    intent = request.get("intent")
    if not isinstance(intent, str):
        raise ValueError("request.intent must be a string")

    blocking_issues = state.get("blocking_issues")
    if not isinstance(blocking_issues, list):
        raise ValueError("blocking_issues must be an array")
    _validate_specialist_unavailability(state)

    change_control = _mapping(state.get("change_control"), "change_control")
    change_status = change_control.get("status")
    if change_status == "AWAITING_COMPARISON":
        return _decision(
            state,
            route="BLOCKED",
            execution_mode="BLOCKED",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "Returned work is still awaiting comparison with the full effective research fingerprint."
            ],
            work_order=_work_order(
                "Complete the full fingerprint comparison before accepting or routing the returned work.",
                "research_fingerprint_check",
                [
                    str(change_control.get("routing_decision_ref")),
                    "effective baseline fingerprint",
                    "candidate fingerprint derived from the returned work",
                ],
                [
                    "Do not accept the returned artifact yet.",
                    "Do not infer that unchanged wording means the material research state was preserved.",
                ],
                [
                    "Every canonical field and protected artifact hash has been compared."
                ],
                "Stop until the fingerprint check is recorded.",
            ),
        )
    if change_status == "CHANGE_PROPOSED":
        changed = change_control.get("changed_paths")
        if not isinstance(changed, list) or not changed:
            raise ValueError("CHANGE_PROPOSED requires changed_paths")
        summary = change_control.get("plain_language_summary")
        if not isinstance(summary, str):
            raise ValueError("CHANGE_PROPOSED requires a plain-language summary")
        return _decision(
            state,
            route="USER_DECISION_REQUIRED",
            execution_mode="PAUSE_FOR_USER",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[summary],
            work_order=_work_order(
                "Explain the proposed research changes in ordinary language and ask whether they should be rejected or become an explicitly new research version.",
                "plain-language research-change decision",
                [str(change_control.get("check_ref")), str(change_control.get("proposal_ref"))],
                [
                    "Do not replace the effective fingerprint before the decision.",
                    "Do not hide, merge, or paraphrase away any changed path.",
                ],
                [
                    "The changed research parts and their practical consequences are stated.",
                    "The existing fingerprint is still shown as effective.",
                ],
                "Stop after asking the one material question.",
            ),
            user_interaction={
                "status": "REQUIRED",
                "question": (
                    "The returned work proposes material changes to the research. Should the existing version remain unchanged, "
                    "or should the proposal create an intentional new research version?"
                ),
                "options": [
                    {
                        "option_id": "choice:keep-current-research-version",
                        "label": "Keep the current research version.",
                        "consequence": "The proposed replacement is rejected and the accepted definitions and evidence remain unchanged.",
                        "assessment": "RECOMMENDED",
                    },
                    {
                        "option_id": "choice:create-new-research-version",
                        "label": "Create a new research version.",
                        "consequence": "The proposed change becomes a separate version and must follow the required checks for that version.",
                        "assessment": "ACCEPTABLE",
                    },
                ],
                "recommendation": (
                    "Keep the existing version unless the proposal answers a question you now explicitly want to study."
                ),
            },
        )

    material_choice = _mapping(
        request.get("material_user_choice"), "request.material_user_choice"
    )
    if material_choice.get("status") == "REQUIRED":
        options = _weighted_options(
            material_choice.get("options"), "material user choice"
        )
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
                "options": options,
                "recommendation": material_choice.get("recommendation"),
            },
        )

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
            "ASSESS_CAUSAL_CLAIM",
            "ESTIMATE_CAUSAL_EFFECT",
            "QUANTITATIVE_ANALYSIS",
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

    requested_claim_level = request.get("requested_claim_level")
    causal_assessment_status = _artifact_status(
        state, "causal_identification_assessment"
    )
    if (
        requested_claim_level in CAUSAL_CLAIM_LEVELS
        and causal_assessment_status != "COMPLETE"
    ):
        return _decision(
            state,
            route="CAUSAL_IDENTIFICATION_REVIEW",
            execution_mode="SPECIALIST_AS_TOOL",
            selected_agent="causal-identification-critic",
            specialist_mode="PRE_ESTIMATION",
            decision_basis=[
                "The requested conclusion is causal, but no accepted identification assessment exists for this research version."
            ],
            work_order=_work_order(
                "Determine whether the requested causal contrast is identified before any causal estimate or causal wording is accepted.",
                "causal_identification_assessment",
                _input_refs(state),
                [
                    "Do not estimate the causal effect or run a backtest.",
                    "Do not treat DML, local projections, event-study regression, Granger precedence, or causal discovery as the identification argument.",
                    "Do not infer predictive value, mechanism proof, or trading profitability from identification.",
                ],
                [
                    "The assessment passes its schema and finance-specific semantic inspector.",
                    "The estimand, source of identifying variation, economic model, assumptions, diagnostics, and forbidden claims are explicit.",
                    "Event, order-flow, panel, and time-series risks relevant to the chosen design are addressed or reported as blockers.",
                ],
                "Stop after PASS, BLOCKED, FAIL, or NOT_REQUIRED_PREDICTIVE is recorded; do not begin estimation.",
            ),
        )

    if intent == "QUANTITATIVE_ANALYSIS":
        if requested_claim_level in CAUSAL_CLAIM_LEVELS:
            return _decision(
                state,
                route="BLOCKED",
                execution_mode="BLOCKED",
                selected_agent=None,
                specialist_mode=None,
                decision_basis=[
                    "The requested conclusion is causal. Quantitative data analysis cannot replace the required causal-identification assessment or issue causal wording."
                ],
                work_order=_work_order(
                    "Keep the causal question on the causal-identification route, or explicitly narrow the request to a non-causal quantitative diagnostic.",
                    "plain-language blocker report",
                    _input_refs(state),
                    [
                        "Do not ask the data analyst for a causal estimate.",
                        "Do not turn correlation, temporal order, a backtest, or an estimator into causal evidence.",
                    ],
                    [
                        "The causal-identification prerequisite or the narrower non-causal question is explicit."
                    ],
                    "Stop until the requested claim is non-causal or the causal route has been completed.",
                ),
            )

        data_analysis_status = _artifact_status(state, "data_analysis")
        if data_analysis_status == "COMPLETE":
            return _decision(
                state,
                route="BLOCKED",
                execution_mode="BLOCKED",
                selected_agent=None,
                specialist_mode=None,
                decision_basis=[
                    "An accepted quantitative analysis already exists for this research version; an equivalent repeat requires new evidence or an explicitly new version."
                ],
                work_order=_work_order(
                    "Preserve the accepted data-analysis report and identify the genuinely new evidence or user-authorized research version needed for another analysis.",
                    "plain-language blocker report",
                    _input_refs(state),
                    [
                        "Do not repeat an equivalent analysis without changed evidence.",
                        "Do not overwrite the accepted data-analysis report.",
                    ],
                    [
                        "The reason a new analysis would add information is recorded, or the existing report remains final for this step."
                    ],
                    "Stop until new evidence or a new research version is recorded.",
                ),
            )

        return _decision(
            state,
            route="DATA_ANALYSIS",
            execution_mode="SPECIALIST_AS_TOOL",
            selected_agent="data-analyst",
            specialist_mode="SCOPED_QUANTITATIVE_ANALYSIS",
            decision_basis=[
                "The user requested a concrete non-causal quantitative question and no accepted data-analysis report exists for this research version."
            ],
            work_order=_work_order(
                "Answer the scoped quantitative question with documented data provenance, quality checks, uncertainty, and practical limits.",
                "data_analysis_report",
                _input_refs(state) + ["the conductor's scoped data references and request summary"],
                [
                    "Do not make a trading, position, sizing, or risk decision.",
                    "Do not change the research question, strategy, definitions, parameters, filters, outcomes, data roles, or effective fingerprint.",
                    "Do not claim causality, a mechanism, validation, or a tradable after-cost edge.",
                    "Do not invent data, silently fill missing observations, mix incompatible horizons or regimes, or run an unrequested backtest.",
                    "Do not delegate, create side branches, repeat equivalent checks, or schedule automatic follow-up.",
                ],
                [
                    "The report passes schemas/data_analysis_report.schema.json and its semantic validator.",
                    "Sources, periods, variables, data roles, availability, quality limits, uncertainty, and stability are explicit.",
                    "Correlation or association is not presented as causal evidence, and no trading decision is made.",
                    "Before acceptance, the complete research fingerprint check reports UNCHANGED.",
                ],
                "Stop when the scoped report is complete, inconclusive, not testable, or blocked; do not create automatic follow-up work.",
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

    outcome_contract_status = _artifact_status(state, "outcome_evidence_contract")
    if context.get("stage") == "FROZEN_TEST" and outcome_contract_status != "COMPLETE":
        return _decision(
            state,
            route="BLOCKED",
            execution_mode="BLOCKED",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "The test is marked as frozen, but no complete frozen outcome evidence contract exists."
            ],
            work_order=_work_order(
                "Return to the research-case stage and define outcome roles and decision consequences before any test is run.",
                "plain-language blocker report",
                _input_refs(state),
                [
                    "Do not reconstruct an outcome contract after viewing test results.",
                    "Do not run or interpret the frozen test without the contract.",
                ],
                [
                    "The missing pre-test commitment is explicit and no result has been used to fill it."
                ],
                "Stop before empirical testing.",
            ),
        )

    pipeline_integrity_status = _artifact_status(
        state, "pipeline_integrity_assessment"
    )
    if context.get("stage") == "FROZEN_TEST" and pipeline_integrity_status != "COMPLETE":
        return _decision(
            state,
            route="BLOCKED",
            execution_mode="BLOCKED",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "The test is marked as frozen, but the complete pipeline has not passed its required pre-freeze controls."
            ],
            work_order=_work_order(
                "Return to the research-case stage and assess the unchanged complete pipeline on locked null controls and positive sentinels.",
                "plain-language blocker report",
                _input_refs(state),
                [
                    "Do not reconstruct the controls after viewing validation results.",
                    "Do not use validation or final-holdout data to design the controls.",
                    "Do not treat synthetic-control success as evidence for the market claim, prediction, mechanism, or executable edge.",
                ],
                [
                    "The missing pre-freeze pipeline check is explicit and no validation result has been used to fill it."
                ],
                "Stop before empirical validation.",
            ),
        )

    if (
        context.get("stage") == "RESEARCH_CASE"
        and intent == "START_OR_CONTINUE_RESEARCH"
        and outcome_contract_status != "COMPLETE"
    ):
        return _decision(
            state,
            route="DEFINE_OUTCOME_EVIDENCE_CONTRACT",
            execution_mode="CONDUCTOR_ONLY",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "The research case is approaching a test, but outcome roles, contradiction rules, and target-specific stability claims are not yet frozen."
            ],
            work_order=_work_order(
                "Define the outcome evidence contract before the test is frozen.",
                "outcome_evidence_contract",
                _input_refs(state),
                [
                    "Do not inspect validation outcomes while defining the contract.",
                    "Do not let an exploratory or mechanism diagnostic outcome silently replace the primary outcome.",
                    "Do not infer mechanism support from predictive success.",
                ],
                [
                    "Every outcome has a fixed role, target, measurement rule, falsifier, multiplicity family, and decision consequence.",
                    "Mechanical coupling and target-specific transportability are explicit.",
                    "The contract passes schema and semantic validation.",
                ],
                "Stop after the contract is frozen and before empirical testing.",
            ),
        )

    if (
        context.get("stage") == "RESEARCH_CASE"
        and intent == "START_OR_CONTINUE_RESEARCH"
        and pipeline_integrity_status in {"INVALID", "BLOCKED"}
    ):
        return _decision(
            state,
            route="BLOCKED",
            execution_mode="BLOCKED",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "The required pipeline-integrity gate did not pass."
            ],
            work_order=_work_order(
                "Explain which pipeline control failed or could not be constructed and what practical research step is prevented.",
                "plain-language blocker report",
                _input_refs(state),
                [
                    "Do not proceed to validation.",
                    "Do not weaken the locked control after seeing its result.",
                    "Do not present a synthetic result as market evidence.",
                ],
                [
                    "The failed or blocked control and its consequence are stated without changing the research claim."
                ],
                "Stop until a visible new research version or a valid control design is authorized.",
            ),
        )

    if (
        context.get("stage") == "RESEARCH_CASE"
        and intent == "START_OR_CONTINUE_RESEARCH"
        and outcome_contract_status == "COMPLETE"
        and pipeline_integrity_status != "COMPLETE"
    ):
        return _decision(
            state,
            route="ASSESS_PIPELINE_INTEGRITY",
            execution_mode="CONDUCTOR_ONLY",
            selected_agent=None,
            specialist_mode=None,
            decision_basis=[
                "The outcome contract is complete, but the unchanged full pipeline has not yet passed its locked pre-freeze controls."
            ],
            work_order=_work_order(
                "Lock and assess the complete research pipeline on structure-appropriate negative controls and a known-effect positive sentinel.",
                "pipeline_integrity_assessment",
                _input_refs(state),
                [
                    "Do not inspect validation or final-holdout outcomes.",
                    "Do not use one random walk as the only negative control.",
                    "Do not omit a relevant dependency merely because a simpler synthetic model is available.",
                    "Do not promote a passed synthetic or surrogate control into evidence for the market claim, prediction, mechanism, or executable edge.",
                    "Do not import Q-Fin or other unvalidated model code merely because it implements a named stochastic process.",
                ],
                [
                    "The exact pipeline fingerprint, model specification, parameter provenance, random-seed policy, preserved and missing structures, repeat counts, uncertainty, and locked acceptance rule are recorded.",
                    "At least one required negative control and one required known-effect sentinel have assessed results.",
                    "The artifact passes schema and semantic validation, and only an overall PASS permits the freeze path.",
                ],
                "Stop after PASS, FAIL, or BLOCKED is recorded and before real validation.",
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
        decision = route_state(load_object(args.state), base_dir=args.state.resolve().parent)
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
