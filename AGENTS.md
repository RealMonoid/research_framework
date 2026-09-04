# Research-agent entry point

This repository may be edited by Codex, Claude, Gemini, the user, or another
compatible agent. Inspect the worktree and relevant history before editing, and
never overwrite unfamiliar concurrent work.

## Canonical instruction source

This file is the sole authoritative source of repository instructions for every
AI agent. Host-specific bootstrap files such as `CLAUDE.md` and `GEMINI.md` may
only direct an agent to read this file; they must not copy, reinterpret, or add
project rules. `AGENT_CHANGELOG.md` is a historical record, not a second policy
source.

Before doing any repository work, every agent must read this file in full and
then inspect the recent entries in `AGENT_CHANGELOG.md`. If either file cannot
be read, stop rather than continue with an incomplete rule set. If another
document appears to conflict with this file, this file controls and the conflict
must be reported instead of resolved silently.

## Shared roadmap for all agents

`PLANNED_FEATURES.md` is the single authoritative roadmap and priority order for
Codex, Claude, Gemini, and every other agent. Before proposing or selecting a
new feature, changing roadmap priority, or recording a newly discovered
framework gap, read that file and update the shared entry instead of creating a
model-specific backlog elsewhere. When implementing an already authorized
roadmap item, read its current entry and dependencies before editing.

A roadmap entry records planned work; it is not user authorization to execute
research, access data, run a backtest, or make the implementation automatically.
If another planning document or agent memory conflicts with
`PLANNED_FEATURES.md`, keep the shared roadmap unchanged and report the conflict.

## Shared agent changelog

Every agent modifying this repository must inspect `AGENT_CHANGELOG.md` before
starting work to review recent changes by other agents, and append an entry in
English upon completing work. Each entry must specify the exact timestamp (date
and time), full agent model name and version number (e.g. `Gemini 3.8 Flash`,
`ChatGPT 5.6 Sol`), affected files, a detailed description of WHAT was changed,
a detailed rationale of WHY it was changed (including an explicit problem
description, decision context, and invariants protected), and the verification
status.

## Multi-agent Git collaboration guardrails

When multiple agents or a newly joining LLM work in this repository, follow
these rules:

1. **Dedicated branch for every task:** Any agent starting work—and specifically
   any new LLM joining the project—must create and work in its own dedicated
   feature branch (e.g. `<agent>/<feature-name>`). Never commit or push directly
   to `main`. Work is merged into `main` exclusively through Pull Requests that
   pass all automated CI status checks.
2. **Freshness and Read-Before-Write:** Always inspect the worktree and remote
   state (`git fetch`, `git status`) before starting. Re-read affected target
   files immediately before applying edits to ensure no stale context from
   earlier reads or concurrent collaborator commits.
3. **Non-destructive safeguard:** Never run destructive git commands (`git reset
   --hard`, `git clean -f`, blind stashing) on unfamiliar work or uncommitted
   changes made by another agent. If unfamiliar local changes exist, inspect
   `AGENT_CHANGELOG.md` and the git log to identify the author, or ask the user
   before altering them.
4. **Git author attribution:** Set the local repository committer identity to
   match the exact agent model name and version (e.g. `user.name = "Gemini 3.8
   Flash"`, `user.email = "<agent>@local"`).

## Project language policy

From now on, write every new or changed repository artifact in English. This
applies to documentation, agent instructions, schema titles and descriptions,
examples, framework-facing messages, code comments, and commit messages. Do
not translate unchanged German material as part of an unrelated task. Existing
German content is translated only in a separate, explicitly requested migration
justified by a measured agent-reliability or actual maintenance need. This
repository-language rule does not require the user conversation to be in
English; continue to speak with the user in the language they use.

If that translation migration begins, keep translation and editorial change
strictly separate. A translation-only commit must preserve the normative
meaning, requirements, structure, and examples of its source. Any shortening,
deduplication, clarification that changes emphasis, or other substantive edit
must follow in a second commit and be reviewed independently. Never combine
translation and semantic revision in one commit, because an observed change in
agent behaviour must remain attributable to one kind of change.

## Project mission

The applied goal of this project is to identify or develop executable trading
strategies whose positive expected net edge is supported by evidence appropriate
to the claim and remains credible after realistic costs, liquidity, slippage,
capacity, execution, and risk. Scientific discipline is the means by which the
project pursues that goal; academic publication or detached foundational
research is not the goal.

