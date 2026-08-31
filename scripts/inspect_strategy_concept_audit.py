#!/usr/bin/env python3
"""Validate and summarize a pre-operationalization strategy concept audit."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing development dependency 'jsonschema'. "
        "Install with: python -m pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "strategy_concept_audit.schema.json"


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

    source_refs = set(document.get("source_claim_refs", []))
    construct_refs = set(document.get("construct_refs", []))
    conditions = document.get("condition_map", [])
    condition_ids = [item.get("condition_id") for item in conditions if isinstance(item, Mapping)]
    condition_ids = [item for item in condition_ids if isinstance(item, str)]
    for duplicate in sorted(_duplicates(condition_ids)):
        errors.append(f"duplicate condition id {duplicate!r}")

    for item in conditions:
        if not isinstance(item, Mapping):
            continue
        condition_id = item.get("condition_id")
        unknown_source = set(item.get("source_claim_refs", [])) - source_refs
        unknown_construct = set(item.get("construct_refs", [])) - construct_refs
        if unknown_source:
            errors.append(
                f"condition {condition_id!r} references unknown source claims: "
                f"{', '.join(sorted(unknown_source))}"
            )
        if unknown_construct:
            errors.append(
                f"condition {condition_id!r} references unknown constructs: "
                f"{', '.join(sorted(unknown_construct))}"
            )

    dependencies = document.get("construction_dependencies", [])
    dependency_ids = [item.get("dependency_id") for item in dependencies if isinstance(item, Mapping)]
    dependency_ids = [item for item in dependency_ids if isinstance(item, str)]
    for duplicate in sorted(_duplicates(dependency_ids)):
        errors.append(f"duplicate construction dependency id {duplicate!r}")
    dependency_targets = source_refs | construct_refs | set(condition_ids)
    for item in dependencies:
        if not isinstance(item, Mapping):
            continue
        dependency_id = item.get("dependency_id")
        unknown = (set(item.get("from_refs", [])) | set(item.get("to_refs", []))) - dependency_targets
        if unknown:
            errors.append(
                f"construction dependency {dependency_id!r} references unknown targets: "
                f"{', '.join(sorted(unknown))}"
            )

    instruments = document.get("measurement_instruments", [])
    instrument_ids = [item.get("instrument_id") for item in instruments if isinstance(item, Mapping)]
    instrument_ids = [item for item in instrument_ids if isinstance(item, str)]
    for duplicate in sorted(_duplicates(instrument_ids)):
        errors.append(f"duplicate measurement instrument id {duplicate!r}")
    for item in instruments:
        if isinstance(item, Mapping) and item.get("construct_ref") not in construct_refs:
            errors.append(
                f"measurement instrument {item.get('instrument_id')!r} references unknown construct "
                f"{item.get('construct_ref')!r}"
            )

    if document.get("audit_status") == "COMPLETE" and not any(
        isinstance(item, Mapping) and item.get("classification") == "UNKNOWN_SUCCESS_CONDITION"
        for item in conditions
    ):
        errors.append("complete audit must preserve an UNKNOWN_SUCCESS_CONDITION entry")

    return errors


def validate(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    return schema_errors(document, schema) + semantic_errors(document)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a pre-operationalization concept audit without selecting a definition."
    )
    parser.add_argument("audit", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    audit_path = args.audit if args.audit.is_absolute() else ROOT / args.audit
    schema_path = args.schema if args.schema.is_absolute() else ROOT / args.schema
    document = load_json(audit_path)
    schema = load_json(schema_path)
    errors = validate(document, schema)
    if errors:
        print("Strategy concept audit is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    counts: dict[str, int] = {}
    for item in document["condition_map"]:
        label = item["classification"]
        counts[label] = counts.get(label, 0) + 1
    count_text = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(
        f"VALID {document['audit_id']} status={document['audit_status']} "
        f"conditions=({count_text}) dependencies={len(document['construction_dependencies'])} "
        f"instruments={len(document['measurement_instruments'])}"
    )
    print("No definition was selected and no market test or backtest was run by this command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
