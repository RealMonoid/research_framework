# ADR-003: Scope and evidence-tiered intake of intraday hypotheses

**Status:** Accepted **Date:** 2026-08-30 **Deciders:** Project manager and research framework maintainer

## Context

Ideas for intraday research are often described simultaneously as a market mechanism, observed pattern, forecast signal and tradable anomaly. This results in impermissible jumps in the chain of evidence. Examples are:

- from documented market-maker hedging to an immediately profitable gamma strategy,
- inferring a safe price path from an index or funding rule,
- treating a historical return decomposition as a stand-alone mechanism,
- or treating a peer-reviewed finding without project-specific replication as an identified executable trading edge.

At the same time, the expression “news-free” is ambiguous. It may mean the exclusion of classic information events such as earnings, CPI or FOMC, although planned structural events such as index changes, auctions or funding timestamps are still used. However, it can also be understood as an untestable statement that no new information entered the market at any time. The latter is not empirically observable.

The framework therefore requires a binding intake rule that defines the scope of an idea before it is developed and strictly separates mechanism evidence from forward predictability and an executable net edge.

## Decision

Each new intraday hypothesis is classified before data selection, backtest and modeling. The classification is not a quality rating or activation release.

### 1. Scope taxonomy

Each candidate receives exactly one primary scope. Secondary scopes may be supplemented if the hypothesis actually connects several mechanisms.

| Scope | Definition | Typical examples | Normative boundary |
|---|---|---|---|
| `INFORMATION_EVENT` |Price response to the publication of new company, macro or policy information|Earnings and PEAD, guidance, CPI, FOMC, ad hoc notifications|Not allowed under a policy that excludes news or macro events|
| `SCHEDULED_STRUCTURAL_EVENT` |Pre-scheduled market, benchmark, settlement or mandate process that can generate mechanical flows|Index rebalancing, opening/closing auction, funding timestamp, month-/quarter-end rebalancing|Is an event, even if it does not respond to new fundamental information|
| `CONTINUOUS_ENDOGENOUS_MECHANISM` |Continuous process arising from trading, liquidity provision, inventory, hedging or interaction of markets|Order flow imbalance, liquidity withdrawal, lead lag, execution flows, conditional gamma hedging|May not be considered prognostic solely because of mechanical plausibility|
| `RETURN_DECOMPOSITION` |Descriptive breakdown of observed returns by time window, session, factor or portfolio|Overnight versus intraday, open-to-close versus close-to-open, session seasonality|Is initially a measurement and diagnostic perspective, not an independent mechanism|

The taxonomy is final for scope and routing; the mechanism families examined within it are expressly **not exhaustive**. In particular, eligible candidates are not limited to three or four supposedly fundamental mechanisms.

### 2. Operationalization of “news-free”

“News-free” is not claimed as a property of reality, but only operationalized as a documented research policy. Such a test must at least record:

1. which event classes are excluded,
2. which calendars, feeds, providers and versions cover these events,
3. which instrument and event-specific exclusion windows apply,
4. how late, corrected or missing messages are handled;
5. which known coverage gaps remain.

The absence of a hit in the feeds used does not prove the absence of new information. Results are therefore called “filtered according to policy and known feed coverage”, not information-free. Planned structural events must be declared separately and must not become invisible under the label “news-free”.

### 3. Separate evidence levels

Each hypothesis is conducted at exactly the highest level actually occupied. The steps must not be skipped by linguistic plausibility.

#### `mechanism_supported`

There is robust evidence that the claimed economic or mechanical channel can exist in a defined setting. This may include primary academic studies, stock market rules, index methodologies, fund prospectuses or direct market data.

This stage allows the formulation of a falsifiable hypothesis. It demonstrates neither stable predictive power nor tradability. The direction of a signal must be conditionally correct, such as the sign of net gamma exposure or an actually documented rebalancing mandate.

#### `forward_predictive_oos`

The pre-frozen hypothesis shows time-correct predictive power on previously unseen data. At least:

- decision-time available features and point-in-time data,
- a defined target and forecast window,
- timely out-of-sample or walk-forward separation,
- control of selection, multiple testing and leakage risks,
- stability and regime analysis,
- as well as the event and coverage filters specified for the scope.

Out-of-sample predictability can be gross and yet untradable according to costs, latency or capacity limits.

#### `executable_net_edge`

The forecast can be implemented as a robust net edge with the real instruments and decision times available. In addition to the previous stage, at least:

- executable prices instead of non-executable reference or auction prints,
- latency, queue position and fill probability,
- spread, fees, slippage and market impact,
- borrow, funding, margin and liquidation risk, where applicable;
- turnover, capacity, position limits and operational errors,
- as well as prospective shadow, paper or live evidence after the freeze.

