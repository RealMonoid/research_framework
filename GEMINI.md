# Memory

## Active project

`research_framework` may be edited by Codex, Claude, and Gemini, including concurrently.

## Project language policy

- Write every new or changed repository artifact in English, including
  documentation, agent instructions, schema text, examples, framework-facing
  messages, code comments, and commit messages.
- Do not translate otherwise unchanged German content during unrelated work.
  A separate migration may translate the existing material only when the user
  explicitly requests it and a measured agent-reliability or actual
  maintenance need justifies it.
- This rule applies to repository content, not to the conversation: continue
  speaking with the user in the language they use.
- If a translation migration begins, use translation-only commits that
  preserve the source meaning, requirements, structure, and examples. Put any
  shortening, deduplication, change of emphasis, or substantive clarification
  in a second commit and validate it separately. Never combine translation and
  semantic revision in one commit; changes in agent behaviour must remain
  attributable to one type of change.

## Scope and restraint

- Treat this as a private decision-support framework for one research owner
  working with AI agents, not as an academic-publication, external-review, or
  human-team onboarding project.
- Add or retain process when it protects a research or capital decision, or
  when it demonstrably improves agents' delivery of an existing protection.
  Do not add work solely for public presentation, external persuasion,
  hypothetical contributors, or stylistic completeness.
- A full migration of legacy German material is conditional on measured agent
  reliability or maintenance value; it is not justified by an assumed public
  audience.
- Prune conservatively. If the protective value of an existing rule is
  uncertain, keep it until the hard-gate inventory, a real Research Case, or
  behavioural agent evaluation supports removal. Make each removal explicit
  and independently reviewable.
- Never commit proprietary strategies, private data, real Research Cases, or
  empirical results to this public repository. Use an external private
  location or the ignored `private_research/` path. Preserve existing examples
  until the user authorizes a separate privacy review and any resulting
  removal.

## Data acquisition and verification burden

- Prefer one complete, reusable, versioned data export or snapshot that can be
  checked by code. Do not make repeated TradingView scrolling, bar-by-bar
  loading, or manual extraction of chart segments a normal prerequisite.
- Run automated integrity, coverage, and cross-source checks first. Use manual
  visual review only for a named residual risk that code cannot check
  reliably. Define the case-selection rule before inspection and keep the
  burden to the smallest defensible scope.
- Never impose an arbitrary screenshot quota or ask the user to certify data
  quality through repetitive visual checking.
- If suitable data cannot be obtained as a coherent dataset without material
  repetitive user work, report `REMEDIABLE_GAP`, `NOT_TESTABLE`, or `BLOCKED`
  as applicable. Do not weaken the claim, coarsen the strategy, substitute an
  instrument, or transfer data-engineering work to the user merely to continue.
- Preserve residual data uncertainty even when a manual check is not justified.

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

- Do not assume that Codex or Claude is the only author of local or remote changes.
- Treat unfamiliar changes and commits as potentially belonging to Codex, Claude, or the user.
- Maintain `AGENT_CHANGELOG.md`: check it before starting work to review recent changes by other agents, and record every completed change in English with exact timestamp (date and time), full agent model name and version number (e.g. `Gemini 3.8 Flash`, `ChatGPT 5.6 Sol`), affected files, detailed WHAT was changed, detailed WHY it was changed (including an explicit problem description, decision context, and invariants protected), and verification status.
- Before editing, committing, merging, switching, or pushing, inspect the current worktree and relevant branch history again.
- Re-read affected files immediately before patching when another collaborator may have worked on them.
- Never overwrite, reset, revert, or otherwise discard unfamiliar work without first identifying its origin and obtaining user direction when needed.
- Treat the user as a research decision-maker, not a software developer. Lead with outcomes and decisions, use plain language, and omit implementation details unless requested or decision-relevant.
