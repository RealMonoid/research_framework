# 01_RESEARCH_STANDARD.md

**Version:** 2.0
**As of:** 2026-08-31
**Status:** DRAFT FOR ADOPTION
**Purpose:** Normative standard for developing, falsifying, validating, and monitoring trading phenomena, edge hypotheses, and strategies.
---

# 1. Research objective

Strategy research should not retrospectively find rules that generate a nice equity curve.

It should determine:

1. whether a reproducible market phenomenon exists,
2. whether this phenomenon provides additional information compared to an explicit zero model,
3. how big the effect is,
4. how uncertain this estimate is,
5. how much truly independent evidence exists,
6. under which pre-observable market states the effect is stronger, weaker, irrelevant or inverted,
7. whether the effect persists on genuinely new data,
8. whether it is economically usable according to costs and real execution,
9. and whether the strategy built from it remains stable in forward operation.

The central position is:

> We formulate verifiable predictions about conditional market distributions and try to refute them. Only surviving claims can be translated into strategies.

The logical strategy architecture remains:

`Market model → edge hypothesis → strategy → setup → trigger → trade plan → execution/management → evaluation`

The empirical research process can begin bottom-up:

`Observation → description → measurement → candidate hypothesis → freeze → new data → evaluation → decision`

Discovery and confirmation must be strictly separated.

In addition, **prediction and causality** must be strictly separated. A robust predictive edge can be economically useful without causally identifying its mechanism. Conversely, an identified causal effect does not guarantee a tradable prediction after costs.

## 1.1 Applicability, status router and testability

Before `PROMOTED` only the staggered intake from `QUICKSTART.md` and `schemas/hypothesis_candidate.schema.json` applies. An `INBOX` or `REJECTED` entry is not a research case and does not have to load or fill out the full standard.

From `PROMOTED` the core rules of this standard apply completely. However, method and tooling details are loaded only for the activated claim and selected method. Unselected optional procedures do not require N/A series.

A phase or gate status set by the executing agent is a self-declaration. It can only be tested by the named schema, the associated run/evidence reference and, if necessary, an independent review. Normative language does not replace this evidence.

---

# 2. Data roles and information budget

Each data set receives exactly one current role:

- `DISCOVERY`
- `DEVELOPMENT`
- `VALIDATION`
- `FINAL_HOLDOUT`
- `FORWARD_OOS`

As soon as a result influences a design decision, the relevant data set is Development Data.

A data set can lose its independent information value through use. Research thus has an **information budget**. Holdout data is a scarce resource and is not consumed until the project is statistically and economically testable.

---

# 3. Phase 0 – Feasibility and information budget

## 3.0 Entry threshold before phase 0

An observation-driven idea may enter phase 0 only after an early surrogate screen. Before the first screen, the complete candidate universe, planned test count, family alpha, and correction method are fixed in `schemas/search_space.schema.json`. All generated candidates count in the search space as soon as they are checked against data; counting only survivors is not allowed. Each investigated noise candidate increases this search space and thus raises the detection threshold for later real findings. For more than one planned screen, a multiplicity correction is mandatory. `NONE_JUSTIFIED` is only allowed for a one-test family and is not a waiver for a larger search space.

The screen uses `DISCOVERY` or `SYNTHETIC` data and preserves relevant dependencies such as session profile, autocorrelation, or volatility clusters. Naive permutation that destroys this structure is inadmissible. The null period must be comparable in time and market structure because it also drifts. `PASS` only means that Phase-0 effort is justified. It confirms neither effect, mechanism, OOS prediction, nor edge. Theory-driven, time-stamped event, and published replication ideas may use a reasoned waiver.

## 3.1 Purpose

Phase 0 prevents valuable independent data from being consumed for a hypothesis that cannot be meaningfully decided with the available data or at realistic costs.

The phase begins as soon as a rough definition of phenomena and outcome scale is available and is carried out in two stages:

1. **Pre-examination:** conservative screening before extensive discovery/development work. A `CONTINUE` opens only Discovery and Development.
2. **Formal recalculation:** after full operationalization of outcome, zero model, dependency, effective N and validation plan, but before pipeline integrity gate and freeze.

Independent validation must begin only after `PASS` of the formal recalculation.

## 3.2 Economic threshold

A **minimum economically relevant effect size** is defined.

It must be formulated in the same unit as the primary outcome.

In the case of a gross outcome, the following can apply conceptually:

\[
\delta_{econ} = \text{expected round-trip costs} + \text{necessary safety margin}
\]

For already net calculated outcomes, the threshold is adjusted accordingly.

The safety margin shall be justified in advance. It must not be set according to the result in such a way that an observed effect appears just “economically relevant”.

The margin of safety means an **additional absolute amount** to estimate costs. If a multiplier is used, the notation must clearly state whether the entire threshold is multiplied or only the margin. A universal multiplier for all strategies is not allowed; uncertainty in costs, slippage and capacity must be treated design-specifically.

## 3.3 Provisional cost model

Already in phase 0 conservative values are estimated for relevant cost components:

- fees,
- spread,
- slippage,
- funding, if relevant,
- expected fill disadvantages.

The model is deliberately rough. It should only answer whether the desired effect size could be economically interesting at all.

## 3.4 Power / decisionability

Before the formal test:

- primary test or primary estimate;
- desired error level or equivalent decision request,
- target power or equivalent precision requirement;
- economic relevance threshold `δ_econ`,
- assumed true planning effect `δ_plan` or direct precision goal,
- explicit null and alternative hypothesis or interval decision rule,
- assumed dispersion,
- expected dependency structure,
- required N or required independent information.

The minimum sample comes from this calculation or simulation, **not** from the number of already existing cases.

For classical formal tests, in the absence of a factually better, well-founded decision rule set in advance, `α = 0.05` two-sided and `Power = 80%` are considered working defaults. In the case of a tight final holdout or high cost of a false negative result, `90%` or a direct precision target should be tested. A one-sided test, lower power or other error weighting is only allowed with documented justification before the result is known. These defaults do not replace either loss function or design-specific simulation.

For the dispersion, separately documented:

- exploratory point estimator,
- the source, sample size and transferability of that estimator;
- uncertainty range,
- conservative planning value or predefined stress scenario.

A single estimator from a small, selected, or heavy-tailed discovery sample must not be used unchecked as the true planning dispersion. Depending on the design, external or pooled references, an upper uncertainty limit calculated under valid model assumptions, robust scale measures with a justified stress surcharge, or a scenario calculation are acceptable. `CONTINUE` is permitted only if feasibility also exists in the conservative scenario or the additional required information is explicitly procured.

The stress rule is set before the calculation. Among several pre-eligible and factually transferable candidates, the gate uses the most conservative value or the full scenario bandwidth. Robust scale measures may only be used after traceable mapping of the primary estimator sample distribution, if necessary by design-specific simulation.

`δ_econ` and `δ_plan` are not interchangeable. For example, if success requires the lower interval limit to be above `δ_econ`, the planning must map exactly to that decision rule; a mere power calculation for `0` versus `δ_econ` is not enough.

