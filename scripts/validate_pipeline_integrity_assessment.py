#!/usr/bin/env python3
"""Validate pre-freeze pipeline controls and their claim boundaries."""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "pipeline_integrity_assessment.schema.json"


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("The assessment must contain one JSON object.")
    return value


def _mapping(value: Any, label: str, errors: list[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        errors.append(f"{label} must be an object.")
        return {}
    return value


def _parse_timestamp(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be a valid timestamp.")
        return None


def semantic_errors(assessment: Mapping[str, Any]) -> list[str]:
    """Return hard-rule errors that JSON Schema cannot express cleanly."""

    errors: list[str] = []
    status = assessment.get("status")
    raw_controls = assessment.get("controls")
    controls = raw_controls if isinstance(raw_controls, list) else []

    plan_locked_at = _parse_timestamp(
        assessment.get("plan_locked_at"), "plan_locked_at", errors
    )
    first_run_at = _parse_timestamp(
        assessment.get("first_run_at"), "first_run_at", errors
    )
    if plan_locked_at and first_run_at and plan_locked_at >= first_run_at:
        errors.append("plan_locked_at must be earlier than first_run_at.")

    control_ids: list[str] = []
    purposes: list[str] = []
    required_results: list[str] = []
    required_null_families: list[str] = []

    for index, raw_control in enumerate(controls):
        control = _mapping(raw_control, f"controls[{index}]", errors)
        control_id = control.get("control_id")
        if isinstance(control_id, str):
            control_ids.append(control_id)
        purpose = control.get("purpose")
        if isinstance(purpose, str):
            purposes.append(purpose)

        model = _mapping(control.get("model"), f"controls[{index}].model", errors)
        result = _mapping(control.get("result"), f"controls[{index}].result", errors)
        acceptance = _mapping(
            control.get("acceptance_rule"),
            f"controls[{index}].acceptance_rule",
            errors,
        )

        if control.get("required_for_gate") is True:
            result_status = result.get("status")
            if isinstance(result_status, str):
                required_results.append(result_status)
            if purpose == "NULL_NEGATIVE_CONTROL":
                family = model.get("family")
                if isinstance(family, str):
                    required_null_families.append(family)

            missing_structure = model.get("unpreserved_relevant_structure")
            if result_status == "PASS" and (
                model.get("structure_adequacy") != "ADEQUATE_FOR_PURPOSE"
                or (isinstance(missing_structure, list) and missing_structure)
            ):
                errors.append(
                    f"controls[{index}] cannot PASS a required gate with an inadequate or materially incomplete reference structure."
                )

        planned_runs = control.get("planned_runs")
        minimum_runs = acceptance.get("minimum_runs")
        actual_runs = control.get("actual_runs")
        if isinstance(planned_runs, int) and isinstance(minimum_runs, int):
            if planned_runs < minimum_runs:
                errors.append(
                    f"controls[{index}].planned_runs cannot be below its frozen minimum_runs."
                )
        if status == "ASSESSED" and isinstance(actual_runs, int) and isinstance(minimum_runs, int):
            if actual_runs < minimum_runs:
                errors.append(
                    f"controls[{index}].actual_runs did not reach its frozen minimum_runs."
                )
            evidence_refs = result.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                errors.append(
                    f"controls[{index}] needs result evidence once the assessment is ASSESSED."
                )

    if len(control_ids) != len(set(control_ids)):
        errors.append("control_id values must be unique within the assessment.")
    if "NULL_NEGATIVE_CONTROL" not in purposes:
        errors.append("At least one required NULL_NEGATIVE_CONTROL is mandatory.")
    if "POSITIVE_SENTINEL" not in purposes:
        errors.append("At least one required POSITIVE_SENTINEL is mandatory.")
    if assessment.get("causal_tooling_required") is True and "CAUSAL_TOOL_SENTINEL" not in purposes:
        errors.append(
            "causal_tooling_required needs a required CAUSAL_TOOL_SENTINEL."
        )
    if set(required_null_families) == {"RANDOM_WALK"}:
        errors.append(
            "A RANDOM_WALK cannot be the only required negative control; use a control that preserves the material dependency structure."
        )

    if status == "ASSESSED":
        if "FAIL" in required_results:
            expected_gate = "FAIL"
        elif "BLOCKED" in required_results:
            expected_gate = "BLOCKED"
        elif required_results and all(item == "PASS" for item in required_results):
            expected_gate = "PASS"
        else:
            expected_gate = None
            errors.append("Every required control must have an assessed result.")
        if expected_gate and assessment.get("overall_gate") != expected_gate:
            errors.append(
                f"overall_gate must be {expected_gate} from the required control results."
            )

    return errors


def schema_errors(assessment: Mapping[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:  # pragma: no cover - environment failure.
        raise RuntimeError(
            "Missing development dependency 'jsonschema'. Install requirements-dev.txt."
        ) from exc

    schema = load_object(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{error.json_path}: {error.message}"
        for error in validator.iter_errors(assessment)
    ]


def validate_assessment(assessment: Mapping[str, Any], *, base_dir: Path = ROOT) -> list[str]:
    errors = schema_errors(assessment)
    if errors:
        return errors
    errors += semantic_errors(assessment)
    for control in assessment["controls"]:
        rule = control["acceptance_rule"]
        n = control["planned_runs"]
        floor = max(200, math.ceil(0.25 / rule["maximum_standard_error"] ** 2))
        if rule["minimum_runs"] < floor or n < rule["minimum_runs"]:
            errors.append("Replication budget does not meet the prospective worst-case Bernoulli precision bound.")
        if len(control["seeds"]) != n:
            errors.append("A complete unique seed list is required for every planned replication.")
        if rule["pass_rate_min"] > rule["pass_rate_max"]:
            errors.append("Numerical acceptance interval is reversed.")
        if assessment["status"] == "ASSESSED" and control["actual_runs"] != n:
            errors.append("Completed replications must equal the locked planned count.")
    null_maxima = [c['acceptance_rule']['pass_rate_max'] for c in assessment['controls']
                   if c['purpose'] == 'NULL_NEGATIVE_CONTROL' and c['required_for_gate']]
    for control in assessment['controls']:
        if control['purpose'] in {'POSITIVE_SENTINEL', 'CAUSAL_TOOL_SENTINEL'} and null_maxima:
            if control['acceptance_rule']['pass_rate_min'] <= max(null_maxima):
                errors.append('Known-effect sentinel must require a detection rate above every null acceptance interval.')
    try:
        from pipeline_execution import verify_plan, execution_errors
        verify_plan(assessment, base_dir)
        if assessment["status"] == "ASSESSED":
            errors += execution_errors(assessment, base_dir)
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        errors.append(f"Missing or invalid pipeline execution evidence: {exc}")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one pre-freeze pipeline-integrity assessment."
    )
    parser.add_argument("assessment", type=Path, help="Assessment JSON file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        assessment = load_object(args.assessment)
        errors = validate_assessment(assessment, base_dir=args.assessment.resolve().parent)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"Pipeline integrity validation failed: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Pipeline integrity assessment passed schema and semantic validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
