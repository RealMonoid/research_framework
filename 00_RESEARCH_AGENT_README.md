# 00_RESEARCH_AGENT_README.md

**Version:** 2.5
**As of:** 2026-08-31
**Status:** DRAFT FOR ADOPTION
**Purpose:** Binding reading and execution instructions for AI agents handling trading research projects.
---

## 1. Staggered entry and document router

Every new idea starts with `QUICKSTART.md` and an intake after `schemas/hypothesis_candidate.schema.json`. If no raw idea exists yet, `scripts/generate_hypotheses.py` can optionally convert the versioned catalogue `generation/mechanism_catalog.v1.json` into cheap `INBOX` candidates. This generator is a production layer and does not make a screening, evidence, backtest or promotion decision.

For `INBOX`, `MERGED` or `REJECTED`, the six detailed documents do not have to be preloaded. The short intake nevertheless records origin, raw idea and already consumed information references.

Only a `PROMOTED` intake opens phase 0; promotion is not evidence. Then `00_RESEARCH_AGENT_README.md` and `01_RESEARCH_STANDARD.md` are loaded. `02_RESEARCH_CASE_TEMPLATE.md` is used when creating the specific research case. From `03_RESEARCH_METHODS.md`, `04_CAUSAL_TOOLING.md` and `05_AGENT_OPERATIONS.md`, only the sections activated by method, claim level and created artifacts are loaded.

Each actual agent run receives a valid run manifest validated against `schemas/run_manifest.schema.json`. Decision-relevant statements, human reviews and real eval results are listed as separate operational artifacts according to `05_AGENT_OPERATIONS.md` and referenced in the research case.

The sections `U–Y` of this copy remain inactive in section `T` until a passed phenomenon decision. After `VALIDATED_PHENOMENON` they are activated only by an explicit continuation decision. Otherwise, `VALIDATED_PHENOMENON` remains a permissible stand-alone end state and the block is marked `DEFERRED_AFTER_VALIDATION`. If `T` is not completed as `VALIDATED_PHENOMENON`, the block is marked `NOT_ACTIVATED_BY_T_GATE`. In both cases, the individual fields are not filled with a series of `N/A` entries. Section `Z` remains active from the start because decisions, versions, and rejection reasons must be logged throughout the research process.

The files perform various functions:

| File | Function | When to load? |
|---|---|---|
| `QUICKSTART.md` |Short path, enforcement boundary and status router|Always|
| `generation/mechanism_catalog.v1.json` |Literature-based mechanisms for intraday and short swing ideas|When creating ideas or expanding the catalogue|
| `generation/README.md` |Operation and limits of the generator|In the case of a generator run|
| `agents/intraday-hypothesis-generator.md` | Optional autonomous generator contract |In the case of agentic idea generation|
| `agents/scientific-philosophy-critic.md` |Concept and requirement review before operationalization, plus Duhem-Quine/Lakatos/Kuhn continuation review|Before completion of any incompletely defined source reconstruction; after a non-positive Q8 result when material revision or continuation is considered|
| `agents/condition-inquiry-analyst.md` |Quantitative assessment of measuring instruments and generation of observable condition hypotheses|After provisional operationalization, when measurement value, definition dependence or unknown success modifiers are examined|
| `agents/causal-identification-critic.md` |Independent examination of whether a financial-market design supports the intended causal statement|Before any interventional or counterfactual estimate and before causal language; not for purely predictive questions|
| `references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md` |Versioned research basis for financial market-specific identification risks|At each causality test|
| `reconstruction/README.md` |Source-based translation of book/article/video/course strategies|When a source strategy is not fully operationalized|
| `00_RESEARCH_AGENT_README.md` |Routing, gate and non-skip rules|From `PROMOTED`|
| `01_RESEARCH_STANDARD.md` |Normative research standard|From `PROMOTED`|
| `02_RESEARCH_CASE_TEMPLATE.md` |Operational working artifact per Research ID|When opening a research case|
| `03_RESEARCH_METHODS.md` |Selection of methods and rules of engagement|Only selected method sections|
| `04_CAUSAL_TOOLING.md` |Router for executable causal core operations|At `TOOLING_REQUIRED`|
| `05_AGENT_OPERATIONS.md` |Provenance, Evidence, Reviews, Evals and Release|Appropriate sections for the respective artifacts/system changes|
| `schemas/` |Machine-readable artifact contracts|Once the artifact type is created|
| `evals/` |Producer, scorer and regression gate|For agent/prompt/model/tool changes|
| `decisions/` |Architectural decisions and consequences|In case of affected decision|

