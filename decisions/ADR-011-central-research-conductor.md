# ADR-011: Central research conductor with binding specialist routing

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Research owner and research-framework maintainer

## Context

The framework has specialist roles for idea generation, philosophy of science,
and quantitative condition questions. It did not previously specify who leads a
case, preserves its state across work steps, or decides when each role must be
involved.

A role description alone is not enough. A language model can forget a required
review, specialists can duplicate work, and user communication can collapse into
technical details. Two transitions are especially critical: the concept review
before operationalizing an incomplete book strategy, and the
scientific-philosophy continuation review after a non-positive frozen result.

## Decision

1. Every user-facing research task is led by exactly one `research-conductor`.
   It remains the user's sole contact and owns the next-step decision.
2. Before every material transition, the conductor records the current state in
   a machine-testable checkpoint.
3. A deterministic router uses that classified state to choose the next
   permitted work step. The language model classifies the meaning of the
   request; fixed transition rules are not left to its memory.
4. The `scientific-philosophy-critic` is mandatory before operationalizing an
   incomplete prose strategy once source reconstruction exists and concept
   review is still missing.
5. The same specialist is mandatory after `FALSIFIED`, `PRECISE_NULL`,
   `INCONCLUSIVE`, or `INVALID_TEST` when the owner wants to attribute causes,
   materially change the investigation, or continue empirically.
6. The `condition-inquiry-analyst` is used only after a provisional
   operationalization exists and the question concerns measurement quality,
   definition sensitivity, or observable success conditions.
7. The idea generator is used only when the owner actually wants new short-term
   trading ideas. It does not replace intake, reconstruction, or rescue of an
   existing idea.
8. Specialists work sequentially under a bounded order and specified output
   format. They do not speak directly to the user and do not change the research
   question, source strategy, or frozen result.
9. Specialist results are reviewed before the conductor advances the state. A
   missing or invalid required contribution blocks the transition; the main
   agent must not silently simulate it.
10. A routing decision does not automatically authorize data access or a
    backtest. Empirical work still requires a separate assignment and its own
    prerequisites.
11. For Codex and compatible agents, `AGENTS.md` is the binding entry point;
    Claude also reads `CLAUDE.md`, which points to that same source.
12. Before and after every specialist handoff on an existing case, compare the
    research question, strategy, market, time horizon, trigger, and target.
    Only an unchanged comparison permits acceptance. A deviation remains
    ineffective, is explained clearly to the user, and requires an explicitly
    new research version before it can be adopted.
13. An intended `INTERVENTIONAL` or `COUNTERFACTUAL` claim is routed to the
    `causal-identification-critic` before estimation or causal wording. Purely
    predictive questions do not trigger this step.
14. The causal critic supplies a separate machine- and semantically validated
    identification artifact. Estimators, event windows, temporal ordering, and
    causal discovery do not replace the identification argument.

## Rejected alternatives

- **Let each specialist decide when it is needed:** rejected because no one
  specialist reliably owns the complete state and order.
- **Use only a free-form main agent without fixed transition rules:** rejected
  because required reviews would depend on one run's prompt interpretation and
  memory.
- **Use completely rigid automation without semantic classification:** rejected
  because the meaning of a user question and the materiality of a decision
  cannot be derived from file states alone.
- **Let specialists speak directly to the user:** rejected because it creates
  conflicting explanations, technical inside views, and unclear overall
  responsibility.
- **Make parallel specialists the default:** rejected because the relevant steps
  depend on each other and agreement between agents is not evidence.

## Consequences

- The scientific-philosophy critic is automatically required at the two critical
  transitions instead of being merely documented as an option.
- Causal language is released only after an independent, finance-specific
  identification review. This does not automatically raise mechanism, forecast,
  or trading status.
- The user receives one merged, understandable response from the conductor and
  does not have to coordinate internal agent work.
- Checkpoints and clear responsibilities make resumption, error analysis, and
  collaboration with several writing tools more robust.
- Fixed routing prevents forgotten required transitions, but does not prove that
  a specialist's substantive answer is correct.
- Deterministic contract and routing tests check structure and order. Whether a
  particular model follows the control in a live dialogue must additionally be
  checked by a marked `LIVE_AGENT` run.
- Routing and reconstruction themselves do not test a strategy, access market
  data, or run a backtest.

## Action items

1. [x] Define the central research conductor as an agent role.
2. [x] Make checkpoints and routing decisions machine-testable.
3. [x] Implement mandatory transitions for concept review, condition inquiry,
   and scientific-philosophy continuation.
4. [x] Document the mandatory entry point for Codex and Claude.
5. [x] Add positive and negative routing cases to contract and regression tests.
6. [x] Add a six-point drift check before accepting existing research handoffs.
   This first version was superseded by the full research fingerprint in
   ADR-013.
7. [x] Add the causal critic, required artifact, and router gate for causal
   claims.
8. [ ] Check the behaviour of an actually connected main agent in a
   `LIVE_AGENT` run before claiming a model or prompt release.
