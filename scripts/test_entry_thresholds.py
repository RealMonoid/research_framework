#!/usr/bin/env python3
"""Contract tests for entry noise screens and multiplicity registers."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Callable

from validate_entry_thresholds import (
    EntryThresholdError,
    validate_entry_threshold_bundle,
    validate_noise_screen,
    validate_schema,
    validate_search_space,
)


ROOT = Path(__file__).resolve().parents[1]


def load(relative_path: str) -> dict[str, Any]:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"Expected object in {relative_path}")
    return value


def expect_rejected(label: str, operation: Callable[[], None]) -> None:
    try:
        operation()
    except EntryThresholdError:
        print(f"PASS negative: {label}")
        return
    raise AssertionError(f"Expected rejection: {label}")


def main() -> int:
    search_space = load("examples/search_space.minimal.json")
    passed = load("examples/noise_screen.pass.json")
    failed = load("examples/noise_screen.fail.json")
    validate_entry_threshold_bundle(search_space, [passed, failed])
    print("PASS positive: Bonferroni search space with PASS and FAIL screens")

    invalid_pass = copy.deepcopy(passed)
    invalid_pass["surrogate_exceedance_count"] = 20
    expect_rejected(
        "noise screen PASS requires exceedance below threshold",
        lambda: validate_noise_screen(invalid_pass, search_space),
    )

    late_threshold = copy.deepcopy(passed)
    late_threshold["threshold_set_at"] = late_threshold["created_at"]
    expect_rejected(
        "noise screen threshold cannot be set after measurement",
        lambda: validate_noise_screen(late_threshold, search_space),
    )

    validation_data = copy.deepcopy(passed)
    validation_data["data_role"] = "VALIDATION"
    expect_rejected(
        "noise screen cannot consume validation data",
        lambda: validate_schema(validation_data, "noise_screen.schema.json"),
    )

    final_holdout = copy.deepcopy(passed)
    final_holdout["data_role"] = "FINAL_HOLDOUT"
    expect_rejected(
        "noise screen cannot consume final holdout",
        lambda: validate_schema(final_holdout, "noise_screen.schema.json"),
    )

    too_few_surrogates = copy.deepcopy(passed)
    too_few_surrogates["surrogate_count"] = 199
    expect_rejected(
        "surrogate count below minimum is rejected",
        lambda: validate_schema(too_few_surrogates, "noise_screen.schema.json"),
    )

    lost_structure = copy.deepcopy(passed)
    lost_structure["preserved_structure"] = ["SESSION_PROFILE"]
    expect_rejected(
        "session preserving shuffle requires preserved structure",
        lambda: validate_schema(lost_structure, "noise_screen.schema.json"),
    )

    blocked_without_reason = copy.deepcopy(passed)
    blocked_without_reason["screen_result"] = "BLOCKED"
    expect_rejected(
        "BLOCKED screen requires blocking reason",
        lambda: validate_schema(blocked_without_reason, "noise_screen.schema.json"),
    )

    threshold_mismatch = copy.deepcopy(passed)
    threshold_mismatch["threshold_percentile"] = 95.0
    expect_rejected(
        "noise screen threshold must match search space register",
        lambda: validate_noise_screen(threshold_mismatch, search_space),
    )

    wrong_bonferroni = copy.deepcopy(search_space)
    wrong_bonferroni["effective_threshold_percentile"] = 95.0
    expect_rejected(
        "Bonferroni threshold is recomputed from frozen family size",
        lambda: validate_search_space(wrong_bonferroni),
    )

    bh_search = copy.deepcopy(search_space)
    bh_search.update(
        {
            "screens_performed": 4,
            "screens_passed": 1,
            "adjustment_method": "BENJAMINI_HOCHBERG",
            "effective_threshold_percentile": 98.75,
        }
    )
    bh_search["method_parameters"].update(
        {
            "bh_rank": 1,
            "p_values_ref": "artifact:entry-screen-p-values-v1",
        }
    )
    validate_search_space(bh_search)
    print("PASS positive: finalized Benjamini-Hochberg family")

    incomplete_bh = copy.deepcopy(bh_search)
    incomplete_bh["screens_performed"] = 3
    expect_rejected(
        "Benjamini-Hochberg requires a completed family",
        lambda: validate_search_space(incomplete_bh),
    )

    multiplicity_bypass = copy.deepcopy(search_space)
    multiplicity_bypass["adjustment_method"] = "NONE_JUSTIFIED"
    multiplicity_bypass["effective_threshold_percentile"] = 95.0
    expect_rejected(
        "NONE_JUSTIFIED cannot bypass correction for multiple screens",
        lambda: validate_search_space(multiplicity_bypass),
    )

    duplicate_index = copy.deepcopy(failed)
    duplicate_index["screen_index"] = 1
    expect_rejected(
        "screen bundle must cover each registered index once",
        lambda: validate_entry_threshold_bundle(search_space, [passed, duplicate_index]),
    )

    wrong_pass_total = copy.deepcopy(search_space)
    wrong_pass_total["screens_passed"] = 2
    expect_rejected(
        "screen bundle PASS count must match register",
        lambda: validate_entry_threshold_bundle(wrong_pass_total, [passed, failed]),
    )

    result_after_register_update = copy.deepcopy(failed)
    result_after_register_update["created_at"] = "2026-08-31T09:21:00Z"
    expect_rejected(
        "screen result must be covered by register update time",
        lambda: validate_entry_threshold_bundle(
            search_space, [passed, result_after_register_update]
        ),
    )

    print("Entry-threshold tests passed: 2 positive paths, 14 negative invariants.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
