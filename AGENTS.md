# Research-agent entry point

This repository may be edited by Codex, Claude, the user, or another compatible
agent. Inspect the worktree and relevant history before editing, and never
overwrite unfamiliar concurrent work.

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
5. before accepting the returned artifact, compare research question,
   strategy, market, time horizon, trigger, and target with
   `scripts/check_research_identity.py`;
6. accept and validate the artifact only when that check reports `UNCHANGED`,
   then save a new checkpoint.

If the requested conclusion is `INTERVENTIONAL` or `COUNTERFACTUAL`, the router
must send the design to `agents/causal-identification-critic.md` before any
causal estimate or causal wording is accepted. A predictive strategy question
does not trigger this review. An estimator, event window, temporal ordering, or
causal-discovery result is never a substitute for the required identification
assessment.

If the identity check finds a difference, keep the pre-handoff identity and the
returned artifact unaccepted. Explain the changed dimensions and practical
consequences in ordinary language, then ask whether the original research
should remain in force or an explicitly new version should be created. A
specialist may propose a change, but may not make it effective silently.

Do not substitute a prose claim that a specialist "would be useful" for the
required specialist call. If the host cannot invoke that specialist, stop at
the unmet prerequisite and say plainly what remains undone.

Treat the user as a research decision-maker, not a software developer. Lead
with findings and decisions, use ordinary language, and omit implementation
details unless requested or decision-relevant. A request to reconstruct or
operationalize a strategy does not itself authorize a backtest.
