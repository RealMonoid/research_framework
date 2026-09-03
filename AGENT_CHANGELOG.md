# Agent Collaboration Changelog

This file records completed work by AI agents. It is a historical record, not
an instruction source. All binding repository rules and changelog requirements
are defined only in `AGENTS.md`. Read `AGENTS.md` in full before using this log.

## Log entries

### 2026-09-03T16:04:00+02:00 | ChatGPT 5.6 Sol | Add quant-finance evidence to failed-strategy synthesis
- **Files/areas**: `references/FAILED_STRATEGY_EPISTEMOLOGY.md` and `AGENT_CHANGELOG.md`.
- **What**: Extended the epistemic research note with primary quant-finance and forecast-evaluation work on White's Reality Check, Hansen's Superior Predictive Ability test, the Model Confidence Set, Probability of Backtest Overfitting, Deflated Sharpe Ratio, local forecast comparison under instability, post-sample versus post-publication decay, and joint calibration of false and missed discoveries. Grouped these methods into selection accounting, set-valued comparison, failure-pattern localization, and decision calibration, and integrated their limits into the broader rival-explanation synthesis.
- **Why**: **Problem description**: Philosophy and general statistics establish why failure attribution is underdetermined, but the user's requested synthesis also needed methods tailored to adaptive searches over one financial history, unstable predictive performance, and asymmetric capital costs. **Decision context**: This remains a literature synthesis only; no strategy, data, backtest, or framework rule was changed. **Protected invariants**: Search-risk diagnostics are not presented as market-mechanism identification; a local break does not name its economic cause; a selected quant metric cannot confirm a post-hoc explanation; predictive comparison, causal explanation, and executable edge remain separate; non-identification and multiple surviving explanations remain permitted outcomes.
- **Verification**: Checked the eight added records against official journal DOI pages, author-hosted manuscripts, or an institutional open repository; verified that each method's permitted inference and attribution limit are stated; `git diff --check` passed. No market data, empirical strategy test, simulation, backtest, trade, framework validator, or live-agent release gate was run.

### 2026-09-03T15:51:54+02:00 | ChatGPT 5.6 Sol | Research epistemic learning from failed strategies
- **Files/areas**: `references/FAILED_STRATEGY_EPISTEMOLOGY.md` and `AGENT_CHANGELOG.md`.
- **What**: Added one bounded research note synthesizing primary philosophy-of-science and mathematical/statistical sources on what can and cannot be learned from a failed strategy. The note covers Duhem and Quine on underdetermination, Lakatos on progressive versus degenerating continuation, Mayo's severe-testing account, Bayesian comparison and predictive model criticism, statistical identifiability and misspecification, discriminating and sequential experimental design, selective inference, and the exploratory/confirmatory distinction. For every approach it records permitted inferences, prohibited inferences, and the design conditions required for learning. It then combines them into a discriminating-failure map that preserves bundle-level negative knowledge, tests whether rival explanations have different observable signatures, separates relative comparison from absolute model adequacy, accounts for adaptive selection, and allows non-identification or failure of the entire candidate model set as explicit outcomes.
- **Why**: **Problem description**: A binary strategy failure can invite either over-narrow technical debugging or unconstrained post-hoc stories about mechanisms, regimes, and conditions. The existing Duhem-Quine and Lakatos controls correctly prevent unique blame and retrospective rescue, but the user requested a broader account of whether a failure can produce knowledge and how philosophy can be connected to mathematical and statistical methods. **Decision context**: This was a research-only sidecar limited to philosophy and statistical foundations; quant-finance backtest-overfitting literature, strategy data, market tests, framework-rule changes, and backtest proposals were explicitly excluded. **Protected invariants**: The frozen meaning of any strategy result remains unchanged; a failed conjunction is not silently converted into unique causal attribution; post-hoc explanation remains hypothesis generation unless selection is accounted for or new evidence is used; relative model preference is not treated as absolute adequacy; non-identification remains an acceptable conclusion; no market, trading, profitability, or causal claim was added.
- **Verification**: Read `AGENTS.md` in full and inspected the latest changelog entries before editing; fetched the remote state and confirmed a clean dedicated branch based on current `origin/main`; checked all fourteen cited records against original works, official journal/publisher DOI pages, or author-hosted manuscripts; confirmed that all eight requested topic families are present with inference limits and design conditions; `git diff --check` passed. No strategy data, market test, simulation, backtest, trade, framework validator, or live-agent release gate was run.

### 2026-09-03T14:43:01+02:00 | ChatGPT 5.6 Sol | Integrate bounded quantitative Data specialist
- **Files/areas**: `AGENTS.md`, `agents/data-analyst.md`, `agents/research-conductor.md`, `00_RESEARCH_AGENT_README.md`, `05_AGENT_OPERATIONS.md`, `QUICKSTART.md`, `README.md`, `PLANNED_FEATURES.md`, `HARD_GATE_INVENTORY.md`, `decisions/ADR-015-bounded-data-specialist.md`, `schemas/data_analysis_report.schema.json`, `schemas/orchestration_state.schema.json`, `schemas/routing_decision.schema.json`, `examples/data_analysis_report.synthetic.json`, `examples/orchestration_state.prose_strategy.json`, `examples/routing_decision.pre_operationalization.json`, `scripts/validate_data_analysis_report.py`, `scripts/test_data_analysis_report.py`, `scripts/route_research_task.py`, `scripts/test_research_orchestration.py`, `scripts/test_schemas.py`, `scripts/test_schemas.ps1`, `scripts/validate_framework.py`, and `scripts/validate_framework.ps1`.
- **What**: Added a provider-neutral, conditional `data-analyst` specialist route and a machine-checked `data_analysis_report` contract. The report records scoped question, source snapshot, period, instrument, grain, variables, decision-time availability, data role, quality checks, missingness, outliers, leakage/look-ahead, survivorship, dependence, session/regime separation, uncertainty, stability, alternatives, and limits. The route is available only for an explicit non-causal `QUANTITATIVE_ANALYSIS` intent; causal requests remain on the causal-identification route, and the Data report has no causal-review status of its own. Equivalent repeats are blocked. The role remains distinct from condition inquiry, causal identification, the planned data-fitness gate, and research execution. Updated checkpoints and routing to version 1.7.0, added a synthetic example, semantic/schema regressions, a hard-gate inventory entry, and user-facing documentation.
- **Why**: **Problem description**: Quantitative requests could otherwise be delegated informally, allowing an analysis provider to turn a number into an unsupported trading, causal, validation, or research-state decision, hide data gaps or leakage, mix horizons, or repeat work without new information. **Decision context**: The user requested integration of the Data analytics specialist while preserving the existing conductor, AI-Psychiatry controls, causal route, and planned prospective data-fitness work. **Protected invariants**: The conductor remains the only owner and user-facing decision-maker; Data receives only scoped inputs, cannot trade or change risk/research state, cannot claim causality, cannot delegate or create automatic follow-up, and must stop with `NOT_TESTABLE`/`BLOCKED` when coherent data are unavailable. The full fingerprint comparison remains required before acceptance. The provider is documented as an implementation option, not a new runtime or parallel architecture.
- **Verification**: `python scripts/validate_data_analysis_report.py examples/data_analysis_report.synthetic.json`; `python scripts/test_data_analysis_report.py`; `python scripts/test_schemas.py`; `python scripts/test_research_orchestration.py`; `python scripts/validate_framework.py`; `python -m json.tool schemas/data_analysis_report.schema.json`; and `git diff --check` all passed. The full framework check ran protocol smoke and unit tests only; no live market data, trade, or backtest was executed.

