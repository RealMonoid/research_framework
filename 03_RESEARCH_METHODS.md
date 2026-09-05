# 03_RESEARCH_METHODS.md

**Version:** 1.9 **As of:** 2026-08-31 **Status:** DRAFT FOR USE **Purpose:** Method selection for AI agents. This document does not say that every method must always be applied. It prevents necessary methods from being forgotten or treated as decorative.

---

# 1. Usage rule

For each relevant group of methods, the agent must document in the research artifact:

1. `APPLY`, `N/A + justification`, or `BLOCKED + missing information`,
2. why,
3. which specific variant,
4. which assumptions the method requires,
5. which decision can follow from the result.

A method must not just be mentioned.

Once the method is implemented as an executable causal work step, the library and reproducibility router from `04_CAUSAL_TOOLING.md` also applies. A suitable specialist library is the default; its output remains tied to the assumptions and claim limits documented here.

---

# 2. Phase-0 Power and Sampling

## Apply where:

- a primary effect is to be formally validated,
- a holdout is scarce,
- a minimum sample is required;
- the economically relevant effect quantity can be defined in advance.

## Not sufficient

`We have 20 cases` or `the latest CSV contains 15 pairs`.

## Required inputs

- `δ_econ`,
- `δ_plan` or direct precision target,
- explicit null/alternative hypothesis or interval decision rule,
- target power or precision target,
- error level/decision rule,
- exploratory scatter point estimator including source and uncertainty,
- conservative planning dispersion or stress scenario,
- test/estimate type,
- dependency assumption.

## Dispersion planning

A single point estimator from small, selected or heavy-tailed discovery data must not be used unchecked as true planning dispersion.

At least:

1. **Basic scenario** – best possible objectively justified dispersion estimation,
2. **Stress scenario** – conservative, but still plausible planning dispersion.

Possible bases are external or pooled references, an upper uncertainty limit calculated under valid model assumptions, robust scale measures with a justified stress surcharge or a predefined scenario calculation. An upper limit is to be preferred only if its distribution assumptions fit the data.

The selection rule for the stress scenario is fixed before the calculation. For multiple pre-eligible and factually transferable candidates, the gate uses the most conservative value or full bandwidth. A robust scale measure may only be used after explicit mapping of the primary estimator sample distribution, if necessary by design-specific simulation.

`δ_econ` is the economic limit; `δ_plan` is an assumed true effect for planning. For example, if later success requires `lower interval bound > δ_econ`, this rule must be simulated or planned via a suitable precision target. A power calculation for `0` versus `δ_econ` does not answer this stricter question.

The source and justification of `δ_plan` are mandatory. A discovery point estimator is not adopted unchecked; selection bias and uncertainty are taken into account by conservative scenarios, shrinkage or external references.

## Working Defaults for Classical Tests

If there is no objectively better, well-founded decision rule set in advance:

- `α = 0.05`, two-sided,
- `Power = 80%` as minimum working default,
- in the case of a tight final holdout or high cost of false negative results `90 %` or a direct precision target.

One-sided tests, lower power or other error weightings must be justified before the result is known. These values are governance defaults, not a universal statement of sufficient evidence.

## Possible procedures

- analytical power calculation for simple tests,
- Monte Carlo simulation,
- cluster-based simulation,
- Bootstrap-based precision planning.

## Decision

- current independent information is sufficient in the conservative scenario for the respective gate purpose → `CONTINUE`,
- testable in principle, but too little information → `OBTAIN_DATA`,
- economically/statistically unreasonable → `ABORT`.

Phase 0 is performed as an early pre-examination and formal recalculation after determining outcome, zero model, dependency, effective N and validation plan. Only the formal recalculation must open the way to freeze.

---

# 3. Effective sample size

## Problem

Nominal `N` overestimates evidence in autocorrelation, clustering and correlated symbols.

## Testing

- autocorrelation of outcomes/signals,
- signals per session/event,
- joint macro events,
- correlation structure of the symbols,
- overlapping forward windows.

## Possible outputs

- effective N,
- number of independent clusters,
- conservative range,
- Design Effect.

## Rule

If a serious effective N estimate is not possible, `nominal N` must not be reported as an independent evidence count.

For gates, report the method/simulation, point estimator, conservative lower bound and independent cluster count. What matters is the conservative lower limit. The order of planning shall be:

`required N_eff/cluster count → design-specific DE or simulation → required nominal N`, rounded up each time.

## Design Effect

General form:

\[ DE = \frac{Var(\hat\theta\mid actual\design)}{Var(\hat\theta\mid IID\text{-reference})}, \qquad N {eff} \approx \frac{N}{DE} \]

Only in the case of a simple exchangeable cluster structure with clusters of equal size may approximate use be made:

\[
DE = 1 + (m-1)\rho
\]

with average cluster size `m` and intracluster correlation `ρ`. For unequal cluster sizes, temporal dependence, multiple cluster levels or correlated symbols, a suitable extension or simulation is required. An unfounded default for `DE` is inadmissible.

For fewer than 30 plausibly independent clusters, set `SMALL_CLUSTER_WARNING`. This is not an automatic FAIL; however, a small-sample method, design-specific simulation/calibration, or `BLOCKED` is required.

In the stress scenario, `DE < 1` or `N_eff > N` is only taken into account if the information gain is robustly supported by external, transferable evidence and a predefined model; otherwise, at least `DE = 1` applies to the planning.

---

# 4. Block-Bootstrap

## Apply where:

- there is temporal dependence within contiguous market periods;
- individual trades must not be independently resampled.

## Idea

Sample time blocks instead of individual observations.

## Design questions

- block length,
- fixed or variable blocks,
- session boundaries,
- intraday versus multi-day structure.

## Risk

Too-short blocks destroy dependency; blocks that are too long provide few effective resampling units.

---

# 5. Cluster bootstrap / cluster-robust inference

## Apply where:

Observations meaningfully belong together in groups, for example:

- trading day,
- session,
- macro event,
- impulse cluster,
- symbol group.

## Rule

The cluster unit must be defined **before validation** or derived from a clear data structure.

An agent may not choose the cluster unit that produces the most favorable interval according to the result.

For `SMALL_CLUSTER_WARNING`, an ordinary cluster bootstrap or asymptotic cluster interval may not be considered reliable by its name alone. Cluster sizes, leverage, number and balance of the clusters as well as the concrete interval construction must be taken into account in a design-matching simulation or small sample correction. The warning does not automatically mean that each interval is too narrow.

---

# 6. Purging and embargo

## Apply where:

- labels/outcomes are defined via time windows,
- Forward horizons overlap,
- Train and test observations could include common future price sections.

## Purging

Remove observations whose label/outcome period exceeds the train/test limit.

## Embargo

Additional temporal safety zone around the separation point.

## Requirement

The agent must check whether the outcomes used overlap in time. `N/A` is only allowed with justification.

---

# 7. Correlation between Symbols

## Problem

Multiple symbols can reflect the same risk factor or macro event.

