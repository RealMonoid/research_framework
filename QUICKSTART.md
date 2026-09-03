# Trading Research Framework – Quickstart

This short path is the only mandatory entry point for any new idea. The long standard documents are routed only by status and task; they no longer have to be loaded completely in advance into the context.

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

The framework is a tool for research and trading decisions, not a software project whose technical details must be tracked by the user. Every agent assumes that **no software developer** is sitting in front of him.

The following rules therefore apply to any visible response:

1. **Result and meaning first.** The agent starts with what came out,
why it is relevant for research and whether something has to be decided.
2. **General language.** Software terms, internal field names,
Function names, file paths, schema names, test names, CI details and technical architecture remain out of the answer unless the user expressly requests them or they actually change their decision.
3. **Research specialist language is also translated. *** Inevitable terms from
Statistics, causality or market structure are explained in a simple sentence at the first occurrence. Internal status codes may also be mentioned, but never without their meaning in everyday language.
4. **Decisions are declared ready for decision.** When the user chooses
The agent states why the decision is needed now, explains the understandable possibilities and their practical consequences, and gives a reasoned recommendation. A list of internal options or codes is not enough.
5. **Technical work remains in the background.** Reported after implementation
the agent only what has changed for the user, whether it has been checked, which factual restriction remains and whether a decision is open. Implementation details are only explained on request.
6. **No unasked developer justification. ** Statements about how
Functions cut, imports placed, adapters set up or individual tests named do not belong in the user response. Instead, for example, it suffices: “The change is working and has been checked.” You don’t have to decide anything about it.

The precise technical and scientific artifacts are fully preserved internally. This communication rule does not change a research rule; it only separates the internal documentation from the understandable response to the user.

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
- Revision or continuation following a non-positive frozen result:
continuing scientific-philosophical examination before new empiricism;
- intended intervention or counterfactual statement:
causality testing before effect estimation or causal formulation;
- new ideas only on an actual request for ideation; an existing idea goes into
intake and not back to the generator.

A simple result statement does not automatically trigger a specialist agent. A necessary user decision will only be requested if it materially changes the research question, the identity of the source strategy or the permissible claim. After each accepted specialist article, its artifact is checked, the work status updated and routed again.

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

Normative language controls behavior but does not replace technical enforcement. The framework claims automatic enforcement only where a scheme, test or CI-check is named.

## 2. Optional: Generate ideas

If no raw idea exists yet, the short-term executable generator may be used before the intake:

```bash
python scripts/generate_hypotheses.py --output-dir artifacts/ideas-001 \
  --run-id generation:ideas-001 --markets FUTURES --max-candidates 20
```

This is based on [`generation/mechanism_catalog.v1.json`](generation/mechanism_catalog.v1.json) and the four operators `PHASE_PATH`, `EXPECTATION_VIOLATION`, `MECHANISM_CONNECTION`, and `ASSUMPTION_RELAXATION`. The generation routes are constraint-first, microstructure state, instrument linkage, literature replication, and observation. A named compelled actor is not a universal condition.

The run writes a validated generation run and minimal `INBOX` files. The generator does not perform screening, backtesting, evidence grading, ranking or promotion. Details and filter options are available in [`generation/README.md`](generation/README.md).

The generation run documents the generated candidate space. If approximately all 96 candidates are screened using data, a family with `planned_screen_count = 96` is fixed in [`schemas/search_space.schema.json`](schemas/search_space.schema.json) before the first result. The threshold of each [`noise_screen`](schemas/noise_screen.schema.json) must correspond to the multiplicity correction stored there.

## 2a. Optional: Reconstruct a strategy from a book, article, video, or course

If a source describes a setup but does not fully operationalize its terms and alternatives, create a [`strategy_reconstruction`](schemas/strategy_reconstruction.schema.json) before specifying it. The process separates source rules, recommendations, options, examples, discretion, and open definitions. Possible translations remain candidates; they are neither automatically chosen nor tested.

Before the reconstruction is completed, use the [`scientific-philosophy-critic`](agents/scientific-philosophy-critic.md) in pre-operationalization mode. Its [`strategy_concept_audit`](schemas/strategy_concept_audit.schema.json) separates:

- what defines the strategy;
- what the source names only as an application condition;
- what is only suspected as a success modifier; and
- which conditions for success remain unknown.

It also reveals common computing components and windows without treating them as causal or automatic errors. Regime and state filters remain preliminary measuring instruments: group frequency alone is not separation performance, prognostic separation is not proof of a real hidden state and no proof of mechanism.

After a preliminary operationalization, a [`condition_inquiry`](schemas/condition_inquiry.schema.json) can be activated. The [`condition-inquiry-analyst`](agents/condition-inquiry-analyst.md) can assess measuring instruments, make definition dependence visible, and generate new observable condition hypotheses. Conditions found from data remain new hypotheses; they are not written back into the source strategy.

The workflow is in [`reconstruction/README.md`](reconstruction/README.md). The completed [`VWAP price-discovery example`](examples/strategy_reconstruction.vwap_wave_price_discovery.json) deliberately ends as `SOURCE_EXTRACTION` with all decisions open. It is not a backtest and does not claim that the source is profitable.

## 2b. Only on a real causality question

A trading strategy can be fully studied as a forecast without claiming that a signal is causing the market. In this normal case, no additional causality expenditure arises.

