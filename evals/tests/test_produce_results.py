from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from evals import produce_results, run_evals


EVALS_DIR = Path(__file__).resolve().parents[1]


class EvalProducerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = run_evals.load_json(EVALS_DIR / "catalog.v1.json")
        cls.reference = run_evals.load_json(EVALS_DIR / "examples" / "smoke-results.v1.json")
        cls.baseline = run_evals.load_json(EVALS_DIR / "baseline.v1.json")

    def test_blind_request_never_contains_expected_assertions(self) -> None:
        request = produce_results.build_case_request(self.catalog, self.catalog["cases"][0])
        self.assertNotIn("expected", request)
        self.assertNotIn("expected", request["case"])
        self.assertNotIn("expected", request["case"]["input"])

    def test_command_producer_closes_protocol_loop(self) -> None:
        adapter = EVALS_DIR / "tests" / "reference_adapter.py"
        reference = EVALS_DIR / "examples" / "smoke-results.v1.json"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "produced-results.json"
            command = json.dumps([sys.executable, str(adapter), str(reference)])
            return_code = produce_results.main([
                "--output", str(output),
                "--run-id", "producer-protocol-smoke",
                "--run-kind", "PROTOCOL_SMOKE",
                "--adapter-id", "reference-adapter-test",
                "--command-json", command,
            ])
            self.assertEqual(return_code, 0)
            produced = run_evals.load_json(output)
            self.assertEqual(produced["producer"]["producer_type"], "COMMAND")
            self.assertEqual(set(produced["cases"]), {case["case_id"] for case in self.catalog["cases"]})
            report = run_evals.score_results(self.catalog, produced, self.baseline)
            self.assertTrue(report["passed"])

    def test_release_gate_rejects_protocol_smoke(self) -> None:
        report = run_evals.score_results(
            self.catalog,
            self.reference,
            self.baseline,
            required_run_kind="LIVE_AGENT",
        )
        self.assertFalse(report["passed"])
        self.assertTrue(any("required_run_kind=LIVE_AGENT" in item for item in report["gate_failures"]))

    def test_live_agent_cannot_claim_reference_fixture_producer(self) -> None:
        invalid = copy.deepcopy(self.reference)
        invalid["run_kind"] = "LIVE_AGENT"
        with self.assertRaises(run_evals.FixtureError):
            run_evals.validate_results(invalid, self.catalog)

    def test_results_reject_uncontracted_top_level_metadata(self) -> None:
        invalid = copy.deepcopy(self.reference)
        invalid["unreviewed_note"] = "not part of eval-results.v2"
        with self.assertRaises(run_evals.FixtureError):
            run_evals.validate_results(invalid, self.catalog)

    def test_results_require_timezone_aware_producer_timestamps(self) -> None:
        invalid = copy.deepcopy(self.reference)
        invalid["created_at"] = "2026-08-30T20:00:00"
        invalid["producer"]["completed_at"] = "2026-08-30T20:00:00"
        with self.assertRaises(run_evals.FixtureError):
            run_evals.validate_results(invalid, self.catalog)

    def test_command_json_requires_strings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "invalid.json"
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                return_code = produce_results.main([
                    "--output", str(output),
                    "--run-id", "invalid-command",
                    "--adapter-id", "invalid-command-test",
                    "--command-json", '["python", 3]',
                ])
            self.assertEqual(return_code, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
