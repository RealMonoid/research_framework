#!/usr/bin/env python3
"""Validate and score deterministic research-agent evaluation results.

The harness deliberately uses only the Python standard library.  It evaluates an
adapter format rather than raw prose so that every score has a reproducible,
machine-readable reason.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


CATALOG_SCHEMA_VERSION = "eval-catalog.v1"
RESULTS_SCHEMA_VERSION = "eval-results.v2"
BASELINE_SCHEMA_VERSION = "eval-baseline.v1"

RUN_KINDS = {"PROTOCOL_SMOKE", "LIVE_AGENT"}
PRODUCER_TYPES = {"REFERENCE_FIXTURE", "COMMAND", "HTTP_JSON"}
PRODUCER_PROTOCOL = "eval-agent-request.v1"

CAPABILITIES = {
    "source_attribution",
    "fact_vs_inference",
    "missing_evidence",
    "conflicting_sources",
    "stale_source",
    "calculation",
    "thesis_update",
    "thesis_invalidation",
    "academic_source_status",
    "hypothesis_intake",
}
STATEMENT_CLASSES = {
    "SOURCE_FACT",
    "CALCULATED_VALUE",
    "ESTIMATE",
    "INFERENCE",
    "FORECAST",
    "HUMAN_JUDGMENT",
}
EVIDENCE_STATUSES = {
    "SUPPORTED",
    "PARTIAL",
    "UNKNOWN",
    "CONFLICTING",
    "STALE",
    "NOT_APPLICABLE",
}
OPERATORS = {"equals", "set_equals", "approx_equals", "is_empty", "exists"}
METRICS = {
    "citation_accuracy",
    "epistemic_classification_accuracy",
    "unknown_safety_rate",
    "contradiction_handling_rate",
    "source_freshness_rate",
    "calculation_accuracy",
    "thesis_governance_accuracy",
    "academic_source_governance_accuracy",
    "hypothesis_intake_accuracy",
}

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
MISSING = object()


class FixtureError(ValueError):
    """Raised when a catalog, results file, or baseline is malformed."""


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _is_iso_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except OSError as exc:
        raise FixtureError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise FixtureError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FixtureError(f"{path} must contain a JSON object")
    return value


def _raise_errors(kind: str, errors: Sequence[str]) -> None:
    if errors:
        formatted = "\n".join(f"- {error}" for error in errors)
        raise FixtureError(f"invalid {kind}:\n{formatted}")


def validate_catalog(catalog: Mapping[str, Any]) -> None:
    errors: list[str] = []
    _require(catalog.get("schema_version") == CATALOG_SCHEMA_VERSION,
             f"schema_version must be {CATALOG_SCHEMA_VERSION!r}", errors)
    _require(isinstance(catalog.get("catalog_id"), str) and bool(ID_RE.fullmatch(catalog["catalog_id"])),
             "catalog_id must be a lowercase stable identifier", errors)
    _require(isinstance(catalog.get("catalog_version"), str)
             and bool(SEMVER_RE.fullmatch(catalog["catalog_version"])),
             "catalog_version must be semantic x.y.z", errors)
    _require(_is_iso_datetime(catalog.get("created_at")), "created_at must be an ISO-8601 datetime", errors)

    cases = catalog.get("cases")
    _require(isinstance(cases, list) and bool(cases), "cases must be a non-empty array", errors)
    if not isinstance(cases, list):
        _raise_errors("catalog", errors)
        return

    seen_cases: set[str] = set()
    covered_capabilities: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        case_id = case.get("case_id")
        _require(isinstance(case_id, str) and bool(ID_RE.fullmatch(case_id or "")),
                 f"{prefix}.case_id must be a lowercase stable identifier", errors)
        if isinstance(case_id, str):
            _require(case_id not in seen_cases, f"duplicate case_id {case_id!r}", errors)
            seen_cases.add(case_id)
        capability = case.get("capability")
        _require(capability in CAPABILITIES, f"{prefix}.capability is unsupported", errors)
        if capability in CAPABILITIES:
            covered_capabilities.add(capability)
        _require(isinstance(case.get("description"), str) and bool(case.get("description")),
                 f"{prefix}.description must be non-empty", errors)

        inputs = case.get("input")
        _require(isinstance(inputs, dict), f"{prefix}.input must be an object", errors)
        source_ids: set[str] = set()
        if isinstance(inputs, dict):
            _require(isinstance(inputs.get("task"), str) and bool(inputs.get("task")),
                     f"{prefix}.input.task must be non-empty", errors)
            sources = inputs.get("sources")
            _require(isinstance(sources, list), f"{prefix}.input.sources must be an array", errors)
            if isinstance(sources, list):
                for source_index, source in enumerate(sources):
                    source_prefix = f"{prefix}.input.sources[{source_index}]"
                    if not isinstance(source, dict):
                        errors.append(f"{source_prefix} must be an object")
                        continue
                    source_id = source.get("source_id")
                    _require(isinstance(source_id, str) and bool(ID_RE.fullmatch(source_id or "")),
                             f"{source_prefix}.source_id is invalid", errors)
                    if isinstance(source_id, str):
                        _require(source_id not in source_ids,
                                 f"{prefix} has duplicate source_id {source_id!r}", errors)
                        source_ids.add(source_id)
                    _require(isinstance(source.get("title"), str) and bool(source.get("title")),
                             f"{source_prefix}.title must be non-empty", errors)
                    _require(_is_iso_datetime(source.get("published_at")),
                             f"{source_prefix}.published_at must be ISO-8601", errors)
                    _require(_is_iso_datetime(source.get("accessed_at")),
                             f"{source_prefix}.accessed_at must be ISO-8601", errors)
                    _require(isinstance(source.get("authoritative"), bool),
                             f"{source_prefix}.authoritative must be boolean", errors)
                    _require(isinstance(source.get("content"), str) and bool(source.get("content")),
                             f"{source_prefix}.content must be non-empty", errors)

        expected = case.get("expected")
        _require(isinstance(expected, dict), f"{prefix}.expected must be an object", errors)
        assertions: Any = expected.get("assertions") if isinstance(expected, dict) else None
        _require(isinstance(assertions, list) and bool(assertions),
                 f"{prefix}.expected.assertions must be a non-empty array", errors)
        if not isinstance(assertions, list):
            continue
        seen_assertions: set[str] = set()
        for assertion_index, assertion in enumerate(assertions):
            assertion_prefix = f"{prefix}.expected.assertions[{assertion_index}]"
            if not isinstance(assertion, dict):
                errors.append(f"{assertion_prefix} must be an object")
                continue
            assertion_id = assertion.get("assertion_id")
            _require(isinstance(assertion_id, str) and bool(ID_RE.fullmatch(assertion_id or "")),
                     f"{assertion_prefix}.assertion_id is invalid", errors)
            if isinstance(assertion_id, str):
                _require(assertion_id not in seen_assertions,
                         f"{prefix} has duplicate assertion_id {assertion_id!r}", errors)
                seen_assertions.add(assertion_id)
            _require(assertion.get("metric") in METRICS,
                     f"{assertion_prefix}.metric is unsupported", errors)
            _require(isinstance(assertion.get("path"), str) and bool(assertion.get("path")),
                     f"{assertion_prefix}.path must be non-empty", errors)
            operator = assertion.get("operator")
            _require(operator in OPERATORS, f"{assertion_prefix}.operator is unsupported", errors)
            _require("expected" in assertion, f"{assertion_prefix}.expected is required", errors)
            _require(isinstance(assertion.get("critical"), bool),
                     f"{assertion_prefix}.critical must be boolean", errors)
            weight = assertion.get("weight")
            _require(_is_number(weight) and weight > 0,
                     f"{assertion_prefix}.weight must be a positive finite number", errors)
            if operator == "set_equals":
                _require(isinstance(assertion.get("expected"), list),
                         f"{assertion_prefix}.expected must be an array for set_equals", errors)
            if operator == "approx_equals":
                _require(_is_number(assertion.get("expected")),
                         f"{assertion_prefix}.expected must be numeric for approx_equals", errors)
                _require(_is_number(assertion.get("tolerance")) and assertion.get("tolerance") >= 0,
                         f"{assertion_prefix}.tolerance must be a non-negative number", errors)
            if operator in {"is_empty", "exists"}:
                _require(isinstance(assertion.get("expected"), bool),
                         f"{assertion_prefix}.expected must be boolean for {operator}", errors)

    missing = sorted(CAPABILITIES - covered_capabilities)
    _require(not missing, f"catalog is missing required capabilities: {', '.join(missing)}", errors)
    _raise_errors("catalog", errors)


def validate_results(results: Mapping[str, Any], catalog: Mapping[str, Any]) -> None:
    errors: list[str] = []
    expected_top_level = {
        "schema_version",
        "catalog_id",
        "catalog_version",
        "run_id",
        "created_at",
        "run_kind",
        "producer",
        "cases",
    }
    _require(set(results) == expected_top_level,
             f"result top-level fields must be exactly {sorted(expected_top_level)}", errors)
    _require(results.get("schema_version") == RESULTS_SCHEMA_VERSION,
             f"schema_version must be {RESULTS_SCHEMA_VERSION!r}", errors)
    _require(results.get("catalog_id") == catalog.get("catalog_id"),
             "catalog_id must match the catalog", errors)
    _require(results.get("catalog_version") == catalog.get("catalog_version"),
             "catalog_version must match the catalog exactly", errors)
    _require(isinstance(results.get("run_id"), str) and bool(ID_RE.fullmatch(results.get("run_id", ""))),
             "run_id must be a lowercase stable identifier", errors)
    _require(_is_iso_datetime(results.get("created_at")), "created_at must be an ISO-8601 datetime", errors)
    run_kind = results.get("run_kind")
    _require(run_kind in RUN_KINDS, f"run_kind must be one of {sorted(RUN_KINDS)}", errors)
    producer = results.get("producer")
    _require(isinstance(producer, dict), "producer must be an object", errors)
    if isinstance(producer, dict):
        expected_producer_fields = {
            "producer_type",
            "adapter_id",
            "request_protocol",
            "started_at",
            "completed_at",
            "configuration_sha256",
        }
        _require(set(producer) == expected_producer_fields,
                 f"producer fields must be exactly {sorted(expected_producer_fields)}", errors)
        _require(producer.get("producer_type") in PRODUCER_TYPES,
                 f"producer.producer_type must be one of {sorted(PRODUCER_TYPES)}", errors)
        _require(isinstance(producer.get("adapter_id"), str)
                 and bool(ID_RE.fullmatch(producer.get("adapter_id", ""))),
                 "producer.adapter_id must be a lowercase stable identifier", errors)
        _require(producer.get("request_protocol") == PRODUCER_PROTOCOL,
                 f"producer.request_protocol must be {PRODUCER_PROTOCOL!r}", errors)
        _require(_is_iso_datetime(producer.get("started_at")),
                 "producer.started_at must be ISO-8601", errors)
        _require(_is_iso_datetime(producer.get("completed_at")),
                 "producer.completed_at must be ISO-8601", errors)
        _require(isinstance(producer.get("configuration_sha256"), str)
                 and bool(re.fullmatch(r"[0-9a-f]{64}", producer.get("configuration_sha256", ""))),
                 "producer.configuration_sha256 must be a lowercase SHA-256 digest", errors)
        if run_kind == "LIVE_AGENT":
            _require(producer.get("producer_type") != "REFERENCE_FIXTURE",
                     "LIVE_AGENT cannot use a REFERENCE_FIXTURE producer", errors)
        if (_is_iso_datetime(producer.get("started_at"))
                and _is_iso_datetime(producer.get("completed_at"))):
            started_at = datetime.fromisoformat(producer["started_at"].replace("Z", "+00:00"))
            completed_at = datetime.fromisoformat(producer["completed_at"].replace("Z", "+00:00"))
            _require(started_at <= completed_at,
                     "producer.started_at must not be after producer.completed_at", errors)
            _require(results.get("created_at") == producer.get("completed_at"),
                     "created_at must equal producer.completed_at", errors)
    result_cases = results.get("cases")
    _require(isinstance(result_cases, dict), "cases must be an object keyed by case_id", errors)
    if not isinstance(result_cases, dict):
        _raise_errors("results", errors)
        return

    catalog_cases = {case["case_id"]: case for case in catalog["cases"]}
    expected_ids = set(catalog_cases)
    actual_ids = set(result_cases)
    _require(actual_ids == expected_ids,
             f"case ids must match catalog; missing={sorted(expected_ids - actual_ids)}, "
             f"unknown={sorted(actual_ids - expected_ids)}", errors)

    for case_id in sorted(actual_ids & expected_ids):
        case_result = result_cases[case_id]
        prefix = f"cases.{case_id}"
        if not isinstance(case_result, dict):
            errors.append(f"{prefix} must be an object")
            continue
        claims = case_result.get("claims")
        _require(isinstance(claims, dict), f"{prefix}.claims must be an object keyed by claim_id", errors)
        if not isinstance(claims, dict):
            continue
        known_sources = {
            source["source_id"] for source in catalog_cases[case_id]["input"]["sources"]
        }
        for claim_id, claim in claims.items():
            claim_prefix = f"{prefix}.claims.{claim_id}"
            _require(isinstance(claim_id, str) and bool(ID_RE.fullmatch(claim_id)),
                     f"{claim_prefix} has invalid claim_id", errors)
            if not isinstance(claim, dict):
                errors.append(f"{claim_prefix} must be an object")
                continue
            _require(claim.get("statement_class") in STATEMENT_CLASSES,
                     f"{claim_prefix}.statement_class is unsupported", errors)
            _require(claim.get("evidence_status") in EVIDENCE_STATUSES,
                     f"{claim_prefix}.evidence_status is unsupported", errors)
            source_ids = claim.get("source_ids")
            _require(isinstance(source_ids, list) and all(isinstance(item, str) for item in source_ids or []),
                     f"{claim_prefix}.source_ids must be a string array", errors)
            if isinstance(source_ids, list):
                _require(len(source_ids) == len(set(source_ids)),
                         f"{claim_prefix}.source_ids must not contain duplicates", errors)
                unknown = sorted(set(source_ids) - known_sources)
                _require(not unknown, f"{claim_prefix}.source_ids contains unknown sources: {unknown}", errors)
    _raise_errors("results", errors)


def validate_baseline(baseline: Mapping[str, Any], catalog: Mapping[str, Any]) -> None:
    errors: list[str] = []
    _require(baseline.get("schema_version") == BASELINE_SCHEMA_VERSION,
             f"schema_version must be {BASELINE_SCHEMA_VERSION!r}", errors)
    _require(baseline.get("catalog_id") == catalog.get("catalog_id"),
             "catalog_id must match the catalog", errors)
    _require(baseline.get("catalog_version") == catalog.get("catalog_version"),
             "catalog_version must match the catalog exactly", errors)
    _require(isinstance(baseline.get("baseline_id"), str)
             and bool(ID_RE.fullmatch(baseline.get("baseline_id", ""))),
             "baseline_id must be a lowercase stable identifier", errors)
    _require(_is_iso_datetime(baseline.get("recorded_at")),
             "recorded_at must be an ISO-8601 datetime", errors)
    catalog_case_ids = {case["case_id"] for case in catalog["cases"]}
    for field in ("minimums", "metrics", "case_scores"):
        value = baseline.get(field)
        _require(isinstance(value, dict), f"{field} must be an object", errors)
        if isinstance(value, dict):
            for key, score in value.items():
                _require(isinstance(key, str) and bool(key), f"{field} keys must be non-empty", errors)
                _require(_is_number(score) and 0 <= score <= 1,
                         f"{field}.{key} must be between 0 and 1", errors)
    if isinstance(baseline.get("case_scores"), dict):
        actual_case_ids = set(baseline["case_scores"])
        _require(actual_case_ids == catalog_case_ids,
                 "case_scores must contain every catalog case exactly once", errors)
    policy = baseline.get("regression_policy")
    _require(isinstance(policy, dict), "regression_policy must be an object", errors)
    if isinstance(policy, dict):
        for field in ("max_metric_drop", "max_case_drop"):
            value = policy.get(field)
            _require(_is_number(value) and 0 <= value <= 1,
                     f"regression_policy.{field} must be between 0 and 1", errors)
    _raise_errors("baseline", errors)


def _resolve_path(value: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = value
    for component in dotted_path.split("."):
        if not isinstance(current, dict) or component not in current:
            return MISSING
        current = current[component]
    return current


def _strict_equal(actual: Any, expected: Any) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if _is_number(actual) and _is_number(expected):
        return actual == expected
    return type(actual) is type(expected) and actual == expected


def _canonical_set(value: Any) -> Any:
    if not isinstance(value, list):
        return MISSING
    try:
        return {json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value}
    except (TypeError, ValueError):
        return MISSING


def evaluate_assertion(case_result: Mapping[str, Any], assertion: Mapping[str, Any]) -> tuple[bool, Any]:
    actual = _resolve_path(case_result, assertion["path"])
    operator = assertion["operator"]
    expected = assertion["expected"]
    if operator == "equals":
        passed = actual is not MISSING and _strict_equal(actual, expected)
    elif operator == "set_equals":
        actual_set = _canonical_set(actual)
        expected_set = _canonical_set(expected)
        passed = actual_set is not MISSING and actual_set == expected_set
    elif operator == "approx_equals":
        passed = (_is_number(actual)
                  and abs(float(actual) - float(expected)) <= float(assertion["tolerance"]))
    elif operator == "is_empty":
        is_empty = actual is not MISSING and hasattr(actual, "__len__") and len(actual) == 0
        passed = is_empty is expected
    elif operator == "exists":
        passed = (actual is not MISSING) is expected
    else:  # Catalog validation makes this unreachable.
        raise AssertionError(f"unsupported operator: {operator}")
    return passed, None if actual is MISSING else actual


def score_results(
    catalog: Mapping[str, Any],
    results: Mapping[str, Any],
    baseline: Mapping[str, Any],
    required_run_kind: str | None = None,
) -> dict[str, Any]:
    validate_catalog(catalog)
    validate_results(results, catalog)
    validate_baseline(baseline, catalog)

    metric_totals: dict[str, float] = defaultdict(float)
    metric_passed: dict[str, float] = defaultdict(float)
    case_reports: dict[str, Any] = {}
    total_weight = 0.0
    passed_weight = 0.0
    critical_total = 0
    critical_passed = 0

    for case in catalog["cases"]:
        case_id = case["case_id"]
        case_result = results["cases"][case_id]
        assertion_reports: list[dict[str, Any]] = []
        case_total = 0.0
        case_passed = 0.0
        for assertion in case["expected"]["assertions"]:
            passed, actual = evaluate_assertion(case_result, assertion)
            weight = float(assertion["weight"])
            metric = assertion["metric"]
            total_weight += weight
            case_total += weight
            metric_totals[metric] += weight
            if passed:
                passed_weight += weight
                case_passed += weight
                metric_passed[metric] += weight
            if assertion["critical"]:
                critical_total += 1
                critical_passed += int(passed)
            assertion_reports.append({
                "assertion_id": assertion["assertion_id"],
                "metric": metric,
                "passed": passed,
                "path": assertion["path"],
                "operator": assertion["operator"],
                "expected": assertion["expected"],
                "actual": actual,
                "critical": assertion["critical"],
                "weight": weight,
            })
        score = case_passed / case_total
        case_reports[case_id] = {
            "capability": case["capability"],
            "score": score,
            "passed": math.isclose(score, 1.0),
            "assertions": assertion_reports,
        }

    metrics = {
        metric: metric_passed[metric] / metric_totals[metric]
        for metric in sorted(metric_totals)
    }
    metrics["overall_score"] = passed_weight / total_weight
    metrics["critical_assertion_pass_rate"] = (
        critical_passed / critical_total if critical_total else 1.0
    )

    gate_failures: list[str] = []
    if required_run_kind is not None and results["run_kind"] != required_run_kind:
        gate_failures.append(
            f"run_kind={results['run_kind']} does not satisfy required_run_kind={required_run_kind}"
        )
    for metric, minimum in baseline["minimums"].items():
        actual = metrics.get(metric)
        if actual is None:
            gate_failures.append(f"required metric {metric!r} was not produced")
        elif actual + 1e-12 < minimum:
            gate_failures.append(f"{metric}={actual:.4f} is below minimum {minimum:.4f}")

    regression_failures: list[str] = []
    max_metric_drop = baseline["regression_policy"]["max_metric_drop"]
    for metric, previous in baseline["metrics"].items():
        actual = metrics.get(metric)
        if actual is None:
            regression_failures.append(f"baseline metric {metric!r} was not produced")
        elif previous - actual > max_metric_drop + 1e-12:
            regression_failures.append(
                f"{metric} regressed by {previous - actual:.4f} "
                f"(baseline={previous:.4f}, current={actual:.4f}, allowed={max_metric_drop:.4f})"
            )
    max_case_drop = baseline["regression_policy"]["max_case_drop"]
    for case_id, previous in baseline["case_scores"].items():
        actual = case_reports[case_id]["score"]
        if previous - actual > max_case_drop + 1e-12:
            regression_failures.append(
                f"case {case_id} regressed by {previous - actual:.4f} "
                f"(baseline={previous:.4f}, current={actual:.4f}, allowed={max_case_drop:.4f})"
            )

    return {
        "schema_version": "eval-report.v1",
        "catalog_id": catalog["catalog_id"],
        "catalog_version": catalog["catalog_version"],
        "run_id": results["run_id"],
        "run_kind": results["run_kind"],
        "passed": not gate_failures and not regression_failures,
        "metrics": metrics,
        "cases": case_reports,
        "gate_failures": gate_failures,
        "regression_failures": regression_failures,
    }


def _default_paths() -> tuple[Path, Path, Path]:
    root = Path(__file__).resolve().parent
    return (
        root / "catalog.v1.json",
        root / "examples" / "smoke-results.v1.json",
        root / "baseline.v1.json",
    )


def build_parser() -> argparse.ArgumentParser:
    catalog, results, baseline = _default_paths()
    parser = argparse.ArgumentParser(
        description="Validate and score research-agent eval results against a versioned baseline."
    )
    parser.add_argument("--catalog", type=Path, default=catalog)
    parser.add_argument("--results", type=Path, default=results)
    parser.add_argument("--baseline", type=Path, default=baseline)
    parser.add_argument("--report", type=Path, help="Optional path for the full JSON report")
    parser.add_argument("--verbose", action="store_true", help="Print failed assertion details")
    parser.add_argument(
        "--require-run-kind",
        choices=sorted(RUN_KINDS),
        help="Fail the gate unless the result was produced with this declared run kind.",
    )
    return parser


def _write_report(path: Path, report: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        catalog = load_json(args.catalog)
        results = load_json(args.results)
        baseline = load_json(args.baseline)
        report = score_results(
            catalog,
            results,
            baseline,
            required_run_kind=args.require_run_kind,
        )
    except FixtureError as exc:
        print(f"STRUCTURAL ERROR\n{exc}", file=sys.stderr)
        return 2

    if args.report:
        try:
            _write_report(args.report, report)
        except OSError as exc:
            print(f"REPORT ERROR\ncannot write {args.report}: {exc}", file=sys.stderr)
            return 2

    status = "PASS" if report["passed"] else "FAIL"
    print(
        f"{status}: {report['catalog_id']}@{report['catalog_version']} "
        f"run={report['run_id']} kind={report['run_kind']} "
        f"overall={report['metrics']['overall_score']:.4f} "
        f"critical={report['metrics']['critical_assertion_pass_rate']:.4f}"
    )
    if report["run_kind"] == "PROTOCOL_SMOKE":
        print(
            "NOTICE: PROTOCOL_SMOKE validates contracts and scoring only; "
            "it is not a release-quality measurement of a live agent.",
            file=sys.stderr,
        )
    for failure in report["gate_failures"]:
        print(f"GATE: {failure}", file=sys.stderr)
    for failure in report["regression_failures"]:
        print(f"REGRESSION: {failure}", file=sys.stderr)
    if args.verbose:
        for case_id, case_report in report["cases"].items():
            for assertion in case_report["assertions"]:
                if not assertion["passed"]:
                    print(
                        f"ASSERTION: {case_id}/{assertion['assertion_id']} "
                        f"path={assertion['path']} expected={assertion['expected']!r} "
                        f"actual={assertion['actual']!r}",
                        file=sys.stderr,
                    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
