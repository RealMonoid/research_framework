# Pipeline Integrity Controls

## What problem this solves

A research pipeline can produce a convincing result even when no market effect
exists. A timing mistake, hidden look-ahead, shifted index, reused window, sign
error, or adaptive selection step may manufacture an apparent signal.

The framework therefore tests the complete unchanged pipeline before real
validation. It asks two simple questions:

1. Does the pipeline invent too many effects in worlds where no effect was
   constructed?
2. Can it recover a deliberately inserted effect with the correct sign and
   timing?

A pass answers only those technical questions. It does not show that a real
market effect exists, predicts future returns, has the proposed cause, or can
be traded profitably.

## Required controls

Before a validation test may be frozen, the assessment needs at least:

- a repeated negative control with no constructed effect; and
- a repeated positive sentinel containing a known effect with a fixed sign and
  timing.

The same feature construction, filtering, event selection, timing, model
selection, and evaluation steps used by the intended research must run in each
control. Testing only an isolated formula is insufficient.

If causal tooling is required, a separate known causal sentinel is mandatory.
It checks whether the tooling recovers the permitted adjustment set and effect
direction in a world whose causal structure is known. It does not establish
identification in the real market study.

## Why one random walk is not enough

An artificial market is useful only for the question it is capable of
answering. A simple random walk usually omits volatility clustering, session
patterns, dependence between observations, gaps, liquidity, spreads, and
regime persistence. If the research pipeline uses any of those properties, an
unstructured random walk can be an unrealistically easy control.

The assessment therefore records:

- the model and its exact specification;
- where its parameters came from;
- the code or method version;
- the random-seed policy;
- which relevant structures were preserved;
- which relevant structures were not preserved; and
- whether the resulting reference world is adequate for the stated purpose.

A required control cannot pass while a relevant structural omission remains.
A random walk may be one diagnostic, but it cannot be the only required
negative control.

## Stress and construction challenges

Optional synthetic models may probe a suspected construction dependency or a
specific stress such as persistent volatility changes. These controls are
one-sided challenges:

- a failure can expose fragility or make a proposed test invalid;
- a pass does not provide positive evidence for the market claim.

If a synthetic challenge is intended to change a material conclusion, that
role and consequence must also have been frozen in the outcome evidence
contract. Otherwise it remains a diagnostic or a proposal for a later research
version.

## Lifecycle and gate

- `PLANNED`: the pipeline fingerprint, controls, repeat counts, expected truth,
  relevant structure, and acceptance rules are locked before the first run.
- `ASSESSED`: every control has a result, uncertainty statement, and evidence
  reference.
- `PASS`: all required controls passed. This authorizes only the next freeze
  step.
- `FAIL`: at least one required control failed. Real validation cannot begin.
- `BLOCKED`: a required structurally adequate control could not be completed.
  Real validation cannot begin.

The orchestration checkpoint maps these results strictly: an assessed `PASS`
is recorded as artifact status `COMPLETE`, `FAIL` as `INVALID`, and `BLOCKED`
as `BLOCKED`. Schema validity alone never earns `COMPLETE` status.

The router fails closed if a test is already marked frozen without a complete
passing assessment. Controls must never be reconstructed after validation
results are visible.

## Dependency policy

This framework does not import Q-Fin or trust any other package merely because
it implements a named stochastic process. A simulation implementation needs
its own mathematical validation, version record, deterministic seed policy,
and purpose-specific adequacy assessment before it can serve as a control.

## Machine-enforced files

- Schema: `schemas/pipeline_integrity_assessment.schema.json`
- Semantic validator: `scripts/validate_pipeline_integrity_assessment.py`
- Regression tests: `scripts/test_pipeline_integrity_assessment.py`
- Worked example:
  `examples/pipeline_integrity_assessment.synthetic_controls.json`

The assessed artifact and the exact pipeline fingerprint it covers are
material research state. Both belong in the complete research fingerprint.