## 1.1 Enforcement boundary

An agent who writes `COMPLETE`, `PASS` or `SUPPORTED` does not prove anything. These values are self-declarations unless the associated artifact has been verified against a schema, the evidence reference has been resolved, or an independent review documented. Normative prose controls behavior but is not technical enforcement.

Automatically enforced are only explicitly named schemas, tests, eval gates, and CI checks. A green `PROTOCOL_SMOKE` only confirms contracts and scorers. A statement about model or prompt quality requires a blindly produced `LIVE_AGENT` run.

This package does not automatically replace active project rules. A formal activation in the trading project takes place only after the planned version and release logic.

## 1.2 Understandable user communication is mandatory

The user is treated as a professional decision maker, not a software developer. Internal precision and external language are two separate levels: artifacts, schemas, logs and tests retain their exact terms; the visible user response translates their meaning into ordinary language.

Every user response MUST:

- begin with result, meaning and a possible open decision,
- avoid technical terms or explain them simply when they are first used,
- translate internal codes into everyday language,
- omit technical implementation details unless they contain a result, risk, or information that changes the user's decision,
- for a necessary decision question, explain the occasion, options, practical consequences, and a reasoned recommendation,
- say clearly if the user does not have to decide or do anything technically.

The Agent SHOULD NOT output function, class, adapter, import, schema, CI or test details as a progress or final report unsolicited. File names and internal status fields are only mentioned if the user requests them or really needs them for traceability. The fact that an agent has implemented or checked something is no reason to burden the user with the technical way there.

This rule also applies to statistical, causal and scientific-philosophical terminology. The precise designation may remain internally; externally, it must first be explained what it means in the specific case.

## 1.3 Binding head of research and executable routing

Each user-side research task has exactly one responsible research conductor according to `agents/research-conductor.md`. The conductor remains the only voice to the user, records the current state of work, and does not freely decide whether a prescribed technical examination takes place.

Before each material transition, an `orchestration_state` is stored and validated against `schemas/orchestration_state.schema.json`, then transferred by `scripts/route_research_task.py` into exactly one next work order. The generated `routing_decision` is validated against `schemas/routing_decision.schema.json` and records at least:

- why this step is now permissible or necessary,
- which specialised agent may be required,
- what documents it may see,
- what it must not change or investigate,
- which outcome is expected and when it must stop,
- which step is mandatory afterwards.

The fixed router decides on objective conditions. The research lead remains responsible for the substantive classification of the user intention and the source status. Uncertain classification is stored as such; a material user decision must not be invented by the router.

Specialised agents work as bounded tools of the research conductor. They do not have their own user conversation, do not determine the overall status and may not extend the research mandate. After each contribution, the conductor checks the required artifact, updates the work status and routes again. If a mandatory specialist agent is technically not available, the step `BLOCKED` remains; the conductor may not simulate its contribution and at the same time declare that it was made.

Before each material research step, the full effective research fingerprint is recorded. It includes not only research question, strategy, market, time horizon, trigger and goal, but also operationalizations, parameters, lookbacks, filters, exclusions, data roles, evaluation rules, cost and execution assumptions, frozen results and the checksums of the effective documents. After the work step, `scripts/check_research_fingerprint.py` compares the entire fingerprint. Only `UNCHANGED` allows acceptance.

The original status shall remain valid for any deviation. The change is stored visibly with its exact paths as `CHANGE_PROPOSED` and explained to the user with its practical consequence. Only an explicit decision may turn it into a new Research ID or Research version. An existing state is never quietly overwritten. This rule also applies to material work performed by the conductor.

In particular, for an incomplete prose strategy, the source is first reconstructed, then the concept and prerequisite examination is carried out by the `scientific-philosophy-critic`, and only then is it operationalized. This procedure does not authorize a backtest.

