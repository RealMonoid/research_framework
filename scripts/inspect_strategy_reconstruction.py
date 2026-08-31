#!/usr/bin/env python3
"""Validate and summarize a prose-strategy reconstruction artifact.

This command performs structural and reference-integrity checks only. It does
not select an operationalization, construct a trading rule, access market data,
or run a backtest.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "strategy_reconstruction.schema.json"


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def duplicates(values: Sequence[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def semantic_errors(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    locator_ids = [item["locator_id"] for item in document["source"]["locators_reviewed"]]
    claim_ids = [item["claim_id"] for item in document["source_claims"]]
    construct_ids = [item["construct_id"] for item in document["constructs"]]

    for label, values in (
        ("source locator", locator_ids),
        ("source claim", claim_ids),
        ("construct", construct_ids),
    ):
        repeated = duplicates(values)
        if repeated:
            errors.append(f"Duplicate {label} IDs: {', '.join(repeated)}")

    locator_set = set(locator_ids)
    claim_set = set(claim_ids)
    claim_by_id = {item["claim_id"]: item for item in document["source_claims"]}

    unknown_scope = sorted(set(document["translation_scope"]["included"]) - locator_set)
    if unknown_scope:
        errors.append(f"Translation scope references unknown locators: {', '.join(unknown_scope)}")

    for claim in document["source_claims"]:
        unknown = sorted(set(claim["source_locator_refs"]) - locator_set)
        if unknown:
            errors.append(
                f"Claim {claim['claim_id']} references unknown locators: {', '.join(unknown)}"
            )

    for claim_ref in document["strategy_identity_claim_refs"]:
        if claim_ref not in claim_set:
            errors.append(f"Strategy identity references unknown claim: {claim_ref}")
        elif not claim_by_id[claim_ref]["core_to_strategy"]:
            errors.append(f"Strategy identity claim is not marked core_to_strategy: {claim_ref}")

    complete = document["reconstruction_status"] in {
        "RECONSTRUCTION_COMPLETE",
        "DISCRETIONARY_PROTOCOL_COMPLETE",
    }

    for construct in document["constructs"]:
        construct_id = construct["construct_id"]
        unknown_claims = sorted(set(construct["source_claim_refs"]) - claim_set)
        if unknown_claims:
            errors.append(
                f"Construct {construct_id} references unknown claims: {', '.join(unknown_claims)}"
            )

        candidates = construct["operationalization_candidates"]
        candidate_ids = [item["candidate_id"] for item in candidates]
        repeated_candidates = duplicates(candidate_ids)
        if repeated_candidates:
            errors.append(
                f"Construct {construct_id} has duplicate candidate IDs: "
                f"{', '.join(repeated_candidates)}"
            )

        decision = construct["decision"]
        chosen_id = decision["chosen_candidate_id"]
        if chosen_id is not None and chosen_id not in set(candidate_ids):
            errors.append(
                f"Construct {construct_id} chooses an unknown candidate: {chosen_id}"
            )

        if complete and construct["unresolved_questions"]:
            errors.append(
                f"Complete reconstruction retains unresolved questions in {construct_id}"
            )

    if document["fidelity_label"] == "REPLICATION":
        non_exact = [
            item["construct_id"]
            for item in document["constructs"]
            if item["source_status"] != "SOURCE_SPECIFIED"
        ]
        if non_exact:
            errors.append(
                "REPLICATION is not permitted while source definitions are alternative, "
                "unspecified, discretionary or contradictory: " + ", ".join(non_exact)
            )

    return errors


def validate(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: item.json_path)
    ]
    errors.extend(semantic_errors(document))
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate and summarize a source-to-operationalization reconstruction. "
            "No choices or market tests are performed."
        )
    )
    parser.add_argument("artifact", type=Path, help="Reconstruction JSON to inspect")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    artifact_path = args.artifact if args.artifact.is_absolute() else ROOT / args.artifact
    schema_path = args.schema if args.schema.is_absolute() else ROOT / args.schema

    try:
        document = load_object(artifact_path)
        schema = load_object(schema_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    errors = validate(document, schema)
    if errors:
        print("Strategy reconstruction is invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    source_counts = Counter(item["source_status"] for item in document["constructs"])
    decision_counts = Counter(item["decision"]["status"] for item in document["constructs"])
    candidate_count = sum(
        len(item["operationalization_candidates"]) for item in document["constructs"]
    )
    open_question_count = sum(len(item["unresolved_questions"]) for item in document["constructs"])

    print(f"VALID {document['reconstruction_id']}")
    print(
        f"status={document['reconstruction_status']} "
        f"fidelity={document['fidelity_label']} "
        f"concept_audit={document['concept_audit']['status']} "
        f"claims={len(document['source_claims'])} "
        f"constructs={len(document['constructs'])}"
    )
    print(
        "source_status="
        + ",".join(f"{key}:{source_counts[key]}" for key in sorted(source_counts))
    )
    print(
        "decisions="
        + ",".join(f"{key}:{decision_counts[key]}" for key in sorted(decision_counts))
    )
    print(f"candidates={candidate_count} unresolved_questions={open_question_count}")
    print("No operationalization was selected and no market test was run by this command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
