# 02_RESEARCH_CASE_TEMPLATE.md

**Template version:** 2.1 **INSTRUCTION:** Copy this file for each research project. Do not delete any mandatory field. Complete non-applicable fields with `N/A + justification`. Mark unknown mandatory fields with `BLOCKED + missing information`.

**CONDITIONAL ACTION:** The sections `U–Y` will only be opened when section `T` is completed with `VALIDATED_PHENOMENON` **and** strategy engineering is explicitly chosen as the next step. If the phenomenon is validated but not continued, the block gets `DEFERRED_AFTER_VALIDATION`; without the validated phenomenon, it gets `NOT_ACTIVATED_BY_T_GATE`. In both cases, it is not filled field by field with `N/A`. Section `Z` remains active throughout the project.

**EARLY GATE BREAKDOWN:** If a gate terminates the current research version before section `T`, all later sections that can no longer be reached are marked once as `NOT_REACHED_DUE_TO_FAILED_GATE`. They are not filled in field by field; section `Z` remains active.

**Early BLOCKED:** `BLOCKED` does not end the version. Subsequent sections remain untouched, `Z` logs blockers and missing information, and editing continues only after resolution in the same version. `NOT_REACHED_DUE_TO_FAILED_GATE` applies only after `FAIL`.

**GATE STATUS MAPPING:** `PASS → PHASE STATUS COMPLETE`, `FAIL → PHASE STATUS FAILED`, `BLOCKED → PHASE STATUS BLOCKED`. After `FAIL` or `BLOCKED`, no dependent follow-up step begins.

---

# A. Research metadata

| Field | Entry |
|---|---|
| Research-ID | |
| Research title | |
| Version | |
| Research status | `DISCOVERY / DEVELOPMENT / CANDIDATE_HYPOTHESIS / IN_TEST / NO_PHENOMENON / INCONCLUSIVE / VALIDATED_PHENOMENON / ECONOMICALLY_UNTRADEABLE / ACTIVE_STRATEGY_CANDIDATE / ACTIVE / UNDER_OBSERVATION / SUSPENDED / REVALIDATED / REJECTED` |
|Created on| |
|Latest amendment| |
| Freeze date | |
|Responsible researcher/agent| |
|Hypothesis version| |
| Claim level | `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL` |
| Estimand version | `N/A for ASSOCIATIONAL_PREDICTIVE` |
| Identification status | `NOT_REQUIRED_PREDICTIVE / PASS / FAIL / BLOCKED` |
| Structural-model/identification-design version | |
| Tooling status | `TOOLING_REQUIRED / TOOLING_NOT_REQUIRED / TOOLING_BLOCKED` |
| Tooling manifest version | |
| Cost-model version | |
|Primary data set| |
| Operational governance version | |
| Run manifest register | `Path/URI to the register of all run IDs for this research version` |
| Evidence ledger version | |
| Review ledger version | |
| Eval suite version | |
| Latest regression-gate status | `PASS / FAIL / BLOCKED / NOT_RUN_NO_AGENT_CHANGE` |
| Intake idea ID / intake version | |
| Event class | `INFORMATION_EVENT / SCHEDULED_STRUCTURAL_EVENT / CONTINUOUS_ENDOGENOUS_MECHANISM / RETURN_DECOMPOSITION` |
| Mechanism evidence | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` |
| Forward-OOS forecast | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` |
|Net executable edge| `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` |

## A1. Active project sources at start

|Source| Version/status |Relevance to this research|
|---|---|---|
| ACTIVE_DOCUMENTS.md | | |
| Trading_System.md | | |
| Projekt-Workflow.md | | |
| Chart_Indikator_Settings.md | | |
| Masterjournal.md | | |
|Other| | |

## A2. Operational artifact register

The register references the machine-readable artifacts for `05_AGENT_OPERATIONS.md`. A hash refers to the unchanged stored content, not a later newly created export.

| Artifact type | ID/version | Schema/format version | Path/URI | Content hash | Status |
|---|---|---|---|---|---|
| Run-Manifest | | | | | `COMPLETE / FAILED / BLOCKED` |
| Evidence Ledger | | | | | `COMPLETE / INCOMPLETE / CONFLICTED / BLOCKED` |
| Review Ledger | | | | | `NO_REVIEW / OPEN / ACCEPTED / REJECTED / SUPERSEDED` |
| Forecast Ledger | | | | | `N/A / OPEN / PARTIALLY_RESOLVED / RESOLVED` |
|Eval result| | | | | `PASS / FAIL / BLOCKED / NOT_RUN` |
|Hypothesis intake| | `1.4.0` | | | `INBOX / SCREENED / MERGED / REJECTED / PROMOTED` |
|Strategy Reconstruction, if source strategy| | `1.1.0` | | | `SOURCE_EXTRACTION / TRANSLATION_DRAFT / RECONSTRUCTION_COMPLETE / DISCRETIONARY_PROTOCOL_COMPLETE / NOT_OPERATIONALIZABLE` |
|Concept audit, before completing a source reconstruction| | `1.0.0` | | | `DRAFT / COMPLETE / BLOCKED` |
|Condition Inquiry, if activated| | `1.0.0` | | | `PLAN / EXPLORATORY_RESULTS / INDEPENDENT_RESULTS / BLOCKED` |
|Causal identification assessment, in the case of a causal claim| | `1.0.0` | | | `PASS / FAIL / BLOCKED / NOT_REQUIRED_PREDICTIVE` |
|Philosophy of Science Review if Q9 is activated| | `1.0.0` | | | `BUNDLE_MAPPED / CONTINUATION_REVIEWED / BLOCKED` |
|Search space register| | `1.0.0` | | | `N/A (counting register)` |
| Entry Noise Screen | | `1.0.0` | | |`PASS / FAIL / BLOCKED` or intake waiver|

## A3. Academic source protocol

**ACADEMIC_SOURCE_STATUS:** `REQUIRED / NOT_RELEVANT + justification / BLOCKED + missing information`

For `REQUIRED`, **05_AGENT_OPERATIONS.md §5.4** and `schemas/evidence.schema.json` version 2.0.0 apply. Concrete versions of scientific papers are sought and evaluated, not only search hits or citations.

### A3.1 Research coverage

| Channel | Search query/filter | Search timestamp |Result| Evidence/URI |
|---|---|---|---|---|
| The Journal of Finance | | | `SEARCHED_HIT / SEARCHED_NO_HIT / NOT_RELEVANT + reason / BLOCKED + reason` | |
| Journal of Financial Economics | | | `SEARCHED_HIT / SEARCHED_NO_HIT / NOT_RELEVANT + reason / BLOCKED + reason` | |
| arXiv q-fin | | | `SEARCHED_HIT / SEARCHED_NO_HIT / NOT_RELEVANT + reason / BLOCKED + reason` | |
| Other journals/working-paper series/repositories | | | | |

### A3.2 Source, version, and integrity registers

| work_id | source_id | Study type | Publication status | concrete version | Authors/year | Venue | DOI | arXiv ID / q-fin category / version | Integrity status / checked on / notice | Code | Data | Independent replication / source IDs | Permitted use of evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | |

### A3.3 Version families and independence

|Verified source ids|Decision| work_id(s) |Justification|Tester/Time|
|---|---|---|---|---|
| | `SAME_WORK / DISTINCT_WORK / UNCERTAIN` | | | |

Journal name, DOI, citation number and q-fin category do not automatically increase the Evidence Grade. `PREPRINT`, `WORKING_PAPER` and `OTHER` are marked as provisional; a concrete arXiv version is frozen with version suffix. Correction, Expression of Concern, Retraction, Withdrawal as well as code, data and replication status are re-checked before freeze and release.