### 2026-09-03T13:53:41+02:00 | Integrate bounded AI-Psychiatry review and permanent conductor controls
- **Recorded author**: ChatGPT 5.6 Sol
- **Files/areas**: `agents/framework-control-reviewer.md`, `agents/research-conductor.md`, `AGENTS.md`, `README.md`, `QUICKSTART.md`, `00_RESEARCH_AGENT_README.md`, `PLANNED_FEATURES.md`, `HARD_GATE_INVENTORY.md`, `schemas/routing_decision.schema.json`, `schemas/orchestration_state.schema.json`, `schemas/framework_control_review.schema.json`, `scripts/route_research_task.py`, `scripts/validate_framework_control_review.py`, `scripts/test_framework_control_review.py`, `scripts/test_schemas.py`, `scripts/test_schemas.ps1`, `scripts/validate_framework.py`, `scripts/validate_framework.ps1`, routing and orchestration examples, and `decisions/ADR-014-framework-control-review-and-runtime-boundary.md`.
- **What**:
  - Added a provider-neutral, bounded framework-control reviewer contract that AI Psychiatry can supply when an explicit trigger or observable workflow signal warrants red-team, strategy-laundering, scope, loophole, root-cause, rule-conflict, or memory review.
  - Bound the reviewer to observable evidence, one corrective attempt, no private chain-of-thought, no backtests or claim promotion, no research-state changes, no research-goal ownership, no recursive delegation, and no commits, pushes, merges, or direct changes to `main`.
  - Made scope lock, one-level delegation, evidence-bound conclusions, changed-evidence requirements for repeated checks, and evidence-backed completion permanent controls in the conductor documentation and the version 1.6.0 routing contract. Added negative schema regressions for each relaxation.
  - Added the synthetic review example, validator, tests, hard-gate entry, roadmap status, and ADR so the optional AI-Psychiatry layer does not become a second authority and the existing scientific-philosophy and causal-identification routes remain distinct.
  - Used OpenAI Developers as an architecture review aid. Documented that the current conductor/router/contracts already supply the useful manager-led boundary; did not add an Agents SDK or MCP runtime because this repository has no runnable agent service and a second orchestration path would add untested state and failure modes.
- **Why**:
  - **Problem description**: A flexible LLM can drift in scope, delegate recursively, repeat unchanged checks, produce fluent but unsupported conclusions, or claim completion while satisfying only a schema. Optional specialist reviews alone do not reliably prevent those failures, while making every critic a permanent gate would add unnecessary cost and duplicate authority.
  - **Decision context**: The user requested AI Psychiatry first as a bounded review layer and OpenAI Developers second as a technical architecture aid. Existing `AGENTS.md`, conductor ownership, deterministic routing, fingerprinting, and specialist routes had to remain authoritative. The repository is a private decision-support tool, not a general agent platform.
  - **Protected invariants**: One conductor retains the user conversation, acceptance, and research state; material changes remain visible proposals under the full fingerprint and user-decision process; mandatory scientific and causal specialists are not replaced; no plugin or reviewer can set research goals, alter results, or change `main`; no SDK/MCP dependency or parallel state machine is introduced without a demonstrated runtime need.
- **Verification**:
  - `python scripts/validate_framework_control_review.py` passed.
  - `python scripts/test_framework_control_review.py` passed.
  - `python scripts/test_schemas.py` passed 30 positive and 99 negative cases, including all permanent-control relaxations.
  - `python scripts/test_research_orchestration.py` passed.
  - `python scripts/validate_agent_instruction_sources.py` passed.
  - `python scripts/validate_framework.py` passed all contract, orchestration, threshold, generator, and evaluation checks; the live-agent release gate was not run.
  - `git diff --check` passed. No backtest, market-data access, or research case was run. OpenAI official architecture and guardrail documentation was reviewed; no runtime migration was claimed.

### 2026-09-03T10:39:30+02:00 | Translate the repository corpus into English
- **Recorded author**: ChatGPT 5.6 Sol
- **Files/areas**: `README.md`, `QUICKSTART.md`, `00_RESEARCH_AGENT_README.md`, `01_RESEARCH_STANDARD.md`, `02_RESEARCH_CASE_TEMPLATE.md`, `03_RESEARCH_METHODS.md`, `04_CAUSAL_TOOLING.md`, `05_AGENT_OPERATIONS.md`, `HARD_GATE_INVENTORY.md`, agent contracts, ADRs 001–011 and 013, evaluation documentation and fixtures, reconstruction/generation/reference documentation, affected schemas, and related validation scripts.
- **What**:
  - Translated the explicitly authorized legacy German repository content into English across normative documents, agent-facing instructions, decision records, examples, schema descriptions, evaluation fixtures, and user-facing validation messages.
  - Kept translation-only work separate from substantive framework redesign. Corrected translation-only syntax and wording defects discovered during review, including malformed agent frontmatter, formula rendering, status labels, decimal rendering, obvious mistranslations, and stale README language.
  - Translated human-readable example values while retaining controlled machine fields, enums, identifiers, paths, schema structures, routing order, examples' decision meaning, and normative requirements.