## Testing

- return correlation,
- signal correlation,
- outcome correlation,
- shared underlyings/factors,
- simultaneous event clusters.

## Practical treatment

- Underlying/factor clustering;
- separate symbol reports,
- result without dominant symbol,
- do not simply add correlated symbols to the evidence count.

---

# 8. Influence diagnostics

## Required diagnostics

At minimum:

- leave-one-out,
- leave-one-cluster-out,
- without a dominant symbol,
- no dominant period/event group.

## Additional measures

Depending on the model:

- Cook's distance,
- leverage-like dimensions,
- share of sum of squares/dispersion,
- contribution to total return,
- contribution to the point estimator.

## Binding minimum decision

If the economic conclusion or the sign of removing a single plausible cluster tips, the evidence is not robustly confirmed.

Further numerical thresholds must be specified project-specifically in the freeze.

---

# 9. Heavy-tail outcomes and robust location parameters

## Problem

Trading outcomes can be heavy-tailed. An average can depend greatly on a few extreme values.

## Predefine before validation

- primary location parameter,
- robust sensitivity index;
- outlier handling,
- transformation rules.

## Possible estimators

- arithmetic mean,
- median,
- trimmed mean,
- winsorized mean,
- robust M-estimators.

## Interpretation recommendation

If economic expectancy is the object, the mean value can remain primary. Then, however, it must additionally be checked how sensitive it is to extreme values.

A robust estimator must not be chosen only after the primary result looks unfavorable.

---

# 10. Uncertainty intervals

## Objective

Report more than point values alone.

## Possible procedures

- classic confidence interval with suitable assumptions,
- bootstrap interval,
- block/cluster bootstrap interval,
- cluster-robust interval,
- Bayesian posterior interval if the entire design is designed for it.

## Selection rule

The method must match data dependency and outcome distribution.

In the case of `SMALL_CLUSTER_WARNING`, it must also be documented how the coverage or error rate for the specific design is calibrated or why the analysis was classified as `BLOCKED`.

---

# 11. Economic relevance instead of only testing zero

## Core idea

The relevant comparison is often not:

`Effect > 0?`

but:

`Effect > δ_econ?`

Or in the case of two-sided questions:

`|Effect| > δ_econ?`

## Four interpretations

1. clearly economically relevant in the expected direction,
2. clearly economically relevant in the opposite direction,
3. clearly economically irrelevant,
4. imprecise.

These four states must already be defined in the freeze.

---

# 12. False Discovery Rate (FDR)

## Apply where:

many hypotheses are tested in parallel and the expected share of false discoveries is to be controlled.

## Suitable for

- many state variables,
- many features,
- several parallel hypothesis families.

## Not sufficient if:

Only the best trading backtest should be assessed from a highly adaptive strategy selection. For this, reality-check-/SPA-/PBO-like procedures are often closer to the problem.

---

# 13. White's Reality Check

## Apply where:

Many strategies/models have been tested against a benchmark and should be judged whether the best historical winner performs more than would be expected through data snooping.

## Important

The actually tested strategy family must be mapped as completely as possible. Including only the surviving models underestimates the search space.

---

# 14. Hansen SPA

## Apply where:

Several models can be compared against a benchmark and White's Reality Check could be too conservative or insensitive.

## Objective

Assess the candidate family's Superior Predictive Ability versus the benchmark.

---

# 15. Deflated Sharpe Ratio

## Apply where:

- Sharpe Ratio is the central selection indicator,
- many variants were tested,
- returns are not normal,
- the best backtest was selected.

## Purpose

Reduce naive Sharpe optimism caused by selection distortion and distribution problems.

## Not to be used as

sole edge validation. DSR does not replace a sound OOS design.

---

# 16. Probability of Backtest Overfitting (PBO)

## Apply where:

Many strategy variants exist and it should be checked how often in-sample winners disappoint out-of-sample.

## Interpretation

PBO quantifies selection risk, not market causality.

---

# 17. Pipeline integrity and selection testing

## 17.1 Pipeline Negative Controls Before Freeze

### Purpose

Check whether implementation errors, leakage, incorrect timing, sign errors, index shifts or an adaptive selection pipeline generate apparent evidence even without real effect.

### Required design

- The **complete** feature, selection, filter, timing and evaluation pipeline is executed.
- Zero/surrogate data shall contain the time, cluster, state and volatility structure relevant under the zero model as far as methodologically possible.
- The check is repeated often enough to assess false alarm rate and zero effect distribution with meaningful Monte Carlo uncertainty.
- At least one synthetic known positive effect with fixed sign and timing serves as a sentinel against sign, indexing and look-ahead errors.
- Acceptance rules for false alarms, effect distribution, direction and timing are defined in advance.

The control base and data role are logged. Design-influencing tests use only development data or purely synthetic data. In advance, target precision of the false alarm rate and planned `B` are defined; subsequently, actual `B` and Monte Carlo standard error or a binomial interval are reported. `PASS` presupposes the achieved target precision.

Naive label shuffling is inadmissible if it destroys relevant time or cluster dependency. A volatility-adjusted random walk can be a control, but alone proves neither correct calibration nor freedom from error. A single control run is not enough.

### Decision

- checks within the predefined tolerances and sentinels correctly detected → `PASS`,
- false alarms, false sign/timing or unexplained pipeline effects → `FAIL`,
- no structurally valid control can be constructed → `BLOCKED`.

Without `PASS` no freeze.

Status mapping: `Gate PASS → Phase COMPLETE`, `Gate FAIL → Phase FAILED`, `Gate BLOCKED → Phase BLOCKED`.

## 17.2 Bootstrap of the entire research pipeline

### Apply where:

The objective is to estimate not only the uncertainty of a fixed model, but also the uncertainty of the **selection process**.

### Pipeline

```text
Resample the data
→ test candidates again
→ select the winner again
→ measure winner performance
```

Instead of just:

```text
Resample the fixed winner
```

### Benefit

Shows how much the final result depends on the fact that this sample just created this winner.

---

# 18. Holdout versus Nested Walk-Forward

## Prefer a Final Holdout

- sufficient data is available,
- a truly untouched block can be reserved,
- Strategy development can be completed before the final test.

## Prefer Nested Walk-Forward if

- the market is non-steady-state;
- ongoing re-calibration is part of the design,
- a big final holdout would be too expensive.

## Rule

External test windows shall not be used to optimise the internal model.

## 18.1 Historical data roles under instability

### Apply where:

- a study uses a long history to make a current trading decision;
- the signal, costs, execution environment or investable universe may have changed over time; or
- historical stress periods are material to the strategy's risk or economic interpretation.

### Required design distinction

Before model or window selection, state separately:

1. which structurally comparable period estimates current gross and net performance, including the applicable cost, capacity and execution assumptions;
2. which older segments test historical existence, regime coverage, stress exposure or a proposed economic mechanism; and
3. how any rolling, expanding or time-weighted window family will be selected with time-ordered development data rather than the external test window.

