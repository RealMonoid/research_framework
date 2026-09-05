"""Synthetic execution and adversarial evidence tests, including public CLIs."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pipeline_execution import run, runtime, control_commitment
from validation_execution import digest, outcome_commitment
from check_research_fingerprint import calculate_fingerprint_sha256
from validate_pipeline_integrity_assessment import validate_assessment
from validate_outcome_evidence_contract import validate_contract

ROOT = Path(__file__).resolve().parents[1]


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    return {'path': str(path.resolve()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def synthetic_observer_log(record):
    # Deliberately generated test data, never represented as a real adapter trace.
    events = [{'event':'START', 'at':record['actual_start']}]
    previous_count = 0
    for inspection in record['interim_inspections']:
        events += [{'event':'OBSERVATION','at':inspection['at_time']} for _ in range(inspection['at_count'] - previous_count)]
        events.append({'event':'INSPECTION','at':inspection['at_time'],'p_value':inspection['p_value']})
        previous_count = inspection['at_count']
    events += [{'event':'OBSERVATION','at':record['actual_end']} for _ in range(record['actual_count'] - previous_count)]
    events += [{'event':'DEVIATION','at':record['actual_end'],'description':text} for text in record['deviations']]
    events.append({'event':'END','at':record['actual_end'],'reason':record['termination_reason']})
    return {'protocol_sha256':record['protocol_sha256'],
            'research_fingerprint_sha256':record['research_fingerprint_sha256'], 'events':events}


def prepare_outcome(directory):
    source = ROOT / 'examples'
    contract = json.loads((source / 'outcome_evidence_contract.predictor_without_mechanism.json').read_text())
    record = json.loads((source / contract['execution_record']['path']).read_text())
    frozen = json.loads((source / record['frozen_contract']['path']).read_text())
    contract['research_fingerprint_file']['path'] = str((source / contract['research_fingerprint_file']['path']).resolve())
    frozen['research_fingerprint_file'] = contract['research_fingerprint_file']
    record['frozen_contract'] = save(directory / 'result-frozen.json', frozen)
    record['event_log']['path'] = str((source / record['event_log']['path']).resolve())
    contract['execution_record'] = save(directory / 'result-execution.json', record)
    return contract


def prepare_plan(directory):
    source = ROOT / 'examples'
    plan = json.loads((source / 'pipeline_integrity_assessment.synthetic_controls.json').read_text())
    manifest = json.loads((source / plan['pipeline_manifest']['path']).read_text())
    manifest['runtime'] = runtime()
    manifest['entrypoint']['path'] = str((source / manifest['entrypoint']['path']).resolve())
    for control in plan['controls']:
        control['generator']['file']['path'] = str((source / control['generator']['file']['path']).resolve())
    plan['pipeline_manifest'] = save(directory / 'manifest.json', manifest)
    fingerprint = json.loads((source / plan['research_fingerprint_file']['path']).read_text())
    for artifact in fingerprint['protected_artifacts']:
        if artifact['artifact_ref'] == plan['assessment_id'] + ':pipeline-manifest':
            artifact['content_sha256'] = digest(manifest)
        if artifact['artifact_ref'] == plan['assessment_id'] + ':control-plan':
            artifact['content_sha256'] = digest(control_commitment(plan))
    fingerprint['fingerprint_sha256'] = calculate_fingerprint_sha256(fingerprint)
    plan['pipeline_fingerprint_sha256'] = fingerprint['fingerprint_sha256']
    plan['research_fingerprint_file'] = save(directory / 'fingerprint.json', fingerprint)
    save(directory / 'plan.json', plan)
    return plan


class PipelineExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.directory = Path(cls.temp.name)
        cls.plan = prepare_plan(cls.directory)
        completed = subprocess.run([sys.executable, str(ROOT / 'scripts/pipeline_execution.py'),
            str(cls.directory / 'plan.json'), '--output', str(cls.directory / 'run')], capture_output=True, text=True)
        if completed.returncode:
            raise AssertionError(completed.stderr)
        cls.assessed = json.loads((cls.directory / 'run/assessment.json').read_text())

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_real_synthetic_execution_and_cli(self):
        self.assertEqual([], validate_assessment(self.assessed))
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate_pipeline_integrity_assessment.py'),
            str(self.directory / 'run/assessment.json')], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_router_cli_verifies_actual_artifacts_before_freeze_and_assessment(self):
        from test_research_orchestration import neutral_state
        from route_research_task import route_state
        state = neutral_state()
        frozen = json.loads((ROOT / 'examples/outcome_evidence_contract.synthetic_frozen.json').read_text())
        frozen['research_fingerprint_file'] = self.plan['research_fingerprint_file']
        state['request']['intent'] = 'START_OR_CONTINUE_RESEARCH'
        state['research_context'].update(research_id=frozen['research_id'], research_version=1, stage='FROZEN_TEST')
        state['effective_research_fingerprint'] = {
            'fingerprint_ref':self.plan['pipeline_fingerprint_ref'],
            'fingerprint_sha256':self.plan['pipeline_fingerprint_sha256']}
        state['artifacts']['outcome_evidence_contract'] = {'status':'COMPLETE',
            'artifact_ref':frozen['contract_id'], 'evidence_file':save(self.directory / 'route-frozen.json', frozen)}
        state['artifacts']['pipeline_integrity_assessment'] = {'status':'COMPLETE',
            'artifact_ref':self.assessed['assessment_id'],
            'evidence_file':save(self.directory / 'route-controls.json', self.assessed)}
        self.assertEqual('CONDUCT_RESEARCH', route_state(state)['route'])
        path = self.directory / 'state.json'
        save(path, state)
        command = [sys.executable, str(ROOT / 'scripts/route_research_task.py'), str(path)]
        self.assertEqual(0, subprocess.run(command, capture_output=True).returncode)
        for status in ('FROZEN', 'ASSESSED'):
            for both in (False, True):
                bad = copy.deepcopy(frozen)
                bad['status'] = status
                if both:
                    bad['forward_testing_protocol'] = bad['validation_protocol']
                else:
                    del bad['validation_protocol']
                state['artifacts']['outcome_evidence_contract']['evidence_file'] = save(self.directory / 'route-bad.json', bad)
                save(path, state)
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertNotEqual(0, result.returncode)
                self.assertNotIn('CONDUCT_RESEARCH', result.stdout)
        missing = copy.deepcopy(state)
        del missing['artifacts']['outcome_evidence_contract']['evidence_file']
        with self.assertRaises(ValueError):
            route_state(missing)

    def test_no_declaration_without_execution(self):
        value = copy.deepcopy(self.assessed)
        del value['execution_evidence']
        self.assertTrue(validate_assessment(value))

    def test_forged_counts_statistics_seeds_rules_and_pipeline(self):
        mutations = [lambda a: a['controls'][0].update(actual_runs=199),
            lambda a: a['controls'][0]['result']['uncertainty_record'].update(estimate=0.5),
            lambda a: a['controls'][0]['seeds'].__setitem__(0, 99999),
            lambda a: a['controls'][0]['seeds'].__setitem__(0, 1),
            lambda a: a['controls'][0]['acceptance_rule'].update(pass_rate_max=0.9),
            lambda a: a.update(pipeline_fingerprint_sha256='b' * 64),
            lambda a: a['controls'][0]['result'].update(status='FAIL'),
            lambda a: a['controls'][0]['acceptance_rule'].update(maximum_standard_error=0.001)]
        for mutate in mutations:
            value = copy.deepcopy(self.assessed)
            mutate(value)
            with self.subTest(mutate=mutate):
                self.assertTrue(validate_assessment(value))

    def test_repeated_random_walks(self):
        value = copy.deepcopy(self.plan)
        value['controls'][0]['model']['family'] = 'RANDOM_WALK'
        duplicate = copy.deepcopy(value['controls'][0])
        duplicate['control_id'] = 'control:another-random-walk'
        value['controls'].append(duplicate)
        self.assertTrue(any('RANDOM_WALK' in e for e in validate_assessment(value)))

    def test_missing_or_tampered_output_bytes(self):
        value = copy.deepcopy(self.assessed)
        evidence = json.loads(Path(value['execution_evidence']['path']).read_text())
        evidence['controls'][0]['outputs']['sha256'] = '0' * 64
        value['execution_evidence'] = save(self.directory / 'bad-evidence.json', evidence)
        self.assertTrue(validate_assessment(value))

    def test_review_sentinel_truth_and_acceptance_bypasses(self):
        for field in ('truth', 'acceptance'):
            plan = copy.deepcopy(self.plan)
            sentinel = plan['controls'][1]
            if field == 'truth':
                sentinel['generator']['configuration']['effect'] = 0
            else:
                sentinel['acceptance_rule'].update(pass_rate_min=0, pass_rate_max=0.1)
            fingerprint = json.loads(Path(plan['research_fingerprint_file']['path']).read_text())
            for artifact in fingerprint['protected_artifacts']:
                if artifact['artifact_ref'].endswith(':control-plan'):
                    artifact['content_sha256'] = digest(control_commitment(plan))
            fingerprint['fingerprint_sha256'] = calculate_fingerprint_sha256(fingerprint)
            plan['pipeline_fingerprint_sha256'] = fingerprint['fingerprint_sha256']
            plan['research_fingerprint_file'] = save(self.directory / f'{field}-fingerprint.json', fingerprint)
            errors = validate_assessment(plan)
            self.assertTrue(any('known-effect' in e.lower() for e in errors), errors)

    def test_review_cross_version_binding(self):
        plan = copy.deepcopy(self.plan)
        plan['research_version'] = '2'
        self.assertTrue(any('identity' in e for e in validate_assessment(plan)))

    def test_review_isolated_invocations(self):
        evidence = json.loads(Path(self.assessed['execution_evidence']['path']).read_text())
        for record in evidence['controls']:
            inputs = json.loads(Path(record['inputs']['path']).read_text())
            self.assertEqual(200, len(record['isolated_invocations']))
            self.assertTrue(all(len(r['replications']) == 1 for r in inputs['requests']))
        # The pipeline itself rejects a batch; the successful runner therefore
        # demonstrates complete per-replication process calls rather than batching.
        source = ROOT / 'scripts/synthetic_reference_pipeline.py'
        bad = subprocess.run([sys.executable, str(source)], input=json.dumps({
            'replications':[[0] * 32] * 2, 'configuration':{'center':0,'threshold':0.8}}),
            text=True, capture_output=True)
        self.assertNotEqual(0, bad.returncode)

    def test_review_result_routes_require_consistent_assessed_evidence(self):
        from test_research_orchestration import neutral_state
        from route_research_task import route_state
        state = neutral_state()
        state['request']['intent'] = 'INTERPRET_RESULT'
        for result in ('VALIDATED', 'FALSIFIED', 'INCONCLUSIVE', 'INVALID_TEST'):
            state['research_context']['frozen_result_status'] = result
            with self.assertRaises(ValueError):
                route_state(state)
        contract = prepare_outcome(self.directory)
        fingerprint = json.loads(Path(contract['research_fingerprint_file']['path']).read_text())
        state['research_context'].update(research_id=contract['research_id'], research_version=1,
                                         stage='POST_RESULT', frozen_result_status='VALIDATED')
        state['effective_research_fingerprint'] = {'fingerprint_ref':fingerprint['fingerprint_id'],
                                                  'fingerprint_sha256':fingerprint['fingerprint_sha256']}
        state['artifacts']['outcome_evidence_contract'] = {'status':'COMPLETE',
            'artifact_ref':contract['contract_id'], 'evidence_file':save(self.directory / 'route-result.json', contract)}
        self.assertEqual('CONDUCT_RESEARCH', route_state(state)['route'])
        state['research_context']['frozen_result_status'] = 'FALSIFIED'
        with self.assertRaisesRegex(ValueError, 'classification contradicts'):
            route_state(state)

    def test_no_overwrite_of_prior_attempt(self):
        with self.assertRaises(FileExistsError):
            run(self.directory / 'plan.json', self.directory / 'run')


class ValidationExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        source = ROOT / 'examples'
        self.contract = json.loads((source / 'outcome_evidence_contract.predictor_without_mechanism.json').read_text())
        self.record = json.loads((source / self.contract['execution_record']['path']).read_text())
        self.frozen = json.loads((source / self.record['frozen_contract']['path']).read_text())
        self.fingerprint = json.loads((source / self.frozen['research_fingerprint_file']['path']).read_text())

    def bind(self):
        self.frozen['validation_protocol'] = copy.deepcopy(self.contract['validation_protocol'])
        for artifact in self.fingerprint['protected_artifacts']:
            if artifact['artifact_ref'].endswith(':outcome-design'):
                artifact['content_sha256'] = digest(outcome_commitment(self.contract))
            if artifact['artifact_ref'].endswith(':validation-protocol'):
                artifact['content_sha256'] = digest(self.contract['validation_protocol'])
        self.fingerprint['fingerprint_sha256'] = calculate_fingerprint_sha256(self.fingerprint)
        ref = save(self.directory / 'fingerprint.json', self.fingerprint)
        self.frozen['research_fingerprint_file'] = ref
        self.contract['research_fingerprint_file'] = ref
        self.record['frozen_contract'] = save(self.directory / 'frozen.json', self.frozen)
        self.record['protocol_sha256'] = digest(self.contract['validation_protocol'])
        self.record['research_fingerprint_sha256'] = self.fingerprint['fingerprint_sha256']
        return self.refresh_record()

    def refresh_record(self):
        log = synthetic_observer_log(self.record)
        self.record['event_log'] = save(self.directory / 'log.json', log)
        self.contract['execution_record'] = save(self.directory / 'record.json', self.record)
        return validate_contract(self.contract)

    def test_review_fingerprint_cannot_contain_alternative_commitments(self):
        self.assertEqual([], self.bind())
        duplicate = copy.deepcopy(self.fingerprint['protected_artifacts'][0])
        duplicate['content_sha256'] = 'f' * 64
        self.fingerprint['protected_artifacts'].append(duplicate)
        self.assertTrue(any('unique' in e for e in self.bind()))

    def test_review_same_timestamp_consumption_after_alpha_stop(self):
        p = self.contract['validation_protocol']
        p.update(stopping_rule={'horizon_type':'FIXED_CALENDAR_WINDOW', 'start_at':'2026-09-02T00:00:00Z',
                               'end_at':'2026-09-03T00:00:00Z'},
                 peeking_policy='PREDECLARED_ALPHA_SPENDING', early_termination_allowed=True,
                 alpha_budget=0.05, inspection_schedule=[{'at_time':'2026-09-02T01:00:00Z',
                                                          'alpha_increment':0.02,'p_value_threshold':0.02}])
        self.record.update(actual_count=1, actual_end='2026-09-02T01:00:00Z', termination_reason='ALPHA_BOUNDARY',
            interim_inspections=[{'at_count':1,'at_time':'2026-09-02T01:00:00Z','p_value':0.01}])
        self.assertEqual([], self.bind())
        self.record['actual_count'] = 2
        self.assertTrue(any('Early termination' in e for e in self.refresh_record()))

    def test_reference_valid(self):
        self.assertEqual([], self.bind())

    def test_early_late_abort_peek_and_clipping(self):
        self.assertEqual([], self.bind())
        original = copy.deepcopy(self.record)
        mutations = [dict(actual_count=499), dict(actual_count=501),
            dict(actual_start='2026-09-02T01:00:00Z'), dict(termination_reason='SAFETY_ABORT'),
            dict(deviations=['Explained but unauthorized exclusion']),
            dict(interim_inspections=[{'at_count':100,'at_time':'2026-09-02T01:00:00Z','p_value':None}])]
        for change in mutations:
            self.record = copy.deepcopy(original)
            self.record.update(change)
            with self.subTest(change=change):
                self.assertTrue(any('INVALID_TEST' in e for e in self.refresh_record()))

    def test_invalid_execution_can_be_recorded_without_repair_or_support(self):
        from validation_execution import execution_errors
        self.assertEqual([], self.bind())
        self.record['actual_count'] = 499
        self.assertTrue(self.refresh_record())
        violations = execution_errors(self.contract, ROOT)
        self.contract['execution_validation'] = {'status':'INVALID_TEST','violations':violations}
        for outcome in self.contract['outcomes']:
            outcome['assessment']['result'] = 'INVALID_TEST'
        for stage in self.contract['stage_conclusions'].values():
            if stage['status'] != 'UNKNOWN':
                stage['status'] = 'BLOCKED'
        self.assertEqual([], validate_contract(self.contract))
        self.contract['stage_conclusions']['forward_predictive_oos']['status'] = 'SUPPORTED'
        self.assertTrue(validate_contract(self.contract))

    def test_calendar_window_and_historical_clipping(self):
        for kind in ('FIXED_CALENDAR_WINDOW', 'HISTORICAL_STATIC_HOLDOUT'):
            self.contract['validation_protocol']['stopping_rule'] = {'horizon_type':kind,
                'start_at':'2026-09-02T00:00:00Z', 'end_at':'2026-09-03T00:00:00Z'}
            self.record['actual_end'] = '2026-09-03T00:00:00Z'
            self.assertEqual([], self.bind())
            for end in ('2026-09-02T23:00:00Z', '2026-09-03T01:00:00Z'):
                self.record['actual_end'] = end
                self.assertTrue(self.refresh_record())

    def test_complete_alpha_schedule(self):
        p = self.contract['validation_protocol']
        p.update(peeking_policy='PREDECLARED_ALPHA_SPENDING', early_termination_allowed=True,
                 alpha_budget=0.05, inspection_schedule=[{'at_count':100,'alpha_increment':0.02,'p_value_threshold':0.02}])
        self.record.update(actual_count=100, actual_end='2026-09-02T01:00:00Z', termination_reason='ALPHA_BOUNDARY',
            interim_inspections=[{'at_count':100,'at_time':'2026-09-02T01:00:00Z','p_value':0.01}])
        self.assertEqual([], self.bind())
        self.record['interim_inspections'][0]['p_value'] = 0.03
        self.assertTrue(self.refresh_record())

    def test_nonterminating_audit_and_incomplete_policies(self):
        p = self.contract['validation_protocol']
        p.update(peeking_policy='FIXED_AUDITS_WITHOUT_TERMINATION', inspection_schedule=[{'at_count':100}])
        self.record['interim_inspections'] = [{'at_count':100,'at_time':'2026-09-02T01:00:00Z','p_value':None}]
        self.assertEqual([], self.bind())
        p['inspection_schedule'] = []
        self.assertTrue(self.bind())


if __name__ == '__main__':
    unittest.main()