## A4. Research scope

| Field | Entry |
|---|---|
|Market and instrument(s)| |
|Venue(s) and specific data feeds| |
| Book view | `VENUE_DIRECT / CONSOLIDATED / TOP_OF_BOOK / L2 / L3 / N/A + reason` |
| Trading phase | `PRE_MARKET / OPENING_AUCTION / CONTINUOUS / CLOSING_AUCTION / POST_MARKET / OVERNIGHT / CROSS_SESSION / OTHER` |
|Venue calendar, time zone and DST rule| |
|Primary time basis| `CLOCK_TIME / EVENT_TIME / TRADING_DAY / OTHER + definition` |
|Forecast/outcome horizon| |
| Event class | `INFORMATION_EVENT / SCHEDULED_STRUCTURAL_EVENT / CONTINUOUS_ENDOGENOUS_MECHANISM / RETURN_DECOMPOSITION` |
| News/macro policy | `INCLUDED_AS_SIGNAL / NOT_USED_AS_SIGNAL / FILTER_KNOWN_EVENTS / SCHEDULED_EVENT_STUDY` |
|News/event feeds used and coverage period| `Required for FILTER_KNOWN_EVENTS; otherwise N/A + reason` |
|Exclusion window and timestamp convention| `Required for FILTER_KNOWN_EVENTS; otherwise N/A + reason` |
|known coverage gaps| |
| Explicitly excluded research questions | |

**Scope rule:** `NOT_USED_AS_SIGNAL` does not mean that events have been removed from the sample. The term “news-free” is used only as a short form of a documented `FILTER_KNOWN_EVENTS` policy and is always reported along with feed coverage and known gaps.

## A5. Upstream hypothesis inbox

The raw idea is recorded before section `B` and validated against `schemas/hypothesis_candidate.schema.json`. `PROMOTED` opens only the phase 0 pre-test; it is not a positive evidence finding.

| Field | Entry |
|---|---|
| Idea-ID / Version | |
| Intake status | `INBOX / SCREENED / MERGED / REJECTED / PROMOTED` |
|Origin / concrete source| |
| Idea class | `ASSOCIATIONAL_PATTERN / PREDICTIVE_PRECEDENCE / MECHANISM_CANDIDATE / STRUCTURAL_FLOW_CANDIDATE / RELATIVE_VALUE_CANDIDATE / EVENT_RESPONSE_CANDIDATE / RETURN_DECOMPOSITION_CANDIDATE / OTHER` |
| Mechanism family |non-exhaustive router label or `UNCLASSIFIED`|
| Actor status |Named hypothesis with compulsion/action/alternative or `UNSPECIFIED / NOT_CLAIMED`|
| Observable footprint | |
|Expected outcome and horizon| |
|Main alternative explanations| |
|Required resolution / data fields / venue coverage| |
|Clock sync, sequence and observability requirements| |
|Early cost, latency, queue, borrow, funding or leg-risk hurdle| |
|Dataset IDs already considered / current data role| |
| Variable-selection mode | `PREDEFINED / DATA_DRIVEN / HYBRID` |
|Reason for selection / variables retained| |
|DATA_DRIVEN/HYBRID: Candidate universe / effective number of candidates| |
|DATA_DRIVEN/HYBRID: Selection data + role / outcome visibility| |
|DATA_DRIVEN/HYBRID: Methods / search space / selection-bias controls| |
| Duplicate / merged_into_id | |
|Screening decision and reason| |
|at PROMOTED: next research ID and phase 0 question| |

### A5.1 Separate evidence levels

| Level | Status | Supporting evidence/run IDs |Justification / next test|
|---|---|---|---|
| `mechanism_supported` | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` | | |
| `forward_predictive_oos` | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` | | |
| `executable_net_edge` | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` | | |

The steps are not upgraded in a cascade. In particular, a mechanism paper does not provide a forward forecast, a contemporaneous context does not provide a future return, and a mid-quote effect does not provide a net executable edge.

### A5.2 Two independent axes

| Axis | Entry |
|---|---|
| Research-Claim-Level | `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL` |
| Validation/trading status | the three separate statuses from A5.1 |

No axis is derived from another. In particular, an identified interventional effect may be economically untradeable after costs, while an associative forecast may be executable without a causal claim.

---

# B. Phase 0 – Feasibility and Information Budget

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

## B1. Preliminary observation

**What was observed?**

...

**Why is it worthy of research?**

...

**What is NOT to be explicitly claimed yet?**

...

## B2. Primary outcome scale

| Field | Entry |
|---|---|
|Primary outcome| |
| Unit | e.g. R, ATR-normalized return, basis points, event probability |
|Typical horizon| |
|Exploratory scatter from permitted discovery/development data| |
|Sample size and effective cluster number of this estimate| |
|Uncertainty/bandwidth of dispersion estimation| |
|Source and transferability to validation market/state| |
|Heavy tails already visible?| `YES / NO / UNCLEAR` |

## B3. Provisional cost hurdle

| Cost component |Estimation|Source|State-dependent?|
|---|---:|---|---|
|Fees Round Trip| | | |
| Spread | | | |
| Slippage | | | |
| Funding/financing | | | |
|Other| | | |

**Total Conservative Round Trip Costs in Outcome Unit:** ...

**Additional margin of safety:** ...

**Minimum economically relevant effect size `δ_econ`:** ...

**Justification of the margin of safety:** ...

## Power/precision planning

| Field | Entry |
|---|---|
|Primary test/estimator| |
|Error level / α / equivalent threshold|Working default in classical test: `α = 0.05`, two-sided; justify any deviation in advance|
|Target power / precision target|Working default: `80%`; use `90%` for a close final holdout or high cost of false negatives, or specify a direct precision target|
| Economic relevance threshold | `δ_econ = ...` |
| Assumed true planning effect |`δ_plan = ...`; do not equate with `δ_econ`|
|Source/justification of `δ_plan`|including dealing with discovery bias, uncertainty and, if necessary, shrinkage|
| Null/alternative hypothesis | `H0: ... / H1: ...` |
| Interval/decision rule |e.g. `lower bound > δ_econ`; plan exactly for this|
| Baseline dispersion assumption | |
| Conservative planning dispersion / stress scenario | |
|Derivation of conservative adoption| `external/pooled reference / model-valid upper bound / robust scale + stress uplift / scenario analysis / OTHER` |
|Dependency assumption| |
| Power/simulation method | |
|Required nominal N – baseline scenario| |
|Required effective N/cluster number – baseline scenario| |
|Required nominal N – stress scenario| |
|Required effective N/cluster number – stress scenario| |

**Mandatory rule:** A single point estimator from a small, selected, or non-transferable discovery sample is not sufficient as a conservative planning assumption. `CONTINUE` assumes that feasibility also exists in the stress scenario or that the additional information required is explicitly obtained.

## B5. Information available

| Item | Value |
|---|---:|
| Nominal events | |
| Trading days | |
| Sessions | |
| Event clusters | |
| Symbols | |
| Approximate correlation groups | |
|Method/simulation for effective N| |
|Design effect used and assumptions| |
|Estimated effective N| |
|Conservative lower limit of effective N| |
|Plausibly independent cluster number| |
|Realistically additionally obtainable independent data| |

## B6. Feasibility decision

**Research decision:** `CONTINUE / OBTAIN_DATA / ABORT`

** Justification:** ...

**Is the decision also valid under the conservative planning dispersion?** `YES / NO / BLOCKED`

**If OBTAIN_DATA:** What data, how much, and why? ...

**If ABORT:** Which gate makes the project uninformative? ...

### B-Gate

`PASS / FAIL / BLOCKED`

**Fixed mapping:** `CONTINUE → PASS`, `OBTAIN_DATA → BLOCKED until data are available`, `ABORT → FAIL`. `BLOCKED` is not a fourth research decision.

**Reach:** A `PASS` here only opens Discovery/Development. Before Freeze, the formal Phase-0 recalculation in `N3` is mandatory.

**Next permitted step:** ...

---

# C. Data inventory and roles

**PHASE STATUS:** `COMPLETE / BLOCKED`

| Dataset ID |File/source|Period|Markets/symbols| Role | Already viewed? | Influenced a design decision? | Current role correct? |
|---|---|---|---|---|---|---|---|
| | | | | `DISCOVERY / DEVELOPMENT / VALIDATION / FINAL_HOLDOUT / FORWARD_OOS` | | | |

## C1. Contamination log

| Date | Dataset |What information was seen?| Which design decision was influenced? |Consequence for data role|
|---|---|---|---|---|
| | | | | |

**Rule:** Once a dataset influences a design decision, it may no longer be considered an independent validation/holdout.

---

# D. Discovery and Case Catalogue

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED`

