"""Frozen protocol comparison. File integrity is not producer authentication."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from check_research_fingerprint import verify_fingerprint

ROOT = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def read_reference(ref, base):
    path = (base / ref['path']).resolve()
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != ref['sha256']:
        raise ValueError(f"Evidence hash mismatch: {path}")
    return json.loads(data), path.parent


def schema_check(value, name):
    schema = json.loads((ROOT / 'schemas' / name).read_text(encoding='utf-8'))
    return [f"{e.json_path}: {e.message}" for e in
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value)]


def timestamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timezone is required')
    return result


def protocol_errors(protocol):
    errors = []
    rule = protocol['stopping_rule']
    count_based = 'target_count' in rule
    start = timestamp(rule['start_at'])
    end = rule.get('target_count') if count_based else timestamp(rule['end_at'])
    if not count_based and end <= start:
        errors.append('Calendar end must follow start.')
    policy = protocol['peeking_policy']
    schedule = protocol['inspection_schedule']
    if policy == 'NO_INTERIM_STOPPING' and schedule:
        errors.append('NO_INTERIM_STOPPING permits no interim inspection.')
    if policy != 'NO_INTERIM_STOPPING' and not schedule:
        errors.append('Nontrivial peeking policy requires a complete inspection schedule.')
    if protocol['early_termination_allowed'] != (policy == 'PREDECLARED_ALPHA_SPENDING'):
        errors.append('Only PREDECLARED_ALPHA_SPENDING permits early_termination_allowed.')
    previous = 0 if count_based else start
    spending = 0
    for item in schedule:
        key = 'at_count' if count_based else 'at_time'
        if key not in item:
            errors.append('Inspection coordinates must match the stopping horizon.')
            continue
        point = item[key] if count_based else timestamp(item[key])
        if not previous < point < end:
            errors.append('Inspection schedule must be strictly ordered inside the horizon.')
        previous = point
        if policy == 'PREDECLARED_ALPHA_SPENDING':
            if not {'alpha_increment', 'p_value_threshold'} <= item.keys():
                errors.append('Alpha spending requires each increment and decision threshold.')
            else:
                spending += item['alpha_increment']
                if item['p_value_threshold'] > item['alpha_increment']:
                    errors.append('Decision threshold exceeds its alpha allocation.')
        elif 'alpha_increment' in item or 'p_value_threshold' in item:
            errors.append('Non-terminating audits cannot contain stopping thresholds.')
    if policy == 'PREDECLARED_ALPHA_SPENDING':
        if 'alpha_budget' not in protocol or spending > protocol['alpha_budget'] + 1e-12:
            errors.append('Alpha spending exceeds or lacks the frozen total budget.')
    elif 'alpha_budget' in protocol:
        errors.append('Alpha budget is only valid for alpha spending.')
    return errors


def outcome_commitment(contract):
    return {
        'contract_id': contract['contract_id'],
        'validation_protocol': contract['validation_protocol'],
        'outcomes': [{k:v for k,v in item.items() if k != 'assessment'} for item in contract['outcomes']],
        'transportability_by_target': [{k:v for k,v in item.items()
            if k not in {'status', 'evidence_refs', 'plain_language_scope'}}
            for item in contract['transportability_by_target']],
    }


def fingerprint_errors(contract, base):
    fingerprint, _ = read_reference(contract['research_fingerprint_file'], base)
    errors = schema_check(fingerprint, 'research_fingerprint.schema.json')
    verify_fingerprint(fingerprint, 'contract')
    if (fingerprint['research_id'], fingerprint['research_version']) != (
            contract['research_id'], contract['research_version']):
        errors.append('Contract research identity differs from the complete fingerprint.')
    expected = (contract['contract_id'] + ':validation-protocol', digest(contract['validation_protocol']))
    if expected not in {(a['artifact_ref'], a['content_sha256']) for a in fingerprint['protected_artifacts']}:
        errors.append('Complete fingerprint does not protect the exact validation protocol.')
    design = (contract['contract_id'] + ':outcome-design', digest(outcome_commitment(contract)))
    if design not in {(a['artifact_ref'], a['content_sha256']) for a in fingerprint['protected_artifacts']}:
        errors.append('Complete fingerprint does not protect the frozen outcome design.')
    return errors


def execution_errors(contract, base):
    """All mismatches invalidate the test, including explicitly explained deviations."""
    record, record_base = read_reference(contract['execution_record'], base)
    errors = schema_check(record, 'validation_execution.schema.json')
    if errors:
        return errors
    frozen, frozen_base = read_reference(record['frozen_contract'], record_base)
    from validate_outcome_evidence_contract import validate_contract
    if frozen.get('status') != 'FROZEN':
        return ['Execution requires the original FROZEN contract.']
    frozen_errors = validate_contract(frozen, base_dir=frozen_base)
    if frozen_errors:
        raise ValueError('Original frozen contract is invalid: ' + '; '.join(frozen_errors))
    for key in ('contract_id', 'research_id', 'research_version', 'validation_protocol', 'research_fingerprint_file'):
        if contract[key] != frozen[key]:
            errors.append(f'Executed contract differs from frozen {key}.')
    # Assessment text/results may change; the pre-test outcome commitments may not.
    for field, result_fields in [('outcomes', {'assessment'}),
                                 ('transportability_by_target', {'status', 'evidence_refs', 'plain_language_scope'})]:
        project = lambda items: [{k: v for k, v in x.items() if k not in result_fields} for x in items]
        if project(contract[field]) != project(frozen[field]):
            errors.append(f'Frozen {field} commitments changed.')
    protocol = frozen['validation_protocol']
    fingerprint, _ = read_reference(frozen['research_fingerprint_file'], frozen_base)
    if record['protocol_sha256'] != digest(protocol) or record['research_fingerprint_sha256'] != fingerprint['fingerprint_sha256']:
        errors.append('Execution fingerprint/protocol binding differs.')
    if timestamp(contract['updated_at']) < timestamp(record['actual_end']):
        errors.append('Assessment predates execution completion.')
    if timestamp(frozen['updated_at']) >= timestamp(record['actual_start']):
        errors.append('Contract was not frozen before execution started.')
    rule = protocol['stopping_rule']
    if timestamp(record['actual_start']) != timestamp(rule['start_at']):
        errors.append('Actual start differs: selective truncation or start mismatch.')
    if timestamp(record['actual_end']) < timestamp(record['actual_start']):
        errors.append('Actual end precedes start.')
    if record['deviations']:
        errors.append('Recorded deviations invalidate the test; explanation is not authorization.')
    # The observer log is separate from the agent-written summary and must reconcile exactly.
    log, _ = read_reference(record['event_log'], record_base)
    expected_log = {k: record[k] for k in ('actual_start', 'actual_end', 'actual_count',
                    'termination_reason', 'interim_inspections', 'deviations',
                    'protocol_sha256', 'research_fingerprint_sha256')}
    from validation_observer import observed_summary
    if observed_summary(log) != expected_log:
        errors.append('Execution summary disagrees with the observer event log.')
    count_based = 'target_count' in rule
    key = 'at_count' if count_based else 'at_time'
    point = lambda x: x[key] if count_based else timestamp(x[key])
    inspections = record['interim_inspections']
    schedule = protocol['inspection_schedule']
    actual_end = record['actual_count'] if count_based else timestamp(record['actual_end'])
    expected_end = rule['target_count'] if count_based else timestamp(rule['end_at'])
    expected_inspections = [x for x in schedule if point(x) <= actual_end]
    if [point(x) for x in inspections] != [point(x) for x in expected_inspections]:
        errors.append('Undeclared, missing, duplicate, or reordered interim inspection.')
    if any(timestamp(a['at_time']) > timestamp(b['at_time']) or a['at_count'] > b['at_count']
           for a, b in zip(inspections, inspections[1:])):
        errors.append('Inspection times and counts must be chronologically ordered.')
    for inspection in inspections:
        if not (0 <= inspection['at_count'] <= record['actual_count'] and
                timestamp(record['actual_start']) <= timestamp(inspection['at_time']) <= timestamp(record['actual_end'])):
            errors.append('Inspection falls outside the executed test.')
    crossings = []
    if protocol['peeking_policy'] == 'PREDECLARED_ALPHA_SPENDING':
        for actual, planned in zip(inspections, expected_inspections):
            if actual['p_value'] is None:
                errors.append('Alpha inspection requires its observed p-value.')
            elif actual['p_value'] <= planned['p_value_threshold']:
                crossings.append(point(actual))
    if record['termination_reason'] == 'ALPHA_BOUNDARY':
        if (not crossings or crossings[0] != actual_end or actual_end >= expected_end
                or not inspections or timestamp(record['actual_end']) != timestamp(inspections[-1]['at_time'])
                or record['actual_count'] != inspections[-1]['at_count']):
            errors.append('Early termination lacks a predeclared crossed alpha boundary.')
    elif record['termination_reason'] != 'HORIZON_REACHED' or actual_end != expected_end or crossings:
        errors.append('Premature/late termination or ignored stopping boundary.')
    return errors
