# ADR-015: Bounded quantitative data specialist

**Status:** Accepted
**Date:** 2026-09-03
**Decision owner:** Research conductor

## Context

The framework sometimes needs a quantitative calculation or a data-quality
diagnostic, but numbers alone do not justify handing a research or trading
decision to a specialist. A provider-backed data agent could also silently
turn an association into a causal story, mix intraday and swing data, hide
leakage, or report a plausible metric without saying what data were available.
The planned prospective data-fitness gate is broader and is not yet an
implemented artifact.

## Decision

Add one provider-neutral `data-analyst` role beneath the existing research
conductor. The role is conditional and is routed only for a concrete
quantitative information need that cannot be answered as simply by the
conductor. It returns one `data_analysis_report` containing:

- the exact question scope and decision relevance;
- data sources, snapshots, periods, instruments, grain, variables and data
  roles;
- completeness, missingness, duplicates, validity, outliers, timeliness,
  leakage/look-ahead, survivorship, dependence, and regime/session checks;
- methods, estimates, uncertainty, stability, alternatives, limitations and a
  bounded disposition.

The report schema fixes explicit no-action fields. The analyst cannot trade,
change positions or risk limits, alter the research question or rules,
authorize a backtest or validation, claim causality or a mechanism, change the
fingerprint or checkpoint, address the user, delegate, repeat an equivalent
analysis without new evidence, or create automatic follow-up. The conductor
validates the report, compares the complete fingerprint, interprets it, and
retains the final decision.

The Data analytics plugin may provide an implementation of this role, but the
repository contract is provider-neutral and has no plugin runtime dependency.
The condition-inquiry and causal-identification roles remain distinct. The
future data-fitness gate remains a separate prerequisite for operationalization
or empirical testing.

## Consequences

Positive:

- Quantitative work has a reproducible, inspectable boundary instead of an
  informal request to “look at the data”.
- The owner receives useful diagnostics without granting a specialist authority
  to trade, revise the hypothesis, or turn correlation into causality.
- Data-quality and trading-specific failure modes become visible before a
  report is accepted.

Costs and limits:

- The route adds a schema and validation step when it is actually used.
- The report still depends on truthful source and input references; it does not
  prove that an external provider supplied complete data.
- It does not replace the planned prospective data-fitness gate, a causal
  identification review, pipeline integrity controls, or a real validation.

## Verification

The route is covered by the deterministic router tests. The report is covered
by schema tests and semantic regressions for unavailable data, decision-time
leakage, unsupported backtests, failed quality checks, causal overreach, and
the no-trading boundary.