The source and justification of `δ_plan` are logged. A discovery point estimator must not be accepted as `δ_plan` unchecked; selection bias and uncertainty must be taken into account through conservative scenarios, shrinkage, or external references. `δ_plan` must not be changed after the validation result is known.

## 3.5 Available N and Effective N

The following shall be documented:

- nominal observation count,
- number of independent days/sessions/event clusters,
- symbol clusters,
- overlapping label/holding periods,
- estimated effective sample size or conservative bandwidth.

The gate is determined by the conservative lower limit of the effective N and the independent number of clusters, not just a point estimator. The order of calculation shall be:

`required independent information → design-specific DE/simulation → required nominal N`, each rounded up conservatively.

In the stress scenario, an estimated information gain `DE < 1` or `N_eff > N` is only taken into account if it is robustly supported by external, transferable evidence and a predefined model; otherwise, at least `DE = 1` applies to the planning.

For fewer than 30 plausibly independent clusters, `SMALL_CLUSTER_WARNING` is set. This threshold is a diagnostic and escalation point, not a universal criterion of existence. The warning status requires an inference suitable for a few clusters, design-specific simulation/calibration, or `BLOCKED`. It does not allow the blanket statement that a certain interval is necessarily too narrow or invalid just because of the number of clusters.

## 3.6 Phase 0 Decision

There are exactly three main decisions:

### `CONTINUE`

The currently available independent information is sufficient in the conservative scenario for the gate purpose reached. In the preliminary examination, `CONTINUE` allows only discovery/development; only the formal recalculation can open the way to freeze.

### `OBTAIN_DATA`

The hypothesis is basically testable, but the currently available independent information is insufficient. Only information that can realistically be obtained in the future therefore leads to `OBTAIN_DATA`, not to `CONTINUE`.

### `ABORT / CURRENTLY NOT TESTABLE`

The economic threshold, the available data or the expected dependency do not make a meaningful test with reasonable effort possible.

`OBTAIN_DATA` or `ABORT` must not be circumvented by lowering the economic threshold after the data are known.

---

# 4. Discovery – observe, describe, collect cases

Research may begin with theory or observation.

No theory is required. An observed pattern is sufficient as a starting point.

The first question is not:

> How do I trade this?

Instead:

> What exactly am I observing?

In Discovery you can:

- review charts,
- collect cases,
- try variables,
- change definitions,
- visualize relationships,
- seek counterexamples,

and record the changes.

Discovery is intentionally flexible. However, the data used for this purpose are not independent confirmation afterwards.

The case catalogue must contain not only winners or “nice” examples, but also:

- clear hits,
- clear failures,
- borderline cases,
- different time periods,
- various volatility states,
- and, where appropriate, several comparable instruments.

## 4.0 Optional preliminary idea generation

If a raw idea is missing, the mechanism catalog producer from `generation/` may be executed before the intake. It combines a literature or market mechanism with a phase and an observable imprint. Permitted generation routes are:

- `CONSTRAINT_FIRST`,
- `MICROSTRUCTURE_STATE`,
- `LINKAGE_OR_IDENTITY`,
- `LITERATURE_REPLICATION`,
- `OBSERVATION_DRIVEN`.

The operators `PHASE_PATH`, `EXPECTATION_VIOLATION`, `MECHANISM_CONNECTION` and `ASSUMPTION_RELAXATION` create separate families of ideas. In particular, a missing or inverted expected imprint is not a subsequent rescue of the original idea, but a new `INBOX` candidate with its own ID.

Creating ideas is not a gate. It requires neither a universally named forced actor nor premortem, validity self-classification, backtest, confidence, evidence grade or promotion decision. Their final state is exclusively an unscreened intake.

Each catalogue entry records its development path in `entry_origin`. Repeated observations may feed new mechanisms through stable journal references as `INTERNAL_OBSERVATION`; this does not give them a higher evidence level. The generation run is preserved as a complete candidate-universe reference.

## 4.1 Upstream hypothesis intake

A raw idea is neither evidence nor a `Candidate Hypothesis`. It is recorded as a versioned intake dataset before the Phase-0 pre-test and may be transferred to a research case only after documented screening.

For `INBOX` only stable identity, time, origin, raw idea, already used information references and the status are stored. `LLM_IDEA` and secondary sources are sources of ideas, not evidence. `MERGED` and `REJECTED` only complement the respective transition and justification.

`SCREENED` complements idea class, family of mechanisms and alternative explanations. Only `PROMOTED` additionally logs at least:

- idea class
  (`ASSOCIATIONAL_PATTERN / PREDICTIVE_PRECEDENCE / MECHANISM_CANDIDATE /
  STRUCTURAL_FLOW_CANDIDATE / RELATIVE_VALUE_CANDIDATE /
  EVENT_RESPONSE_CANDIDATE / RETURN_DECOMPOSITION_CANDIDATE / OTHER`),
- market, instrument, venue, trading phase, time zone/calendar and forecast horizon,
  - the actor status: either a named actor hypothesis with compulsion,
  expected action, observable reference and competing actor hypothesis or explicitly `UNSPECIFIED / NOT_CLAIMED`, if the question is purely associative or predictive and no actor is robustly known,
- a linked noise screen or a justified waiver allowed by policy,
- the observable footprint that distinguishes the story from mere prose,
- at least one competing declaration;
- required data, resolution, timestamp/clock sync, venue and feed coverage,
- early hurdles due to spread, fees, slippage, latency, queue position, borrow,
funding or leg-risk, as applicable;
- the detailed classification of already considered data and their information budgets,
- the mode and provenance of variable and construct selection,
- the promotion decision and next research ID.

Typical intraday candidates for an actor hypothesis are market makers under inventory risk, option desks in hedging, time-bound execution algorithms, rebalancing and margin processes, and stop clusters at technical levels. The mention remains a plausibility check and is not a proof of mechanism. If a credible actor hypothesis is missing, it must not be invented. The explicitly unknown status of actor allows an associative or predictive investigation, but does not bear any causal or mechanistic interpretation.

`PROMOTED` only means that an idea is precise and basically testable enough for phase 0. It confirms neither the mechanism nor a forecast or trading edge. Rejections and merges shall be maintained with justification; a discarded idea is not deleted and later reintroduced as a new independent idea.

## 4.1a Variable-selection provenance

Each `PROMOTED` dataset declares the selection mode as `PREDEFINED`, `DATA_DRIVEN` or `HYBRID`.

- `PREDEFINED` requires a concise technical justification and the references of
retained variables or constructs. No artificial search space is invented.
- `DATA_DRIVEN` and `HYBRID` also require the frozen
  candidate universe, all selection data and its data role, the visibility of the outcome during selection, method references, the effective number of candidates, a versioned search space and concrete controls against selection bias.

All selection data also appears in `consumed_data_refs`. A dataset that has influenced variable choice or search space is no longer an independent validation or holdout. Feature importance, SHAP/Shapley, impurity or similar procedures are optional model or association diagnoses. They are neither a duty nor proof of causal relevance.

## 4.1b Reconstruction of a strategy of prose