Once the strongest intended claim is `INTERVENTIONAL` or `COUNTERFACTUAL`, the `causal-identification-critic` is mandatory before estimation and causal wording. The critic examines the estimand, source of identifying variation, economic model, assumptions, financial-market-specific distortions, falsification checks, and sensitivity. DML, local projections, event-study regressions, temporal ordering, and causal discovery do not replace this review. An explicitly predictive project is not forced into this additional route as a precaution.

---

## Rules of source and jurisdiction

This research package regulates the development and validation of new market phenomena, edge hypotheses and strategies.

It does not replace operational trading rules from:

- `Trading_System.md`
- `Projekt-Workflow.md`
- `Chart_Indikator_Settings.md`
- `ACTIVE_DOCUMENTS.md`
- `Masterjournal.md`
- `ChangeLog.md`
- `LLM_README` of the native trading journal

In case of conflicts with active project rules, the existing project hierarchy applies. New research results are **not active trading rules** until formally activated after the project process.

---

## 3. No skip protocol

The agent may not silently omit any phase within the path activated by status and router. Unenabled methods or artifact types do not generate artificial series of `N/A` entries.

For each phase, the research artifact must contain exactly one of the following states:

- `COMPLETE` – fully processed.
- `N/A` – not materially applicable; justification is mandatory.
- `BLOCKED` – required but not currently executable; missing information or resource must be named.
- `FAILED` – gate or criterion failed.

If a current Research version is terminated by a gate, all subsequent sections which can no longer be reached thereby receive the block status `NOT_REACHED_DUE_TO_FAILED_GATE` once; they are not artificially filled in individually. Section `Z` remains active for conclusion and justification.

`BLOCKED` does not terminate the Research version. Dependent follow-up sections remain untouched, section `Z` logs blockers and missing information, and the same version may not be continued until the blocker has been resolved. `NOT_REACHED_DUE_TO_FAILED_GATE` is used only after `FAIL`.

`N/A` without justification is inadmissible.

The only block exception is the expressly conditional post-T area `U–Y`: `NOT_ACTIVATED_BY_T_GATE` or `DEFERRED_AFTER_VALIDATION` replaces the individual statuses of these five sections. This is not skipping, but the predefined gate sequence.

An agent may not jump from `BLOCKED` to a later phase out of convenience if the blocked phase is a requirement.

---

## 4. Gate rule

The research pipeline contains real gates. A failed gate must not be linguistically relabeled and skipped into an “interesting observation”.

Gate and phase status are fixedly coupled:

- `Gate PASS → Phase COMPLETE`
- `Gate FAIL → Phase FAILED`
- `Gate BLOCKED → Phase BLOCKED`

After `FAIL` or `BLOCKED` no dependent follow-up step is allowed.

Binding gates are at least:

1. **Phase-0 feasibility gate**
2. **Causality/Identification gate** as soon as an interventional or counterfactual claim is made
3. **Measurement/leakage gate**
4. **Pipeline integrity gate**
5. **Freeze-completeness gate**
6. **Validation-independence gate**
7. **Economic-feasibility gate**
8. **Activation gate**

For purely associative or predictive research, the identification status is `NOT_REQUIRED_PREDICTIVE`; this is not causal `PASS` and does not allow causal language.

If a gate is `FAILED`, the current Research version ends. A continuation, depending on the case, requires:

- more data,
- a new research version,
- a new hypothesis,
- or an abort.

## 4.1 Conceptual and prerequisite testing before operationalization

A strategy reconstructed from incomplete prose may not be completed as `RECONSTRUCTION_COMPLETE` or `DISCRETIONARY_PROTOCOL_COMPLETE` before the `scientific-philosophy-critic` has created a `strategy_concept_audit` after `schemas/strategy_concept_audit.schema.json`.

The audit separates strategy-defining conditions, application conditions cited by the source, suspected success modifiers, and unknown success conditions. Suspected or unknown conditions must not enter the source strategy as a mandatory filter.

Trigger, state, target and outcome are checked for common raw data, windows and deterministic calculations. Such a design dependence can create an association with or change the answered question. It is neither causal nor automatically a mistake.

Regime, state and context filters are considered as preliminary measuring instruments. Their class frequency does not measure separation performance. Even a later prognostic separation does not prove a literally real hidden state, actor or mechanism.

