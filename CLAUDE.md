# Memory

## Active project

`research_framework` may be edited by both Codex and Claude, including concurrently.

## Mandatory research coordination

- For every user-facing trading-research task, act as the top-level
  `research-conductor` defined in `agents/research-conductor.md`.
- Before a material research transition, update an orchestration checkpoint and
  run `scripts/route_research_task.py`; follow mandatory specialist routes.
- Specialists return bounded artifacts to the conductor and do not take over
  the user conversation. Validate their output before advancing.
- Around every specialist handoff on existing research, preserve and compare
  the six-part research identity: question, strategy, market, time horizon,
  trigger, and target. Run `scripts/check_research_identity.py` before accepting
  the output. If it differs, keep the original in force and explain the change
  to the user before any new version is created.
- If a required specialist cannot be invoked, stop at that prerequisite instead
  of simulating its contribution.
- Reconstructing or operationalizing a strategy does not authorize a backtest.
- Route every requested interventional or counterfactual claim to the
  `causal-identification-critic` before estimation or causal wording. Do not
  trigger it for a question that remains explicitly predictive. DML, local
  projections, event-study coefficients, Granger precedence, and causal
  discovery do not count as identification by themselves.

## Collaboration preferences

- Do not assume that Codex is the only author of local or remote changes.
- Treat unfamiliar changes and commits as potentially belonging to Claude or the user.
- Before editing, committing, merging, switching, or pushing, inspect the current worktree and relevant branch history again.
- Re-read affected files immediately before patching when another collaborator may have worked on them.
- Never overwrite, reset, revert, or otherwise discard unfamiliar work without first identifying its origin and obtaining user direction when needed.
- Treat the user as a research decision-maker, not a software developer. Lead with outcomes and decisions, use plain language, and omit implementation details unless requested or decision-relevant.
