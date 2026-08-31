#!/usr/bin/env python3
"""Validate entry-screen schemas plus arithmetic and cross-artifact invariants."""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
TOLERANCE = 1e-8


class EntryThresholdError(ValueError):
    """Raised when a structurally valid artifact violates a semantic invariant."""


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise EntryThresholdError(f"Expected a JSON object in {path}")
    return value


def validate_schema(document: dict[str, Any], schema_name: str) -> None:
    schema = load_json(ROOT / "schemas" / schema_name)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda error: error.json_path)
    if errors:
        details = "; ".join(f"{error.json_path}: {error.message}" for error in errors)
        raise EntryThresholdError(f"Schema validation failed for {schema_name}: {details}")


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise EntryThresholdError(f"Timestamp must include a timezone: {value}")
    return parsed


def expected_threshold(search_space: dict[str, Any]) -> float:
    alpha = float(search_space["family_alpha"])
    planned = int(search_space["planned_screen_count"])
    method = search_space["adjustment_method"]
    parameters = search_space["method_parameters"]

    if method == "BONFERRONI":
        cutoff = alpha / planned
    elif method == "BENJAMINI_HOCHBERG":
        if search_space["screens_performed"] != planned:
            raise EntryThresholdError(
                "BENJAMINI_HOCHBERG requires a completed batch: screens_performed "
                "must equal planned_screen_count"
            )
        rank = parameters["bh_rank"]
        if rank != search_space["screens_passed"]:
            raise EntryThresholdError("BH rank must equal screens_passed")
        cutoff = 0.0 if rank == 0 else alpha * rank / planned
    elif method == "EFFECTIVE_TESTS_ESTIMATE":
        effective_count = float(parameters["effective_test_count"])
        if effective_count > planned:
            raise EntryThresholdError(
                "effective_test_count cannot exceed planned_screen_count"
            )
        cutoff = alpha / effective_count
    elif method == "NONE_JUSTIFIED":
        if planned != 1:
            raise EntryThresholdError(
                "NONE_JUSTIFIED is allowed only for a one-test family; "
                "multiple screens require multiplicity adjustment"
            )
        cutoff = alpha
    else:  # Defensive; the schema already controls this enum.
        raise EntryThresholdError(f"Unsupported adjustment_method: {method}")

    return 100.0 * (1.0 - cutoff)


def validate_search_space(document: dict[str, Any]) -> None:
    validate_schema(document, "search_space.schema.json")

    if parse_timestamp(document["created_at"]) > parse_timestamp(document["updated_at"]):
        raise EntryThresholdError("search-space created_at must not be after updated_at")
    if document["planned_screen_count"] > document["candidates_registered"]:
        raise EntryThresholdError(
            "planned_screen_count cannot exceed candidates_registered"
        )
    if document["screens_performed"] > document["planned_screen_count"]:
        raise EntryThresholdError("screens_performed cannot exceed planned_screen_count")
    if document["screens_passed"] > document["screens_performed"]:
        raise EntryThresholdError("screens_passed cannot exceed screens_performed")

    expected = expected_threshold(document)
    actual = float(document["effective_threshold_percentile"])
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=TOLERANCE):
        raise EntryThresholdError(
            "effective_threshold_percentile is inconsistent with the declared "
            f"multiplicity method: expected {expected:.12g}, got {actual:.12g}"
        )


def validate_noise_screen(
    screen: dict[str, Any], search_space: dict[str, Any]
) -> None:
    validate_schema(screen, "noise_screen.schema.json")
    validate_search_space(search_space)

    if screen["search_space_ref"] != search_space["search_space_id"]:
        raise EntryThresholdError("noise screen references a different search space")
    if not 1 <= screen["screen_index"] <= search_space["screens_performed"]:
        raise EntryThresholdError(
            "screen_index must refer to an already counted performed screen"
        )
    if parse_timestamp(screen["threshold_set_at"]) >= parse_timestamp(screen["created_at"]):
        raise EntryThresholdError("threshold_set_at must be strictly before created_at")
    if screen["surrogate_exceedance_count"] > screen["surrogate_count"]:
        raise EntryThresholdError(
            "surrogate_exceedance_count cannot exceed surrogate_count"
        )

    registered_threshold = float(search_space["effective_threshold_percentile"])
    screen_threshold = float(screen["threshold_percentile"])
    if not math.isclose(
        screen_threshold, registered_threshold, rel_tol=0.0, abs_tol=TOLERANCE
    ):
        raise EntryThresholdError(
            "noise-screen threshold does not match the search-space register"
        )

    empirical_p = screen["surrogate_exceedance_count"] / screen["surrogate_count"]
    cutoff = 1.0 - screen_threshold / 100.0
    if screen["screen_result"] == "PASS" and not empirical_p < cutoff:
        raise EntryThresholdError(
            "PASS requires surrogate_exceedance_count / surrogate_count to be "
            "strictly below the multiplicity-adjusted cutoff"
        )
    if screen["screen_result"] == "FAIL" and empirical_p < cutoff:
        raise EntryThresholdError(
            "FAIL contradicts an exceedance rate below the registered cutoff"
        )


def validate_entry_threshold_bundle(
    search_space: dict[str, Any], screens: Sequence[dict[str, Any]]
) -> None:
    """Validate a complete register snapshot, not merely isolated screen files."""

    validate_search_space(search_space)
    for screen in screens:
        validate_noise_screen(screen, search_space)

    performed = search_space["screens_performed"]
    if len(screens) != performed:
        raise EntryThresholdError(
            "the supplied noise-screen bundle must contain exactly screens_performed files"
        )

    screen_ids = [screen["screen_id"] for screen in screens]
    if len(screen_ids) != len(set(screen_ids)):
        raise EntryThresholdError("noise-screen bundle contains duplicate screen_id values")

    actual_indexes = {screen["screen_index"] for screen in screens}
    expected_indexes = set(range(1, performed + 1))
    if actual_indexes != expected_indexes:
        raise EntryThresholdError(
            "noise-screen indexes must cover every performed screen exactly once"
        )

    actual_passes = sum(screen["screen_result"] == "PASS" for screen in screens)
    if actual_passes != search_space["screens_passed"]:
        raise EntryThresholdError(
            "screens_passed does not match PASS results in the supplied bundle"
        )

    register_created = parse_timestamp(search_space["created_at"])
    register_updated = parse_timestamp(search_space["updated_at"])
    for screen in screens:
        if parse_timestamp(screen["threshold_set_at"]) < register_created:
            raise EntryThresholdError(
                "noise-screen threshold cannot predate the search-space register"
            )
        if parse_timestamp(screen["created_at"]) > register_updated:
            raise EntryThresholdError(
                "noise-screen result is not covered by search-space updated_at"
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a search-space register and one or more linked noise screens, "
            "including arithmetic rules JSON Schema cannot express."
        )
    )
    parser.add_argument("--search-space", type=Path, required=True)
    parser.add_argument("--noise-screen", type=Path, action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        search_space = load_json(args.search_space)
        screens = [load_json(path) for path in args.noise_screen]
        validate_entry_threshold_bundle(search_space, screens)
    except (EntryThresholdError, OSError, json.JSONDecodeError) as error:
        print(f"Entry-threshold validation failed: {error}", file=sys.stderr)
        return 1
    print(
        f"Entry-threshold validation passed: {search_space['search_space_id']}, "
        f"{len(args.noise_screen)} screen(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