A long history can reduce estimation uncertainty and expose rare loss states, but it does not by itself establish current profitability. A short recent sample can be more comparable to current execution, but it can leave crisis and tail estimates imprecise. If a detected or economically documented break motivates different windows or weights, record the affected claim and the remaining non-comparability; a break test is not proof of a named market regime or a sufficient reason to discard all earlier data.

Do not preset a universal number of years, decay half-life, weighting scheme or post-break cutoff. Treat a choice among alternative window or weighting rules as part of the model-selection family and preserve it for the applicable multiplicity and out-of-sample assessment. See C25 in `references/INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md` and §19 for state or regime measurement.

---

# 19. State/regime analysis

## Continuous testing

Before setting categories such as `Trend`, `Range`, `High Vol`, examine:

- functional relationship,
- monotonicity,
- plateaus,
- U-shapes,
- transition regions.

## Discretion thereafter if

- operationally necessary,
- justified by the relationship,
- not just for P&L maximization.

## Incremental-information test

Do not merely inspect `E[R|P,S]`; test whether `P` provides information beyond `S`.

## 19.1 Filter as a measuring instrument, not as market proof

A regime, state or context filter operationalizes a division. It does not prove that the market has a literally real hidden state with the given name. The assessment shall record:

- the exact purpose of the filter,
- its input data and its observation time;
- future targets that are not already in its calculation,
- a comparison with the continuous input variables or a simple
rule without filter,
- and the claim that is actually affected in the absence of separation performance.

The share `Range`, `Trend` or any other class is neither a good nor a bad sign in itself. The decisive factor is whether the fixed classification for its declared purpose provides additional information about later behavior. Even then, the result remains predictive; it identifies neither actor nor mechanism.

## 19.2 Design dependencies

Triggers, filters, target and outcome are attributed to common raw inputs, calculation windows and deterministic transformations. Mathematical coupling can create associations if two variables have common components. Deterministically derived variables can be represented as separate nodes in a DAG. The diagnosis only answers where a statistical link can partly come from; it is neither causal nor automatic refutation.

Suitable tools:

- structural dependency map before data analysis,
- neutral or structure-faithful simulation to test whether the construction alone
  makes the expected association visible,
- separate interpretation of the remaining empirical portion.

Methodological anchors:

- Archie, *Mathematic coupling of data: a common source of error*,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC1345065/>.
- Tennant et al., *Depicting deterministic variables within directed acyclic
  graphs*, <https://academic.oup.com/aje/article/194/2/469/7698093>.

## 19.3 Sensitivity to acceptable definitions

If several definitions have been accepted as permissible in advance, a specification curve or multiverse analysis can show whether the statement about these translations remains stable. The process discovers no true definition and no unknown premise. It shows which operationalization decisions carry the result.

- Simonsohn, Simmons and Nelson, *Specification Curve Analysis*
  <https://www.nature.com/articles/s41562-020-0912-z>.
- Steegen et al., *Increasing Transparency Through a Multiverse Analysis*,
  <https://stat.columbia.edu/~gelman/research/published/multiverse_published.pdf>.

## 19.4 Interpretable condition generation

If plausible state variables are present, but their interactions or thresholds are unknown, discovery may purposefully generate new condition hypotheses. Preference is given first to interpretable methods:

- model-based recursive partitioning: checks for which variable or model
  parameter becomes unstable, partitions there and repeats this within the emerging groups;
- Conditional inference trees: reduce the known preference of
variables with many possible separation points;
- generalized random forests only as a complement when there are many candidates and
  sufficient cases. Without identified treatment, their results are called predictive, not causal.

A data-based generated split or threshold is a new `PERFORMANCE_MODIFIER`, not a subsequently found source rule.

Methodological anchors:

- Zeileis, Hothorn and Hornik, *Model-based Recursive Partitioning*,
  <https://www.zeileis.org/papers/Zeileis%2BHothorn%2BHornik-2008.pdf>.
- Hothorn, Hornik and Zeileis, *Unbiased Recursive Partitioning*,
  <https://www.zeileis.org/papers/Hothorn%2BHornik%2BZeileis-2006.pdf>.
- Athey, Tibshirani and Wager, *Generalized Random Forests*,
  <https://www.gsb.stanford.edu/faculty-research/publications/generalized-random-forests>.

## 19.5 Conditional predictive ability and recurrence

The practical question is not only which variant was better on average, but whether information available at the time of the decision showed when the forecast performance changed. A test of conditional prognostic ability is suitable for this purpose. Subsequent fluctuation analysis looks at the entire time path of relative performance and prevents an overall average from obscuring temporal instability.

- Giacomini and White, *Tests of Conditional Predictive Ability*
  <https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0262.2006.00718.x>.
- Giacomini and Rossi, *Forecast Comparisons in Unstable Environments*,
  <https://onlinelibrary.wiley.com/doi/10.1002/jae.1177>.

Invariance over predefined markets, instruments or session environments can support the recurrence of a context. It is not called a universal causality test without the necessary identification assumptions.

## 19.6 Negative controls and necessary conditions

Negative controls can reveal a suspected or unexpected source of distortion if exposure or outcomes should not respond under the claimed mechanism. They are diagnostics and do not alone create a condition for success.

- Lipsitch, Tchetgen Tchetgen and Cohen, *Negative Controls: A Tool for
  Detecting Confounding and Bias in Observational Studies*,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/>.

Necessary Condition Analysis can be used to explore a condition without which a high outcome does not occur. Because “without X does not guarantee success” in noisy short-term markets is a particularly strong statement, it is not a default. It needs its own justification and is not issued from an empty corner in the scatter diagram alone as a market law.

- Dul, *Necessary Condition Analysis*,
  <https://repub.eur.nl/pub/90024/>.

---

# 20. Cost modeling

## Phase 0

Conservative gross cost hurdle for economic feasibility.

The margin of safety shall be documented as an additional amount or as a clearly identified overall threshold. A multiplier must distinguish between `total hurdle = M × cost` and `safety margin = M × cost`; there is no universal multiplier.

## Strategy Engineering

Detailed model, where applicable:

\[
\text{Cost}=f(\text{state},\text{volatility},\text{liquidity},\text{size},\text{speed},\text{session},\text{execution})
\]

## Special checks

- breakouts,
- news,
- fast markets,
- illiquid time windows,
- market orders,
- larger size.

A fixed slippage model is only allowed if the data shows or makes the application plausible that state dependency is negligible.

---

# 21. Prerequisite tree / transition tree

## Apply when

After empirical phenomenon validation, when real implementation problems have to be structured.

A brief effect-cause-effect map may already be used in Discovery as an optional hypothesis generator; the rules in Section 25.10 apply. Prerequisite and transition trees, on the other hand, remain tools for real implementation bottlenecks after phenomenon validation.

## Prerequisite Tree

Question:

> Which obstacles prevent an executable strategy and which intermediate objectives are necessary?

## Transition tree

Question:

> What specific sequence of actions leads from the validated idea to the verified implementation?