If an idea comes from a book, article, video or course and lacks reproducible definitions, the source interpretation is not immediately issued as a finished strategy. Before your own specification, a `strategy_reconstruction` can be created and validated against `schemas/strategy_reconstruction.schema.json`.

The artifact separates:

- the source section actually tested,
- rule, recommendation, option, example, and explicit discretion,
- the source assertions indispensable for the strategy identity,
- source-defined, alternative, open, discretionary, and contradictory constructs,
- possible definitions and their real origin,
- later conscious selection or a human protocol.

An example does not automatically become the general rule. A list of possible operationalizations is neither a selection nor a backtest, nor is it automatically a search space that has actually been studied. If discretion is removed, the result may be `SIMPLIFIED_VARIANT`, but not a tacit replication. `REPLICATION` is allowed only if the source specifies all essential constructs reproducibly. Details and an example are in `reconstruction/README.md`.

Before `RECONSTRUCTION_COMPLETE` or `DISCRETIONARY_PROTOCOL_COMPLETE`, a `strategy_concept_audit` validated against `schemas/strategy_concept_audit.schema.json` is mandatory. The `scientific-philosophy-critic` separates:

- strategy defining conditions,
- conditions of use specified by the source,
- merely suspected success modifiers,
- and unknown conditions for success.

Suspected modifiers remain candidates. Unknown conditions are not replaced by plausible prose and neither category may secretly enter the reconstruction as a mandatory filter.

The audit attributes trigger, condition, goal and outcome to common inputs, windows and deterministic calculations. Such design dependencies can create associations or alter the estimand through the definition. They are not proof of causation and are not automatically a mistake. A source-related target is not quietly replaced by a methodologically more convenient question.

Regime, state, and context filters are initially provisional measuring instruments. The proportion of their classes is not a measure of separation performance. Groups that differ in forecast outcomes can have practical information value, but prove neither a literally real hidden state nor an actor or causal mechanism.

## 4.2 Binding research scope

Before `PROMOTED`, the scope is specified narrowly enough that different designs are not mixed under the same label. For `INBOX`, the raw idea is sufficient; the full scope is required for a complete research case. At a minimum, market/instrument, venue and data feed, trading phase (`PRE_MARKET / OPENING_AUCTION / CONTINUOUS / CLOSING_AUCTION / POST_MARKET / OVERNIGHT / CROSS_SESSION / OTHER`), calendar/time zone/DST rule, clock or event time horizon, and one of the following event classes shall be specified:

- `INFORMATION_EVENT`,
- `SCHEDULED_STRUCTURAL_EVENT`,
- `CONTINUOUS_ENDOGENOUS_MECHANISM`,
- `RETURN_DECOMPOSITION`.

These classes are a design router, not a final taxonomy of market mechanisms.

The news/macro policy is exactly one of the following:

- `INCLUDED_AS_SIGNAL`,
- `NOT_USED_AS_SIGNAL`,
- `FILTER_KNOWN_EVENTS`,
- `SCHEDULED_EVENT_STUDY`.

`NOT_USED_AS_SIGNAL` does not mean that information events have been removed from the sample. `FILTER_KNOWN_EVENTS` requires named feeds, coverage, timestamps, exclusion windows, and known coverage gaps. Therefore, the unqualified claim “news-free” is inadmissible; only a statement about known events under the documented policy and feed coverage is allowed.

PEAD, CPI, FOMC or similar release studies belong to `INFORMATION_EVENT` and must not be issued as evidence of a strictly filtered, continuous intraday mechanism. Index changes, funding timestamps and auctions are planned structural events and are not combined with continuous order book mechanics. Close-to-open versus open-to-close yields are initially `RETURN_DECOMPOSITION`, not an independent news-free trading rule.

## 4.3 Three separate evidence levels

For each idea based on a suspected mechanism, three statuses are kept separately:

1. `mechanism_supported` – the mechanism is for the claimed market, actor
and period adequately documented;
2. `forward_predictive_oos` – the footprint observable at the time of decision
forecasts the predefined future outcome on independent data;
3. `executable_net_edge` – the forecast remains at executable prices after all
relevant costs, latency, fill, queue, borrow, funding and capacity effects economically positive.

Each status is independent: `UNKNOWN`, `SUPPORTED`, `NOT_SUPPORTED`, or `BLOCKED`. There is no automatic upgrade: a theory or paper on the mechanism does not set the two later stages to `SUPPORTED`; a contemporaneous relationship is not a forward forecast; and a mid-price effect is not an executable net edge.

## 4.4 Two independent axes

| Axis | Allowed values | Question answered |
|---|---|---|
| Research claim level | `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL` | What kind of distribution, intervention, or counterfactual is claimed? |
| Validation/trading status | `mechanism_supported / forward_predictive_oos / executable_net_edge`, each with its own status | What evidence exists for the mechanism, forecast, and economics? |

There is no automatic inference between the axes. An interventional effect with an existing identification gate can be `executable_net_edge = NOT_SUPPORTED` after costs. An associative, time-clear forecast, on the other hand, can have an executable net edge without identifying a causal mechanism.

---

# 5. Claim level, identification model and observability

## 5.1 Claim level

Each research version declares the strongest intended statement:

- `ASSOCIATIONAL_PREDICTIVE`: statement about observed or predicted distributions, for example `P(Y|X,C)`.
- `INTERVENTIONAL`: statement about the effect of an intervention or structurally identified shock, for example `E[Y|do(X=x)]`.
- `COUNTERFACTUAL`: statement about what would have happened in the same specific case under another intervention.

Without an explicit declaration, `ASSOCIATIONAL_PREDICTIVE` applies. A predictive edge is not devalued simply because it has no identified mechanism; its description must then remain predictive.

The claim level classifies the question, not the notation used. Neither a DAG nor potential-outcome symbols nor a specific estimator increase the claim level without a passed identification gate.

## 5.2 Causal estimand

For `INTERVENTIONAL` or `COUNTERFACTUAL`, a precise estimand is set before estimation. It shall designate at least:

- treatment, intervention or structural shock,
- outcome and horizon,
- target population or event class,
- contrast and unit,
- total, direct or mediated effect,
- and the chronological order.

The word “effect” alone is not an estimand. The `do(·)` operator must not be used for an ordinary conditional forecast.

The identification model is declared as `SCM_DAG`, `POTENTIAL_OUTCOMES`, `STRUCTURAL_ECONOMETRIC` or `OTHER_EXPLICIT`. The representations can be translated into each other for many questions, but do not have to be used together. In particular, a potential outcomes design makes explicit consistency, positivity, the design-specific assignment/exchangeability assumption and interference or exposure mapping. An additional DAG is not mandatory if the chosen design fully discloses estimand and identification assumptions.

## 5.3 Purpose and limits of the DAG

A directed acyclic graph can be used to make explicit suspected temporal and structural relationships between variables. It is a permissible formalism, but not mandatory for every identified design.

Example:

`Information set(t−) → expected shock(t−) → event shock(t) → 2Y response(t+) → equity response(t+)`

