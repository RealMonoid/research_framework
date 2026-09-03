# 04_CAUSAL_TOOLING.md

**Version:** 1.1 **As of:** 2026-08-31 **Status:** BINDING **Purpose:** Binding router for specialized Python libraries with explicit identification, optional DAG checking, causal estimation, refutation, and time-series-specific causal discovery.

---

# 1. Basic rule

This document only regulates the tools **after** the content identification check. For `INTERVENTIONAL` or `COUNTERFACTUAL`, a validated `causal_identification_assessment` conforming to `schemas/causal_identification_assessment.schema.json` must be available beforehand. A library run cannot replace this mandatory artifact. The binding financial market-specific research basis is in `references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md`.

Once a causal method is executed as code, the agent uses a suitable specialized library, provided a well-maintained and design-friendly implementation is available. Causal core algorithms are not rewritten ad hoc.

Exceptions are only allowed if:

- no suitable library supports the required method,
- a small self-implementation serves exclusively as an independent control test,
- or a published replication requires exactly the original implementation.

In each exceptional case, reason, tests and deviations are documented.

The status per Research version is:

- `TOOLING_REQUIRED`,
- `TOOLING_NOT_REQUIRED + justification`,
- or `TOOLING_BLOCKED + missing runtime/library/API/compatibility`.

A tooling blocker does not automatically terminate purely descriptive discovery. However, it blocks any dependent causal freeze or estimation step.

---

# 2. What Libraries Don't Do

A library can perform the logical and numerical operations correctly. It cannot guarantee from market observations alone that:

- that the supplied DAG is true,
- that no relevant latent confounder is missing,
- an instrument meets the exclusion restriction;
- positivity/overlap is given,
- an event surprise is exogenous,
- a found edge remains stable over regimes,
- or the estimated effect is tradable.

A successful API result does not increase the claim level. `ASSOCIATIONAL_PREDICTIVE`, `INTERVENTIONAL` and `COUNTERFACTUAL` are assigned exclusively to `01_RESEARCH_STANDARD.md`.

The choice of library does not decide on formalism either. Depending on the question, the identification model can be formulated as SCM/DAG, potential outcomes design, structural econometric or other explicit model. Graph libraries are only mandatory if a core graphics operation is actually part of the design.

For this work, no in-house LLM has to be trained. `EconML`, `DoubleML`, and similar procedures can fit research nuisance or effect models; this is normal statistical model estimation, not training of a language model.

---

# 3. Binding library router

| Task | Primary default | Suitable for | Not as |
|---|---|---|---|
| Model–identify–estimate–refute | `DoWhy` | explicit graph, identification, estimation, placebos, refuters, and sensitivity | Oracle for DAG truth or identification assumptions |
| DAG, d-separation, and adjustment test | `pgmpy` | Backdoor/frontdoor checks, adjustment sets, and graphical or probabilistic queries | Automatic truth search from any market time series |
| CATE, causal forest, or flexible DML estimate | `EconML` | Heterogeneous effects and ML nuisance models after identification | Replacement for unconfoundedness, IV validity, or temporal split logic |
| DML in supported formal designs | `DoubleML` | Orthogonal scores and cross-fitting for supported PLR/IRM/IV/DID/RDD classes | Universal causal estimator or IID justification for time series |
| Time-series causal discovery | `Tigramite` | PCMCI/PCMCI+, LPCMCI, and suitable conditional-independence tests | A “true DAG” without algorithm assumptions |
| Simple binary treatment | `causalinference` | Overlap, propensity, trimming, matching, blocking, weighting, and least squares | Standard for DML, time-series discovery, or general graphical identification |

`causalinference` here denotes the separate Python package. It should not be confused with `pgmpy.inference.CausalInference`.

A primary library is set for each task. Two libraries for the same step are only useful if the second run is defined in advance as independent replication or compatibility control.

---

# 4. Selection by research question

## 4.1 Purely predictive reaction innovation

Example: A temporal OOS estimated model predicts the 2Y or Nasdaq response to a CPI shock; the residual serves as `REACTION_INNOVATION`.