## D1. Neutral description of the phenomenon

...

## D2. Case types

| Case type | Count | Note |
|---|---:|---|
| clear hits | | |
|Clear failures| | |
|Borderline cases| | |
| unclassified | | |

## D3. Exploratively tested variables and variants

**Important:** Also enter discarded variants.

| ID | Variable/idea | Lookback/parameter |Result gross| Retained? |Did hypothesis influence?|
|---|---|---|---|---|---|
| | | | | | |

## D4. Discovery decisions

Which terms have been rejected, changed or specified? ...

---

# E. Claim Level, Identification Model and Observability

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

## E1. Claim level and target size

**Strongest intended claim:** `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`

**Causal formalism:** `SCM_DAG / POTENTIAL_OUTCOMES / STRUCTURAL_ECONOMETRIC / OTHER_EXPLICIT / NOT_REQUIRED_PREDICTIVE`

**Predictive target, if applicable:** `P(...) / E[...] / quantile / other quantity`

**Causal estimand:** ... / `N/A + justification: ASSOCIATIONAL_PREDICTIVE`

| Component | Definition |
|---|---|
| Treatment/intervention/structural shock | |
|Outcome and horizon| |
| Target population/event class | |
| Contrast and unit | |
| Total/direct/mediation effect | |
| Temporal ordering | |
|Consistency / SUTVA or deviation| |
| Positivity / Overlap | |
| Assignment/exchangeability/design assumption | |
| Interference/exposure mapping | |

## E2. Structural model or identification design

**Representation:** `SCM_DAG / POTENTIAL_OUTCOMES / STRUCTURAL_ECONOMETRIC / OTHER_EXPLICIT / NOT_REQUIRED_PREDICTIVE`

**Structural-model/design version:** ... / `N/A for NOT_REQUIRED_PREDICTIVE`

**Graphic, counterfactual, or structural definition:**

```text
...
```

**Which edges, contrasts or assignment mechanisms remain only partially identified?** ...

## E3 Structural assumptions and alternative explanations

| Structural assumption/edge |Acceptance|Possible confounder/collider/measurement error|Alternative statement| Testable consequence/negative control |
|---|---|---|---|---|
| | | | | |

## E4. Identification strategy

**Strategy:** `Randomization / natural variation / Backdoor / Frontdoor / IV / RD / DiD / high-frequency identification / other / NOT_REQUIRED_PREDICTIVE`

**Why does this strategy identify exactly the estimand?** ...

|Acceptance| Testable? | Evidence/diagnostic | Violation risk |Sensitivity/placebo/negative control|
|---|---|---|---|---|
| | `YES/NO/PARTIAL` | | | |

**Adjustment set or comparable design restriction and justification:** ...

**Positivity/overlap or instrument relevance, if applicable:** ...

**Which post-treatment variables/mediators may not be accepted as ordinary controls?** ...

## E5. Causal discovery/time series procedure, if used

| Method |Permitted claim|Claims not permitted|Assumptions required| Result label |
|---|---|---|---|---|
| Granger |additional forecast information relative to the information set|Interventional causality|Stationarity/model specification/information set| `PREDICTIVE_PRECEDENCE` |
| CI/score/invariance/time-series discovery |DAG candidates/equivalence class under assumptions|“true DAG” without additional assumptions|Specifically document| `CAUSAL_HYPOTHESIS` |

## E6. Observability table

| Variable | Role | Raw data + vintage |Calculation|Earliest fully known time|Available at decision time?| Delay | Leakage/revision risk |Permitted?|
|---|---|---|---|---|---|---|---|---|
| | `Predictor / State / Treatment / Shock / Mediator / Trigger / Outcome` | | | | `YES/NO` | | | `YES/NO` |

### E7-Gate – causality/identification

`PASS / FAIL / BLOCKED / NOT_REQUIRED_PREDICTIVE`

**Causal-identification-assessment ID:** ... / `N/A for NOT_REQUIRED_PREDICTIVE`

For `INTERVENTIONAL` or `COUNTERFACTUAL`, E7 may only be transferred from a validated `causal_identification_assessment`. A self-set `PASS`, an estimator run, a narrow event window or a discovery result is not enough.

- `PASS`: Only for the frozen causal claim and under documented assumptions.
- `NOT_REQUIRED_PREDICTIVE`: Research may continue, but only with predictive/associative language.
- `FAIL/BLOCKED`: No causal freeze. A continuation as predictive research requires a new correspondingly declared version.

### E8-Gate – Leakage/Observability

`PASS / FAIL / BLOCKED`

## E9 Tooling Router and Reproducible Environment

**Tooling status:** `TOOLING_REQUIRED / TOOLING_NOT_REQUIRED / TOOLING_BLOCKED`

** Justification:** ...

| Task |Primary library| Exact version |Main class/function|Permissible statement|Inadmissible statement|Independent verification|
|---|---|---|---|---|---|---|
| Structural model/adjustment | `DoWhy / pgmpy / design-specific / N/A` | | | | | |
|Effect assessment| `DoWhy / EconML / DoubleML / causalinference / other / N/A` | | | | | |
|Refutation/sensitivity| `DoWhy / design-specific / N/A` | | | | | |
| Time-series discovery | `Tigramite / other / N/A` | | | | | |

| Reproducibility field | Entry |
|---|---|
| Python/runtime version | |
|Environment/Lockfile path or hash| |
| Package source | `official release / justified other source` |
| Seed(s) | |
| Temporal/cluster split logic | |
| Structural-model/design/estimand version | |
| Adjustment set | |
|Import/API/compatibility smoke test| `PASS / FAIL / BLOCKED / NOT_REQUIRED` |
| Relevant warnings/deprecations | |

**E9-Gate – Tooling reproducibility:** `PASS / FAIL / BLOCKED / NOT_REQUIRED`

**Phase mapping:** `E7 PASS or NOT_REQUIRED_PREDICTIVE`, `E8 PASS`, and `E9 PASS or NOT_REQUIRED` → `COMPLETE`. Every `FAIL` → `FAILED`; every `BLOCKED` → `BLOCKED`.

**If FAIL:** exit research version or redefine variable. No retroactive repair within the same validation version.

---

# F. Operationalization

**PHASE STATUS:** `COMPLETE / BLOCKED`

**Strategy reconstruction ID, if the idea comes from an incompletely defined source:** ... / `N/A + justification`

