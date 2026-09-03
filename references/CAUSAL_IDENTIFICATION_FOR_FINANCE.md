# Causal identification in quantitative finance

**Version:** 1.0

**As of:** 2026-08-31

**Purpose:** Binding research basis for the `causal-identification-critic`.

## Core message

A statistical method can estimate an effect only within a design that has
already identified what is being compared. The method cannot decide by itself
whether an observed difference was caused by the claimed intervention, a
common piece of news, simultaneous reactions, selection, a misspecified return
model, or another unobserved influence.

For financial data, four questions are therefore kept separate:

1. **Identification:** What comparison represents the claimed intervention,
   and under which assumptions?
2. **Estimation:** How large is the identified effect, and how uncertain is it
   once temporal, market-wide, and event-related dependence are accounted for?
3. **Prediction:** Does the information improve forecasts for genuinely later,
   previously unknown observations?
4. **Tradeability:** Was the information observable in time and usable after
   costs and execution constraints?

## What the critic must apply from quantitative research

| Research design | Clarify before causal wording |
|---|---|
| Financial event study | Counterfactual return model, systematic event timing, volatility, horizon, other events, and dependence. Classical abnormal returns can produce a spurious effect when the factor model is wrong. |
| High-frequency identification | Exact release time, leakage, other news in the window, construction of the surprise, predictability from advance information, possible information shocks, separability of effects, and dominance of the intended shock. A narrow window helps, but is not a complete identification argument. |
| Order flow and price effect | Simultaneity, reverse causality, common information inflow, measurement order, and an exogenous source of variation or structural model. |
| Difference-in-differences and dynamic event study | Anticipation, parallel trends, staggered or repeated treatment, feedback, time-varying effects, spillovers, and cluster-robust time-aware uncertainty. An inconspicuous pre-trend test does not prove the assumption. |
| Instrumental variables | Relevance, exclusion of other pathways, independence, monotonicity where required, and the actual local effect. |
| Synthetic control | Credible donors, good pre-event fit, no contamination or spillover, suitable placebos, and sensitivity to the donor set and period. |
| Backdoor/control design | Completeness of relevant pre-treatment confounders, overlap, no colliders or post-treatment variables, and robustness to unobserved confounders. |
| DML, causal forests, and local projections | These methods can model flexibly or dynamically. Identification assumptions must come from a separate argument; the estimator does not create them. Time series require suitable splits and dependence corrections. |
| Causal discovery | Assumptions about lags, stationarity, latent confounders, measurement error, and conditional independence. The result remains a candidate graph or an equivalence class. |
| Mathematically coupled variables | Common windows, raw inputs, denominators, thresholds, and deterministic transformations. These can create a statistical relationship or change the estimand; they are neither automatically an error nor causal evidence. |

## Primary sources and their binding lessons

- Judea Pearl (2009/2010), *The Foundations of Causal Inference*: causal
  conclusions require causal assumptions that are not fully testable from the
  observed distribution. <https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf>
- Charles Kahn and Toni Whited (2018), *Identification Is Not Causality, and
  Vice Versa*: exogenous variation and an economic model answer different parts
  of a causal question; an effect does not automatically identify the
  mechanism. <https://academic.oup.com/rcfs/article/7/1/1/4590088>
- Victor Chernozhukov et al. (2018), *Double/Debiased Machine Learning for
  Treatment and Structural Parameters*: DML protects estimation against
  regularization error under assumed identification; it does not create that
  identification. <https://www.nber.org/papers/w23564>
- John Cochrane and Monika Piazzesi (2002), *The Fed and Interest Rates – A
  High-Frequency Identification*: an early design for identifying a monetary
  surprise with a narrow time window. <https://www.nber.org/papers/w8839>
- Michael Bauer and Eric Swanson (2023), *A Reassessment of Monetary Policy
  Surprises and High-Frequency Identification*: advance information can predict
  supposed surprises; orthogonalization and information channels must be
  checked. <https://www.nber.org/papers/w29939>
- Francesco Bianchi, Sydney Ludvigson and Sai Ma (revised 2026), *A Structural
  Approach to High-Frequency Identification of Monetary Non-Neutrality*:
  high-frequency signals receive an economic interpretation only within a
  structural model. <https://www.nber.org/papers/w30072>
- Alessandro Casini and Adam McCloskey (preprint 2024, revised 2025),
  *Identification and Estimation of Causal Effects in High-Frequency Event
  Studies*: a narrow time window is not enough. Causal interpretation also
  requires, among other things, separability and relative exogeneity so that
  the intended shock dominates the remaining shocks in the window.
  <https://arxiv.org/abs/2406.15667>
- Paul Goldsmith-Pinkham and Tianshu Lyu (preprint 2025), *Causal Inference in
  Financial Event Studies*: factor-model misspecification can make classic
  event-study estimators inconsistent, especially for longer, volatile, or
  systematic scheduled events; replicating portfolios and quasi-experimental
  designs are possible alternatives. <https://arxiv.org/abs/2511.15123>
- Jonathan B. Cohn, Travis L. Johnson and Zack Liu (JFE 2026), *Past is
  Prologue: Inference from the Cross Section of Returns Around an Event*: an
  event relationship should be tested against the same relationship on
  pre-event days because confounding events can produce plausible sham results.
  <https://www.sciencedirect.com/science/article/pii/S0304405X26000498>
- Òscar Jordà (2005), *Estimation and Inference of Impulse Responses by Local
  Projections*: local projections estimate dynamic responses; identification of
  the shock is an upstream task. <https://www.aeaweb.org/articles?id=10.1257%2F0002828053828518>
- Jonathan Roth (2022), *Pretest with Caution*: pre-trend tests can have low
  power, and selecting a specification after a pass can distort inference.
  <https://www.aeaweb.org/articles?id=10.1257%2Faeri.20210236>
- Ashesh Rambachan and Jonathan Roth (2023), *A More Credible Approach to
  Parallel Trends*: sensitivity analysis and partial identification make clear
  how strongly results depend on allowable violations of parallel trends.
  <https://www.aeaweb.org/articles?id=10.1257%2Frestud.20220186>
- Alberto Abadie (2021), *Using Synthetic Controls*: the donor pool,
  pre-period fit, no-interference assumption, and placebos are central design
  components. <https://www.aeaweb.org/articles?id=10.1257%2Fjel.20191450>
- Wang Miao, Xu Shi and Eric Tchetgen Tchetgen (2020), *A Confounding Bridge
  Approach for Double Negative Control Inference*: negative controls help only
  under explicit assumptions and are not an automatic all-clear.
  <https://academic.oup.com/jrsssb/article/82/2/521/7056052>
- Jakob Runge et al. (2019), *Inferring causation from time series in Earth
  system sciences*: time-series causal discovery requires assumptions about
  dependence, lags, and confounding; it does not replace an external
  identification design. <https://www.nature.com/articles/s41467-019-10105-3>

Preprints and recent works are marked as such. They complement the established
identification rules but do not replace them. None of these sources proves a
concrete trading edge.