On the other hand, as soon as an intervention, a structural shock, or a counterfactual is to be claimed, the [`causal-identification-critic`](agents/causal-identification-critic.md) must check whether the comparison carries this meaning at all. Its [`causal_identification_assessment`](schemas/causal_identification_assessment.schema.json) identifies target impact, the source of identifying variation, the economic model, assumptions, financial-market risks, negative controls, sensitivity, and the strongest allowable statement.

A model or estimator does not replace this test. This applies explicitly to DML, causal forests, local projections, VARs, event-study regressions, Granger procedures, and causal discovery. Financial event studies must cover, among other things, the counterfactual return model, event timing, volatility, and other news; high-frequency designs add leakage, timestamps, surprise construction, and information shocks. The mandatory research basis is in [`references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md`](references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md).

A passed identification gate allows only the named causal estimate under its assumptions. Mechanism, prediction and tradable net edge remain questions of their own.

## 2c. Freeze outcome meaning before validation

Before validation data are opened, create a frozen
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
- An empty `transition` object.

See [`examples/hypothesis_candidate.inbox.json`](examples/hypothesis_candidate.inbox.json). If the idea is discarded during screening, the short `REJECTED` record with a justification is sufficient; see [`examples/hypothesis_candidate.rejected.json`](examples/hypothesis_candidate.rejected.json).

Only `PROMOTED` requires complete scope, an explicitly documented actor status, a passed noise screen or a well-founded theory-/event-/replication-based waiver, observable footprints, alternative explanations, data requirements, early feasibility, the three separate evidence levels and a record for variable selection. With `PREDEFINED` justification and retained constructs are sufficient. `DATA_DRIVEN` and `HYBRID` additionally require candidate universe, selection data and their role, outcome visibility, method, effective candidate number, search space and controls against selection bias. SHAP, impurity or other feature import procedures are possible diagnoses, but neither duty nor proof of causality. If no actor is known to be reliable for a purely predictive or associative question, `UNSPECIFIED / NOT_CLAIMED` is recorded. This is not an obstacle to this limited question, but it must not be read as a proof of mechanism. Promotion does not confirm an evidence level.

## 4. Document router by promotion

After `PROMOTED` everything is not loaded flat-rate:

1. [`00_RESEARCH_AGENT_README.md`](00_RESEARCH_AGENT_README.md) for gate and routing logic.
2. [`01_RESEARCH_STANDARD.md`](01_RESEARCH_STANDARD.md) for the mandatory research path.
3. [`02_RESEARCH_CASE_TEMPLATE.md`](02_RESEARCH_CASE_TEMPLATE.md) only when creating the specific research case.
4. From [`03_RESEARCH_METHODS.md`](03_RESEARCH_METHODS.md), only the sections selected by the method router.
5. [`04_CAUSAL_TOOLING.md`](04_CAUSAL_TOOLING.md) only for an executable causal core operation; otherwise record `TOOLING_NOT_REQUIRED`.
6. From [`05_AGENT_OPERATIONS.md`](05_AGENT_OPERATIONS.md), the sections belonging to the created artifact or system change.

The non-skip protocol applies within the activated path. Unenabled optional methods do not generate series of justified `N/A` entries.

## 4a. After a non-positive validation result

`FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE`, and `INVALID_TEST` are not replaced by a subsequently suspected operationalization. If, however, a material revision or a new empirical test is considered, use the [`scientific-philosophy-critic`](agents/scientific-philosophy-critic.md). Its [`scientific_philosophy_review`](schemas/scientific_philosophy_review.schema.json) separates the core claim from auxiliary assumptions, keeps an inconclusive error allocation open, and classifies continuation ideas as `PROGRESSIVE`, `DEGENERATIVE`, `DIAGNOSTIC_ONLY`, or `UNRESOLVED`.

Only `PROGRESSIVE` authorizes empirical continuation: a new Research ID, a previously unimplied prediction, a falsifier, and an independent evaluation plan. The [`synthetic example`](examples/scientific_philosophy_review.synthetic_failed_reconstruction.json) shows the book strategy only as a thought case; it contains no backtest.

## 5. Non-negotiable core rules

- Observation, mechanism, forward OOS forecast and net executable edge remain separate statements.
- Claim level (`ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`) and validation/trading status (`mechanism_supported / forward_predictive_oos / executable_net_edge`) are independent axes. Neither axis automatically upgrades the other.
- Causal identification may be formulated as SCM/DAG, potential outcomes design, structural econometric or other explicit identification model. The notation does not decide on the claim level.
- Data already considered is recorded in the information budget.
- Created and actually screened candidates are fully counted in the Search Space Register; Noise screen `PASS` is not evidence.
- Predictors must actually be available at the decision time.
- Material rules are frozen before independent evaluation.
- Costs, latency, fills and, where applicable, queue/borrow are assessed before a net edge claim.
- `IDENTIFIED_CAUSAL_LEVER` requires a passed identification gate and an Estimand artifact.
- `IMPLEMENTATION_CONSTRAINT` requires a validated phenomenon and a pass feasibility test.
- Unknown conditions for success remain unknown; plausible conditions are not
silently turned into mandatory filters.
- Design dependence, statistical dependence, prognostic benefit
and causal mechanism remain separate statements.
- A regime filter is a measuring instrument. Its class frequency does not
validate it; predictive separation proves neither a real state nor an actor or mechanism.

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

Both paths check framework contracts. The included 1.000 Eval run is only `PROTOCOL_SMOKE` and not a proof of quality for a live agent.

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
