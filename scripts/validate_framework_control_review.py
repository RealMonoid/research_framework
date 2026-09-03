#!/usr/bin/env python3
"""Validate a bounded provider-neutral framework-control review."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - environment failure.
    raise SystemExit(
        "Missing development dependency 'jsonschema'. "
        "Install with: python -m pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "framework_control_review.schema.json"
DEFAULT_EXAMPLE = ROOT / "examples" / "framework_control_review.synthetic.json"


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
        for error in sorted(
            validator.iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def semantic_errors(document: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    try:
        created_at = datetime.fromisoformat(str(document["created_at"]).replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(str(document["updated_at"]).replace("Z", "+00:00"))
        if updated_at < created_at:
            errors.append("updated_at precedes created_at")
    except (KeyError, TypeError, ValueError):
        pass

    finding = document.get("finding", {})
    action = document.get("corrective_action", {})
    regression = document.get("regression", {})
    disposition = document.get("disposition")

    if isinstance(finding, Mapping) and isinstance(action, Mapping):
        finding_status = finding.get("status")
        action_status = action.get("status")
        if finding_status == "NOT_CONFIRMED" and action_status == "APPLIED":
            errors.append("an unconfirmed finding cannot have an applied correction")

    if isinstance(action, Mapping) and isinstance(regression, Mapping):
        if action.get("status") == "APPLIED" and regression.get("result") != "PASS":
            errors.append("an applied correction requires a passing regression")

    if disposition == "CLOSED" and (
        not isinstance(regression, Mapping) or regression.get("result") != "PASS"
    ):
        errors.append("CLOSED disposition requires a passing regression")

    if disposition == "NOT_CONFIRMED" and (
        not isinstance(finding, Mapping) or finding.get("status") != "NOT_CONFIRMED"
    ):
        errors.append("NOT_CONFIRMED disposition requires a NOT_CONFIRMED finding")

    if disposition == "CHANGE_PROPOSED":
        if not isinstance(finding, Mapping) or finding.get("material_state_change") not in {
            "VISIBLE_CHANGE_PROPOSAL",
            "NEW_RESEARCH_VERSION",
            "USER_DECISION_REQUIRED",
        }:
            errors.append(
                "CHANGE_PROPOSED disposition requires a visible material-state proposal"
            )

    if isinstance(finding, Mapping) and finding.get("status") == "CONFIRMED":
        if not isinstance(finding.get("protected_intent"), str):
            errors.append("a confirmed finding must name the protected intent")

    if document.get("research_state_unchanged") is not True:
        errors.append("framework-control review cannot change the effective research state")
    if document.get("no_private_chain_of_thought") is not True:
        errors.append("framework-control review must not request or expose private chain-of-thought")

    return errors


def validate(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    return schema_errors(document, schema) + semantic_errors(document)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a bounded workflow-control review without running research."
    )
    parser.add_argument("review", type=Path, nargs="?", default=DEFAULT_EXAMPLE)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    review_path = args.review if args.review.is_absolute() else ROOT / args.review
    schema_path = args.schema if args.schema.is_absolute() else ROOT / args.schema
    document = load_json(review_path)
    schema = load_json(schema_path)
    errors = validate(document, schema)
    if errors:
        print("Framework-control review is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Valid framework-control review {document['review_id']}: "
        f"mode={document['mode']}, finding={document['finding']['status']}, "
        f"disposition={document['disposition']}."
    )
    print("The effective research state is unchanged; no backtest or market test was run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