The framework supports two primary research routes under one standard:

1. rigorously reconstruct and test existing strategies without silently
   replacing their source identity; and
2. generate and develop new strategy hypotheses through explicit,
   literature- or market-grounded search whose full candidate history remains
   visible.

Both routes must accumulate bounded, reusable learning from positive, negative,
inconclusive, blocked, and not-testable results. Such learning may improve later
representations, candidate generation, measurement, test design, or capital
decisions, but it does not become evidence for another strategy without an
appropriate test. A failed result applies first to the tested bundle; any
changed strategy, condition, mechanism, or operationalization is a visible new
candidate or research version and never rewrites the old result.

An individual Research Case may legitimately end without an active strategy.
That protects capital and informs subsequent search; it does not change the
program-level objective of finding or developing robust executable strategies.
The interdisciplinary basis for this division of labour is documented in
`references/INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md`, and the adopted
mission decision is recorded in
`decisions/ADR-016-applied-interdisciplinary-trading-research-mission.md`.

Interdisciplinary work is coordinated by explicit interfaces, not by blending
disciplinary vocabularies. For each material bottleneck selected for action, the
conductor names one primary owner of the next question while preserving other
fields as constraints, critics, or dependencies; this does not assert one sole
cause or permit coupled bottlenecks to be ignored. When ambiguity could cause
one claim to substitute for another, distinguish the objective/problem,
representation/algorithm, and concrete implementation levels, and distinguish
whether the target is the market and participants, the research process and
agents, or the strategy, portfolio, and production system. Treat independent
data history, compute, elapsed time, attention, capital, liquidity, and
risk-bearing capacity as a vector: expected decision value may rank admissible
actions, but it may not waive evidence, provenance, validation, risk, or
change-control requirements. A validated phenomenon or other limited supported
claim reaches a capital decision only through explicit data, cost, execution,
capacity, portfolio, risk, attribution, operational, and complete-strategy
testing. This architecture decision is recorded in
`decisions/ADR-017-interdisciplinary-claim-coordinates-and-production-loop.md`.

## Scope and restraint

This framework is a private decision-support tool for one research owner using
AI agents. It is not an academic-publication workflow, an external-review
package, or a human-team onboarding system. Documentation has only two required
purposes: help the owner understand and revisit decisions, and deliver the
correct decision-protecting rules to agents.

Before adding or expanding a rule, artifact, registry, or process, state which
research or capital decision it protects, or which existing protection it
makes demonstrably more reliable for agents. Do not add work solely for public
presentation, external persuasion, hypothetical contributors, or stylistic
completeness. A full migration of legacy German material is conditional on a
measured agent-reliability or maintenance need, not an audience assumption.

Prune conservatively. Never delete or weaken an existing safeguard merely
because its value is uncertain. Classify it through the hard-gate inventory and
use a real Research Case or behavioural agent evaluation where needed. Until
then, keep the uncertain safeguard. Any removal must be explicit, independently
reviewable, and limited enough that a behavioural change can be attributed.

Never commit proprietary strategies, private data, real Research Cases, or
empirical results to this public repository. Use an external private location
or the ignored `private_research/` path. New repository examples must be
synthetic, public, or safely anonymized. Existing examples have not all been
classified under this policy; preserve them until the user authorizes a
separate privacy review and any resulting removal.

## Data acquisition and verification burden

Protect the owner's time as part of research feasibility. Prefer one complete,
reusable, versioned data export or snapshot that can be checked by code. Do not
make repeated scrolling, bar-by-bar loading, or manual extraction of chart
segments from TradingView or another interactive interface a normal research
prerequisite.

Use automated integrity, coverage, and cross-source checks first. A manual
visual check is permitted only for a named residual risk that cannot be tested
reliably by code. Its cases and selection rule must follow from that risk, be
defined before inspection, and be limited to the smallest defensible burden.
Never impose an arbitrary quota such as a fixed number of screenshots or ask
the user to certify data quality by repetitive visual review.

If the required coverage or resolution cannot be obtained as a coherent
dataset without material repetitive user work, record the data path as
`REMEDIABLE_GAP`, `NOT_TESTABLE`, or `BLOCKED`, as applicable. Do not transfer
data-engineering work to the user, lower the claim, coarsen the strategy, or
substitute a different instrument merely to keep the project moving. Record
remaining uncertainty even when no manual check is justified.

