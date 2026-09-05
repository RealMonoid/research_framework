"""Derive execution facts from an adapter's append-only observation event stream.

The adapter must observe all consumption and inspections. This parser cannot
discover an action omitted by an untrusted adapter or host.
"""
from datetime import datetime


def observed_summary(log):
    if set(log) != {'protocol_sha256', 'research_fingerprint_sha256', 'events'}:
        raise ValueError('Observer log requires bindings and a complete event stream.')
    events = log['events']
    if not isinstance(events, list) or len(events) < 2:
        raise ValueError('Observer log must contain START and END events.')
    if events[0].get('event') != 'START' or events[-1].get('event') != 'END':
        raise ValueError('Observer event stream must begin with START and finish with END.')
    count = 0
    inspections, deviations = [], []
    previous = None
    for index, event in enumerate(events):
        kind = event['event']
        expected = {'event', 'at'} | {'END': {'reason'}, 'INSPECTION': {'p_value'}, 'DEVIATION': {'description'}}.get(kind, set())
        if kind not in {'START', 'END', 'OBSERVATION', 'INSPECTION', 'DEVIATION'} or set(event) != expected:
            raise ValueError('Malformed or unknown observer event.')
        time = datetime.fromisoformat(event['at'].replace('Z', '+00:00'))
        if time.tzinfo is None or (previous is not None and time < previous):
            raise ValueError('Observer timestamps must be zoned and chronologically ordered.')
        previous = time
        if kind == 'START' and index != 0 or kind == 'END' and index != len(events) - 1:
            raise ValueError('Observer stream contains a second start/end or appended observations.')
        if kind == 'OBSERVATION':
            count += 1
        elif kind == 'INSPECTION':
            p = event['p_value']
            if p is not None and (type(p) not in (int, float) or not 0 <= p <= 1):
                raise ValueError('Inspection p-value must be null or a finite probability.')
            inspections.append({'at_count': count, 'at_time': event['at'], 'p_value': p})
        elif kind == 'DEVIATION':
            if not isinstance(event['description'], str) or not event['description']:
                raise ValueError('Deviation requires a description.')
            deviations.append(event['description'])
    return {'actual_start':events[0]['at'], 'actual_end':events[-1]['at'], 'actual_count':count,
            'termination_reason':events[-1]['reason'], 'interim_inspections':inspections,
            'deviations':deviations, 'protocol_sha256':log['protocol_sha256'],
            'research_fingerprint_sha256':log['research_fingerprint_sha256']}
