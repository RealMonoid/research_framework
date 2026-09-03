# ADR-001: Separate, artifact-based operations layer for the research agent

**Status:** Accepted  
**Date:** 2026-08-30  
**Deciders:** Research owner and research-framework maintainer

## Context

The documents **00_RESEARCH_AGENT_README.md** through
**04_CAUSAL_TOOLING.md** already form an extensive methodological core for
trading research. They cover data roles, feasibility, claim level,
identification, leakage, statistical inference, freeze, validation, tooling,
and research end states.

However, operating an actual LLM agent also requires independent,
machine-testable controls for:

- the provenance of an individual agent run;
- separation of source fact, calculation, estimate, inference, forecast, and
  human judgement;
- a claim-level evidence chain;
- source and citation checks;
- deterministic evidence grades;
- traces, costs, retries, and errors;
- human corrections and overrides;
- delta detection and a forecast ledger;
- LLM evaluations and a controlled improvement loop; and
- safe use of multiple agents.

Putting these fields directly into **02_RESEARCH_CASE_TEMPLATE.md** would mix
the already large case artifact with runtime telemetry. A specific database or
orchestration platform has not yet been selected and should not be assumed.

Constraints:

- The methodological core of 00–04 must not be duplicated or weakened
  semantically.
- The operations layer must work as files and JSON artifacts before a runtime
  platform exists.
- All decision-bearing relationships must be auditable, versioned, and
  immutable.
- Confidence must not come from free-form LLM self-assessment.
- A multi-agent system must not be released until a single agent has been
  verified.

## Decision

We introduce a separate, artifact-first operations layer.

1. **05_AGENT_OPERATIONS.md** becomes the normative standard for run
   provenance, epistemic claim types, evidence chains, source verification,
   evidence grades, observability, errors, human review, deltas, forecasts,
   evaluations, and multi-agent gates.
2. **schemas/run_manifest.schema.json**, **schemas/evidence.schema.json**,
   **schemas/forecast.schema.json**, and **schemas/review.schema.json** define
   the machine-testable core artifacts. Each schema version has a stable ID;
   changes are versioned.