The DAG is not a proof of causality. Every arrow and every shared parent are assumptions. Where the data does not distinguish several structures, competing DAGs or an equivalence class are documented. Temporal order excludes reaction to the past, but does not eliminate latent confounders, measurement errors, selection, or simultaneity within the selected time resolution.

The DAG serves in particular to:

- distinguish confounders, colliders, mediators, and post-treatment variables,
- make unlawful adjustments visible,
- formulate competing declarations,
- derive testable implications and negative controls,
- and to check whether the desired estimand is identifiable at all.

## 5.4 Identification gate

For `INTERVENTIONAL` or `COUNTERFACTUAL`, at least:

- identification strategy, such as randomisation, natural variation, backdoor/frontdoor criterion, instrument variable, regression discontinuity, difference-in-differences or reasoned high-frequency identification,
- non-testable and testable assumptions of the strategy,
- selecting the adjustment set or the comparable design restrictions from the identification model instead of from purely predictive feature selection,
- positivity/overlap or instrument relevance, where relevant,
- possible latent confounders, selection, measurement errors and interference,
- negative controls, placebos and sensitivity analyses, where design-specific,
- and the result `PASS / FAIL / BLOCKED`.

For `ASSOCIATIONAL_PREDICTIVE` the status is `NOT_REQUIRED_PREDICTIVE`. This is not proof of identification.

Without `PASS`, no causal claim may be frozen. A continuation as predictive research requires a correspondingly declared new research version; the data already viewed retains its consumed role.

## 5.5 Causal discovery and time series

Conditional-independence, score-based, invariance and time-series procedures may constrain DAG candidates or generate hypotheses. Their output is interpreted only under the documented algorithm assumptions, for example:

- causal Markov and Faithfulness assumptions,
- causal sufficiency or explicit handling of latent variables,
- stationarity or defined environments,
- correct lag length and time resolution,
- appropriate functional shape and measurement quality,
- valid conditional-independence tests under autocorrelation.

Conditional independences are often followed by only one Markov equivalence class. Stronger orientation requires additional structural assumptions or interventions.

Granger tests answer whether the history of `X` improves the forecast of `Y` relative to a chosen set of information. They do not provide a Pearl interventional effect without additional identification assumptions and are marked as `PREDICTIVE_PRECEDENCE`.

## 5.6 Role of the LLM

An LLM may:

- formulate alternative DAGs and mechanisms,
- propose confounder, instrument and negative control candidates,
- translate assumptions into verifiable consequences,
- identify inconsistencies between the hypothesis, data timing, and estimand.

We must not:

- treat a plausible sounding arrow as empirically proven,
- derive instrument validity from literature or correlation on their own,
- re-label a causal-discovery result as a unique “true DAG”,
- confuse an estimation method with an identification strategy.

## 5.7 Observability table

For each variable, it is mandatory to record:

- name,
- calculation,
- required raw data and data vintage,
- earliest time of full availability,
- use as predictor/state/treatment/shock/mediator/outcome,
- leakage/look-ahead risk.

A signal shall only be used as a predictor in the formal test if it was fully known at the time of decision. Confounders must be determined before treatment or shock; post-treatment variables must not accidentally enter into a total effect as ordinary controls.

Retrospective pivots, retrospectively confirmed extreme points, revised macro data or profile sizes calculated after the session end must not be treated retroactively as if they were previously known.

## 5.8 DAG and identification versioning

As soon as a DAG, claim level, estimand or an identification assumption influences a design decision, the relevant version is logged.

Material changes after Freeze generate a new Research version.

## 5.9 Machine-testable constraint and lever labels

For market transmission, DAGs, alternative explanations, and quantitative response equations are used directly; an upstream ECE map is not a standard part of the path.

Anyone using one of the labels `TRANSMISSION_DIAGNOSTIC`, `INFORMATION_BOTTLENECK_CANDIDATE`, `IDENTIFIED_CAUSAL_LEVER` or `IMPLEMENTATION_CONSTRAINT` creates an artifact after `schemas/constraint_assessment.schema.json`. In particular:

- `IDENTIFIED_CAUSAL_LEVER` requires `identification = PASS`, an estimand and supporting evidence.
- `IMPLEMENTATION_CONSTRAINT` requires a validated phenomenon, a passed feasibility test, a defined system goal and a measurable bottleneck size.

After phenomenon validation, Goldratt’s focus logic can optionally help to prioritize an already occupied implementation bottleneck. It is not a market, estimation or identification method.

## 5.10 Tooling routers for causal analysis

For each research version, one of the following statuses is set:

- `TOOLING_REQUIRED`: executable code for graph verification, identification, causal estimation, refutation, or causal discovery is part of the design.
- `TOOLING_NOT_REQUIRED`: the research does not contain an executable causal core operation, for example because it remains purely associative/predictive; justification is mandatory.
- `TOOLING_BLOCKED`: a necessary library, compatible runtime or validated API is not available.

For `TOOLING_REQUIRED`, a primary library is selected for each task under `04_CAUSAL_TOOLING.md`. Specialized implementations are the default; self-written causal core algorithms are allowed only if no suitable library exists or if they serve exclusively as an independent test. The reason and additional synthetic tests are documented.

The tasks shall remain separate:

- graph and adjustment check: primary `pgmpy` or `DoWhy`,
- Model–Identify–Estimate–Refute workflow: primary `DoWhy`,
- DML/CATE after identification: `EconML` or `DoubleML`, not automatically both,
- time-series-specific discovery: `Tigramite`,
- simple binary treatment with matching/propensity: `causalinference` only as a narrow optional case.

A library may assume multiple roles, but no API output replaces domain assumptions or the identification gate. A tool or model change after Freeze is material. Before freeze, runtime, exact package versions, lockfile/environment, main classes or functions, seed, split logic, structural model/design/estimand version, adjustment set or comparable design restriction, warnings and compatibility are logged. Untested package combinations and major version changes require a smoke test on a known synthetic case.

---

# 6. Operationalization

If a source strategy is not fully operationalized, the source reconstruction from §4.1b is referenced before this phase. Section 6 then documents the specification actually selected; it must not obscure retrospectively which definition comes from the source and which was added during reconstruction.

After a preliminary operationalization, a `condition_inquiry` can be activated after `schemas/condition_inquiry.schema.json`. It answers one of five separate questions:

1. Does the measuring instrument separate future behavior according to its stated purpose, beyond what is already built into its calculation?
2. What association is induced by common inputs, windows, or deterministic construction?
3. How dependent is the finding on the operationalizations accepted in advance?
4. Under which conditions known at the decision time does the forecast or effect size change?
5. Does a discovered condition recur over time, markets, or other pre-defined environments?

The quantitative condition search is a hypothesis generator, not a covert redesign of the source strategy. A condition discovered from data receives its own condition hypothesis. It is only called recurring after independent repetition and remains separate from causal or real state claims.

Terms such as:

- Trend,
- Expansion,
- overextension,
- Buildup,
- Rejection,
- strong move,
- high pressure,
- low persistence

shall be operationalised before validation.

At least:

- variable,
- formula/calculation,
- lookback,
- session,
- timeframe,
- observation timestamp,
- outcome horizon.

Where possible, variables are first examined continuously.

