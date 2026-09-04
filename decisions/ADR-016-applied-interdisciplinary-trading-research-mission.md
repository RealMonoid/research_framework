# ADR-016: Applied interdisciplinary trading-research mission

**Status:** Accepted
**Date:** 2026-09-04
**Decision owner:** Research owner

## Context

The framework already supports reconstruction of source strategies,
mechanism-led candidate generation, empirical evaluation, strategy engineering,
and protection against unsupported claim promotion. Its purpose was nevertheless
described mainly as decision support and research control. That wording could be
read as making scientific governance or foundational inquiry the end goal.

The interdisciplinary foundation now explains how finance, cognitive science,
AI search, philosophy of science, experimental design, statistics, machine
learning, and decision theory can cooperate through bounded roles and explicit
interfaces. The project needs an applied mission that connects this architecture
to strategy research without weakening the evidential boundaries.

## Decision

Adopt the following program-level mission:

> Identify or develop executable trading strategies whose positive expected net
> edge is supported by evidence appropriate to the claim and remains credible
> after realistic costs, liquidity, slippage, capacity, execution, and risk.

The project pursues this mission through two primary research routes under one
standard:

1. rigorously reconstruct and test existing strategies without silently
   changing their source identity; and
2. generate and develop new strategy hypotheses through bounded, explicit, and
   fully recorded search.

Both routes must also accumulate bounded reusable learning from positive,
negative, inconclusive, blocked, and not-testable outcomes. Learning may concern
market representations, mechanism candidates, observable conditions,
measurement choices, research methods, or failure modes. It may guide later
candidate generation, test design, and capital decisions, but it is not evidence
for another strategy unless that transfer receives an appropriate test.

Scientific and interdisciplinary controls are means to the applied mission, not
an academic-publication or detached foundational-research objective. An
individual Research Case may correctly stop without producing an active
strategy. Such a stop protects capital and informs later search; it does not
replace the program-level objective.

## Consequences

Positive:

- The project has one explicit applied purpose connecting strategy generation,
  evaluation of existing strategies, and cumulative learning.
- Negative and inconclusive results remain useful without being relabelled as
  strategy success.
- Machine learning retains a bounded predictive role inside a wider research
  architecture rather than becoming the identity of the project.
- Existing gates can be judged by whether they improve strategy generation,
  evaluation, learning, or capital protection while preserving evidential
  integrity.

Costs and limits:

- The framework does not guarantee that a viable strategy exists or that a
  research line will produce one.
- Learning across strategies, instruments, horizons, or regimes remains a new
  claim with explicit scope; similarity alone does not validate transfer.
- A changed strategy, condition, mechanism, or operationalization remains a new
  candidate or research version. It never rewrites the prior result.
- The mission does not authorize market-data access, a backtest, deployment, or
  capital allocation without the required case-specific decisions and gates.

## Research basis

The division of disciplinary labour, relevance filter, anti-eclecticism rules,
trading implications, and source ledger are documented in
[`INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md`](../references/INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md).

## Verification

The mission is reflected in the canonical agent policy, human-facing README,
mandatory Quickstart, normative research standard, agent entry document, and
shared roadmap without changing the existing implementation order or claiming
that a strategy, market result, or live-agent reliability has been validated.