## Not to be used for

Proof of a market edge.

Even a correctly identified implementation constraint does not prove a market mechanism. It only shows what limits the feasibility of the already validated idea.

---

# 22. Evaporating Cloud

## Optionally apply if

there is a real conflict of aims, for example:

- Previous entry versus confirmed entry,
- strict filter versus sufficient trade frequency.

## Purpose

Make assumptions behind the conflict visible and generate new testable hypotheses.

## Not to be used as

Evidence of the resulting solution.

---

# 23. Prediction list

## Duty before freeze

Each candidate hypothesis should produce additional consequences.

Example structure:

```text
If H is true,
Y should occur alongside the discovery pattern,
especially under state Z,
but not under control condition C.
```

The more independent the consequence of the discovery observation is, the more informative is its failure or existence.

---

# 24. Pre-Mortem

## Duty before freeze

Acceptance:

> The research result is later revealed to be false or useless.

Then collect reasons and translate any relevant reason into:

- Check,
- Guardrail,
- counter-hypothesis,
- rejection criterion.

A pre-mortem without operational consequence is only pessimism with table format.

---

# 25. Causal claims, event shocks and reaction innovations

## 25.1 Claim router

Before each method selection, the question is classified:

The router classifies the destination query, not the formalism. Graphical SCMs/DAGs, potential outcomes, and structural econometric designs are permitted explicit representations; none is itself a proof or a higher claim level.

### `ASSOCIATIONAL_PREDICTIVE`

The goal is a conditional distribution, forecast, or tradable decision under observed conditions. A causal estimand is not required. The identification gate is `NOT_REQUIRED_PREDICTIVE`; causal language and `do(·)` remain inadmissible.

### `INTERVENTIONAL`

The aim is the effect of an intervention or a shock identified as structural. Treatment/shock, outcome, population, horizon, contrast and total/direct/mediation effect must be determined before the estimate.

### `COUNTERFACTUAL`

The aim is to make a statement about the same specific case under a non-existent intervention. This level requires an explicit structural model and usually stronger assumptions than an average intervention effect.

A research project may have two separate targets, such as an identified average event effect and a predictive trading signal. Their evidence and final decisions are reported separately.

## 25.2 Explicit identification model and gate

### Mandatory order for causal claims

1. Define the causal estimand.
2. Formulate an SCM/DAG, potential-outcomes design, structural econometric, or
   other explicit identification model.
3. Document every edge, every omitted common parent, or—in a potential-outcomes
   design—consistency, positivity, assignment/exchangeability, and interference
   or exposure mapping as assumptions.
4. Derive the identification strategy and permitted adjustment set or comparable
   design restriction from the model.
5. Establish testable implications, negative controls, placebos and sensitivities.
6. Only then choose a suitable estimator.

This sequence is not only documented, but enforced by a separate test step. Before effect estimation or causal formulation, the `causal-identification-critic` creates a `causal_identification_assessment`. The main agent may only accept `E7 PASS` from a schematically and semantically tested assessment. For an explicitly predictive question, the result is `NOT_REQUIRED_PREDICTIVE`; it is not interpreted as a causality test.

The financial market-specific test base is versioned in `references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md`. It complements the general method standard in particular by factor model misspecification and systematic event timing in financial event studies, pre-information and information shocks in high-frequency identification, simultaneous price/order flow determination as well as feedback, spillovers and time-dependent treatment.

For an actually required graph and adjustment check, `pgmpy` or `DoWhy` are primarily used. A DAG is not additionally mandatory if a potential-outcomes or other explicit design identifies the estimand under fully documented assumptions. The model accepted by the tool is still an input assumption; a successful API query does not confirm the truth of the model.

Observational data and conditional independence structures often identify only one equivalence class without additional assumptions. Additional orientation can come from interventions, time restrictions, non-Gaussian/additive structure assumptions or invariance over environments. These assumptions are not replaced by good forecast quality.

### Gate

- Estimand can be identified from documented structural model and design-specific assumptions/diagnoses completely → `PASS`.
- Predictive question → `NOT_REQUIRED_PREDICTIVE`.
- Claimed causal effect under approved models not identifiable or core assumption refuted → `FAIL`.
- necessary information or a diagnosis is missing → `BLOCKED`.

`FAIL` or `BLOCKED` prohibits the causal claim. A new predictive version is allowed to further examine the relationship without re-imposing the existing data as independent.

## 25.3 Granger, conditional independence, and causal discovery

### Granger

Granger analysis checks whether the history of `X` improves the forecast of `Y` relative to a defined information set. The result label is `PREDICTIVE_PRECEDENCE`.

At least:

- information set,
- lag selection,
- stationarity/stability treatment,
- autocorrelation and innovation diagnostics,
- simultaneity within the time resolution,
- multiple testing,
- possible common unobserved drivers.

A positive outcome is neither a valid intervention nor an exclusion of confounding.

### Causal Discovery

PC/FCI, score-based, additive-noise, invariance and PCMCI-type procedures may generate candidates or exclude edges. The agent documents algorithm-specifically:

- causal Markov/Faithfulness assumptions,
- causal sufficiency or modelling of latent confounders,
- stationarity or definition of environments,
- time resolution and maximum lags,
- functional form,
- quality and power of conditional independence tests,
- measurement error and selection mechanism,
- output equivalence class or unoriented edges.

PCMCI+ is developed, for example, for lagged and contemporaneous relationships in autocorrelated time series, but its basic consistency statement is valid under the assumptions made in the procedure and not as a universal proof of truth.

For PCMCI/PCMCI+-type analyses, `Tigramite` is the primary specialized implementation. The conditional-independence test, `tau_max`, link assumptions, handling of latent confounders, significance/multiplicity rule, and output graph status are logged. The result remains `CAUSAL_HYPOTHESIS` until the identification gate has independently passed.

## 25.4 Double/debiased machine learning

DML reduces regularization and overfitting bias when estimating low-dimensional target parameters through Neyman orthogonal scores and cross-fitting. It does not identify the target parameter itself.

Before DML must therefore be determined:

- causal estimand,
- the assumption of identification, for example unconfoundedness or a valid IV structure,
- the permitted covariate set,
- overlap/positivity or instrument relevance,
- the dependency and split logic.

Standard theory must not be transferred unchecked with random IID cross-fitting to autocorrelated market time series. Temporal blocks, purging/embargo, cluster structure and a matching inference or simulation are required.

A high DML estimate for unexplained confounding remains a precisely estimated value under unexplained assumptions, not a repaired causal claim.

For implementation, a primary library is selected for each estimand: `EconML` for CATE/causal forest or flexible DML tasks, `DoubleML` for a DML design covered by its formal model classes. Using both in parallel is useful only as a pre-defined replication. `DoWhy` can orchestrate identification and refutation; the specific DoWhy–EconML version combination must be tested separately because of possible API incompatibilities. The `causalinference` package is intended only for its narrow binary matching/propensity/weighting range and is not the general DML default.

## 25.5 High-frequency event design

