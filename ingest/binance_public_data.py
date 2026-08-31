#!/usr/bin/env python3
"""Nicht-normativer Adapter fuer das oeffentliche Binance-Datenarchiv.

Dieser Adapter ist KEIN Bestandteil des normativen Frameworks. Er ist eine
Bezugsquelle, die einen zu ``schemas/data_snapshot.schema.json`` konformen
Snapshot erzeugt. Andere Anbieter koennen durch weitere Adapter ergaenzt werden,
ohne dass sich der Vertrag aendert.

Der Adapter laedt ausschliesslich oeffentlich zugaengliche Dateien. Er benoetigt
keinen API-Key, keinen Account und keine Zugangsdaten.

Er trifft keine Aussage darueber, ob die geladenen Daten fuer eine bestimmte
Hypothese ausreichen. Ob Historientiefe und Ereignisdichte fuer eine Studie
genuegen, entscheidet die Machbarkeitspruefung, nicht der Download.

Aufbau: Planung, Pruefsummen-Parsing und Abdeckungsanalyse sind reine
Funktionen ohne Netzwerkzugriff und werden offline getestet. Nur ``fetch`` und
``run`` sprechen mit dem Netz.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

BASE_URL = "https://data.binance.vision"

MARKETS = {
    "spot": "data/spot",
    "um": "data/futures/um",
    "cm": "data/futures/cm",
}

# Binance-Datenart -> (Pfadsegment, data_kind im Snapshot-Vertrag)
KINDS = {
    "klines": ("klines", "OHLCV"),
    "aggTrades": ("aggTrades", "AGG_TRADES"),
    "trades": ("trades", "TRADES"),
    "fundingRate": ("fundingRate", "FUNDING_RATE"),
}

INTERVAL_SECONDS = {
    "1s": 1, "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
    "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600, "8h": 28800,
    "12h": 43200, "1d": 86400,
}


class IngestError(RuntimeError):
    """Fehler in Planung, Pruefsumme oder Abdeckungsanalyse."""


# --------------------------------------------------------------------------
# Reine Planungs- und Parsing-Funktionen (offline getestet)
# --------------------------------------------------------------------------


def month_range(start: str, end: str) -> list[str]:
    """Liefert YYYY-MM Strings von start bis end einschliesslich."""
    try:
        first = datetime.strptime(start, "%Y-%m")
        last = datetime.strptime(end, "%Y-%m")
    except ValueError as exc:
        raise IngestError(f"Monat muss als YYYY-MM angegeben werden: {exc}") from exc
    if first > last:
        raise IngestError("Startmonat liegt nach Endmonat")
    out: list[str] = []
    year, month = first.year, first.month
    while (year, month) <= (last.year, last.month):
        out.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            year, month = year + 1, 1
    return out


def archive_name(kind: str, symbol: str, month: str, interval: str | None) -> str:
    if kind == "klines":
        if not interval:
            raise IngestError("klines benoetigen ein Intervall")
        return f"{symbol}-{interval}-{month}.zip"
    return f"{symbol}-{kind}-{month}.zip"


def build_urls(
    market: str,
    kind: str,
    symbol: str,
    months: Sequence[str],
    interval: str | None = None,
) -> list[str]:
    """Baut die Archiv-URLs. Reine Funktion, kein Netzwerkzugriff."""
    if market not in MARKETS:
        raise IngestError(f"unbekannter Markt {market!r}; erlaubt: {sorted(MARKETS)}")
    if kind not in KINDS:
        raise IngestError(f"unbekannte Datenart {kind!r}; erlaubt: {sorted(KINDS)}")
    if kind == "fundingRate" and market == "spot":
        raise IngestError("fundingRate existiert nur fuer Futures-Maerkte")
    if kind == "klines" and interval not in INTERVAL_SECONDS:
        raise IngestError(f"unbekanntes Intervall {interval!r}")

    segment = KINDS[kind][0]
    prefix = f"{BASE_URL}/{MARKETS[market]}/monthly/{segment}/{symbol}"
    if kind == "klines":
        prefix = f"{prefix}/{interval}"
    return [f"{prefix}/{archive_name(kind, symbol, month, interval)}" for month in months]


def parse_checksum(text: str) -> str:
    """Liest den SHA-256 aus einer .CHECKSUM-Datei von Binance."""
    parts = text.split()
    if not parts:
        raise IngestError("leere Pruefsummendatei")
    digest = parts[0].strip().lower()
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise IngestError(f"kein gueltiger SHA-256 in Pruefsummendatei: {digest!r}")
    return digest


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _epoch_to_utc(raw: str) -> datetime:
    """Binance liefert Millisekunden, seit 2025 fuer SPOT teils Mikrosekunden."""
    value = int(raw)
    divisor = 1_000_000 if value > 10**14 else 1_000
    return datetime.fromtimestamp(value / divisor, tz=timezone.utc)


def iter_kline_rows(paths: Iterable[Path]) -> Iterator[list[str]]:
    """Liest Kline-Zeilen aus ZIPs oder CSVs. Binance-Archive haben keinen Header."""
    for path in sorted(paths):
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as archive:
                for name in sorted(archive.namelist()):
                    with archive.open(name) as handle:
                        text = (line.decode("utf-8") for line in handle)
                        for row in csv.reader(text):
                            if row and not row[0].lower().startswith("open_time"):
                                yield row
        else:
            with path.open(encoding="utf-8") as handle:
                for row in csv.reader(handle):
                    if row and not row[0].lower().startswith("open_time"):
                        yield row


@dataclass
class Coverage:
    first_observation: str
    last_observation: str
    row_count: int
    gaps: list[dict[str, Any]]
    missing_units: int
    zero_volume_rows: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "first_observation": self.first_observation,
            "last_observation": self.last_observation,
            "row_count": self.row_count,
            "timezone": "UTC",
            "continuity_checked": True,
            "gap_count": len(self.gaps),
            "missing_units": self.missing_units,
            "gaps": self.gaps,
            "zero_volume_rows": self.zero_volume_rows,
        }


def analyse_klines(paths: Iterable[Path], interval: str) -> Coverage:
    """Ermittelt Abdeckung, Luecken und Nullvolumen-Zeilen. Kein Netzwerkzugriff."""
    step = INTERVAL_SECONDS.get(interval)
    if step is None:
        raise IngestError(f"unbekanntes Intervall {interval!r}")

    stamps: list[datetime] = []
    zero_volume = 0
    for row in iter_kline_rows(paths):
        stamps.append(_epoch_to_utc(row[0]))
        if len(row) > 5 and float(row[5]) == 0.0:
            zero_volume += 1
    if not stamps:
        raise IngestError("keine Zeilen gefunden; Abdeckung nicht bestimmbar")

    stamps.sort()
    gaps: list[dict[str, Any]] = []
    missing = 0
    delta = timedelta(seconds=step)
    for previous, current in zip(stamps, stamps[1:]):
        span = current - previous
        if span > delta:
            units = int(span / delta) - 1
            missing += units
            gaps.append({
                "from": _iso(previous),
                "to": _iso(current),
                "missing_units": units,
            })
    return Coverage(
        first_observation=_iso(stamps[0]),
        last_observation=_iso(stamps[-1]),
        row_count=len(stamps),
        gaps=gaps,
        missing_units=missing,
        zero_volume_rows=zero_volume,
    )


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_snapshot(
    *,
    snapshot_id: str,
    market: str,
    kind: str,
    symbol: str,
    interval: str | None,
    files: Sequence[Path],
    coverage: Coverage,
    retrieved_at: str,
    created_at: str,
    root: Path,
    checksums_verified: bool,
    known_limitations: Sequence[str] = (),
) -> dict[str, Any]:
    """Setzt einen vertragskonformen Snapshot zusammen. Kein Netzwerkzugriff."""
    segment, data_kind = KINDS[kind]
    prefix = f"{BASE_URL}/{MARKETS[market]}/monthly/{segment}/{symbol}"
    if kind == "klines":
        prefix = f"{prefix}/{interval}"

    limitations = list(known_limitations)
    if data_kind == "OHLCV":
        limitations.append(
            "Aggregierte Bars erlauben kein echtes Volume-at-Price; Profilgroessen "
            "bleiben Naeherungen, solange kein AGG_TRADES-Snapshot referenziert wird."
        )

    venue = {"spot": "BINANCE_SPOT", "um": "BINANCE_USDM", "cm": "BINANCE_COINM"}[market]
    snapshot: dict[str, Any] = {
        "schema_version": "1.0.0",
        "snapshot_id": snapshot_id,
        "created_at": created_at,
        "data_kind": data_kind,
        "source": {
            "provider": "BINANCE_PUBLIC_DATA",
            "access_method": "BULK_ARCHIVE",
            "base_location": f"{prefix}/",
            "retrieved_at": retrieved_at,
            "terms_ref": (
                "Binance Public Data, oeffentlich und ohne API-Key abrufbar; "
                "Nutzungsbedingungen des Anbieters gelten."
            ),
            "provider_checksums_verified": checksums_verified,
        },
        "instrument": {
            "venue": venue,
            "symbol": symbol,
            "instrument_class": "SPOT" if market == "spot" else "PERPETUAL",
            "timeframe": interval if kind == "klines" else "tick",
        },
        "coverage": coverage.as_dict(),
        "files": [
            {
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in sorted(files)
        ],
    }
    if kind == "fundingRate":
        snapshot["instrument"]["timeframe"] = "8h"
    if limitations:
        snapshot["known_limitations"] = limitations
    return snapshot


# --------------------------------------------------------------------------
# Netzwerkzugriff
# --------------------------------------------------------------------------


def fetch(url: str, target: Path, verify: bool = True) -> Path:
    """Laedt eine Datei und prueft die begleitende .CHECKSUM-Datei."""
    from urllib.request import urlopen  # lokal importiert: Offline-Tests bleiben frei davon

    target.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url) as response, target.open("wb") as handle:
        while chunk := response.read(1 << 20):
            handle.write(chunk)
    if verify:
        with urlopen(f"{url}.CHECKSUM") as response:
            expected = parse_checksum(response.read().decode("utf-8"))
        actual = sha256_file(target)
        if actual != expected:
            target.unlink(missing_ok=True)
            raise IngestError(f"Pruefsumme weicht ab fuer {url}: {actual} != {expected}")
    return target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--market", default="um", choices=sorted(MARKETS))
    parser.add_argument("--kind", default="klines", choices=sorted(KINDS))
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--interval", help="nur fuer klines, z. B. 1m")
    parser.add_argument("--from-month", required=True, help="YYYY-MM")
    parser.add_argument("--to-month", required=True, help="YYYY-MM")
    parser.add_argument("--out", type=Path, required=True, help="Zielverzeichnis")
    parser.add_argument("--snapshot", type=Path, help="Pfad fuer das Snapshot-Manifest")
    parser.add_argument("--plan-only", action="store_true", help="nur URLs ausgeben")
    parser.add_argument("--no-verify", action="store_true", help="Pruefsummen ueberspringen")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    months = month_range(args.from_month, args.to_month)
    urls = build_urls(args.market, args.kind, args.symbol, months, args.interval)

    if args.plan_only:
        for url in urls:
            print(url)
        print(f"{len(urls)} Archive geplant; nichts geladen.")
        return 0

    downloaded = [fetch(url, args.out / url.rsplit("/", 1)[-1], verify=not args.no_verify)
                  for url in urls]
    now = _iso(datetime.now(tz=timezone.utc))

    if args.kind == "klines":
        coverage = analyse_klines(downloaded, args.interval)
    else:
        raise IngestError(
            "Abdeckungsanalyse ist derzeit nur fuer klines implementiert; "
            "fuer andere Datenarten Snapshot manuell vervollstaendigen"
        )

    snapshot = build_snapshot(
        snapshot_id=f"snapshot:binance-{args.market}-{args.symbol.lower()}-"
                    f"{args.interval or args.kind}:{args.from_month}..{args.to_month}",
        market=args.market,
        kind=args.kind,
        symbol=args.symbol,
        interval=args.interval,
        files=downloaded,
        coverage=coverage,
        retrieved_at=now,
        created_at=now,
        root=args.out,
        checksums_verified=not args.no_verify,
    )
    destination = args.snapshot or (args.out / "data_snapshot.json")
    destination.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Snapshot geschrieben: {destination}")
    print(f"  Zeilen {coverage.row_count}, Luecken {len(coverage.gaps)}, "
          f"fehlende Einheiten {coverage.missing_units}")
    print("Der Snapshot belegt Herkunft und Integritaet, nicht die Eignung fuer eine Hypothese.")
    return 0


if __name__ == "__main__":
    sys.exit(run())