Only this level can carry an activation together with all other risk and governance gates. A mechanism paper is never in itself a trading edge. Even a paper with reported strategy performance does not replace point-in-time, cost-conscious and project-specific replication.

### 4. Non-exhaustive families of mechanisms

The intake must allow new families. The current search space includes, among other things:

- order book, order flow, market liquidity and dealer inventory,
- cross-market pricing, lead lag and relative price fixing,
- TWAP, VWAP and other execution flows,
- options, futures and ETF hedging including gamma and delta effects,
- benchmark, fixed mix, target date and other mandate rebalancing;
- Opening, closing and other periodic auctions and session transitions,
- funding, settlement, expiry and margin mechanisms;
- Relative Value, Pairs, Cointegration and Temporary Base Deviations,
- forced deleveraging, liquidation and risk limit flows,
- Participant, access and time zone segmentation.

This list is a research index, not a whitelist, and not a claim that each family contains a prediction or net edge. Academic research, stock market documents and exploratory data analysis are sources or methods of hypothesis, not additional families of mechanisms.

### 5. Minimum content of an intake record

Before forwarding to the research process, at least:

- precise mechanism and forecast claim,
- primary and optionally secondary scope,
- market, venue, instruments, session and time horizon,
- decision-time observable inputs and intended target,
- News/Event policy, feed coverage and exclusion windows,
- currently supported evidence level,
- expected sign including all conditions;
- central alternative explanations and falsification tests,
- implementation, cost and capacity assumptions,
- as well as discontinuation and promotion criteria for the next level of evidence.

## Rejected Blanket Alternatives

### Alternative A: The intraday market can be completely reduced to three or four mechanisms

Rejected. Such lists are useful entry points, but neither complete nor stable about markets, products and market structure changes. They also promote scope laundering when sources, measurement perspectives and mechanisms are equated.

### Alternative B: A mechanical or planned process is automatically news-free

Rejected. For example, index changes require an announcement; opening processes incorporate overnight information; funding and auction windows may coincide with news. The mechanical part remains testable, but must be isolated by policy, coverage and exclusion windows.

### Alternative C: Peer review or journal prestige proves a current trading edge

Rejected. Publication status and source quality are recorded according to ADR-002, but do not replace replication or current out-of-sample and execution evidence.

### Alternative D: A statistically significant pattern proves its mechanism

Rejected. The same pattern can arise from information, institutional constraints, liquidity, measurement errors or multiple overlapping channels. Mechanism claim and forecast claim are tested separately.

### Alternative E: Out-of-sample predictability is already a net edge

Rejected. Non-tradable prices, latency, low fill rates, costs, borrow, funding, impact and capacity can completely eat away at a valid forecast.

### Alternative Q: No hit in the event feed proves the absence of news

Rejected. Feeds have coverage, timestamp, classification and revision limits. The remaining portion of information is unknown and is not set to zero.

## Consequences

- Incoming intraday ideas are accepted as hypothesis candidates, not
as already validated strategies.
- PEAD, earnings, CPI and FOMC are listed as `INFORMATION_EVENT` and are not
  admissible in a research branch that excludes news or macro events.
- Index rebalancing, funding, end-month/quarter processes and auctions remain visible as `SCHEDULED_STRUCTURAL_EVENT`; they may be examined in an appropriately defined structural-event module.
- Order-flow, execution and gamma hypotheses can be used as
  `CONTINUOUS_ENDOGENOUS_MECHANISM`, but require conditional position or sign assumptions and event filters.
- Overnight/intraday findings are initially treated as `RETURN_DECOMPOSITION`. Such a decomposition shall not be declared a strategy without a separate mechanism and execution test.
- A research case can contain multiple scopes, but must report results and gates scope by scope; evidence from one scope must not implicitly release another.
- The Evidence Grade from the operations layer remains separate from the three development stages defined here. Source strength, hypothesis maturity and activation readiness are different dimensions.
- Every promotion to `forward_predictive_oos` or `executable_net_edge` creates a verifiable, versioned decision record. Downgrades for replication errors, regime breaks or cost changes remain possible.
- The additional intake effort reduces the number of quickly activatable ideas,
prevents the equivalence of plausible market history, published findings and reliable net edge.

## Action Items

1. [x] Scope taxonomy and evidence levels included in the normative research workflow.
2. [x] Intake fields integrated into case template and machine-readable intake artifact.
3. [x] Positive and negative contract tests for scope, news policy and promotional pathways.
4. [x] Eval cases for mechanism-to-edge exaggeration, anonymous execution signatures, and incomplete news coverage supplements.
5. [ ] Reclassify existing intraday hypotheses according to the new taxonomy; in the present repository, no specific research cases are yet available, so this remains open as a migration step for the first imported cases.