**Fidelity label of translation:** `REPLICATION / DOCUMENTED_RECONSTRUCTION / SIMPLIFIED_VARIANT / PLAYBOOK_ONLY / N/A`

**Concept-audit ID:** ... / `N/A because there is no incompletely defined source strategy`

**Are the four condition classes separate?**

| Class |Entries/references|May be included in the source strategy?|
|---|---|---|
| strategy-defining | |Yes, true to the source|
| Application referred to by the source | |Only with real source status|
| suspected success modifier | |No; own condition hypothesis|
| unknown success conditions | |No; remain unknown|

**Design dependencies between state, trigger and outcome:** ...

**Preliminary measuring instruments, in particular regime/state filters:** ...

**Which statement would actually be omitted from a non-informational instrument, and which could remain open separately?** ...

| Concept | Exact measurement definition | Unit | Lookback | Session | Timeframe | Timestamp |Continuous or discrete?|
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Which thresholds have NOT yet been set and why?** ...

**Which thresholds are already factually justified?** ...

---

# G. Target variable and null model

**PHASE STATUS:** `COMPLETE / BLOCKED`

## G1. Primary outcome

**Definition:** ...

**Horizon:** ...

Why this outcome?

## G2. Secondary outcomes

| Outcome | Purpose |Primary/diagnostic|
|---|---|---|
| | | |

## G3. Primary null model

**Definition:** ...

Why is this the right comparison?

## G4. Secondary benchmarks

| Benchmark | Purpose |
|---|---|
| | |

## G5. Event/surprise definition

**Applicability:** `APPLY / N/A + justification`

| Field | Specification |
|---|---|
| Event class | |
|Official release time and time zone| |
|Published value + data vintage| |
|Expectation source available before the event| |
| Expectation timestamp/vintage | |
| Surprise formula | |
| Predefined scaling | |
| Number of surprise factors | `1 / multiple + justification` |
| Factor construction/rotation/orthogonalization | |
|Economic Interpretation and Sign Convention by Factor| |
|Primary event window| |
|Secondary Event Window| |
|Rule for simultaneous/overlapping messages| |
|Rule for illiquid/technically defective windows| |
| Structural shock identified? | `YES + E7 PASS / NO, descriptive surprise only` |

## G6. Expected response model

**Applicability:** `APPLY / N/A + justification`

| Field | Specification |
|---|---|
|Training data and data role| |
| Strictly time-ordered training rule `D_<t` | |
|only pre-event known controls `C_t`| |
|Model `m̂_j(F_t,C_t,F_t⊗C_t)`| |
| Refit/update rule | |
| Uncertainty model `σ̂_j,t` | |
| Calibration diagnostic | |
|primary residue `u_j,t`| `R_j,t - m̂_j(F_t,C_t,F_t⊗C_t;D_<t)` |
| standardisierte Innovation `z_j,t` | `u_j,t / σ̂_j,t` |
|Permitted label| `REACTION_INNOVATION / REACTION_ANOMALY` |

**Why is the model deviation not automatically misjudgement or causal break?** ...

**Easiest appropriate model chosen?** `YES / NO + concrete additional question that justifies the complexity`

## G7 Reaction chain and mediators

| Chain link | Measurement window | Expected direction/form | Role `Outcome/Mediator` | Post-event? |Use allowed in total effect?| Identification status |
|---|---|---|---|---|---|---|
| | | | | | | |

**Joint chain-integrity metric:** `N/A by default / APPLY only with predefined weights, covariance, reference distribution, and multiple-testing rule`

**Criterion for the designation `CAUSAL_CHAIN_BREAK`:** ... / `NOT PERMITTED because the chain is not causally identified`

---

