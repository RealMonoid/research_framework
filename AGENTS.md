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
5. validate the returned artifact before advancing and save a new checkpoint.

Do not substitute a prose claim that a specialist "would be useful" for the
required specialist call. If the host cannot invoke that specialist, stop at
the unmet prerequisite and say plainly what remains undone.

Treat the user as a research decision-maker, not a software developer. Lead
with findings and decisions, use ordinary language, and omit implementation
details unless requested or decision-relevant. A request to reconstruct or
operationalize a strategy does not itself authorize a backtest.
