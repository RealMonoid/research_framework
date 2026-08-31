#!/usr/bin/env python3
"""Generate cheap INBOX candidates from a versioned short-horizon mechanism catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "generation" / "mechanism_catalog.v1.json"
PRODUCER_ID = "producer:mechanism-hypothesis-generator"
PRODUCER_VERSION = "1.0.0"

GENERATION_MODES = (
    "CONSTRAINT_FIRST",
    "MICROSTRUCTURE_STATE",
    "LINKAGE_OR_IDENTITY",
    "LITERATURE_REPLICATION",
    "OBSERVATION_DRIVEN",
)
OPERATORS = (
    "PHASE_PATH",
    "EXPECTATION_VIOLATION",
    "MECHANISM_CONNECTION",
    "ASSUMPTION_RELAXATION",
)
MARKET_SCOPES = (
    "EQUITIES",
    "INDEX_ETF",
    "FUTURES",
    "OPTIONS",
    "FX",
    "CRYPTO_SPOT",
    "CRYPTO_PERPETUAL",
    "RATES",
    "COMMODITIES",
    "CROSS_MARKET",
)
NATURAL_HORIZONS = (
    "SUB_SECOND",
    "SECONDS",
    "MINUTES",
    "HOURS",
    "SESSION",
    "ONE_TO_FIVE_DAYS",
)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "candidate"


def lower_initial(value: str) -> str:
    if not value:
        return value
    return value[0].lower() + value[1:]


def compact_key(parts: Sequence[str]) -> str:
    raw = "-".join(slug(part) for part in parts if part)
    if len(raw) <= 76:
        return raw
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    return f"{raw[:63].rstrip('-')}-{digest}"


def validate_timestamp(value: str) -> str:
    parsed = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(parsed)
    except ValueError as error:
        raise argparse.ArgumentTypeError("created-at must be an ISO-8601 timestamp") from error
    return value


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_catalog_invariants(catalog: dict[str, Any]) -> None:
    mechanisms = catalog.get("mechanisms")
    if not isinstance(mechanisms, list) or not mechanisms:
        raise ValueError("Catalog must contain at least one mechanism")
    mechanism_ids = [item.get("mechanism_id") for item in mechanisms if isinstance(item, dict)]
    if len(mechanism_ids) != len(set(mechanism_ids)):
        raise ValueError("mechanism_id values must be unique")
    for mechanism in mechanisms:
        phase_names = [phase["phase"] for phase in mechanism["phases"]]
        if len(phase_names) != len(set(phase_names)):
            raise ValueError(f"Duplicate phase in {mechanism['mechanism_id']}")
        source_ids = [source["source_id"] for source in mechanism["literature_sources"]]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError(f"Duplicate source_id in {mechanism['mechanism_id']}")


def select_mechanisms(
    catalog: dict[str, Any],
    modes: set[str],
    markets: set[str],
    horizons: set[str],
    mechanism_ids: set[str],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for mechanism in sorted(catalog["mechanisms"], key=lambda item: item["mechanism_id"]):
        if modes and not modes.intersection(mechanism["generation_modes"]):
            continue
        if markets and not markets.intersection(mechanism["market_scopes"]):
            continue
        if horizons and not horizons.intersection(mechanism["natural_horizons"]):
            continue
        if mechanism_ids and mechanism["mechanism_id"] not in mechanism_ids:
            continue
        selected.append(mechanism)
    return selected


def choose_mode(mechanism: dict[str, Any], requested_modes: Sequence[str]) -> str:
    for mode in requested_modes:
        if mode in mechanism["generation_modes"]:
            return mode
    return mechanism["generation_modes"][0]


def mechanism_source_refs(mechanisms: Sequence[dict[str, Any]]) -> list[str]:
    return unique(
        source["source_id"]
        for mechanism in mechanisms
        for source in mechanism["literature_sources"]
    )


def make_proposal(
    *,
    key_parts: Sequence[str],
    generation_mode: str,
    operators: Sequence[str],
    mechanisms: Sequence[dict[str, Any]],
    phase: str,
    expected_signature: str,
    statement: str,
) -> dict[str, Any]:
    key = compact_key(key_parts)
    return {
        "key": key,
        "generation_mode": generation_mode,
        "operators": list(operators),
        "mechanisms": list(mechanisms),
        "phase": phase,
        "expected_signature": expected_signature,
        "idea_statement": statement,
    }


def phase_path_proposals(
    mechanisms: Sequence[dict[str, Any]], requested_modes: Sequence[str]
) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for mechanism in mechanisms:
        signature = mechanism["observable_signatures"][0]["statement"]
        for phase in mechanism["phases"]:
            statement = (
                f"When {lower_initial(phase['trigger'])}, test whether "
                f"{lower_initial(phase['expected_response'])}. "
                f"Observable signature: {signature}. Natural horizon: {phase['horizon']}."
            )
            proposals.append(
                make_proposal(
                    key_parts=(mechanism["mechanism_id"], "phase", phase["phase"]),
                    generation_mode=choose_mode(mechanism, requested_modes),
                    operators=("PHASE_PATH",),
                    mechanisms=(mechanism,),
                    phase=phase["phase"],
                    expected_signature=signature,
                    statement=statement,
                )
            )
    return proposals


def expectation_violation_proposals(
    mechanisms: Sequence[dict[str, Any]], requested_modes: Sequence[str]
) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for mechanism in mechanisms:
        phase = mechanism["phases"][0]
        signature = mechanism["observable_signatures"][0]["statement"]
        violation = mechanism["violation_hypotheses"][0]
        statement = (
            f"When {lower_initial(phase['trigger'])}, but the expected signature '{signature}' is "
            f"absent or inverted, "
            f"test this separate hypothesis: {violation}"
        )
        proposals.append(
            make_proposal(
                key_parts=(mechanism["mechanism_id"], "expectation-violation"),
                generation_mode=choose_mode(mechanism, requested_modes),
                operators=("EXPECTATION_VIOLATION",),
                mechanisms=(mechanism,),
                phase=phase["phase"],
                expected_signature=signature,
                statement=statement,
            )
        )
    return proposals


def assumption_relaxation_proposals(
    mechanisms: Sequence[dict[str, Any]], requested_modes: Sequence[str]
) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for mechanism in mechanisms:
        alternative = mechanism["alternative_observables"][0]
        phase = mechanism["phases"][0]
        statement = (
            f"Relax the assumption that primary price return is the best footprint of "
            f"'{mechanism['title']}'. Use '{alternative['observable']}' instead: "
            f"{alternative['hypothesis_prompt']}"
        )
        proposals.append(
            make_proposal(
                key_parts=(mechanism["mechanism_id"], "assumption-relaxation"),
                generation_mode=choose_mode(mechanism, requested_modes),
                operators=("ASSUMPTION_RELAXATION",),
                mechanisms=(mechanism,),
                phase=phase["phase"],
                expected_signature=alternative["observable"],
                statement=statement,
            )
        )
    return proposals


def connection_proposals(
    mechanisms: Sequence[dict[str, Any]], requested_modes: Sequence[str]
) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for left, right in combinations(mechanisms, 2):
        shared_tags = sorted(set(left["connection_tags"]).intersection(right["connection_tags"]))
        if not shared_tags:
            continue
        left_phase = left["phases"][0]
        right_phase = right["phases"][0]
        left_signature = left["observable_signatures"][0]["statement"]
        right_signature = right["observable_signatures"][0]["statement"]
        mode = "LINKAGE_OR_IDENTITY"
        if mode not in left["generation_modes"] and mode not in right["generation_modes"]:
            for requested in requested_modes:
                if requested in left["generation_modes"] or requested in right["generation_modes"]:
                    mode = requested
                    break
            else:
                mode = left["generation_modes"][0]
        statement = (
            f"Test the connection between '{left['title']}' and '{right['title']}' through their shared "
            f"context {shared_tags[0]}. When '{left_phase['trigger']}' and '{right_phase['trigger']}' "
            f"overlap, test whether the joint footprint appears more strongly, earlier, or in a "
            f"different instrument than either mechanism alone. Observables: "
            f"{left_signature}; {right_signature}."
        )
        proposals.append(
            make_proposal(
                key_parts=(left["mechanism_id"], right["mechanism_id"], "connection"),
                generation_mode=mode,
                operators=("MECHANISM_CONNECTION",),
                mechanisms=(left, right),
                phase="CROSS_MECHANISM",
                expected_signature=f"{left_signature}; {right_signature}",
                statement=statement,
            )
        )
    return proposals


def round_robin(buckets: Sequence[Sequence[dict[str, Any]]]) -> list[dict[str, Any]]:
    ordered: list[dict[str, Any]] = []
    offset = 0
    while True:
        appended = False
        for bucket in buckets:
            if offset < len(bucket):
                ordered.append(bucket[offset])
                appended = True
        if not appended:
            return ordered
        offset += 1


def build_candidate(
    proposal: dict[str, Any],
    *,
    run_id: str,
    catalog_id: str,
    created_at: str,
    inbox_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    mechanism_ids = [item["mechanism_id"] for item in proposal["mechanisms"]]
    source_ids = mechanism_source_refs(proposal["mechanisms"])
    candidate_id = f"candidate:{proposal['key']}:1.0.0"
    idea_id = f"idea:{proposal['key']}"
    file_name = f"{proposal['key']}.json"
    candidate = {
        "schema_version": "1.4.0",
        "candidate_id": candidate_id,
        "candidate_version": "1.0.0",
        "inbox_id": inbox_id,
        "idea_id": idea_id,
        "created_at": created_at,
        "updated_at": created_at,
        "provenance": {
            "source_kind": "GENERATOR_RUN",
            "source_refs": unique((run_id, catalog_id, *mechanism_ids, *source_ids)),
            "origin_summary": (
                f"Generated by the mechanism-catalog producer with operator(s) "
                f"{', '.join(proposal['operators'])} from {', '.join(mechanism_ids)}. "
                "Unscreened INBOX candidate; no evidence or edge claim."
            ),
        },
        "idea_statement": proposal["idea_statement"],
        "consumed_data_refs": unique((catalog_id, *mechanism_ids, *source_ids)),
        "intake_status": "INBOX",
        "transition": {},
    }
    record = {
        "candidate_id": candidate_id,
        "idea_id": idea_id,
        "candidate_file": f"candidates/{file_name}",
        "generation_mode": proposal["generation_mode"],
        "operators": proposal["operators"],
        "mechanism_refs": mechanism_ids,
        "phase": proposal["phase"],
        "expected_signature": proposal["expected_signature"],
        "idea_statement": proposal["idea_statement"],
    }
    return candidate, record


def generate(
    catalog: dict[str, Any],
    *,
    run_id: str,
    created_at: str,
    inbox_id: str,
    requested_modes: Sequence[str],
    requested_operators: Sequence[str],
    markets: Sequence[str],
    horizons: Sequence[str],
    mechanism_ids: Sequence[str],
    max_candidates: int,
) -> tuple[dict[str, Any], list[tuple[str, dict[str, Any]]]]:
    validate_catalog_invariants(catalog)
    selected = select_mechanisms(
        catalog,
        set(requested_modes),
        set(markets),
        set(horizons),
        set(mechanism_ids),
    )
    if not selected:
        raise ValueError("No mechanisms match the requested generation scope")

    factories = {
        "PHASE_PATH": lambda: phase_path_proposals(selected, requested_modes),
        "EXPECTATION_VIOLATION": lambda: expectation_violation_proposals(selected, requested_modes),
        "MECHANISM_CONNECTION": lambda: connection_proposals(selected, requested_modes),
        "ASSUMPTION_RELAXATION": lambda: assumption_relaxation_proposals(selected, requested_modes),
    }
    buckets = [factories[operator]() for operator in requested_operators]
    proposals = round_robin(buckets)[:max_candidates]
    if not proposals:
        raise ValueError("The selected operator set produced no candidates")

    records: list[dict[str, Any]] = []
    candidates: list[tuple[str, dict[str, Any]]] = []
    for proposal in proposals:
        candidate, record = build_candidate(
            proposal,
            run_id=run_id,
            catalog_id=catalog["catalog_id"],
            created_at=created_at,
            inbox_id=inbox_id,
        )
        records.append(record)
        candidates.append((record["candidate_file"], candidate))

    run = {
        "schema_version": "1.0.0",
        "generation_run_id": run_id,
        "created_at": created_at,
        "producer": {
            "kind": "DETERMINISTIC",
            "producer_id": PRODUCER_ID,
            "producer_version": PRODUCER_VERSION,
        },
        "catalog_ref": {
            "catalog_id": catalog["catalog_id"],
            "catalog_version": catalog["catalog_version"],
        },
        "request": {
            "generation_modes": list(requested_modes),
            "operators": list(requested_operators),
            "market_scopes": list(markets),
            "natural_horizons": list(horizons),
            "mechanism_ids": list(mechanism_ids),
            "max_candidates": max_candidates,
        },
        "candidate_count": len(records),
        "candidate_records": records,
    }
    return run, candidates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate literature-anchored INBOX hypotheses. The producer performs no screening, "
            "evidence grading, backtesting or promotion."
        )
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--created-at", type=validate_timestamp, default=None)
    parser.add_argument("--inbox-id", default="inbox:generated-short-horizon-ideas")
    parser.add_argument("--modes", nargs="*", choices=GENERATION_MODES, default=[])
    parser.add_argument("--operators", nargs="+", choices=OPERATORS, default=list(OPERATORS))
    parser.add_argument("--markets", nargs="*", choices=MARKET_SCOPES, default=[])
    parser.add_argument("--horizons", nargs="*", choices=NATURAL_HORIZONS, default=[])
    parser.add_argument("--mechanisms", nargs="*", default=[])
    parser.add_argument("--max-candidates", type=int, default=40)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_candidates < 1 or args.max_candidates > 500:
        raise SystemExit("--max-candidates must be between 1 and 500")
    output_dir = args.output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        catalog = read_json(args.catalog.resolve())
        run, candidates = generate(
            catalog,
            run_id=args.run_id,
            created_at=args.created_at or now_utc(),
            inbox_id=args.inbox_id,
            requested_modes=args.modes,
            requested_operators=args.operators,
            markets=args.markets,
            horizons=args.horizons,
            mechanism_ids=args.mechanisms,
            max_candidates=args.max_candidates,
        )
        write_json(output_dir / "generation-run.json", run)
        for relative_path, candidate in candidates:
            write_json(output_dir / relative_path, candidate)
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Generation failed: {error}", file=sys.stderr)
        return 1

    print(
        f"Generated {run['candidate_count']} INBOX candidates in {output_dir}. "
        "No screening or promotion was performed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
