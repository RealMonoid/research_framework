"""Small independent-replication reference world, never a market model."""
import json
import random
import sys

request = json.load(sys.stdin)
configuration = request['configuration']
replications = []
for seed in request['seeds']:
    rng = random.Random(seed)
    # Paired disturbances preserve within-pair dependence. Separate seeds
    # generate independent replications of this explicitly synthetic world.
    disturbances = [rng.uniform(-1, 1) for _ in range(16)]
    replications.append([configuration['effect'] + value
                         for value in disturbances for _ in range(2)])
json.dump(replications, sys.stdout, allow_nan=False)
