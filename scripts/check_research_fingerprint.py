#!/usr/bin/env python3
"""Protect the full effective research state from silent change.

The comparison is deliberately mechanical. It does not decide whether a
change is good. Any difference becomes a pending proposal; the baseline stays
effective until the user explicitly authorizes a new research version.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


METADATA_FIELDS = {"schema_version", "fingerprint_id", "created_at", "fingerprint_sha256"}

SECTION_LABELS = {
    "research_question": "Forschungsfrage",
    "source_strategy": "Quellstrategie",
    "market_and_instruments": "Markt und Instrumente",
    "time_scope": "Zeitraum und Zeithorizont",
    "constructs_and_operationalizations": "Begriffe und Messdefinitionen",
    "trigger_entry_and_position": "Auslöser, Einstieg und Position",
    "outcomes_targets_and_exits": "Ergebnis, Ziel und Ausstieg",
    "conditions_filters_and_exclusions": "Bedingungen, Filter und Ausschlüsse",
    "data_sampling_and_observability": "Daten, Stichprobe und Verfügbarkeit",
    "analysis_and_inference": "Auswertung und Schlussfolgerung",
    "costs_execution_and_risk": "Kosten, Ausführung und Risiko",
    "results_and_continuation": "Ergebnisstand und Fortsetzung",
    "additional_material_commitments": "weitere Festlegungen",
    "protected_artifacts": "geschützte Forschungsunterlagen",
    "completeness": "Vollständigkeitserklärung",
    "research_id": "Research-ID",
    "research_version": "Forschungsversion",
}


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def _normalise(value: Any, key: str | None = None) -> Any:
    if isinstance(value, Mapping):
        return {
            item_key: _normalise(item_value, item_key)
            for item_key, item_value in sorted(value.items())
        }
    if isinstance(value, list):
        items = [_normalise(item) for item in value]
        if key in {"source_refs", "known_gaps"}:
            return sorted(items, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
        if key == "additional_material_commitments":
            return sorted(items, key=lambda item: item.get("commitment_id", ""))
        if key == "protected_artifacts":
            return sorted(items, key=lambda item: item.get("artifact_ref", ""))
        return items
    return value


def fingerprint_payload(fingerprint: Mapping[str, Any]) -> dict[str, Any]:
    """Return the canonical, decision-relevant part of a fingerprint."""

    payload = {
        key: value
        for key, value in fingerprint.items()
        if key not in METADATA_FIELDS
    }
    return _normalise(payload)


def calculate_fingerprint_sha256(fingerprint: Mapping[str, Any]) -> str:
    rendered = json.dumps(
        fingerprint_payload(fingerprint),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(rendered).hexdigest()


def verify_fingerprint(fingerprint: Mapping[str, Any], label: str) -> None:
    expected = fingerprint.get("fingerprint_sha256")
    if not isinstance(expected, str):
        raise ValueError(f"{label}.fingerprint_sha256 must be a string")
    observed = calculate_fingerprint_sha256(fingerprint)
    if expected != observed:
        raise ValueError(
            f"{label} fingerprint hash is invalid: recorded {expected}, calculated {observed}"
        )


def _escape_pointer(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def _diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    if type(before) is not type(after):
        return [{
            "json_pointer": path or "/",
            "before_present": True,
            "after_present": True,
            "before": before,
            "after": after,
        }]
    if isinstance(before, Mapping):
        changes: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after)):
            pointer = f"{path}/{_escape_pointer(str(key))}"
            if key not in before:
                changes.append({
                    "json_pointer": pointer,
                    "before_present": False,
                    "after_present": True,
                    "before": None,
                    "after": after[key],
                })
            elif key not in after:
                changes.append({
                    "json_pointer": pointer,
                    "before_present": True,
                    "after_present": False,
                    "before": before[key],
                    "after": None,
                })
            else:
                changes.extend(_diff(before[key], after[key], pointer))
        return changes
    if isinstance(before, list):
        if before == after:
            return []
        return [{
            "json_pointer": path or "/",
            "before_present": True,
            "after_present": True,
            "before": before,
            "after": after,
        }]
    if before != after:
        return [{
            "json_pointer": path or "/",
            "before_present": True,
            "after_present": True,
            "before": before,
            "after": after,
        }]
    return []


def _plain_labels(changes: list[dict[str, Any]]) -> list[str]:
    labels: list[str] = []
    for change in changes:
        tokens = [token for token in change["json_pointer"].split("/") if token]
        if tokens and tokens[0] == "material_specification" and len(tokens) > 1:
            key = tokens[1]
        elif tokens:
            key = tokens[0]
        else:
            key = "research"
        label = SECTION_LABELS.get(key, key.replace("_", " "))
        if label not in labels:
            labels.append(label)
    return labels


def _derived_id(prefix: str, decision_id: str) -> str:
    candidate = f"{prefix}:{decision_id}"
    if len(candidate) > 199:
        digest = hashlib.sha256(decision_id.encode("utf-8")).hexdigest()[:24]
        candidate = f"{prefix}:{digest}"
    return candidate


def build_fingerprint_check(
    decision: Mapping[str, Any],
    baseline: Mapping[str, Any] | None,
    candidate: Mapping[str, Any],
    *,
    checked_at: str,
) -> dict[str, Any]:
    decision_id = decision.get("decision_id")
    if not isinstance(decision_id, str):
        raise ValueError("decision_id must be a string")
    guard = _mapping(decision.get("fingerprint_guard"), "fingerprint_guard")
    mode = guard.get("mode")
    if mode not in {"PRESERVE_EFFECTIVE", "NEW_RESEARCH_CREATION", "NOT_APPLICABLE"}:
        raise ValueError("fingerprint_guard.mode is unsupported")

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "check_id": _derived_id("fingerprint-check", decision_id),
        "checked_at": checked_at,
        "routing_decision_ref": decision_id,
        "guard_mode": mode,
        "baseline_fingerprint_ref": None,
        "baseline_fingerprint_sha256": None,
        "candidate_fingerprint_ref": None,
        "candidate_fingerprint_sha256": None,
        "overall_status": "NOT_APPLICABLE",
        "changes": [],
        "proposal": None,
        "plain_language_summary": "Für diesen Schritt ist kein bestehender Forschungsstand zu vergleichen.",
        "candidate_may_become_effective": True,
    }

    if mode == "NOT_APPLICABLE":
        return report

    verify_fingerprint(candidate, "candidate")
    candidate_ref = candidate.get("fingerprint_id")
    candidate_hash = candidate.get("fingerprint_sha256")
    if not isinstance(candidate_ref, str):
        raise ValueError("candidate.fingerprint_id must be a string")
    report["candidate_fingerprint_ref"] = candidate_ref
    report["candidate_fingerprint_sha256"] = candidate_hash

    if mode == "NEW_RESEARCH_CREATION":
        report.update({
            "overall_status": "NOT_COMPARABLE_NEW_RESEARCH",
            "plain_language_summary": (
                "Es gibt noch keinen wirksamen Forschungsstand. Der neue Fingerabdruck muss bei der Aufnahme als eigene Forschungsversion sichtbar festgelegt werden."
            ),
        })
        return report

    baseline = _mapping(baseline, "baseline")
    verify_fingerprint(baseline, "baseline")
    baseline_ref = baseline.get("fingerprint_id")
    baseline_hash = baseline.get("fingerprint_sha256")
    if not isinstance(baseline_ref, str):
        raise ValueError("baseline.fingerprint_id must be a string")
    if guard.get("baseline_fingerprint_ref") != baseline_ref:
        raise ValueError("baseline fingerprint reference does not match the routing guard")
    if guard.get("baseline_fingerprint_sha256") != baseline_hash:
        raise ValueError("baseline fingerprint hash does not match the routing guard")

    changes = _diff(fingerprint_payload(baseline), fingerprint_payload(candidate))
    report.update({
        "baseline_fingerprint_ref": baseline_ref,
        "baseline_fingerprint_sha256": baseline_hash,
        "changes": changes,
    })
    if not changes:
        report.update({
            "overall_status": "UNCHANGED",
            "plain_language_summary": (
                "Der vollständige Forschungsfingerabdruck ist unverändert. Es wurden weder Festlegungen noch geschützte Forschungsunterlagen ausgetauscht."
            ),
        })
        return report

    labels = _plain_labels(changes)
    proposal_id = _derived_id("change-proposal", decision_id)
    report.update({
        "overall_status": "CHANGE_PROPOSED",
        "proposal": {
            "proposal_id": proposal_id,
            "status": "PENDING_USER_DECISION",
            "effective_fingerprint_ref": baseline_ref,
            "candidate_fingerprint_ref": candidate_ref,
            "changed_paths": [change["json_pointer"] for change in changes],
            "decision_required": True,
            "effect_if_accepted": "CREATE_NEW_RESEARCH_VERSION",
        },
        "plain_language_summary": (
            "Vorgeschlagene Änderung in: " + ", ".join(labels) + ". "
            "Die bisherige Forschungsversion bleibt wirksam. Die neue Fassung darf nur nach einer sichtbaren Entscheidung als neue Version angelegt werden."
        ),
        "candidate_may_become_effective": False,
    })
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare a candidate research fingerprint with the effective baseline."
    )
    parser.add_argument("decision", type=Path, help="routing-decision JSON file")
    parser.add_argument("baseline", type=Path, help="effective baseline research-fingerprint JSON file")
    parser.add_argument("candidate", type=Path, help="candidate research-fingerprint JSON file")
    parser.add_argument("--output", type=Path, help="optional comparison-report JSON file")
    parser.add_argument("--checked-at", default=None, help="optional ISO timestamp")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    checked_at = args.checked_at or datetime.now(timezone.utc).isoformat()
    try:
        report = build_fingerprint_check(
            _load(args.decision),
            _load(args.baseline),
            _load(args.candidate),
            checked_at=checked_at,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Fingerprint check failed: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 1 if report["overall_status"] == "CHANGE_PROPOSED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
