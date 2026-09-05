"""Resolve COMPLETE declarations on the ordinary router path, without running data."""
from pathlib import Path

from validation_execution import read_reference
from validate_outcome_evidence_contract import validate_contract
from validate_pipeline_integrity_assessment import validate_assessment


def check_completed_artifacts(state, base_dir: Path):
    context = state['research_context']
    effective = state['effective_research_fingerprint']
    result = context['frozen_result_status']
    if result != 'NONE' and state['artifacts']['outcome_evidence_contract']['status'] != 'COMPLETE':
        raise ValueError('A frozen result requires verified COMPLETE ASSESSED outcome evidence before any result route.')
    loaded = {}
    for name, validator, id_field in (
            ('outcome_evidence_contract', validate_contract, 'contract_id'),
            ('pipeline_integrity_assessment', validate_assessment, 'assessment_id')):
        record = state['artifacts'][name]
        if record['status'] != 'COMPLETE':
            continue
        try:
            artifact, base = read_reference(record['evidence_file'], base_dir)
            errors = validator(artifact, base_dir=base)
            if artifact[id_field] != record['artifact_ref']:
                errors.append('Artifact identity differs from checkpoint.')
            if artifact['research_id'] != context['research_id'] or str(artifact['research_version']) != str(context['research_version']):
                errors.append('Artifact belongs to another research case/version.')
            fingerprint, _ = read_reference(artifact['research_fingerprint_file'], base)
            if (fingerprint['fingerprint_sha256'] != effective['fingerprint_sha256'] or
                    fingerprint['fingerprint_id'] != effective['fingerprint_ref']):
                errors.append('Artifact differs from the effective complete research fingerprint.')
            if name == 'outcome_evidence_contract':
                if artifact['status'] not in {'FROZEN', 'ASSESSED'}:
                    errors.append('A draft outcome contract cannot be COMPLETE.')
                if context['frozen_result_status'] != 'NONE' and artifact['status'] != 'ASSESSED':
                    errors.append('A recorded result requires an assessed execution comparison.')
            elif artifact['status'] != 'ASSESSED' or artifact['overall_gate'] != 'PASS':
                errors.append('Only executed, assessed PASS controls can be COMPLETE.')
            if errors:
                raise ValueError('; '.join(errors))
            loaded[name] = artifact
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ValueError(f'{name}: unverified COMPLETE declaration: {exc}. '
                             'Record the prerequisite problem before continuing; do not reconstruct evidence after results.') from exc
    if result != 'NONE':
        outcomes = loaded['outcome_evidence_contract']['outcomes']
        primary = {o['assessment']['result'] for o in outcomes if o['role'] == 'PRIMARY'}
        compatible = {'VALIDATED': {'SUPPORTED'}, 'FALSIFIED': {'CONTRADICTED'},
                      'PRECISE_NULL': {'CONTRADICTED'}, 'INCONCLUSIVE': {'NON_DISCRIMINATING'},
                      'INVALID_TEST': {'INVALID_TEST'}}
        if primary != compatible.get(result):
            raise ValueError('Frozen result classification contradicts the assessed primary outcomes.')
    if len(loaded) == 2 and loaded['pipeline_integrity_assessment']['outcome_contract_ref'] != loaded['outcome_evidence_contract']['contract_id']:
        raise ValueError('Pipeline controls refer to a different outcome contract.')