After preliminary operationalization, a `condition_inquiry` can be activated after `schemas/condition_inquiry.schema.json`. It can generate new condition hypotheses. Conditions found from data are maintained as new success-modifier hypotheses and are not retroactively issued as part of the source strategy.

## 4.2 Scientific-philosophy continuation review

`FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE` and `INVALID_TEST` remain results of the frozen Research ID. They are not relabelled by the fact that, after the result, an operationalization, auxiliary assumption or sample appears suspicious.

As soon as a material revision or a new empirical test is considered after such a Q8 result, the agent contract `agents/scientific-philosophy-critic.md` must be loaded and an `scientific_philosophy_review` to `schemas/scientific_philosophy_review.schema.json` created. The review:

- makes the tested bundle visible according to Duhem-Quine,
- does not claim a single cause of error without distinguishing evidence,
- separates progressive, degenerative, and purely diagnostic changes according to Lakatos,
- and uses Kuhn’s anomaly/rival perspective only to assess the research program, never to rescue the frozen individual test.

Empirical continuation is only allowed as a new Research ID if the revision records a previously unimplied, rebuttable prediction and an independent evaluation plan. Diagnostics may locate errors, but does not validate either the old or the new hypothesis.

---

## 5. Data roles are immutable

Each data set must have a role:

- `DISCOVERY`
- `DEVELOPMENT`
- `VALIDATION`
- `FINAL_HOLDOUT`
- `FORWARD_OOS`

A data set whose result has influenced any design decision is **Development Data** as of this date.

This also applies if only:

- a threshold change;
- adapted a state filter,
- an exit is modified,
- changed a null model,
- changed an outcome,
- modified a data split,
- selected a new robustness metric.

was changed.

A used validation set may not be further referred to as independent validation.

---

## 6. Nuclear rule against statistical self-deception

The agent must never infer `number of independent observations` from `number of trades` automatically.

The agent must actively check for:

- serial dependency,
- overlapping forward horizons,
- repeated signals from the same market impulse,
- event/session clusters,
- highly correlated symbols,
- shared macro events,
- dominant individual observations or clusters.

If dependency is plausible, the inference method must be adjusted or the restriction must be explicitly reported as `BLOCKED`.

For less than 30 plausibly independent clusters, an additional `SMALL_CLUSTER_WARNING` is set. This is **not an automatic FAIL** and not a claim that each interval is then necessarily too narrow. The warning status requires a method suitable for a few clusters, a design-specific simulation/calibration or an explicit classification as `BLOCKED`.

## 6a. No raw idea without intake and scope

An idea generated by observation, paper, LLM, secondary source or market history is initially `INBOX`. In this state, the agent logs only identity, origin, raw idea, and already consumed information references. Duplicates are brought together, not counted as independent ideas. Scope, observable footprint, alternative explanations, data requirements and early feasibility hurdles are gradually supplemented and are only completely mandatory for `PROMOTED`.

Before `PROMOTED`, an observation-driven idea requires a linked noise screen with status `PASS / FAIL / BLOCKED`. Its search space register fixes candidate universe, family size, alpha and correction method before the first result. A waiver is only allowed for theory-driven, terminated event or published replication ideas with justification. `PASS` allows Phase-0 effort and is not evidence. Schema plus `scripts/validate_entry_thresholds.py` enforce time order, quotient, register matching and multiplicity. For more than one planned screen, a correction is mandatory; `NONE_JUSTIFIED` is only allowed for a one-test family.

For intraday ideas, market/instrument, venue/feed, trading phase, calendar/time zone/DST, clock or event time horizon, and event class are mandatory. The news/macro policy is declared as `INCLUDED_AS_SIGNAL`, `NOT_USED_AS_SIGNAL`, `FILTER_KNOWN_EVENTS` or `SCHEDULED_EVENT_STUDY`. Only `FILTER_KNOWN_EVENTS` with named feeds, exclusion windows and coverage gaps allows a qualified statement about excluded known events.

`PROMOTED` also requires a record for variable and construct selection. For `PREDEFINED` a brief justification and the retained variables are sufficient. For `DATA_DRIVEN` or `HYBRID`, the candidate universe, selection data and their data role, outcome visibility, selection methods, effective candidate number, search space and selection bias controls are logged. Any information used is simultaneously recorded in `consumed_data_refs`; independent validation or holdout data must not affect the selection.