# H. Exploratory effect and state analysis

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED / FAILED`

## H1. Unconditional or preconditional baseline effect

|Size|Estimation|
|---|---:|
| E[Outcome \|phenomenon| |
| E[Outcome \| null model] | |
| Difference | |
|Uncertainty| |

**Is the baseline conditional from the beginning?** `YES / NO`

**If YES: Why was the state part of the original definition of the phenomenon and not a subsequent filter?** ...

## H2. State variables initially continuous

| State | Relationship with outcomes | Form of the relationship | Stable range? | Candidate for hypothesis? |
|---|---|---|---|---|
| | | | | |

## Phenomenon vs. State vs. Interaction

|Size|Result|
|---|---|
| E[R \| P] | |
| E[R \| S] | |
| E[R \| P,S] | |
|Additional information from P beyond S| |

## Winners and losers analyzed together?

`YES / NO`

If NO: `FAILED`.

## H4a. Quantitative condition inquiry

**Activation:** `APPLY / NOT_ACTIVATED + justification`

**Condition-Inquiry-ID:** ...

**Question:** `measurement instrument / design dependence / definition sensitivity / success modifier / time stability / environment stability / necessary condition (exploratory)`

| Candidate condition | Origin |Known at the decision?| Role | Status |Need a new hypothesis?|
|---|---|---|---|---|---|
| | `source / concept audit / theory / data-based / unknown` | | `strategy-defining / application / success modifier / unknown` | | |

In the case of an additional measuring instrument:

| Question | Settlement/result |
|---|---|
|Purpose of the instrument| |
|Quantities used in its calculation| |
|future targets that are not in it| |
|Comparison with continuous inputs/simple baseline| |
|Share per label, only descriptive| |
|Additional separation information| |
|Affected claim in the absence of separation| |

A condition discovered from data is not written back into the source strategy. Prognostic separation proves neither a real hidden state nor an actor, mechanism or intervention effect.

## H5. Exploratory event and reaction analysis

**Applicability:** `APPLY / N/A + justification`

| Item | Result | Permitted interpretation |
|---|---|---|
|Gross response| | descriptive |
|Reaction to Surprise| |Predictive or causal only according to E7|
|OOS estimated reaction innovation| | forecast error/anomaly |
| Chain-link deviations | | leg-specific anomalies |
| State/attention interaction | |Counter-hypothesis until independently validated|
|competing news/liquidity statement| |Alternative declaration|

## H6. Quantitative Shock-Response-Map

**Applicability:** `APPLY for a multi-link event/effect chain / N/A + justification`

| Chain link/asset |Horizon| Surprise factors | Pre-event state interactions |Response coefficient + uncertainty|Innovation available in time?|Permitted label|
|---|---|---|---|---|---|---|
| | | | | | | `TRANSMISSION_DIAGNOSTIC` |

### Incremental test of an information-bottleneck candidate

**Defined end outcome:** ...

**M0:** `End outcome ~ surprise factors + pre-event states`

**M1:** `M0 + timely available innovation from the pre-selected chain link`

| Field | Settlement/result |
|---|---|
|Candidate and reason for selection| |
|Time of real availability| |
|primary OOS loss/calibration/net utility size| |
| M0 OOS | |
| M1 OOS | |
|incremental improvement + uncertainty| |
| Multiple-testing treatment | |
|Admissible decision| `INFORMATION_BOTTLENECK_CANDIDATE / NO_ADDED_VALUE / INCONCLUSIVE` |

---

# I. Candidate Hypothesis

**PHASE STATUS:** `COMPLETE / BLOCKED`

## I1. Primary hypothesis

> ...

**Claim-Level:** `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`

**Causal: Estimand version and E7 gate:** ...

**If constraint language is used:**

**Constraint assessment ID after `schemas/constraint_assessment.schema.json`:** ...

| Field | Specification |
|---|---|
| Defined end outcome/system objective | |
| Label | `TRANSMISSION_DIAGNOSTIC / INFORMATION_BOTTLENECK_CANDIDATE / IDENTIFIED_CAUSAL_LEVER / IMPLEMENTATION_CONSTRAINT` |
| Predefined decision criterion | |
|why the label was not derived from correlation or large residual| |

## I2. Counter-hypothesis

> ...

## I3. Expected direction

`POSITIVE / NEGATIVE / TWO_SIDED`

## I4. Economically relevant threshold

`δ_econ = ...`

## I5. Falsification condition

...

## I6. Rule for unexpected signs

If a sufficiently precise effect with opposite sign is observed:

- old hypothesis = `FALSIFIED`,
- new hypothesis = new version/research ID,
- no semantic relabeling.

## I7. Target level of this test

**Primary tested level:** `mechanism_supported / forward_predictive_oos / executable_net_edge`

**What stronger level must NOT be explicitly derived from this design?** ...

**If a contemporary context is examined:** Why is the outcome not labeled as a forward forecast? ...

---

# J. Prediction list

**PHASE STATUS:** `COMPLETE / BLOCKED`

| ID |Additional prediction| Data basis | Test method |How can the result influence the hypothesis?|
|---|---|---|---|---|
| P1 | | | | |
| P2 | | | | |

---

# K. Pre-Mortem and Guardrails

**PHASE STATUS:** `COMPLETE / BLOCKED`

**Assumption:** The result looks good, fails later OOS or live. Why?

|Risk| Why plausible? | Pre-check | Guardrail | Rejection criterion |
|---|---|---|---|---|
| Leakage | | | | |
| Selection Bias | | | | |
| latent confounder/collider | | | | |
|post-treatment control/unidentified mediation| | | | |
| wrong expectation vintage/event-window contamination | | | | |
| mixed news shocks | | | | |
|Attention/positioning/liquidity instead of mechanism breakage| | | | |
|Too little independent evidence| | | | |
| dominant symbol/event | | | | |
| Multiple Testing | | | | |
|Costs/Slippage| | | | |
|Midquote effect without executable fill| | | | |
| Feed latency/clock desynchronization/stale quote | | | | |
|Public tape signature does not identify latent actor| | | | |
|Structural breakage/calendar or venue rule change| | | | |
|Live variable available too late| | | | |
| Other | | | | |

---

# L. Dependence, effective N and inference

**PHASE STATUS:** `COMPLETE / BLOCKED`

## L1. Dependence diagnosis

|Risk| Present? |Measurement/justification|
|---|---|---|
| serial autocorrelation | | |
|multiple signals per pulse| | |
|Overlapping labels| | |
| correlated symbols | | |
| joint macro events | | |
| dominant session/event clusters | | |

## L2. Clusterdefinition

**Primary cluster unit:** ...

**Secondary cluster unit:** ...

## L3. Selected inference method

`IID / BLOCK_BOOTSTRAP / CLUSTER_BOOTSTRAP / CLUSTER_ROBUST / OTHER`

**Why appropriate?** ...

## L4. Purging / Embargo

**Overlapping label/outcome windows over train/test limits?** `YES / NO`

**Purging rule:** ...

**Embargo rule:** ...

## L5. Effective N

**Method:** ...

**Nominal N:** ...

**Effective N / cluster count:** ...

**Design effect `DE = Var(actual design) / Var(IID reference)`:** ...

**Used DE formula/simulation and its assumptions:** ...

**Less than 30 independent clusters?** `YES / NO / UNCLEAR`

**If YES:** Status `SMALL_CLUSTER_WARNING`; small sample method used or calibration: ...

---

# M. Heavy Tails and Influence Diagnostics

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

`N/A` is only allowed for the heavy tail specific subfields if heavy tails have been objectively excluded. Influence diagnostics `M3` remains mandatory.

## M1. Primary location parameter

`MEAN / MEDIAN / TRIMMED_MEAN / ROBUST_M_ESTIMATOR / OTHER`

** Justification:** ...

## M2. Robust sensitivity

**Secondary estimator:** ...

**Trimming/Winsorization allowed?** ...

**If yes: exactly how and only as primary or sensitivity?** ...

## M3. Predefined influence diagnostics

| Diagnostic | Threshold/decision rule |
|---|---|
| Leave-one-out range | |
| Leave-one-cluster-out range | |
|Proportion of greatest observation| |
|Share of largest clusters| |
|Result without dominant symbol| |
|Result without dominant period/event group| |

**Minimum rule:** If removing a single plausible cluster tips the sign or economic conclusion, no robust confirmation.

---

# N. Multiple Testing / Research Search Space

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

A specific multiple testing correction in `N2` can be justified `N/A`. The formal phase 0 recalculation and the pipeline integrity gate are never `N/A`.

## N1. Actually examined degrees of freedom

| Dimension | Count/variants |
|---|---|
|Hypotheses| |
|Predictors| |
| State variables | |
| Lookbacks | |
| Thresholds | |
| Timeframes | |
| Sessions | |
| Symbols/universes | |
| Outcomes/horizons | |
| Entries/Exits | |

## N2. Selected correction/assessment method

`FDR / WHITE_REALITY_CHECK / HANSEN_SPA / DEFLATED_SHARPE / PBO / PIPELINE_BOOTSTRAP / N/A / OTHER`

Why this method?

## N2.1 Outcome evidence contract

| Field | Frozen value |
|---|---|
| Contract reference and version | |
| Status | `FROZEN / BLOCKED` |
| Primary outcome ID | |
| Required mechanism-diagnostic IDs or `NOT_CLAIMED` | |
| Multiplicity-family references | |
| Mechanical-coupling assessment complete? | `YES / NO` |
| Target-specific transportability rules complete? | `YES / NO` |
| Validation data still unseen when frozen? | `YES / NO` |

The referenced artifact must pass
`scripts/validate_outcome_evidence_contract.py`. `BLOCKED` stops validation.
The contract is referenced here rather than copied, so its frozen rules cannot
diverge from the protected artifact.

## Formal Phase-0 Calculation and Validation Specification

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

| Field |Frozen value|
|---|---|
|Final primary outcome and zero model| |
| `δ_econ` | |
|`δ_plan` or direct precision target| |
| `H0 / H1` or interval decision rule | |
|final spread and dependency assumption| |
|Required effective N/cluster number in the stress scenario| |
|nominal N required therefrom by DE/simulation| |
|Current Conservative Lower Limit of Effective N| |
|Validation Dataset, Period, Role and Unviewed Status| |
|Data split / external test window| |
| Success criterion A | |
| Opposite-direction rule B | |
|Precise zero rule C| |
| Inconclusive rule D | |

**Research decision:** `CONTINUE / OBTAIN_DATA / ABORT`

### N3-Gate – Formal feasibility before Freeze

`PASS / FAIL / BLOCKED`

**Fixed mapping:** `CONTINUE → PASS`, `OBTAIN_DATA → BLOCKED until data are available`, `ABORT → FAIL`. Only this `PASS` can open the way to the pipeline integrity gate and freeze.

## N4 Pipeline Integrity Check before Freeze

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

| Machine-enforced assessment | Value |
|---|---|
| Assessment reference and version | |
| Exact pipeline fingerprint reference and SHA-256 | |
| Status | `ASSESSED` |
| Overall gate | `PASS / FAIL / BLOCKED` |
| Validation data still unseen? | `YES` |

The referenced artifact must pass
`scripts/validate_pipeline_integrity_assessment.py`. Only `overall_gate: PASS`
may produce `PHASE STATUS: COMPLETE`; a schema-valid artifact is not enough by
itself.

| Test ID | Control type | Control basis |Empirical dataset + valid role| Null/synthetic design |Resulting time/cluster/state/volatility structure| Planned B |Actual B|Target precision + Monte Carlo SE/interval| Predefined acceptance rule |Result|
|---|---|---|---|---|---|---:|---:|---|---|---|
| PI-NULL | repeated null/surrogate control | `empirically derived / purely synthetic` |only on an empirical basis: `DEVELOPMENT`| | | | | | | |
| PI-SENTINEL |known effect with fixed sign and timing| `purely synthetic` | no empirical dataset | | | | | | | |
| PI-CAUSAL-TOOL |`TOOLING_REQUIRED`: known DAG/adjustment set and known effect| `purely synthetic` | no empirical dataset | | | | | | | |

- [ ] Full feature, selection, filter, timing and evaluation pipeline executed.
- [ ] Zero control does not destroy any dependency relevant to the zero model; any unexplained relevant structural deviation enforces `N4-Gate: BLOCKED`.
- [ ] False alarm rate or zero effect distribution is within the previously defined tolerance.
- [ ] Predefined target precision of the false alarm rate has been achieved.
- [ ] Sentinel was detected with correct sign, index and timing.
- [ ] `TOOLING_REQUIRED` tested import, version, main API and package compatibility; the causal sentinel provided a permissible adjustment set and correct direction.

### N4-Gate – Pipeline integrity

`PASS / FAIL / BLOCKED`

**Status mapping:** `PASS → COMPLETE`, `FAIL → FAILED`, `BLOCKED → BLOCKED`.

A single shuffle or random walk is not enough.

---

# O. FREEZE

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

## O1. Freeze checklist

Each point must be `YES`. `N/A + justification` is only allowed where the table row expressly allows it.

| Checkpoint | Status |
|---|---|
|Research ID/version fixed| |
|Solid candidate hypothesis| |
|Counter-hypothesis fixed| |
|Claim level fixed| |
|Causal estimand solid or `N/A: ASSOCIATIONAL_PREDICTIVE`| |
|Identification strategy/assumptions fixed or `NOT_REQUIRED_PREDICTIVE`| |
|E7 identification gate passed or `NOT_REQUIRED_PREDICTIVE`| |
|For causal claim validated `causal_identification_assessment` available| |
|Structural model/identification design version fixed or `NOT_REQUIRED_PREDICTIVE`| |
|E9 tooling gate passed or `NOT_REQUIRED`| |
|primary library per causal task and main API fixed or `TOOLING_NOT_REQUIRED + justification`| |
|Python/package versions, lockfile/environment, seeds and split logic fixed| |
|Complete observability| |
|Phenomenon fixed| |
|State variables fixed| |
|Fixed exclusions| |
|Fixed primary outcome| |
|Fixed zero model| |
|Event/surprise construction fixed or `N/A + justification`| |
|Expectation source, vintage, timestamp and event window fixed or `N/A`| |
|Number/rotation/Orthogonalization/interpretation of the Surprise factors fixed or `N/A`| |
|Fixed Event Window Contamination Rule or `N/A`| |
|Reaction model/time training rule/uncertainty fixed or `N/A`| |
|Response deviation correctly labeled as non-causal residue or causal chain identified| |
|for information bottleneck claim: end-outcome, candidate, time of availability and M0/M1-OOS test fixed or `N/A`| |
|Constraint label and decision criterion fixed or `N/A`| |
|Expected direction fixed| |
|δ econ fixed| |
|δ plan or direct precision target fixed| |
|H0/H1 or interval decision rule fixed| |
|primary estimator fixed| |
|Robust sensitivity fixed| |
|Dependency method fixed| |
|Efficient N-method| |
|Purging/Embargo Solid or N/A| |
|Influence diagnostics fixed| |
|Heavy-tail rule fixed| |
|Multiple testing method fixed| |
| formal phase-0 recalculation `N3` passed | |
|Validation data split/window fixed| |
|Minimum N fixed from conservative stress scenario| |
|Validation plan and A/B/C/D decision rules fully| |
|Pipeline integrity gate passed| |
|`TOOLING_REQUIRED`: Causal Tool Sentinel and Compatibility Smoke Test| |
|Data rolls fixed| |
| Validation dataset unviewed | |
|Final holdout unseen or `N/A + justification` external walk-forward| |
|Success criterion fixed| |
|Counter-direction rule fixed| |
|Fixed zero-effect rule| |
|Inconclusive rule fixed| |
|Cost model version fixed| |

## O2 Freeze Declaration

> From this point on, no material design changes will be made based on the ongoing validation results. Each material change generates a new Research version and consumes the previously viewed data for this new version as Development Data.

**Freeze confirmed on:** ...

### O-Gate

`PASS / FAIL / BLOCKED`

---

# P. Validation execution of the frozen plan

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

## P1. Freeze comparison

**Reference to frozen plan in N3/O:** ...

**Was any design field changed since freeze?** `YES / NO`

If `YES`: Do not start validation or terminate as `INVALID_TEST`; reclassify affected data to `DEVELOPMENT`.

## P2. Data architecture actually used

| Dataset | Role |Period|Unexamined confirmed?| Matches N3/O? |
|---|---|---|---|---|
| | VALIDATION | | | |

**Final holdout still fully reserved and untouched?** `YES / NO / N/A + justification`

If `NO`: do not start normal validation or discard final holdout status and reclassify data role.

## P3. Sample and start gate

**Minimum frozen N from N3/O:** ...

**Actually available nominal N:** ...

**Actually available conservative lower limit of effective N/cluster number:** ...

### P-Gate validation can start

`PASS / FAIL / BLOCKED`

Only `PASS` allows execution. `FAIL → FAILED`, `BLOCKED → BLOCKED`.

---

# Q. Validation result

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

## Q1 Confirmed Independence?

`YES / NO / UNCLEAR`

If NO: Which design decision was influenced? ...

**Consequence:** Reclassify Dataset to `DEVELOPMENT`; Independent validation is not claimed.

### Q1-Gate – Validation Independence

`PASS / FAIL / BLOCKED`

**Mapping:** `YES → PASS`, `NO → FAIL + INVALID_TEST`, `UNCLEAR → BLOCKED`. Without `PASS`, Q2–Q8 must not be interpreted as independent validation.

## Q2. Primary effect

|Size|Result|
|---|---:|
|Point estimator| |
| Null model | |
| Difference | |
| Uncertainty interval | |
| δ_econ | |
|Primary Decision A/B/C/D| |

## Q3. Robust sensitivity

|Estimator/analysis|Result|Does the conclusion change?|
|---|---:|---|
| | | |

## Q4. Influence diagnostics

| Diagnostic |Result| Gate passed? |
|---|---|---|
| Leave-one-out | | |
| Leave-one-cluster-out | | |
|Without a dominant symbol| | |
|without dominant period/event group| | |

## Q5. Multiple-testing-adjusted evidence

...

## Q6. Identification diagnostics for causal claims

**Applicability:** `APPLY / N/A: ASSOCIATIONAL_PREDICTIVE`

|Frozen acceptance/diagnosis|Result| Passed? |Consequence for causal claim|
|---|---|---|---|
|Overlap/positivity or instrument relevance| | | |
|Balance/Pre-Trends/Placebo if applicable| | | |
| Negative control | | | |
|Sensitivity to latent confounding| | | |
|Alternative allowed DAGs/partial identification| | | |

|Tooling execution|Logged value|
|---|---|
|Runtime, packages and versions| |
|Classes/functions actually used| |
|Seeds and actual split/cross-fitting logic| |
|Warnings, deprecations or compatibility deviations| |
|Artifact/configuration path or hash| |
|Independent reproduction/sensitivity| |

**Causal claim still allowed according to frozen gate?** `YES / NO / BLOCKED`

## Event/response innovation, if applicable

|Size|OOS result|Calibration/uncertainty| Interpretation |
|---|---|---|---|
|Surprise factors including rotation/sign stability| | | |
| Expected response | | | |
| `REACTION_INNOVATION` | | | |
| Chain-link deviations | | | |
|M0 vs M1 for pre-selected information bottleneck candidates| | | `incremental predictive value, not causal evidence` |
|competing news/liquidity statement| | | |

**Was a reaction anomaly without a passed chain-identification design called `CAUSAL_CHAIN_BREAK`?** `NO / YES → INVALID_CAUSAL_CLAIM`

**Authorised constraint/diagnostic label according to OOS:** `TRANSMISSION_DIAGNOSTIC / INFORMATION_BOTTLENECK_CANDIDATE / IDENTIFIED_CAUSAL_LEVER / NO_LABEL / N/A`

## Q8 Validation decision

`VALIDATED / FALSIFIED / PRECISE_NULL / INCONCLUSIVE / INVALID_TEST`

** Justification:** ...

## Q9. Scientific-philosophy continuation review

**Activation:** `ACTIVATED` as soon as a material revision or empirical continuation is considered after `FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE`, or `INVALID_TEST`; `NOT_ACTIVATED_NO_CONTINUATION`.

**Review ID after `schemas/scientific_philosophy_review.schema.json`:** ...

**Frozen Q8 result unchanged?** `YES / NO → FAILED`

| Level | Entry |
|---|---|
|Core claim of the research program| |
|Protective belt/auxiliary assumptions| |
| Attribution of failure | `NON_UNIQUE / UNIQUE_IDENTIFIED / UNRESOLVED` |
|Different evidence for clear attribution| |
| Anomaly status | `ISOLATED / RECURRING / PROGRAM_LEVEL / UNRESOLVED` |
|Is there a viable rival program?| `YES + reference / NO; no positive evidence for the old claim` |

| Revision ID |modified bundle link|New prediction set not previously implied| Falsifier |Independent evaluation plan| Classification |
|---|---|---|---|---|---|
| | | | | | `PROGRESSIVE / DEGENERATIVE / DIAGNOSTIC_ONLY / UNRESOLVED` |

**Continuation decision:**
`NO_CONTINUATION / NEW_RESEARCH_ID / DIAGNOSTIC_ONLY / SUSPEND_JUDGMENT / RETAIN_PROGRAM_PROVISIONALLY / RIVAL_PROGRAM_REQUIRED`

**For `NEW_RESEARCH_ID`:** selected progressive revision ID and new research ID: ...

A new ID alone is not enough. Without new refutable prediction and independence plan, no empirical continuation is authorized. Diagnostics must not relabel the old Q8 result into success.

---

# R. Final holdout / external walk-forward

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED`