Hard thresholds are only introduced later if they are justified by the form of the relationship, practical feasibility or a well-founded design purpose set in advance.

---

# 7. Target variable and null model

## 7.1 Target variable

In early research, the outcome does not already have to be a complete trade P&L.

Possible outcomes:

- forward return,
- volatility normalized forward return,
- MFE,
- MAE,
- time to event,
- probability of a reclaim,
- probability of a new extreme,
- future volatility.

## 7.2 Null model

Every hypothesis requires an explicit comparison.

Possible zero models:

- unconditional forward return,
- time-matched random timestamps,
- volatility matched non-events,
- randomized signals at the same trading frequency,
- identical exit logic with randomized entry,
- simple momentum/mean-reversion benchmark,
- matched passive market drift.

The relevant size is often rather:

\[
\Delta E = E[R\mid X] - E[R\mid Null]
\]

The relevant comparison is not just `E[R|X]` but the incremental difference from the null model.

## 7.3 Event shocks and reaction innovations

For planned publications, the market typically reacts to the new information relative to the previous information level, not to the raw value alone. Therefore, at least separately stored:

- published value including data vintage,
- market expectation available before the event and its source/timestamp,
- pre-specified surprise design and scaling,
- exact time of publication,
- pre-specified reaction window,
- simultaneously or overlappingly published messages,
- liquidity, volatility, and attention state before the event.

A typical descriptive shock variable is:

\[
S_t = \frac{A_t-E_{t^-}[A_t]}{q},
\]

where `q` is a scale predefined on development data or from external evidence. A standardized surprise is only a structural shock when the necessary identification strategy has been passed.

For asset or chain link `j`, the expected response is estimated exclusively from data allowed before the respective event:

\[
u_{j,t}=R_{j,t}-\widehat m_j(S_t,C_t;\mathcal D_{<t}),
\qquad
z_{j,t}=\frac{u_{j,t}}{\widehat\sigma_{j,t}},
\]

with controls known only before the event `C_t`. Model training, scaling, and uncertainty forecasting must be time-ordered OOS. `u` or `z` are called `REACTION_INNOVATION` or `REACTION_ANOMALY`; they are neither automatically a misjudgment nor a `CAUSAL_CHAIN_BREAK`.

In a reaction chain, shock and each chain link are measured separately. A common “chain integrity” indicator requires predefined weights, covariance treatment and multiple testing rule. Post-event mediators may be used to predict a downstream chain link, but not tacitly as controls of an alleged total effect. Direct and mediated effects require an own mediation estimand and additional identification assumptions.

At central-bank events, it is particularly important to check whether an observed surprise contains pure policy news, information about the economic outlook, risk-premium news, or several components at the same time. A narrow event window reduces external messages, but does not guarantee exogeneity.

A single surprise value is not required. If the publication contains several independent information dimensions, a small, economically interpretable factor vector `F_t` is used, for example target, path, and information components. The number, rotation, sign, orthogonalization, and interpretation of factors are fixed using development data. A data-driven factor is not automatically a structural shock.

## 7.4 Quantitative shock-response map

The standard quantitative solution for a suspected impact chain is not an automatic constraint search, but a set of measurable response equations. For asset or chain link `j` and horizon `h`, the starting point can be:

\[
R_{j,t,h}
=\alpha_{j,h}
+\beta_{j,h}^{\top}F_t
+\gamma_{j,h}^{\top}C_t
+\delta_{j,h}^{\top}(F_t\otimes C_t)
+\varepsilon_{j,t,h},
\]

where `F_t` contains the predefined surprise factors and `C_t` exclusively pre-event known states.

Methodological default:

1. For immediate market reactions, a simple high-frequency event regression.
2. For several later horizons with sufficient N separate horizon-specific regressions or local projections.
3. State dependency on few pre-reasoned continuous interactions.
4. More complex VAR/SVAR, change point, ML or common anomaly models only if they answer a specific question and provide additional OOS value compared to the simple model.

The suspected verbal chain need not be estimated as a strictly sequential regression. With almost simultaneous pricing, the asset reactions are modeled as a common response vector on `F_t`. A sequence between reactions is claimed only when time resolution and identification design carry them.

### Incremental test of a chain link

If chain link `j` is to serve as an information bottleneck, a nested comparison is set before Freeze:

```text
M0: End-Outcome ~ Surprise factors + pre-event states
M1: End-Outcome ~ Surprise factors + pre-event states + timely available innovation from chain link j
```

Only a time-stable improvement in a pre-defined loss, calibration, or net-utility measure makes `j` an `INFORMATION_BOTTLENECK_CANDIDATE`. It does not prove a causal lever.

### Allowed labels

- `TRANSMISSION_DIAGNOSTIC`: pass-through, response coefficient, or residual without a constraint claim.
- `INFORMATION_BOTTLENECK_CANDIDATE`: incremental OOS forecast value for the defined end-outcome.
- `IDENTIFIED_CAUSAL_LEVER`: interventional target identified and identification gate passed.
- `IMPLEMENTATION_CONSTRAINT`: limited net executable performance due to data, latency, liquidity, costs, or process.

The selection of the “dominant” member belongs to the research search space. If multiple links, horizons or states are compared, multiple testing and data consumption rules apply.

---

# 8. Effect size, uncertainty, and precision

## 8.1 Effect size before significance

An effect can be statistically striking and economically irrelevant.

Therefore, at least:

- point estimator,
- comparison with the zero model,
- economic relevance threshold,
- uncertainty interval,
- robust sensitivity estimation.

## 8.2 Four result states

Validation is not interpreted only as `significant / not significant`.

### A. Expected economically relevant effect precisely supported

With the previously defined uncertainty logic, the effect is clearly on the expected side of the economic relevance limit.

### B. Opposite economically relevant effect precisely supported

The original hypothesis is falsified. The result must produce a **new** hypothesis, but not save the old one.

### C. Economically irrelevant or zero effect precisely supported

The data sufficiently exclude the predefined economically relevant effect size. The hypothesis is discarded or terminated.

### D. Imprecise / undecidable

The uncertainty includes several economically different states. No result-driven parameter revision shall be carried out.

Only:

- more independent data,
- already predefined additional analysis,
- or concluded as `INCONCLUSIVE`.

## 8.3 Test bundle, error allocation and follow-up revision

A validation result never checks just an isolated sentence. It concerns a bundle of core hypothesis, auxiliary assumptions, operationalization, measurement methods, data quality, scope, model, inference and implementation. A negative or undecidable result therefore does not clearly determine which bundle is wrong without a distinguishing design. This Duhem-Quine subdetermination does not change the result state from §8.2.

After `FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE`, or `INVALID_TEST`, if a material revision is considered:

1. The frozen result and its Research ID remain unchanged.
2. The tested core and the actually needed auxiliary assumptions are recorded separately in a `scientific_philosophy_review`.
3. A clear attribution of error is allowed only with evidence that distinguishes the suspected link from alternatives.
4. A **progressive** follow-up revision generates a previously unimplied,
refutable prediction, names its falsifier, freezes an independent evaluation plan and receives a new Research ID.
5. A **degenerative** revision mainly explains away the already observed failure, restores the desired sign, or narrows the sample after the fact without new empirical content. It does not authorize a new confirmation test.
6. **Diagnostics** may locate measurement, data, or implementation problems. They are neither confirmation nor rescue of the original hypothesis.