Causal tooling: `TOOLING_NOT_REQUIRED` unless a causal effect or DAG claim is estimated. An ordinary statistical/ML library is sufficient. Reaction innovation remains predictive.

## 4.2 Identified average effect

1. Estimand and explicit identification model.
2. For SCM/DAG designs, check the adjustment set and identification strategy
   with `DoWhy` or `pgmpy`; for potential outcomes or other designs, log the
   design-specific identification conditions and diagnoses.
3. Choose the simplest design-specific estimator.
4. Perform estimation and refutation with `DoWhy` or a design-specific library.
5. Provide at least an independent diagnosis, such as alternative permitted adjustment, negative control, placebo or sensitivity analysis.

## 4.3 Heterogeneous effects or high-dimensional controls

1. Identification must already exist.
2. Choose `EconML` **or** `DoubleML` according to the estimand and supported design.
3. Set overlap, effect modifiers, nuisance-model specification, and split logic before freeze.
4. For market time series, do not use random IID folds if they violate temporal or cluster dependency; use external temporal/cluster splits, as long as the selected API supports this correctly.
5. CATE/Policy results require their own multiplicity and OOS rules.

## 4.4 DAG test without effect estimation

`pgmpy` is the default for d-separation, graphical structure, adjustment-set validation, and causal queries on an assumed model. `DoWhy` makes sense if the graph goes directly into a complete identification and refutation workflow.

## 4.5 Causal discovery in time series

`Tigramite` is the default for PCMCI/PCMCI+-type tasks. At least the following shall be frozen before the run:

- variables and time resolution;
- `tau_min`/`tau_max`,
- conditional-independence test,
- link assumptions,
- stationarity/regime logic,
- treatment of latent confounders,
- significance and multiple-testing rule,
- as well as the permitted output as a candidate graph or equivalence class.

The result label remains `CAUSAL_HYPOTHESIS` as long as no additional identification strategy exists.

## 4.6 Matching/Propensity in binary treatment

`causalinference` may be used if its narrow range of functions fits exactly and the current Python/NumPy/SciPy compatibility is confirmed by tests. For new or more complex designs, `DoWhy`, `EconML` or `DoubleML` are preferred. A change must not be made only because a package delivers a more favorable point estimate.

---

# 5. Reproducible environment

No library is quietly installed in a global or shared Python environment. For an executable project, an isolated, project-specific environment or the already released project environment is used.

Before the initial analysis, the following should be recorded:

- Python and operating system version,
- package name and exact installed version,
- installation source,
- Lockfile or complete environment export,
- main class/function and relevant parameters,
- random seeds,
- structural model/design, estimand and data version ID,
- split/cross-fitting logic,
- relevant runtime warnings and deprecations,
- as well as path or hash of the generated configuration and results.

An unversioned `pip install <package>` is not a reproducible freeze. The
specific version is fixed in the project lockfile only after a compatibility
check; this framework deliberately does not freeze a universal package
combination.

---

# 6. Compatibility and integrity gate

Before Freeze, the following must be `PASS` when `TOOLING_REQUIRED` applies:

1. Import all required packages.
2. Report the actual installed versions.
3. Execution of the specifically used main API without unexplained warning.
4. A synthetic identification design with a known target value; for graphical
   adjustment, also a known valid adjustment set.
5. Synthetic positive effect with known sign.
6. Synthetic zero case in which the pipeline must not invent a stable effect.
7. At least one collider/post-treatment sentinel if adjustment is part of the analysis.
8. Time/Leakage Sentinels when market time series or event windows are used.
9. For coupled libraries, an end-to-end smoke test of exactly this version combination.

The decision is:

- `PASS`: only for the logged version combination and API.
- `FAIL`: Implementation or configuration is wrong; no freeze.
- `BLOCKED`: a required runtime, compatible version, or diagnosis is missing;
  no dependent causal step may proceed.
- `NOT_REQUIRED`: no executable causal method in design.

