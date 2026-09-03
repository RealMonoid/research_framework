# ADR-008: Source-faithful reconstruction of incompletely operationalized strategies

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Project manager and research framework maintainer

## Context

Trading books and other secondary sources often provide recognizable setups,
but not unambiguous executable rules. They mix rules, examples, alternatives,
and explicit trader discretion. The previous operationalization table in the
Research Case recorded the selected measurement definition later, but not the
prior translation step: which components came from the source, which were open,
and which were added?

The problem is not a missing backtest rule. Without a source reconstruction, it
is impossible before each test to distinguish whether a later specification
replicates the published strategy, reconstructs it, or materially changes it.

## Decision

1. `schemas/strategy_reconstruction.schema.json` is introduced as a separate
   upstream artifact.
2. The reviewed source excerpt is explicitly bounded; an excerpt must not be
   presented as a fully reviewed work.
3. Source claims are paraphrased and marked as required, recommended, optional,
   illustrative, or unclear. An example is not a rule.
4. Constructs receive one of the statuses `SOURCE_SPECIFIED`,
   `SOURCE_ALTERNATIVES`, `UNSPECIFIED`, `DISCRETIONARY`, or `CONTRADICTORY`.
5. Operationalization candidates retain their origin. A proposal from domain
   convention, external literature, or the researcher's own reconstruction is
   not attributed to the source.
6. Candidates are not selected automatically. Recording them is neither market-
   data access nor automatically a statistical test or search space.
7. Explicit discretion may be retained as a human protocol. Removing it may
   produce a `SIMPLIFIED_VARIANT`, but not a replication.
8. `REPLICATION` is inadmissible while an essential construct remains
   alternative, unspecified, discretionary, or contradictory.
9. `scripts/inspect_strategy_reconstruction.py` checks schema and reference
   integrity and the source-fidelity boundary. It does not execute a strategy.

## Rejected alternatives

- **Write a backtest rule directly:** rejected because source interpretation and
  strategy design would be mixed invisibly.
- **Use every example as the default:** rejected because examples can illustrate
  rules without defining them generally.
- **Automatically test every plausible definition:** rejected because a
  translation catalogue is not a test instruction.
- **Remove discretion completely:** rejected as a general default; this may be
  a legitimate simplified variant, but it must be named as such.
- **Create a global construct catalogue immediately:** rejected for now. The
  first real book example will show which recurring definitions are genuinely
  worth cataloguing. The artifact contract works without pretending that such a
  catalogue is complete.

## Consequences

- Prose strategies can be used as sources of ideas without open terms silently
  becoming alleged author rules.
- A documented reconstruction remains distinguishable from a replication and a
  simplified variant.
- The artifact does not yet generate a finished strategy. Later selection
  remains a conscious domain decision.
- The VWAP book case is a worked reconstruction example, but not a completed
  Research Case and not a backtest.

## Action items

1. [x] Implement the schema and semantic inspector.
2. [x] Capture book excerpts as source-faithful source extraction.
3. [x] Add positive and negative contract tests.
4. [x] Extend the short path and research standard with the optional router.
5. [ ] Decide after further real reconstructions which constructs belong in a
   reusable catalogue.