- **Why**:
  - **Problem description**: Mixed German/English normative and agent-facing text increases semantic ambiguity and maintenance cost when Codex, Claude, Gemini, or another LLM uses the same repository.
  - **Decision context**: The owner explicitly requested the full English migration described in the roadmap. The migration therefore covers the repository corpus, while historical records, source identifiers, private filenames, and machine identifiers remain unchanged where changing them would alter provenance or references.
  - **Protected invariants**: No JSON keys, value types, list lengths, controlled enums, schema contracts, research gates, routing rules, source identities, private research data, evidence claims, or strategy results were changed. No research case, backtest, data access, or trading decision was performed.
- **Verification**:
  - `python scripts/validate_agent_instruction_sources.py` passed.
  - `python scripts/validate_framework.py` passed all contract, orchestration, entry-threshold, generator, and evaluation checks; the output explicitly states that the `LIVE_AGENT` release gate was not run.
  - `python scripts/test_schemas.py` passed 29 positive and 92 negative cases.
  - JSON structural comparison passed for 18 changed JSON files; Markdown heading/fence/table structure comparison passed for 29 changed Markdown files.
  - `git diff --check` passed. A remaining umlaut scan found only proper names in cited academic sources; no untranslated German prose remains outside historical records, source identifiers, or private paths.

### 2026-09-03T03:21:40+02:00 | ChatGPT 5.6 Sol
- **Agent**: ChatGPT 5.6 Sol
- **Files**:
  - `PLANNED_FEATURES.md` (translated)
  - `AGENT_CHANGELOG.md` (modified)
- **What**:
  - Translated the remaining German title, introductory note, and LLM stress-test
    roadmap entry in `PLANNED_FEATURES.md` into English.
  - Preserved the roadmap hierarchy, status, requirements, examples, and
    normative meaning; no priorities were reordered and no content was removed
    or added.
- **Why**:
  - **Problem description**: The shared roadmap still mixed German and English,
    despite the repository policy that new or changed repository artifacts are
    written in English.
  - **Decision context**: The user explicitly requested translation of the
    remaining German content. This is a translation-only change, kept separate
    from editorial revision so any behaviour change remains attributable.
  - **Protected invariants**: All roadmap requirements, statuses, and scope
    boundaries remain unchanged; `PLANNED_FEATURES.md` remains the single
    authoritative roadmap for every agent.
- **Verification**:
  - `python scripts/validate_agent_instruction_sources.py` passed.
  - `python scripts/validate_framework.py` passed all contract, orchestration,
    entry-threshold, generator, and eval tests.
  - `git diff --check` passed.
  - The live-agent release gate was not run; no live-agent claim is made.

### 2026-09-03T02:28:20+02:00 | ChatGPT 5.6 Sol
- **Agent**: ChatGPT 5.6 Sol
- **Files**:
  - `PLANNED_FEATURES.md` (modified)
  - `AGENT_CHANGELOG.md` (modified)
- **What**:
  - Triaged an external red-team audit and a separate architecture review
    against the current repository instead of adopting their severity labels or
    refactoring plan wholesale.
  - Added a confirmed regression target for the repeated-random-walk loophole,
    in which multiple required `RANDOM_WALK` controls can evade the current
    exact-list comparison while still providing no structure-appropriate null
    family.
  - Planned structured Monte Carlo, replication, uncertainty, and seed evidence
    and required pipeline-control results to be bound to execution of the exact
    frozen candidate pipeline rather than accepted as agent-written `PASS`
    declarations.
  - Defined the narrow conditional scope of a future fail-closed conductor:
    artifact dereferencing, actual validator and specialist invocation,
    persistent attempt counting, preservation of non-zero fingerprint stops,
    and predecessor-derived fingerprint baselines in a private append-only or
    content-addressed history.
  - Expanded the adversarial evaluation plan with baseline substitution,
    causal-claim relabelling, phantom sentinel passes, repeated random walks,
    competing validation protocols, ignored fingerprint failures, attempt
    resets, and unbound producer-configuration hashes.
  - Recorded a lower-priority cross-schema identifier-consistency check while
    making shared external schema definitions optional and fail-closed rather
    than treating reduced line count as the objective.
  - Explicitly declined audit recommendations that would weaken change-control
    exit semantics, contaminate pre-freeze controls with validation data,
    collapse distinct epistemic artifacts or specialist roles, split the shared
    roadmap, remove the Windows validation path, or add developer tooling
    without a protected research decision.
- **Why**:
  - **Problem description**: The reviews contained a mixture of genuine bypasses,
    already-recorded gaps, incorrect repository counts, irreproducible revision
    claims, and conventional software-cleanup advice. Copying the full plans
    would give questionable external severity labels authority over the shared
    roadmap and could erase deliberate scientific boundaries.
  - **Decision context**: Both reviews identify revision `4af9cff` while citing
    later material, and their schema, agent, script, mechanism, and generator
    counts do not match that revision or current `main`. Direct code inspection
    nevertheless confirmed the repeated-random-walk defect and the free-text
    Monte Carlo record. The existing roadmap already covered validation
    protocols, caller-enforced gates, the real Research Case, live-agent
    evaluation, search lineage, rule loading, terminology, and conditional
    language migration.
  - **Rationale & protected invariants**: Preserve one authoritative roadmap;
    retain fail-closed fingerprint semantics; keep precommitment separate from
    result assessment and predictive claims separate from causal claims; add
    only controls that make false pipeline, drift, or agent-reliability claims
    harder; and keep proprietary research out of the public repository.
- **Verification**:
  - `python scripts/validate_agent_instruction_sources.py` — PASS.
  - `python scripts/validate_framework.py` — PASS; full deterministic framework
    integrity passed. The `LIVE_AGENT` release gate was not run, so no model or
    prompt reliability claim is made.
  - `git diff --check` — PASS.