In addition, `PROMOTED` requires an `actor_constraint`. It contains either actor, coercion, expected action, observable reference and at least one competing actor hypothesis or explicitly documents `UNSPECIFIED / NOT_CLAIMED`. The second state is allowed for limited associative/predictive questions and prevents an actor from being invented; it does not provide any proof of mechanism.

The agent leads separately:

- `mechanism_supported`,
- `forward_predictive_oos`,
- `executable_net_edge`.

None of these stages is derived from an earlier stage. In particular, a plausible or published mechanism is not an automatic forward forecast and not a tradable net edge.

These three statuses form a different axis than the research claim level `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`. An identified interventional effect may be economically non-tradable; a purely associative forecast, on the other hand, can have an executable net edge. Neither claim level nor stage status is derived from the other axis.

---

## 7. No research without phase 0

Before independent validation data is consumed, the economic-statistical feasibility must be checked.

Phase 0 consists of two mandatory tests:

1. **Early pre-examination** with conservative assumptions before large-scale discovery/development work or holdout consumption is justified,
2. **formal recalculation before Freeze**, after outcome, zero model, dependency, effective N and validation plan are fully specified.

An early `CONTINUE` allows only discovery and development. Independent validation remains blocked until `PASS` of the formal recalculation.

Required fields:

1. minimum economically relevant effect size;
2. typical outcome scale,
3. exploratory spread point estimator including uncertainty and source,
4. conservative planning dispersion or stress scenario,
5. provisional cost hurdle,
6. desired significance/error level,
7. target power or equivalent decision level,
8. separate values for economic boundary `δ_econ` and assumed planning effect `δ_plan` or a direct precision target,
9. required N or required independent information in the baseline and stress scenario,
10. available nominal N and conservative lower limit of effective N,
11. Decision: `CONTINUE / OBTAIN DATA / ABORT`.

The minimum sample must **never** be derived from the number of cases returned by a particular data export.

A single spread point estimator from a small, selected, or non-transferable discovery sample is not sufficient for `CONTINUE`. Depending on the design, for example, external or pooled references, a model-valid upper uncertainty limit, robust scale measures with a justified stress surcharge, or a predefined scenario calculation are permitted. At least basic and conservative stress scenarios must be reported.

The stress scenario rule is set before the calculation. Among several pre-eligible and factually transferable candidates, the gate uses the most conservative value or reports the full bandwidth. A robust scale measure may only be used if it is traceably mapped to the primary estimator sample distribution. In the stress scenario, `DE < 1` or `N_eff > N` is not counted, unless this information gain is supported by external, transferable evidence and a predefined model.

If a classic formal test is used and there is no factually better basis for decision, two-sided `α = 0.05` and `Power = 80%` are considered **working defaults**. In the case of a tight final holdout or high cost of a false negative result, `90%` or a direct precision target should be tested. Working defaults are not a guarantee of quality; any deviation and any one-sided test must be justified before the result is known.

---

## 8. Temporal observability is mandatory

Each predictor, state and trigger variable must be documented:

- what raw data it needs,
- when it is fully known,
- whether it was actually available at the time of the decision,
- what the leakage/look-ahead risk is.

A reversed or subsequently confirmed chart marker is only considered known from its actual confirmation time.

If the observability cannot be reliably determined, the variable is not allowed for the formal test.

## 8a. Causal status and identification are mandatory fields

Each research version declares its strongest claim before the freeze as:

- `ASSOCIATIONAL_PREDICTIVE`,
- `INTERVENTIONAL`,
- or `COUNTERFACTUAL`.

`ASSOCIATIONAL_PREDICTIVE` is the default. An interventional or counterfactual claim additionally requires:

- a precise causal estimand,
- a versioned SCM/DAG, potential-outcomes design,
- a structural econometric or other explicit identification model,
- a named identification strategy,
- assumptions that cannot be derived from the data alone,
- negative controls, placebos or sensitivity analyses where design-specific,
- and an existing identification gate.

The choice between graphical, counterfactual or other explicit formulation is a modeling decision and does not increase the claim level. In the case of potential outcomes, in particular consistency, positivity, the assumption of assignment/exchangeability required for the design and interference or exposure mapping are explicitly treated. A DAG is not additionally mandatory there if the identification design explicitly makes the same relevant assumptions.

