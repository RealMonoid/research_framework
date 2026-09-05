"""Complete toy pipeline: paired input, frozen centering, mean, decision.

No control identity, expected truth, or seed is supplied to this pipeline.
This fixture verifies the execution interface, not a trading backend.
"""
import json
import statistics
import sys

request = json.load(sys.stdin)
configuration = request['configuration']
if len(request['replications']) != 1:
    raise ValueError('Each complete pipeline invocation must isolate one replication.')
outputs = []
for observations in request['replications']:
    if len(observations) != 32:
        raise ValueError('Reference pipeline requires all 32 observations.')
    centered = [x - configuration['center'] for x in observations]
    outputs.append(statistics.mean(centered) > configuration['threshold'])
json.dump(outputs, sys.stdout, allow_nan=False)