## R1. Holdout never viewed before?

`YES / NO`

If no, no final holdout.

## R2. Result

...

## R3. Conclusion

...

---

# S. Robustness and replication

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED`

| Test |Result| Conclusion stable? |
|---|---|---|
| Adjacent parameters | | |
| Other periods | | |
| Other symbols | | |
| State ranges | | |
| Forward horizons | | |
|Alternative permitted DAGs/identification assumptions, if causal| | |
|Other event windows according to Freeze| | |
|Source of expectation/vintage sensitivity| | |
| Reaction-innovation calibration | | |
|Without a dominant cluster| | |
|Without a dominant symbol| | |

---

# T. Phenomenon decision

`NO_PHENOMENON / INCONCLUSIVE / CANDIDATE_HYPOTHESIS / VALIDATED_PHENOMENON / REJECTED`

** Justification:** ...

**Important:** Only at `VALIDATED_PHENOMENON` can Strategy Engineering start as a regular next step.

**Strategy engineering as the next step explicitly decided?** `YES / NO`

**POST-T-BLOCKSTATUS:** `ACTIVATED / DEFERRED_AFTER_VALIDATION / NOT_ACTIVATED_BY_T_GATE`

`ACTIVATED` is only allowed at `VALIDATED_PHENOMENON + YES`. For `VALIDATED_PHENOMENON + NO`, `DEFERRED_AFTER_VALIDATION` applies; without a validated phenomenon, `NOT_ACTIVATED_BY_T_GATE` applies. In the two non-activated states, `U–Y` are not processed field by field; Section `Z` will continue.

---

# U. Strategy engineering

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED`

