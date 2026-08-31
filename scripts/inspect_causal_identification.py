#!/usr/bin/env python3
"""Validate causal-identification assessments and finance-specific semantics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing development dependency 'jsonschema'. "
        "Install with: python -m pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "causal_identification_assessment.schema.json"
EVENT_DESIGNS = {"HIGH_FREQUENCY_EVENT", "FINANCIAL_EVENT_STUDY"}
EVENT_REQUIRED_RISKS = {
    "anticipation_and_leakage",
    "concurrent_events",
    "counterfactual_or_factor_model",
    "simultaneity_reverse_causality_and_information_shocks",
    "adaptive_timing_and_selection",
    "shock_dominance_and_separability",
    "market_microstructure_and_timestamps",
    "temporal_and_cross_sectional_dependence",
}
ESTIMATOR_ONLY_TEXTS = {
    "dml",
    "double machine learning",
    "causal forest",
    "local projections",
    "var",
    "event study regression",
    "regression",
    "granger causality",
    "causal discovery",
}


def load_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def validate(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path))
    ]


def semantic_errors(document: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    requested = document.get("requested_claim_level")
    design = document.get("design", {})
    judgment = document.get("judgment", {})
    status = judgment.get("identification_status")
    family = design.get("design_family")
    allowed = judgment.get("strongest_allowed_claim")

    if requested == "ASSOCIATIONAL_PREDICTIVE":
        return errors

    if status == "NOT_REQUIRED_PREDICTIVE":
        errors.append("a causal request cannot use NOT_REQUIRED_PREDICTIVE")

    source = str(design.get("assignment_or_variation_source", "")).strip().lower()
    if source in ESTIMATOR_ONLY_TEXTS:
        errors.append(
            "assignment_or_variation_source names only an estimator or discovery method; "
            "it must name the source of identifying variation"
        )

    if family == "CAUSAL_DISCOVERY_ONLY" and status == "PASS":
        errors.append("causal discovery alone cannot receive identification PASS")

    if status == "PASS":
        if judgment.get("unresolved_blockers"):
            errors.append("PASS cannot retain unresolved blockers")
        if requested != allowed:
            errors.append(
                "PASS must not authorize a stronger or different causal claim than the requested claim"
            )
        risks = document.get("finance_risk_checks", {})
        blocking = [
            name
            for name, record in risks.items()
            if isinstance(record, Mapping) and record.get("status") == "BLOCKING"
        ]
        if blocking:
            errors.append("PASS cannot contain blocking finance risks: " + ", ".join(blocking))
        if family in EVENT_DESIGNS:
            not_addressed = [
                name
                for name in sorted(EVENT_REQUIRED_RISKS)
                if not isinstance(risks.get(name), Mapping)
                or risks[name].get("status") != "ADDRESSED"
            ]
            if not_addressed:
                errors.append(
                    "event-design PASS requires explicit treatment of: "
                    + ", ".join(not_addressed)
                )

    if status in {"BLOCKED", "FAIL"}:
        if judgment.get("causal_estimation_authorized") or judgment.get(
            "causal_language_authorized"
        ):
            errors.append("BLOCKED or FAIL cannot authorize causal estimation or language")
        if not judgment.get("unresolved_blockers"):
            errors.append("BLOCKED or FAIL must state at least one unresolved blocker")
        if allowed not in {"ASSOCIATIONAL_PREDICTIVE", "CAUSAL_HYPOTHESIS"}:
            errors.append("BLOCKED or FAIL cannot retain interventional or counterfactual wording")

    assumption_types = {
        item.get("type")
        for item in document.get("identifying_assumptions", [])
        if isinstance(item, Mapping)
    }
    if status == "PASS" and family == "INSTRUMENTAL_VARIABLES":
        required = {"INSTRUMENT_RELEVANCE", "EXCLUSION_RESTRICTION"}
        if not required.issubset(assumption_types):
            errors.append("IV PASS requires relevance and exclusion assumptions")
    if status == "PASS" and family == "DID_EVENT_STUDY":
        required = {"PARALLEL_TRENDS", "NO_ANTICIPATION"}
        if not required.issubset(assumption_types):
            errors.append("DiD/event-study PASS requires parallel-trends and no-anticipation assumptions")

    estimand = document.get("estimand")
    if isinstance(estimand, Mapping) and estimand.get("effect_type") in {"DIRECT", "INDIRECT"}:
        roles = {
            item.get("role")
            for item in document.get("post_treatment_variables", [])
            if isinstance(item, Mapping)
        }
        if "MEDIATOR_SEPARATE_ESTIMAND" not in roles:
            errors.append(
                "direct or indirect effects require an explicitly separated mediator estimand"
            )

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one causal-identification assessment."
    )
    parser.add_argument("assessment", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        document = load_object(args.assessment)
        schema = load_object(args.schema)
        errors = validate(document, schema) + semantic_errors(document)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Causal-identification assessment is valid; identification, estimation, "
        "prediction, and trading claims remain separate."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