An LLM may propose competing DAGs, confounder candidates, instrument candidates, and testable consequences. It must not declare arrows as true on the basis of plausible prose.

The following results are in themselves **no** proof of causality:

- temporal ordering,
- Granger forecast improvement,
- conditional independence or causal discovery output;
- In-Sample-Fit,
- OOS stability;
- backtest profitability,
- Double Machine Learning.

DML and other flexible estimators may only be designated as causal estimators after the determination of the causal estimand and its identification assumptions. The `do(·)` operator is only allowed if an interventional quantity is actually identified.

In event research, publication value and shock are separated. The shock is constructed from an expectation available before the event; expectation source, data vintage, timestamp, scaling, event window and competing messages are logged.

A deviation between expected and actual market reaction is first called `REACTION_INNOVATION` or `REACTION_ANOMALY`. It may only be called `CAUSAL_CHAIN_BREAK` if the relevant chain including mediators has been causally identified and tested against predefined alternative explanations.

For quantitative event and transmission analysis, the defaults are:

- a few economically justified surprise factors,
- simple event-response regressions,
- state interactions known before the event,
- time-ordered OOS reaction innovations,
- and an incremental OOS comparison against a simpler zero model.

A chain link must not be declared a “constraint” solely because of high correlation, a large `|z|`, or a plausible story. The term is used only with a defined system goal and one of the following labels:

- `TRANSMISSION_DIAGNOSTIC` – descriptive pass-through or residual result,
- `INFORMATION_BOTTLENECK_CANDIDATE` – provides frozen and OOS additional forecast information for the end-outcome,
- `IDENTIFIED_CAUSAL_LEVER` – causal estimand and identification gate passed,
- `IMPLEMENTATION_CONSTRAINT` – data, timing, liquidity, cost, or process bottleneck.

`IDENTIFIED_CAUSAL_LEVER` and `IMPLEMENTATION_CONSTRAINT` are additionally tested against `schemas/constraint_assessment.schema.json`. Goldratt’s focus logic is only an optional thinking tool after phenomenon validation for already occupied `IMPLEMENTATION_CONSTRAINT` bottlenecks. It is not part of early market transmission or identification analysis.

## 8b. Specialized causal libraries are mandatory if appropriate

Once executable code is required for DAG verification, identification, causal effect estimation, refutation, or causal discovery, the agent must apply the router in `04_CAUSAL_TOOLING.md`. The default is a specialized, documented library instead of an ad hoc self-written implementation:

- `DoWhy` for the Model–Identify–Estimate–Refute workflow,
- `pgmpy` for graph, d-separation, adjustment and causal queries,
- `EconML` or `DoubleML` for DML or heterogeneous effects after existing identification,
- `Tigramite` for time series specific causal discovery,
- `causalinference` only optional for its narrow matching/propensity application range.

There is no package requirement for purely predictive event regressions or simple reaction innovations. The status is `TOOLING_REQUIRED`, `TOOLING_NOT_REQUIRED` or `TOOLING_BLOCKED` and is justified.

Library issues do not change the claim level. In particular, a found adjustment set, a DML estimator, a refutation test, or a discovery graph do not make a causal claim out of an unidentified question. Before execution, Python, package and API versions, random seed, splits, estimand, graph, adjustment set, and relevant warnings are logged. Untested package combinations require a compatibility smoke test; if it fails, `TOOLING_BLOCKED` applies.

An LLM does not have to be trained for this. Some estimators fit project-specific nuisance or effect models; this is an ordinary statistical estimate within the research pipeline, not training a new language model.

---

## Scientific sources require proven works, versions and integrity

Each academic source is also governed by **05_AGENT_OPERATIONS.md §5.4** and the Academic Metadata object in **schemas/evidence.schema.json**.

Required logic:

1. A **work id** combines preprint, working paper, accepted manuscript, version of record, correction and other versions of the same intellectual work.
2. Each version actually used has its own **source id**, exact version, URI, retrieval time and snapshot hash.
3. Multiple versions or indices of the same work id never count as independent confirmations.
4. Publication status, DOI, and venue are verified; a DOI or journal name is not proof of quality.
5. For relevant finance questions **The Journal of Finance** and the **Journal of Financial Economics** are searched specifically. This is a coverage rule, not a prestige gate and not an exclusion of other primary sources.
6. With arXiv, q-fin subcategory and specific version number are stored. Allowed are **q-fin.CP / q-fin.EC / q-fin.GN / q-fin.MF / q-fin.PM / q-fin.PR / q-fin.RM / q-fin.ST / q-fin.TR**. The category is subject classification, not peer review.
7. Before freeze, external release, and revalidation, corrections, expressions of concern, retractions, and withdrawals are reviewed via the publisher/journal, Crossmark/DOI metadata, Crossref Retraction Watch, and repository history.
8. Code, data, and replication statuses are recorded separately. Availability is not proof of quality; technical reproduction proves neither identification nor external validity.

A withdrawn or retracted work may no longer support the relevant material claim positively. Under Evidence Ruleset **1.1.0**, the claim becomes **INSUFFICIENT**, and the change is at least one operational **BREAKING** delta. A material correction, new arXiv version, modified deduplication, or conflicting replication requires a new claim, grade, and delta check.

If the source revision changes the hypothesis, design, gate or decision, the Research Version and Data Consumption Rules in Section 16 also apply. Pure bibliographic format corrections without semantic impact remain operational **NON MATERIAL** deltas.

---

## 9. No hidden hypothesis revision

An unexpected result must not be declared a success by semantic reinterpretation.

Example:

- Hypothesis: `Mean Reversion`
- Result: stable `Continuation` effect

Therefore:

- original hypothesis falsified,
- possible new hypothesis discovered,
- new Research ID or new main version required,
- new freeze and validation sequence is required.

---

## 10. Pipeline integrity testing is mandatory

Before the freeze, the **complete executable research pipeline** must be checked for control data. At least:

- repeated zero/surrogate runs that maintain the relevant time, cluster, state and volatility structure as far as methodologically possible;
- the same selection, filtering and evaluation steps as in real research,
- at least one known sign and timing synthetic test to detect sign, indexing and look-ahead errors;
- Predefined tolerances for false alarms, direction, timing and expected zero distribution.

The control base and data role are logged. Design-influencing pipeline tests must not consume independent validation or holdout data. For the zero controls, a target precision of the estimated false alarm rate shall be specified in advance; `PASS` requires sufficient Monte Carlo precision.

A single shuffle or random walk is not enough. If a control destroys the dependency structure relevant to the test, it must be adjusted or marked as insufficient.

The result is `PASS / FAIL / BLOCKED`. Without `PASS`, the freeze may not be confirmed.

---

## 11. Four outcome states instead of “significant / not significant”

A validation result must be placed in at least one of these states:

1. **Expected economically relevant effect supported with sufficient precision**
2. **Opposite economically relevant effect supported with sufficient precision**
3. **No economically relevant effect supported with sufficient precision**
4. **Imprecise / undecidable**

State 4 does not allow **a result-driven revision**. Only:

- more independent data,
- methodologically already defined additional analysis,
- Or discontinuation as undecidable.

---

## 12. Diagnostics of influence are mandatory

Before validation, it is determined how to check whether individual observations or clusters dominate the result.

At minimum:

- Leave-one-out or leave-one-cluster-out,
- result without dominant symbol,
- Result without dominant time/event group,
- Share of the largest observation/cluster in a predefined result or scatter variable.

If the removal of an individual cluster overturns the sign or the economic conclusion, the evidence is generally considered **not robustly confirmed**, unless the freeze expressly provides for another, factually justified rule.

---

## 13. Heavy-tail rule

For heavy-tailed outcomes, the following must be determined before validation:

- primary location parameter,
- robust sensitivity index;
- treatment of outliers,
- whether winsorisation/trimming is allowed,
- and whether this transformation is part of the primary or only sensitivity analysis.

The estimator may not be changed after knowledge of the validation result.

---

## 14. Cost logic in two stages

Costs are checked twice:

### Early: Phase-0 feasibility

Rough, conservative cost hurdle so that no tight holdout data is consumed for an effect that would be economically too small anyway.

### Late: Strategy Engineering

Detailed model that is as condition-dependent as possible:

`Costs = f(state, volatility, liquidity, size, speed, session, execution)`

The early cost gate does not replace the later execution exam.