## U1. Validated phenomenon to be implemented

...

## U2. Setup

...

## U3. Trigger

...

## U4. Invalidation

...

## U5. Entry

...

## U6. Stop

...

## U7. Target

...

## U8. Management

...

## U9. Position size / risk model

...

## U10. Detailed conditional cost model

|State/execution condition|Fees| Spread | Slippage | Funding | Total cost |
|---|---:|---:|---:|---:|---:|
| | | | | | |

## U11 Capacity/Liquidity

...

## U12. Planned entry/exit diagnostics

| Item | Store? |
|---|---|
| MFE | |
| MAE | |
| Time to MFE | |
| Time to MAE | |
| Time to stop | |
| Time to target | |
| Exit reason | |

---

# V. Prerequisite Tree / Transition Tree

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED`

## V1. Implementation constraint register

**Defined system objective:** `executable risk-adjusted net performance / specify`

| Candidate | Type |How does it limit the system objective?| Evidence | Controllable? |Next action| Falsification criterion |
|---|---|---|---|---|---|---|
| | `data/latency/liquidity/cost/process` | | | | | |

**Current `IMPLEMENTATION_CONSTRAINT`:** ... / `NONE_IDENTIFIED`

## V2. Implementation obstacles

| Obstacle | Necessary intermediate objective |
|---|---|
| | |

## V3. Transition tree

|Step| Action | Expected new state |Test|
|---|---|---|---|
| | | | |

---

# W. Complete strategy – renewed OOS/Forward test

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED`

| Field | Entry |
|---|---|
| OOS/forward dataset | |
| Data role | |
| Cost-model version | |
| Number of nominal trades | |
| Effective cluster count | |
| Net Expectancy | |
| Drawdown | |
| MFE/MAE diagnostics | |
| Process deviations | |
|Result| |

---

# X. Activation gate

**PHASE STATUS:** `COMPLETE / BLOCKED / FAILED`

| Gate | PASS/FAIL/BLOCKED |
|---|---|
|Phenomenon validated| |
| Strategy engineering frozen | |
|Complete strategy OOS passed| |
|Costs realistic| |
|Total risk/position size logic| |
| Process reproducible | |
| Degradation rules predefined | |

**Decision:** `ACTIVE_STRATEGY_CANDIDATE / ACTIVE / NOT_ACTIVE`

---

# Y. Forward-OOS and degradation

**PHASE STATUS:** `COMPLETE / N/A / BLOCKED`

## Y1. Predefined warning/suspension rules

| Level | Warning threshold | Suspension threshold | Revalidation criterion |
|---|---|---|---|
| statistical | | | |
| economic | | | |
| State/Regime | | | |
| Event/Reaction Innovation | | | |
|Identification diagnosis, if causal| | | |
| process | | | |

## Y2. Ongoing monitoring results

|Period| N | Effective N/cluster | Expectancy |Costs| Drawdown | State mix | Reaction-innovation calibration | Event contamination |Process quality| Status |
|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| | | | | | | | | | | |

---

# Z. Decision and version protocol

| Date | Research version | Phase |Decision|Justification|Data that was consumed| New status |
|---|---|---|---|---|---|---|
| | | | | | | |

## Z1. Preliminary noted reasons for rejection

