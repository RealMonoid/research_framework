# ADR-007: Entry noise screen and pre-fixed search space

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Research owner and research-framework maintainer

## Context

The generator makes it cheap to create many hypotheses. It does not make their
statistical testing cheap and does not remove multiplicity. A run with 96
data-screened candidates is a family of 96 tests, even if only a few later
appear in a research case.

The former §13 rule required documenting the search space, but had no entry
artifact that fixed family size and the threshold before the first result. A
single five-percent screen could therefore produce expected false survivors
from a large null family.

The origin of new catalogue entries was also not explicit. The mechanism
catalogue could not cleanly distinguish literature, market rules, and the
owner's observations or grow systematically from new observations.

## Decision

1. Each mechanism carries an `entry_origin` with origin type, stable
   references, a brief rationale, and collection time. The owner's observations
   use `INTERNAL_OBSERVATION` and a journal or observation reference.
2. A generator run is a candidate-universe reference. Before the first
   data-based entry screen, fix the planned test family in
   `schemas/search_space.schema.json`.
3. The register contains registered candidates, planned and completed screens,
   family alpha, correction method, and effective percentile.
4. `schemas/noise_screen.schema.json` stores the statistic, surrogate method,
   preserved structure, pre-set threshold, exceedance count, data role, and
   search-space reference.
5. An observation-driven candidate requires a screen before `PROMOTED`.
   Theory-driven, scheduled-event, and published-replication ideas may use a
   justified waiver.
6. `PROMOTED` requires an `actor_constraint` with actor, compulsion, expected
   action, observability, and a competing actor hypothesis. This is a
   plausibility requirement, not proof of a mechanism.
7. `scripts/validate_entry_thresholds.py` checks rules that JSON Schema cannot
   express: date order, ratios, counter bounds, cross-artifact references, and
   the recalculated correction threshold.
8. Bonferroni uses the pre-planned family size. An effective-tests approach
   requires an evidence reference. Benjamini–Hochberg may decide only after a
   complete batch with a documented rank. `NONE_JUSTIFIED` is allowed only when
   `planned_screen_count = 1`; for several planned screens the correction
   cannot be explained away.
9. Noise screens use only `DISCOVERY` or `SYNTHETIC` data. `PASS` permits Phase-0
   expenditure and is not evidence of an effect, mechanism, forecast, or net
   edge.

## Rejected alternatives

- **Fixed universal p-value:** rejected because family size and dependency
  structure vary, and the market null distribution drifts.
- **Naive permutation as the standard:** rejected when it destroys session
  structure, autocorrelation, or volatility clusters.
- **Count only surviving candidates:** rejected because this shrinks the actual
  search space after seeing results.
- **Increase family size after each screen:** rejected because decisions already
  made would retroactively receive a different threshold.
- **Benjamini–Hochberg as a running individual-test cutoff:** rejected because
  the BH rank requires the complete sorted p-value family.
- **Noise screen for every idea without exception:** rejected in favour of a
  narrowly defined waiver for theory, scheduled events, and replication.
- **Require an actor constraint already at `INBOX`:** rejected so raw ideas can
  continue to be recorded cheaply without losing their origin.
- **Treat schema prose as a calculation check:** rejected; semantic invariants
  are validated by executable code.

## Consequences

- A large generator run can no longer be silently treated as a series of
  independent five-percent screens.
- The catalogue can grow from internal observations without confusing
  observation with evidence.
- `INBOX` remains lightweight; additional obligations begin only at a
  data-based screen or promotion.
- The framework is still not tested end to end in practice. The known gap of a
  fully completed real Research Case remains.

## Action items

1. [x] Add catalogue origins and migrate existing entries.
2. [x] Create search-space and noise-screen schemas.
3. [x] Implement a semantic cross-artifact validator.
4. [x] Tighten the `PROMOTED` intake and actor constraint.
5. [x] Add positive, negative, arithmetic, and cross-platform tests.