### Surprise instead of raw value

For planned release `A_t`, the new information is defined relative to the expectation available before the event:

\[
S_t=\frac{A_t-E_{t^-}[A_t]}{q}.
\]

If a publication contains several information dimensions, `S_t` is replaced by a small factor vector `F_t`. In FOMC events, for example, high-frequency studies show that a single target factor is not sufficient and a path factor is additionally required. This does not justify a universal two-factor default: factor number, input contracts, rotation, orthogonalization, signs and economic interpretation are specified for the event class using development data.

Required fields:

- official release time and time zone,
- real-time vintage of the published value,
- expectation source, sample, aggregation rule and timestamp,
- pre-specified scaling `q`,
- exact price sources and synchronization,
- primary and secondary event window,
- overlapping publications and other news,
- rules for defaults, revisions, illiquidity, and outliers.

A narrow time window improves temporal isolation, but does not guarantee exogeneity or a single structural shock. If the measured surprise is predictable from pre-event information, the consequence for exogeneity must be documented and, if necessary, a pre-defined orthogonalization checked.

Central-bank events shall consider at least the following competing components:

- pure policy surprise,
- information on the economic outlook,
- risk-premium or communication shock,
- concurrent external news.

A sign breakdown of multiple asset reactions is itself an identification strategy with assumptions and is not treated as an observed truth.

## 25.6 Expected reaction versus actual reaction

For each asset or chain link `j`, use a model trained only on time-eligible data. With several surprise factors and pre-event states, the general form is:

\[
\widehat R_{j,t,h}=\widehat m_{j,h}(F_t,C_t,F_t\otimes C_t;\mathcal D_{<t}),
\]

\[
u_{j,t,h}=R_{j,t,h}-\widehat R_{j,t,h},
\qquad
z_{j,t,h}=\frac{u_{j,t,h}}{\widehat\sigma_{j,t,h}}.
\]

`C_t` contains only states known before the event. `\widehat\sigma_{j,t}` comes from a frozen, OOS-calibrated uncertainty model. If `Expected − Actual` is used instead, only the sign changes; the convention is set before freeze.

### Minimum diagnostics

- OOS calibration of mean and forecast intervals,
- Distribution, heavy tails and autocorrelation of `u`/`z`,
- sensitivity to event windows and pre-event states according to the freeze,
- concurrent news and liquidity controls;
- Leave-one-event/leave-one-cluster-out,
- Multiple testing across assets, chain links, horizons and states.

For a vector of chain links, define a common anomaly measure in advance if needed:

\[
Q_t=u_t^\top\widehat\Sigma_t^{-1}u_t.
\]

Weights, regularization of `\widehat\Sigma_t`, the reference distribution, and thresholds are frozen on development data. Selecting a conspicuous chain link after the fact is multiple testing.

A common anomaly measure is optional and not the default. Often, separate, interpretable response equations with pre-defined horizons are sufficient. For immediate reactions, high-frequency event regressions are preferred; local projections are a possible extension for several later horizons. VAR/SVAR, change-point, or ML models require a specific supplementary question and demonstrated incremental OOS benefit.

### Permitted interpretation

A large `|z|` or `Q` initially means:

- poor calibration,
- unusual reaction,
- omitted message or state variable,
- liquidity/positioning effect,
- parameter drift,
- or, only as a further possibility, an altered mechanism.

The permitted label is `REACTION_INNOVATION` or `REACTION_ANOMALY`. `CAUSAL_CHAIN_BREAK` is only allowed for an identified chain/mediation model and passed predefined test.

## 25.7 Mediation and post-treatment variables

For a chain such as

`Shock → 2Y yield → dollar/equity`

The intermediate reactions are post-treatment mediators. For the total effect of the shock on equity, do not control for them as if they were ordinary pre-treatment confounders. Anyone who wants to separate direct and mediated effects must define a mediation estimand and document the additional assumptions, especially mediator–outcome confounding.

For pure prediction, an already observed intermediate reaction may be used to predict a later chain link. The resulting signal remains predictive unless a separate mediation design is specified.

## 25.8 Validation, backtest and monitoring

### Separate decisions

1. **Identification:** Is the claimed causal parameter identified under the established assumptions?
2. **Estimate:** How large is it, and how uncertain is it?
3. **Prediction:** Is the response to genuinely new data calibrated and stable?
4. **Trading:** Does the reaction innovation deliver incremental net performance after costs?

A backtest can support point 4 and OOS forecasts can support point 3. Neither can decide point 1 retroactively.

Monitor the live surprise distribution, model calibration, `u`/`z`, event contamination, and response coefficients. Exceeding pre-defined thresholds triggers diagnosis, revalidation, or suspension; the system does not identify the cause automatically.

## 25.9 Role of an LLM

### Permitted

- Collect candidates for mechanisms, DAGs, confounders, instruments and negative controls
- formulate alternative explanations and falsifications,
- explain assumptions,
- structure literature and data documentation,
- check code and pipeline consistency.

### Inadmissible

- confirm arrows based on linguistic plausibility,
- claim instrument exclusion or unconfoundedness because it sounds “reasonable”,
- treat a discovery process as an oracle,
- output p-values, backtests or DML as a substitute for identification,
- automatically declare an unusual reaction to be a tradable regime or causal break.

## 25.10 Constraint and Lever labels

For market transmission, DAGs, alternative explanations, surprise factors, and response equations are the direct standard path. There is no upstream Goldratt/ECE obligation.

The four permitted labels are stored in `schemas/constraint_assessment.schema.json`:

- `TRANSMISSION_DIAGNOSTIC`: descriptive pass-through or residual finding.
- `INFORMATION_BOTTLENECK_CANDIDATE`: timely observable innovation with pre-frozen incremental OOS value.
- `IDENTIFIED_CAUSAL_LEVER`: intervention/mediation estimand and identification gate passed.
- `IMPLEMENTATION_CONSTRAINT`: demonstrated data, timing, liquidity, cost, or process bottleneck after phenomenon validation and feasibility testing.

A large coefficient, an unusual residual, or an OOS forecast is not sufficient for a causal or constraint status. If a simple M0/M1 comparison does not confirm the additional information, reject the link.

Goldratt’s focus logic may be used only after phenomenon validation, and only optionally to prioritize several already established `IMPLEMENTATION_CONSTRAINT` candidates. It produces no label, estimand, or gate status.

## 25.11 Scientific basis

Primary sources for the limits and procedures used in this section:

