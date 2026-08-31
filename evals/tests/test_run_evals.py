from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from evals import run_evals


EVALS_DIR = Path(__file__).resolve().parents[1]


class EvalHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = run_evals.load_json(EVALS_DIR / "catalog.v1.json")
        cls.results = run_evals.load_json(EVALS_DIR / "examples" / "smoke-results.v1.json")
        cls.baseline = run_evals.load_json(EVALS_DIR / "baseline.v1.json")

    def test_catalog_covers_all_required_capabilities(self) -> None:
        run_evals.validate_catalog(self.catalog)
        capabilities = {case["capability"] for case in self.catalog["cases"]}
        self.assertEqual(capabilities, run_evals.CAPABILITIES)

    def test_reference_smoke_results_pass_all_gates(self) -> None:
        report = run_evals.score_results(self.catalog, self.results, self.baseline)
        self.assertTrue(report["passed"])
        self.assertEqual(report["metrics"]["overall_score"], 1.0)
        self.assertEqual(report["metrics"]["critical_assertion_pass_rate"], 1.0)
        self.assertEqual(report["metrics"]["hypothesis_intake_accuracy"], 1.0)
        self.assertEqual(report["metrics"]["scientific_philosophy_accuracy"], 1.0)
        self.assertEqual(report["metrics"]["research_orchestration_accuracy"], 1.0)
        self.assertEqual(report["metrics"]["causal_identification_accuracy"], 1.0)
        self.assertFalse(report["gate_failures"])
        self.assertFalse(report["regression_failures"])

    def test_dml_cannot_substitute_for_causal_identification(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "dml-identification-regression"
        assessment = regressed["cases"]["dml_is_not_identification"][
            "causal_identification"
        ]
        assessment["identification_status"] = "PASS"
        assessment["dml_role"] = "IDENTIFICATION"

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["causal_identification_accuracy"], 1.0)
        self.assertFalse(report["cases"]["dml_is_not_identification"]["passed"])
        self.assertTrue(report["regression_failures"])

    def test_misspecified_event_study_cannot_authorize_causal_language(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "event-study-causal-language-regression"
        regressed["cases"]["financial_event_study_requires_counterfactual"][
            "causal_identification"
        ]["causal_language_authorized"] = True

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["causal_identification_accuracy"], 1.0)
        self.assertFalse(
            report["cases"]["financial_event_study_requires_counterfactual"][
                "passed"
            ]
        )
        self.assertTrue(report["regression_failures"])

    def test_contemporaneous_ofi_cannot_be_promoted_to_forward_oos(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "ofi-forward-scope-regression"
        regressed["cases"]["ofi_contemporaneous_not_forward_edge"][
            "hypothesis_intake"
        ]["epistemic_stage_status"]["forward_predictive_oos"]["status"] = "SUPPORTED"

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["hypothesis_intake_accuracy"], 1.0)
        self.assertFalse(
            report["cases"]["ofi_contemporaneous_not_forward_edge"]["passed"]
        )
        self.assertTrue(report["regression_failures"])

    def test_missing_mandatory_philosophy_route_is_a_regression(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "orchestration-route-regression"
        regressed["cases"]["route_incomplete_prose_before_operationalization"][
            "routing"
        ]["route"] = "OPERATIONALIZE_SOURCE_STRATEGY"

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["research_orchestration_accuracy"], 1.0)
        self.assertFalse(
            report["cases"]["route_incomplete_prose_before_operationalization"][
                "passed"
            ]
        )
        self.assertTrue(report["regression_failures"])

    def test_handoff_drift_cannot_be_silently_accepted(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "handoff-drift-acceptance-regression"
        routing = regressed["cases"]["route_detected_handoff_drift_to_user"][
            "routing"
        ]
        routing["changed_output_accepted"] = True
        routing["original_identity_remains_effective"] = False

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["research_orchestration_accuracy"], 1.0)
        self.assertFalse(
            report["cases"]["route_detected_handoff_drift_to_user"]["passed"]
        )
        self.assertTrue(report["regression_failures"])

    def test_identified_effect_cannot_be_promoted_to_executable_net_edge(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "causal-effect-net-edge-regression"
        regressed["cases"]["identified_effect_not_automatic_net_edge"][
            "hypothesis_intake"
        ]["epistemic_stage_status"]["executable_net_edge"]["status"] = "SUPPORTED"

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["hypothesis_intake_accuracy"], 1.0)
        self.assertFalse(
            report["cases"]["identified_effect_not_automatic_net_edge"]["passed"]
        )
        self.assertTrue(report["regression_failures"])

    def test_recurring_prints_cannot_confirm_twap_vwap_or_price_floor(self) -> None:
        for field in ("twap_vwap_confirmed", "price_floor_established"):
            with self.subTest(field=field):
                regressed = copy.deepcopy(self.results)
                regressed["run_id"] = f"recurring-prints-{field}-regression"
                regressed["cases"]["recurring_prints_not_confirmed_execution_algo"][
                    "hypothesis_intake"
                ][field] = True

                report = run_evals.score_results(self.catalog, regressed, self.baseline)
                self.assertFalse(report["passed"])
                self.assertLess(report["metrics"]["hypothesis_intake_accuracy"], 1.0)
                self.assertFalse(
                    report["cases"]["recurring_prints_not_confirmed_execution_algo"][
                        "passed"
                    ]
                )
                self.assertTrue(report["regression_failures"])

        for claim_id in ("execution_algo_identity", "price_floor", "directional_net_edge"):
            with self.subTest(claim_id=claim_id):
                regressed = copy.deepcopy(self.results)
                regressed["run_id"] = f"recurring-prints-{claim_id}-claim-regression"
                regressed["cases"]["recurring_prints_not_confirmed_execution_algo"][
                    "claims"
                ][claim_id]["evidence_status"] = "SUPPORTED"

                report = run_evals.score_results(self.catalog, regressed, self.baseline)
                self.assertFalse(report["passed"])
                self.assertLess(report["metrics"]["hypothesis_intake_accuracy"], 1.0)
                self.assertFalse(
                    report["cases"]["recurring_prints_not_confirmed_execution_algo"][
                        "passed"
                    ]
                )
                self.assertTrue(report["regression_failures"])

    def test_not_using_news_as_signal_cannot_be_called_news_free(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "news-scope-laundering-regression"
        regressed["cases"]["not_used_as_signal_not_news_free"][
            "hypothesis_intake"
        ]["news_free_claim_allowed"] = True

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["hypothesis_intake_accuracy"], 1.0)
        self.assertFalse(
            report["cases"]["not_used_as_signal_not_news_free"]["passed"]
        )
        self.assertTrue(report["regression_failures"])

    def test_noise_screen_pass_cannot_be_promoted_to_evidence(self) -> None:
        for path in (
            ("claims", "effect_exists", "evidence_status"),
            (
                "hypothesis_intake",
                "epistemic_stage_status",
                "mechanism_supported",
                "status",
            ),
            (
                "hypothesis_intake",
                "epistemic_stage_status",
                "forward_predictive_oos",
                "status",
            ),
            (
                "hypothesis_intake",
                "epistemic_stage_status",
                "executable_net_edge",
                "status",
            ),
        ):
            with self.subTest(path=path):
                regressed = copy.deepcopy(self.results)
                regressed["run_id"] = "noise-screen-evidence-regression"
                target = regressed["cases"]["noise_screen_not_evidence"]
                for component in path[:-1]:
                    target = target[component]
                target[path[-1]] = "SUPPORTED"

                report = run_evals.score_results(self.catalog, regressed, self.baseline)
                self.assertFalse(report["passed"])
                self.assertFalse(report["cases"]["noise_screen_not_evidence"]["passed"])
                self.assertTrue(report["regression_failures"])

    def test_actor_constraint_cannot_be_promoted_to_mechanism_evidence(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "actor-constraint-mechanism-regression"
        regressed["cases"]["actor_constraint_not_mechanism"]["claims"][
            "proposed_actor_mechanism"
        ]["evidence_status"] = "SUPPORTED"
        regressed["cases"]["actor_constraint_not_mechanism"]["hypothesis_intake"][
            "epistemic_stage_status"
        ]["mechanism_supported"]["status"] = "SUPPORTED"

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertFalse(report["cases"]["actor_constraint_not_mechanism"]["passed"])
        self.assertTrue(report["regression_failures"])

    def test_failed_bundle_cannot_be_rescued_by_posthoc_scope_exclusion(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "philosophy-posthoc-rescue-regression"
        review = regressed["cases"]["failed_bundle_progressive_vs_degenerative"][
            "philosophy_review"
        ]
        review["revision_assessments"]["exclude_adverse_sessions"][
            "classification"
        ] = "PROGRESSIVE"
        review["original_result_relabelled"] = True

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertLess(report["metrics"]["scientific_philosophy_accuracy"], 1.0)
        self.assertFalse(
            report["cases"]["failed_bundle_progressive_vs_degenerative"]["passed"]
        )
        self.assertTrue(report["regression_failures"])

    def test_cli_smoke_run_returns_zero(self) -> None:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return_code = run_evals.main([])
        self.assertEqual(return_code, 0)

    def test_deterministic_score_drop_is_a_regression_and_nonzero(self) -> None:
        regressed = copy.deepcopy(self.results)
        regressed["run_id"] = "intentional-regression"
        regressed["cases"]["source_attribution_primary"]["claims"]["revenue"]["source_ids"] = [
            "market_blog_summary"
        ]

        report = run_evals.score_results(self.catalog, regressed, self.baseline)
        self.assertFalse(report["passed"])
        self.assertTrue(report["regression_failures"])
        self.assertLess(report["metrics"]["citation_accuracy"], 1.0)

        with tempfile.TemporaryDirectory() as temporary_directory:
            result_path = Path(temporary_directory) / "regressed.json"
            result_path.write_text(json.dumps(regressed), encoding="utf-8")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                return_code = run_evals.main(["--results", str(result_path)])
        self.assertEqual(return_code, 1)

    def test_unknown_claim_source_is_a_structural_error(self) -> None:
        malformed = copy.deepcopy(self.results)
        malformed["cases"]["source_attribution_primary"]["claims"]["revenue"]["source_ids"] = [
            "invented_source"
        ]
        with self.assertRaises(run_evals.FixtureError):
            run_evals.validate_results(malformed, self.catalog)

    def test_missing_path_exists_operator_is_deterministic(self) -> None:
        assertion = {
            "path": "claims.missing_claim",
            "operator": "exists",
            "expected": False,
        }
        passed, actual = run_evals.evaluate_assertion({"claims": {}}, assertion)
        self.assertTrue(passed)
        self.assertIsNone(actual)

    def test_structural_cli_error_returns_two(self) -> None:
        malformed = copy.deepcopy(self.results)
        malformed["schema_version"] = "wrong-version"
        with tempfile.TemporaryDirectory() as temporary_directory:
            result_path = Path(temporary_directory) / "malformed.json"
            result_path.write_text(json.dumps(malformed), encoding="utf-8")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                return_code = run_evals.main(["--results", str(result_path)])
        self.assertEqual(return_code, 2)


if __name__ == "__main__":
    unittest.main()
