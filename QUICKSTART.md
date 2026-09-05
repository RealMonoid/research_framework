# Trading Research Framework – Quickstart

This short path is the only mandatory entry point for any new idea. The long standard documents are routed only by status and task; they no longer have to be loaded completely in advance into the context.

## Project mission

The project's applied goal is to identify or develop executable trading
strategies with a defensible positive expected net edge after realistic costs,
liquidity, slippage, capacity, execution, and risk. It accepts two primary
inputs: an existing strategy that must be reconstructed and tested without
changing its identity, or a request to generate and develop new strategy
hypotheses through a recorded search.

Every result also contributes bounded learning about representations,
mechanisms, conditions, measurements, methods, or failure modes. That learning
may guide later research but is not edge evidence for another strategy unless
it is separately tested. An individual case may correctly end with rejection,
inconclusive evidence, or non-testability; these outcomes protect the applied
mission rather than replacing it.

The interdisciplinary role boundaries are summarized in
[`INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md`](references/INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md).
The adopted mission and its limits are recorded in
[`ADR-016`](decisions/ADR-016-applied-interdisciplinary-trading-research-mission.md).

## Scope and restraint

This is a private decision-support framework for one research owner working
with AI agents. It is not an academic-publication workflow or a system for
making private strategies legible to an external audience. Retain a rule when
it protects a research or capital decision, or when it demonstrably makes such
a protection more reliable for the agents. Do not add process merely for
publication, external persuasion, or hypothetical team onboarding. When the
protective value of an existing rule is uncertain, keep it until the hard-gate
inventory, a real Research Case, or behavioural evaluation provides evidence
for removal.

Never place proprietary strategies, private data, real Research Cases, or
empirical results in the public repository. Use a separate private location or
the ignored `private_research/` path. Existing examples require a separate
privacy review before removal; uncertainty is not permission to delete them.

## Binding communication with the user

The framework is a tool for research and trading decisions, not a software project whose implementation details the user must track. Every agent must assume that the user is not a software developer.

The following rules therefore apply to any visible response:

1. **Result and meaning first.** The agent starts with what came out,
why it is relevant for research and whether something has to be decided.
2. **Use plain language.** Software terms, internal field names, function names,
file paths, schema names, test names, CI details, and technical architecture stay
out of the answer unless the user expressly requests them or they actually
change the user's decision.
3. **Translate specialist language too.** Explain unavoidable terms related to
statistics, causality, or market structure in one simple sentence when they
first appear. Internal status codes may be included, but never without their
meaning in everyday language.
4. **Make decisions ready for the user.** When the user must choose, the agent
states the concrete question and why it arises now, explains the available
options and their practical consequences, and gives a reasoned recommendation.
A list of internal options or codes is not enough.
5. **Keep technical work in the background.** After implementation, the agent
reports only what changed for the user, whether it was checked, what factual
limitation remains, and whether a decision is still open. Explain implementation
details only on request.
6. **No unsolicited implementation justification.** Do not describe how
functions were changed, imports added, adapters configured, or individual tests
named in the user response. For example, “The change is working and has been
checked” is sufficient. The user should not have to make decisions about those
implementation details.

The precise technical and scientific artifacts are fully preserved internally. This communication rule does not change a research rule; it only separates the internal documentation from the understandable response to the user.

### Mandatory step-by-step owner guidance

Every substantive response must make four points easy to identify in ordinary
language: where the research currently stands, what the framework or agent will
do next, what happens after that, and what the owner needs to do next. When no
owner input is needed, say that explicitly instead of leaving the next action
implicit. The routing decision carries this progress brief for every route so
that the conductor cannot treat a user decision as the only moment worth
explaining.

When an owner decision is genuinely required, present at least two options. For
each option, state its practical consequence and an assessment of
`RECOMMENDED`, `ACCEPTABLE`, or `NOT_RECOMMENDED`, then give one reasoned
recommendation. These are transparent decision weights, not invented
probabilities or claims of precision. Do not ask the owner to choose an
internal implementation detail that has no material research consequence.