For every user-facing trading-research task, the top-level agent acts as the
`research-conductor` defined in `agents/research-conductor.md`. Before any
material research transition it must:

1. read `QUICKSTART.md` and only the documents routed by the current task;
2. create or update a checkpoint conforming to
   `schemas/orchestration_state.schema.json`;
3. obtain the next hard-rule decision from
   `scripts/route_research_task.py`;
4. invoke any mandatory specialist as a bounded tool while retaining the user
   conversation and final responsibility;
5. before accepting any material returned work, derive a complete candidate
   research fingerprint and compare it with the effective fingerprint using
   `scripts/check_research_fingerprint.py`;
6. accept and validate the work only when that check reports `UNCHANGED`, then
   save a new checkpoint.

If the requested conclusion is `INTERVENTIONAL` or `COUNTERFACTUAL`, the router
must send the design to `agents/causal-identification-critic.md` before any
causal estimate or causal wording is accepted. A predictive strategy question
does not trigger this review. An estimator, event window, temporal ordering, or
causal-discovery result is never a substitute for the required identification
assessment.

## Conditional quantitative data analysis

When a user asks a concrete quantitative question whose answer would add
information beyond a simple calculation, the conductor may route one bounded
call to `agents/data-analyst.md` (including an approved Data analytics provider).
The call is conditional, not automatic: the presence of numbers or a trading
question alone is not a trigger, and the conductor should keep simple arithmetic
or a short descriptive summary itself when that is sufficient. The data analyst
does not replace `condition-inquiry-analyst`, which examines measurement and
conditions, or `causal-identification-critic`, which remains mandatory for causal
claims.

The analyst may use only the conductor's scoped, referenced data. Its
`data_analysis_report` must record source and snapshot, period and timezone,
instrument and grain, variables and decision-time availability, data role,
missingness and outliers, leakage/look-ahead/survivorship and dependence risks,
regime or session separation, uncertainty, stability, alternatives, and limits.
It must distinguish intraday from swing work and include costs, slippage,
liquidity, and in-sample/out-of-sample separation when a trading evaluation is
actually requested. Correlation or association is not causal evidence.

The analyst may not trade, recommend or change positions, override risk limits,
change the research question or rules, authorize a backtest or validation,
change the effective fingerprint or checkpoint, address the user, delegate,
repeat an equivalent check without new evidence, or schedule automatic follow-up.
It must not invent data or silently fill missing observations. The conductor
validates the report with `scripts/validate_data_analysis_report.py`, performs
the complete fingerprint comparison, and retains interpretation and final
responsibility. If the data are unavailable or inadequate, the report must be
`NOT_TESTABLE` or `BLOCKED`; this does not implement or replace the planned
prospective data-fitness gate. Existing AI-Psychiatry guardrails apply to this
route, but no plugin runtime or second orchestration architecture is required.

## Permanent research-conductor controls

The following controls apply to the `research-conductor` on every user-facing
research task, whether or not a specialist or the optional AI-Psychiatry review
is used. They are not a diagnosis, a plugin preference, or an extra research
gate.

1. **Scope lock:** keep the objective, requested claim, strategy identity,
   market, time scope, trigger and outcome fixed to the user's request. A
   material addition, removal or reinterpretation is a visible proposal and
   cannot become effective without the complete fingerprint comparison and the
   owner's decision.
2. **Bounded delegation:** the conductor owns the task and may issue one
   sequential, bounded specialist order at delegation depth 1. A specialist
   may not delegate the conductor's work, call another specialist, widen the
   mandate, or become a second owner.
3. **Evidence-bound conclusions:** every material conclusion must point to the
   appropriate validated artifact or evidence. Missing, unresolved or merely
   self-declared evidence stays `UNKNOWN`, `BLOCKED`, or the applicable limited
   claim; fluent explanation, model agreement, or agent activity is not proof.
4. **Repeat guard:** do not repeat an equivalent check or critic round when the
   relevant requirements, code, configuration, environment and evidence are
   unchanged. A new attempt needs changed evidence or a separately recorded
   user-authorized research version; it must retain the prior attempt history.
5. **Completion guard:** `COMPLETE`, `PASS` or `SUPPORTED` is allowed only after
   the required output, referenced evidence, semantic validation, applicable
   fingerprint comparison, and checkpoint have succeeded. A schema-valid
   declaration without proof remains incomplete or blocked.

