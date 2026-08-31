#!/usr/bin/env python3
"""Contract and negative-boundary tests for causal identification."""

from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

from inspect_causal_identification import load_object, semantic_errors, validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "causal_identification_assessment.hfi_pass.json"
SCHEMA = ROOT / "schemas" / "causal_identification_assessment.schema.json"


def require_error(document: dict, expected_fragment: str) -> None:
    errors = semantic_errors(document)
    if not any(expected_fragment in error for error in errors):
        raise AssertionError(
            f"Expected semantic error containing {expected_fragment!r}; observed {errors!r}"
        )


def main() -> int:
    example = load_object(EXAMPLE)
    schema = load_object(SCHEMA)
    errors = validate(example, schema) + semantic_errors(example)
    if errors:
        raise AssertionError("Valid HFI example failed:\n- " + "\n- ".join(errors))

    estimator_only = copy.deepcopy(example)
    estimator_only["design"]["assignment_or_variation_source"] = "Double machine learning"
    require_error(estimator_only, "names only an estimator")

    discovery = copy.deepcopy(example)
    discovery["design"]["design_family"] = "CAUSAL_DISCOVERY_ONLY"
    discovery["design"]["variation_type"] = "ASSUMPTION_BASED_ADJUSTMENT"
    require_error(discovery, "causal discovery alone")

    missed_concurrent_news = copy.deepcopy(example)
    missed_concurrent_news["finance_risk_checks"]["concurrent_events"]["status"] = "NOT_APPLICABLE"
    require_error(missed_concurrent_news, "event-design PASS requires")

    blocked_but_authorized = copy.deepcopy(example)
    blocked_but_authorized["judgment"]["identification_status"] = "BLOCKED"
    blocked_but_authorized["judgment"]["unresolved_blockers"] = [
        "No defensible source of exogenous variation is available."
    ]
    require_error(blocked_but_authorized, "cannot authorize")

    direct_without_mediator = copy.deepcopy(example)
    direct_without_mediator["estimand"]["effect_type"] = "DIRECT"
    require_error(direct_without_mediator, "separated mediator estimand")

    failed_but_causal_wording = copy.deepcopy(example)
    failed_but_causal_wording["judgment"]["identification_status"] = "FAIL"
    failed_but_causal_wording["judgment"]["causal_estimation_authorized"] = False
    failed_but_causal_wording["judgment"]["causal_language_authorized"] = False
    failed_but_causal_wording["judgment"]["unresolved_blockers"] = [
        "The assignment mechanism cannot identify the stated contrast."
    ]
    require_error(failed_but_causal_wording, "cannot retain interventional")

    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "inspect_causal_identification.py"), str(EXAMPLE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"Inspector CLI failed with {completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
        )

    print(
        "Causal-identification tests passed: estimator-only, causal-discovery, "
        "event-contamination, blocked-authorization, and mediation boundaries."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
