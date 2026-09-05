"""Independent truth checks for the currently supported synthetic generator.

Adding another generator requires a reviewed truth/structure verifier. A family
name, custom executable, or self-reported known effect does not supply one.
"""
import hashlib
import math
import random
from pathlib import Path


def verify_reference_control(control, generated=None):
    reference = Path(__file__).with_name('synthetic_control_generator.py')
    if control['generator']['file']['sha256'] != hashlib.sha256(reference.read_bytes()).hexdigest():
        raise ValueError('Unsupported control generator: a reviewed truth verifier is required.')
    config = control['generator']['configuration']
    if set(config) != {'effect'} or type(config['effect']) not in (int, float) or not math.isfinite(config['effect']):
        raise ValueError('Reference generator requires one finite effect shift.')
    effect = config['effect']
    truth = control['expected_truth']
    if truth['effect_state'] == 'NO_EFFECT' and (effect != 0 or truth['direction'] != 'NONE'):
        raise ValueError('Null generator does not implement the declared no-effect truth.')
    if truth['effect_state'] == 'KNOWN_EFFECT' and not (
            truth['direction'] == 'POSITIVE' and effect > 0 or
            truth['direction'] == 'NEGATIVE' and effect < 0):
        raise ValueError('Sentinel generator does not implement the declared known-effect direction.')
    if control['required_for_gate'] and (set(control['model']['preserved_structure']) != {'AUTOCORRELATION'}
            or control['model']['family'] != 'CUSTOM'):
        raise ValueError('Paired-uniform generator verifies within-pair dependence only, not other structures/families.')
    if generated is not None:
        expected = []
        for seed in control['seeds']:
            rng = random.Random(seed)
            pairs = []
            for _ in range(16):
                value = effect + rng.uniform(-1, 1)
                pairs.extend((value, value))
            expected.append(pairs)
        if generated != expected:
            raise ValueError('Retained generator output differs from independently reconstructed seeded truth.')
