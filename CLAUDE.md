# Memory

## Active project

`research_framework` may be edited by both Codex and Claude, including concurrently.

## Project language policy

- Write every new or changed repository artifact in English, including
  documentation, agent instructions, schema text, examples, framework-facing
  messages, code comments, and commit messages.
- Do not translate otherwise unchanged German content during unrelated work.
  A separate migration will translate the existing material and document the
  English terminology when the user explicitly requests it.
- This rule applies to repository content, not to the conversation: continue
  speaking with the user in the language they use.
- During the future translation migration, use translation-only commits that
  preserve the source meaning, requirements, structure, and examples. Put any
  shortening, deduplication, change of emphasis, or substantive clarification
  in a second commit and validate it separately. Never combine translation and
  semantic revision in one commit; changes in agent behaviour must remain
  attributable to one type of change.

## Mandatory research coordination

- For every user-facing trading-research task, act as the top-level
  `research-conductor` defined in `agents/research-conductor.md`.
- Before a material research transition, update an orchestration checkpoint and
  run `scripts/route_research_task.py`; follow mandatory specialist routes.
- Specialists return bounded artifacts to the conductor and do not take over
  the user conversation. Validate their output before advancing.
- Around every material research step, preserve and compare the complete
  effective research fingerprint with `scripts/check_research_fingerprint.py`.
  It covers all definitions, parameters, filters, exclusions, data choices,
  inference rules, execution assumptions, frozen results, continuation
  decisions, and material artifact hashes. Every difference remains a visible
  proposal; keep the original effective until the user explicitly authorizes a
  new Research-ID or research version. Never silently overwrite it.
- If a required specialist cannot be invoked, stop at that prerequisite instead
  of simulating its contribution.
- Reconstructing or operationalizing a strategy does not authorize a backtest.
- Route every requested interventional or counterfactual claim to the
  `causal-identification-critic` before estimation or causal wording. Do not
  trigger it for a question that remains explicitly predictive. DML, local
  projections, event-study coefficients, Granger precedence, and causal
  discovery do not count as identification by themselves.
- Before validation is frozen, create and validate the outcome evidence
  contract. Do not proceed with a frozen test if it is missing, and never
  reconstruct it after viewing results. Apply its decision rules separately:
  predictive success does not preserve a mechanism whose required diagnostics
  were contradicted, non-discriminating, or invalid.
- After the outcome contract and before validation is frozen, require a passing
  pipeline-integrity assessment. Run the unchanged complete pipeline on
  repeated structure-appropriate negative controls and a known-effect
  sentinel. Record the exact pipeline fingerprint, model and parameter source,
  seed policy, preserved and missing relevant structure, repeat counts,
  uncertainty, and rules locked before the first run. One random walk cannot be
  the only required negative control. A pass authorizes only the freeze path;
  it is not evidence for a market effect, prediction, mechanism, causal effect,
  or trading edge. Do not import Q-Fin or another model implementation merely
  because it carries a recognized model name.

## Collaboration preferences

- Do not assume that Codex is the only author of local or remote changes.
- Treat unfamiliar changes and commits as potentially belonging to Claude or the user.
- Before editing, committing, merging, switching, or pushing, inspect the current worktree and relevant branch history again.
- Re-read affected files immediately before patching when another collaborator may have worked on them.
- Never overwrite, reset, revert, or otherwise discard unfamiliar work without first identifying its origin and obtaining user direction when needed.
- Treat the user as a research decision-maker, not a software developer. Lead with outcomes and decisions, use plain language, and omit implementation details unless requested or decision-relevant.