In Lakatos's sense, a research program may be provisionally maintained despite an anomaly; this does not make the failed individual test successful. In Kuhn's sense, isolated, recurring, and program-wide anomalies, as well as available rivals, are logged. The lack of a better rival is not positive evidence for the tested hypothesis.

---

# 9. Dependence and effective sample size

Trading data is often not IID.

The following shall be checked:

- temporal autocorrelation,
- repeated signals from the same market impulse,
- event/session clusters,
- overlapping forward horizons,
- correlated symbols,
- shared macro events.

Depending on the structure:

- block bootstrap,
- cluster bootstrap,
- cluster-robust inference,
- event clustering,
- purging,
- embargo,
- symbol- or factor-based clustering.

The principle is:

> The uncertainty model must fit the actual dependency structure of the data.

If this is not possible with the available information, the analysis must not be “finished” with an incorrect IID assumption. The status is `BLOCKED` or the uncertainty is explicitly treated conservatively.

The design effect is basically defined as:

\[ DE = \frac{Var(\hat\theta\mid actual\design)}{Var(\hat\theta\mid IID\text{-reference})} \]

and can be approximately translated to `N_eff ≈ N / DE`. The known approximation `DE = 1 + (m−1)ρ` only applies to a simple exchangeable cluster structure with clusters of equal size. For unequal cluster sizes, temporal dependence, multiple cluster levels or correlated symbols, a suitable extension or simulation must be used. A default for `DE` without estimated dependency parameters is inadmissible.

---

# 10. Influence diagnostics and heavy tails

## 10.1 Influence diagnostics

Before validation, at least:

- leave-one-out or leave-one-cluster-out,
- result without dominant symbol,
- result without dominant time/event group,
- Dominance measure of the largest observation/cluster.

The specific dominance threshold is set in the freeze.

Minimum rule:

> If the sign or economic conclusion is overturned by removing a single plausible cluster, the evidence is not robustly confirmed.

## 10.2 Heavy Tails

For heavy-tailed outcomes, the following are determined before validation:

- primary location parameter,
- robust sensitivity index,
- dealing with extreme observations,
- permissibility of trimming/winsorisation,
- primary versus secondary analysis.

The estimator is not exchanged after the validation result.

---

# 11. State and Regime Research

A regime is not a metaphysical market mode, but an observable state that changes the conditional distribution of a concrete phenomenon.

The central question is:

> Which market variables observable before the outcome change the effect or risk of this phenomenon?

State variables are first examined as continuously as possible.

At least the following shall be compared, where factually appropriate:

\[
E[R\mid P]
\]

\[
E[R\mid S]
\]

\[
E[R\mid P,S]
\]

This checks whether the phenomenon provides **additional** information beyond the state.

Winners and losers are analyzed together. Winner-only regime research is unacceptable.

Transition states such as `Balance → Expansion` or `Trend → Balance` may be independently examined. `UNCLASSIFIED` is a permitted outcome of a state classifier.

For event reactions, it is additionally checked whether sensitivity, variance, or signs change with an **observable** state before the event. A “regime” name derived after the reaction is not a permitted conditioning variable. Different reactions may reflect, among other things, attention, positioning, liquidity, risk premia, competing news, or real parameter drift; a change of mechanism is only one competing hypothesis among several.

Invariance over predefined environments can support a causal mechanism or discard candidates. It replaces an identification design only under the respective model assumptions and may not be used as a universal causality test.

---

# 12. Candidate hypothesis, prediction list and pre-mortem

After discovery and basic measurement, a precise candidate hypothesis arises.

It shall contain:

- phenomenon,
- claim level `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`,
- for causal claims: estimand, identification strategy and identification status,
- for claimed effect chain: structural model/identification design version,
- for constraint language: defined final destination, permitted constraint label and decision criterion,
- expected direction,
- primary outcomes;
- relevant state, if part of the hypothesis,
- null model,
- economic effect threshold,
- falsification condition.

This is followed by two adversarial steps.

## 12.1 Prediction list

Question:

> What additional observable consequences would have to occur if the hypothesis is correct?

A good hypothesis has to do more than retell the discovery data.

## 12.1a Outcome evidence contract

Before validation is frozen, every planned outcome is recorded in a validated
`outcome_evidence_contract`. The contract assigns each outcome a fixed role,
evidence target, measurement rule, falsifier, multiplicity family, and result
consequence. It also records mechanical coupling and a separate
transportability expectation for every material evidence target.

Prediction, mechanism, phenomenon, and executable net edge remain separate
conclusions. A supported primary prediction may coexist with a contradicted
mechanism diagnostic. In that case the prediction may remain supported, but
the mechanism conclusion must follow the frozen not-supported rule. A
non-discriminating test and an invalid test remain distinct outcomes.

If the research state has reached `FROZEN_TEST` without a complete contract,
validation is blocked. The contract must not be reconstructed after validation
results have been viewed.

## 12.2 Pre-Mortem

Acceptance:

> The result looks convincing, but later proves to be false, unstable or economically useless. Why?

Risks are translated into:

- checks,
- competing hypotheses,
- guardrails,
- rejection criteria.

At least:

- Leakage,
- Selection Bias,
- latent confounders and unintentional collider conditioning,
- post-treatment controls or unidentified mediation,
- contaminated event windows or false expectation vintages,
- mixing of multiple news shocks,
- change in response due to attention, positioning, liquidity or parameter drift,
- state can only be defined after outcome,
- too large research search space,
- dominance of individual instruments/events,
- lack of independent evidence,
- underestimated costs,
- delayed live availability of variables.

---

# 13. Multiple testing and research degrees of freedom

The search space includes not only parameters, but every design decision:

- hypotheses,
- indicators,
- lookbacks,
- timeframes,
- sessions,
- symbols,
- long/short directions,
- outcomes,
- exits,
- state variables,
- filters,
- thresholds.

The number and type of variants tested is documented.

Generator runs are considered a candidate universe. If all 96 candidates of a run are screened, the pre-fixed family size is 96 and not the number of later survivors. `scripts/validate_entry_thresholds.py` calculates Bonferroni/Effective test thresholds; Benjamini-Hochberg decides only after a complete batch.

Depending on the scope, suitable procedures are chosen, for example:

- False Discovery Rate,
- White's Reality Check,
- Hansen SPA,
- Deflated Sharpe Ratio,
- Probability of Backtest Overfitting,
- Bootstrap of the entire selection pipeline.

The larger the search space, the more strictly the selection distortion must be taken into account.

## 13.1 Pipeline integrity check before freeze

The uncertainty of a selection pipeline and the technical integrity of its implementation are separate issues. Before the freeze, the complete executable pipeline must therefore be additionally checked for control data.

Required components:

