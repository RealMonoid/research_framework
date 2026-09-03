# ADR-006: Upstream mechanism catalogue as a genuine idea generator

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Research owner and research-framework maintainer

## Context

The framework could already accept, route, and test incoming hypotheses
rigorously. It did not, however, contain a producer that created new ideas
before intake. Without an external prompt, the inbox remained empty; adding
more screening rules would not have fixed that gap.

Short-horizon literature documents productive mechanism families including
order-book imbalance, split large orders, intermediary inventory, stop clusters,
derivative hedging, option expiry, predictable futures rolls, closing auctions,
cross-market price discovery, intraday repetition, index rebalancing, and
funding and liquidation mechanics. These studies do not prove a new strategy,
but they provide mechanisms, expected signatures, and natural horizons from
which candidates can be deduced.

A purely actor-based approach is too narrow. Not every productive intraday idea
has a clearly identifiable compelled actor; order-book states, lead-lag
relationships, and repeatable clock-time patterns can also generate ideas.
Conversely, a known constraint creates more than direct price pressure:
anticipation, additional liquidity provision, and a later unwind are separate
candidates.

From the discussion of insight heuristics, we adopt only three productive
transformations: contradiction, connection, and relaxation of an assumption.
They generate candidates, not validity or evidence claims. Premortems,
intuitive self-rating, and process metaphors are not part of the generation
layer.

## Decision

1. `generation/mechanism_catalog.v1.json` is the versioned initial catalogue,
   limited to intraday and short-swing horizons of up to five trading days.
2. The catalogue supports five equivalent generation routes:
   `CONSTRAINT_FIRST`, `MICROSTRUCTURE_STATE`, `LINKAGE_OR_IDENTITY`,
   `LITERATURE_REPLICATION`, and `OBSERVATION_DRIVEN`.
3. The generator uses the grammar `Mechanism × Phase × Observable Imprint` and
   the operators `PHASE_PATH`, `EXPECTATION_VIOLATION`,
   `MECHANISM_CONNECTION`, and `ASSUMPTION_RELAXATION`.
4. `scripts/generate_hypotheses.py` is a deterministic producer. It creates a
   generation run and valid minimal `INBOX` artifacts.
5. `agents/intraday-hypothesis-generator.md` defines an optional agent
   extension with the same triggers, limits, and output fields.
6. A generation run always ends before screening and promotion. It assigns no
   evidence grade or confidence score and makes no claim about profitability.
7. The existing `INBOX` remains lightweight. Richer generator provenance is
   stored in a separate generation run and referenced from the candidate.

## Explicit non-decisions

Not introduced:

- a universally mandatory `actor_constraint`;
- a premortem field or premortem operator in the generator;
- a self-assigned validity class;
- a ban on promoting observation-driven ideas;
- a new noise, backtest, or security gate;
- Kaizen, Gemba, or other management metaphors as normative prose;
- a claim that rejection clusters are automatically market anomalies; or
- portfolio theory or long-term investment factors.

These exclusions do not remove the existing downstream research reviews. They
keep the generation layer separate from testing and release.

## Consequences

- The framework now has an executable path from a versioned mechanism catalogue
  to new intake artifacts.
- Contradictions do not rescue an old hypothesis; they create a new idea family
  with its own ID.
- Predictable flows generate anticipation, absorption, and unwind ideas rather
  than only naive directional bets.
- The catalogue can grow under source and version control without bloating the
  intake schema with mandatory fields.
- The quality and tradability of generated ideas remain open questions for the
  existing downstream process.

## Sources motivating the initial catalogue

- Cont, Kukanov, and Stoikov (2014),
  <https://doi.org/10.1093/jjfinec/nbt003>
- Gould and Bonart (2016), <https://arxiv.org/abs/1512.03492>
- Moro et al. (2009), <https://doi.org/10.1103/PhysRevE.80.066102>
- Hendershott and Menkveld (2014),
  <https://doi.org/10.1016/j.jfineco.2014.08.001>
- Osler (2003), <https://doi.org/10.1111/1540-6261.00588>
- Baltussen et al. (2021),
  <https://doi.org/10.1016/j.jfineco.2021.04.029>
- Ni, Pearson, and Poteshman (2005),
  <https://doi.org/10.1016/j.jfineco.2004.08.005>
- Bessembinder et al. (2016),
  <https://www.sciencedirect.com/science/article/pii/S0304405X16300113>
- Wu and Jegadeesh (2022), <https://doi.org/10.1016/j.jfineco.2021.12.003>
- Chan (1992), <https://doi.org/10.1093/rfs/5.1.123>
- Heston, Korajczyk, and Sadka (2010),
  <https://doi.org/10.1111/j.1540-6261.2010.01573.x>
- Pavlova and Sikorskaya (2023), <https://doi.org/10.1093/rfs/hhac055>
- Greenwood and Sammon (2025), <https://doi.org/10.1111/jofi.13410>
- Cheng, Deng, Wang, and Yu (2021), <https://arxiv.org/abs/2102.04591>
- He, Manela, Ross, and von Wachter (2022),
  <https://arxiv.org/abs/2212.06888>

## Action items

1. [x] Create the mechanism catalogue and schemas.
2. [x] Implement the deterministic producer.
3. [x] Create the agent contract with trigger examples and an output contract.
4. [x] Persist a reproducible four-operator run as an example.
5. [x] Integrate positive, negative, and end-to-end producer tests into CI.
6. [ ] After practical use, extend the catalogue with additional venue- and
   instrument-specific mechanisms.
