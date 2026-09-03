#!/usr/bin/env python3
"""Validate a bounded quantitative data-analysis report without executing it."""

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
DEFAULT_SCHEMA = ROOT / "schemas" / "data_analysis_report.schema.json"


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
            validator.iter_errors(document), key=lambda item: list(item.absolute_path)
        )
    ]


def _parse_timestamp(value: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


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
    created = _parse_timestamp(document.get("created_at"))
    updated = _parse_timestamp(document.get("updated_at"))
    if created is not None and updated is not None and updated < created:
        errors.append("updated_at precedes created_at")

    data_context = document.get("data_context", {})
    quality = document.get("data_quality", {})
    interpretation = document.get("interpretation", {})
    disposition = document.get("disposition", {})
    status = data_context.get("status") if isinstance(data_context, Mapping) else None
    sources = data_context.get("sources", []) if isinstance(data_context, Mapping) else []
    findings = document.get("findings", [])
    methods = document.get("methods", [])
    variables = document.get("variables", [])

    source_refs = [
        item.get("source_ref")
        for item in sources
        if isinstance(item, Mapping) and isinstance(item.get("source_ref"), str)
    ]
    for duplicate in sorted(_duplicates(source_refs)):
        errors.append(f"duplicate data source reference {duplicate!r}")

    method_refs = [
        item.get("method_ref")
        for item in methods
        if isinstance(item, Mapping) and isinstance(item.get("method_ref"), str)
    ]
    for duplicate in sorted(_duplicates(method_refs)):
        errors.append(f"duplicate method reference {duplicate!r}")

    variable_refs = [
        item.get("variable_ref")
        for item in variables
        if isinstance(item, Mapping) and isinstance(item.get("variable_ref"), str)
    ]
    for duplicate in sorted(_duplicates(variable_refs)):
        errors.append(f"duplicate variable reference {duplicate!r}")

    source_ref_set = set(source_refs)
    for variable in variables:
        if isinstance(variable, Mapping) and variable.get("source_ref") not in source_ref_set:
            errors.append(
                f"variable {variable.get('variable_ref', '<unknown>')} cites an undocumented source"
            )
    for method in methods:
        if not isinstance(method, Mapping):
            continue
        for source_ref in method.get("data_source_refs", []):
            if source_ref not in source_ref_set:
                errors.append(
                    f"method {method.get('method_ref', '<unknown>')} cites an undocumented source {source_ref!r}"
                )

    finding_refs = [
        item.get("finding_id")
        for item in findings
        if isinstance(item, Mapping) and isinstance(item.get("finding_id"), str)
    ]
    for duplicate in sorted(_duplicates(finding_refs)):
        errors.append(f"duplicate finding id {duplicate!r}")

    check_items = quality.get("checks", []) if isinstance(quality, Mapping) else []
    check_refs = [
        item.get("check_id")
        for item in check_items
        if isinstance(item, Mapping) and isinstance(item.get("check_id"), str)
    ]
    for duplicate in sorted(_duplicates(check_refs)):
        errors.append(f"duplicate data-quality check id {duplicate!r}")

    if status in {"USED", "PARTIAL"} and not sources:
        errors.append("USED or PARTIAL data_context requires at least one documented source")
    if status in {"NOT_AVAILABLE", "UNKNOWN"}:
        if sources:
            errors.append("NOT_AVAILABLE or UNKNOWN data_context must not claim usable sources")
        if findings:
            errors.append("NOT_AVAILABLE or UNKNOWN data_context cannot contain findings")
        if disposition.get("status") not in {"NOT_TESTABLE", "BLOCKED"}:
            errors.append("unavailable data requires NOT_TESTABLE or BLOCKED disposition")

    if findings and status not in {"USED", "PARTIAL"}:
        errors.append("findings require USED or PARTIAL data_context")
    if not findings and interpretation.get("evidence_assessment") in {"SUPPORTS", "WEAKENS"}:
        errors.append("SUPPORTS or WEAKENS requires at least one finding")
    if not findings and interpretation.get("claim_level_reached") == "PREDICTIVE":
        errors.append("PREDICTIVE claim requires at least one finding")

    method_types = {
        item.get("type")
        for item in methods
        if isinstance(item, Mapping)
    }
    predictive_methods = {"PREDICTIVE_EVALUATION", "BACKTEST_SUMMARY"}
    predictor_refs_with_unknown_timing = {
        item.get("variable_ref")
        for item in variables
        if isinstance(item, Mapping)
        and item.get("role") == "PREDICTOR"
        and item.get("available_at_decision") in {"NO", "UNKNOWN"}
    }
    if predictor_refs_with_unknown_timing and method_types & predictive_methods:
        errors.append(
            "predictive evaluation cannot use a predictor unavailable or unknown at decision time"
        )

    if "BACKTEST_SUMMARY" in method_types:
        trading_checks = document.get("trading_checks", {})
        required_backtest_checks = {
            "in_sample_out_of_sample": "SEPARATED",
            "leakage_check": "CONTROLLED",
            "costs_slippage_liquidity": "INCLUDED",
        }
        for name, preferred in required_backtest_checks.items():
            value = trading_checks.get(name) if isinstance(trading_checks, Mapping) else None
            if value in {None, "UNKNOWN", "NOT_APPLICABLE"}:
                errors.append(f"BACKTEST_SUMMARY requires an explicit {name} check")
            elif name == "in_sample_out_of_sample" and value not in {
                "SEPARATED",
                "CONTROLLED",
            }:
                errors.append("BACKTEST_SUMMARY requires separated or controlled in-sample/out-of-sample data")
            elif name == "leakage_check" and value not in {"SEPARATED", "CONTROLLED"}:
                errors.append("BACKTEST_SUMMARY requires a controlled leakage check")
            elif name == "costs_slippage_liquidity" and value != preferred:
                errors.append("BACKTEST_SUMMARY requires costs, slippage, and liquidity to be included")

    quality_status = quality.get("status") if isinstance(quality, Mapping) else None
    failed_quality_checks = [
        item
        for item in check_items
        if isinstance(item, Mapping) and item.get("status") in {"FAIL", "UNKNOWN"}
    ]
    if quality_status == "PASS" and failed_quality_checks:
        errors.append("data_quality PASS cannot coexist with failed or unknown quality checks")
    if quality_status in {"FAIL", "BLOCKED"} and disposition.get("status") == "REPORT_READY":
        errors.append("failed or blocked data quality cannot produce a REPORT_READY disposition")
    failed_leakage = any(
        isinstance(item, Mapping)
        and item.get("type") in {"LEAKAGE", "LOOKAHEAD", "SURVIVORSHIP"}
        and item.get("status") in {"FAIL", "UNKNOWN"}
        for item in check_items
    )
    if failed_leakage and (
        interpretation.get("evidence_assessment") in {"SUPPORTS", "WEAKENS"}
        or interpretation.get("claim_level_reached") == "PREDICTIVE"
    ):
        errors.append("failed or unknown leakage-related checks prevent predictive support")

    if data_context.get("missing_data_treatment") == "IMPUTED_PREDECLARED":
        summary = str(data_context.get("coverage_summary", "")) + " " + str(
            quality.get("missingness_summary", "")
        )
        if "imput" not in summary.lower():
            errors.append("predeclared imputation must be described in the missingness record")
        if "zero" in summary.lower() and "predeclared" not in summary.lower():
            errors.append("zero filling must never be silent")

    if disposition.get("status") == "CAUSAL_REVIEW_REQUIRED":
        errors.append("causal-identification review is a router prerequisite, not a data-analysis disposition")
    if interpretation.get("evidence_assessment") in {"NOT_TESTABLE", "BLOCKED"} and disposition.get(
        "status"
    ) not in {"NOT_TESTABLE", "BLOCKED"}:
        errors.append("a not-testable or blocked interpretation requires the matching disposition")

    for source in sources:
        if not isinstance(source, Mapping):
            continue
        start = _parse_timestamp(source.get("period_start"))
        end = _parse_timestamp(source.get("period_end"))
        if start is not None and end is not None and end <= start:
            errors.append(f"source {source.get('source_ref', '<unknown>')} has a non-positive period")

    return errors


def validate(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    return schema_errors(document, schema) + semantic_errors(document)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a bounded quantitative data-analysis report without executing it."
    )
    parser.add_argument("report", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report_path = args.report if args.report.is_absolute() else ROOT / args.report
    schema_path = args.schema if args.schema.is_absolute() else ROOT / args.schema
    document = load_json(report_path)
    schema = load_json(schema_path)
    errors = validate(document, schema)
    if errors:
        print("Data analysis report is invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Valid data analysis report {document['report_id']}: "
        f"status={document['disposition']['status']} "
        f"findings={len(document['findings'])}"
    )
    print("This report supplies bounded evidence; it did not execute a trade or change research state.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