- Judea Pearl et al., *Probabilistic and Causal Inference: The Works of Judea Pearl* – causal hierarchy, DAGs and identification per do-calculus: <https://ftp.cs.ucla.edu/pub/stat_ser/ACMBook-published-2022.pdf>
- Guido Imbens (2020), *Potential Outcome and Directed Acyclic Graph Approaches to Causality: Relevance for Empirical Practice in Economics* – Comparison and Translatability of the Two Causal Traditions: <https://www.nber.org/papers/w26104>
- Dominik Janzing, Lenon Minorics and Patrick Blöbaum (2020), *Feature Relevance Quantification in Explainable AI: A Causal Problem* – Limitations of purely observation-based feature relevance for causal statements: <https://proceedings.mlr.press/v108/janzing20a.html>
- C. W. J. Granger (1969), *Investigating Causal Relations by Econometric Models and Cross-spectral Methods*: <https://doi.org/10.2307/1912791>
- Jonas Peters et al. (2014), *Causal Discovery with Continuous Additive Noise Models* – Identification only under additional structure: <https://jmlr.org/papers/v15/peters14a.html>
- Jonas Peters, Peter Bühlmann and Nicolai Meinshausen, *Causal inference using invariant prediction*: <https://arxiv.org/abs/1501.01332>
- Jakob Runge (2020), *Discovering contemporaneous and lagged causal relations in autocorrelated nonlinear time series datasets* – PCMCI+: <https://proceedings.mlr.press/v124/runge20a.html>
- Victor Chernozhukov et al. (2018), *Double/debiased machine learning for treatment and structural parameters*: <https://academic.oup.com/ectj/article/21/1/C1/5056401>
- DoWhy User Guide – Modeling, Identification, Estimation and Refutation: <https://www.pywhy.org/dowhy/v0.14/user_guide/>
- pgmpy Causal Identification Guide – Identification and verification of adjustment sets: <https://pgmpy.org/guides/causal_identification.html>
- EconML Documentation – DML and CATE estimators: <https://econml.azurewebsites.net/>
- DoubleML User Guide – orthogonal scores, cross-fitting and supported designs: <https://docs.doubleml.org/stable/guide/guide.html>
- Tigramite Documentation – PCMCI/PCMCI+ and time series specific conditional independence tests: <https://jakobrunge.github.io/tigramite/>
- Causalinference Documentation – narrow range of functions for Propensity, Matching, Blocking, Weighting and Least Squares: <https://causalinferenceinpython.org/>
- John Cochrane and Monika Piazzesi (2002), *The Fed and Interest Rates – A High-Frequency Identification*: <https://www.aeaweb.org/articles?id=10.1257/000282802320189069>
- Roberto Rigobon and Brian Sack (2002), *The Impact of Monetary Policy on Asset Prices* – Endogenity and Identification via Heteroscedasticity: <https://www.federalreserve.gov/econres/feds/the-impact-of-monetary-policy-on-asset-prices.htm>
- Marek Jarociński and Peter Karadi (2020), *Deconstructing Monetary Policy Surprises—The Role of Information Shocks*: <https://www.aeaweb.org/articles?id=10.1257%2Fmac.20180090>
- Michael Bauer and Eric Swanson (2022/2023), *A Reassessment of Monetary Policy Surprises and High-Frequency Identification* – Predictability from pre-event information: <https://www.nber.org/papers/w29939>
- T. Niklas Kroner (2025), *How Markets Process Macro News: The Importance of Investor Attention* – time-variable CPI response strength: <https://www.federalreserve.gov/econres/feds/how-markets-process-macro-news-the-importance-of-investor-attention.htm>
- Refet Gürkaynak, Brian Sack and Eric Swanson (2004/2005), *Do Actions Speak Louder Than Words?* – Target and Path factors instead of a one-dimensional FOMC shock: <https://www.federalreserve.gov/econres/feds/do-actions-speak-louder-than-words-the-response-of-asset-prices-to-monetary-policy-actions-and-statements.htm>
- Torben Andersen, Tim Bollerslev, Francis Diebold and Clara Vega (2006), *Real-Time Price Discovery in Global Stock, Bond and Foreign Exchange Markets* – standardized news and dynamic cross-asset response equations: <https://www.federalreserve.gov/econres/ifdp/real-time-price-discovery-in-global-stock-bond-and-foreign-exchange-markets.htm>
- Linda Goldberg and Christian Grisse (2013), *Time Variation in Asset Price Responses to Macro Announcements* – state- and time-dependent reaction coefficients: <https://www.nber.org/papers/w19523>
- Òscar Jordà (2005), *Estimation and Inference of Impulse Responses by Local Projections* – horizon-specific impulse responses as a robust alternative to fully specified VARs: <https://www.aeaweb.org/articles?id=10.1257%2F0002828053828518>
- James Stock and Mark Watson (2018), *Identification and Estimation of Dynamic Causal Effects in Macroeconomics Using External Instruments* – Relevance and Exogenity Conditions for Structural Dynamic Effects: <https://www.nber.org/papers/w24216>

These sources do not justify a specific trading edge. They justify the methodological barriers and the obligation to check identification, forecasting and trading benefits separately.

---

# 25a. Mechanism-based idea generation

This section is only activated if you want to create new intraday or short swing ideas. It is not part of the downstream screening.

The executable producer under `scripts/generate_hypotheses.py` reads `generation/mechanism_catalog.v1.json`. Each catalogue entry contains mechanism history, possible actors or rules, expected actions, observable signatures, natural phases, alternative observables, contradiction hypotheses, connection tags, primary sources and an explicit `entry_origin`. Internal observations may only extend the catalogue through stable observational or journal references.

The basic grammar is:

```text
Mechanism × phase × observable response → unscreened INBOX candidate
```

From the same source, different candidates are generated:

- `PHASE_PATH`: anticipation, active phase, absorption, transmission,
  exhaustion, or unwind,
- `EXPECTATION_VIOLATION`: the expected imprint is absent or reverses;
  this creates a separate hypothesis about absorption, a competing flow, another
  transfer path, or a state change,
- `MECHANISM_CONNECTION`: two mechanisms share a clock, venue, flow, hedge path,
  or payoff,
- `ASSUMPTION_RELAXATION`: the imprint is shifted from price direction to depth,
  spread, basis, volume, volatility, timing, or a linked instrument.

The actor question is a productive route, but not a general admission condition. It is particularly suitable for rolls, auctions, expiration, benchmarking, hedging, funding and liquidations. Order book states, instrument links and clock-time repetitions may be generated without a clearly identified forced actor.

This method does not include portfolio allocation, long-term factor ideas, a
premortem, validity labels, rejection statistics, a noise screen, a backtest,
ranking, or promotion. This separation is recorded in
`decisions/ADR-006-mechanism-first-hypothesis-generator.md`.

However, the generator run is the candidate-universe reference for later
screens. The downstream entry screen counts each idea actually tested against
data and uses the pre-fixed correction from the search-space register; this does
not make the screen a generator operator.

---

# 26. Intraday hypothesis router

## 26.1 Scope boundary

The router assigns raw ideas to a suitable first test design. It is not a
complete list of all intraday mechanisms and is not evidence that the assigned
story is true or tradable. Every idea starts with `ASSOCIATIONAL_PREDICTIVE`
unless its own identification design justifies a higher claim level.

Before each detailed analysis, three questions are separated:

1. Is the claimed mechanism sufficiently supported in the specific market?
2. Does its ex ante observable footprint predict a future outcome OOS?
3. Does this effect remain positive at executable prices after costs?