When a problem occurs, explain the problem and the research step it prevents,
then offer at least two weighted recovery options and a recommendation. Before
the issue is reported as blocking or materially disruptive, create and validate
one separate `problem_record` file for that occurrence. It records the exact
model name and version, occurrence and recording timestamps, description,
practical impact, recovery options, and available orchestration references. For
a real Research Case, store each file under
`private_research/<research-case>/problems/`; retain only its stable reference
in the checkpoint. Do not overwrite the original problem description or work
around an unresolved issue silently. Use
`scripts/validate_problem_record.py` to validate the file before accepting it.

Routing and orchestration checkpoints use schema version 1.9.0 for this
workflow. Do not overwrite a version 1.7.0 or 1.8.0 checkpoint. Before an older
checkpoint is routed again, create a visible migrated checkpoint that preserves
its historical evidence, uses weighted option objects, references a separate
problem record for every blocker, and initializes `specialist_capability` to
`NOT_CHECKED` when no validated capability record exists.

## Binding data-fitness prerequisite

Apply the data-fitness rule in [`AGENTS.md`](AGENTS.md#data-acquisition-and-verification-burden)
before detailed operationalization and every empirical test. Confirm that the
available dataset can answer the exact hypothesis at the requested claim level;
record the evidence and remaining limits. Inadequate or unresolved material data
quality means the affected test must not start, even if a backtester can run.
The hypothesis remains untested with those data, not disproved. Cheap idea
intake may remain unassessed. This prerequisite applies now; the roadmap plans
only additional structured enforcement, not permission to postpone the rule.

## Binding research conductor

Each research task is guided by exactly one [`research-conductor`](agents/research-conductor.md). The conductor remains the user's contact, keeps the current status, and calls specialist agents only through a defined work order. Specialist agents do not take over the conversation or the overall decision.

The conductor permanently applies five basic controls on every task: the scope
stays tied to the request; delegation is one level deep; material conclusions
need validated evidence; an unchanged check is not repeated; and `COMPLETE`,
`PASS`, or `SUPPORTED` requires the corresponding evidence and validation. These
controls remain active even when no specialist is needed or AI Psychiatry is
unavailable.

Before each important transition, the work status is stored as [`orchestration_state`](schemas/orchestration_state.schema.json). The executable router [`route_research_task.py`](scripts/route_research_task.py) determines the next mandatory step. In particular, these sequences apply:

- incomplete prose strategy: source reconstruction → conceptual and
prerequisite review → only then operationalization;
- question about usefulness or unknown observable conditions:
completed concept review → preliminary operationalization → condition analysis;
- revision or continuation following a non-positive frozen result:
continuing scientific-philosophical examination before new empiricism;
- intended intervention or counterfactual statement:
  causality testing before effect estimation or causal formulation;
- concrete quantitative question that needs more than simple arithmetic:
  one bounded data-analysis report with provenance, quality checks and
  uncertainty; this does not authorize a backtest or trading decision;
- new ideas only on an actual request for ideation; an existing idea goes into
intake and not back to the generator.

A simple result statement does not automatically trigger a specialist agent. A necessary user decision will only be requested if it materially changes the research question, the identity of the source strategy, or the permissible claim. After each accepted specialist contribution, its artifact is checked, the work status is updated, and the task is routed again.

### Specialist capability preflight

When the router selects a specialist, the conductor first inspects the active
runtime's tool inventory and any available tool-search surface. It records that
inspection in a separate
[`specialist_capability_check`](schemas/specialist_capability_check.schema.json),
validates the record against the exact routing decision, and stores its
reference in the next checkpoint.

An internal agent run that returns to the conductor in the same conversation is
a valid invocation interface when it provides a separate bounded run, accepts
only the allowed context, returns its result to the conductor, and preserves the
one-level delegation and no-user-contact controls. A separate user-visible
window is not required. If any inspected interface satisfies the requirements,
the check must be `AVAILABLE` and the conductor must invoke it. `UNKNOWN` means
discovery is incomplete and must be retried; it cannot support a blocker. Only
a complete `UNAVAILABLE` result may lead to a linked problem record and blocked
route. Validate the check with
`scripts/validate_specialist_capability_check.py`.

### Conditional quantitative data analysis

When the user asks a concrete quantitative question whose answer would add
information beyond simple arithmetic, the conductor may call the bounded
[`data-analyst`](agents/data-analyst.md). It is not called just because a task
contains numbers. The analyst receives only the named data and returns a
[`data_analysis_report`](schemas/data_analysis_report.schema.json).

The report must show the source and snapshot, period, instrument, sampling
grain, variables and their availability at decision time, data role,
missingness, outliers, leakage/look-ahead, survivorship, dependence, and
session/regime separation where relevant. It must state uncertainty and what
the data cannot establish. Intraday and swing work remain separate, and costs,
slippage, liquidity, and in-sample/out-of-sample separation are required when
the question actually concerns a trading evaluation. Correlation is not
causality, and a single backtest is not validation.

The analyst cannot trade, recommend or change positions, override risk limits,
change the research question or rules, authorize a test, change the fingerprint
or checkpoint, address the user, delegate, repeat an equivalent check, or
schedule follow-up. Validate the report with
`scripts/validate_data_analysis_report.py`; then compare the full fingerprint
before accepting it. If data are missing or cannot be obtained as one coherent
dataset, keep the result `NOT_TESTABLE` or `BLOCKED` rather than silently
weakening the research question. This role does not replace the binding data-fitness prerequisite or its
planned structured enforcement.

Before and after each material research step, the full research fingerprint is compared. In addition to research question, source strategy, market and time horizon, it also contains measurement definitions, parameters, lookbacks, filters and exclusions, data and sample decisions, evaluation rules, cost and execution assumptions, frozen results and the checksums of all effective research documents.

A contribution is accepted only if [`check_research_fingerprint.py`](scripts/check_research_fingerprint.py) reports the complete state as `UNCHANGED`. Any deviation remains a visible change proposal. The old state is never silently overwritten; only an explicit user decision may turn it into a new research version.

### Conditional framework-control review

If the owner asks for a framework stress test, or a concrete trace suggests a
skipped check, reset attempt counter, repeated equivalent strategy, unjustified
scope change, instruction conflict, stale memory, or unexplained failure, the
conductor may use the [framework-control reviewer](agents/framework-control-reviewer.md).
It performs one bounded review of observable evidence and returns a structured
report. It does not diagnose people, run a backtest, alter the research state,
or add a universal step to every case. The optional AI-Psychiatry plugin may
provide these same provider-neutral review modes; it never overrides
`AGENTS.md`, and its use is never claimed when it was unavailable.

The report must pass
[`validate_framework_control_review.py`](scripts/validate_framework_control_review.py).
An applied correction needs a passing regression check. A material research
change remains a visible proposal under the full fingerprint process and still
requires the owner's decision. A clean review is a control diagnostic, not proof
that every live agent will behave correctly.

## 1. What is technically enforced – and what is not

| Level | Meaning |
|---|---|
| Machinery tested | JSON schemas, complete research fingerprints, schema contract tests, evaluation scorer, producer protocol, and CI checks can objectively pass or fail. |
| Evidence checked | A status such as `SUPPORTED`, `PASS`, or `COMPLETE` is reliable only when the required evidence/run artifact exists and its associated machine test passes. |
| Self-declaration | Prose, checklist markers, and a `COMPLETE` status set by the executing agent are initially claims. Without artifact testing or independent review, they do not prove correct execution. |

Normative language controls behavior but does not replace technical enforcement. The framework claims automatic enforcement only where a schema, test, or CI check is named.

## 2. Optional: Generate ideas

If no raw idea exists yet, the short-horizon executable generator may be used before the intake:

```bash
python scripts/generate_hypotheses.py --output-dir artifacts/ideas-001 \
  --run-id generation:ideas-001 --markets FUTURES --max-candidates 20
```

This is based on [`generation/mechanism_catalog.v1.json`](generation/mechanism_catalog.v1.json) and the four operators `PHASE_PATH`, `EXPECTATION_VIOLATION`, `MECHANISM_CONNECTION`, and `ASSUMPTION_RELAXATION`. The generation routes are constraint-first, microstructure state, instrument linkage, literature replication, and observation. A named forced actor is not a universal requirement.

The run writes a validated generation run and minimal `INBOX` files. The generator does not perform screening, backtesting, evidence grading, ranking or promotion. Details and filter options are available in [`generation/README.md`](generation/README.md).

The generation run documents the generated candidate space. If, for example, all 96 candidates are screened using data, a family with `planned_screen_count = 96` is fixed in [`schemas/search_space.schema.json`](schemas/search_space.schema.json) before the first result. The threshold of each [`noise_screen`](schemas/noise_screen.schema.json) must correspond to the multiplicity correction stored there.

## 2a. Optional: Reconstruct a strategy from a book, article, video, or course

If a source describes a setup but does not fully operationalize its terms and alternatives, create a [`strategy_reconstruction`](schemas/strategy_reconstruction.schema.json) before specifying it. The process separates source rules, recommendations, options, examples, discretion, and open definitions. Possible translations remain candidates; they are neither automatically chosen nor tested.

Before the reconstruction is completed, use the [`scientific-philosophy-critic`](agents/scientific-philosophy-critic.md) in pre-operationalization mode. Its [`strategy_concept_audit`](schemas/strategy_concept_audit.schema.json) separates:

- what defines the strategy;
- what the source names only as an application condition;
- what is only suspected as a success modifier; and
- which conditions for success remain unknown.

It also reveals shared calculation components and windows without treating them as causal evidence or automatic errors. Regime and state filters remain provisional measurement instruments: group frequency alone does not establish discrimination; predictive separation does not prove a real underlying state, an actor, or a mechanism.

After a preliminary operationalization, a [`condition_inquiry`](schemas/condition_inquiry.schema.json) can be activated. The [`condition-inquiry-analyst`](agents/condition-inquiry-analyst.md) can assess measuring instruments, make definition dependence visible, and generate new observable condition hypotheses. Conditions found from data remain new hypotheses; they are not written back into the source strategy.

The workflow is in [`reconstruction/README.md`](reconstruction/README.md). The completed [`VWAP price-discovery example`](examples/strategy_reconstruction.vwap_wave_price_discovery.json) deliberately ends as `SOURCE_EXTRACTION` with all decisions open. It is not a backtest and does not claim that the source is profitable.

## 2b. Only on a real causality question

A trading strategy can be fully studied as a forecast without claiming that a signal is causing the market. In this normal case, no additional causal-identification work is required.

On the other hand, as soon as an intervention, a structural shock, or a counterfactual is to be claimed, the [`causal-identification-critic`](agents/causal-identification-critic.md) must check whether the comparison carries this meaning at all. Its [`causal_identification_assessment`](schemas/causal_identification_assessment.schema.json) identifies target impact, the source of identifying variation, the economic model, assumptions, financial-market risks, negative controls, sensitivity, and the strongest allowable statement.

A model or estimator does not replace this test. This applies explicitly to DML, causal forests, local projections, VARs, event-study regressions, Granger procedures, and causal discovery. Financial event studies must cover, among other things, the counterfactual return model, event timing, volatility, and other news; high-frequency designs add leakage, timestamps, surprise construction, and information shocks. The mandatory research basis is in [`references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md`](references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md).

A successful identification gate permits only the specified causal estimate under its assumptions. Mechanism, prediction, and tradable net edge remain questions of their own.

## 2c. Freeze outcome meaning before validation

Before opening validation data, create a frozen
[`outcome_evidence_contract`](schemas/outcome_evidence_contract.schema.json).
It assigns every measurement a role and records which conclusion it may change.
It also exposes shared inputs or reference models, names the relevant
multiplicity family, and states what support, contradiction, a
non-discriminating result, or an invalid test would mean.

The contract is checked by
[`validate_outcome_evidence_contract.py`](scripts/validate_outcome_evidence_contract.py).
If a test is already marked frozen without a complete contract, the router
stops. The missing contract must not be reconstructed after validation results
have been viewed. See
[`06_OUTCOME_EVIDENCE_CONTRACT.md`](06_OUTCOME_EVIDENCE_CONTRACT.md) for the
plain-language rule and the worked example.

## 2d. Test the research pipeline before validation

After the outcome contract is complete and before a validation test is frozen,
create and assess a
[`pipeline_integrity_assessment`](schemas/pipeline_integrity_assessment.schema.json).
Run the unchanged complete pipeline on repeated structure-appropriate negative
controls and on a synthetic known-effect sentinel with fixed sign and timing.

The assessment records the exact pipeline fingerprint, simulation or surrogate
design, parameter source, seed policy, preserved and missing market structure,
repeat counts, uncertainty, and rules locked before the first run. One random
walk cannot be the only required negative control. A pass permits only the next
freeze step and supplies no evidence for the strategy, prediction, mechanism,
or after-cost edge.

The router stops if this assessment is missing, failed, or blocked. Validate it
with
[`validate_pipeline_integrity_assessment.py`](scripts/validate_pipeline_integrity_assessment.py).
The practical explanation is in
[`07_PIPELINE_INTEGRITY_CONTROLS.md`](07_PIPELINE_INTEGRITY_CONTROLS.md).

## 3. Cheap intake

A new idea starts as `INBOX` after [`schemas/hypothesis_candidate.schema.json`](schemas/hypothesis_candidate.schema.json). Initially, record only:

- stable IDs and timestamps,
- origin,
- the raw idea,
- information/data references already consumed,
- `intake_status = INBOX`,
- an empty `transition` object.

See [`examples/hypothesis_candidate.inbox.json`](examples/hypothesis_candidate.inbox.json). If the idea is discarded during screening, the short `REJECTED` record with a justification is sufficient; see [`examples/hypothesis_candidate.rejected.json`](examples/hypothesis_candidate.rejected.json).

Only `PROMOTED` requires complete scope, an explicitly documented actor status, a
passed noise screen or a well-founded theory-, event-, or replication-based
waiver, observable footprints, alternative explanations, data requirements,
early feasibility, the three separate evidence levels, and a record for
variable selection. For `PREDEFINED`, a justification and retained constructs
are sufficient. `DATA_DRIVEN` and `HYBRID` additionally require the candidate
universe, selection data and their role, outcome visibility, the method, the
effective candidate count, the search space, and controls against selection
bias. SHAP, impurity, and other feature-importance methods are possible
diagnostics, but they are neither mandatory nor evidence of causality. If no
actor can be identified with sufficient confidence for a purely predictive or
associative question, record `UNSPECIFIED / NOT_CLAIMED`. That does not block
this limited question, but it must not be read as evidence of a mechanism.
Promotion does not confirm an evidence level.

## 4. Document router by promotion

After `PROMOTED`, load documents selectively:

1. [`00_RESEARCH_AGENT_README.md`](00_RESEARCH_AGENT_README.md) for gate and routing logic.
2. [`01_RESEARCH_STANDARD.md`](01_RESEARCH_STANDARD.md) for the mandatory research path.
3. [`02_RESEARCH_CASE_TEMPLATE.md`](02_RESEARCH_CASE_TEMPLATE.md) only when creating the specific research case.
4. From [`03_RESEARCH_METHODS.md`](03_RESEARCH_METHODS.md), only the sections selected by the method router.
5. [`04_CAUSAL_TOOLING.md`](04_CAUSAL_TOOLING.md) only for an executable causal core operation; otherwise record `TOOLING_NOT_REQUIRED`.
6. From [`05_AGENT_OPERATIONS.md`](05_AGENT_OPERATIONS.md), the sections belonging to the created artifact or system change.

The non-skip protocol applies within the activated path. Optional methods that
are not activated do not require a series of justified `N/A` entries.

## 4a. After a non-positive validation result

`FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE`, and `INVALID_TEST` are not replaced by a subsequently suspected operationalization. If, however, a material revision or a new empirical test is considered, use the [`scientific-philosophy-critic`](agents/scientific-philosophy-critic.md). Its [`scientific_philosophy_review`](schemas/scientific_philosophy_review.schema.json) separates the core claim from auxiliary assumptions, leaves error attribution open when it is inconclusive, and classifies continuation ideas as `PROGRESSIVE`, `DEGENERATIVE`, `DIAGNOSTIC_ONLY`, or `UNRESOLVED`.

Only `PROGRESSIVE` authorizes empirical continuation: a new Research ID, a
prediction not implied by the earlier idea, a falsifier, and an independent
evaluation plan. The [`synthetic example`](examples/scientific_philosophy_review.synthetic_failed_reconstruction.json) shows the book strategy only as a thought case; it contains no backtest.

## 5. Non-negotiable core rules

- Observation, mechanism, forward OOS forecast and net executable edge remain separate statements.
- Claim level (`ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`) and validation/trading status (`mechanism_supported / forward_predictive_oos / executable_net_edge`) are independent axes. Neither axis automatically upgrades the other.
- Causal identification may be formulated as an SCM/DAG, a potential-outcomes design, a structural econometric model, or another explicit identification model. The notation does not decide the claim level.
- Data already considered are recorded in the information budget.
- Created and actually screened candidates are fully counted in the Search Space Register; Noise screen `PASS` is not evidence.
- Predictors must actually be available at the decision time.
- Material rules are frozen before independent evaluation.
- Costs, latency, fills and, where applicable, queue/borrow are assessed before a net edge claim.
- `IDENTIFIED_CAUSAL_LEVER` requires a passed identification gate and an Estimand artifact.
- `IMPLEMENTATION_CONSTRAINT` requires a validated phenomenon and a passed feasibility test.
- Unknown conditions for success remain unknown; plausible conditions are not
silently turned into mandatory filters.
- Design dependence, statistical dependence, prognostic benefit
and causal mechanism remain separate statements.
- A regime filter is a measurement instrument. The frequency of its classes does
  not validate the filter; predictive separation proves neither a real state,
  an actor, nor a mechanism.

The last two rules are machine-testable in [`schemas/constraint_assessment.schema.json`](schemas/constraint_assessment.schema.json).

## 6. Check framework integrity

Platform-neutral:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_framework.py
```

Windows/PowerShell remains as the second entry checked in CI:

```powershell
.\scripts\validate_framework.ps1
```

Both paths check framework contracts. The included 1,000-case evaluation run is
only `PROTOCOL_SMOKE` and is not proof of quality for a live agent.

## 7. Evaluating Real Agents

`evals/produce_results.py` sends each agent adapter only case input and output contract – never the expected assertions. It supports a local subprocess or a JSON/HTTP endpoint. Then the release check must explicitly request `LIVE_AGENT`:

```bash
python evals/produce_results.py --output artifacts/live-results.json \
  --run-id candidate-model-001 --run-kind LIVE_AGENT \
  --adapter-id local-agent --command-json '["python","my_agent_adapter.py"]'

python scripts/validate_framework.py \
  --live-results artifacts/live-results.json \
  --report artifacts/live-eval-report.json
```

Without produced `LIVE_AGENT` artifact, only the framework integrity is tested, not the quality of a model or prompt change.

## 8. Known open validation gap

The repository does not currently contain a fully completed real-world research case. Schema fixtures and Eval cases test contracts, not the practical probation of the entire research process. Until a suitable case exists, the framework must therefore not be described as end-to-end practice-tested.