### 2026-09-03T01:02:16+02:00 | OpenAI Codex (GPT-5)
- **Agent**: OpenAI Codex (GPT-5)
- **Files**:
  - `README.md` (modified)
  - `QUICKSTART.md` (modified)
  - `AGENT_CHANGELOG.md` (modified)
  - GitHub repository name, description, and local `origin` URL (repository metadata)
- **What**:
  - Renamed the visible project from **Research Framework** to **Trading Research Framework**.
  - Renamed the GitHub repository from `research_framework` to `trading-research-framework`, updated its public description, and changed the local Git remote to the new canonical URL.
  - Updated the raw Quickstart link to the new repository path.
  - Deliberately retained existing `urn:research-framework:*` schema identifiers, generic lower-case descriptions, historical architecture records, and the local workspace directory name.
- **Why**:
  - **Problem description**: The generic project name did not tell an outside reader that the framework is specifically intended to govern trading research, while a repository-wide textual replacement would alter stable identifiers and historical evidence for no decision-protecting benefit.
  - **Decision context**: Inspection found only two visible document titles and one canonical raw link that required file changes. Twenty schema files use `research-framework` as a stable machine identity and therefore were excluded from the rename.
  - **Rationale & protected invariants**: Make the project's purpose immediately clear without breaking schema identity, changing normative meaning, rewriting history, or disturbing the Codex workspace path.
- **Verification**:
  - `python scripts/validate_agent_instruction_sources.py` — PASS.
  - `python scripts/validate_framework.py` — PASS; full framework integrity passed, with the existing notice that no `LIVE_AGENT` release gate was requested.
  - `git diff --check` — PASS.
  - GitHub repository lookup and `git ls-remote origin` resolve the new canonical repository URL.

### 2026-09-03T00:55:35+02:00 | OpenAI Codex (GPT-5)
- **Agent**: OpenAI Codex (GPT-5)
- **Files**:
  - `AGENT_CHANGELOG.md` (modified)
  - Git branch references (repository maintenance; no framework files removed)
- **What**:
  - Removed five stale remote branches whose changes had already been merged through pull requests: prose strategy reconstruction, research-question drift control, causal-axis provenance, entry-threshold controls, and the mechanism-first generator.
  - Removed seven corresponding or already-merged local branches, including the concept-audit, research-conductor, and scientific-philosophy working branches whose remotes had previously been deleted.
  - Retained `codex/framework-maintenance-checkpoint-plan` and `feature/data-snapshot-contract` as explicit temporary archives because each contains unmerged material that may still justify a small, newly designed future change.
  - Kept `main` and all merged pull-request history unchanged; no stale branch was merged wholesale.
- **Why**:
  - **Problem description**: Old working branches made it appear that several completed framework features were still separate or missing, while two genuinely unmerged experiments were indistinguishable from the already-integrated branches.
  - **Decision context**: Patch-equivalence checks and merged pull-request records showed that the deleted work was already represented in `main`. The two retained archives were deliberately excluded because one holds planning ideas not yet reconciled with the central roadmap and the other holds a closed data-snapshot proposal that conflicts with newer architecture but contains a potentially useful provider-neutral reproducibility concept.
  - **Rationale & protected invariants**: Keep `main` as the only current implementation, reduce cross-agent branch confusion, preserve all merged history, and avoid either losing uncertain unmerged ideas or importing obsolete code and policy into the current framework.
- **Verification**:
  - Remote branch listing contains only `main` and the two named archives, plus the temporary task branch until this pull request is merged.
  - Local branch listing contains only `main`, the retained maintenance archive, and the temporary task branch.
  - `python scripts/validate_agent_instruction_sources.py` — PASS.
  - `python scripts/validate_framework.py` — PASS; full framework integrity passed, with the existing notice that no `LIVE_AGENT` release gate was requested.
  - `git diff --check` — PASS.

### 2026-09-03T00:42:48+02:00 | OpenAI Codex (GPT-5)
- **Agent**: OpenAI Codex (GPT-5)
- **Files**:
  - `AGENT_CHANGELOG.md` (modified)
- **What**:
  - Backfilled twelve decision-changing milestones that predated the creation of the collaboration changelog.
  - Reconstructed factual provenance from 29 substantive commits and their architecture decisions, then used the recorded owner conversation only to explain the practical problems and decisions behind those changes.
  - Grouped related work into milestones, omitted routine fixes and merge-only commits, and explicitly marked unavailable historical model versions and verification commands instead of inventing them.
  - Kept private strategy details, data, and empirical results out of the public repository.
- **Why**:
  - **Problem description**: The changelog began after much of the framework's epistemic and operational architecture had already been built. Later agents could see the current rules but not the main failure modes and owner decisions that caused those rules to exist.
  - **Rationale & protected invariants**: A concise, evidence-bound history helps future agents distinguish intentional safeguards from accidental complexity without turning the changelog into duplicate documentation. Git remains the source for what changed; conversational context explains why; uncertainty about historical attribution remains visible.
- **Verification**:
  - `python scripts/validate_agent_instruction_sources.py` — PASS.
  - `python scripts/validate_framework.py` — PASS; full framework integrity passed, with the existing notice that no `LIVE_AGENT` release gate was requested.
  - `git diff --check` — PASS.

### 2026-09-03T00:32:07+02:00 | OpenAI Codex (GPT-5)
- **Agent**: OpenAI Codex (GPT-5)
- **Files**:
  - `AGENTS.md` (modified)
  - `AGENT_CHANGELOG.md` (modified)
  - `PLANNED_FEATURES.md` (modified)
  - `scripts/validate_agent_instruction_sources.py` (modified)
- **What**:
  - Made `PLANNED_FEATURES.md` the single shared roadmap and authoritative implementation priority for Codex, Claude, Gemini, and other agents, while preserving the distinction between planning and user authorization.
  - Added an urgent first-priority roadmap item covering the incomplete enforcement of validation boundaries, stopping rules, and peeking controls.
  - Recorded the required fixes in dependency order: one mandatory canonical protocol, machine-checkable boundaries, a separate execution record, automatic plan-versus-execution comparison, complete interim-inspection rules, schema migration, and adversarial negative tests.
  - Renumbered the remaining authoritative priorities and updated their cross-references without changing their substantive scope.
  - Extended instruction-source validation so CI fails if `AGENTS.md` or `PLANNED_FEATURES.md` loses the shared-roadmap declaration.
