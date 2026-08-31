#!/usr/bin/env python3
"""Vertragstests fuer data_snapshot: Schema-Invarianten plus semantische Pruefungen.

Ein Snapshot belegt Herkunft, Abdeckung und Integritaet eines Datenstands. Er
belegt keine Datenqualitaet und keine Eignung fuer eine bestimmte Hypothese.
"""

from __future__ import annotations

import copy
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "data_snapshot.schema.json").read_text(encoding="utf-8"))
EXAMPLE = ROOT / "examples" / "data_snapshot.binance_klines.json"


def _ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def semantic_errors(doc: dict[str, Any]) -> list[str]:
    """Invarianten, die JSON Schema nicht ausdruecken kann."""
    out: list[str] = []
    cov = doc.get("coverage", {})
    gaps = cov.get("gaps", [])

    if cov.get("gap_count") != len(gaps):
        out.append("gap_count entspricht nicht der Anzahl gelisteter Luecken")
    if gaps and cov.get("missing_units") != sum(g["missing_units"] for g in gaps):
        out.append("missing_units entspricht nicht der Summe der Luecken")
    if "first_observation" in cov and "last_observation" in cov:
        if _ts(cov["first_observation"]) >= _ts(cov["last_observation"]):
            out.append("first_observation liegt nicht vor last_observation")

    files = doc.get("files", [])
    digests = [f["sha256"] for f in files if "sha256" in f]
    if len(set(digests)) != len(digests):
        out.append("doppelter sha256 in files: identische Datei mehrfach gezaehlt")
    if files and all("row_count" in f for f in files):
        if sum(f["row_count"] for f in files) != cov.get("row_count"):
            out.append("Summe der Dateizeilen weicht von coverage.row_count ab")

    split = doc.get("split_declaration")
    if split:
        retrieved = doc.get("source", {}).get("retrieved_at")
        if retrieved and _ts(split["declared_at"]) > _ts(retrieved):
            out.append(
                "split_declaration.declared_at liegt nach source.retrieved_at: "
                "die Aufteilung waere nach Datensicht festgelegt worden"
            )
        lo = cov.get("first_observation")
        hi = cov.get("last_observation")
        for key in ("is_boundary", "val_boundary"):
            if key in split and lo and hi and not _ts(lo) < _ts(split[key]) < _ts(hi):
                out.append(f"{key} liegt ausserhalb der Abdeckung")
        if "is_boundary" in split and "val_boundary" in split:
            if _ts(split["is_boundary"]) >= _ts(split["val_boundary"]):
                out.append("is_boundary liegt nicht vor val_boundary")
    return out


def validate(doc: dict[str, Any]) -> list[str]:
    errors = [e.message for e in Draft202012Validator(SCHEMA).iter_errors(doc)]
    return errors + semantic_errors(doc)


MINIMAL: dict[str, Any] = {
    "schema_version": "1.0.0",
    "snapshot_id": "snapshot:minimal",
    "created_at": "2026-08-31T00:00:00Z",
    "data_kind": "FUNDING_RATE",
    "source": {
        "provider": "BINANCE_PUBLIC_DATA",
        "access_method": "BULK_ARCHIVE",
        "retrieved_at": "2026-08-31T00:00:00Z",
        "terms_ref": "frei zugaenglich ohne API-Key",
    },
    "instrument": {
        "venue": "BINANCE_USDM",
        "symbol": "ETHUSDT",
        "instrument_class": "PERPETUAL",
        "timeframe": "8h",
    },
    "coverage": {
        "first_observation": "2020-01-01T00:00:00Z",
        "last_observation": "2020-02-01T00:00:00Z",
        "row_count": 93,
        "timezone": "UTC",
        "continuity_checked": True,
        "gap_count": 0,
    },
    "files": [{"path": "funding.parquet", "bytes": 4096, "sha256": "a" * 64}],
}


def drop_continuity(doc: dict[str, Any]) -> None:
    doc["coverage"]["continuity_checked"] = False
    doc["coverage"]["gap_count"] = 0
    doc["coverage"].pop("gaps", None)
    doc["coverage"].pop("missing_units", None)
    doc.pop("known_limitations", None)


NEGATIVES: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
    ("unbekanntes Top-Level-Feld wird abgelehnt",
     lambda d: d.update({"note": "x"})),
    ("data_kind OTHER ohne Beschreibung",
     lambda d: d.update({"data_kind": "OTHER"})),
    ("provider OTHER ohne Beschreibung",
     lambda d: d["source"].update({"provider": "OTHER"})),
    ("OHLCV kann keine tick-Aufloesung haben",
     lambda d: d["instrument"].update({"timeframe": "tick"})),
    ("timeframe muss dem Muster entsprechen",
     lambda d: d["instrument"].update({"timeframe": "1 minute"})),
    ("Zeitzone muss UTC sein",
     lambda d: d["coverage"].update({"timezone": "Europe/Berlin"})),
    ("sha256 muss 64 Hexzeichen haben",
     lambda d: d["files"][0].update({"sha256": "deadbeef"})),
    ("Datei ohne Pruefsumme wird abgelehnt",
     lambda d: d["files"][0].pop("sha256")),
    ("gap_count > 0 verlangt gelistete Luecken",
     lambda d: d["coverage"].pop("gaps")),
    ("gap_count muss zur Anzahl der Luecken passen",
     lambda d: d["coverage"].update({"gap_count": 5})),
    ("missing_units muss der Summe der Luecken entsprechen",
     lambda d: d["coverage"].update({"missing_units": 999})),
    ("nicht gepruefte Kontinuitaet verlangt known_limitations",
     drop_continuity),
    ("last_observation darf nicht vor first_observation liegen",
     lambda d: d["coverage"].update({"last_observation": "2019-01-01T00:00:00Z"})),
    ("doppelter sha256 wird abgelehnt",
     lambda d: d["files"][1].update({"sha256": d["files"][0]["sha256"]})),
    ("Summe der Dateizeilen muss coverage.row_count treffen",
     lambda d: d["coverage"].update({"row_count": 12345})),
    ("Aufteilung darf nicht nach dem Datenabruf deklariert werden",
     lambda d: d["split_declaration"].update({"declared_at": "2026-08-31T23:00:00Z"})),
    ("Aufteilungsgrenze darf nicht ausserhalb der Abdeckung liegen",
     lambda d: d["split_declaration"].update({"is_boundary": "2030-01-01T00:00:00Z"})),
    ("is_boundary muss vor val_boundary liegen",
     lambda d: d["split_declaration"].update({"is_boundary": "2019-12-28T00:00:00Z"})),
    ("Ableitung ohne Formel wird abgelehnt",
     lambda d: d.update({"derivations": [{"name": "VWAP", "input_columns": ["close"]}]})),
]


def main() -> int:
    Draft202012Validator.check_schema(SCHEMA)
    base = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    positives = 0
    for label, doc in (("committed Binance kline snapshot", base),
                       ("minimal funding-rate snapshot without optional blocks", MINIMAL)):
        errors = validate(doc)
        if errors:
            print(f"FAIL positive: {label}")
            for message in errors:
                print("   ", message)
            return 1
        print(f"PASS positive: {label}")
        positives += 1

    failed = 0
    for label, mutation in NEGATIVES:
        doc = copy.deepcopy(base)
        mutation(doc)
        if validate(doc):
            print(f"PASS negative: {label}")
        else:
            print(f"FAIL negative: {label} was accepted")
            failed += 1

    if failed:
        return 1
    print(
        f"Data-snapshot tests passed: {positives} positive, "
        f"{len(NEGATIVES)} negative invariants."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
