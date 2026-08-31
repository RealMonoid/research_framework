"""Offline-Tests fuer den Binance-Adapter.

Kein Test in dieser Datei greift auf das Netz zu. Geprueft werden Planung,
Pruefsummen-Parsing, Abdeckungsanalyse und vor allem, dass der erzeugte
Snapshot dem Vertrag ``schemas/data_snapshot.schema.json`` genuegt.
"""

from __future__ import annotations

import json
import sys
import unittest
from datetime import timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ingest"))

from jsonschema import Draft202012Validator  # noqa: E402

import binance_public_data as bpd  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "ETHUSDT-1m-sample.csv"
SCHEMA = json.loads(
    (ROOT / "schemas" / "data_snapshot.schema.json").read_text(encoding="utf-8")
)


class PlanningTests(unittest.TestCase):
    def test_month_range_is_inclusive(self) -> None:
        self.assertEqual(
            bpd.month_range("2024-11", "2025-02"),
            ["2024-11", "2024-12", "2025-01", "2025-02"],
        )

    def test_month_range_single_month(self) -> None:
        self.assertEqual(bpd.month_range("2024-01", "2024-01"), ["2024-01"])

    def test_reversed_range_is_rejected(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.month_range("2025-01", "2024-01")

    def test_malformed_month_is_rejected(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.month_range("2024/01", "2024-02")

    def test_kline_url_layout(self) -> None:
        urls = bpd.build_urls("um", "klines", "ETHUSDT", ["2024-01"], "1m")
        self.assertEqual(
            urls,
            [
                "https://data.binance.vision/data/futures/um/monthly/klines/"
                "ETHUSDT/1m/ETHUSDT-1m-2024-01.zip"
            ],
        )

    def test_aggtrades_url_has_no_interval_segment(self) -> None:
        url = bpd.build_urls("um", "aggTrades", "ETHUSDT", ["2024-01"])[0]
        self.assertTrue(url.endswith("aggTrades/ETHUSDT/ETHUSDT-aggTrades-2024-01.zip"))

    def test_funding_rate_is_futures_only(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.build_urls("spot", "fundingRate", "ETHUSDT", ["2024-01"])

    def test_klines_require_known_interval(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.build_urls("um", "klines", "ETHUSDT", ["2024-01"], "7m")

    def test_unknown_market_is_rejected(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.build_urls("kraken", "klines", "ETHUSDT", ["2024-01"], "1m")


class ChecksumTests(unittest.TestCase):
    def test_parses_digest_before_filename(self) -> None:
        digest = "b" * 64
        self.assertEqual(bpd.parse_checksum(f"{digest}  ETHUSDT-1m-2024-01.zip\n"), digest)

    def test_rejects_short_digest(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.parse_checksum("deadbeef  file.zip")

    def test_rejects_empty_file(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.parse_checksum("   ")


class EpochTests(unittest.TestCase):
    def test_milliseconds(self) -> None:
        moment = bpd._epoch_to_utc("1704067200000")
        self.assertEqual(moment.astimezone(timezone.utc).isoformat(), "2024-01-01T00:00:00+00:00")

    def test_microseconds_are_detected(self) -> None:
        moment = bpd._epoch_to_utc("1704067200000000")
        self.assertEqual(moment.astimezone(timezone.utc).isoformat(), "2024-01-01T00:00:00+00:00")


class CoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.coverage = bpd.analyse_klines([FIXTURE], "1m")

    def test_bounds_and_row_count(self) -> None:
        self.assertEqual(self.coverage.first_observation, "2024-01-01T00:00:00Z")
        self.assertEqual(self.coverage.last_observation, "2024-01-01T00:06:00Z")
        self.assertEqual(self.coverage.row_count, 5)

    def test_gap_is_detected_and_counted(self) -> None:
        self.assertEqual(len(self.coverage.gaps), 1)
        self.assertEqual(self.coverage.gaps[0]["missing_units"], 2)
        self.assertEqual(self.coverage.missing_units, 2)

    def test_zero_volume_rows_are_reported(self) -> None:
        self.assertEqual(self.coverage.zero_volume_rows, 1)

    def test_empty_input_is_an_error(self) -> None:
        with self.assertRaises(bpd.IngestError):
            bpd.analyse_klines([], "1m")


class SnapshotContractTests(unittest.TestCase):
    """Der Adapter muss den Vertrag erfuellen, nicht nur irgendein JSON liefern."""

    def _snapshot(self) -> dict:
        return bpd.build_snapshot(
            snapshot_id="snapshot:binance-um-ethusdt-1m:2024-01",
            market="um",
            kind="klines",
            symbol="ETHUSDT",
            interval="1m",
            files=[FIXTURE],
            coverage=bpd.analyse_klines([FIXTURE], "1m"),
            retrieved_at="2026-08-31T15:00:00Z",
            created_at="2026-08-31T15:00:00Z",
            root=FIXTURE.parent,
            checksums_verified=True,
        )

    def test_snapshot_validates_against_schema(self) -> None:
        errors = list(Draft202012Validator(SCHEMA).iter_errors(self._snapshot()))
        self.assertEqual([e.message for e in errors], [])

    def test_gap_count_matches_listed_gaps(self) -> None:
        coverage = self._snapshot()["coverage"]
        self.assertEqual(coverage["gap_count"], len(coverage["gaps"]))
        self.assertEqual(coverage["missing_units"], sum(g["missing_units"] for g in coverage["gaps"]))

    def test_files_carry_real_digests(self) -> None:
        entry = self._snapshot()["files"][0]
        self.assertEqual(entry["sha256"], bpd.sha256_file(FIXTURE))
        self.assertEqual(entry["bytes"], FIXTURE.stat().st_size)

    def test_ohlcv_snapshot_declares_profile_limitation(self) -> None:
        limitations = " ".join(self._snapshot()["known_limitations"])
        self.assertIn("Volume-at-Price", limitations)

    def test_venue_and_class_reflect_market(self) -> None:
        snapshot = self._snapshot()
        self.assertEqual(snapshot["instrument"]["venue"], "BINANCE_USDM")
        self.assertEqual(snapshot["instrument"]["instrument_class"], "PERPETUAL")


if __name__ == "__main__":
    unittest.main()
