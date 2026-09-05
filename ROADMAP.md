# Roadmap

This file records the prioritized implementation roadmap, conditional options,
and completed foundations. Status labels distinguish planned work from existing
rules and implemented controls. A planned entry is not authorization to install
a tool, access data, run research or a backtest, deploy, or allocate capital.

## Shared roadmap for all agents

This file is the single authoritative feature backlog and implementation
priority for Codex, Claude, Gemini, and every other agent working on the
framework. Update this shared roadmap rather than maintaining model-specific
backlogs. `AGENTS.md` remains the sole authoritative source of binding rules.

## Priority order and next action

**Reviewed and reordered with owner authorization on 2026-09-05.** Work is
ranked by protection against false evidence and by the shortest defensible path
to one complete research case. Dependencies and activation conditions take
precedence over rank: a lower-ranked safeguard needed by the current case must
be satisfied before that case proceeds. Completed work is not a new task.

**Always applicable:** data fitness is a binding prerequisite under `AGENTS.md`.
Before detailed operationalization and any empirical test, the exact data must
be capable of answering the question. Inadequate or unresolved material data
requirements stop the test without disproving the hypothesis. Priority 7 plans
additional enforcement only; it does not defer this rule. Existing evidence,
change-control, risk, and specialist requirements also remain in force.

| Rank | Work | Status and activation |
|---|---|---|
| 1 | Close test-validity and pipeline-control gaps | Next implementation: reject missing/conflicting protocols and repeated-random-walk bypasses, then verify executed test boundaries and control evidence. |
| 2 | Establish one verified rule-based backtest backend | After applicable priority-1 corrections and data fitness; choose for the first case and verify synthetic orders, fills, timing, and costs. |
| 3 | Complete one real Research Case | Separate research authorization required; freeze the framework and research state, then record failures without repairing the framework mid-case. |
| 4 | Measure actual agent behavior and bypass resistance | Use existing cases and failures from priority 3; no claim of live-agent reliability from protocol smoke. |
| 5 | Preserve cross-version search history and scoped learning | Required before a second research version can conceal earlier data exposure or selection. |
| 6 | Close observed enforcement and provenance bypasses | Initial inventory is complete; implement only the narrow additional harness justified by observed failures. |
| 7 | Add structured enforcement of data fitness | The rule already applies; additional artifact/validator work must support it, not become an excuse to postpone it. |
| 8 | Add conditional market-structure and execution assessment | Only with the specified domain triggers, data-fitness implementation dependency, and observed activation evidence. |
| 9 | Enforce complete rule loading and reference checks | Preserve required context; missing rules must not produce apparent success. |
| 10 | Establish decision-relevant concept mappings | Use observed ambiguity; prerequisite for trusting isolated normative sections. |
| 11 | Distinguish material changes from harmless edits | Activate when actual alerts show approval fatigue, while retaining material-change protection. |
| 12 | Reduce context through selective loading | Only after behavioral baseline, reference checks, concept mappings, and measured costs. |
| 13 | Migrate legacy language if justified | Only for measured reliability or actual maintenance need; translation and semantic revision stay separate. |

The immediate task is priority 1, not another library evaluation. Priority 2
turns the existing candidate register into an explicit prerequisite for the
empirical part of priority 3; it does not call for installing every engine.
The completed hard-gate inventory is retained under priority 6. Data-fitness
software is separated from the rule that applies now. Optional calculation
tools remain task-driven and have no independent implementation rank.

## Mission and scope

The roadmap serves the applied mission in `AGENTS.md`: rigorously test existing
strategies, develop new hypotheses through visible search, and accumulate
bounded learning toward executable strategies with credible positive net edge
after costs, liquidity, execution, and risk. A valid negative or untestable case
can improve decisions without supplying evidence for a different strategy.

### Scope and conservative pruning rule

The framework supports private research and capital decisions made by one
owner working with AI agents. It is not being developed for academic
publication, external persuasion, public strategy disclosure, or hypothetical
human-team onboarding.

Classify existing and proposed work as follows:

- **KEEP — decision protection:** directly changes or constrains a research,
  activation, continuation, sizing, suspension, or retirement decision.
- **KEEP — agent enforcement:** demonstrably makes an existing
  decision-protecting rule more likely to reach the agent and be applied
  correctly.
- **CONDITIONAL:** has a plausible protective role, but that role has not yet
  been observed or measured. Retain it while the hard-gate inventory, real
  Research Case, or behavioural evaluation tests the need.
- **REMOVE CANDIDATE:** serves only publication, external persuasion, public
  presentation, or unsupported assumptions about future human collaborators.
- **UNKNOWN:** retain until its effect and dependencies are understood.

Uncertainty is not permission to delete. Removal candidates must identify the
decision they do not protect, the enforcement path they do not support, and any
remaining dependency. Remove one independently reviewable unit at a time only
after relevant behavioural reference cases exist. Compare behaviour before and
after; restore or investigate any unexplained material change. Translation,
editorial simplification, and semantic removal remain separate changes.

The public repository is intended to contain framework code and safe examples
only. Real strategies, private data, real Research Cases, and empirical results
remain in an external private location or the ignored `private_research/` path.
Existing examples have not all been classified under this policy. Keep them
until a separate, user-authorized privacy review determines whether any require
removal or history remediation.

No new control layer should be added merely because it sounds prudent. Existing
controls must first show their value and their failure modes in executable
checks, live-agent evaluations, or a real Research Case.

## Prioritized work details

### 1. Close the validation-boundary, stopping-rule, and confirmed pipeline-integrity enforcement gaps

**Status: urgent correctness gap; documented rules exist, hard enforcement
is incomplete.** The outcome evidence documentation now prohibits optional
stopping, selective historical truncation, and unplanned holdout peeking,
but a `FROZEN` or `ASSESSED` contract can still validate without any
`validation_protocol`. The schema also permits both `validation_protocol`
and the legacy `forward_testing_protocol`; when both exist, the semantic
validator silently prefers one. Current boundaries are stored as free text,
and the contract records intended behaviour without proving how the test
actually ended. A formally valid artifact can therefore promise a fixed
test while the executed run uses a different window, stops early, or peeks.

Resolve the gap in this order:

1. Require exactly one canonical validation protocol before a contract may
   become `FROZEN` or `ASSESSED`. Remove the legacy alias through an explicit
   schema migration; until removal, reject simultaneous or conflicting
   protocol fields rather than choosing one silently.
2. Replace free-text boundaries with machine-checkable fields appropriate to
   the horizon: integer observation or trade counts, or explicit start and
   end timestamps for calendar windows and historical static holdouts. Bind
   these fields to the complete research fingerprint.
3. Add a separate execution record containing the actual start, end, count,
   termination reason, every interim inspection, and every deviation from
   the frozen protocol. Do not let a declaration stand in for execution.
