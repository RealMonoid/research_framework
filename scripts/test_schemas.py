#!/usr/bin/env python3
"""Cross-platform JSON Schema contract tests.

This mirrors the PowerShell contract suite so Linux/macOS CI does not depend on
PowerShell.  The fixtures remain the shared source of truth.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - environment failure.
    raise SystemExit(
        "Missing development dependency 'jsonschema'. "
        "Install with: python -m pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
Mutation = Callable[[dict[str, Any]], None]


def load(relative_path: str) -> dict[str, Any]:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"{relative_path} must contain a JSON object")
    return value


def validator(schema_path: str) -> Draft202012Validator:
    schema = load(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def resolve(value: Any, path: Iterable[str | int]) -> Any:
    current = value
    for component in path:
        current = current[component]
    return current


def set_value(path: tuple[str | int, ...], value: Any) -> Mutation:
    def mutate(document: dict[str, Any]) -> None:
        parent = resolve(document, path[:-1])
        parent[path[-1]] = value

    return mutate


def delete_value(path: tuple[str | int, ...]) -> Mutation:
    def mutate(document: dict[str, Any]) -> None:
        parent = resolve(document, path[:-1])
        del parent[path[-1]]

    return mutate


def add_nonacademic_metadata(document: dict[str, Any]) -> None:
    academic = load("examples/evidence.academic.json")
    document["sources"][0]["academic_metadata"] = copy.deepcopy(
        academic["sources"][0]["academic_metadata"]
    )


def remove_applied_review_event(document: dict[str, Any]) -> None:
    document["reviews"][0]["audit_trail"] = [
        event
        for event in document["reviews"][0]["audit_trail"]
        if event["event_type"] != "APPLIED"
    ]


def configure_data_driven_selection(document: dict[str, Any]) -> None:
    """Replace the lightweight predefined record with full search provenance."""

    document["variable_selection"] = {
        "mode": "DATA_DRIVEN",
        "rationale": (
            "A discovery-only screen reduced a frozen candidate universe before "
            "the validation sample was opened."
        ),
        "candidate_universe_ref": "artifact:variable-universe-v1",
        "selection_data_refs": ["dataset:es-lob-discovery-v1"],
        "selection_dataset_role": "DISCOVERY",
        "outcome_visibility": "VISIBLE_DURING_SELECTION",
        "selection_methods": ["method:mutual-information-screen"],
        "retained_variable_refs": [
            "variable:top3-order-flow-imbalance",
            "variable:spread-state",
        ],
        "effective_candidate_count": 48,
        "search_space_ref": "search-space:ofi-variable-screen-v1",
        "selection_bias_controls": [
            "All 48 candidates remain in the search log.",
            "Selection uses discovery data only; validation remains sealed.",
        ],
    }


def invalidate_data_driven_selection(field: str, value: Any) -> Mutation:
    def mutate(document: dict[str, Any]) -> None:
        configure_data_driven_selection(document)
        document["variable_selection"][field] = value

    return mutate


def replace_noise_screen_with_invalid_waiver(document: dict[str, Any]) -> None:
    del document["noise_screen_ref"]
    document["noise_screen_waiver"] = {"reason": "THEORY_DRIVEN"}


POSITIVES = [
    ("generation/mechanism_catalog.v1.json", "schemas/mechanism_catalog.schema.json"),
    ("examples/strategy_reconstruction.vwap_wave_price_discovery.json", "schemas/strategy_reconstruction.schema.json"),
    ("examples/strategy_concept_audit.synthetic.json", "schemas/strategy_concept_audit.schema.json"),
    ("examples/condition_inquiry.synthetic_measurement.json", "schemas/condition_inquiry.schema.json"),
    ("examples/scientific_philosophy_review.synthetic_failed_reconstruction.json", "schemas/scientific_philosophy_review.schema.json"),
    ("examples/generated-run/generation-run.json", "schemas/generation_run.schema.json"),
    ("examples/generated-run/candidates/mechanism-futures-cash-price-discovery-phase-transmission.json", "schemas/hypothesis_candidate.schema.json"),
    ("examples/search_space.minimal.json", "schemas/search_space.schema.json"),
    ("examples/noise_screen.pass.json", "schemas/noise_screen.schema.json"),
    ("examples/noise_screen.fail.json", "schemas/noise_screen.schema.json"),
    ("examples/run_manifest.minimal.json", "schemas/run_manifest.schema.json"),
    ("examples/evidence.minimal.json", "schemas/evidence.schema.json"),
    ("examples/evidence.academic.json", "schemas/evidence.schema.json"),
    ("examples/forecast.minimal.json", "schemas/forecast.schema.json"),
    ("examples/review.minimal.json", "schemas/review.schema.json"),
    ("examples/constraint_assessment.causal_lever.json", "schemas/constraint_assessment.schema.json"),
    ("examples/hypothesis_candidate.inbox.json", "schemas/hypothesis_candidate.schema.json"),
    ("examples/hypothesis_candidate.rejected.json", "schemas/hypothesis_candidate.schema.json"),
    ("examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json"),
]


NEGATIVES: list[tuple[str, str, str, Mutation]] = [
    ("mechanism catalog rejects additional property", "generation/mechanism_catalog.v1.json", "schemas/mechanism_catalog.schema.json", set_value(("confidence_score",), 0.8)),
    ("strategy reconstruction rejects additional property", "examples/strategy_reconstruction.vwap_wave_price_discovery.json", "schemas/strategy_reconstruction.schema.json", set_value(("backtest_result",), "invented")),
    ("unknown success condition cannot be smuggled into strategy", "examples/strategy_concept_audit.synthetic.json", "schemas/strategy_concept_audit.schema.json", set_value(("condition_map", 3, "incorporation_status"), "SOURCE_COMPONENT")),
    ("construction dependency cannot claim causal evidence", "examples/strategy_concept_audit.synthetic.json", "schemas/strategy_concept_audit.schema.json", set_value(("construction_dependencies", 0, "causal_evidence"), True)),
    ("filter label share alone cannot validate instrument", "examples/condition_inquiry.synthetic_measurement.json", "schemas/condition_inquiry.schema.json", set_value(("measurement_assessment", "label_share_alone_validates_instrument"), True)),
    ("measurement assessment cannot reuse its construction target", "examples/condition_inquiry.synthetic_measurement.json", "schemas/condition_inquiry.schema.json", set_value(("measurement_assessment", "targets_reused_in_construction"), True)),
    ("philosophy review cannot relabel frozen result", "examples/scientific_philosophy_review.synthetic_failed_reconstruction.json", "schemas/scientific_philosophy_review.schema.json", set_value(("frozen_result", "remains_unchanged"), False)),
    ("progressive revision requires a genuinely new prediction", "examples/scientific_philosophy_review.synthetic_failed_reconstruction.json", "schemas/scientific_philosophy_review.schema.json", set_value(("revision_proposals", 1, "novel_prediction", "relation_to_prior"), "ALREADY_IMPLIED")),
    ("source extraction cannot select an operationalization", "examples/strategy_reconstruction.vwap_wave_price_discovery.json", "schemas/strategy_reconstruction.schema.json", set_value(("constructs", 0, "decision", "status"), "SELECTED")),
    ("source alternatives require at least two candidates", "examples/strategy_reconstruction.vwap_wave_price_discovery.json", "schemas/strategy_reconstruction.schema.json", set_value(("constructs", 3, "operationalization_candidates"), [])),
    ("unspecified construct requires an unresolved question", "examples/strategy_reconstruction.vwap_wave_price_discovery.json", "schemas/strategy_reconstruction.schema.json", set_value(("constructs", 0, "unresolved_questions"), [])),
    ("mechanism catalog requires literature source", "generation/mechanism_catalog.v1.json", "schemas/mechanism_catalog.schema.json", set_value(("mechanisms", 0, "literature_sources"), [])),
    ("mechanism catalog requires entry origin", "generation/mechanism_catalog.v1.json", "schemas/mechanism_catalog.schema.json", delete_value(("mechanisms", 0, "entry_origin"))),
    ("generation run uses controlled operators", "examples/generated-run/generation-run.json", "schemas/generation_run.schema.json", set_value(("request", "operators", 0), "PREMORTEM")),
    ("generation run candidate path stays relative", "examples/generated-run/generation-run.json", "schemas/generation_run.schema.json", set_value(("candidate_records", 0, "candidate_file"), "C:/tmp/candidate.json")),
    ("generated candidate requires generator source reference", "examples/generated-run/candidates/mechanism-futures-cash-price-discovery-phase-transmission.json", "schemas/hypothesis_candidate.schema.json", set_value(("provenance", "source_refs"), [])),
    ("noise screen cannot consume validation data", "examples/noise_screen.pass.json", "schemas/noise_screen.schema.json", set_value(("data_role",), "VALIDATION")),
    ("noise screen cannot consume final holdout", "examples/noise_screen.pass.json", "schemas/noise_screen.schema.json", set_value(("data_role",), "FINAL_HOLDOUT")),
    ("surrogate count below minimum is rejected", "examples/noise_screen.pass.json", "schemas/noise_screen.schema.json", set_value(("surrogate_count",), 199)),
    ("session preserving shuffle requires preserved structure", "examples/noise_screen.pass.json", "schemas/noise_screen.schema.json", set_value(("preserved_structure",), ["SESSION_PROFILE"])),
    ("BLOCKED screen requires blocking reason", "examples/noise_screen.pass.json", "schemas/noise_screen.schema.json", set_value(("screen_result",), "BLOCKED")),
    ("run rejects additional property", "examples/run_manifest.minimal.json", "schemas/run_manifest.schema.json", set_value(("unexpected_field",), True)),
    ("SUCCEEDED run requires release PASS", "examples/run_manifest.minimal.json", "schemas/run_manifest.schema.json", set_value(("operational_release", "overall_status"), "FAIL")),
    ("release PASS cannot hide failed subgate", "examples/run_manifest.minimal.json", "schemas/run_manifest.schema.json", set_value(("operational_release", "gates", "evidence_chain"), "FAIL")),
    ("claim revision is required", "examples/evidence.minimal.json", "schemas/evidence.schema.json", delete_value(("claims", 0, "claim_revision"))),
    ("evidence set id requires UUID syntax", "examples/evidence.minimal.json", "schemas/evidence.schema.json", set_value(("evidence_set_id",), "not-a-uuid")),
    ("SOURCE_FACT requires evidence link", "examples/evidence.minimal.json", "schemas/evidence.schema.json", set_value(("claims", 0, "evidence_links"), [])),
    ("SUFFICIENT evidence rejects failed check", "examples/evidence.minimal.json", "schemas/evidence.schema.json", set_value(("overall_evidence_assessment", "checks", 0, "outcome"), "FAIL")),
    ("ACADEMIC source requires academic metadata", "examples/evidence.academic.json", "schemas/evidence.schema.json", delete_value(("sources", 0, "academic_metadata"))),
    ("academic publication status is controlled", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "publication_status"), "FAMOUS_JOURNAL")),
    ("arXiv id must be version-compatible", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 1, "academic_metadata", "arxiv", "id"), "not-an-arxiv-id")),
    ("arXiv category must be q-fin taxonomy", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 1, "academic_metadata", "arxiv", "primary_category"), "cs.AI")),
    ("arXiv source requires exact version", "examples/evidence.academic.json", "schemas/evidence.schema.json", delete_value(("sources", 1, "academic_metadata", "arxiv", "version"))),
    ("modern arXiv id requires valid month", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 1, "academic_metadata", "arxiv", "id"), "2699.12345")),
    ("retraction requires notice URI", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "integrity", "status"), "RETRACTED")),
    ("open academic code requires URI", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "code_availability", "uris"), [])),
    ("academic code URI requires a URI scheme", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "code_availability", "uris"), ["not a uri"])),
    ("unavailable academic code cannot expose resource URI", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "code_availability", "status"), "NOT_AVAILABLE")),
    ("no-notice integrity status rejects notice URI", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "integrity", "notice_uri"), "https://example.org/notices/none")),
    ("academic integrity check requires ISO timestamp", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "integrity", "checked_at"), "not-a-date")),
    ("positive replication status requires source reference", "examples/evidence.academic.json", "schemas/evidence.schema.json", set_value(("sources", 0, "academic_metadata", "independent_replication", "status"), "REPLICATED")),
    ("non-academic source rejects academic metadata", "examples/evidence.minimal.json", "schemas/evidence.schema.json", add_nonacademic_metadata),
    ("identified causal lever requires identification gate PASS", "examples/constraint_assessment.causal_lever.json", "schemas/constraint_assessment.schema.json", set_value(("stage_gates", "identification"), "FAIL")),
    ("identified causal lever requires estimand reference", "examples/constraint_assessment.causal_lever.json", "schemas/constraint_assessment.schema.json", set_value(("estimand_ref",), None)),
    ("hypothesis candidate rejects additional property", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("confidence_score",), 0.95)),
    ("INBOX candidate always records consumed information references", "examples/hypothesis_candidate.inbox.json", "schemas/hypothesis_candidate.schema.json", delete_value(("consumed_data_refs",))),
    ("INBOX candidate cannot pretend that screening already occurred", "examples/hypothesis_candidate.inbox.json", "schemas/hypothesis_candidate.schema.json", set_value(("transition", "screened_at"), None)),
    ("PROMOTED candidate requires full research scope", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("research_scope",))),
    ("PROMOTED candidate requires variable-selection provenance", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("variable_selection",))),
    ("PROMOTED candidate requires noise screen or waiver", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("noise_screen_ref",))),
    ("noise screen waiver requires justification", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", replace_noise_screen_with_invalid_waiver),
    ("PROMOTED candidate requires actor constraint", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("actor_constraint",))),
    ("PROMOTED actor constraint rejects UNKNOWN observability", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("actor_constraint", "observability"), "UNKNOWN")),
    ("actor constraint requires alternative actor hypotheses", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("actor_constraint", "alternative_actor_hypotheses"))),
    ("unspecified actor cannot claim a mechanism", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("actor_constraint",), {"actor_status": "UNSPECIFIED", "mechanism_claim_status": "CLAIMED", "reason": "No defensible actor is known."})),
    ("hypothesis candidate scope requires an instrument", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("research_scope", "instruments"), [])),
    ("intraday scope requires explicit timezone", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("research_scope", "timezone"))),
    ("FILTER_KNOWN_EVENTS requires named feed coverage", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("research_scope", "news_event_coverage", "feeds"), [])),
    ("FILTER_KNOWN_EVENTS requires exclusion window", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("research_scope", "news_event_coverage", "exclusion_windows"), [])),
    ("event feed coverage requires provider provenance", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("research_scope", "news_event_coverage", "feeds", 0, "provider"))),
    ("event filtering requires an explicit timestamp convention", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", delete_value(("research_scope", "news_event_coverage", "timestamp_convention"))),
    ("PROMOTED candidate requires alternative explanation", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("alternative_explanations",), [])),
    ("PROMOTED candidate requires concrete data resolution", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("data_requirements", "minimum_resolution"), None)),
    ("PROMOTED candidate requires queue applicability screening", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("early_feasibility", "queue", "status"), "UNKNOWN")),
    ("FEASIBLE assessment cannot contain a blocked component", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("early_feasibility", "latency", "status"), "BLOCKED")),
    ("BLOCKED assessment requires a blocked feasibility component", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("early_feasibility", "assessment_status"), "BLOCKED")),
    ("MERGED candidate requires target idea", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("intake_status",), "MERGED")),
    ("REJECTED candidate requires rejection reason", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("intake_status",), "REJECTED")),
    ("epistemic stage status uses controlled independent states", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("epistemic_stage_status", "forward_predictive_oos", "status"), "PROBABLY")),
    ("supported epistemic stage requires evidence reference", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("epistemic_stage_status", "mechanism_supported", "status"), "SUPPORTED")),
    ("supported executable net edge requires supported forward OOS evidence", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", set_value(("epistemic_stage_status", "executable_net_edge", "status"), "SUPPORTED")),
    ("data-driven selection requires candidate-universe provenance", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", invalidate_data_driven_selection("candidate_universe_ref", None)),
    ("data-driven selection requires a frozen search-space reference", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", invalidate_data_driven_selection("search_space_ref", None)),
    ("data-driven selection requires selection-bias controls", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", invalidate_data_driven_selection("selection_bias_controls", [])),
    ("data-driven selection cannot use NOT_APPLICABLE data role", "examples/hypothesis_candidate.minimal.json", "schemas/hypothesis_candidate.schema.json", invalidate_data_driven_selection("selection_dataset_role", "NOT_APPLICABLE")),
    ("probability forecast requires calibration", "examples/forecast.minimal.json", "schemas/forecast.schema.json", set_value(("forecasts", 0, "prediction", "kind"), "PROBABILITY")),
    ("OPEN forecast cannot contain resolution", "examples/forecast.minimal.json", "schemas/forecast.schema.json", set_value(("forecasts", 0, "resolution"), {"resolved_at": "2026-09-01T08:00:00Z", "resolved_by": {"actor_type": "HUMAN", "actor_id": "reviewer-001"}, "actual_value": "UP", "source_refs": ["official-close-dataset"], "source_vintage": "2026-08-31", "applied_rule": "Demonstrationsregel", "score": 1, "rationale": "Aufgeloest."})),
    ("APPLIED review requires APPLIED audit event", "examples/review.minimal.json", "schemas/review.schema.json", remove_applied_review_event),
]


def apply_compound_mutations(name: str, document: dict[str, Any]) -> None:
    """Complete mutations that need several coordinated field changes."""

    if name == "SUFFICIENT evidence rejects failed check":
        document["overall_evidence_assessment"]["grade"] = "SUFFICIENT"
    elif name == "retraction requires notice URI":
        document["sources"][0]["academic_metadata"]["integrity"]["notice_uri"] = None
    elif name == "positive replication status requires source reference":
        replication = document["sources"][0]["academic_metadata"]["independent_replication"]
        replication["checked_at"] = "2026-08-30T08:10:00Z"
        replication["source_ids"] = []
    elif name == "PROMOTED candidate requires queue applicability screening":
        document["early_feasibility"]["queue"]["model"] = "UNKNOWN"
    elif name == "FEASIBLE assessment cannot contain a blocked component":
        document["early_feasibility"]["blockers"] = ["End-to-end latency has not been measured."]
    elif name == "BLOCKED assessment requires a blocked feasibility component":
        document["early_feasibility"]["blockers"] = ["Generic blocker without a mapped component."]
    elif name == "MERGED candidate requires target idea":
        transition = document["transition"]
        transition["merged_into_idea_id"] = None
        transition["promotion_conditions"] = []
        transition["promoted_research_id"] = None
    elif name == "REJECTED candidate requires rejection reason":
        transition = document["transition"]
        transition["rejection_reasons"] = []
        transition["promotion_conditions"] = []
        transition["promoted_research_id"] = None
    elif name == "supported executable net edge requires supported forward OOS evidence":
        stages = document["epistemic_stage_status"]
        stages["forward_predictive_oos"]["status"] = "NOT_SUPPORTED"
        stages["forward_predictive_oos"]["evidence_refs"] = ["validation:forward-oos-negative"]
        stages["executable_net_edge"]["evidence_refs"] = ["validation:net-edge-positive"]
    elif name == "probability forecast requires calibration":
        prediction = document["forecasts"][0]["prediction"]
        prediction["probability"] = 0.7
        prediction["calibration_ref"] = None


def main() -> int:
    validators: dict[str, Draft202012Validator] = {}
    positive_count = 0
    negative_count = 0

    for example_path, schema_path in POSITIVES:
        schema_validator = validators.setdefault(schema_path, validator(schema_path))
        errors = list(schema_validator.iter_errors(load(example_path)))
        if errors:
            print(f"Expected valid fixture was rejected: {example_path}", file=sys.stderr)
            for error in errors:
                print(f"- {error.json_path}: {error.message}", file=sys.stderr)
            return 1
        positive_count += 1
        print(f"PASS positive: {example_path}")

    intake_schema = load("schemas/hypothesis_candidate.schema.json")
    inbox = load("examples/hypothesis_candidate.inbox.json")
    if len(intake_schema["required"]) != 12:
        print("INBOX top-level required list no longer contains exactly 12 fields", file=sys.stderr)
        return 1
    if "actor_constraint" in inbox or "noise_screen_ref" in inbox or "noise_screen_waiver" in inbox:
        print("INBOX fixture was burdened with promotion-only entry fields", file=sys.stderr)
        return 1
    positive_count += 1
    print("PASS positive: INBOX remains a 12-field actor/noise-free cheap path")

    data_driven = load("examples/hypothesis_candidate.minimal.json")
    configure_data_driven_selection(data_driven)
    candidate_validator = validators.setdefault(
        "schemas/hypothesis_candidate.schema.json",
        validator("schemas/hypothesis_candidate.schema.json"),
    )
    errors = list(candidate_validator.iter_errors(data_driven))
    if errors:
        print("Expected valid data-driven candidate was rejected", file=sys.stderr)
        for error in errors:
            print(f"- {error.json_path}: {error.message}", file=sys.stderr)
        return 1
    positive_count += 1
    print("PASS positive: data-driven variable-selection provenance")

    actor_unspecified = load("examples/hypothesis_candidate.minimal.json")
    actor_unspecified["idea_class"] = "PREDICTIVE_PRECEDENCE"
    actor_unspecified["actor_constraint"] = {
        "actor_status": "UNSPECIFIED",
        "mechanism_claim_status": "NOT_CLAIMED",
        "reason": (
            "The predictive question does not identify a defensible actor; "
            "no actor or mechanism is inferred."
        ),
    }
    errors = list(candidate_validator.iter_errors(actor_unspecified))
    if errors:
        print("Expected valid actor-unspecified candidate was rejected", file=sys.stderr)
        for error in errors:
            print(f"- {error.json_path}: {error.message}", file=sys.stderr)
        return 1
    positive_count += 1
    print("PASS positive: predictive candidate may preserve an unspecified actor")

    for name, fixture_path, schema_path, mutation in NEGATIVES:
        document = load(fixture_path)
        mutation(document)
        apply_compound_mutations(name, document)
        schema_validator = validators.setdefault(schema_path, validator(schema_path))
        if schema_validator.is_valid(document):
            print(f"Expected invalid fixture was accepted: {name}", file=sys.stderr)
            return 1
        negative_count += 1
        print(f"PASS negative: {name}")

    # Separate multi-field construction for the implementation-constraint invariant.
    implementation = load("examples/constraint_assessment.causal_lever.json")
    implementation["label"] = "IMPLEMENTATION_CONSTRAINT"
    implementation["stage_gates"].update({
        "identification": "NOT_REQUIRED",
        "phenomenon_validation": "NOT_RUN",
        "implementation_feasibility": "PASS",
    })
    implementation["estimand_ref"] = None
    implementation["system_objective"] = "Executable risk-adjusted net performance"
    implementation["bottleneck_metric"] = "Median round-trip latency in milliseconds"
    if validators["schemas/constraint_assessment.schema.json"].is_valid(implementation):
        print("Expected invalid fixture was accepted: implementation constraint requires validated phenomenon", file=sys.stderr)
        return 1
    negative_count += 1
    print("PASS negative: implementation constraint requires validated phenomenon")

    print(f"Schema contract tests passed: {positive_count} positive, {negative_count} negative.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
