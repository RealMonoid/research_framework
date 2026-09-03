# ADR-009: Scientific-philosophy review of failure attribution and continuation

**Status:** Accepted; pre-operationalization scope amended by ADR-010
**Date:** 2026-08-31
**Deciders:** Research owner and research-framework maintainer

## Context

A test concerns not only a hypothesis, but also auxiliary assumptions,
operationalization, measurement, data quality, scope, model, and implementation.
After a negative result, logic therefore does not determine automatically which
link failed. This is especially important for strategies reconstructed from
prose: otherwise a false dilemma appears—either reject the core idea too early
or keep changing the operationalization after seeing the result until the
desired outcome appears.

The existing four-state outcome decision and the rule that an unexpected sign
can generate at most a new hypothesis protect the frozen result. What was
missing was a separate contract for deciding which follow-up change contains
genuinely new scientific content.

## Decision

1. `agents/scientific-philosophy-critic.md` is a permanent agent contract.
2. `schemas/scientific_philosophy_review.schema.json` separates the core claim,
   auxiliary assumptions, error attribution, research programme, anomaly status,
   and revision proposals.
3. Duhem–Quine is used as an attribution limit: without discriminating evidence,
   the cause of failure remains `NON_UNIQUE` or `UNRESOLVED`.
4. The Q8 result of the old Research ID remains unchanged.
5. Lakatos classifies follow-up changes as `PROGRESSIVE`, `DEGENERATIVE`,
   `DIAGNOSTIC_ONLY`, or `UNRESOLVED`.
6. `PROGRESSIVE` requires a previously unimplied prediction, a falsifier, an
   independent evaluation plan, and a new Research ID.
7. Degenerative changes and diagnostics do not authorize a new confirmatory
   test. Diagnostics can locate an error, but cannot rescue an old claim.
8. Kuhn's perspective is limited to the status of the research programme.
   Isolated or recurring anomalies and available rivals are recorded; the
   absence of a rival is not positive evidence.

## Rejected alternatives

- **Attribute every failure uniquely to the hypothesis:** rejected because the
  test concerns the entire bundle.
- **Retest every alternative operationalization:** rejected because a post-result
  variant without new empirical content merely circumvents the failure.
- **Use a new Research ID as the sole solution:** rejected; a new label creates
  no new prediction.
- **Use Kuhn to justify ignoring an anomaly:** rejected; programme-level status
  does not change the finding of the individual test.
- **Make philosophy of science a mandatory block for every raw idea:** rejected.
  ADR-010 requires early concept testing specifically for incompletely defined
  source strategies; ordinary raw ideas are not burdened.

## Consequences

- A negative result may remain honestly underdetermined without permitting
  arbitrary post-result rescue.
- Source strategies may continue with a reasoned new operationalization when it
  produces an independent risky prediction.
- The artifact is neither a backtest, a result generator, nor a human review.
- The synthetic VWAP case demonstrates only the contract; it claims no real test
  or edge.
