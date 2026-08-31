#!/usr/bin/env python3
"""Validate and summarize a quantitative condition-inquiry artifact."""

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
DEFAULT_SCHEMA = ROOT / "schemas" / "condition_inquiry.schema.json"


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

    candidates = document.get("candidate_conditions", [])
    candidate_ids = [item.get("condition_id") for item in candidates if isinstance(item, Mapping)]
    candidate_ids = [item for item in candidate_ids if isinstance(item, str)]
    for duplicate in sorted(_duplicates(candidate_ids)):
        errors.append(f"duplicate candidate condition id {duplicate!r}")

    methods = document.get("method_plan", [])
    method_ids = [item.get("method_id") for item in methods if isinstance(item, Mapping)]
    method_ids = [item for item in method_ids if isinstance(item, str)]
    for duplicate in sorted(_duplicates(method_ids)):
        errors.append(f"duplicate method id {duplicate!r}")

    if document.get("inquiry_status") == "PLAN":
        for item in candidates:
            if isinstance(item, Mapping) and item.get("status") != "UNEXAMINED":
                errors.append("PLAN inquiry cannot report examined candidate-condition results")

    if document.get("inquiry_status") == "INDEPENDENT_RESULTS" and not any(
        isinstance(item, Mapping) and item.get("stage") == "INDEPENDENT_EVALUATION"
        for item in methods
    ):
        errors.append("INDEPENDENT_RESULTS requires an INDEPENDENT_EVALUATION method")

    if document.get("purpose") == "PERFORMANCE_MODIFIER_DISCOVERY" and not candidates:
        errors.append("PERFORMANCE_MODIFIER_DISCOVERY requires candidate_conditions")

    return errors


def validate(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    return schema_errors(document, schema) + semantic_errors(document)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a condition-inquiry plan or result without executing it."
    )
    parser.add_argument("inquiry", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    inquiry_path = args.inquiry if args.inquiry.is_absolute() else ROOT / args.inquiry
    schema_path = args.schema if args.schema.is_absolute() else ROOT / args.schema
    document = load_json(inquiry_path)
    schema = load_json(schema_path)
    errors = validate(document, schema)
    if errors:
        print("Condition inquiry is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"VALID {document['inquiry_id']} purpose={document['purpose']} "
        f"status={document['inquiry_status']} methods={len(document['method_plan'])} "
        f"candidate_conditions={len(document['candidate_conditions'])}"
    )
    print("This command validated the record; it did not execute a market test or backtest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
