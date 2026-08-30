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


POSITIVES = [
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
