#!/usr/bin/env python3
"""Validate one separately stored research-workflow problem record."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - environment failure.
    raise SystemExit(
        "Missing development dependency 'jsonschema'. "
        "Install with: python -m pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "problem_record.schema.json"


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("input must contain one JSON object")
    return value


def _parse_timestamp(value: Any, field: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{field} is not an ISO 8601 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{field} must include a timezone")
        return None
    return parsed


def validate_problem_record(document: Mapping[str, Any]) -> list[str]:
    schema = load_object(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: item.json_path)
    ]
    if errors:
        return errors

    occurred_at = _parse_timestamp(document.get("occurred_at"), "occurred_at", errors)
    recorded_at = _parse_timestamp(document.get("recorded_at"), "recorded_at", errors)
    if occurred_at is not None and recorded_at is not None and recorded_at < occurred_at:
        errors.append("recorded_at cannot precede occurred_at")

    options = document.get("resolution_options")
    if not isinstance(options, list):  # Schema validation above makes this defensive.
        return errors
    option_ids = [option.get("option_id") for option in options if isinstance(option, Mapping)]
    if len(option_ids) != len(set(option_ids)):
        errors.append("resolution_options must use unique option_id values")
    recommended_option_id = document.get("recommended_option_id")
    if recommended_option_id not in option_ids:
        errors.append("recommended_option_id must identify one listed resolution option")
    recommended = [
        option
        for option in options
        if isinstance(option, Mapping) and option.get("assessment") == "RECOMMENDED"
    ]
    if len(recommended) != 1:
        errors.append("resolution_options must contain exactly one RECOMMENDED option")
    elif recommended[0].get("option_id") != recommended_option_id:
        errors.append("recommended_option_id must identify the RECOMMENDED option")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one separately stored research-workflow problem record."
    )
    parser.add_argument("problem_record", type=Path, help="Path to one problem-record JSON file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        errors = validate_problem_record(load_object(args.problem_record))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Problem-record validation failed: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Problem-record validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Problem record valid: {args.problem_record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
