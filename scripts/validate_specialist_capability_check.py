#!/usr/bin/env python3
"""Validate one specialist capability-discovery record and optional route binding."""

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
SCHEMA_PATH = ROOT / "schemas" / "specialist_capability_check.schema.json"


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("input must contain one JSON object")
    return value


def validate_specialist_capability_check(
    document: Mapping[str, Any], routing_decision: Mapping[str, Any] | None = None
) -> list[str]:
    schema = load_object(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: item.json_path)
    ]
    if errors:
        return errors

    required = set(document["required_capabilities"])
    interfaces = document["interfaces"]
    capable = [
        interface
        for interface in interfaces
        if interface["availability"] == "AVAILABLE"
        and required.issubset(set(interface["capabilities"]))
    ]
    capable_ids = {interface["interface_id"] for interface in capable}
    status = document["status"]
    selected = document["selected_interface_id"]
    next_action = document["next_action"]
    discovery = document["discovery"]

    if capable:
        if status != "AVAILABLE":
            errors.append(
                "status must be AVAILABLE when an inspected invocation interface satisfies every required capability"
            )
        if selected not in capable_ids:
            errors.append(
                "selected_interface_id must identify an available interface that satisfies every required capability"
            )
        if next_action != "INVOKE_SPECIALIST":
            errors.append("a capable interface requires next_action INVOKE_SPECIALIST")
    elif status == "AVAILABLE":
        errors.append("AVAILABLE requires one inspected interface with every required capability")

    if status == "UNAVAILABLE":
        if discovery["search_complete"] is not True:
            errors.append("UNAVAILABLE requires a complete capability search")
        if any(interface["availability"] == "UNKNOWN" for interface in interfaces):
            errors.append("UNAVAILABLE cannot retain an interface with UNKNOWN availability")
        if selected is not None:
            errors.append("UNAVAILABLE cannot select an invocation interface")
        if next_action != "RECORD_UNAVAILABILITY_BLOCKER":
            errors.append("UNAVAILABLE requires next_action RECORD_UNAVAILABILITY_BLOCKER")
    elif status == "UNKNOWN":
        if discovery["search_complete"] is not False:
            errors.append("UNKNOWN requires an incomplete capability search")
        if selected is not None:
            errors.append("UNKNOWN cannot select an invocation interface")
        if next_action != "RETRY_DISCOVERY":
            errors.append("UNKNOWN requires next_action RETRY_DISCOVERY")

    if routing_decision is not None:
        if routing_decision.get("execution_mode") != "SPECIALIST_AS_TOOL":
            errors.append("the referenced routing decision must require SPECIALIST_AS_TOOL")
        if document["routing_decision_ref"] != routing_decision.get("decision_id"):
            errors.append("routing_decision_ref does not match the supplied routing decision")
        if document["orchestration_ref"] != routing_decision.get("orchestration_ref"):
            errors.append("orchestration_ref does not match the supplied routing decision")
        if document["required_specialist"] != routing_decision.get("selected_agent"):
            errors.append("required_specialist does not match the routed specialist")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one specialist capability-discovery record."
    )
    parser.add_argument("capability_check", type=Path)
    parser.add_argument(
        "--routing-decision",
        type=Path,
        help="Optional routing decision that the capability check must match.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        check = load_object(args.capability_check)
        decision = load_object(args.routing_decision) if args.routing_decision else None
        errors = validate_specialist_capability_check(check, decision)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Specialist capability-check validation failed: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Specialist capability-check validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Specialist capability check valid: {args.capability_check}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