These reasons are noted **before** the relevant test.

1. ...
2. ...
3. ...

## Z2. Final decision

**Current/final status:** `NO_PHENOMENON / INCONCLUSIVE / CANDIDATE_HYPOTHESIS / IN_TEST / VALIDATED_PHENOMENON / ECONOMICALLY_UNTRADEABLE / ACTIVE_STRATEGY_CANDIDATE / ACTIVE / UNDER_OBSERVATION / SUSPENDED / REVALIDATED / REJECTED`

**Next process decision:** `CONTINUE / NEW_VERSION / MORE_DATA / ABORT / N/A`

**If Q9 `NEW_RESEARCH_ID`:** new Research ID and progressive revision ID: ...

** Justification:** ...

---

# Final check for the AI agent

The agent must not designate the activated part of the research artifact as complete until it has explicitly answered the relevant questions. After an early `FAIL`, checkpoints collected behind the aborted gate are considered `NOT_REACHED_DUE_TO_FAILED_GATE`; They do not require artificial individual responses.

## Achieved research path `A–T` and always active protocol `Z`

- [ ] Was the raw idea with origin, scope, alternative explanations, data requirements and spent information budget recorded in the hypothesis inbox?
- [ ] Was the intake before phase 0 `PROMOTED`, without issuing a promotion as evidence confirmation?
- [ ] Are the venue, trading phase, calendar/DST, time base, horizon and event class unique?
- [ ] Is the news/macro policy operationalized and are `FILTER_KNOWN_EVENTS` feeds, exclusion windows and coverage gaps documented?
- [ ] Are `mechanism_supported`, `forward_predictive_oos` and `executable_net_edge` run separately and not automatically upgraded?
- [ ] Was phase 0 carried out?
- [ ] Does minimum N come from power/precision instead of from existing N?
- [ ] Was conservative planning dispersion and a stress scenario used instead of just one Discovery point estimator?
- [ ] Are all dataset roles correct and contaminations logged?
- [ ] Is the claim level explicitly declared as predictive, interventional or counterfactual?
- [ ] Do causal claims have a precise estimand, an identification strategy, documented assumptions and `E7 PASS`?
- [ ] Were Granger/Causal Discovery results interpreted only within their assumptions and not as automatic causal proof?
- [ ] Was the tooling router applied and `TOOLING_REQUIRED / TOOLING_NOT_REQUIRED / TOOLING_BLOCKED` justified?
- [ ] Was executable causal analysis using a suitable specialized library instead of an untested self-implementation?
- [ ] Are runtime, exact package versions, main APIs, seeds, splits, alerts and environment reproducible logged?
- [ ] Was a library output not treated as a substitute for identification or as an automatic claim level upgrade?
- [ ] If there is a versioned SCM/DAG, potential-outcomes design,
structural econometric or other explicit identification model or `NOT_REQUIRED_PREDICTIVE`?
- [ ] Is the observability time documented for each predictor variable?
- [ ] Are confounders known before shock/treatment and post-treatment mediators not accidentally used as total effect controls?
- [ ] Are Expectation Source, Vintage, Surprise Formula, Time Stamp, Event Window and Contamination Rule frozen at Event Research?
- [ ] Are the number, construction and interpretation of the Surprise factors frozen and counted to the research search space?
- [ ] Was the simplest adequate shock-response regression used first?
- [ ] Is a `INFORMATION_BOTTLENECK_CANDIDATE` based on a predefined time M0/M1-OOS comparison?
- [ ] Were the information bottleneck, causal leverage and implementation constraint linguistically separated?
- [ ] Is `Expected − Actual` described as a reaction innovation and only in the identified chain as causal break?
- [ ] Is the null model explicit?
- [ ] Are the effect size and uncertainty given?
- [ ] Was effective N assessed instead of only nominal N?
- [ ] Have cluster/overlap/correlation been tested?
- [ ] Was `SMALL_CLUSTER_WARNING` triggered and methodically handled in less than 30 independent clusters?
- [ ] Are Influence Diagnostics Predefined?
- [ ] Is heavy tail treatment predefined?
- [ ] Is multiple testing documented?
- [ ] Did the full pipeline pass the integrity gate before Freeze?
- [ ] Are Prediction List and Pre-Mortem Completed?
- [ ] Is the freeze complete?
- [ ] Was validation really independent?
- [ ] Were OOS/backtest success and causal identification assessed separately?
- [ ] Was an imprecise result not used as an occasion for result-driven revision?
- [ ] Was an opposite sign treated as a new hypothesis?
- [ ] If continued after a non-positive Q8 result, was the tested bundle disclosed, the old result left unchanged and only a progressive revision with new prediction, falsifier, independent evaluation plan and new research ID authorized?
- [ ] Was the `Z` section maintained throughout the research process?

## `POST-T-BLOCKSTATUS: ACTIVATED` – Strategy Engineering `U–Y`

- [ ] Was the economic feasibility checked in detail by phenomenon validation?
- [ ] Has the full strategy been reviewed again OOS/Forward?
- [ ] Are degradation and shutdown rules defined before activation?

## Operational agent artifacts

- [ ] Was a valid orchestration state stored and a valid routing decision generated before each material research transition?
- [ ] Were mandatory specialist agents only called with a limited work order, their results checked before takeover and then routed again?
- [ ] Is there a validated causal identification assessment for each interventional or counterfactual claim before estimation and causal language?
- [ ] Does every persistent crude idea have a valid, versioned hypothesis-intake artifact?
- [ ] Does each actual LLM/agent run have a unique Run ID and a valid Run Manifest?
- [ ] Are model/snapshot, prompts, parameters, tools, data statuses, source statuses and output hashes reproducibly referenced per run?
- [ ] Does every decision-relevant statement have a claim ID and an epistemic class?
- [ ] Are `SOURCE_FACT` claims with a specific source and reference?
- [ ] Has relevant finance research documented the coverage of Journal of Finance, Journal of Financial Economics, arXiv `q-fin` and other relevant primary sources?
- [ ] Does each academic source have a `work_id`, its own `source_id` for the specific version used as well as publication status, study type, authors, venue/DOI or arXiv-ID/category/version?
- [ ] Were versions and indices of the same `work_id` deduplicated and not counted as independent confirmations?
- [ ] Are preprints and working papers marked as preliminary without deriving a quality upgrade from arXiv category or journal prestige?
- [ ] Have Correction, Expression of Concern, Retraction and Withdrawal been tested with Test Method, Time and, if applicable, Notice URI?
- [ ] Are code, data and independent replication statuses and references logged?
- [ ] Do `CALCULATED_VALUE`, `ESTIMATE`, `INFERENCE` and `FORECAST` reference their input claims and methods?
- [ ] Are source conflicts, lack of evidence and `UNKNOWN` visible without linguistically smoothing them?
- [ ] Are human reviews and overrides append-only logged and protected against silent overwriting?
- [ ] Was the versioned Eval and Regression Gate passed after material agent changes?
- [ ] Do all entries in the operational artifact register match their stored hashes and status values?

## Gate consistency

- [ ] In case of an early gate termination: Were all subsequent sections that can no longer be reached marked once as `NOT_REACHED_DUE_TO_FAILED_GATE` and `Z` completed?
- [ ] For `BLOCKED`: Were subsequent sections untouched and were blockers/missing information logged in `Z`?
- [ ] Were `U–Y` only activated after passing T-Gate?
- [ ] For `DEFERRED_AFTER_VALIDATION` or `NOT_ACTIVATED_BY_T_GATE`: Were `U–Y` left closed instead of being artificially filled with single `N/A`?
