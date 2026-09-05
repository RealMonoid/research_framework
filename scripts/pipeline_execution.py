"""Execute explicitly selected synthetic controls and verify their retained evidence.

The caller owns adapter approval and complete dependency disclosure. Receipts
are local evidence, not authenticated attestations against a hostile producer.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from validation_execution import read_reference, digest, schema_check, timestamp
from check_research_fingerprint import verify_fingerprint
from reference_control_evidence import verify_reference_control


def runtime():
    return {'python': platform.python_version(), 'implementation': platform.python_implementation()}


def write_file(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write('\n')
    return {'path': str(path.resolve()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def check_file(ref, base):
    path = (base / ref['path']).resolve()
    if hashlib.sha256(path.read_bytes()).hexdigest() != ref['sha256']:
        raise ValueError(f'Executable/dependency hash mismatch: {path}')
    return path


def control_commitment(assessment):
    controls = copy.deepcopy(assessment['controls'])
    for control in controls:
        control.pop('actual_runs', None)
        control.pop('result', None)
        control['generator']['file'].pop('path', None)
    return {'controls': controls, 'plan_locked_at': assessment['plan_locked_at'],
            'outcome_contract_ref': assessment['outcome_contract_ref'],
            'causal_tooling_required': assessment['causal_tooling_required']}


def verify_plan(assessment, base):
    manifest, manifest_base = read_reference(assessment['pipeline_manifest'], base)
    if set(manifest) != {'entrypoint', 'dependencies', 'configuration', 'runtime'}:
        raise ValueError('Pipeline manifest requires entrypoint, dependencies, configuration, runtime.')
    entry = check_file(manifest['entrypoint'], manifest_base)
    for dependency in manifest['dependencies']:
        check_file(dependency, manifest_base)
    fingerprint, _ = read_reference(assessment['research_fingerprint_file'], base)
    errors = schema_check(fingerprint, 'research_fingerprint.schema.json')
    verify_fingerprint(fingerprint, 'pipeline')
    if errors:
        raise ValueError('; '.join(errors))
    if fingerprint['fingerprint_sha256'] != assessment['pipeline_fingerprint_sha256']:
        raise ValueError('Complete pipeline fingerprint mismatch.')
    if (fingerprint['fingerprint_id'] != assessment['pipeline_fingerprint_ref']
            or fingerprint['research_id'] != assessment['research_id']
            or str(fingerprint['research_version']) != assessment['research_version']):
        raise ValueError('Pipeline fingerprint identity mismatch.')
    protected = {(x['artifact_ref'], x['content_sha256']) for x in fingerprint['protected_artifacts']}
    if (assessment['assessment_id'] + ':pipeline-manifest', digest(manifest)) not in protected:
        raise ValueError('Fingerprint does not protect the complete pipeline manifest.')
    if (assessment['assessment_id'] + ':control-plan', digest(control_commitment(assessment))) not in protected:
        raise ValueError('Fingerprint does not protect the locked control specifications and seeds.')
    for control in assessment['controls']:
        check_file(control['generator']['file'], base)
        verify_reference_control(control)
    return manifest, entry


def statistics(outputs):
    if not outputs or any(type(x) is not bool for x in outputs):
        raise ValueError('Pipeline must return one boolean detection per replication.')
    n = len(outputs)
    k = sum(outputs)
    p = k / n
    return {'method': 'BERNOULLI_STANDARD_ERROR', 'estimate': p,
            'standard_error': math.sqrt(p * (1 - p) / n),
            'completed_replications': n, 'successes': k}


def result_status(control, stats):
    rule = control['acceptance_rule']
    if control['required_for_gate'] and (control['model']['structure_adequacy'] != 'ADEQUATE_FOR_PURPOSE'
            or control['model']['unpreserved_relevant_structure']):
        return 'BLOCKED'
    return 'PASS' if (rule['pass_rate_min'] <= stats['estimate'] <= rule['pass_rate_max']
                      and stats['standard_error'] <= rule['maximum_standard_error']) else 'FAIL'


def planned_projection(value, base):
    value = copy.deepcopy(value)
    for ref in [value['pipeline_manifest'], value['research_fingerprint_file']] + [c['generator']['file'] for c in value['controls']]:
        ref['path'] = str((base / ref['path']).resolve())
    for key in ('status', 'updated_at', 'first_run_at', 'execution_evidence', 'overall_gate', 'plain_language_conclusion'):
        value.pop(key, None)
    for control in value['controls']:
        control.pop('actual_runs', None)
        control.pop('result', None)
    return value


def execution_errors(assessment, base):
    manifest, _ = verify_plan(assessment, base)
    evidence, evidence_base = read_reference(assessment['execution_evidence'], base)
    plan, plan_base = read_reference(evidence['locked_plan'], evidence_base)
    from validate_pipeline_integrity_assessment import validate_assessment
    if plan.get('status') != 'PLANNED':
        return ['Execution requires the original PLANNED control artifact.']
    errors = validate_assessment(plan, base_dir=plan_base)
    if planned_projection(plan, plan_base) != planned_projection(assessment, base):
        errors.append('Control plan changed after execution (seeds, rules, model, or pipeline).')
    if evidence['pipeline_manifest_sha256'] != digest(manifest):
        errors.append('Execution did not use the exact frozen pipeline manifest.')
    if evidence['runtime'] != manifest['runtime']:
        errors.append('Executed runtime differs from frozen manifest.')
    if evidence['pipeline_fingerprint_sha256'] != assessment['pipeline_fingerprint_sha256']:
        errors.append('Execution fingerprint differs.')
    if evidence['started_at'] != assessment['first_run_at'] or timestamp(plan['plan_locked_at']) >= timestamp(evidence['started_at']):
        errors.append('Control plan was not locked before the first execution.')
    if timestamp(evidence['ended_at']) < timestamp(evidence['started_at']):
        errors.append('Control execution chronology is invalid.')
    records = evidence['controls']
    if [r['control_id'] for r in records] != [c['control_id'] for c in assessment['controls']]:
        return errors + ['Missing, reordered, or duplicate control executions.']
    for control, record in zip(assessment['controls'], records):
        inputs, _ = read_reference(record['inputs'], evidence_base)
        outputs, _ = read_reference(record['outputs'], evidence_base)
        request, _ = read_reference(record['generator_request'], evidence_base)
        if request != {'seeds': control['seeds'], 'configuration': control['generator']['configuration']}:
            errors.append('Generator request does not match the frozen seeds/configuration.')
        if record['generator_sha256'] != control['generator']['file']['sha256']:
            errors.append('Generator implementation differs from the plan.')
        expected_requests = [{'replications': [item], 'configuration': manifest['configuration']}
                             for item in record['generated_inputs']]
        if inputs != {'requests': expected_requests}:
            errors.append('Pipeline inputs differ from retained generator output/configuration.')
        if len(record['generated_inputs']) != len(control['seeds']) or len(outputs) != len(control['seeds']):
            errors.append('Incomplete or extended replication execution.')
        if record['returncode'] != 0 or record['generator_returncode'] != 0:
            errors.append('A required execution failed.')
        verify_reference_control(control, record['generated_inputs'])
        invocations = record['isolated_invocations']
        expected_invocations = [{'replication_index': i, 'seed': seed, 'input_sha256': digest(request),
                                 'output': result, 'returncode': 0}
                                for i, (seed, request, result) in enumerate(zip(control['seeds'], expected_requests, outputs))]
        if invocations != expected_invocations:
            errors.append('Per-replication isolated-process receipts are missing or inconsistent.')
        stats = statistics(outputs)
        if stats != control['result']['uncertainty_record'] or len(outputs) != control['actual_runs']:
            errors.append('Numerical result disagrees with executed replications.')
        if control['result']['status'] != result_status(control, stats):
            errors.append('Self-declared result differs from the frozen numerical decision rule.')
    return errors


def call(entry, request):
    result = subprocess.run([sys.executable, str(entry)], input=json.dumps(request),
                            text=True, capture_output=True, timeout=60, check=False)
    if result.returncode:
        raise ValueError(f'Control subprocess failed ({result.returncode}): {result.stderr}')
    return json.loads(result.stdout)


def run(plan_path, output):
    from validate_pipeline_integrity_assessment import validate_assessment
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    base = plan_path.resolve().parent
    errors = validate_assessment(plan, base_dir=base)
    if errors or plan['status'] != 'PLANNED':
        raise ValueError('Invalid locked plan: ' + '; '.join(errors))
    if any(c['basis'] != 'SYNTHETIC_MODEL' for c in plan['controls']):
        raise ValueError('This runner permits explicitly scoped synthetic controls only.')
    manifest, entry = verify_plan(plan, base)
    if runtime() != manifest['runtime']:
        raise ValueError('Current runtime differs from the frozen runtime.')
    # Refuse reuse rather than overwriting a prior attempt.
    output.mkdir(parents=True, exist_ok=False)
    evidence = {'locked_plan': {'path': str(plan_path.resolve()), 'sha256': hashlib.sha256(plan_path.read_bytes()).hexdigest()},
                'pipeline_manifest_sha256': digest(manifest), 'runtime': runtime(),
                'pipeline_fingerprint_sha256': plan['pipeline_fingerprint_sha256'],
                'started_at': datetime.now(timezone.utc).isoformat(), 'controls': []}
    assessed = copy.deepcopy(plan)
    for i, control in enumerate(assessed['controls']):
        request = {'seeds': control['seeds'], 'configuration': control['generator']['configuration']}
        request_ref = write_file(output / f'{i}.generator-request.json', request)
        generated = call(check_file(control['generator']['file'], base), request)
        verify_reference_control(control, generated)
        requests = [{'replications': [item], 'configuration': manifest['configuration']} for item in generated]
        inputs_ref = write_file(output / f'{i}.inputs.json', {'requests': requests})
        outputs, invocations = [], []
        for index, (seed, request) in enumerate(zip(control['seeds'], requests)):
            returned = call(entry, request)
            if not isinstance(returned, list) or len(returned) != 1 or type(returned[0]) is not bool:
                raise ValueError('Each isolated replication must produce exactly one boolean detection.')
            outputs.append(returned[0])
            invocations.append({'replication_index': index, 'seed': seed, 'input_sha256': digest(request),
                                'output': returned[0], 'returncode': 0})
        outputs_ref = write_file(output / f'{i}.outputs.json', outputs)
        if len(generated) != len(control['seeds']) or len(outputs) != len(control['seeds']):
            raise ValueError('Runner did not receive the complete planned replication set.')
        stats = statistics(outputs)
        control['actual_runs'] = len(outputs)
        control['result'] = {'status': result_status(control, stats),
            'evidence_refs': [control['control_id'] + ':execution'], 'uncertainty_record': stats,
            'monte_carlo_uncertainty': 'Bernoulli standard error across independent seeded replications; no market inference.',
            'plain_language_interpretation': 'Computed from the retained pipeline outputs under the locked numerical rule.'}
        evidence['controls'].append({'control_id': control['control_id'], 'generator_request': request_ref,
            'generator_sha256': control['generator']['file']['sha256'], 'generated_inputs': generated,
            'inputs': inputs_ref, 'outputs': outputs_ref, 'isolated_invocations': invocations,
            'returncode': 0, 'generator_returncode': 0})
    # Detect changed source/dependency/plan bytes during the run.
    verify_plan(plan, base)
    read_reference(evidence['locked_plan'], base)
    evidence['ended_at'] = datetime.now(timezone.utc).isoformat()
    assessed.update(status='ASSESSED', first_run_at=evidence['started_at'], updated_at=evidence['ended_at'])
    statuses = [c['result']['status'] for c in assessed['controls'] if c['required_for_gate']]
    assessed['overall_gate'] = 'FAIL' if 'FAIL' in statuses else 'BLOCKED' if 'BLOCKED' in statuses else 'PASS'
    assessed['plain_language_conclusion'] = 'Executed synthetic controls only; local receipts do not authenticate a hostile producer.'
    assessed['execution_evidence'] = write_file(output / 'execution.json', evidence)
    # Resolve source-relative references before writing the result in another directory.
    for ref in [assessed['pipeline_manifest'], assessed['research_fingerprint_file']]:
        ref['path'] = str((base / ref['path']).resolve())
    for control in assessed['controls']:
        control['generator']['file']['path'] = str((base / control['generator']['file']['path']).resolve())
    # Projection compares resolved references; the copied plan keeps the same paths.
    return assessed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        assessed = run(args.plan, args.output)
        write_file(args.output / 'assessment.json', assessed)
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f'Pipeline execution failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