- repeated zero/surrogate runs with time, cluster, state and volatility structure obtained as far as possible;
- identical feature, selection, filter, timing and evaluation steps as in real research,
- at least one synthetic known positive effect with a fixed sign and timing as a sentinel against sign, indexing and look-ahead errors,
- for `TOOLING_REQUIRED`: import/version and API smoke test and a synthetic causal test that checks at least correct direction and allowable adjustment set,
- Predefined acceptance rules for false alarm rate, effect distribution, direction and timing.

In addition, the control base and data role are logged. Pipeline tests that influence design decisions use only development data or purely synthetic data. For the estimated false alarm rate, planned and actual repeat numbers as well as target precision and Monte Carlo uncertainty are documented. `PASS` assumes that this target precision has been achieved.

A single permuted run or a single random walk is not sufficient calibration. Naive permutation is inadmissible if it destroys the dependency relevant under the zero model. The pipeline integrity gate is `PASS / FAIL / BLOCKED`; without `PASS`, the test Freeze must not be confirmed.

Machine enforcement uses a versioned
`pipeline_integrity_assessment`. It binds the controls to the exact complete
pipeline fingerprint and records model specification, parameter provenance,
seed policy, preserved and missing relevant structure, planned and actual
repeats, Monte-Carlo uncertainty, and the rule locked before the first run. A
passed control authorizes only the freeze path; it cannot support a market
effect, forward prediction, mechanism, or executable edge. The artifact must
pass `scripts/validate_pipeline_integrity_assessment.py`.

---

# 14. Test freeze

At least the following shall be frozen before formal validation:

- Research ID and version,
- Candidate Hypothesis,
- competing hypothesis,
- Claim-Level,
- causal estimand or `N/A + justification: ASSOCIATIONAL_PREDICTIVE`,
- Identification strategy, assumptions and gate status or `NOT_REQUIRED_PREDICTIVE`,
- structural model/identification design version or `N/A + justification: ASSOCIATIONAL_PREDICTIVE`,
- tooling status, primary library per task, exact runtime/package versions, main API and reproducible environment, or reasoned `TOOLING_NOT_REQUIRED`,
- observability table,
- market/instrument/session/timeframe,
- data roles,
- definition of the phenomenon,
- state variables,
- exclusions;
- primary outcome,
- secondary outcomes,
- null model,
- for event research: source of expectation/vintage, surprise formula, scaling, event window and contamination rule,
- for multidimensional events: number, construction, rotation/orthogonalization and interpretation of the surprise factors,
- for response innovations: expected response model, timing training rule, uncertainty scaling, and designation as a non-causal residual,
- for information bottleneck claim: end-outcome, chain link availability time and frozen `M0` versus `M1` OOS comparison,
- expected direction,
- economic effect threshold,
- primary estimator,
- robust sensitivity estimation,
- uncertainty method,
- dependency/cluster logic,
- effective-N method,
- Purging/Embargo rule, if necessary,
- influence diagnostics,
- heavy-tail rule,
- multiple-testing method,
- full validation plan including data split, minimum N and decision rules,
- passed formal Phase-0 recalculation,
- Pipeline integrity design and existing pipeline integrity gate,
- `TOOLING_REQUIRED`: Passed import/API/compatibility smoke test and synthetic causal sentinel,
- data split,
- minimum sample from phase 0,
- success criteria,
- rejection criteria,
- inconclusive rule,
- Warning/suspension criteria for later forward operations.

The freeze completeness gate must be `PASS` before validation begins.

Gate and phase statuses are clearly coupled: `PASS → COMPLETE`, `FAIL → FAILED`, `BLOCKED → BLOCKED`. After `FAIL` or `BLOCKED` no dependent follow-up step must begin.

---

# 15. Validation and Final Holdout

## 15.1 Validation

Validation uses data that has not affected the current Research version.

If the result is used for adjustment, the data set is used up and then Development Data.

## 15.2 Final Holdout

If the data allows it, a final holdout remains completely untouched until:

- discovery complete,
- development complete,
- candidate hypothesis frozen,
- ordinary validation is complete.

## 15.3 Nested Walk-Forward

If a large final holdout is not practical, a nested walk forward design can be used:

- internal window for development/model selection,
- external window for unseen evaluation.

For overlapping labels, purging/embargo must be taken into account accordingly.

## 15.4 Importance of OOS evidence for causal claims

OOS stability, replication and backtest profitability test prediction and action benefits. They prove neither the validity of the DAG nor the identification of an intervention effect.

In the case of a causal claim, the frozen design-specific identification diagnoses are therefore additionally evaluated, for example:

- Overlap/Positivity and Covariate Balance
- Pre-Trends and Placebos
- instrument relevance and plausibility of exclusion/independence,
- negative controls,
- sensitivity to unobserved confounding,
- alternative permitted DAGs or partial identification limits.

Double/debiased machine learning, flexible outcome models or causal forests do not replace these requirements. They estimate targets under an already established identification structure.

---

# 16. Robustness and replication

An effect is not only valued at its best point.

The following shall be checked:

- neighboring parameters,
- other time periods,
- other comparable instruments,
- different state ranges,
- different forward horizons,
- removal of dominant clusters,
- removal of dominant symbols.

We are looking for a stable area, not a historical pinprick.

Cross-symbol tests are only evaluated as additional evidence if the dependency structure allows this. Highly correlated markets are not automatically independent replications.

---

# 17. Economic feasibility and strategy engineering

A validated phenomenon is not yet a strategy.

`VALIDATED_PHENOMENON` is a permissible stand-alone end state. The status refers only to a phenomenon validated according to the frozen design. It confirms neither a causal mechanism nor a causal claim, nor an executable net edge. Strategy engineering begins only after an explicit decision to continue. If it does not continue immediately, downstream engineering, activation, and monitoring steps remain closed as `DEFERRED_AFTER_VALIDATION`; the phenomenon does not lose its validated status.

After phenomenon validation, it is checked whether it is actually tradable.

The following shall be developed:

- Setup,
- Trigger,
- Invalidation,
- Entry,
- Stop,
- Target,
- Management,
- position size,
- order type,
- Execution model.

## 17.1 Detailed cost model

Now the early phase 0 cost estimate is being replaced by a realistic model.

Costs may depend on the state:

\[
\text{Cost} = f(\text{state},\text{volatility},\text{liquidity},\text{size},\text{speed},\text{session},\text{execution})
\]

Especially critical:

- breakouts,
- news,
- volatility shocks,
- illiquid time windows,
- larger position sizes.

## 17.2 Diagnosing entry and exit separately

Where possible, the following shall be stored:

- MFE,
- MAE,
- time to MFE,
- time to MAE,
- time to stop,
- time to target,
- exit reason.

This makes it possible to distinguish between:

- a weak signal,
- a poor entry,
- an incorrect stop,
- a poor exit,
- a cost problem.

## 17.3 Prerequisite tree / transition tree

After empirical validation, prerequisite tree and transition tree can be used to structure real implementation problems and their order.

These tools do not generate additional edge evidence.

---

# 18. Full strategy to re-test out-of-sample

After defining entry, exit, stop, management and execution, the developed trading strategy must again be tested on unseen data or in a controlled forward paper test.

