# ADR-017: Interdisciplinary claim coordinates and production loop

**Status:** Accepted
**Date:** 2026-09-04
**Decision owner:** Research owner

## Context

ADR-016 adopted an applied mission that combines rigorous testing of existing
strategies, controlled generation of new candidates, and scoped cumulative
learning. The interdisciplinary foundation assigns different question types to
finance, cognitive science, AI search, epistemology, experimental design,
statistics and ML, and decision theory.

An external synthesis supplied four useful refinements: distinguish a claim's
explanatory level from its target; make one lane lead the question currently
blocking progress; account explicitly for scarce research resources; and close
the path from research to strategy through data, execution, portfolio, risk,
and operating work. Taken literally, however, parts of that synthesis would
create new errors. A single expected-utility currency could price away hard
epistemic constraints, exactly one bottleneck could be mistaken for exactly one
cause, and universal cost, sample-size, ML, capacity, or retail-trading rules
could be imported without their assumptions.

## Decision

Adopt four linked operating principles.

### 1. Locate ambiguous claims on two coordinates

When interdisciplinary substitution is a material risk, identify:

- the **explanatory level**: objective/problem, representation/algorithm, or
  concrete implementation; and
- the **target**: market and participants, research process and agents, or
  strategy, portfolio, and production system.

These coordinates clarify scope. They do not supply evidence, replace the
predictive/interventional/counterfactual claim level, or promote a conclusion.

### 2. Give each selected bottleneck question a primary owner

For each material bottleneck selected for action, name one disciplinary or
production lane as the primary owner of its next question. Keep every other
relevant field and competing bottleneck visible as a constraint, critic, or
dependency. Primary ownership coordinates work; it does not establish one true
cause, erase coupled bottlenecks, or give one field authority to answer another
field's question. When ownership is genuinely uncertain, retain the rival
diagnoses and use a bounded discriminating check.

### 3. Use a resource vector with hard admissibility boundaries

Treat independent data history, compute, elapsed time, attention, capital,
liquidity, and risk-bearing capacity as distinct scarce resources. Expected
decision value and value of computation may rank actions only after hard
research and capital protections are satisfied. No scalar score may waive
provenance, leakage, identification, validation, risk, or change control.

### 4. Close the applied loop through production reality

A validated phenomenon or other limited supported claim is not yet an
executable strategy. Strategy engineering must preserve the exact claim and
evidence status while addressing the versioned data path and quality,
decision-time availability, execution and microstructure, realistic costs,
liquidity and capacity, portfolio construction, risk and ruin constraints, PnL
attribution, monitoring, and operational reliability. The complete strategy
then requires unseen-data or controlled forward evidence. Production work may
reject, defer, or improve an implementation, but it cannot retrospectively
create evidence for the phenomenon, prediction, or mechanism. If production
work changes strategy behavior or another material assumption, it creates a new
version requiring new complete-strategy evidence; any retained upstream evidence
keeps only its original limited status.

## Explicit non-adoptions

The project does not adopt from the external synthesis:

- one universally conserved expected-utility currency across epistemic,
  computational, capital, and risk decisions;
- exactly one true bottleneck or one exclusive discipline for a research
  failure;
- the claim that only abduction or representation change can generate novelty;
- a universal movement-to-cost multiple or fixed order of research operations;
- a universal trade-count, Sharpe-to-sample-size, or ML sample cutoff;
- the substitution of mechanistic plausibility for independent predictive
  evidence when effective sample size is small;
- a general claim that capacity is immaterial; or
- discretionary retail intraday trading, swing trading, institutional quant,
  or any other segment as the unstated project default.

Any scoped empirical result about one market, horizon, participant population,
or implementation style remains evidence only for that scope unless a separate
transfer claim is tested.

## Consequences

Positive:

- Apparent disciplinary conflicts can be separated into different levels and
  targets instead of resolved by vocabulary.
- The conductor can route the next bounded question without pretending that a
  complex failure has one cause.
- Research prioritization becomes resource-aware without making safeguards
  tradable.
- The project's applied mission now includes the production work that stands
  between a research result and a defensible capital decision.

Costs and limits:

- The coordinates and primary-owner designation add small documentation and
  routing overhead when the distinction is material.
- This decision does not implement new machine-readable fields or prove that
  the architecture improves agent reliability or trading performance.
- `AGENTS.md` is the binding source for this adopted architecture. The research
  standard retains its inherited `DRAFT FOR ADOPTION` status and does not become
  an independent source of authority through this ADR.
- Production completeness is strategy-specific; this ADR supplies categories,
  not universal numerical thresholds.

## Research basis

The academic basis, source scopes, anti-substitution rules, and the distinction
between source-backed findings and project synthesis remain in
[`INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md`](../references/INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md).

## Verification

The decision is reflected in the canonical policy, normative research standard,
research-conductor role, human-facing README, and interdisciplinary foundation.
It changes no strategy, Research Case, empirical result, roadmap priority,
backtest authorization, deployment decision, or capital allocation.