The answers are independently listed as `mechanism_supported`, `forward_predictive_oos` and `executable_net_edge`. A positive result at an earlier stage does not set a later stage to `SUPPORTED`.

## 26.2 Router-Matrix

| Idea family | Admissible initial claim | Minimum data and integrity | Typical artifacts / alternative explanations | Minimum falsification | Early feasibility hurdle |
|---|---|---|---|---|---|
| Limit order book / OFI / queue imbalance | A pre-defined book state improves the forecast of a future quote or execution outcome; no automatic causal or edge claim | Exact instrument and venue; event feed with trades, adds, cancels, and sequence checks; book depth; tick size; timestamp and clock synchronization; documented trade signing; known hidden-liquidity limits | Current price response rather than forward effect; mechanical tick change; time of day, volatility, depth; feed gaps; cross-venue liquidity | Event time and clock time separately; incremental value over depth, spread, volatility, and time of day; new data; executable bid/ask outcomes rather than mid-quotes alone | Feed resolution and latency must be shorter than the effect; queue/fill model, fees, spread, and slippage must not consume `δ_econ` |
| Spread widening | First, a volatility or liquidity-risk forecast; direction only with an additional ex-ante signal | Tick-accurate quotes, book depth, cancels, trades, venue rules, and time of day | A move from 1 to 2 ticks appears as “doubling”; volatility, low activity, queue depletion, inventory, or adverse selection are not identifiable from spread alone | Absolute ticks and relative change separately; matching/controls; incremental OOS value; no direction from spread alone | The wider spread is itself part of the cost hurdle |
| Cross-market / lead-lag | Market A improves the rolling OOS forecast of the future efficient price of B | Direct, synchronized quotes; clock audit; contract/instrument mapping; futures basis, dividends, interest rate, and maturity; session overlap | Stale/asynchronous quotes, common factor, bid-ask bounce, feed or venue latency; time-varying lead direction | A-versus-B and B-versus-A; rolling information share/VECM or simpler OOS benchmarks; regime and placebo tests | Executable basis deviation after two spreads, fees, latency, queue, and leg risk |
| Execution / meta-order signature | Public data allow at most a calibrated meta-order probability; no safely detected TWAP/VWAP | Trades and quotes across relevant venues; order marks; inter-arrival times; sizes; participation rate; daily volume curve; order/participant IDs as far as possible | Round lots, batching, icebergs, fragmentation, multiple actors, adaptive/randomized algorithms | Classification against a null model that receives time of day, volume curve, and size frequency; then a separate OOS return test | Without identifiers, the mechanism remains latent; an alleged “floor” must be proven separately by executable, cost-adjusted returns |
| Relative value / pairs / cointegration | A pre-formed spread has stable conditional mean reversion OOS; industry similarity alone is not enough | Point-in-time universe; corporate-action-adjusted synchronous quotes; integration characteristics; estimated hedge coefficient; borrow/short data | Mere correlation; unstable beta; common factor; earnings/corporate actions; structural breaks; data snooping across many pairs | Strictly separate formation and trading; unit-root/cointegration/error-correction diagnostics; break tests; pair-selection multiplicity; factor exposure OOS | Two-legged fills, leg risk, spread/slippage, borrow, capacity, and residual factor risk must be included in `δ_econ` |
| Derivatives hedging / gamma | Conditional on the sign and size of a documented or robustly estimated intermediary exposure; no universal momentum direction | Option chain, Greeks/volatility surface, underlying/futures, OI/volume, multiple dealer-side assumptions, event filters | Open interest does not identify the dealer side; long gamma can dampen and short gamma can amplify; trend may be cause rather than hedge consequence | Sign-symmetric predictions; sensitivity to dealer-side assumptions; long- versus short-gamma days; filter earnings/macro/index events | The result must not rely on an unobservable position assumption; hedge instrument and costs must be feasible |
| Rebalancing / benchmark or fixed-mix flow | Only for documented mandates, index rules, or holdings; no general legal obligation | Versioned benchmark/prospectus rule; announcement and effective date separately; weight difference; tracking AUM/holdings; auction imbalance | Anticipation, active funds, other corporate events, cash inflows, derivatives, deviating tracking methods | Matched controls; expected-flow cross-section; announcement versus effective window; reversal/stock effect separated | Timing, available auction liquidity, impact, borrow, and anticipation can eliminate the edge |
| Session / opening or closing auction | Venue-specific change in liquidity, imbalance, or price distribution; no universal “power hour” pattern | Versioned venue calendar, auction type, imbalance publication times, time zone/DST/holidays; continuous and auction periods separately | Simultaneous high volume and wide spreads; hard-coded local times; regulatory changes; closing print not guaranteed executable | Venue- and regime-specific null models; auction/continuous separately; momentum and reversion as competing directions | Order type, cutoffs, imbalance access, fill/impact, and actual auction price |
| Crypto funding | Change in funding, basis, OI, or volume around a contract-specific timestamp; no automatic directional spot-return claim | Venue, contract, rule version, exact funding timestamp, ex-ante visible rate, spot/perpetual quotes, OI/liquidations | Intervals are not universally eight hours; finalized rate may contain leakage; liquidations or news may drive both sizes | Basis/OI/volume outcomes primary, spot return secondary; rate direction and magnitude; placebo timestamps; rule changes | Fees, funding, basis, slippage, margin, liquidation, and venue risk |
| Planned information event | Surprise/response claim according to §25.5; belongs to `INFORMATION_EVENT` | Release time, point-in-time expectation/vintage, event feed, contamination rule | Raw value instead of surprise; multiple news dimensions; external messages | Freeze the surprise model and windows; placebos/controls; time-ordered OOS | Do not classify it as a “news-free” intraday mechanism |
| Endogenous price/volume event | Conditional prediction based on an observable trigger; not automatically an exogenous event shock | Trigger confirmation time, full path dependency, pre-trigger states, executable quotes | Selection on outcome, look-ahead, volatility state, stop cascades falsely attributed to the trigger | Matched non-events, randomized or true-trigger placebos, purged OOS test | Trigger must be determined live in time; cost and crowd/impact risk |
| Overnight versus intraday | First, a return decomposition, not a mechanism or edge | Official and executable open/close definition, corporate actions, calendar, financing/borrow | Earnings, macro, and other overnight news; non-negotiable official print; sample-dependent mean values | Subperiods/markets, costs, and gap risk; a separate mechanism hypothesis is required | It does not fit a pure continuous intraday scope and does not carry a news-free rule by itself |

## 26.3 Data integrity at very short horizons

For order book and lead lag ideas, a positive statistical test is inadmissible as long as at least one of the following points is materially unexplained:

- direct venue data versus a consolidated view,
- sequence gaps, drop/recovery behavior and book reconstruction,
- Exchange, feed, capture and strategy clock including synchronization errors,
- Trade signing rule and treatment of cancels/corrections,
- Tick-size, lot-size, auction or matching rule version,
- Hidden/Iceberg liquidity and unobserved venues,
- queue position, order type, fill and cancel latency,
- and the difference between observed mid-quote and executable price.