3. **examples/** contains minimum valid examples. Examples are not substantive
   release approval.
4. **evals/** contains a versioned catalogue, an explicit baseline, a
   deterministic runner, and tests for LLM/agent regressions.
5. Run, evidence, and review artifacts are append-only or revision-based. A
   change creates a new object with an explicit predecessor relationship;
   released originals are never overwritten.
6. The epistemic classes **SOURCE_FACT**, **CALCULATED_VALUE**, **ESTIMATE**,
   **INFERENCE**, **FORECAST**, and **HUMAN_JUDGMENT** are orthogonal to the
   research claim level in **01 §5**.
7. The only operational confidence class is the deterministically derived
   evidence grade **SUFFICIENT**, **LIMITED**, or **INSUFFICIENT**. It does not
   replace methodological validation.
8. Human overrides form a separate review layer. They must not relabel
   evidence or methodological gate results.
9. A single agent remains the default. Multi-agent execution requires separate
   child runs, unambiguous artifact ownership, conflict resolution, and a
   passed multi-agent gate.
10. The layer remains runtime-neutral. File-based artifacts may later be
    mirrored to a database or observability platform as long as IDs, hashes,
    lineage, and immutability are preserved.

The normative boundary is:

**00–04 decide what is methodologically permissible; 05 and the operational
artifacts show how an agent reached its result and whether that result may be
released.**

## Options considered

### Option A: Integrate all operational fields into the research-case template

| Dimension | Assessment |
|---|---|
| Complexity | Medium for the initial implementation, high in ongoing use |
| Cost | Low technically, high through manual maintenance |
| Scalability | Low; a Markdown document becomes the runtime log |
| Team familiarity | High; the existing template remains the only entry point |

**Pros:**

- Only one visible work artifact per research case.
- No new artifact layer is required to get started.
- Directly readable by the owner.

**Cons:**

- Mixes a long-lived research case with many short-lived agent runs.
- Increases the scope and conflict risk of the already large template.
- JSON Schema validation, hashing, append-only auditing, and automated evals
  become unwieldy.
- Multiple runs and parallel agents are difficult to represent cleanly.

### Option B: Separate, artifact-first operations layer

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | Medium initially, low to medium in operation |
| Scalability | High; runs and claims are separate versioned objects |
| Team familiarity | Medium; new artifacts and gates must be learned |

**Pros:**

- Clear separation between research substance and agent operations.
- Machine-testable provenance, evidence, and reviews.
- Multiple runs, regressions, and multi-agent lineage remain comparable.
- Runtime- and provider-neutral.
- Existing documents 00–04 remain largely stable.

**Cons:**

- More artifacts must be managed together.
- Referential integrity and hashing require validators.
- Human readers need a derived, merged view.

### Option C: Immediately introduce a central database and observability platform

| Dimension | Assessment |
|---|---|
| Complexity | High |
| Cost | High |
| Scalability | High |
| Team familiarity | Low to medium, depending on the platform |

**Pros:**

- Good query, dashboard, and access-control options.
- Append-only events and large run volumes can be managed efficiently.
- Later automation can be integrated directly.

**Cons:**

- Early commitment to technology and a data model.
- Infrastructure work before the agent flow and fields are stable and tested.
- Migration and platform operation can dominate the methodological work.
- Local, verifiable use of the framework becomes harder.

### Option D: No additional operations layer

| Dimension | Assessment |
|---|---|
| Complexity | Low in the short term |
| Cost | Low in the short term, high during error analysis |
| Scalability | Very low |
| Team familiarity | High |

**Pros:**

- No new files, schemas, or processes.
- Immediate continuation with the existing document package.

**Cons:**

- Individual LLM runs are not reproducible.
- Claim and citation errors remain difficult to locate.
- Prompt, model, or tool changes can regress unnoticed.
- Human overrides, forecasts, and multi-agent contributions are not audit-proof.

## Trade-off analysis

Option A looks simple at first, but makes one case Markdown document serve as
the research record, telemetry log, evidence graph, and review system at once.
That coupling complicates both human work and automated validation.

Option C could be efficient at very high run volumes, but it fixes the
infrastructure before the substantive artifacts have been stabilized through
real use. The first technical decision is the data and control model, not the
storage technology.

Option B adds artifacts while keeping their responsibilities small and
explicit. JSON schemas enable early automation, while Markdown keeps normative
rules readable. Content hashes and stable IDs create a later migration
boundary: a database can be added without reinventing the substantive model.

The additional effort is justified because run provenance, evidence chains, and
immutable reviews are not editorial extras. They are prerequisites for
reliably detecting agent errors, regressions, and human intervention.

## Consequences

- Methodological research documents and operational run artifacts are maintained
  separately and linked by `research_id`, `research_version`, and `run_id`.
- Every decision-bearing run requires a validated manifest and evidence
  document; human intervention requires a review document.
- Claims can be reviewed and withdrawn at claim level without rewriting
  historical runs.
- Prompt, model, tool, data, and schema changes become visible as deltas and
  trigger evals or reviews when material.
- The improvement loop becomes measurable; an overall score increase must not
  hide a critical individual regression.
- Multi-agent work becomes possible but requires additional lineage, ownership,
  and merge controls.
- The number of files and references increases. Validators and a later merged
  reading view become important.
- SHA-256 and file artifacts protect content integrity, but not truth,
  availability, or long-term archiving; retention and storage remain separate
  decisions.
- Runtime, cost, and trace data may contain sensitive information and require
  project-specific retention and access controls.
- The choice of a database, event store, signature, or observability platform
  is postponed until real run volumes and query requirements are known.

## Action items

1. [x] Create the normative operations standard in **05_AGENT_OPERATIONS.md**.
2. [x] Document an ADR for separating the methodological core and operations
   layer.
3. [x] Validate run, evidence, forecast, and review schemas against positive and
   negative fixtures.
4. [x] Automatically check minimal examples for all four schemas.
5. [x] Run the evaluation catalogue, baseline, runner, and unit tests.
6. [ ] Obtain substantive approval of the initial evaluation baseline from an
   identified human.
7. [ ] Fully implement validators for referential integrity, hashes,
   evidence-grade rules, and the release gate.
8. [ ] Set project-wide retention, access-control, and signature rules.
9. [ ] After real pilot runs, check whether a database or observability platform
   is required.
