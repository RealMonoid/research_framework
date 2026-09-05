#!/usr/bin/env python3
"""Validate outcome-role contracts and their cross-field decision rules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "outcome_evidence_contract.schema.json"

TARGET_TO_STAGE = {
    "PHENOMENON": "phenomenon",
    "FORWARD_PREDICTIVE_OOS": "forward_predictive_oos",
    "MECHANISM_SUPPORTED": "mechanism_supported",
    "EXECUTABLE_NET_EDGE": "executable_net_edge",
}

RESULT_TO_EFFECT = {
    "SUPPORTED": "support_effect",
    "CONTRADICTED": "contradiction_effect",
    "NON_DISCRIMINATING": "non_discriminating_effect",
    "INVALID_TEST": "invalid_test_effect",
}

FORCED_STAGE_STATUS = {
    "TARGET_NOT_SUPPORTED": "NOT_SUPPORTED",
    "TARGET_BLOCKED": "BLOCKED",
}


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("The contract must contain one JSON object.")
    return value


def _mapping(value: Any, label: str, errors: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        errors.append(f"{label} must be an object.")
        return {}
    return value


def semantic_errors(contract: Mapping[str, Any]) -> list[str]:
    """Return hard-rule errors not expressible cleanly in JSON Schema."""

    errors: list[str] = []
    status = contract.get("status")
    raw_outcomes = contract.get("outcomes")
    outcomes = raw_outcomes if isinstance(raw_outcomes, list) else []

    outcome_ids: list[str] = []
    primary_count = 0
    used_targets: set[str] = set()

    for index, raw_outcome in enumerate(outcomes):
        outcome = _mapping(raw_outcome, f"outcomes[{index}]", errors)
        outcome_id = outcome.get("outcome_id")
        if isinstance(outcome_id, str):
            outcome_ids.append(outcome_id)
        if outcome.get("role") == "PRIMARY":
            primary_count += 1
        target = outcome.get("target")
        if isinstance(target, str) and target != "NONE":
            used_targets.add(target)

        coupling = _mapping(
            outcome.get("mechanical_coupling"),
            f"outcomes[{index}].mechanical_coupling",
            errors,
        )
        coupling_status = coupling.get("status")
        if status in {"FROZEN", "ASSESSED"} and coupling_status == "UNKNOWN":
            errors.append(
                f"outcomes[{index}] cannot retain UNKNOWN mechanical coupling once the contract is {status}."
            )
        related = coupling.get("related_element_refs")
        if isinstance(outcome_id, str) and isinstance(related, list) and outcome_id in related:
            errors.append(
                f"outcomes[{index}].mechanical_coupling cannot refer to its own outcome_id."
            )

    if len(outcome_ids) != len(set(outcome_ids)):
        errors.append("outcome_id values must be unique within the contract.")
    if primary_count < 1:
        errors.append("At least one PRIMARY outcome is required.")

    raw_transport = contract.get("transportability_by_target")
    transport = raw_transport if isinstance(raw_transport, list) else []
    transport_targets = [
        item.get("target") for item in transport if isinstance(item, Mapping)
    ]
    if len(transport_targets) != len(set(transport_targets)):
        errors.append("transportability_by_target may contain each target only once.")
    missing_transport = sorted(used_targets - set(transport_targets))
    if missing_transport:
        errors.append(
            "Every material outcome target needs its own transportability record; missing: "
            + ", ".join(missing_transport)
            + "."
        )

    stages = _mapping(contract.get("stage_conclusions"), "stage_conclusions", errors)
    forced: dict[str, set[str]] = {}
    supported_targets: set[str] = set()

    if status == "ASSESSED":
        for index, raw_outcome in enumerate(outcomes):
            outcome = _mapping(raw_outcome, f"outcomes[{index}]", errors)
            target = outcome.get("target")
            if target not in TARGET_TO_STAGE:
                continue
            assessment = _mapping(
                outcome.get("assessment"), f"outcomes[{index}].assessment", errors
            )
            result = assessment.get("result")
            decision_rule = _mapping(
                outcome.get("decision_rule"),
                f"outcomes[{index}].decision_rule",
                errors,
            )
            effect_field = RESULT_TO_EFFECT.get(result)
            effect = decision_rule.get(effect_field) if effect_field else None
            if result == "SUPPORTED" and effect == "MAY_SUPPORT_TARGET":
                supported_targets.add(target)
            forced_status = FORCED_STAGE_STATUS.get(effect)
            if forced_status:
                forced.setdefault(target, set()).add(forced_status)

        for target, required_statuses in forced.items():
            if len(required_statuses) > 1:
                errors.append(
                    f"The frozen outcome rules force conflicting conclusions for {target}: "
                    + ", ".join(sorted(required_statuses))
                    + "."
                )
                continue
            stage_name = TARGET_TO_STAGE[target]
            stage = _mapping(stages.get(stage_name), f"stage_conclusions.{stage_name}", errors)
            required_status = next(iter(required_statuses))
            if stage.get("status") != required_status:
                errors.append(
                    f"{stage_name} must be {required_status} because a frozen outcome rule requires it."
                )

        for target, stage_name in TARGET_TO_STAGE.items():
            stage = _mapping(stages.get(stage_name), f"stage_conclusions.{stage_name}", errors)
            if stage.get("status") == "SUPPORTED" and target not in supported_targets:
                errors.append(
                    f"{stage_name} cannot be SUPPORTED without a supported outcome that targets it."
                )

        mechanism = _mapping(
            stages.get("mechanism_supported"),
            "stage_conclusions.mechanism_supported",
            errors,
        )
        prediction = _mapping(
            stages.get("forward_predictive_oos"),
            "stage_conclusions.forward_predictive_oos",
            errors,
        )
        edge = _mapping(
            stages.get("executable_net_edge"),
            "stage_conclusions.executable_net_edge",
            errors,
        )
        if edge.get("status") == "SUPPORTED" and prediction.get("status") != "SUPPORTED":
            errors.append(
                "executable_net_edge cannot be SUPPORTED unless forward_predictive_oos is SUPPORTED."
            )
        if mechanism.get("status") == "SUPPORTED" and "MECHANISM_SUPPORTED" in forced:
            errors.append(
                "A mechanism conclusion cannot remain SUPPORTED after a required mechanism diagnostic contradicts or blocks it."
            )


    return errors


def schema_errors(contract: Mapping[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:  # pragma: no cover - environment failure.
        raise RuntimeError(
            "Missing development dependency 'jsonschema'. Install requirements-dev.txt."
        ) from exc

    schema = load_object(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{error.json_path}: {error.message}" for error in validator.iter_errors(contract)]


def validate_contract(contract: Mapping[str, Any], *, base_dir: Path = ROOT) -> list[str]:
    from validation_execution import protocol_errors, fingerprint_errors, execution_errors
    errors = schema_errors(contract)
    if errors:
        return errors
    errors += semantic_errors(contract)
    try:
        if "validation_protocol" in contract:
            errors += protocol_errors(contract["validation_protocol"])
        if contract["status"] in {"FROZEN", "ASSESSED"}:
            errors += fingerprint_errors(contract, base_dir)
        if contract["status"] == "ASSESSED":
            deviations = execution_errors(contract, base_dir)
            expected = {"status": "INVALID_TEST" if deviations else "VALID", "violations": deviations}
            if contract["execution_validation"] != expected:
                errors.append("INVALID_TEST: execution classification must equal the computed violations: " + repr(expected))
            if deviations:
                for outcome in contract["outcomes"]:
                    if outcome["assessment"]["result"] != "INVALID_TEST":
                        errors.append("INVALID_TEST: an invalid execution cannot support or contradict an outcome.")
                for stage in contract["stage_conclusions"].values():
                    if stage["status"] == "SUPPORTED":
                        errors.append("INVALID_TEST: an invalid execution cannot support any evidence stage.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"INVALID_TEST: missing or invalid execution/protocol evidence: {exc}")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one outcome evidence contract against schema and hard decision rules."
    )
    parser.add_argument("contract", type=Path, help="Outcome evidence contract JSON file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        contract = load_object(args.contract)
        errors = validate_contract(contract, base_dir=args.contract.resolve().parent)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"Outcome evidence contract validation failed: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if contract.get("execution_validation", {}).get("status") == "INVALID_TEST":
        print("Outcome record is consistent: INVALID_TEST; no prediction or edge support is permitted.")
    else:
        print("Outcome evidence contract passed schema and semantic validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