Warnings are not generally suppressed. They are first classified and only filtered specifically if their cause is understood and documented in the artifact.

---

# 7. Tool-specific minimum rules

## 7.1 DoWhy

- Graph, Treatment, Outcome and Estimand are explicitly versioned.
- `identify_effect` or the corresponding current API is executed before `estimate_effect`.
- The strategy used by the identifier and the adjustment set are stored.
- Refuters are falsification attempts, not confirmation of the truth.
- placebo, negative-control, and sensitivity tests are selected design-specifically; not every refuter makes sense for every design.

## 7.2 pgmpy

- Model type and edge list are versioned.
- Backdoor/frontdoor and adjustment queries are checked against the specific Estimand.
- A technically valid adjustment set is valid only relative to the assumed graph.
- Probabilistic query and interventional query are separated linguistically.

## 7.3 EconML and DoubleML

- Identification assumption and estimand are fixed before the model class.
- Treatment, outcome, confounder, instrument and effect modifier roles are not interchanged.
- Nuisance readers, hyperparameters, tuning room and cross-fitting are frozen.
- Overlap/instrument relevance and dependence are diagnosed.
- A flexible estimator is tested against a simpler, identically identified baseline.
- Uncertainties are only used if their prerequisites match the split/cluster structure.

## 7.4 Tigramite

- The conditional-independence test and its distribution assumptions match the data.
- Lag search and edge space are part of multiple testing.
- Simultaneous edges are not causally oriented by mere order within coarse bars.
- Regime or context procedures require predefined environments or their own validation logic.

## 7.5 causalinference

- Use only for binary treatment and the actual supported propensity/matching/weighting steps.
- Report overlap, trimming, balance and estimator variant.
- Test against the current runtime before use.
- Do not use as a substitute for graph identification, DML or time series methods.

---

# 8. Required Research Case artifact

Section `E9` of `02_RESEARCH_CASE_TEMPLATE.md` contains at least:

```text
TOOLING_STATUS:
TASK:
PRIMARY_LIBRARY:
PACKAGE_VERSION:
PYTHON_VERSION:
MAIN_API:
GRAPH_VERSION:
ESTIMAND_VERSION:
ADJUSTMENT_SET:
SEED:
SPLIT_LOGIC:
LOCKFILE_OR_ENV_HASH:
COMPATIBILITY_SMOKE_TEST:
SYNTHETIC_CAUSAL_SENTINEL:
WARNINGS:
INDEPENDENT_CHECK:
ALLOWED_CLAIM:
FORBIDDEN_CLAIM:
```

Without this artifact, `E9 PASS` is inadmissible at `TOOLING_REQUIRED`.

---

# 9. Anti-window-dressing rule

The minimum sufficient stack wins:

- no causal discovery library for an already identified simple event regression,
- no causal forest if a pre-specified linear effect answers the question,
- not DoWhy, pgmpy, EconML and DoubleML simultaneously without separate task,
- no GCM/counterfactual model for a purely predictive residual alarm,
- no package change after looking at validation results.

Complexity is added only if it can answer a previously named identification, estimate, heterogeneity, refutation, or discovery question and be incrementally validated.

---

# 10. Official documentation

- DoWhy User Guide: <https://www.pywhy.org/dowhy/v0.14/user_guide/>
- DoWhy Refutation Guide: <https://www.pywhy.org/dowhy/v0.14/user_guide/refuting_causal_estimates/index.html>
- pgmpy Causal Identification Guide: <https://pgmpy.org/guides/causal_identification.html>
- pgmpy `CausalInference` API: <https://pgmpy.org/api/generated/causal_inference/pgmpy.inference.CausalInference.CausalInference.html>
- EconML Documentation: <https://econml.azurewebsites.net/>
- DoubleML User Guide: <https://docs.doubleml.org/stable/guide/guide.html>
- Tigramite Documentation: <https://jakobrunge.github.io/tigramite/>
- Causalinference Documentation: <https://causalinferenceinpython.org/>

Before each new project environment, the current official documentation is checked again. APIs, optional dependencies and tested package combinations can change.
