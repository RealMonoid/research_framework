#!/usr/bin/env python3
"""Contract and semantic tests for prose-strategy reconstruction."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from inspect_strategy_reconstruction import semantic_errors, validate


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = "examples/strategy_reconstruction.vwap_wave_price_discovery.json"
SCHEMA = "schemas/strategy_reconstruction.schema.json"


def load(relative_path: str) -> dict[str, Any]:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} must contain an object")
    return value


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
        raise AssertionError("Committed reconstruction fixture is invalid:\n- " + "\n- ".join(errors))

    if example["reconstruction_status"] != "SOURCE_EXTRACTION":
        raise AssertionError("Worked example must remain a source extraction")
    if example["fidelity_label"] != "UNASSESSED":
        raise AssertionError("Worked example must not claim reconstruction fidelity")
    if any(item["decision"]["status"] != "UNDECIDED" for item in example["constructs"]):
        raise AssertionError("Worked example silently selected an operationalization")
    if not any(
        claim["source_force"] == "ILLUSTRATIVE" for claim in example["source_claims"]
    ):
        raise AssertionError("Worked example does not distinguish examples from rules")
    if not any(
        item["source_status"] == "DISCRETIONARY" for item in example["constructs"]
    ):
        raise AssertionError("Worked example erased the source's discretionary component")
    if not any(
        item["source_status"] == "CONTRADICTORY" for item in example["constructs"]
    ):
        raise AssertionError("Worked example does not retain source contradictions")

    unknown_claim = copy.deepcopy(example)
    unknown_claim["constructs"][0]["source_claim_refs"] = ["claim:does-not-exist"]
    assert_semantic_failure(unknown_claim, "references unknown claims")

    unknown_choice = copy.deepcopy(example)
    decision = unknown_choice["constructs"][0]["decision"]
    decision.update(
        {
            "status": "SELECTED",
            "chosen_candidate_id": "op:not-listed",
            "choice_basis": "RESEARCHER_DECISION",
            "rationale": "Synthetic negative test.",
        }
    )
    unknown_choice["reconstruction_status"] = "TRANSLATION_DRAFT"
    assert_semantic_failure(unknown_choice, "chooses an unknown candidate")

    false_replication = copy.deepcopy(example)
    false_replication["fidelity_label"] = "REPLICATION"
    assert_semantic_failure(false_replication, "REPLICATION is not permitted")

    command = [
        sys.executable,
        str(ROOT / "scripts" / "inspect_strategy_reconstruction.py"),
        EXAMPLE,
    ]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(
            f"Inspector failed with {completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
        )
    if "No operationalization was selected and no market test was run" not in completed.stdout:
        raise AssertionError("Inspector output lost its explicit non-testing boundary")

    print(
        f"Strategy reconstruction tests passed: {len(example['source_claims'])} source claims, "
        f"{len(example['constructs'])} constructs, no selected definitions, and 3 semantic negatives."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
