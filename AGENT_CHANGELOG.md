# Agent Collaboration Changelog

This log is the central record of work performed by AI agents (Codex, Claude, Gemini, etc.) in this repository.

## Rule for all AI agents

All entries in this log **must be written in English**. Whenever you perform work, update code, or modify documentation in this repository:
1. **Branch isolation**: When starting any new task, or when a new LLM joins the project, create and work in a dedicated feature branch (e.g. `<agent>/<feature-name>`). Never commit or push directly to `main`. All changes must merge into `main` exclusively through Pull Requests that pass all automated status checks.
2. **Read this log and worktree first**: Inspect `AGENT_CHANGELOG.md` and check `git fetch` / `git status` before starting to see what other agents have recently changed. Re-read target files immediately before applying edits.
3. **Non-destructive safeguard**: Never execute destructive git commands (`git reset --hard`, `git clean -f`) or overwrite unfamiliar uncommitted work from another agent.
4. **Git attribution**: Configure your Git committer identity to match your exact agent model name and version (e.g. `user.name = "Gemini 3.8 Flash"`, `user.email = "<agent>@local"`).
5. **Append an entry** to this log in English upon completing your changes, including:
   - **Timestamp**: Exact date and time with timezone offset in ISO 8601 format (e.g. `2026-09-02T23:47:00+02:00`).
   - **Agent**: Full agent model name and version number (e.g. `Gemini 3.8 Flash`, `ChatGPT 5.6 Sol`, `Claude 3.7 Sonnet`).
   - **Files**: List of files modified, created, or deleted.
   - **What**: Detailed explanation of concrete modifications made to code, schemas, documentation, or configuration.
   - **Why**: Detailed explanation that MUST explicitly include:
     - **Problem description**: The exact problem, gap, risk, ambiguity, or failure mode observed.
     - **Rationale & protected invariants**: Why this solution was chosen, how it resolves the problem, and which decisions or safeguards are protected.
   - **Verification**: Exact test suites or verification commands executed, including status (PASS/FAIL).

---

## Log entries

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