- **Why**:
  - **Problem description**: Different LLMs could maintain separate feature priorities even after receiving one common rule source. In addition, the new stopping-rule contract remained optional, allowed two competing protocol fields, stored boundaries as free text, and recorded declared intent without proving the executed test followed it.
  - **Rationale & protected invariants**: A single shared roadmap prevents silent priority drift between agents. Giving the known false-hard-gate problem first priority protects validation and capital decisions from optional stopping, endpoint selection, hidden peeking, and a compliant-looking artifact that does not match the executed test.
- **Verification**:
  - `python scripts/validate_agent_instruction_sources.py` — PASS.
  - `python scripts/validate_framework.py` — PASS; full framework integrity passed, with the existing notice that no `LIVE_AGENT` release gate was requested.
  - `git diff --check` — PASS.

### 2026-09-03T00:18:42+02:00 | OpenAI Codex (GPT-5)
- **Agent**: OpenAI Codex (GPT-5)
- **Files**:
  - `AGENTS.md` (modified)
  - `AGENT_CHANGELOG.md` (modified)
  - `CLAUDE.md` (modified)
  - `GEMINI.md` (modified)
  - `scripts/validate_agent_instruction_sources.py` (created)
  - `scripts/validate_framework.py` (modified)
- **What**:
  - Declared `AGENTS.md` as the sole authoritative repository instruction source for every AI agent.
  - Replaced the duplicated Claude and Gemini rule sets with identical minimal bootstraps that require the complete canonical instructions and recent collaboration history to be read before work begins.
  - Removed duplicated policy from the changelog preamble so the changelog remains a historical record rather than a competing source of rules.
  - Added a fail-closed validation that rejects changed or expanded host bootstraps, a normative changelog preamble, or loss of the canonical-source declaration, and included it in the full framework validation.
- **Why**:
  - **Problem description**: Codex, Claude, and Gemini received materially equivalent rules through three independently maintained files, while the changelog repeated a fourth subset. Future edits could therefore create silent policy drift, contradictory instructions, and unnecessary context cost.
  - **Rationale & protected invariants**: One canonical policy makes every agent receive the same research and collaboration safeguards. Minimal host bootstraps preserve automatic discovery by different tools without permitting agent-specific reinterpretation. The new validation makes renewed duplication visible and blocks it from passing framework checks.
- **Verification**:
  - `python scripts/validate_agent_instruction_sources.py` — PASS.
  - `python scripts/validate_framework.py` — PASS; full framework integrity passed, with the existing notice that no `LIVE_AGENT` release gate was requested.

### 2026-09-03T00:01:00+02:00 | Gemini 3.8 Flash
- **Agent**: Gemini 3.8 Flash (High)
- **Files**:
  - `06_OUTCOME_EVIDENCE_CONTRACT.md` (modified)
  - `schemas/outcome_evidence_contract.schema.json` (modified)
  - `scripts/validate_outcome_evidence_contract.py` (modified)
  - `scripts/test_outcome_evidence_contract.py` (modified)
  - `AGENT_CHANGELOG.md` (modified)
- **What**:
  - Extended validation stopping, sample boundary, and peeking rules in `06_OUTCOME_EVIDENCE_CONTRACT.md` to explicitly govern historical static holdout backtests alongside prospective forward tests.
  - Added `validation_protocol` property and `validationProtocol` definition in `schemas/outcome_evidence_contract.schema.json`, maintaining backwards compatibility with `forward_testing_protocol`.
  - Updated validator `scripts/validate_outcome_evidence_contract.py` and regression tests `scripts/test_outcome_evidence_contract.py` to enforce no early termination for both static holdouts and forward protocols under `NO_INTERIM_STOPPING`.
- **Why**:
  - **Problem description**: While forward tests risk optional stopping (terminating early at interim profit peaks), historical backtests are exposed to the symmetrical distortion of selective sample truncation, endpoint cherry-picking (clipping dates to avoid adverse drawdown periods), and repeated holdout peeking.
  - **Rationale & protected invariants**: Mandating full window evaluation without selective truncation for backtests protects the integrity of holdout evidence and ensures backtest boundaries cannot be cherry-picked post-hoc.
- **Verification**: `pwsh scripts/validate_framework.ps1 -PythonExecutable .venv\Scripts\python.exe` (all schema contracts, outcome evidence tests, and regression harnesses PASS).

### 2026-09-02T23:58:00+02:00 | Gemini 3.8 Flash
- **Agent**: Gemini 3.8 Flash (High)
- **Files**:
  - `06_OUTCOME_EVIDENCE_CONTRACT.md` (modified)
  - `schemas/outcome_evidence_contract.schema.json` (modified)
  - `scripts/validate_outcome_evidence_contract.py` (modified)
  - `scripts/test_outcome_evidence_contract.py` (modified)
  - `PLANNED_FEATURES.md` (modified)
  - `AGENT_CHANGELOG.md` (modified)
- **What**:
  - Added forward validation stopping rules and peeking prohibition to `06_OUTCOME_EVIDENCE_CONTRACT.md` and schema `schemas/outcome_evidence_contract.schema.json`.
  - Added semantic validator check in `scripts/validate_outcome_evidence_contract.py` preventing early termination when peeking policy is `NO_INTERIM_STOPPING`, along with regression tests in `scripts/test_outcome_evidence_contract.py`.
  - Updated `PLANNED_FEATURES.md` Priority 4 to require execution trajectory and tool-invocation auditing (verifying that the router, specialists, and fingerprint checks were genuinely called), and noted IAAFT / phase-randomized surrogate methods as catalog options.
- **Why**:
  - **Problem description**: Without explicit stopping horizons and strict peeking prohibitions, prospective / forward validation tests can be compromised by optional stopping (terminating early when performance crosses an attractive threshold, or peeking repeatedly without alpha correction). In addition, agent evaluations that only score final artifacts allow models to fake compliance while bypassing mandatory orchestration steps, specialists, or error states.
  - **Rationale & protected invariants**: Predeclared stopping horizons protect against p-hacking and selective termination in forward OOS tests. Trajectory auditing ensures agents cannot take unauthorized shortcuts or simulate specialist handoffs.