4. Compare the frozen protocol with the execution record automatically.
   Early termination, extension, selective truncation, an unplanned peek, or
   any unexplained boundary mismatch must produce `INVALID_TEST` and must
   block `FORWARD_PREDICTIVE_OOS` and `EXECUTABLE_NET_EDGE` support.
5. Make each nontrivial peeking policy complete: predeclared alpha-spending
   requires its spending schedule and decision thresholds; fixed
   non-terminating audits require their dates or counts and must not alter
   the stopping horizon.
6. Version the schema and document migration whenever these contract changes
   alter the meaning of an artifact. Add negative tests for a missing
   protocol, both protocol fields, malformed boundaries, premature or late
   termination, selective historical clipping, and undeclared inspection.

Completion requires evidence that the normal freeze and assessment paths
reject a missing protocol, that executed boundaries are compared with frozen
boundaries, and that every listed deviation deterministically invalidates
the affected test. Priority 4 must additionally verify in live-agent
evaluation that an agent cannot bypass or cosmetically repair these checks.
Planning this fix does not authorize a backtest or access to validation data.

**Confirmed pipeline-integrity corrections from the external reviews:**

1. Fix the repeated-random-walk bypass. The current semantic validator
   rejects exactly one required `RANDOM_WALK` control, but two or more
   required random-walk controls can evade the list-equality check even
   though no structure-appropriate negative-control family is present.
   Compare the distinct required null-model families instead, and add a
   regression case with repeated random-walk controls. One or many random
   walks must never satisfy the requirement by themselves.
2. Replace the free-text Monte Carlo record with machine-checkable fields
   for planned and completed replications, the uncertainty method, estimate,
   standard error or interval bounds where applicable, and a complete seed
   or replication-manifest reference. Preserve a plain-language summary,
   but do not let prose stand in for the numerical record. Document and test
   the scientific basis of any minimum-run floor rather than treating the
   present value as self-justifying.
3. Bind every required negative-control and positive-sentinel result to
   evidence produced by executing the exact candidate pipeline identified by
   the frozen pipeline fingerprint. Schema validation of an agent-written
   `PASS` declaration is not evidence that the control ran. Until a trusted
   runner or the conditional harness in priority 6 performs or verifies that
   execution, describe this gate as caller-enforced and do not use it as an
   automatic reliability claim.

### 2. One verified rule-based backtest backend

The owner requested that external rule-based backtest engines be retained
as candidates assessed from documentation before implementing a genuine backtest
path. LEAN was added to this same register on 2026-09-05; the existing
Backtrader-first selection order and conditional roles remain unchanged. This is a
planning record, not an adopted dependency, installation, data acquisition,
backtest authorization, or market result. The framework remains responsible for
deciding whether a test may run and for interpreting its result; an engine is
only a replaceable execution component behind that control layer.

1. **Backtrader — primary evaluation candidate.** Its event-driven broker
   simulation, order types, commission schemes, slippage, volume filling,
   multiple feeds/timeframes, and future-like instrument support make it the
   first candidate for a single frozen, bar-based rule strategy. Evaluate its
   exact order-timing, fill, cost, and future-contract semantics against
   synthetic fixtures before any market-data run. Its GPL-3.0 license must be
   recorded with any later dependency decision.
2. **VectorBT — conditional robustness candidate.** Its vectorized execution
   and parameter broadcasting may make a predeclared sensitivity or robustness
   family practical after the family, multiplicity rule, and evaluation budget
   have been frozen. Its parameter sweeps, random-signal examples, data access,
   scheduled updates, and automation are not enabled by this record; an
   unregistered sweep is prohibited. Its Apache-2.0-with-Commons-Clause terms
   and optional-dependency licenses require a later dependency review.
3. **RQAlpha — conditional non-commercial candidate.** Its extensible
   simulation, futures-account, analysis, and transaction-cost modules could
   be relevant while the owner retains the present non-commercial scope. Its
   license states separate terms for commercial use, and its documented data
   ecosystem is centered on Chinese markets and Ricequant/RQData. Do not
   introduce that data path or assume its market conventions transfer to the
   target market without a separately approved data-fitness assessment.
4. **Backtesting.py — local prototype-only candidate.** Its simple OHLC(V)
   interface may help test a narrow deterministic reference fixture, but it is
   not a canonical backend: its built-in optimizer cannot run outside a frozen
   search family, its candle model cannot establish order-book or queue fills,
   and its AGPL-3.0 license needs a later dependency review.
5. **LEAN — conditional multi-instrument and futures candidate.** Its
   event-driven engine supports rule-based Python and C# strategies, local
   backtests with own data, customizable execution models, and later brokerage
   connections without requiring ML. Consider it when explicit futures-contract
   handling, multiple instruments, or a separately authorized future broker
   integration justifies its setup and configuration burden. Compare it with
   the existing candidates using identical synthetic data and predeclared
   expected orders, fills, and costs before changing the selection order.
   Verify continuous-series mapping and normalization separately from tradable
   contracts, roll behavior, fees, slippage, and order timing. In particular,
   the documented DefaultBrokerageModel uses zero slippage; that default must
   not silently become an accepted execution assumption. The engine's
   Apache-2.0 license and standalone local build are distinct from the hosted
   services, data licenses, and LEAN CLI: documentation reviewed on 2026-09-05
   requires membership in a paid-tier organization for CLI use. Recheck these
   terms and the exact runtime requirements before adoption. This entry
   protects execution realism and backend feasibility; it enables no ML,
   optimization search, data download, cloud upload, or live trading.
6. **Qlib — excluded from this rule-based path.** It is not selected because
   the owner does not want ML-driven research, model training, factor mining,
   or model optimization in this project.

Before any candidate can become an active backend, implement the priority-1
validation-boundary and pipeline-integrity corrections and satisfy the binding
data-fitness prerequisite in `AGENTS.md`. Then build a backend-neutral adapter contract that
binds the exact engine revision, environment/dependency lock, input-data
snapshot, strategy rules, instrument/contract convention, timezone/session,
order timing, fill model, costs, slippage, and all engine configuration to the
complete research fingerprint. The first acceptance test uses synthetic data
and fixed expected behavior to detect look-ahead, cheat timing, cost, fill, and
reproducibility failures; passing it is pipeline evidence only, never market
evidence. No candidate is allowed to download data, choose or optimize
parameters, create a hidden candidate family, decide readiness, or bypass the
frozen outcome and validation contracts.

