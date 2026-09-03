# ADR-005: Independent causal and commercial axis and conditional variable selection provenance

**Status:** Accepted
**Date:** 2026-08-31

## Context

The framework already introduced three claim levels and separate statuses for mechanism, forward OOS forecast and net executable edge. However, the relationship between the two groups was only implicit. This left the misconception possible that an identified causal effect was automatically prognostic or tradable at cost.

At the same time, the intake lacked a machine-testable difference between predefined variables and a data-driven search for many candidates. A universal duty to feature import procedures would burden the simple case and pretend causal relevance.

## Decision

1. The research claim level
   (`ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`) and the
   validation/trading statuses (`mechanism_supported`, `forward_predictive_oos`,
   `executable_net_edge`) are expressly independent axes.
2. A causal claim may be based on an SCM/DAG, potential-outcomes design,
   structural econometric model, or another explicit identification model. The
   notation itself does not increase the claim level.
3. Each promoted intake declares variable selection as `PREDEFINED`,
   `DATA_DRIVEN`, or `HYBRID`.
4. `PREDEFINED` needs only a justification and the retained variables. `DATA_DRIVEN`
   and `HYBRID` additionally require the candidate universe, selection data and
   role, outcome visibility, methods, effective candidate number, search space,
   and selection-bias controls.
5. SHAP, Shapley, Impurity and other feature import procedures remain
optional diagnoses. They are neither a duty nor a proof of causality.
6. `VALIDATED_PHENOMENON` confirms neither a causal claim nor an executable
   net edge.

## Consequences

- The hypothesis schema increases to version `1.2.0`; `PROMOTED` demands the new
  variable-selection record.
- Positive and negative contract tests cover both the light `PREDEFINED` path
  and the stricter data-driven provenance.
- An eval case protects the separation between an identified effect and economic
  tradability.
- Real research cases are not invented by this change. The known end-to-end
  validation gap remains until a real case is available.

## Rejected alternatives

### Universal DAG requirement

Rejected because potential-outcomes and other explicit designs can identify an
estimand without an additional DAG. A diagram alone does not improve
identification.

### Mandatory SHAP/MDI interpretation

Rejected because these methods describe model- and distribution-dependent relevance and do not provide a general causal variable selection.

### Causal PASS as an automatic trade release

Rejected because a scientifically identified effect below spread, fees, slippage or latency can be economically worthless.