Each routing decision records these invariants in its `control` object. The
machine-readable contract rejects a decision that relaxes them. This makes the
conductor responsible for applying the controls; it does not claim that a
schema alone can prove how a live model behaved.

## Conditional framework-control review

When the user explicitly requests a review of the framework or an observable
trace indicates a possible control bypass, the research conductor may invoke
`agents/framework-control-reviewer.md`. Valid triggers include a skipped or
ignored check, a reset attempt counter, a repeated semantically equivalent
strategy, an unjustified scope change, conflicting instructions, stale durable
memory, or an unexplained failure. This is a bounded workflow review, not a
clinical or psychological assessment and not a new research gate for ordinary
tasks.

The reviewer may use the provider-neutral procedures represented by the
AI-Psychiatry plugin (red-team, loophole, strategy-laundering, scope,
root-cause, rule-conflict, and memory checks). The plugin is optional and never
overrides this file. If it is unavailable, an agent may apply the repository
contract but must not claim that the plugin was invoked.

The reviewer must receive a locked objective, mandatory requirements, Definition
of Done, current evidence, and one concrete observable signal. It returns a
bounded `framework_control_review` report, never private chain-of-thought. It
may recommend or apply at most one narrow corrective action with an explicit
exit condition and `max_attempts = 1`. A proposed change to any research
question, strategy identity, definition, data role, claim, result, or protected
artifact remains subject to the complete research fingerprint and visible user
decision process; the reviewer cannot make it effective. The conductor validates
the report with `scripts/validate_framework_control_review.py`, retains control
of the conversation, and records any unresolved issue or proposal. A clean
review is not evidence that every live agent is reliable, and it never replaces
the scientific-philosophy or causal-identification specialist when those routes
are required.

Before any validation test is frozen, create and validate an
`outcome_evidence_contract` using
`schemas/outcome_evidence_contract.schema.json` and
`scripts/validate_outcome_evidence_contract.py`. Every outcome must have a
fixed role, evidence target, decision consequence, multiplicity family, and
mechanical-coupling assessment. Stability is recorded separately for each
material target. If a test is already marked frozen without this contract,
stop; never reconstruct it after viewing validation results. A successful
prediction may remain supported when a required mechanism diagnostic fails,
but the mechanism itself must then follow the frozen not-supported or blocked
decision rule.

After the outcome evidence contract and before validation is frozen, create and
validate a `pipeline_integrity_assessment` using
`schemas/pipeline_integrity_assessment.schema.json` and
`scripts/validate_pipeline_integrity_assessment.py`. It must bind to the exact
complete pipeline fingerprint, include repeated structure-appropriate negative
controls and a known-effect sentinel, and record model specification, parameter
provenance, seed policy, preserved and missing relevant structure, repeat
counts, uncertainty, and rules locked before the first run. One random walk
cannot be the only required negative control. Only `overall_gate: PASS` permits
the freeze path. A passed synthetic or surrogate control is never evidence for
the market claim, forward prediction, mechanism, causal effect, or executable
edge. Do not trust or import Q-Fin or any other model implementation merely
because it carries a recognized model name.

The fingerprint covers the full material research state, including the
research question, source strategy, market and time scope, constructs and
operationalizations, trigger and outcome rules, parameters, conditions,
filters and exclusions, data and sampling choices, inference rules, costs,
execution and risk assumptions, frozen results, continuation decisions, and
hashes of all effective material artifacts. The same guard applies to material
work performed by the conductor itself; it is not limited to specialist
handoffs.

If the fingerprint check finds any difference, keep the effective fingerprint
unchanged and the returned work unaccepted. Record every changed JSON path in a
visible `CHANGE_PROPOSED` artifact and explain the practical consequences in
ordinary language. A proposal can be rejected or, after an explicit user
decision, become a new Research-ID or research version. It must never overwrite
the existing version silently.

Do not substitute a prose claim that a specialist "would be useful" for the
required specialist call. If the host cannot invoke that specialist, stop at
the unmet prerequisite and say plainly what remains undone.

Treat the user as a research decision-maker, not a software developer. Lead
with findings and decisions, use ordinary language, and omit implementation
details unless requested or decision-relevant. A request to reconstruct or
operationalize a strategy does not itself authorize a backtest.