If the resolution necessary for the claimed horizon is missing, mark the idea
`REJECTED` or `BLOCKED` at intake; do not proceed with coarser data.

## 26.4 Rules of interpretation for typical exaggerations

- An OFI or multi-level OFI regression to the concurrent midprice change
is `mechanism_supported` evidence or measurement diagnostics, not a 5–60 second forecast.
- “Spread doubled” is not a universal information shock: a move from one to
  two ticks is simply a one-tick change and provides no direction without an
  additional signal.
- Futures do not lead ETFs by definition; leadership and strength must be
  estimated and can reverse with period, liquidity, or volatility.
- Recurring print sizes or distances do not identify a specific algorithm or
  price floor.
- The same industry, high synchronization, or a 2–3 sigma distance proves
  neither cointegration nor market neutrality.
- Dealer hedging can increase net-gamma-driven movement or counteract positive
  exposure; the position is usually known only through proxies.
- Index or fixed-mix flows rely on concrete rules and mandates, not a universal
  legal obligation at the closing price.
- Funding intervals, auction times, and sessions must be loaded from versioned
  venue rules rather than hard-coded as universal times.

## 26.5 Primary Sources as Methodological Anchors

The following works establish individual mechanisms or test limits, but not a finished trading edge:

- Cont, Kukanov and Stoikov, *The Price Impact of Order Book Events*,
<https://doi.org/10.1093/jjfinec/nbt003> – OFI and current short-term price changes.
- Chen, Chung and Lien, *Price Discovery in the S&P 500 Index Derivatives
Markets*, <https://doi.org/10.1016/j.iref.2016.07.008> – time/state dependent pricing contributions instead of universal leadership.
- van Kervel and Menkveld, *High-Frequency Trading around Large Institutional
Orders*, <https://doi.org/10.1111/jofi.12759> – Reactions to parent orders are dynamic and not synonymous with a fixed price bottom.
- Engle and Granger, *Co-Integration and Error Correction*,
<https://doi.org/10.2307/1913236> – Definition and testing of cointegration.
- Do and Faff, Are Pairs Trading Profits Robust to Trading Costs?*,
<https://doi.org/10.1111/j.1475-6803.2012.01317.x> – Cost and period dependence of historical pair findings.
- Baltussen et al., *Hedging Demand and Market Intraday Momentum*,
<https://doi.org/10.1016/j.jfineco.2021.04.029> – conditional role of short-gamma hedging.
- Parker, Schoar and Sun, *Retail Financial Innovation and Stock Market Dynamics:
  The Case of Target Date Funds*,
  <https://doi.org/10.1111/jofi.13258> – rebalancing of identified target-date
  funds rather than blanket pension-fund assumptions.
- Wu and Jegadeesh, *Closing Auctions: Nasdaq versus NYSE*,
<https://doi.org/10.1016/j.jfineco.2021.12.003> – venue- and design-specific closing auction findings.

Each research version records the actual version of this or another source in
addition to the Academic Source protocol. This list does not replace source or
version/integrity verification.

---

# 27. Method matrix for AI agents

| Problem | Minimum test | Typical method |
|---|---|---|
| Too little data | Phase-0 power/precision | Power calculation/simulation |
| Serial dependence | Autocorrelation/cluster | Block bootstrap |
| Shared events | Event cluster | Cluster bootstrap |
| Overlapping labels | Check time windows | Purging/embargo |
| Correlated symbols | Correlations/factors | Symbol/factor clusters |
| Heavy tails | Influence/distribution | Robust estimator + sensitivity |
| Single dominant cases | LOO/LOCO | Influence diagnostics |
| Many hypotheses | Document the search space | FDR |
| Many strategies versus a benchmark | Model family | Reality Check / SPA |
| Selected high Sharpe | Selection bias | Deflated Sharpe |
| Many backtest variants | IS/OOS range instability | PBO |
| Uncertain selection process | Complete pipeline | Pipeline bootstrap |
|Pipeline finds effects below zero / possible timing or indexing error|Complete pipeline on true-to-structure zero/surrogate data plus known positive sentinels|Pipeline integrity gate|
| Scarce independent data | Data roles | Holdout or nested WF |
| Costs vary with signal | State test | Conditional cost model |
| Unclear value of a regime filter | Future target not included in the filter + incremental comparison | Measurement assessment + conditional predictive ability |
| Triggers and outcomes share inputs or windows | Deterministic provenance map | Structural dependency map + optional neutral simulation |
| Result may depend on acceptable definitions | Pre-limited definition family | Specification curve / multiverse |
| Unknown observable success modifiers | Interpretable discovery, then separate return check | Model-based recursive partitioning / conditional inference tree |
| Condition may be temporary | Full time path rather than overall average | Performance fluctuation test |
| Condition should apply across the market | Pre-defined environments and limited interpretation | Invariance analysis |
| Causal claim | Estimand + DAG + identification assumptions | Identification gate before estimator selection |
| Granger-/Discovery-Signal |Information set + Algorithm assumptions + Equivalence class|`Tigramite` for PCMCI-like time series discovery; label as hypothesis generator/predictive precision|
|high-dimensional confounders under valid identification|Overlap + Split/Dependency Design|`EconML` or `DoubleML` with valid cross-fitting|
|DAG/adjustment test| versionierter Graph + Estimand |`pgmpy` or `DoWhy`; Tool result does not confirm DAG truth|
|Refutation of an identified estimator|design-specific placebos/negative controls/sensitivities|`DoWhy` plus at least one independent design-specific examination|
| Planned macro event | Expectation vintage + release time + event window + external news | Surprise/high-frequency event design |
| Event contains several news dimensions | Pre-determine factor number/rotation/interpretation | Small surprise-factor vector instead of raw value |
| Actual reaction deviates | OOS calibration + news/liquidity controls | Standardized `REACTION_INNOVATION` |
| Several chain links are conspicuous | Covariance + pre-defined weights + multiplicity | Common `Q` score and link-specific diagnostics |
| Direct/mediated effect claimed | Post-treatment roles + mediator–outcome confounding | Explicit mediation estimand |
| Multi-link verbal chain of action | End outcome + measurable/latent nodes + alternative paths | Competing DAGs and response equations |
| Claimed information bottleneck | Real availability + frozen M0/M1 OOS comparison | `INFORMATION_BOTTLENECK_CANDIDATE` or discard |
| Strategy fails feasibility | System objective + demonstrated data/timing/cost bottleneck | `IMPLEMENTATION_CONSTRAINT` + prerequisite/transition tree |

---

# 28. Closing rule

The agent must not consider any method “done” just because its name appears in the report.

A method is only completed when documented:

- why it fits,
- how it was parameterized,
- which assumptions apply,
- what the result is,
- and what decision will follow.

The research pipeline itself is considered executable only when the pipeline
integrity gate is `PASS` before freeze.
