#!/usr/bin/env python3
"""Contract and semantic tests for scientific-philosophy reviews."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from inspect_scientific_philosophy_review import semantic_errors, validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = "examples/scientific_philosophy_review.synthetic_failed_reconstruction.json"
SCHEMA = "schemas/scientific_philosophy_review.schema.json"


def load(relative_path: str) -> dict[str, Any]:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must contain an object")
    return value


def assert_failure(document: dict[str, Any], expected_fragment: str) -> None:
    errors = validate(document, load(SCHEMA))
    if not any(expected_fragment in error for error in errors):
        raise AssertionError(
            f"Expected failure containing {expected_fragment!r}; observed {errors!r}"
        )


def assert_semantic_failure(document: dict[str, Any], expected_fragment: str) -> None:
    errors = semantic_errors(document)
    if not any(expected_fragment in error for error in errors):
        raise AssertionError(
            f"Expected semantic failure containing {expected_fragment!r}; observed {errors!r}"
        )


def main() -> int:
    example = load(EXAMPLE)
    schema = load(SCHEMA)
    errors = validate(example, schema)
    if errors:
        raise AssertionError("Committed philosophy fixture is invalid:\n- " + "\n- ".join(errors))

    if example["frozen_result"]["status"] != "FALSIFIED":
        raise AssertionError("Synthetic fixture must retain the imagined FALSIFIED result")
    if example["frozen_result"]["remains_unchanged"] is not True:
        raise AssertionError("Frozen result was not protected")
    if example["underdetermination"]["attribution_status"] != "NON_UNIQUE":
        raise AssertionError("Duhem-Quine bundle was given a spurious unique attribution")
    classifications = {
        proposal["classification"] for proposal in example["revision_proposals"]
    }
    if classifications != {"PROGRESSIVE", "DEGENERATIVE"}:
        raise AssertionError("Fixture must contrast progressive and degenerative revisions")

    relabelled = copy.deepcopy(example)
    relabelled["frozen_result"]["remains_unchanged"] = False
    assert_failure(relabelled, "True was expected")

    fake_progress = copy.deepcopy(example)
    progressive = fake_progress["revision_proposals"][1]
    progressive["novel_prediction"]["relation_to_prior"] = "ALREADY_IMPLIED"
    assert_failure(fake_progress, "'NOT_IMPLIED' was expected")

    non_independent_progress = copy.deepcopy(example)
    non_independent_progress["revision_proposals"][1]["novel_prediction"][
        "independence_plan"
    ] = None
    assert_failure(non_independent_progress, "None is not of type 'string'")

    unknown_bundle_target = copy.deepcopy(example)
    unknown_bundle_target["revision_proposals"][1]["target_refs"] = ["aux:not-listed"]
    assert_semantic_failure(unknown_bundle_target, "unknown bundle target")

    rescue_selected = copy.deepcopy(example)
    rescue_selected["continuation"]["selected_revision_ref"] = "revision:exclude-adverse-months"
    rescue_selected["continuation"]["new_research_id"] = "research:synthetic-rescue"
    assert_semantic_failure(rescue_selected, "must select a PROGRESSIVE revision")

    reused_id = copy.deepcopy(example)
    reused_id["revision_proposals"][1]["proposed_research_id"] = example["research_id"]
    reused_id["continuation"]["new_research_id"] = example["research_id"]
    assert_semantic_failure(reused_id, "reuses the original Research-ID")

    command = [
        sys.executable,
        str(ROOT / "scripts" / "inspect_scientific_philosophy_review.py"),
        EXAMPLE,
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(
            f"Inspector failed with {completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
        )
    if "no market test or backtest was run" not in completed.stdout:
        raise AssertionError("Inspector output lost its explicit non-testing boundary")

    print(
        "Scientific-philosophy review tests passed: frozen result retained, "
        "non-unique attribution preserved, progressive/degenerative contrast, "
        "and 6 negative cases."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