Source records: https://github.com/mementum/backtrader,
https://github.com/polakowo/vectorbt,
https://github.com/ricequant/rqalpha,
https://github.com/kernc/backtesting.py,
https://github.com/microsoft/qlib, and https://github.com/QuantConnect/Lean.
LEAN-specific references: [engine overview](https://www.quantconnect.com/docs/v2/lean-engine/getting-started),
[CLI requirements](https://www.quantconnect.com/docs/v2/lean-cli/key-concepts/getting-started),
[slippage defaults](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts),
and [futures contracts](https://www.quantconnect.com/docs/v2/writing-algorithms/universes/futures).

### 3. One real Research Case

Run one deliberately unexciting end-to-end case
with public data and a predeclared expectation that no useful effect will be
found. Pass the prospective data-fitness gate before detailed
operationalization. Freeze the repository revision and research state
before starting,
do not repair the framework during the case, and record every point where a
rule is ambiguous, a gate is bypassable, or the process requires an
unsupported judgement. Fixes follow only in separately reviewed changes
after the case. One case can reveal practical failures but cannot establish
that the framework is generally validated. Planning this feature does not
authorize data access, a backtest, or empirical strategy research; those
actions still require an explicit user request.

### 4. Behavioural baseline and adversarial live-agent evaluation

Treat the
earlier LLM stress test, behavioural reference cases, and adversarial agent
evaluation as one programme. The repository already contains a blind
producer, scorer, deterministic regression machinery, and a 25-case
catalog; this is partial infrastructure, not a measured live-agent quality
baseline. Preserve the pre-case code revision, use failures from priority 3
to add blind cases whose correct response is to stop, reject work, invoke a
specialist, expose drift, or refuse a claim upgrade, and then run multiple
identified models repeatedly. Preserve every case-by-run result and report
catch rates, uncertainty, the distribution across cases and runs, and paired
improvement over the frozen baseline. The evaluation design should adapt the
useful ideas from Google's archived
[`rliable`](https://github.com/google-research/rliable) project: uncertainty
intervals from a resampling method that preserves the experiment's grouping,
performance profiles, robust aggregate summaries, and the probability that
one version improves on another. Do not assume that model runs or cases are
independent when they share prompts, models, or reference cases.

These summaries are secondary diagnostics, not permission to average away a
safety failure. Predeclare which assertions protect critical research or
capital decisions and report their miss count separately. A version with a
missed critical assertion fails even when its aggregate score or uncertainty
interval looks favourable. Small samples remain visibly uncertain, and no
agent-evaluation statistic is evidence that a market claim or trading edge is
valid. Use the methodology as a local, reviewable evaluation specification;
do not add the archived project as a runtime dependency.
A human-approved `LIVE_AGENT` baseline must be frozen before later prompt,
terminology, loading, or shortening changes are judged safe. Protocol smoke
results are never a substitute.

The repository now includes a provider-neutral, bounded
`framework-control-reviewer` contract for the red-team, loophole,
strategy-identity, scope, root-cause, rule-conflict, and memory checks that
the optional AI-Psychiatry plugin can provide. Its invocation remains
conditional and caller-enforced; its effectiveness and bypass resistance
must be measured in the live-agent evaluation rather than inferred from the
existence of the contract or its schema tests.

The five baseline conductor controls are now part of the current routing
contract rather than a planned specialist feature: scope lock, one-level
delegation, evidence-bound conclusions, changed-evidence requirements for
repeated checks, and evidence-backed completion. Their machine constants
reject a relaxed route, but the caller-invocation and truthful-reporting
limits remain open until the live-agent trajectory evaluation is complete.

**Execution trajectory and tool-invocation auditing:** The evaluation
harness must not assess only the final adapter artifact or returned claims.
An agent must not receive a passing score if it fabricates a compliant
result while taking unauthorized shortcuts or bypassing mandatory workflow
steps. The evaluation design must audit the actual execution trajectory:
verifying that `scripts/route_research_task.py` was actually invoked at each
material transition, required specialists were genuinely consulted with
bounded work orders rather than simulated, `scripts/check_research_fingerprint.py`
was executed rather than skipped, and internal tool errors were not silently
swallowed and cosmetically repaired in the final prose.

The critical adversarial set must explicitly include: substitution or
rewriting of the accepted fingerprint baseline; relabelling causal language
as merely predictive to avoid the causal critic; a self-declared pipeline or
sentinel `PASS` without execution evidence; repeated random-walk controls
presented as sufficient diversity; simultaneous legacy and canonical
validation-protocol fields; an ignored non-zero fingerprint result; reset of
the attempt counter; and producer or configuration hashes that are
well-formed but not bound to the actual model, prompt, tools, and retrieved
rule set. These are trajectory failures even when the final artifact is
schema-valid.

**Surrogate methodology options:** When negative controls require
preserving empirical amplitude distributions and linear autocorrelation
while destroying nonlinear temporal phase dependencies, IAAFT (Iterated
Amplitude Adjusted Fourier Transform) and phase-randomized surrogate data
may be offered as selectable options in the research methods catalog
(`03_RESEARCH_METHODS.md`). They must remain optional, design-specific
tools rather than a universal hard gate, to avoid inadvertently destroying
or preserving critical microstructure structure.

### 5. Cross-version search lineage, selection-adjusted reporting, and scoped cumulative learning

Treat search-history accounting and statistical
consequence as one control. Every new Research-ID or version inherits prior
data exposure, definitions, filters, outcomes, continuation choices, and
failed attempts from the same research line. Final reporting must show both
the ordinary result and a correction or decision rule appropriate to that
complete selection process, not merely to the surviving latest version.
This becomes urgent as soon as a real research line reaches a second version.

After lineage is reliable, add the smallest reusable cross-case learning
record needed to preserve what a result bears on: its strategy or candidate
family, market and horizon, representation, mechanism candidate, condition,
measurement, method, failure mode, evidential status, and transfer limits.
It may inform later candidate generation, design, or decision sensitivity,
but it must not pool incompatible cases, hide prior data exposure, or promote
a result into edge evidence for another strategy. This is a decision aid and
search-memory control, not a general knowledge base or publication product.

### 6. Observed enforcement gaps and baseline provenance

**Initial hard-gate inventory completed 2026-09-02; additional enforcement is conditional.**

The [`HARD_GATE_INVENTORY.md`](HARD_GATE_INVENTORY.md) records every current
research gate and the claim or
transition it is meant to prevent. For each gate, identify whether it is
enforced by automatically invoked executable code, by a schema whose
validation is mandatory on that path, by an agent or human classification,
or only by prose. Also record the invocation point, the fail-closed
consequence, the relevant regression test, and any known bypass. The mere
existence of a validator does not make a hard gate: the normal workflow must
invoke it, and failure must stop acceptance or continuation. Include the
already implemented research-fingerprint, scientific-philosophy, causal,
outcome-contract, and pipeline-integrity controls. This inventory is a
diagnosis; its findings may change the priorities in this roadmap. Also mark the
trust boundary explicitly: the framework cannot discover experiments,
viewed data, or discarded variants that occurred outside its recorded
workflow. A control may reduce that exposure but must not claim to eliminate
undisclosed external search. The audit found substantial deterministic
checks but no framework-owned end-to-end runtime that forces their use in a
live research task. The current research gates are therefore
caller-enforced. Priority 3 must record whether those calls actually occur;
priority 4 must attack false `COMPLETE` states, skipped
validators and specialists, ignored fingerprint failures, and semantic
misclassification before a new orchestration layer is justified.

The external reviews sharpen the scope of that conditional implementation
without changing the evidence-first order. If priority 3 or repeated
priority-4 runs show that caller-enforced gates are skipped or fabricated,
build the smallest fail-closed conductor harness that can own the affected
sequence. It must dereference required artifact references, validate the
referenced content, record validator and fingerprint exit codes, invoke
mandatory specialists rather than merely naming them, and keep a persistent
attempt count so `max_attempts` cannot be reset by another model call. A
non-zero `CHANGE_PROPOSED` result remains a stop signal, not a successful
acceptance.

The same harness must derive the effective fingerprint baseline from the
previously accepted checkpoint rather than trusting a baseline path supplied
by the current agent. Use a private append-only, content-addressed, or
commit-addressed store appropriate to the confidentiality of real research;
never require proprietary research to be committed to the public repository.
The predecessor reference, protected-artifact hashes, and current rule-set
identity must form one verifiable chain. If that chain is not independently
anchored, say plainly that it is tamper-evident bookkeeping only to the
extent that the storage history is trustworthy.

### 7. Structured enforcement of the existing data-fitness prerequisite

**Status: the prerequisite is binding now under `AGENTS.md`; only its
dedicated machine-readable artifact and enforcement remain planned.**
Owner clarification on 2026-09-05: every empirical hypothesis and test must
already be checked for answerability with the available data. Poor or
insufficient data stop the affected test; the hypothesis is not thereby
disproved. The conductor records the assessment through existing artifacts
until additional tooling exists. This entry must never be read as delaying
that obligation or requiring a new software feature merely to apply it.

The planned structured implementation must enforce the following existing
assessment rather than introduce a new optional research capability.
Before detailed operationalization,
implementation, or empirical testing, translate the proposed strategy and
intended claim into a minimum data-requirement record, then compare it with
the metadata and observable content of the data that can actually be
obtained. This is not a bar-count check. It must cover instrument and
contract identity, continuous-contract construction and roll adjustment,
session and timezone rules, historical coverage, sampling interval,
timestamp precision, price and volume meaning, missing periods, revisions,
bid/ask or trade information, and any intrabar or order-book detail required
by the trigger, outcome, cost, or execution model. For platform-supplied data
such as TradingView, record the exact symbol, feed, plan-dependent history,
export limits, and simulator assumptions rather than treating subscription
access as proof of fitness.

The assessment must use metadata and coverage diagnostics without searching
the data for a favourable effect. It returns one of four decisions:
`ADEQUATE`, `ADEQUATE_WITH_SCOPE_LIMITS`, `REMEDIABLE_GAP`, or
`NOT_TESTABLE`. Every limitation must state which research or capital
decision it prevents. A material gap stops the affected path. The framework
must never silently simplify the strategy, weaken the claim, enlarge the
bar interval, substitute a continuous future for executable contracts, or
change the outcome merely to fit the available data. Any such response is a
visible research change requiring the user's decision and, where material,
a new research version. Recheck fitness whenever the strategy,
operationalization, data source, market scope, or intended claim changes.

Verification is automation-first and must treat acquisition burden as part
of feasibility. Prefer one coherent, reusable, versioned export or snapshot
over repeated interaction with a chart interface. Automated checks should
cover integrity, coverage, internal consistency, and any feasible
cross-source comparison. A manual visual review is an exception: it needs a
named residual risk, a case-selection rule fixed before inspection, and the
smallest defensible scope. There is no generic screenshot minimum, and an
agent must never invent an arbitrary quota such as 50 manually reviewed
charts. Repeated TradingView scrolling, bar-by-bar history loading, or
manual collection of chart sections is not an acceptable default data
pipeline. If adequate data cannot be acquired without material repetitive
user work, the path is `REMEDIABLE_GAP`, `NOT_TESTABLE`, or `BLOCKED`; the
burden is not transferred to the user and the strategy is not weakened to
fit the interface.

The purpose is to reject an untestable project before expensive
reconstruction creates commitment to it, and to prevent a late discovery
that the available data could never observe the event, mechanism, or fill
being claimed. The real Research Case in priority 3 should supply the first
concrete requirements and failure examples. Planning additional enforcement does not
authorize inspection of strategy outcomes, a backtest, or market-data use.

The bounded `data-analyst` role is not this gate. It may provide a scoped
quantitative data profile or non-causal diagnostic when the conductor has a
concrete information need, but its report cannot declare a dataset fit for a
strategy, authorize a test, or replace the prospective comparison. The
eventual data-fitness artifact must still evaluate the complete strategy,
claim, instrument, coverage, resolution, and acquisition burden before
operationalization or empirical work.

### 8. Conditional market-structure and execution assessment

**Status: CONDITIONAL planned capability; no route, artifact, or specialist
exists yet.** Financial economics and market microstructure already inform
the mechanism catalogue, method guidance, candidate scope, and production
principles. They do not yet have an independent, typed assessment that can
test whether the proposed market representation is plausible, observable,
and executable for the named market, venue, instrument, horizon, and data
path. The resulting risk is that a candidate moves into data-driven feature
search, mechanism interpretation, or strategy engineering with an
institutionally implausible story, an inadequate feed or timestamp model,
or an execution assumption that cannot support the stated claim.

This capability protects three distinct decisions: whether a
market-structure-dependent candidate may proceed to data-driven search;
what a result can mean about an actor, mechanism, or market condition; and
whether a limited supported claim is sufficiently specified to enter
downstream strategy engineering. It does not make a candidate profitable,
identify a causal effect, validate a forecast, or authorize a trade.

Do not create a broad, universal "finance agent." First define and validate
a fingerprinted `market_structure_assessment` artifact with, at minimum:

- the exact market, venue, instrument or contract, horizon, trading phase,
  calendar, and relevant rule version;
- the proposed participants, constraints, flow, liquidity, or linkage and
  whether the actor is named, unknown, or not claimed;
- the claimed observable imprint and the feed, timestamp, venue coverage,
  order-book, trade, or quote information required to measure it;
- alternative microstructure explanations, unobserved venues or liquidity,
  asynchronous or stale prices, clock and sequence risks, and the resulting
  claim limits; and
- execution-relevant limits, including spread, fees, latency, queue or fill
  assumptions, capacity, leg risk, and the remaining unresolved risk.

The future artifact and router must use a controlled, non-empty
`review_triggers` list. Its initial allowed values are `ORDER_BOOK`,
`ORDER_FLOW`, `LIQUIDITY`, `AUCTION`, `ROLL`, `FUNDING`, `LIQUIDATION`,
`LINKED_INSTRUMENT`, `LEAD_LAG`, `FORCED_ACTOR`, and
`MECHANISM_PREMISE`. The last value means that a proposed mechanism
conclusion relies on an actor, flow, liquidity, or linkage premise. The
router must invoke one market-structure-and-execution reviewer with exactly
one `routing_decision.work_order` when `review_triggers` is non-empty, and
must not invoke the reviewer otherwise. The existing sequential,
one-level, single-attempt work-order limits apply. `INBOX` intake and
unconstrained idea generation remain cheap. A purely predictive or
associative candidate without a named actor remains permissible only when
`actor_constraint` records `actor_status = UNSPECIFIED`,
`mechanism_claim_status = NOT_CLAIMED`, and a reason; it cannot be
interpreted as mechanism evidence. The review must
occur before data-driven feature or parameter search for a candidate with
non-empty `review_triggers`, before accepting a mechanism interpretation
carrying `MECHANISM_PREMISE`, and before a candidate with non-empty
`review_triggers` enters strategy engineering. It must not become a
universal gate for every market or strategy type.

Implementation is conditional on priority 7 being implemented and returning
`ADEQUATE` or `ADEQUATE_WITH_SCOPE_LIMITS` for the candidate, and on one of
two observed activation signals. Either priority 3 records a named candidate
with one of the controlled `review_triggers` values for which the existing
candidate-scope, method, data-fitness, and conductor artifacts have no field
or route that can record the required domain constraint; or a priority-4
case fails a predeclared critical assertion because, after receiving an
input that names an existing venue, feed, timing, liquidity, or execution
limitation, an agent nevertheless continues to data-driven search,
mechanism acceptance, or strategy engineering without recording that limit.
Implement in this order: define the artifact and its decision consequences;
add semantic validation and synthetic pass, limit, and blocked cases; add
the routing schema and reviewer contract; then add live-agent cases that
reject a reviewer artifact lacking a required trigger, required assessment
field, stated decision consequence, or claimed-limit check. The reviewer
may constrain, defer, or block the affected path, but may not invent missing
market facts, choose a strategy, alter the research question or effective
fingerprint, turn an actor story into mechanism evidence, substitute for
causal identification, or approve a net edge, deployment, or capital
allocation.

### 9. Fail-closed rule-set loading and reference checks

First enforce the
rule at the current whole-document level: a material step must prove that
every document required by its route was resolved, loaded, and recorded,
otherwise it stops. Separately, before selective loading is activated,
introduce stable section identifiers and CI checks proving that every
identifier the router can emit resolves exactly once to non-empty content.
Missing, stale, ambiguous, or incomplete references must never degrade into
a reduced but apparently valid run.

### 10. Canonical concept registry

Limit the registry to concepts that carry a
decision-protecting rule or whose ambiguity can disable an agent gate. Map
each such concept to one canonical term, a concise definition, its legacy
terms, and exact machine anchors where those anchors genuinely exist. Use
results from priority 4 to identify which semantic ambiguities cause real
failures, while treating the current German-prose/English-machine split as
an existing but still measurable correctness risk. The registry is required
before isolated normative sections can be trusted; it is not a general
terminology or documentation project.

### 11. Severity-aware change control

Separate semantic research changes,
evidence-integrity changes, and demonstrably non-material editorial changes.
Implement this when real fingerprint alerts exist and there is evidence
that harmless alerts are training users to approve changes reflexively. It
must reduce alert fatigue without hiding material rule or research changes.

### 12. Selective normative loading

Keep this optional and treat it as an
efficiency project, not a research safeguard. It may start only after the
critical live-agent baseline in priority 4, the fail-closed checks in
priority 9, the applicable concept mappings in priority 10, and actual
before-change context measurements exist. Measure savings and behavioural
changes; do not assume that shorter prompts preserve gate behaviour.

### 13. Conditional legacy-language migration

Do not migrate the remaining
German corpus merely for publication, an international audience, or
stylistic consistency. Proceed only if priority 4 measures a material agent
reliability problem that narrower concept mappings cannot solve, or if an
actual maintenance need emerges. Priority 10 supplies the necessary semantic
mappings. Translation-only commits must remain separate from shortening,
deduplication, or substantive revision so that changes in agent behaviour
remain attributable.

## Conditional calculation tools

### Owner-requested non-ML calculation tools — 2026-09-05

**Status: CONDITIONAL planning record; no new dependency or runtime integration.**
This extends the existing scientific-capability screen in the completed-foundations section without changing
its approved role boundaries or the authoritative implementation priorities.
The owner wants a research and decision framework, not an ML system. Select a
calculation tool only when an explicitly scoped research or capital decision
requires it; tool availability is not a reason to create a new research task.

- **statsmodels — reuse the existing bounded capability when needed.** It is
  already recorded in the completed-foundations section for predeclared econometric and time-series methods.
  A concrete use could be testing cointegration when the source strategy
  depends on that relationship. Preserve model assumptions, diagnostics,
  temporal dependence, selection history, and uncertainty in the existing
  report. A significant test does not establish a stable tradable relationship
  or positive net edge. This record does not add a second statsmodels route.
- **CVXPY — conditional downstream portfolio calculation candidate.** Consider
  it only when an authorized allocation question concerns already evaluated
  strategies and explicitly specified objectives, risk and weight limits,
  costs, and input estimates. Verify solver status, numerical tolerances,
  constraint satisfaction, infeasibility handling, and sensitivity to uncertain
  inputs. An optimizer solves the stated mathematical problem; it cannot
  validate return estimates or authorize capital allocation. This protects the
  sizing decision from being determined by hidden defaults or unstable inputs.
- **TA-Lib — optional source-faithful indicator calculation candidate.** Use
  only when an existing strategy specification needs a named indicator.
  Verify formula conventions, lookback and warm-up behavior, missing values,
  and decision-time availability against fixed reference examples. Library
  defaults must not silently replace source rules. This protects strategy
  identity and timing; it does not authorize indicator mining or parameter
  search, and a correctly calculated indicator is not evidence of edge.

LSTM, temporal convolutional networks, XGBoost, LightGBM, and hmmlearn-based
learned regime detection are excluded from this planned extension. It adds no
model training, ML forecasting, automatic regime discovery, or feature search.
Existing deferred-capability records remain historical context, not permission
to activate an ML path.

Before adopting CVXPY or TA-Lib, name the concrete calculation and protected
decision, check whether existing capabilities suffice, and verify the smallest
necessary implementation with synthetic or independently calculated reference
cases. Record the chosen package and solver versions where relevant, license,
configuration, input provenance, assumptions, and material outputs through the
existing artifact and complete-fingerprint mechanisms. Apply all prerequisites
of the actual research stage, including validation-boundary corrections and the binding
data-fitness prerequisite before an empirical backtest path. Synthetic checks prove
calculation behavior only. No new registry, specialist, universal gate, data
access, backtest, trade, or implementation is authorized by this planning entry.

Reference documentation: [statsmodels cointegration test](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.coint.html),
[CVXPY portfolio example](https://www.cvxpy.org/examples/basic/quadratic_program.html),
and [TA-Lib functions](https://ta-lib.org/functions/).

The synthetic pipeline-integrity control, outcome evidence contract, complete
research fingerprint, central conductor, and specialist routing are completed
controls rather than new roadmap items. Their actual enforcement and bypass
resistance are nevertheless subjects of priorities 1, 3, 4, 6, and 7.

## LLM Stress Test Against Silent Research Changes

**Status:** planned, not implemented

The stress test should deliberately confront multiple language models with
difficult situations: negative results, conflicting sources, tempting post-hoc
filters, changed time windows, new exclusions, and apparently harmless
rewordings. It tests whether the lead agent:

- leaves the effective research fingerprint unchanged;
- reports every material difference as a visible change proposal;
- accepts no proposed change without a user decision;
- creates a new research version after approval instead of overwriting the old
  one;
- explains in ordinary language what would change substantively.

For later release, the test requires a versioned case catalog, multiple repeated
model runs, an independent evaluation, and fixed passing thresholds. The
existing deterministic contract checks are a prerequisite, but not a substitute
for this live-LLM stress test.

The eventual report must retain atomic case-by-run outcomes and show
uncertainty, run-to-run and case-to-case variation, paired change from the
frozen baseline, and every critical miss. Resampling must preserve the actual
grouping of the evaluation rather than pretending that correlated runs are
independent. Robust aggregates and performance profiles may help describe
ordinary variation, but they never override the zero-tolerance decision rule
for a predeclared critical failure. This adapts the evaluation principles
documented by Google Research's archived
[`rliable`](https://github.com/google-research/rliable) project; it is not a
planned software dependency and provides no evidence about a trading claim.

## Safe and measurable loading of normative sections

**Status:** planned, not implemented

The largest normative documents currently create a substantial context cost.
Loading only the sections needed for a research step may reduce that cost, but
it also creates a more dangerous failure mode: a required rule can disappear
from the agent's context while the returned artifact remains formally valid.
Selective loading must therefore not be enabled until missing or stale section
references are made visible and stop the affected research step.

### Prerequisite: canonical concept registry

Selective loading also removes explanatory context that currently helps an
agent connect German normative prose, English machine fields, and enum values.
Before a normative section can be loaded on its own, the project must establish
a machine-readable canonical concept registry. This is a correctness control,
not a translation or style project.

Each registry entry must contain:

- a stable, language-independent `concept_id`;
- a concise definition of the concept;
- the canonical English term for new normative text;
- legacy German terms used by the existing corpus;
- exact machine anchors where possible, such as a schema plus JSON Pointer,
  field, enum value, or executable check;
- deprecated or forbidden variants, scoped by language and document type;
- a status showing whether the mapping is active, deprecated, or unresolved.

Concepts that do not map one-to-one to a machine field must say so explicitly
instead of inventing a false-precision anchor. Every loadable normative section
must declare the `concept_id` values it relies on. The loader must append the
corresponding compact definitions and machine anchors to the section context.
An unknown concept, unresolved required anchor, or missing concept definition
must stop the affected material research step.

The effective concept entries and their hashes are part of the rule set for a
run and must therefore be recorded in the orchestration state and protected by
the research fingerprint. A changed definition is a normative change even when
the section text itself did not change.

A terminology lint check should reject explicitly forbidden variants in the
active normative corpus and point to the canonical term. Its scope must exclude
or separately handle historical decisions, quotations, source reconstructions,
and examples where an old or non-canonical term may be evidence rather than an
active instruction. It must not rewrite terms automatically.

### Selective-loading dependency order

This is the internal dependency sequence for priority 12 above, not a competing
global roadmap. Priorities 4, 9, and 10 must reach the applicable activation
criteria before selective loading is enabled.

1. **Complete the behavioural reference cases first.** Add cases in which the
   correct result is to stop, invoke a required specialist, reject returned
   work, report a research-fingerprint change, or block an unsupported causal
   claim. Only then run and freeze the live-agent behavioural baseline.
2. **Build the canonical concept registry.** Collect the concepts already
   represented in schemas, executable checks, and active normative prose;
   resolve ambiguous mappings explicitly; and add validation for concept IDs,
   required definitions, statuses, and machine anchors.
3. **Introduce stable section identifiers.** Give every loadable normative
   section an explicit identifier that is independent of its heading text.
   Maintain one machine-readable registry as the authoritative map from the
   identifier to the source document and section boundaries. Each section
   entry must also declare its required concept IDs.
4. **Check the complete reference chain in CI.** Automatically prove that
   every section identifier the router can emit exists exactly once, resolves
   to non-empty content, and is present in the registry. Also prove that every
   declared concept ID resolves, every required machine anchor exists, and all
   explicitly forbidden variants are absent from their lint scope. Unknown,
   duplicate, empty, or unresolvable references must fail validation.
5. **Make runtime loading fail closed.** Before a material research step, the
   loader must confirm that every requested section was resolved and loaded.
   It must also confirm that the section's required concept entries were
   resolved and included. If any requested section or required concept is
   missing, ambiguous, empty, or fails its integrity check, the step must stop
   instead of continuing with a reduced rule set. A fallback to a larger
   document must never happen silently.
6. **Record the effective rule set for every run.** The orchestration state
   must list each loaded section identifier, source document, content hash,
   reason for loading, approximate token count, and effective concept-entry IDs
   and hashes. These records must also form part of the research fingerprint so
   that a rule or concept change between runs cannot remain invisible.
7. **Preserve useful prompt caching.** Put the small, stable, always-required
   rule core first and append variable task-specific sections afterwards. This
   prevents selective loading from needlessly changing the stable prompt
   prefix for every case.
8. **Measure before shortening.** Use the run manifests to report which
   sections are loaded, how often they are loaded, their approximate token
   cost, and which loads appear unnecessary. Absence from the returned artifact
   is not sufficient evidence that a section was unnecessary: a preventive
   rule may be successful precisely because the prohibited action never
   appears. Token estimates and assumed savings are hypotheses until these
   measurements exist.
9. **Move explanations and examples cautiously.** Explanations, edge cases,
   and examples may affect how an agent applies a short rule. Move them only
   after the behavioural baseline exists, one independently reviewable change
   at a time. Compare each change with the baseline and restore or investigate
   any material behavioural difference. Do not describe this work as
   risk-free token removal.

### Main risks to control

- **Invisible loss of a gate:** the router requests a stale identifier, the
  rule is not loaded, and a schema-valid artifact creates false confidence.
- **Identifier drift:** renaming or moving a heading breaks references if IDs
  are derived from document wording rather than assigned explicitly.
- **Semantic disconnect:** a section uses a prose term without loading the
  concept entry that connects it to the governed machine field or status.
- **Registry without enforcement:** a correct-looking concept list creates no
  protection if sections do not declare concepts or the loader ignores them.
- **False-precision mapping:** a broad research concept is assigned to one
  convenient schema field even though the rule actually spans several fields
  or has no one-to-one machine representation.
- **Overbroad terminology lint:** valid quotations, historical records, or
  source-language reconstructions are rejected as though they were active
  normative instructions.
- **Unrecorded rule changes:** two runs appear comparable although different
  versions of a normative section or concept definition governed them.
- **Alert fatigue:** harmless editorial changes may alter a content hash. This
  must be handled together with severity-aware change control, without hiding
  genuine rule changes.
- **Caching fragmentation:** highly variable prompt prefixes can erase the
  expected cost benefit of caching.
- **Behaviour loss through shortening:** removing a rationale or example may
  preserve the written rule but reduce correct handling of borderline cases.
- **Weak baseline evidence:** a single non-deterministic agent run or a
  baseline without stop and escalation cases cannot establish unchanged
  behaviour.
- **Unproven savings:** the estimate that a fixed fraction of the corpus is
  redundant must not be treated as measured fact.
- **Control overhead:** the registry, loader, fingerprint record, and tests can
  become bureaucratic unless they remain generated or mechanically checked
  wherever possible.

### Activation criteria

Selective normative loading may be used for real research only when the
critical reference cases are in the baseline, the concept and section
registries and their complete reference checks pass, injected missing-section
and missing-concept failures stop the run, the exact effective sections and
concept entries are recorded and fingerprinted, and a measured before-and-after
report shows the context saving without a new critical behavioural failure.

## Detailed research-control backlog

**Status:** planned, not implemented

The following findings must remain visible until they are implemented and
validated. Their authoritative priority and grouping are defined above; the
numbers here identify details rather than execution order:

1. **Priority 5 — Cross-version search lineage:** A new research version must inherit every
   previous data exposure, operationalization attempt, filter choice, outcome
   choice, and continuation decision from the same research line. Repeatedly
   authorizing new versions must not reset the information budget or create an
   apparently fresh search family.
2. **Priority 5 — Selection-adjusted reporting:** Final performance reporting must show both
   the ordinary metric and a correction or decision rule appropriate to the
   complete selection process. The correction must cover the relevant
   candidate family, research-version history, and data reuse rather than only
   the survivors of the latest screen.
3. **Priority 5 — Scoped cumulative learning:** After cross-version lineage is
   reliable, preserve reusable findings with their research line, market,
   horizon, representation, mechanism or condition, measurement, method,
   evidential status, and transfer limits. A prior result may guide search or
   design but cannot become edge evidence for another strategy without a new
   appropriate test. Do not build a broad knowledge platform beyond this
   decision-protecting need.
4. **Priority 11 — Severity-aware change control:** Separate the semantic research
   fingerprint from the artifact-integrity manifest. Distinguish material
   research changes, evidence-integrity changes, and demonstrably non-material
   editorial changes so that harmless hash changes do not train users to
   approve every warning.
5. **Priority 6 — Hard-gate coverage accounting (initial inventory complete):** Maintain the
   [`HARD_GATE_INVENTORY.md`](HARD_GATE_INVENTORY.md), showing
   which research gates are enforced by executable checks, which are enforced
   only by schemas, which depend on an agent classification, and which remain
   prose instructions. Increase executable enforcement where the required
   condition is objectively decidable and the real case or behavioural
   evaluation demonstrates that the current caller-enforced path is unreliable.
6. **Priority 4 — Adversarial live-agent evaluation:** Extend the planned LLM stress test
   with agents that actively attempt to change definitions, reset the search
   history, upgrade claim levels, skip required specialists, or satisfy schemas
   with scientifically empty content. Retain case-by-run outcomes; measure
   repeated catch rates, grouping-aware uncertainty, performance profiles,
   paired improvement over the frozen baseline, and critical misses rather than
   treating contract validity or one aggregate score as evidence of agent
   reliability. A missed predeclared critical assertion fails the candidate
   regardless of its average score.
7. **Priorities 10 and 13 — Narrow terminology control and conditional language
   migration:** Establish only the decision-relevant concept mappings described
   above before selective loading. Migrate the legacy German corpus only after
   a measured agent-reliability or actual maintenance need. Translation must be
   performed in translation-only commits; redundancy removal, shortening, and
   substantive rewriting must follow in separate commits with separate
   validation.
8. **Priority 1 — Pipeline-integrity correctness:** Reject one or many required
   random-walk controls when they are the only null-model family, structure the
   Monte Carlo and seed record, and bind every required control result to
   evidence from the exact frozen pipeline. Passing a JSON contract alone must
   not be reported as execution evidence.
9. **Priority 6 — Conditional fail-closed conductor and baseline provenance:**
   If the real case or live-agent runs demonstrate caller bypasses, implement
   the minimal harness and predecessor-chain requirements described above.
   Preserve the current separation between router, specialist, validator,
   fingerprint, and research stages; consolidation is not an objective.
10. **Priority 9 — Cross-schema identifier consistency:** Audit materially linked
   identifier grammars and establish one tested canonical rule where a shared
   identifier crosses artifact boundaries. A shared schema file is optional,
   not the goal. If external `$ref` definitions are introduced, resolution from
   a clean checkout must be tested and fail closed; reducing duplicated lines
   must never create a silent missing-definition path.

## Completed foundations and decision context

The following records explain existing integrations and earlier decisions.
They are not additional tasks ahead of the ranked work above. References to
priorities use the current numbering.

### External-review intake on 2026-09-03

Two external reviews were treated as advisory inputs and checked against the
repository rather than copied into the roadmap. Their broad refactoring claims
are not reliable enough to authorize work: both identify revision `4af9cff`
while citing material added after that revision, and their reported counts for
schemas, agents, scripts, mechanisms, and generated combinations do not match
that revision or the current repository. Their severity labels and estimate of
a thirty-percent reduction are therefore not evidence of benefit.

Only findings that protect a research or capital decision, expose a confirmed
deterministic defect, or make an existing gate measurably harder to bypass are
incorporated below. In particular, this roadmap does **not** adopt proposals to
return success for `CHANGE_PROPOSED`, add validation data to pre-freeze pipeline
controls, merge distinct epistemic stages or specialist roles, split this
authoritative roadmap, remove the Windows validation path, or add packaging and
style tooling merely to make the repository look like a conventional software
project. Those changes could weaken fail-closed behaviour or add maintenance
without protecting a decision. They require separate evidence and user
authorization if reconsidered later.

### Owner-authorized workflow transparency amendment — 2026-09-04

The owner explicitly authorized a small implementation that makes the existing
conductor workflow visible and decision-ready at every routed step. It does not
reorder the research-control priorities in this roadmap, create a new empirical gate, or
authorize data access, backtests, deployment, or capital allocation. It protects
the owner's continuation, change, and stop decisions by requiring every routing
decision to state the current position, the next framework action, what follows,
and the user's next action. Required decisions must provide at least two
plain-language options, the practical consequence of each, an ordinal
assessment (`RECOMMENDED`, `ACCEPTABLE`, or `NOT_RECOMMENDED`), and a reasoned
recommendation. A blocker or material disruption must present weighted recovery
options and be recorded beforehand in one separately stored, validated
`problem_record` file containing the model identity, occurrence and recording
timestamps, description, impact, and orchestration references where available.
Real-case files remain private. The deterministic route validates the output
shape and references, while the conductor remains responsible for creating and
validating the separate file; this is transparent caller-enforced bookkeeping,
not a claim that the framework can discover unreported problems. Future
live-agent evaluation must test omissions, vague next actions, unweighted
choices, absent problem records, and attempts to proceed around a documented
problem.

### Observed specialist-capability correction — 2026-09-04

A real workflow trace showed that the conductor declared a mandatory specialist
unavailable before inspecting the active internal agent tools. The route was
therefore blocked for a host limitation that did not exist. This confirmed
caller-enforcement failure, so the smallest corrective implementation is
authorized without reordering the research priorities in this roadmap: every specialist
route receives a separate validated capability-discovery record bound to the
exact routing decision and summarized in the checkpoint. A suitable inspected
internal interface forces `AVAILABLE` and invocation; incomplete discovery is
`UNKNOWN`; only a complete search with no suitable interface permits
`UNAVAILABLE` and a linked blocker. Regression cases cover the false blocker,
ignored interface, incomplete search, and route mismatch. This correction does
not perform the specialist review, change research state, authorize data or a
backtest, or claim that a caller-enforced checkpoint can independently discover
an interface the live agent omitted from its inventory record.
### Owner-authorized scientific-method capability integration — 2026-09-04

The owner authorized the use of four local scientific-method capabilities where
they provide a concrete improvement to a research or capital decision:
`scientific-critical-thinking`, `scientific-brainstorming`,
`hypothesis-generation`, and `statistical-analysis`. This is a
**KEEP — agent enforcement** integration: it makes existing controls for
alternative explanations, evidence limits, measurement, falsification, and
quantitative uncertainty more likely to be applied consistently. It does not
add a new routing gate, artifact type, claim status, specialist owner, or
authorization for data access, a backtest, validation, deployment, or capital
allocation.

The integration is deliberately role-bound. Critical thinking may expose bias,
confounding, design, or claim-overreach risks, but may not replace the
scientific-philosophy, causal-identification, evidence, or outcome-contract
requirements. Brainstorming may structure genuinely requested new ideation,
but every trading idea remains an unranked `INBOX` candidate with visible
origin and the complete candidate family remains subject to search-space
accounting. Hypothesis generation may draft rivals, discriminating predictions,
operationalizations, and falsifiers, but its templates are not canonical
project artifacts and it cannot promote a candidate or accept causal wording.
Statistical analysis may be used only by the bounded `data-analyst` for a
scoped, referenced data question; finance-specific checks for temporal
dependence, decision-time availability, leakage, regimes, costs, execution,
and time-separated evaluation remain mandatory.

The capabilities may also support a bounded research-process or live-agent
evaluation question when that work protects a named framework or capital
decision. They do not authorize detached AI, psychology, or philosophy
research. Their implementation must preserve the existing conductor, artifact,
fingerprint, and validation boundaries. A framework-integrity run can verify
that these contracts remain present; it cannot by itself establish that a model
uses the methods well, which remains a live-agent evaluation question under
priority 4.

### Subsequent scientific-capability screen — 2026-09-04

Six subsequently installed capabilities were screened against the same
decision-protection criterion. `statistical-power`, `statsmodels`, PyMC, and
SymPy have a direct, bounded use inside already-authorized work: respectively,
prospective sensitivity to a decision-relevant after-cost effect; specified
econometric/time-series estimation and diagnostics; predeclared Bayesian
uncertainty models with prior and posterior predictive checks; and exact
formula or boundary-condition verification before an operationalization is
tested. They remain method aids and must write their material inputs, output,
versions, seeds where applicable, assumptions, and limitations into the
existing artifact and fingerprint.

`experimental-design` is not activated for market research. Its randomization,
treatment, and experimental-unit machinery does not transfer to naturally
occurring market observations, and it would not supply causal identification.
It may be reconsidered only for an owner-requested, separately scoped
simulation or live-agent evaluation design with a genuine assignment or run-
order problem. `timesfm-forecasting` is likewise not activated: zero-shot
forecast output would create a new predictive model and a material search path.
It may be proposed only as a named new candidate after the validation-boundary
and live-agent controls applicable to that path are implemented; its model
weights, configuration, context, horizon, data transformations, forecast
availability, and baselines would then be fingerprinted and tested as part of
the unchanged full pipeline. Neither deferred capability is an authorization to
download a model, access data, run a backtest, or make a forecast claim.

### Owner-authorized scientific-skill discovery and reproducibility — 2026-09-04

The approved and deferred local scientific-method capabilities are recorded in
`capabilities/scientific_skill_manifest.v1.json`, validated by
`schemas/scientific_skill_manifest.schema.json` and its regression test. This
is a **KEEP — agent enforcement** addition: it protects the method-selection
and reproducibility decision by giving every project agent one versioned map of
allowed roles, scope, prohibitions, source license, and the reviewed `SKILL.md`
version and hash. It does not vendor third-party skill packages, because a
copied package would create a second update and license-maintenance surface.

The manifest is not evidence that a host actually exposes a skill. Before an
active optional skill is used, the agent must inspect its current inventory and
match the installed `SKILL.md` to the reviewed snapshot. If absent or changed,
the optional method is simply unavailable for that task; it is not a blocker
and cannot be claimed as used. If it materially influences a research artifact,
the effective runtime snapshot and, where relevant, the manifest are protected
through the existing `METHOD` artifact/fingerprint mechanism. This adds no
new route, owner, specialist, gate, data access, backtest, deployment, or
capital-allocation authority. The manifest/test verifies discoverability and
snapshot consistency only; live-agent evaluation remains required to claim a
behavioral improvement.

