# ADR-010: Concept audit and quantitative condition inquiry

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Research owner and research-framework maintainer

## Context

Source reconstruction makes open definitions visible, but the framework did
not previously distinguish cleanly between four things: strategy components,
application instructions stated by the source, suspected success conditions,
and completely unknown success conditions. Plausible prerequisites could
therefore be treated as facts without being noticed before operationalization.

Triggers, filters, and outcomes can also use common raw variables or windows.
The resulting statistical relationship is neither automatically a market
mechanism nor automatically an error. Regime filters had been treated as state
variables, but not explicitly as provisional measuring instruments with limited
scope.

Finally, the framework lacked a positive method for generating condition
hypotheses. It could document known conditions, but did not regulate how to ask
under which observable circumstances an outcome changes.

## Decision

1. Before any incompletely defined source reconstruction is completed, the
   `scientific-philosophy-critic` creates a `strategy_concept_audit`.
2. The audit separates `STRATEGY_DEFINING`, `SOURCE_STATED_APPLICATION`,
   `SUSPECTED_PERFORMANCE_MODIFIER`, and `UNKNOWN_SUCCESS_CONDITION`.
3. Suspected and unknown conditions must not silently enter the source strategy
   as mandatory filters. The audit does not claim completeness.
4. Common inputs, windows, and deterministic transformations are recorded as
   construction dependencies. They can create associations or change the
   question being answered, but they are neither causal evidence nor
   automatically a design error.
5. Regime, state, and context filters are provisional measuring instruments.
   Their class frequency does not measure separation performance. Assessment
   uses future behaviour not already used to construct the filter and an
   incremental comparison with continuous inputs or a simple baseline.
6. Predictive separation validates at most the declared practical purpose of a
   classification. It proves neither a real hidden market state nor an actor,
   intention, coercion, or causal mechanism.
7. A non-informative filter invalidates the state claim that depends on it. An
   event claim that can be separated from the filter may remain open.
8. If a reliable actor hypothesis is missing for an associative or predictive
   question, record the actor status explicitly as `UNSPECIFIED / NOT_CLAIMED`.
   This prevents an invented mechanism story without banning the narrower
   question.
9. After provisional operationalization, the `condition-inquiry-analyst` may
   create a `condition_inquiry` for construction diagnostics, definition
   sensitivity, interpretable condition generation, conditional predictive
   ability, or stability across time and environments.
10. A condition found from data is a new success-modifier hypothesis. It does
    not retroactively become part of the source rule.
11. A source-defined target must not be silently replaced by a methodologically
    more independent target. The new target answers a new question.
12. Necessary Condition Analysis is only a justified exploratory special case,
    not the default for noisy short-term markets.

## Rejected alternatives

- **Add every plausible context immediately as a filter:** rejected because it
  would make assumptions indistinguishable from the source strategy.
- **Judge a filter by its class frequency:** rejected because frequency does not
  measure separation power.
- **Treat different filter groups predictively as real regimes:** rejected;
  practical information value, ontology, and causality are different claims.
- **Treat common windows automatically as errors:** rejected. The dependence
  must be made visible and interpreted narrowly; its substantive admissibility
  depends on the original question.
- **Use an independent outcome as a neutral repair:** rejected. It may be a
  meaningful new question, but it does not silently replace the source claim.
- **Make condition search only another protection gate:** rejected. Its primary
  purpose is to generate understandable, observable, and later testable
  condition hypotheses.

## Consequences

- The framework cannot fully discover unknown prerequisites, and no longer
  claims that it can.
- Hidden assumptions become visible before operationalization without turning
  plausible ideas prematurely into facts.
- State filters can be assessed for their stated purpose without upgrading their
  names into market ontology or causal explanations.
- Quantitative condition search becomes a generator of new research questions
  and remains separate from the identity of the source strategy.
- The synthetic examples perform no backtest and contain no market result.
