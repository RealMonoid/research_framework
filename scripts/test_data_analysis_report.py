#!/usr/bin/env python3
"""Regression tests for the bounded quantitative data-analysis contract."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from validate_data_analysis_report import load_json, validate


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "examples" / "data_analysis_report.synthetic.json"
SCHEMA = ROOT / "schemas" / "data_analysis_report.schema.json"
Mutation = Callable[[dict[str, Any]], None]


def assert_invalid(base: dict[str, Any], mutation: Mutation, label: str) -> None:
    candidate = copy.deepcopy(base)
    mutation(candidate)
    errors = validate(candidate, load_json(SCHEMA))
    if not errors:
        raise AssertionError(f"{label}: mutation was accepted")


def main() -> int:
    report = load_json(REPORT)
    schema = load_json(SCHEMA)
    errors = validate(report, schema)
    if errors:
        raise AssertionError("synthetic report is invalid:\n- " + "\n- ".join(errors))

    assert_invalid(
        report,
        lambda value: value.__setitem__("no_trading_action", False),
        "trading boundary must remain true",
    )
    assert_invalid(
        report,
        lambda value: value.__setitem__("no_causal_claim", False),
        "causal boundary must remain true",
    )
    assert_invalid(
        report,
        lambda value: (
            value["data_context"].update({"status": "NOT_AVAILABLE", "sources": []}),
            value["disposition"].update({"status": "NOT_TESTABLE"}),
        ),
        "unavailable data cannot carry findings",
    )

    def add_unknown_predictor(value: dict[str, Any]) -> None:
        value["variables"].append(
            {
                "variable_ref": "variable:unknown-timing",
                "name": "Unknown-timing predictor",
                "role": "PREDICTOR",
                "available_at_decision": "UNKNOWN",
                "source_ref": "dataset:synthetic-bars:v1",
                "construction_note": "Timing was not established.",
                "post_outcome_risk": "Unknown.",
            }
        )
        value["methods"].append(
            {
                "method_ref": "method:predictive-evaluation:v1",
                "type": "PREDICTIVE_EVALUATION",
                "data_source_refs": ["dataset:synthetic-bars:v1"],
                "data_role": "DEVELOPMENT",
                "parameters_locked": True,
                "parameter_refs": ["parameter:predictive-rules:v1"],
                "purpose": "Evaluate a forecast.",
                "result_summary": "Not run in this mutation.",
            }
        )

    assert_invalid(report, add_unknown_predictor, "predictive method requires decision-time predictors")

    def add_unsupported_backtest(value: dict[str, Any]) -> None:
        value["methods"].append(
            {
                "method_ref": "method:backtest-summary:v1",
                "type": "BACKTEST_SUMMARY",
                "data_source_refs": ["dataset:synthetic-bars:v1"],
                "data_role": "DEVELOPMENT",
                "parameters_locked": True,
                "parameter_refs": ["parameter:backtest-rules:v1"],
                "purpose": "Summarize a backtest.",
                "result_summary": "Not run in this mutation.",
            }
        )

    assert_invalid(report, add_unsupported_backtest, "backtest needs separation and trading assumptions")

    def fail_quality_check(value: dict[str, Any]) -> None:
        value["data_quality"]["status"] = "PASS"
        value["data_quality"]["checks"][0]["status"] = "FAIL"

    assert_invalid(report, fail_quality_check, "PASS cannot hide a failed quality check")

    def claim_support_with_leakage(value: dict[str, Any]) -> None:
        value["interpretation"]["evidence_assessment"] = "SUPPORTS"
        value["interpretation"]["claim_level_reached"] = "PREDICTIVE"
        value["data_quality"]["checks"].append(
            {
                "check_id": "quality:leakage-failed:v1",
                "type": "LEAKAGE",
                "status": "FAIL",
                "evidence_refs": ["method:data-quality-profile:v1"],
                "impact": "The prediction is not admissible.",
                "note": "Synthetic negative case.",
            }
        )

    assert_invalid(report, claim_support_with_leakage, "leakage failure blocks predictive support")

    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_data_analysis_report.py"), str(REPORT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(f"report validator CLI failed:\n{completed.stdout}\n{completed.stderr}")
    if "did not execute a trade" not in completed.stdout:
        raise AssertionError("validator output did not state the no-trading boundary")

    print(
        "Data-analysis report tests passed: provenance and quality requirements, "
        "decision-time availability, backtest boundaries, leakage controls, "
        "non-causal interpretation, and no-action contract."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