- **Verification**: `pwsh scripts/validate_framework.ps1 -PythonExecutable .venv\Scripts\python.exe` (all schema contracts, outcome evidence tests, and regression harnesses PASS).

### 2026-09-02T23:47:00+02:00 | Gemini 3.8 Flash
- **Agent**: Gemini 3.8 Flash (High)
- **Files**:
  - `AGENT_CHANGELOG.md` (modified)
  - `AGENTS.md` (modified)
  - `CLAUDE.md` (modified)
  - `GEMINI.md` (modified)
- **What**:
  - Adopted industry best practices for multi-LLM collaboration into repository guidelines.
  - Mandated that every agent starting work—and specifically any newly joining LLM—must create its own dedicated feature branch (`<agent>/<topic>`) rather than committing directly to `main`.
  - Formalized pre-flight worktree and remote sync, read-before-write checks, non-destructive Git rules (banning blind resets/cleans), and exact Git author attribution.
- **Why**:
  - **Problem description**: Parallel or sequential LLMs modifying a shared repository risk race conditions, branch collision, overwriting each other's uncommitted work, and obscuring commit provenance when operating on a single shared branch.
  - **Rationale & protected invariants**: Branch isolation ensures clean sandboxing and requires passing CI status checks before merging. Read-before-write and non-destructive rules protect collaborator progress and maintain the decision integrity of the framework.
- **Verification**: Framework validation suite (`scripts/validate_framework.ps1`) executed; all contracts passed.

### 2026-09-02T23:41:00+02:00 | Gemini 3.8 Flash
- **Agent**: Gemini 3.8 Flash (High)
- **Files**:
  - `AGENT_CHANGELOG.md` (modified)
  - `AGENTS.md` (modified)
  - `CLAUDE.md` (modified)
  - `GEMINI.md` (modified)