Good phenomenon validation does not protect against overfitting in later strategy implementation.

---

# 19 Forward OOS, Monitoring and Degradation

Paper/Live operation is again out-of-sample.

Four types of degradation shall be monitored:

## Statistical

- Expectancy,
- hit rate,
- R distribution,
- Drawdown,
- dispersion,
- loss clusters.

## Economic

- fees,
- Spread,
- Slippage,
- Funding,
- Capacity/Liquidity.

## State-related

- frequency of the validated state,
- change in its effect,
- misclassification,
- state transitions.

## Mechanism/event related, if applicable

- calibration of the expected response,
- distribution and autocorrelation of the `REACTION_INNOVATION`,
- frequency of predefined chain deviations,
- Surprise distribution and quality of expected source,
- stability and interpretability of frozen Surprise factors,
- event-window contamination,
- stability of the predefined reaction coefficients and uncertainty intervals,
- continuing incremental OOS value of an `INFORMATION_BOTTLENECK_CANDIDATE` versus `M0`.

An accumulation of large response innovations triggers diagnosis or revalidation. It is not automatically classified as a new market mechanism or tradable regime change.

## Process-related

- observability,
- trigger reproducibility,
- compliance with the rules,
- execution.

Warning, suspension and fault criteria are set before activation.

---

# 20. Research end states

A research project does not have to end in an active strategy.

Permissible conditions:

- `NO_PHENOMENON`
- `INCONCLUSIVE`
- `CANDIDATE_HYPOTHESIS`
- `IN_TEST`
- `VALIDATED_PHENOMENON`
- `ECONOMICALLY_UNTRADEABLE`
- `ACTIVE_STRATEGY_CANDIDATE`
- `ACTIVE`
- `UNDER_OBSERVATION`
- `SUSPENDED`
- `REVALIDATED`
- `REJECTED`

A falsified sign can create a new hypothesis. It does not retroactively convert the original test into a success.

---

# 21. Binding core rules

1. Phenomenon before finished strategy.
2. Explicit zero model before edge claim.
3. Phase-0 feasibility before consumption of independent validation data.
4. Minimum sample from power/precision calculation, never from the last run.
5. All predictors must be fully observable at the decision time.
6. Discovery data does not confirm their own hypothesis.
7. Every design decision consumes data.
8. Number of trades is not automatically number of independent observations.
9. Effect size and uncertainty shall be reported together.
10. Precise zero effect and imprecise result are different findings.
11. Unexpected sign produces at most a new hypothesis.
12. First, examine state variables as continuous variables as far as possible.
13. Analyze winners and losers together.
14. A regime filter is a measuring instrument: its class frequency does not validate it; its additional information value is judged by future behavior that is not already in its construction.
15. Multiple testing covers the entire research pipeline.
16. Influence diagnostics is determined before validation.
17. Heavy tail treatment is set before validation.
18. Validation data is not reused after it has influenced design decisions.
19. Costs are modeled early as a feasibility hurdle and later in detail/execution close.
20. Before freeze, the complete pipeline exists, repeated structurally faithful null controls are run, and a known-positive sentinel is passed.
21. Risk management does not create an edge.
22. A validated phenomenon is not yet a validated strategy.
23. The complete strategy again needs OOS/forward evidence.
24. Active strategies remain falsifiable.
25. Material changes create new versions.
26. Each claim is declared predictive, interventional or counterfactual.
27. Causal language requires an estimand and a passed identification gate.
28. Granger and causal discovery issues are hypothesis generators without additional assumptions, not causal evidence.
29. DML and other flexible estimators do not solve an identification problem.
30. An expected minus actual reaction is initially a reaction innovation, not a causal break.
31. Event shocks require pre-available expectations, data vintages, timestamps and contamination rules.
32. Backtest or OOS success does not retroactively validate the claimed causal mechanism.
33. Post-treatment mediators are not used as ordinary controls of a total effect.
34. Constraint/Lever labels follow the machine contract; Goldratt is at most an optional prioritization tool for occupied implementation constraints.
35. Quantitative default is the simplest measurable shock response map, not an automatic constraint score.
36. An information bottleneck requires a defined end-outcome and incremental time OOS forecast value.
37. An identified causal lever, a predictive information bottleneck and an operational implementation bottleneck are different statements.
38. Several Surprise factors, chain links, horizons and states count entirely in the research search space.
39. For executable causal analysis, the tooling router from `04_CAUSAL_TOOLING.md` is binding; suitable specialized libraries are the default.
40. A library output does not replace identification or domain assumptions and does not increase the claim level.
41. Exact runtime, package, API, seed and split information is reproducibly logged before Freeze.
42. `EconML`/`DoubleML` are only used after identification; `Tigramite`-Discovery remains a candidate generator.
43. A crude idea is screened in a versioned form before phase 0; `PROMOTED` means testable, not confirmed.
44. Mechanism evidence, forward OOS forecast and net executable edge are three separate statuses.
45. Intraday research fixes venue, trading phase, calendar, time base, feed coverage, and event class.
46. “News-free” is never claimed as a blanket condition; it is operationalized only as a documented news/macro policy with known coverage limits.
47. Mechanism families and intraday routers are not exhaustive and do not generate edge by classification.
48. A generation run generates only `INBOX` candidates; Mechanism catalogue, operator or literature source confirm neither hypothesis nor edge.
49. Before completing an incompletely defined source reconstruction, strategy-defining, source-named, suspected, and unknown conditions are separated in a concept audit.
50. Design dependence, statistical dependence, prognostic benefit
and causal mechanism are four different statements.
51. A success condition found in data is a new hypothesis and not a subsequently discovered source rule.
52. Predictive separation by a state filter does not prove a real hidden state, actor, or mechanism.

---

# 22. Binding pipeline

```text
G. OPTIONAL IDEA GENERATION FROM MECHANISM CATALOG → INBOX
0. HYPOTHESIS INTAKE + SCOPE + SCREENING
0a. IF SOURCE STRATEGY: RECONSTRUCTION + CONCEPT AUDIT
1. Preliminary observation / outcome scale
2. PHASE-0 PRELIMINARY SCREEN
3. Discovery / case catalogue + optional effect-cause-effect map
4. Claim level + explicit identification model + observability + tooling router
5. Operationalization
5a. OPTIONAL: QUANTITATIVE CONDITION INQUIRY
6. Target variable + null model + where applicable surprise factors/shock-response map
7. Effect size + uncertainty
8. Dependence + effective N
9. State/regime analysis
10. Candidate Hypothesis
11. Prediction list + pre-mortem
12. Multiple-testing/influence/heavy-tail plan
13. FORMAL PHASE-0 RECALCULATION + VALIDATION PLAN
14. PIPELINE INTEGRITY GATE
15. FREEZE
16. Independent validation
17. Final holdout or outer walk-forward
18. Robustness / replication
19. Economic feasibility
20. Strategy engineering
21. Complete strategy retested OOS
22. Forward OOS
23. Monitoring / degradation
24. Revalidate / suspend / reject
```

No AI agent must silently skip a step. Non-applicable steps must be marked as `N/A` with justification.
