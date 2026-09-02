# Research-agent entry point

This repository may be edited by Codex, Claude, Gemini, the user, or another
compatible agent. Inspect the worktree and relevant history before editing, and
never overwrite unfamiliar concurrent work.

## Shared agent changelog

Every agent modifying this repository must inspect `AGENT_CHANGELOG.md` before
starting work to review recent changes by other agents, and append a concise
entry with timestamp, agent name, affected files, summary, and verification
status upon completing work.

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
