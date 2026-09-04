#!/usr/bin/env python3
"""Regression tests for the scientific skill capability manifest."""

from __future__ import annotations

import copy

from validate_scientific_skill_manifest import ROOT, load_object, validate_manifest


def main() -> int:
    baseline = load_object(ROOT / "capabilities" / "scientific_skill_manifest.v1.json")
    if validate_manifest(baseline):
        raise SystemExit("Expected the checked-in scientific skill manifest to be valid")

    duplicate = copy.deepcopy(baseline)
    duplicate["skills"].append(copy.deepcopy(duplicate["skills"][0]))
    if not any("skill_id values must be unique" in error for error in validate_manifest(duplicate)):
        raise SystemExit("Duplicate skill ID was accepted")

    deferred_without_reason = copy.deepcopy(baseline)
    deferred = next(entry for entry in deferred_without_reason["skills"] if entry["status"] == "DEFERRED_NO_USE")
    del deferred["defer_reason"]
    if not validate_manifest(deferred_without_reason):
        raise SystemExit("Deferred skill without a reason was accepted")

    active_with_reason = copy.deepcopy(baseline)
    active = next(entry for entry in active_with_reason["skills"] if entry["status"] == "ACTIVE_OPTIONAL")
    active["defer_reason"] = "This field must not hide an active status."
    if not validate_manifest(active_with_reason):
        raise SystemExit("Active skill with a defer reason was accepted")

    print("Scientific skill manifest tests passed: valid map and status/identity regressions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
