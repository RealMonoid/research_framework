#!/usr/bin/env python3
"""Integration tests for the short-horizon hypothesis producer."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


def load(relative_path: str | Path) -> dict[str, Any]:
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"Expected object in {path}")
    return value


def assert_valid(document: dict[str, Any], schema_path: str) -> None:
    validator = Draft202012Validator(load(schema_path), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda error: error.json_path)
    if errors:
        details = "\n".join(f"- {error.json_path}: {error.message}" for error in errors)
        raise AssertionError(f"Schema validation failed for {schema_path}:\n{details}")


def main() -> int:
    catalog = load("generation/mechanism_catalog.v1.json")
    assert_valid(catalog, "schemas/mechanism_catalog.schema.json")

    mechanism_ids = [item["mechanism_id"] for item in catalog["mechanisms"]]
    if len(mechanism_ids) != len(set(mechanism_ids)):
        raise AssertionError("Catalog mechanism IDs are not unique")
    if not any(not item["actors"] for item in catalog["mechanisms"]):
        raise AssertionError("Catalog must demonstrate that actor naming is not universal")
    if not all(item.get("entry_origin") for item in catalog["mechanisms"]):
        raise AssertionError("Every mechanism must retain its catalog-entry origin")
    if any("portfolio allocation" in item["mechanism_summary"].lower() for item in catalog["mechanisms"]):
        raise AssertionError("Long-horizon portfolio theory leaked into the mechanism catalog")

    observed_catalog = copy.deepcopy(catalog)
    observed_catalog["mechanisms"][0]["entry_origin"] = {
        "origin_kind": "INTERNAL_OBSERVATION",
        "origin_refs": ["observation:order-book-journal-2026-08-31-001"],
        "origin_summary": "A repeated internal tape observation proposed a new catalog entry.",
        "captured_at": "2026-08-31T12:03:00Z",
    }
    assert_valid(observed_catalog, "schemas/mechanism_catalog.schema.json")

    expected_run = load("examples/generated-run/generation-run.json")
    assert_valid(expected_run, "schemas/generation_run.schema.json")
    if expected_run["candidate_count"] != len(expected_run["candidate_records"]):
        raise AssertionError("Example candidate_count does not match candidate_records")

    expected_candidates: dict[str, dict[str, Any]] = {}
    for record in expected_run["candidate_records"]:
        relative_path = Path("examples/generated-run") / record["candidate_file"]
        candidate = load(relative_path)
        assert_valid(candidate, "schemas/hypothesis_candidate.schema.json")
        expected_candidates[record["candidate_file"]] = candidate
        if candidate["intake_status"] != "INBOX" or candidate["transition"] != {}:
            raise AssertionError("Generator example performed screening or transition work")
        if candidate["provenance"]["source_kind"] != "GENERATOR_RUN":
            raise AssertionError("Generated candidate lost generator provenance")
        forbidden = {"confidence_score", "early_feasibility", "epistemic_stage_status"}
        if forbidden.intersection(candidate):
            raise AssertionError("Generated INBOX candidate contains downstream screening fields")

    with tempfile.TemporaryDirectory(prefix="research-framework-generator-") as temp_dir:
        output_dir = Path(temp_dir) / "run"
        command = [
            sys.executable,
            str(ROOT / "scripts" / "generate_hypotheses.py"),
            "--output-dir",
            str(output_dir),
            "--run-id",
            "generation:example-001",
            "--created-at",
            "2026-08-31T12:00:00Z",
            "--markets",
            "FUTURES",
            "--mechanisms",
            "mechanism:futures-cash-price-discovery",
            "mechanism:gamma-hedging",
            "--operators",
            "PHASE_PATH",
            "EXPECTATION_VIOLATION",
            "MECHANISM_CONNECTION",
            "ASSUMPTION_RELAXATION",
            "--max-candidates",
            "4",
        ]
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            raise AssertionError(
                f"Generator command failed with {completed.returncode}:\n{completed.stdout}\n{completed.stderr}"
            )
        produced_run_path = output_dir / "generation-run.json"
        with produced_run_path.open("r", encoding="utf-8") as handle:
            produced_run = json.load(handle)
        if produced_run != expected_run:
            raise AssertionError("Deterministic producer no longer matches the committed generation-run fixture")
        assert_valid(produced_run, "schemas/generation_run.schema.json")

        for record in produced_run["candidate_records"]:
            path = output_dir / record["candidate_file"]
            with path.open("r", encoding="utf-8") as handle:
                candidate = json.load(handle)
            if candidate != expected_candidates[record["candidate_file"]]:
                raise AssertionError(f"Produced candidate drifted from fixture: {record['candidate_file']}")
            assert_valid(candidate, "schemas/hypothesis_candidate.schema.json")

        repeated = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        if repeated.returncode == 0 or "Refusing to overwrite" not in repeated.stderr:
            raise AssertionError("Generator must refuse to overwrite a non-empty output directory")

        actorless_output = Path(temp_dir) / "actorless"
        actorless_command = [
            sys.executable,
            str(ROOT / "scripts" / "generate_hypotheses.py"),
            "--output-dir",
            str(actorless_output),
            "--run-id",
            "generation:actorless-example",
            "--created-at",
            "2026-08-31T12:01:00Z",
            "--modes",
            "OBSERVATION_DRIVEN",
            "--mechanisms",
            "mechanism:intraday-clock-recurrence",
            "--operators",
            "PHASE_PATH",
            "--max-candidates",
            "1",
        ]
        actorless_completed = subprocess.run(
            actorless_command, cwd=ROOT, text=True, capture_output=True, check=False
        )
        if actorless_completed.returncode != 0:
            raise AssertionError(
                "Actor-free observation route failed:\n"
                f"{actorless_completed.stdout}\n{actorless_completed.stderr}"
            )
        actorless_run_path = actorless_output / "generation-run.json"
        with actorless_run_path.open("r", encoding="utf-8") as handle:
            actorless_run = json.load(handle)
        assert_valid(actorless_run, "schemas/generation_run.schema.json")
        actorless_record = actorless_run["candidate_records"][0]
        if actorless_record["generation_mode"] != "OBSERVATION_DRIVEN":
            raise AssertionError("Actor-free example was forced into a constraint-first route")
        with (actorless_output / actorless_record["candidate_file"]).open(
            "r", encoding="utf-8"
        ) as handle:
            actorless_candidate = json.load(handle)
        assert_valid(actorless_candidate, "schemas/hypothesis_candidate.schema.json")

        full_output = Path(temp_dir) / "full-catalog"
        full_command = [
            sys.executable,
            str(ROOT / "scripts" / "generate_hypotheses.py"),
            "--output-dir",
            str(full_output),
            "--run-id",
            "generation:full-catalog-contract-test",
            "--created-at",
            "2026-08-31T12:02:00Z",
            "--max-candidates",
            "500",
        ]
        full_completed = subprocess.run(
            full_command, cwd=ROOT, text=True, capture_output=True, check=False
        )
        if full_completed.returncode != 0:
            raise AssertionError(
                f"Full-catalog generation failed:\n{full_completed.stdout}\n{full_completed.stderr}"
            )
        with (full_output / "generation-run.json").open("r", encoding="utf-8") as handle:
            full_run = json.load(handle)
        assert_valid(full_run, "schemas/generation_run.schema.json")
        if full_run["candidate_count"] != len(full_run["candidate_records"]):
            raise AssertionError("Full-catalog run has an inconsistent candidate count")
        full_candidate_ids: set[str] = set()
        for record in full_run["candidate_records"]:
            with (full_output / record["candidate_file"]).open("r", encoding="utf-8") as handle:
                full_candidate = json.load(handle)
            assert_valid(full_candidate, "schemas/hypothesis_candidate.schema.json")
            full_candidate_ids.add(full_candidate["candidate_id"])
        if len(full_candidate_ids) != full_run["candidate_count"]:
            raise AssertionError("Full-catalog generation produced duplicate candidate IDs")

    observed_operators = {
        operator
        for record in expected_run["candidate_records"]
        for operator in record["operators"]
    }
    expected_operators = {
        "PHASE_PATH",
        "EXPECTATION_VIOLATION",
        "MECHANISM_CONNECTION",
        "ASSUMPTION_RELAXATION",
    }
    if observed_operators != expected_operators:
        raise AssertionError("Example does not cover all intended generation operators")

    print(
        f"Generator tests passed: {len(catalog['mechanisms'])} mechanisms, "
        f"{expected_run['candidate_count']} deterministic example candidates, 4 operators, "
        f"one actor-free observation route, and {full_run['candidate_count']} full-catalog candidates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
