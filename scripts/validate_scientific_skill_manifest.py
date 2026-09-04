#!/usr/bin/env python3
"""Validate the versioned map of optional scientific-method skills."""

from __future__ import annotations

import argparse
import json
import sys
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
SCHEMA_PATH = ROOT / "schemas" / "scientific_skill_manifest.schema.json"


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def validate_manifest(document: Mapping[str, Any]) -> list[str]:
    schema = load_object(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [f"{error.json_path}: {error.message}" for error in validator.iter_errors(document)]

    skills = document.get("skills")
    if isinstance(skills, list):
        skill_ids = [entry.get("skill_id") for entry in skills if isinstance(entry, Mapping)]
        if len(skill_ids) != len(set(skill_ids)):
            errors.append("skill_id values must be unique")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a scientific skill capability manifest.")
    parser.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        default=ROOT / "capabilities" / "scientific_skill_manifest.v1.json",
        help="manifest JSON path (defaults to the repository capability map)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        errors = validate_manifest(load_object(args.manifest))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Scientific skill manifest validation failed: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Scientific skill manifest validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Scientific skill manifest valid: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