The margin of safety is an **additional amount** added to the conservative cost estimate. If a multiplier is used instead, distinguish clearly between `total hurdle = multiplier × costs` and `margin of safety = multiplier × costs`. There is no universal cost multiplier for all strategies.

---

## 15. Internal working protocol and understandable user response

After each phase is completed, the agent must record the following **in the research artifact**:

```text
PHASE:
STATUS: COMPLETE / N/A / BLOCKED / FAILED
INPUTS:
DECISIONS:
OPEN ITEMS:
GATE RESULT:
NEXT PERMITTED STEP:
```

No phase ends with mere prose without status.

This block is not a mandatory format for the visible user response and is not reproduced there unasked. Instead, the agent summarizes the user in a concise and generally understandable way:

1. What was found?
2. What does this mean for the idea or investigation?
3. Does the user have to decide something? If so, what are the possibilities, practical consequences, and recommendation?
4. What is the next objective step?

Technical details, internal field names and status codes are only supplemented on explicit request or in case of decision-relevant impact.

---

## 16. Versioning

Each research file needs at least:

- Research-ID,
- Version,
- Status,
- creation date,
- Freeze date,
- data roles,
- structural-model/identification-design version,
- Tooling manifest with runtime, package and API versions or `TOOLING_NOT_REQUIRED`,
- hypothesis version,
- decision log.

Material changes create a new version.

In particular, material changes to:

- hypothesis,
- claim level or causal estimand,
- identification strategy or its core assumptions,
- primary causal library, main API, version combination or split/seed logic,
- surprise design, event window or reaction model,
- surprise factors, response model or constraint assessment,
- direction of the expected effect,
- null model,
- outcome,
- data universe,
- session,
- timeframe,
- state filter,
- Trigger,
- Invalidation,
- Stop,
- Target,
- Management,
- cost model,
- data split,
- primary evaluation method.

For academic sources, a new version, changed publication/integrity status, material correction, retraction/withdrawal, replication conflict, or deduplication with changed independent evidence is first an operational delta under **05_AGENT_OPERATIONS.md §5.4.8 and §9**. As soon as the hypothesis, method, gate, evidence conclusion, or final decision changes, the research change is material and creates a new version.

---

## 16a. Operational Agent Artifacts and Regression Gate

Research version and agent run are different identities:

- The **Research-ID/Research-Version** indicates the technical research status.
- The **Run-ID** denotes a specific execution of this status with a specific model, prompt, tool and data state.

For each LLM/agent run, the contracts from `05_AGENT_OPERATIONS.md` and `schemas/` apply in addition:

0. An optional generation run ends at `INBOX`; it must not anticipate screening or promotion. If an LLM or agent is used, that call also receives a run manifest.
1. Before opening a research case, a valid hypothesis intake is persisted and screened for `PROMOTED`.
2. A unique run ID is generated before execution; the run manifest is completely persisted at the latest at the end of the run.
3. Decision-relevant statements receive an epistemic class and a claim ID.
4. Facts require a specific source and reference; calculated values and inference claims reference their inputs.
5. Academic sources receive work id, concrete version, publication/integrity status, code, data and replication status; versions of the same work are deduplicated.
6. Missing evidence is reported as `UNKNOWN` or blocking evidence status and is not replaced by plausible prose.
7. Human corrections and overrides are stored append-only and must not be quietly overwritten.
8. Changes to the system/task prompt, model or snapshot, retrieval, tool description, orchestration or output schema require a passed eval and regression run before productive release.
9. A syntactically or semantically invalid obligatory artifact, an unexplained critical source collision or an unaccepted regression blocks the operational release, even if the research result sounds plausible in content.

A single run manifest does not replace the research case or its gates. Conversely, a methodically complete research case does not make a non-reproducible agent run operationally releaseable.

---

## 17. Closing rule

An AI agent may only designate a research idea as `VALIDATED_PHENOMENON` or `ACTIVE_STRATEGY_CANDIDATE` if the related research artifact has passed the prescribed gates.

`VALIDATED_PHENOMENON` only confirms the frozen phenomenon according to its design. The status does not increase the claim level, nor does it automatically set `mechanism_supported` or `executable_net_edge` to `SUPPORTED`.

Missing data, untested dependencies, a used validation set or an untested decision-making academic source version are not editorial details, but state errors of the research process.