- **What**:
  - Mandated that the WHY section in all changelog entries and agent instructions must explicitly include a dedicated problem description.
  - Updated rule definitions in `AGENT_CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
  - Refined all prior changelog entries to clearly separate problem description from rationale and protected invariants.
- **Why**:
  - **Problem description**: Rationale alone can become abstract or generic without a concrete problem statement, making it hard for future agents to determine what specific vulnerability, ambiguity, or failure mode motivated the change.
  - **Rationale & protected invariants**: Explicitly documenting the problem alongside the rationale and protected invariants provides complete epistemic context for cross-agent collaboration, preventing regressions and unnecessary rewrites.
- **Verification**: Framework validation suite (`scripts/validate_framework.ps1`) executed; all contracts passed.

### 2026-09-02T23:38:00+02:00 | Gemini 3.8 Flash
- **Agent**: Gemini 3.8 Flash (High)
- **Files**:
  - `AGENT_CHANGELOG.md` (modified)
  - `AGENTS.md` (modified)
  - `CLAUDE.md` (modified)
  - `GEMINI.md` (modified)
- **What**:
  - Mandated that all changelog entries must strictly be written in English.
  - Required all agents to provide comprehensive, detailed breakdowns for both WHAT was changed and WHY it was changed.
  - Updated repository instructions (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) to reflect the English and What/Why requirement.
- **Why**:
  - **Problem description**: Unstructured or brief summaries in non-English or fragmented styles make cross-model collaboration difficult to audit and lead to misunderstandings between different agent families.
  - **Rationale & protected invariants**: Mandating English and detailed WHAT/WHY breakdowns ensures operational transparency, protects research invariants, and prevents subsequent agents from misinterpreting past decisions.
- **Verification**: Framework validation suite (`scripts/validate_framework.ps1`) executed; all contracts passed.

### 2026-09-02T23:35:00+02:00 | Gemini 3.8 Flash
- **Agent**: Gemini 3.8 Flash (High)
- **Files**:
  - `AGENT_CHANGELOG.md` (modified)
  - `AGENTS.md` (modified)
  - `CLAUDE.md` (modified)
  - `GEMINI.md` (modified)
- **What**:
  - Mandated explicit agent model name and version number along with date and time for every change across all agent guidelines.
- **Why**:
  - **Problem description**: Generic agent names (e.g. "Gemini" or "ChatGPT") omit model generation and version details, making it impossible to correlate changes or mistakes with specific model capabilities.
  - **Rationale & protected invariants**: Mandating full model names and version numbers provides exact provenance for behavioral audits and cross-agent traceability.
- **Verification**: Framework validation suite (`scripts/validate_framework.ps1`) executed; all contracts passed.

### 2026-09-02T23:28:00+02:00 | Gemini 3.8 Flash
- **Agent**: Gemini 3.8 Flash (High)
- **Files**:
  - `AGENTS.md` (modified)
  - `CLAUDE.md` (modified)
  - `GEMINI.md` (created)
  - `AGENT_CHANGELOG.md` (created)
- **What**:
  - Registered Gemini alongside Codex and Claude as authorized collaborators in `AGENTS.md` and `CLAUDE.md`.
  - Added dedicated `GEMINI.md` rule and memory entry point.
  - Established `AGENT_CHANGELOG.md` as mandatory cross-agent activity log and added its update rule to agent instructions.
- **Why**:
  - **Problem description**: Gemini was participating in the workspace without being explicitly registered as an authorized collaborator or having its dedicated entrypoint, risking concurrent edit collisions with Codex and Claude.
  - **Rationale & protected invariants**: Explicitly registered Gemini across all instruction files and established `AGENT_CHANGELOG.md` to guarantee mutual awareness and safe concurrent work.
- **Verification**: Full framework validation suite (`scripts/validate_framework.ps1`) executed via Python virtual environment; all schema and integrity contracts passed.

## Backfilled milestones from before this log existed

The entries below were reconstructed on 2026-09-03 from immutable Git history,
the corresponding architecture decisions, and the research owner's recorded
decision context. They summarize decision-changing milestones rather than every
commit. Commit timestamps and authors are taken from Git. Exact LLM model
versions and historical verification commands were not recorded and are not
inferred. Present-day validation cannot prove which checks were run at the time.

### 2026-09-02T19:47:34+02:00 | Historical milestone: Protect data feasibility and measure agent reliability
- **Recorded authors**: Codex; exact historical LLM model/version was not recorded.
- **Evidence**: `26de20d`, `713ebbc`, `82d75ce`.
- **Files/areas**: data-fitness assessment, manual-verification policy, live-agent evaluation roadmap, repository instructions.
- **What**:
  - Added a prospective check that asks whether the available data can test the intended strategy before operationalization or validation proceeds.
  - Made repeated chart scrolling, piecemeal downloads, and arbitrary screenshot quotas unacceptable as normal research prerequisites.
  - Planned repeated live-agent evaluations that measure uncertainty and whether agents actually stop, reject, or escalate when required.
- **Why**:
  - **Problem description**: A strategy can look testable until limited history, resolution, or export access becomes a late bottleneck. Transferring that problem to the owner through repetitive manual work creates fragile evidence and an unreasonable burden. Schema-valid outputs also do not show that agents reliably obey the gates.
  - **Rationale & protected invariants**: Establish data sufficiency before expensive work, prefer complete reusable exports and automated checks, keep residual manual checks risk-based and minimal, and measure agent behaviour rather than assuming compliant prose is enough.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-09-02T18:58:54+02:00 | Historical milestone: Re-scope the framework and inventory real gate strength
- **Recorded authors**: RealMonoid and Codex; exact historical LLM model/version was not recorded.
- **Evidence**: `dd5a229`, `4af9cff`, `d668e91`.
- **Files/areas**: `PLANNED_FEATURES.md`, `AGENTS.md`, hard-gate inventory and validation.
- **What**:
  - Reordered planned work by its ability to prevent false confidence in a trading edge and made the roadmap central for all participating agents.
  - Defined the repository as private decision support for one owner, not an academic publication or contributor-onboarding system.
  - Classified important safeguards by how they are enforced: executable hard gate, schema constraint, agent judgment, or prose-only rule.
- **Why**:
  - **Problem description**: Governance can grow into costly ceremony that serves a hypothetical audience while the protections that actually govern capital decisions remain weaker than their wording suggests.
  - **Rationale & protected invariants**: Keep controls that protect a research or capital decision; avoid audience-only work; preserve uncertain safeguards until evidence supports removal; and make the remaining dependence on agent judgment visible before claiming a gate is hard.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-09-01T23:29:50+02:00 | Historical milestone: Test the pipeline before trusting market results
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `0f53d51` and ADR-015.
- **Files/areas**: pipeline-integrity schema, validator, fixtures, router, instructions and evaluation cases.
- **What**:
  - Required structure-appropriate negative controls, repeated runs, a known-effect sentinel, and a fingerprint binding before validation can be frozen.
  - Made the path fail closed when the pipeline-integrity assessment does not pass.
  - Explicitly separated successful synthetic controls from evidence for a market claim or trading edge.
- **Why**:
  - **Problem description**: A valid-looking result can be manufactured by leakage, a broken implementation, a favourable random path, or a model pipeline that does not preserve the relevant market structure.
  - **Rationale & protected invariants**: Demonstrate that the exact pipeline rejects effects where none should exist and detects a known effect where one should exist, without treating that diagnostic success as evidence that the strategy itself works.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-09-01T20:42:31+02:00 | Historical milestone: Give every outcome a fixed evidential job
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `15e1bf5` and ADR-014.
- **Files/areas**: outcome-evidence contract schema, validator, router, templates and evaluation cases.
- **What**:
  - Required each outcome to have a precommitted role, evidence target, decision consequence, multiplicity family, and mechanical-coupling assessment.
  - Separated predictive support from mechanism support so that a successful prediction cannot silently rescue a failed mechanism claim.
  - Required stability to be recorded independently for each material target before validation is frozen.
- **Why**:
  - **Problem description**: A strategy can use several outcomes interchangeably after seeing results, or allow an outcome built from the same mathematical components as the trigger to appear informative when the relationship is partly mechanical.
  - **Rationale & protected invariants**: Decide in advance what each result is allowed to support, count related searches together, and prevent correlation, construction dependence, predictive success, and causal mechanism from being conflated.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-09-01T03:11:19+02:00 | Historical milestone: Set language and future context-delivery safeguards
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `287bae0`, `63eb3cb`, `0bf948c`, `f6eee27`, `6967f3d`.
- **Files/areas**: repository language policy, `README.md`, `PLANNED_FEATURES.md`, proposed selective-loading and concept-registry controls.
- **What**:
  - Required all new repository changes to be written in English while deferring legacy translation to a separate, evidence-justified migration.
  - Rewrote the README order so outsiders first see which research problems the framework solves, then how it works, and only then technical details.
  - Recorded, but did not silently implement, safer section-level loading and a canonical concept registry as future work with fail-closed requirements.
- **Why**:
  - **Problem description**: Mixed terminology can disconnect prose rules from English machine fields, while loading the entire normative corpus is costly. Careless selective loading, however, can omit a rule invisibly; combining translation with editing makes behavioural changes impossible to attribute.
  - **Rationale & protected invariants**: Keep future changes linguistically consistent, explain the tool to a non-developer owner, separate translation from semantic revision, and treat section identity and terminology as correctness controls before using selective loading as a cost optimization.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-09-01T02:03:55+02:00 | Historical milestone: Replace narrow handoff checks with the complete research fingerprint
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `3fc41d6`, `2e69c6b`, `c041d68` and ADRs 011-013.
- **Files/areas**: research conductor, executable router, orchestration state, research fingerprint, change proposal, validators and evaluations.
- **What**:
  - Added one top-level conductor that retains the user conversation, asks the router for the next permitted step, and invokes mandatory specialists.
  - Introduced pre- and post-handoff drift checks, then expanded them from six headline fields to the complete effective research state.
  - Required every material difference to become a visible `CHANGE_PROPOSED` artifact instead of silently overwriting the frozen version.
- **Why**:
  - **Problem description**: Specialist agents could be forgotten, handoffs could fragment responsibility, and language models could openly or subtly reformulate a failed hypothesis by changing definitions, parameters, filters, data, or execution assumptions.
  - **Rationale & protected invariants**: Let deterministic routing decide when expertise is mandatory, keep one agent accountable to the owner, compare the whole material research state, and require explicit authorization for a new Research-ID or version.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-08-31T18:48:08+02:00 | Historical milestone: Gate causal language on identification, not association
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `53d1597` and ADR-012.
- **Files/areas**: causal-identification critic, identification assessment schema, router, instructions and evaluation cases.
- **What**:
  - Required a specialist identification review for interventional or counterfactual conclusions.
  - Kept ordinary predictive strategy questions outside that mandatory causal path.
  - Prevented temporal order, event studies, causal discovery, or estimator choice from substituting for an identification argument.
- **Why**:
  - **Problem description**: Noisy observational finance data can support stable associations without identifying what an intervention would do. Mathematical dependence and correlation alone do not establish a causal mechanism.
  - **Rationale & protected invariants**: Match the strength of causal wording to an explicit identification design, while allowing useful predictive research to proceed under an honestly limited claim instead of demanding impossible causal certainty.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-08-31T17:02:05+02:00 | Historical milestone: Expose hidden and unknown strategy conditions before operationalization
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `73c0fc0` and ADR-010.
- **Files/areas**: concept audit, condition inquiry, schemas, templates, router and evaluations.
- **What**:
  - Distinguished strategy-defining conditions, source-stated application conditions, suspected modifiers, and genuinely unknown conditions.
  - Required provisional constructs such as market regimes to be treated as measurement claims that may need their own validation.
  - Required competing explanations and checks for trigger-outcome construction dependence before operationalization can make an idea look more definite than its source.
- **Why**:
  - **Problem description**: A strategy may only work under conditions that neither the source nor the researcher knows. An invented label such as a regime, an intentional story such as a failed breakout, or a trigger and target derived from the same window can quietly determine the result.
  - **Rationale & protected invariants**: Surface what is known, suspected, imposed, or unknown before choosing formulas; do not turn a filter into a market fact; and do not mistake shared construction for evidence about market behaviour or cause.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-08-31T16:10:34+02:00 | Historical milestone: Reconstruct prose strategies without authorizing a backtest
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `adb3598`, `97164a3` and ADR-008.
- **Files/areas**: prose reconstruction rules, reconstruction schema, agent instructions and user-communication policy.
- **What**:
  - Added a source-faithful reconstruction layer for strategies described in books or other prose before any operational definition is selected.
  - Required source statements, researcher additions, unresolved choices, and resulting uncertainty to remain visibly separate.
  - Required user-facing explanations to lead with research consequences in ordinary language and made clear that operationalization is not permission to backtest.
- **Why**:
  - **Problem description**: Book strategies often omit enough detail that coding them requires invention. Technical implementation commentary also obscured decisions for an owner who uses software only as a means to research.
  - **Rationale & protected invariants**: Preserve what the source actually claims, make every added definition an explicit decision, stop when the idea remains indeterminate, and communicate choices without assuming a software developer is present.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-08-31T04:01:54+02:00 | Historical milestone: Add Duhem-Quine and Lakatos controls to failed research
- **Recorded author**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `ce5e675` and ADR-009.
- **Files/areas**: scientific-philosophy continuation critic, continuation schema, instructions, templates and evaluations.
- **What**:
  - Recorded that a failed test rejects a bundle of hypothesis, operationalization, measurement, data, and auxiliary assumptions rather than logically identifying one guilty component.
  - Preserved the frozen result while allowing a separate continuation only when it states a new, risky prediction in advance.
  - Distinguished progressive continuation from retrospective rescue and retained an undecidable or imprecise result state.
- **Why**:
  - **Problem description**: Strict falsification can overstate which part of a research bundle failed, but unrestricted reinterpretation after failure lets the hypothesis move wherever the data look favourable.
  - **Rationale & protected invariants**: Do not pretend the framework can isolate every auxiliary failure; do prevent convenient post-result repair. Any continued programme must risk being wrong in a new Research-ID or version and must not rewrite the old outcome.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-08-31T02:34:50+02:00 | Historical milestone: Generate mechanism-led ideas without hiding the search
- **Recorded authors**: RealMonoid; exact historical LLM model/version was not recorded.
- **Evidence**: `333af69`, `4085fbb`, `8c208eb` and ADRs 005-007.
- **Files/areas**: causal claim axes, variable-selection provenance, mechanism catalogue, hypothesis generator, noise screens and search-space accounting.
- **What**:
  - Separated descriptive, predictive, interventional, and counterfactual claim levels from trading readiness.
  - Added a literature-anchored, mechanism-first generator for candidate ideas and recorded whether variables were theory-selected or data-selected.
  - Froze the generated family and added cheap entry screens so discarded and promoted candidates remain part of the counted search.
- **Why**:
  - **Problem description**: The framework could assess an existing idea but not responsibly generate one. Automated generation can also create a large hidden multiple-testing problem, especially when data-driven variables or appealing market stories are presented as theory.
  - **Rationale & protected invariants**: Generate candidates from named mechanisms without claiming they are true, preserve causal-claim honesty, record the full opportunity set, and prevent screening from erasing unsuccessful trials.
- **Historical verification**: Not recorded in the surviving evidence.

### 2026-08-30T23:59:28+02:00 | Historical milestone: Establish the executable research-governance foundation
- **Recorded author**: Codex; exact historical LLM model/version was not recorded.
- **Evidence**: `b08a285`, `d8d0f41`, `da6cc7f`, `571e4c5` and ADRs 001-004.
- **Files/areas**: normative research documents, schemas, examples, validators, evidence ledger, method router, tiered intake, quickstart and continuous integration.
- **What**:
  - Created the initial artifact-first governance layer with provenance, evidence chains, validation states, decision records, and regression fixtures.
  - Added academic-source identity and integrity controls so versions, corrections, and replications are not treated as independent evidence.
  - Added a tiered hypothesis intake and executable router that classifies a raw idea before data access or backtesting.
  - Turned core contracts into automated validation and CI rather than relying only on agents reading prose.
- **Why**:
  - **Problem description**: A method guide alone could not show which evidence supported which decision, prevent premature promotion of an observed pattern, or coordinate multiple agents without losing provenance.
  - **Rationale & protected invariants**: Make the research state inspectable and machine-checkable, separate idea intake from empirical testing, preserve negative and corrected evidence, and fail early when required artifacts or contracts are missing.
- **Historical verification**: Not recorded in the surviving evidence.
