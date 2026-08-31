#!/usr/bin/env python3
"""Validate and summarize a scientific-philosophy continuation review."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - environment failure.
    raise SystemExit(
        "Missing development dependency 'jsonschema'. "
        "Install with: python -m pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "scientific_philosophy_review.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _json_path(parts: Iterable[Any]) -> str:
    return ".".join(str(part) for part in parts) or "$"


def schema_errors(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{_json_path(error.absolute_path)}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def _duplicates(values: Sequence[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def semantic_errors(document: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    try:
        created_at = datetime.fromisoformat(str(document["created_at"]).replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(str(document["updated_at"]).replace("Z", "+00:00"))
        if updated_at < created_at:
            errors.append("updated_at precedes created_at")
    except (KeyError, TypeError, ValueError):
        pass

    bundle = document.get("test_bundle", {})
    core_claims = bundle.get("core_claims", []) if isinstance(bundle, Mapping) else []
    assumptions = bundle.get("auxiliary_assumptions", []) if isinstance(bundle, Mapping) else []
    core_ids = [item.get("claim_id") for item in core_claims if isinstance(item, Mapping)]
    assumption_ids = [item.get("assumption_id") for item in assumptions if isinstance(item, Mapping)]
    core_ids = [item for item in core_ids if isinstance(item, str)]
    assumption_ids = [item for item in assumption_ids if isinstance(item, str)]

    for duplicate in sorted(_duplicates(core_ids)):
        errors.append(f"duplicate core claim id {duplicate!r}")
    for duplicate in sorted(_duplicates(assumption_ids)):
        errors.append(f"duplicate auxiliary assumption id {duplicate!r}")
    for collision in sorted(set(core_ids) & set(assumption_ids)):
        errors.append(f"bundle id is used as both core claim and assumption: {collision!r}")

    bundle_ids = set(core_ids) | set(assumption_ids)
    underdetermination = document.get("underdetermination", {})
    failure_points = (
        underdetermination.get("candidate_failure_points", [])
        if isinstance(underdetermination, Mapping)
        else []
    )
    failure_point_ids = [
        item.get("failure_point_id")
        for item in failure_points
        if isinstance(item, Mapping) and isinstance(item.get("failure_point_id"), str)
    ]
    for duplicate in sorted(_duplicates(failure_point_ids)):
        errors.append(f"duplicate failure point id {duplicate!r}")
    for item in failure_points:
        if isinstance(item, Mapping) and item.get("target_ref") not in bundle_ids:
            errors.append(
                f"failure point {item.get('failure_point_id')!r} references unknown bundle target "
                f"{item.get('target_ref')!r}"
            )

    programme = document.get("research_program", {})
    if isinstance(programme, Mapping):
        for reference in programme.get("hard_core_claim_refs", []):
            if reference not in set(core_ids):
                errors.append(f"hard-core reference {reference!r} is not a core claim")
        for reference in programme.get("protective_belt_assumption_refs", []):
            if reference not in set(assumption_ids):
                errors.append(f"protective-belt reference {reference!r} is not an auxiliary assumption")
        anomaly = programme.get("anomaly_assessment", {})
        if isinstance(anomaly, Mapping):
            rivals = anomaly.get("rival_program_refs", [])
            viable = anomaly.get("viable_rival_available")
            if viable is True and not rivals:
                errors.append("viable_rival_available=true requires at least one rival_program_ref")
            if viable is False and rivals:
                errors.append("rival_program_refs must be empty when no viable rival is available")

    proposals = document.get("revision_proposals", [])
    proposal_ids = [
        item.get("revision_id")
        for item in proposals
        if isinstance(item, Mapping) and isinstance(item.get("revision_id"), str)
    ]
    for duplicate in sorted(_duplicates(proposal_ids)):
        errors.append(f"duplicate revision id {duplicate!r}")
    proposals_by_id = {
        item["revision_id"]: item
        for item in proposals
        if isinstance(item, Mapping) and isinstance(item.get("revision_id"), str)
    }
    for proposal in proposals:
        if not isinstance(proposal, Mapping):
            continue
        proposal_id = proposal.get("revision_id")
        for target in proposal.get("target_refs", []):
            if target not in bundle_ids:
                errors.append(f"revision {proposal_id!r} references unknown bundle target {target!r}")
        if (
            proposal.get("timing") == "AFTER_RESULT"
            and proposal.get("classification") != "DIAGNOSTIC_ONLY"
            and proposal.get("new_research_id_required") is not True
        ):
            errors.append(
                f"post-result revision {proposal_id!r} must require a new Research-ID"
            )
        if proposal.get("classification") == "PROGRESSIVE":
            proposed_research_id = proposal.get("proposed_research_id")
            if proposed_research_id == document.get("research_id"):
                errors.append(
                    f"progressive revision {proposal_id!r} reuses the original Research-ID"
                )

    continuation = document.get("continuation", {})
    if isinstance(continuation, Mapping):
        selected_ref = continuation.get("selected_revision_ref")
        if selected_ref is not None and selected_ref not in proposals_by_id:
            errors.append(f"continuation selects unknown revision {selected_ref!r}")
        if continuation.get("disposition") == "NEW_RESEARCH_ID":
            selected = proposals_by_id.get(selected_ref)
            if not isinstance(selected, Mapping):
                pass
            else:
                if selected.get("classification") != "PROGRESSIVE":
                    errors.append("NEW_RESEARCH_ID continuation must select a PROGRESSIVE revision")
                if selected.get("authorizes_empirical_continuation") is not True:
                    errors.append("selected revision does not authorize empirical continuation")
                if continuation.get("new_research_id") != selected.get("proposed_research_id"):
                    errors.append(
                        "continuation.new_research_id does not match the selected progressive proposal"
                    )
                if continuation.get("new_research_id") == document.get("research_id"):
                    errors.append("continuation reuses the original Research-ID")
        elif continuation.get("new_research_id") is not None:
            errors.append("new_research_id is only allowed for disposition NEW_RESEARCH_ID")

    return errors


def validate(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    return schema_errors(document, schema) + semantic_errors(document)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a Duhem-Quine/Lakatos/Kuhn continuation review without running a market test."
    )
    parser.add_argument("review", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    review_path = args.review if args.review.is_absolute() else ROOT / args.review
    schema_path = args.schema if args.schema.is_absolute() else ROOT / args.schema
    document = load_json(review_path)
    schema = load_json(schema_path)
    errors = validate(document, schema)
    if errors:
        print("Scientific-philosophy review is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    classifications: dict[str, int] = {}
    for proposal in document["revision_proposals"]:
        classification = proposal["classification"]
        classifications[classification] = classifications.get(classification, 0) + 1
    classification_text = ", ".join(
        f"{key}={value}" for key, value in sorted(classifications.items())
    ) or "no revisions"
    print(
        f"Valid scientific-philosophy review {document['review_id']}: "
        f"frozen={document['frozen_result']['status']}, "
        f"attribution={document['underdetermination']['attribution_status']}, "
        f"{classification_text}, disposition={document['continuation']['disposition']}."
    )
    print("The original frozen result remains unchanged; no market test or backtest was run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
