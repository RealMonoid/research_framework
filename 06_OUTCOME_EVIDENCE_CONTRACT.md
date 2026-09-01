# Outcome Evidence Contract

## What problem this solves

A research result can answer one question while leaving another unanswered. A
signal may predict a future return even when the proposed explanation for that
signal is wrong. A real market effect may also disappear after realistic costs.

Without a prior agreement about what each measurement is supposed to test, an
analyst or agent can keep the favorable result and quietly ignore the failed
parts. That turns an economic explanation into a story that can survive any
outcome.

The outcome evidence contract prevents this. Before a validation test starts,
it records:

- the main outcome;
- any required mechanism checks;
- robustness and exploratory measurements;
- what would support, contradict, fail to distinguish, or invalidate each
  test;
- which conclusion each result is allowed to change;
- whether trigger and outcome reuse the same inputs or reference model; and
- where stability is expected and how much change is acceptable.

It does not prove causality and it does not authorize a backtest. It makes the
meaning of a later result harder to rewrite after the result is known.

## Practical interpretation

The contract keeps four conclusions separate:

1. A phenomenon exists in the tested design.
2. A frozen signal predicts a future outcome on unseen data.
3. The claimed mechanism is supported against relevant alternatives.
4. The result remains usable after execution constraints and costs.

Success in one conclusion does not automatically support another. In
particular:

> If the primary prediction succeeds but a required mechanism diagnostic is
> contradicted, the predictive conclusion may remain supported while the
> mechanism conclusion must be marked not supported.

A non-discriminating mechanism test is different from a broken test. The first
was valid but could not separate the competing explanations. The second cannot
support a conclusion because a required measurement or design assumption
failed.

Stability is recorded for each conclusion separately. There is no universal
"stable strategy" label that can hide an unstable mechanism, an unstable
prediction, or an execution result tested in only one environment.

## Required outcome roles

| Role | Purpose | May change a conclusion? |
|---|---|---|
| `PRIMARY` | Tests the main frozen claim | Yes, according to its frozen target and decision rule |
| `MECHANISM_DIAGNOSTIC` | Distinguishes the proposed explanation from named alternatives | Only the mechanism conclusion |
| `ROBUSTNESS` | Tests whether a conclusion survives a specified variation | Only its named target |
| `EXPLORATORY` | Records observations that may generate later research | No |

Every non-exploratory outcome belongs to a named multiplicity family. This
prevents a collection of secondary measurements from being searched and then
reported as though only the successful one had been planned.

## Mechanical coupling

The contract records whether an outcome is independent of, shares inputs with,
or shares a reference model with another research element. For example, if a
trigger and a reversion target both use the same rolling range, changing the
range can change both event selection and apparent success. That dependence
must be visible before the test is frozen.

Mechanical coupling does not itself prove that a relationship is meaningless.
It shows that part of the observed relationship may be produced by the chosen
construction and therefore needs an independent outcome or a specific
sensitivity design.

## Lifecycle

- `DRAFT`: roles and rules are still being prepared; empirical validation must
  not start.
- `FROZEN`: all material roles, decision rules, coupling assessments,
  multiplicity families, and stability expectations are fixed; no outcome has
  been assessed.
- `ASSESSED`: every planned outcome has one recorded result and the separate
  stage conclusions obey the frozen decision rules.

The conductor must create and validate this contract during the research-case
stage. If a test is already marked frozen without a complete contract, routing
fails closed. The contract must not be reconstructed after viewing validation
results.

## Machine-enforced files

- Schema: `schemas/outcome_evidence_contract.schema.json`
- Semantic validator: `scripts/validate_outcome_evidence_contract.py`
- Regression tests: `scripts/test_outcome_evidence_contract.py`
- Worked contradiction example:
  `examples/outcome_evidence_contract.predictor_without_mechanism.json`

The contract is a material research artifact. Its effective version and hash
belong in the complete research fingerprint.
