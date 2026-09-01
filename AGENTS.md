# Research-agent entry point

This repository may be edited by Codex, Claude, the user, or another compatible
agent. Inspect the worktree and relevant history before editing, and never
overwrite unfamiliar concurrent work.

## Project language policy

From now on, write every new or changed repository artifact in English. This
applies to documentation, agent instructions, schema titles and descriptions,
examples, framework-facing messages, code comments, and commit messages. Do
not translate unchanged German material as part of an unrelated task. The
existing German content will be translated and the terminology documented in
a separate, explicitly requested migration later. This repository-language
rule does not require the user conversation to be in English; continue to speak
with the user in the language they use.

When that translation migration begins, keep translation and editorial change
strictly separate. A translation-only commit must preserve the normative
meaning, requirements, structure, and examples of its source. Any shortening,
deduplication, clarification that changes emphasis, or other substantive edit
must follow in a second commit and be reviewed independently. Never combine
translation and semantic revision in one commit, because an observed change in
agent behaviour must remain attributable to one kind of change.

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
