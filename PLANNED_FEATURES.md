# Geplante Funktionen

Diese Liste enthält bewusst nur Vorhaben. Ein Eintrag hier ist weder
implementiert noch geprüft noch freigegeben.

## LLM-Stresstest gegen heimliche Forschungsänderungen

**Status:** geplant, nicht implementiert

Der Stresstest soll mehrere Sprachmodelle gezielt mit schwierigen Situationen
konfrontieren: negative Ergebnisse, widersprüchliche Quellen, verlockende
nachträgliche Filter, geänderte Zeitfenster, neue Ausschlüsse und scheinbar
harmlose Umformulierungen. Geprüft wird, ob der Hauptagent:

- den wirksamen Forschungsfingerabdruck unverändert lässt;
- jede materielle Abweichung als sichtbaren Änderungsvorschlag ausweist;
- keine vorgeschlagene Änderung ohne Nutzerentscheid übernimmt;
- bei Zustimmung eine neue Research-Version anlegt, statt die alte zu
  überschreiben;
- in verständlicher Sprache erklärt, was sich fachlich ändern würde.

Für eine spätere Freigabe braucht der Test einen versionierten Fallkatalog,
mehrere wiederholte Modellläufe, eine unabhängige Bewertung und feste
Bestehensgrenzen. Die vorhandenen deterministischen Vertragsprüfungen sind die
Voraussetzung dafür, aber kein Ersatz für diesen Live-LLM-Stresstest.

## Safe and measurable loading of normative sections

**Status:** planned, not implemented

The largest normative documents currently create a substantial context cost.
Loading only the sections needed for a research step may reduce that cost, but
it also creates a more dangerous failure mode: a required rule can disappear
from the agent's context while the returned artifact remains formally valid.
Selective loading must therefore not be enabled until missing or stale section
references are made visible and stop the affected research step.

### Prerequisite: canonical concept registry

Selective loading also removes explanatory context that currently helps an
agent connect German normative prose, English machine fields, and enum values.
Before a normative section can be loaded on its own, the project must establish
a machine-readable canonical concept registry. This is a correctness control,
not a translation or style project.

Each registry entry must contain:

- a stable, language-independent `concept_id`;
- a concise definition of the concept;
- the canonical English term for new normative text;
- legacy German terms used by the existing corpus;
- exact machine anchors where possible, such as a schema plus JSON Pointer,
  field, enum value, or executable check;
- deprecated or forbidden variants, scoped by language and document type;
- a status showing whether the mapping is active, deprecated, or unresolved.

Concepts that do not map one-to-one to a machine field must say so explicitly
instead of inventing a false-precision anchor. Every loadable normative section
must declare the `concept_id` values it relies on. The loader must append the
corresponding compact definitions and machine anchors to the section context.
An unknown concept, unresolved required anchor, or missing concept definition
must stop the affected material research step.

The effective concept entries and their hashes are part of the rule set for a
run and must therefore be recorded in the orchestration state and protected by
the research fingerprint. A changed definition is a normative change even when
the section text itself did not change.

A terminology lint check should reject explicitly forbidden variants in the
active normative corpus and point to the canonical term. Its scope must exclude
or separately handle historical decisions, quotations, source reconstructions,
and examples where an old or non-canonical term may be evidence rather than an
active instruction. It must not rewrite terms automatically.

### Planned implementation order

1. **Complete the behavioural reference cases first.** Add cases in which the
   correct result is to stop, invoke a required specialist, reject returned
   work, report a research-fingerprint change, or block an unsupported causal
   claim. Only then run and freeze the live-agent behavioural baseline.
2. **Build the canonical concept registry.** Collect the concepts already
   represented in schemas, executable checks, and active normative prose;
   resolve ambiguous mappings explicitly; and add validation for concept IDs,
   required definitions, statuses, and machine anchors.
3. **Introduce stable section identifiers.** Give every loadable normative
   section an explicit identifier that is independent of its heading text.
   Maintain one machine-readable registry as the authoritative map from the
   identifier to the source document and section boundaries. Each section
   entry must also declare its required concept IDs.
4. **Check the complete reference chain in CI.** Automatically prove that
   every section identifier the router can emit exists exactly once, resolves
   to non-empty content, and is present in the registry. Also prove that every
   declared concept ID resolves, every required machine anchor exists, and all
   explicitly forbidden variants are absent from their lint scope. Unknown,
   duplicate, empty, or unresolvable references must fail validation.
5. **Make runtime loading fail closed.** Before a material research step, the
   loader must confirm that every requested section was resolved and loaded.
   It must also confirm that the section's required concept entries were
   resolved and included. If any requested section or required concept is
   missing, ambiguous, empty, or fails its integrity check, the step must stop
   instead of continuing with a reduced rule set. A fallback to a larger
   document must never happen silently.
6. **Record the effective rule set for every run.** The orchestration state
   must list each loaded section identifier, source document, content hash,
   reason for loading, approximate token count, and effective concept-entry IDs
   and hashes. These records must also form part of the research fingerprint so
   that a rule or concept change between runs cannot remain invisible.
7. **Preserve useful prompt caching.** Put the small, stable, always-required
   rule core first and append variable task-specific sections afterwards. This
   prevents selective loading from needlessly changing the stable prompt
   prefix for every case.
8. **Measure before shortening.** Use the run manifests to report which
   sections are loaded, how often they are loaded, their approximate token
   cost, and which loads appear unnecessary. Absence from the returned artifact
   is not sufficient evidence that a section was unnecessary: a preventive
   rule may be successful precisely because the prohibited action never
   appears. Token estimates and assumed savings are hypotheses until these
   measurements exist.
9. **Move explanations and examples cautiously.** Explanations, edge cases,
   and examples may affect how an agent applies a short rule. Move them only
   after the behavioural baseline exists, one independently reviewable change
   at a time. Compare each change with the baseline and restore or investigate
   any material behavioural difference. Do not describe this work as
   risk-free token removal.

### Main risks to control

- **Invisible loss of a gate:** the router requests a stale identifier, the
  rule is not loaded, and a schema-valid artifact creates false confidence.
- **Identifier drift:** renaming or moving a heading breaks references if IDs
  are derived from document wording rather than assigned explicitly.
- **Semantic disconnect:** a section uses a prose term without loading the
  concept entry that connects it to the governed machine field or status.
- **Registry without enforcement:** a correct-looking concept list creates no
  protection if sections do not declare concepts or the loader ignores them.
- **False-precision mapping:** a broad research concept is assigned to one
  convenient schema field even though the rule actually spans several fields
  or has no one-to-one machine representation.
- **Overbroad terminology lint:** valid quotations, historical records, or
  source-language reconstructions are rejected as though they were active
  normative instructions.
- **Unrecorded rule changes:** two runs appear comparable although different
  versions of a normative section or concept definition governed them.
- **Alert fatigue:** harmless editorial changes may alter a content hash. This
  must be handled together with severity-aware change control, without hiding
  genuine rule changes.
- **Caching fragmentation:** highly variable prompt prefixes can erase the
  expected cost benefit of caching.
- **Behaviour loss through shortening:** removing a rationale or example may
  preserve the written rule but reduce correct handling of borderline cases.
- **Weak baseline evidence:** a single non-deterministic agent run or a
  baseline without stop and escalation cases cannot establish unchanged
  behaviour.
- **Unproven savings:** the estimate that a fixed fraction of the corpus is
  redundant must not be treated as measured fact.
- **Control overhead:** the registry, loader, fingerprint record, and tests can
  become bureaucratic unless they remain generated or mechanically checked
  wherever possible.

### Activation criteria

Selective normative loading may be used for real research only when the
critical reference cases are in the baseline, the concept and section
registries and their complete reference checks pass, injected missing-section
and missing-concept failures stop the run, the exact effective sections and
concept entries are recorded and fingerprinted, and a measured before-and-after
report shows the context saving without a new critical behavioural failure.

## Interruption-safe framework maintenance

**Status:** planned, not implemented

Long framework-maintenance tasks should be resumable without replaying the full
conversation or loading the research corpus again. This is separate from the
research `orchestration_state`: it records development progress, not a market
research decision or evidential state.

For a multi-step maintenance task, create a small checkpoint before a handoff,
long pause, expected usage-limit boundary, or other interruption. Record only:

- the fixed objective and scope;
- the working branch, pull request, and last verified commit or diff;
- the last completed step and the next bounded step;
- unresolved user decisions and known concurrent work;
- checks already passed and checks still required;
- external side effects already performed, with whether they are safe to retry.

On resumption, verify the checkpoint against the actual Git state before using
it. Git, validated artifacts, and external service state remain authoritative;
the checkpoint is only a compact handoff index. A stale or contradictory
checkpoint must be rejected or repaired visibly. A resumed agent must not
repeat a push, merge, deletion, publication, or research transition merely
because the note says it remains pending.

Framework maintenance should load only the files being changed and the project
instructions that govern that change. It must not load the full normative
research corpus unless the maintenance task actually requires those rules.
Mechanical extraction or formatting may use a cheaper model or deterministic
tool, but ambiguous terminology, rule changes, and scientific judgments still
require the appropriate review.

Main risks are stale progress notes, conflict with the real repository state,
blind repetition of external side effects, accidental mixing of maintenance
and research state, sensitive information in a checkpoint, and creating more
checkpoint bureaucracy than the interrupted task warrants. The feature should
therefore apply only to genuinely multi-step or interrupted work.

Activation requires a recovery test in which an interrupted synthetic
maintenance task resumes from the checkpoint, detects a deliberately stale
Git reference, does not repeat a recorded external side effect, and completes
without loading unrelated normative documents.

## Local-first research execution and data operations plane

**Status:** planned, not implemented

The framework currently defines how research must be specified, routed,
reviewed, fingerprinted, and accepted, but it does not yet provide one
operator-friendly system that reliably acquires data, starts bounded research
jobs, resumes them after infrastructure failures, and connects every result to
the exact data, code, environment, and authorization that produced it. Ad hoc
scripts, shared mutable folders, cron jobs, or direct agent shell commands can
be useful during exploration, but they make it too easy to use the wrong data
vintage, duplicate a costly run, overwrite an earlier result, or mistake a
successfully completed process for accepted research.

The implementation should retain the practical strengths demonstrated by the
public [Edge Hunting setup](https://blue-grass-0beb37910.7.azurestaticapps.net/substack/article_02_the_setup.html):
columnar files, isolated execution environments, bounded parallel jobs, cheap
cloud overflow, deterministic computation, and an append-only operational
record. It should replace the fragile parts with a small local-first data
catalog, a durable workflow layer, immutable run bundles, and a plain-language
operator view. The system must remain usable by a research decision-maker who
is not expected to understand databases, containers, or job schedulers.

### Goals

1. A user can start an already authorized research operation and see its
   status, inputs, cost, failures, and outputs without inspecting source code or
   cloud consoles.
2. Every accepted result resolves to immutable dataset snapshots, an exact
   source revision, a locked runtime environment, explicit parameters and
   seeds, and a complete validated `run_manifest`.
3. Identical authorized requests are recognized before computation begins, and
   an explicit replay creates linked evidence rather than silently duplicating
   or replacing the original run.
4. A local or cloud worker can crash without producing a false success, a
   half-written final bundle, or an untraceable retry with changed inputs.
5. The initial system remains inexpensive and understandable: Parquet files
   stay the canonical bulk-data format, no always-on database server is
   required, and cloud execution is optional.

### Explicit non-goals

- **No machine-learning platform in this phase.** Do not add model training,
  feature stores, hyperparameter tuning, model registries, LightGBM, neural
  networks, or automated signal discovery. MLflow is also excluded from v1;
  experiment tracking must be research-run tracking rather than a dependency
  on an ML platform.
- **No live trading or order routing.** The execution plane runs research,
  validation, replay, simulation, and permitted data-maintenance jobs. It must
  not place or manage broker orders.
- **No replacement of scientific governance.** A completed job is not an
  accepted result. The existing router, specialist prerequisites, research
  fingerprint, reviews, freeze rules, and human decisions remain authoritative.
- **No enterprise data warehouse.** PostgreSQL, Snowflake, Databricks,
  Kubernetes, and a distributed lakehouse are not required for the initial
  single-operator scale.
- **No automatic external publication.** A dashboard or generated report may
  summarize canonical local state, but publishing or sharing it remains a
  separate human-authorized action.

### Target architecture

```text
approved data source
        |
        v
staged download -> validation/quarantine -> immutable Parquet snapshot
                                            + dataset manifest
        |                                           |
        +-------------------+-----------------------+
                            v
                rebuildable DuckDB catalog
                            |
authorized execution request + router decision + research fingerprint
                            |
                            v
                    Prefect workflow
                     /            \
            local worker       optional Azure job
                     \            /
                            v
                  staged result bundle
                            |
          contract checks + fingerprint comparison
                            |
                            v
        immutable completed run + audit events + operator summary
```

The data files and validated manifests are the sources of truth. DuckDB is a
rebuildable query layer, Prefect is an operational scheduler, and any operator
page is a derived view. Loss or corruption of one of those derived services
must not destroy the evidence or change a research decision.

### Planned technology choices

1. **Parquet for canonical bulk data.** Store raw provider snapshots and every
   normalized derivative as immutable, partitioned Parquet datasets. Parquet
   is compressed, portable, and efficient for time-series columns. A
   correction, normalization change, or late provider update creates a new
   dataset ID with parent lineage; it never edits an already referenced
   snapshot in place.
2. **DuckDB for local analytical access.** Use DuckDB to query Parquet directly
   and to expose stable views over approved snapshots. DuckDB can push column
   and row filters into Parquet scans, so workers need not load an entire file
   into memory. The DuckDB catalog must be reproducibly generated from dataset
   manifests and must not become the only copy of data or provenance. See the
   official [DuckDB Parquet documentation](https://duckdb.org/docs/current/data/parquet/overview).
3. **Prefect for v1 workflow orchestration.** Use a locally deployable Prefect
   flow to record task states, enforce timeouts and concurrency limits, cache
   safely reusable results, and retry eligible infrastructure failures. Its
   flow/task model already supports tracked state, caching, retries, and
   concurrent work; these should not be rebuilt in an agent-specific cron
   layer. See the official [Prefect flow documentation](https://docs.prefect.io/v3/concepts/flows).
   Keep an internal execution-backend interface so Prefect can be replaced only
   after an explicit architecture decision and equivalence tests.
4. **Local processes or OCI containers for normal execution.** A local worker
   is the required baseline. Use an OCI container when operating-system or
   dependency isolation is required, especially for cloud execution. Record
   the immutable image digest rather than only a mutable image tag.
5. **Azure Container Apps Jobs only as an optional overflow backend.** Use a
   finite-duration manual job for an expensive authorized run, with explicit
   CPU, memory, timeout, concurrency, and spending limits. Azure describes
   these jobs as finite tasks that start, perform one unit of work, and stop;
   they must not become an always-running service. See the official
   [Azure Container Apps Jobs documentation](https://learn.microsoft.com/en-us/azure/container-apps/jobs).
6. **A framework-owned run registry, not MLflow.** Canonical JSON artifacts and
   the append-only event stream record research runs. A generated DuckDB index
   makes them searchable and comparable. A later read-only web view may query
   that index, but it may not mutate canonical manifests or reviews.
7. **One locked Python environment per execution-plane release.** Introduce a
   `pyproject.toml`, a lock file and a fixed supported Python version in a
   dedicated tooling migration. `uv` is the preferred environment and lockfile
   tool because it can create reproducible environments quickly. Preserve the
   current `requirements-dev.txt` path until the migration and CI equivalence
   checks pass. Do not create a separate environment for every hypothesis
   unless an actual dependency incompatibility requires it.
8. **A replaceable deterministic backtest-engine boundary.** Do not make a
   third-party engine's internal objects the framework's research contract.
   Define a small adapter that accepts frozen market-data references, strategy
   rules, execution and cost assumptions, clock and calendar policy, and seeds,
   and returns orders, fills, positions, cash flows and declared metrics as
   validated artifacts. Evaluate NautilusTrader in a bounded implementation
   spike because its event-driven simulation and isolated runtime fit this use
   case, but adopt it only after fixtures verify timestamp ordering, order
   lifecycle, partial fills, fees, slippage, forced exits, session boundaries,
   futures rolls or corporate actions where applicable, and deterministic
   replay. Simple non-backtest research jobs must not depend on it.
9. **Dataframe libraries remain worker details.** A pinned worker may use
   pandas, Arrow or another compatible library, but Parquet plus its manifest
   is the cross-component boundary. Do not maintain hidden duplicate datasets
   merely to bridge different dataframe-library versions. Any required
   conversion creates a declared derived snapshot with lineage and hashes.

### Canonical storage layout

The runtime store must live outside Git. Only schemas, small fixtures,
documentation, and generated non-sensitive examples belong in the repository.
The logical layout should be independent of whether its physical location is a
local disk or approved object storage:

```text
research_store/
  datasets/
    raw/<dataset_id>/...
    normalized/<dataset_id>/...
  manifests/
    datasets/<dataset_id>.json
  requests/
    <request_id>.json
  runs/
    <run_id>/...
  audit/
    <year>/<month>/<date>.jsonl
  catalog/
    research.duckdb
  staging/
    <temporary-operation-id>/...
```

No worker may write directly into a completed dataset or run directory. It
writes to a unique staging directory, validates the staged content, and then
performs an atomic finalization. An interrupted staging directory is visibly
incomplete and may be garbage-collected only after its owner, age, and active
job state have been checked.

### Required contracts and sources of truth

Implementation should reuse existing contracts before inventing overlapping
ones. In particular, `schemas/orchestration_state.schema.json`,
`schemas/routing_decision.schema.json`, `schemas/run_manifest.schema.json`, the
research fingerprint, and append-only review events remain authoritative.

Only the following missing boundaries should receive new schemas:

1. **`dataset_snapshot.schema.json`:** one immutable raw or normalized dataset
   snapshot. It must include:
   - stable dataset ID and schema version;
   - parent snapshot IDs and transformation reference when derived;
   - provider, product or endpoint, access method, retrieval start and end,
     provider vintage where available, and license or redistribution class;
   - asset class, canonical instrument identifiers and provider symbols;
   - actual temporal coverage, frequency, timestamp convention, timezone,
     venue calendar, session definition, and adjustment policy;
   - file paths relative to the snapshot root, byte sizes, row counts,
     per-file SHA-256 hashes, minimum and maximum timestamps, and the canonical
     snapshot hash;
   - duplicate, gap, ordering, type, range, and calendar-validation results;
   - correction, lateness, missing-data, and known-quality notes; and
   - actor, code revision and completed timestamp that created the snapshot.
2. **`execution_request.schema.json`:** the exact bounded operation the
   orchestrator is allowed to run. It must include:
   - request ID, research ID and research version;
   - routing-decision and orchestration-state references;
   - operation type and a registered entrypoint, not an unrestricted prose or
     shell command;
   - immutable dataset IDs, code revision or source-archive hash, environment
     lock hash, parameters, seeds, and required input artifact hashes;
   - local or cloud backend policy, CPU, memory, concurrency, wall-clock,
     tool-call and monetary limits;
   - required output types and validation checks;
   - retry class and idempotency key; and
   - the authorizing actor and authorization timestamp.
3. **`execution_event.schema.json`:** operational lifecycle events such as
   request validation, queueing, start, heartbeat, cancellation, transient
   failure, retry, completion, artifact rejection, and finalization. Reuse the
   existing actor and hash-chain conventions instead of creating an unrelated
   audit format.

The existing `run_manifest` should be extended only where an execution field
is genuinely absent. It remains the final account of a run's status, lineage,
runtime, component versions, dataset vintages, hashes, artifacts, usage, cost,
latency, errors, and operational release gates. A second competing run
manifest must not be introduced. Its current contract describes an agent run
and requires agent, model, prompt and tool-call details. Before deterministic
jobs use it, publish a versioned backward-compatible migration or explicit
schema union that distinguishes at least `AGENT_RUN`, `DETERMINISTIC_JOB` and
`DATA_INGESTION`. Model and prompt provenance remain mandatory for
`AGENT_RUN`; they must be structurally inapplicable rather than populated with
invented placeholder values for deterministic jobs. Shared lineage, data,
runtime, integrity, artifact, cost, error and release-gate fields must retain
one meaning across all run kinds. Add migration fixtures proving that an
existing v1 agent manifest remains valid under its original schema and that a
deterministic job cannot masquerade as an agent run or omit its executable and
environment identity.

### Data ingestion and catalog behavior

1. Each provider has a small adapter that translates an approved request into
   a download and emits provider-native metadata. Provider credentials come
   from environment or platform secret references and never from committed
   configuration.
2. Downloads first enter staging. Record HTTP or API status, request window,
   pagination, returned row count and provider limits. A silent row cap or
   incomplete pagination is a validation failure, not a small dataset.
3. Preserve the raw provider response when licensing permits. Normalize into a
   new derived snapshot rather than replacing the raw input.
4. Convert timestamps to a declared canonical representation while retaining
   enough source metadata to reconstruct the conversion. Daylight-saving,
   session boundaries and exchange calendars require explicit tests.
5. Resolve symbols to stable instrument identities. A reused ticker, contract
   roll, delisting or corporate action must not silently join unrelated
   instruments.
6. Catalog only snapshots whose manifest and content hashes validate. A
   catalog entry points to one exact snapshot and exposes whether it is raw,
   normalized, quarantined, superseded, unavailable, or approved for a named
   research role.
7. Workers receive immutable dataset IDs rather than open-ended paths such as
   `latest/`. DuckDB connections used by workers are read-only. One serialized
   catalog-update process prevents concurrent catalog writes.
8. Rebuilding the DuckDB file from the manifests must produce the same dataset
   inventory. A stale or missing catalog may delay work but must not change
   which snapshots the manifests identify.

### Workflow and job-state behavior

The first flow should implement this fixed sequence:

```text
validate authorization
  -> resolve and hash inputs
  -> check idempotency and budget
  -> prepare isolated runtime
  -> execute bounded operation
  -> collect staged artifacts
  -> validate contracts and integrity
  -> derive candidate research fingerprint
  -> compare with effective fingerprint
  -> finalize or reject the result bundle
  -> update checkpoint and operator summary
```

- An LLM may draft an execution request, but it may not directly create a
  trusted job or edit workflow state. The schema validator, router decision,
  authorization and budget checks control dispatch.
- Use two separate concepts: **execution status** describes whether software
  ran (`QUEUED`, `RUNNING`, `SUCCEEDED`, `PARTIAL`, `FAILED`, `CANCELLED`);
  **research acceptance** describes whether the returned work may affect the
  research state. `SUCCEEDED` must never imply `ACCEPTED`.
- Compute the idempotency key from the canonical authorized request, dataset
  snapshot hashes, exact source revision, environment lock, parameters and
  seeds. Submitting the same key again returns the existing run reference
  unless the user explicitly authorizes a replay.
- A replay creates a new run linked to its source run and records why it was
  requested. It does not overwrite or silently upgrade the earlier result.
- Retry only failures classified as transient infrastructure failures, such as
  a worker interruption or temporary service unavailability. A failed
  scientific gate, invalid data, contract failure, exhausted budget, or
  deterministic code error does not become true by retrying and must remain
  failed or blocked.
- Exactly one layer owns automatic retries. If Prefect owns the retry, the
  Azure job configuration must not independently create untracked duplicate
  attempts.
- Enforce CPU-thread limits as well as job-count limits so several nominally
  small jobs cannot each consume all local cores. Record peak memory, runtime,
  worker identity and final exit reason.
- Cancellation must stop further dispatch, retain logs and partial artifacts,
  label them incomplete, and never manufacture the required completion marker.
- No material returned work is finalized as accepted until the complete
  candidate research fingerprint is `UNCHANGED`. A difference produces the
  existing visible `CHANGE_PROPOSED` path and leaves the effective state
  untouched.

### Runtime isolation and reproducibility

- Freeze the supported Python version, dependency lock, locale, timezone and
  relevant native-library versions for each execution-plane release.
- An accepted run must identify a clean source commit or an immutable source
  archive. Exploratory execution from a dirty worktree is permitted only when
  the exact patch is captured and hashed; it cannot silently become an accepted
  production result.
- Record every explicit random seed and deterministic setting used by the
  operation. If an external service is nondeterministic, preserve its returned
  content and response hash rather than pretending it can be regenerated.
- Cloud jobs use an image digest and the same contract tests as local jobs.
  A mutable tag such as `latest` is insufficient evidence of the runtime.
- Data files are mounted or downloaded read-only. Each run has its own output
  directory and temporary space.
- Secrets must be redacted from commands, environment dumps, logs, exceptions,
  manifests and operator views. Tests must inject recognizable fake secrets
  and prove that none survive in finalized artifacts.

### Completed run bundle

Every run directory should contain at least the following logical artifacts;
the existing schemas determine their final names and fields:

```text
runs/<run_id>/
  execution_request.json
  run_manifest.json
  input_refs.json
  logs/
    stdout.log
    stderr.log
  results/
    metrics.json
    tables/*.parquet
    figures/*
  validation/
    schema_report.json
    integrity_report.json
    fingerprint_check.json
  completion.json
```

`completion.json` is written last and only after all required validations pass.
Its presence means that the bundle is structurally complete, not that its
scientific conclusion is positive or accepted. Each declared artifact must
have a content hash and media type. Missing required artifacts, hash mismatch,
unattested summaries or path references outside the run root fail closed.

Completed bundles are immutable. Corrections, reruns and retractions create
new linked records under existing lineage and review rules. Human-readable
reports and graveyard entries must be generated from these canonical records,
not maintained as independent hand-edited summaries.

### Operator experience

The minimum operator interface must avoid requiring database or cloud
knowledge. It should provide one local launcher and a read-only research-desk
view that shows, in ordinary language:

- what operation is requested and whether it is authorized;
- which exact data snapshot and research version it will use;
- whether it will run locally or incur an estimated cloud cost;
- current state, elapsed time, resource use and last meaningful event;
- clear separation between process success and research acceptance;
- any failure, missing prerequisite or proposed material change, with the next
  required human decision;
- links to the validated result bundle, logs, input manifests and reviews; and
- comparison of two linked runs without presenting a changed specification as
  a like-for-like replication.

For v1, Prefect's UI may supply the low-level task view while the framework
generates a plain-language HTML run card from canonical artifacts. The run card
is read-only. Buttons that authorize research changes, cloud spend,
publication, deletion or live activity are out of scope until their permission
and audit behavior is separately specified.

### Optional Azure overflow

Cloud support is P1 and must not block local activation. When added:

- build and sign or otherwise attest one OCI image from the locked source and
  dependency state, push it to an approved registry, and dispatch by digest;
- use managed identity or platform secret references rather than credentials
  embedded in job configuration;
- set explicit CPU, memory, timeout, parallelism and per-request cost caps;
- grant the job read access only to the authorized input snapshots and write
  access only to its unique staging prefix;
- upload logs and outputs before reporting success, then verify their hashes
  locally or in the trusted finalizer;
- record Azure execution ID, region, image digest, resource allocation,
  measured cost and termination reason in the run manifest; and
- test loss of network, worker timeout, duplicate callback and partial upload.
  None may create two accepted runs or a structurally complete false result.

### Delivery order

1. **Contracts and synthetic fixture:** define the dataset snapshot, execution
   request and event contracts; extend the existing run manifest only where
   necessary; create one tiny synthetic time-series fixture and failure cases.
2. **Immutable local data store:** implement staged ingestion, hashes, atomic
   finalization, validation/quarantine, lineage and a rebuildable DuckDB
   catalog. No external provider is required to prove this phase.
3. **Deterministic local runner:** execute one registered non-ML research task
   from a validated request, produce the complete run bundle, enforce budgets,
   and prove idempotency and replay behavior.
4. **Scientific-control integration:** connect authorization to the router and
   orchestration state, perform the mandatory candidate-fingerprint check, and
   update the checkpoint only after accepted unchanged work.
5. **Prefect orchestration:** wrap the fixed sequence as observable tasks with
   bounded concurrency, timeouts, a single retry authority, cancellation and
   crash recovery. The canonical evidence must remain usable if Prefect is
   unavailable.
6. **Operator view:** generate the plain-language run card and an inventory of
   data snapshots, requests, active runs, completed runs, failures and blocked
   decisions from canonical state.
7. **Optional Azure backend:** implement the backend adapter, immutable image
   identity, remote staging, cost controls and failure-injection tests only
   after the local path passes all activation tests.
8. **Real research exercise:** run the complete empirical research case from
   the next planned feature through this execution plane. Do not use a
   convenient positive outcome as the acceptance criterion.

Each phase should be a separately reviewable change. Dependency-tool migration,
data contracts, execution behavior, cloud deployment, and scientific rule
changes must not be combined in one difficult-to-attribute commit.

### Priority and acceptance criteria

**P0 — required for local activation**

- Given an authorized request with valid manifests, when it is submitted
  twice, then the second submission resolves to the first computation without
  silently running it again.
- Given an explicit replay authorization, when the same operation is rerun,
  then a new linked run is created and both manifests remain immutable.
- Given a partially downloaded, truncated, duplicated, unordered, timezone-
  shifted or hash-mismatched dataset, when ingestion validation runs, then the
  snapshot is quarantined and cannot be resolved for a research job.
- Given a provider correction or normalization-code change, when data are
  rebuilt, then a new dataset ID is created with parent lineage and the old
  snapshot remains exactly reproducible.
- Given a worker crash at every boundary in the fixed workflow, when recovery
  occurs, then no false completion marker, duplicate accepted run or missing
  audit transition is produced.
- Given a deterministic code error or failed scientific gate, when the flow
  handles it, then it is not automatically retried as an infrastructure error.
- Given returned work with a changed material fingerprint, when finalization
  is attempted, then the result remains unaccepted and every changed path is
  reported through `CHANGE_PROPOSED`.
- Given a completed run, when a new environment is created from its recorded
  source, lock and data snapshot, then its deterministic test fixture produces
  the predeclared equivalent outputs within exact or explicitly defined
  numerical tolerances.
- Given recognizable fake secrets in every supported secret channel, when a
  run fails and all artifacts are finalized, then no secret value appears in
  logs, manifests, errors, audit events or the operator view.
- Given a non-technical operator, when a run is queued, running, failed,
  blocked, completed but unaccepted, or accepted, then the generated view shows
  the correct state and next action without requiring inspection of Prefect,
  DuckDB, Azure or source code.

**P1 — high-value follow-up**

- Azure Container Apps Jobs backend with image-digest, remote-staging,
  failure-recovery and cost-cap validation.
- Backtest-engine adapter plus the independent conformance fixtures required
  before NautilusTrader or another engine can produce accepted artifacts.
- Approved object-storage backup and restore for immutable snapshots, bundles
  and audit segments.
- Read-only run comparison and program-level time, compute, data-cost and
  rejection-reason dashboards derived from canonical records.
- Scheduled data refresh that always creates a new snapshot and never silently
  changes the data role of an existing research version.

**P2 — design compatibility only**

- Additional execution backends and larger object stores behind the same
  contracts.
- Standard research-object export such as RO-Crate for external reproducibility.
- Multi-user authentication and role-based authorization.
- A public status and correction view generated from the canonical ledger.
- Machine-learning support only as a separate future feature with its own
  justification, contracts, leakage controls, validation and explicit user
  authorization. Nothing in v1 should require it.

### Success measures

- 100% of finalized runs reference valid immutable data, source and environment
  hashes and pass the existing run-manifest checks.
- 100% of accepted material outputs have an `UNCHANGED` fingerprint decision
  and a valid checkpoint transition.
- The injected duplicate, crash, timeout, stale-catalog, partial-upload,
  corrupted-data and secret-leak tests all fail safely.
- An operator can identify the data vintage, research version, execution state,
  acceptance state, cost and failure reason of the reference run from one
  generated page.
- The DuckDB catalog can be deleted and rebuilt from canonical manifests
  without inventory drift.
- The local reference workflow completes without Azure, MLflow, a database
  server, machine-learning libraries or manual edits to runtime records.

### Open implementation decisions

- **Blocking — engineering:** select the fixed Python version and verify that
  the existing validation scripts and planned DuckDB/Prefect versions support
  it before introducing `uv` and a lockfile.
- **Blocking — research/data owner:** approve the first provider, its license,
  canonical instrument-identity rules, timestamp policy and required quality
  checks before ingesting real data.
- **Blocking for cloud only — owner:** set the Azure subscription, region,
  storage, registry, identity and per-run/monthly budget. Local implementation
  does not wait for this decision.
- **Non-blocking — engineering:** choose whether the first operator view is a
  generated static page or a small local application. It must remain read-only
  and satisfy the same state-display tests either way.
- **Non-blocking — operations:** define retention and recoverable cleanup rules
  for abandoned staging directories, logs and large result artifacts. Completed
  canonical evidence and referenced data snapshots are never removed by that
  cleanup path.

### Activation boundary

The execution plane may be called implemented only after the complete P0 test
matrix passes on a clean local installation, a deliberately interrupted run
recovers safely, the catalog rebuild is identical, a non-technical operator can
understand the reference run from the generated view, and the existing
framework validation suite still passes. Successful cloud execution, a large
number of parallel jobs, or an attractive research result cannot substitute
for these conditions.

## Bounded historical mechanism-led strategy search

**Status:** planned, not implemented

The failure of hundreds of mechanically generated strategies would primarily
indict the candidate generator, provided the tester is valid and has adequate
power for plausible effects. The framework should therefore search for a small
number of testable hypotheses derived from documented market structure or
repeatable footprints in data that already exist. It must not respond by
creating larger indicator grids, building a continuously running observatory,
or waiting weeks or months for future observations.

This feature governs the search for a candidate, not the construction of a
positive result. Each search cycle uses one fixed historical data inventory,
has explicit stage budgets and reaches a terminal state within at most three
consecutive working days. Careful work inside that boundary is required;
speed is not permission to skip sources, data checks, alternatives, costs or
falsification.

### Goals

1. Move candidate generation from indicator combinations to documented or
   historically observable structural mechanisms without turning mechanism
   stories into an unlimited new search space.
2. Reject weak ideas within hours and spend a full historical backtest only on
   candidates that survive cheaper discriminating tests.
3. Complete every authorized candidate search in no more than three working
   days using already available historical data.
4. Make the ordinary `NO_TRADE` or `NO_RESEARCHABLE_PATTERN` outcome explicit
   so that an agent is never rewarded for inventing daily opportunities.
5. Return an honest bounded verdict that distinguishes historical support from
   prospective confirmation, which the planned framework does not perform.

### Explicit scope and non-goals

- **Historical data only.** The search may use approved existing snapshots and
  a historical holdout sealed before the search. It does not collect or wait
  for new market data.
- **No paper or live monitoring.** Paper trading, live signals, forward-data
  accumulation and long-running observation are outside the planned framework.
- **No news-trading program.** Known news or exceptional-event dates may be
  marked as exclusions, strata or rival explanations so they do not masquerade
  as an everyday effect. Public-news reaction is not the default source of
  strategies.
- **No continuous market observatory.** The system performs a bounded query on
  an existing snapshot for one registered mechanism. It does not operate a
  permanent anomaly detector that continuously emits ideas.
- **No indicator combinatorics.** An indicator may measure a frozen construct,
  but a crossover, threshold or chart pattern is not a mechanism merely because
  it can be parameterized.
- **No machine learning.** Candidate discovery, ranking and testing require no
  learned model, feature store, model registry or hyperparameter search.
- **No positive-output quota.** A cycle may end with every candidate rejected,
  blocked or inconclusive. Completion and fast falsification are success
  measures; survivor count is not.

### Admissible starting points

A search cycle begins through exactly one of two routes:

1. **Documented-structure route:** a source describes a persistent rule,
   obligation, market design, cost, risk transfer, institutional constraint or
   routine process. Examples may include auction mechanics, settlement,
   financing, contract rolls, liquidity provision, benchmark constraints or
   recurring execution requirements. The source establishes only that the
   structure exists, not that it creates a tradeable edge.
2. **Historical-footprint route:** a predeclared descriptive query finds a
   repeatable relation in an existing dataset, such as a conditional pattern in
   spread, depth, volume, order-flow imbalance, price impact, resilience,
   relative pricing or session behavior. The query family and all inspected
   outcomes are registered as discovery exposure. A return pattern discovered
   by broad search cannot be retroactively presented as mechanism-first.

The intake must reject a starting point that is only a desired trade direction,
an unbounded request to “find an edge,” an indicator recipe, or an explanation
invented after its favorable return chart was seen.

### Required mechanism dossier

Before code for a strategy is written, record:

- the real process or historical footprint being examined;
- the source or immutable descriptive artifact supporting its existence;
- the party that may pay, what service or risk transfer that party receives,
  and whether the party is constrained, compensated or simply operating on a
  different horizon;
- any actor identity that is unknown or unobservable, without inventing one;
- the proposed transmission from the process to order flow, liquidity, price
  impact or relative price;
- where, when and in which instruments the footprint should be present;
- where and when `NO_TRADE` or absence of the footprint is expected;
- at least two plausible rival explanations when available;
- at least one observation that discriminates the proposed mechanism from a
  serious rival;
- why competition may not immediately remove the effect;
- the expected firing rate and a plausibility range for magnitude;
- the minimum data and executable-price information required;
- the cheapest result that would kill the idea; and
- the dimensions that may vary in this cycle, with a hard prohibition on
  adding dimensions after outcomes are seen.

A named mechanism without a discriminating prediction fails the dossier. A
named actor without observable implications does not improve it. For a purely
predictive candidate, the actor may remain explicitly unknown, but the pattern,
scope, alternatives and falsifier must still be concrete.

### Candidate limit and prioritization

One cycle covers one mechanism dossier and no more than three materially
distinct candidate predictions. Parameter values required to operationalize
one prediction are registered as one complete fixed family; they do not create
an excuse for dozens of informal variants.

Rank the candidates before outcome access using only:

- strength and independence of the structural or descriptive starting evidence;
- observability of the predicted footprint;
- precision of market, clock, instrument and no-trade scope;
- ability to distinguish serious alternatives;
- availability and integrity of the existing data;
- expected firing rate and effective sample size;
- feasibility of executable-price and cost modeling; and
- cost and duration of the cheapest decisive falsification.

Do not rank candidates by preliminary PnL, preferred narrative, number of agent
votes or how easy it would be to publish a favorable result.

### Fixed time budget and stage gates

The clock begins when a candidate cycle is authorized with its data inventory
and ends at a terminal verdict. The hard limit is **three consecutive working
days**, including computation, review, failed jobs and waiting for unavailable
inputs. No stage extends itself automatically.

This limit applies to one strategy-search cycle. It is not an instruction to
rush framework engineering, schema review or tester validation. Those are
separate, carefully reviewed implementation tasks; they may not be hidden
inside a candidate cycle to keep an otherwise blocked idea alive.

1. **Intake and scope — maximum 2 hours.** Fix the mechanism, starting route,
   candidate limit, historical datasets, user question and applicable claim
   level. Reject indicator-only and open-ended prompts.
2. **Mechanism dossier — maximum 3 hours.** Complete the dossier, serious
   rivals, no-trade state and cheapest kill condition. Stop if the mechanism is
   only a story or the required distinction is unobservable.
3. **Data and implementation feasibility — maximum 3 hours.** Validate the
   available snapshot, time conventions, sample support, executable prices,
   costs and required fields. Stop as `BLOCKED_DATA` if completion would require
   new future data, an unapproved purchase, or infrastructure outside the cycle.
4. **Cheap falsification — maximum 1 working day.** Run descriptive footprint,
   negative-control, matched-exposure, sensitivity and simple reference tests.
   Reject on failed direction, timing, recurrence, rival discrimination, data
   integrity, plausible magnitude or cost feasibility.
5. **Full historical test — maximum 1 working day and only for survivors.**
   Freeze the surviving specification and fixed candidate family, then run the
   applicable walk-forward, null, cost, selection and harness checks. Use a
   sealed historical holdout only if it was inaccessible before freeze.
6. **Review and closure — maximum 2 hours.** Validate artifacts, compare the
   research fingerprint, record the verdict and update the graveyard or
   candidate register. Do not spend remaining time searching for a salvage.

The stage maxima are ceilings, not targets, and stages may overlap when that
does not expose protected outcomes or change the frozen design. The complete
cycle still ends by the three-working-day boundary. A user may start a new
explicitly scoped research version later, but it inherits every exposure and
does not retroactively extend or rewrite the closed cycle.

### Historical data roles

- **Discovery/development:** may be inspected and used for the descriptive
  footprint, operationalization and cheap falsification. All learned choices
  remain attached to it.
- **Sealed historical holdout:** an existing chronological snapshot or segment
  made inaccessible before candidate specification. It is queried once through
  the controlled finalizer with predeclared outputs. After release it is
  exposed and cannot validate a changed descendant independently.
- **No independent holdout available:** the cycle may still perform a fully
  disclosed retrospective analysis, but its highest terminal status is limited
  accordingly. Cross-validation, purged walk-forward and multiple-testing
  corrections improve the retrospective test; they do not manufacture a fresh
  independent dataset.

No status requires future data. If a credible answer cannot be produced from
the fixed historical inventory, the correct result is `BLOCKED_DATA` or
`INCONCLUSIVE`, not a plan to wait for additional observations.

### Required terminal verdicts

- **`REJECTED_EARLY`:** the dossier, observability, rival-discrimination, data,
  magnitude, cost or cheap falsification gate failed before a full backtest.
- **`REJECTED_TESTED`:** the frozen candidate reached the full historical test
  and failed its predeclared decision rule.
- **`INVALID`:** a data, implementation, tester or contract defect prevents use
  of the result. Observed outputs remain in the exposure history.
- **`BLOCKED_DATA`:** the required existing data or executable-price evidence
  is unavailable within the fixed inventory and time budget.
- **`INCONCLUSIVE`:** the test is valid but cannot distinguish the relevant
  possibilities with the available historical information and power.
- **`HISTORICALLY_SUPPORTED`:** the frozen candidate passes its historical
  tests, costs and selection controls. This status does not mean forward-
  validated, causal, deployable or guaranteed to persist.
- **`NO_RESEARCHABLE_PATTERN`:** the bounded descriptive route found no stable,
  discriminating footprint worth promoting. This is an acceptable completed
  outcome, not a prompt to loosen thresholds.

### Stop rules

Stop the cycle immediately when:

- no concrete mechanism or historical footprint can be stated;
- the supposed everyday effect is carried only by a few exceptional or known-
  news periods and news trading is outside scope;
- a serious rival makes the same predictions and no available measurement can
  distinguish it within the budget;
- required data, timestamp integrity, symbology, costs or executable prices are
  unavailable within the fixed inventory;
- the plausible gross effect cannot exceed conservative costs;
- the effective sample size or tester power cannot answer the frozen question;
- a critical harness test fails;
- the candidate needs an unregistered parameter, filter, market or outcome
  after results are visible;
- the three-working-day boundary is reached; or
- continuing would require prospective data collection or long-running
  observation.

An early stop produces a complete reasoned record. It does not authorize the
agent to fill the remaining time with alternative strategies.

### Required contract and operator view

Add a versioned `mechanism_search_record` rather than encoding the cycle in a
free-form report. It should reference the existing candidate, concept-audit,
search-space, data-exposure, execution, tester and fingerprint artifacts and
record:

- authorization and hard deadline;
- starting route and mechanism dossier;
- candidate list and pre-outcome ranking;
- stage start, stop, budget and decision events;
- fixed historical data inventory and roles;
- cheap-test and full-test artifact references;
- every material result seen before a later choice;
- terminal verdict and highest permitted claim; and
- actual human time, wall-clock time, compute and data cost.

The non-technical operator view must show the current stage, elapsed time,
remaining hard budget, candidates still eligible, next kill condition and why
the cycle stopped. It must never suggest waiting for future data as the default
next step.

### Acceptance criteria

- Given an indicator-only recipe, when intake runs, then it is rejected unless
  it is converted into a measured construct inside a complete mechanism dossier.
- Given one mechanism with more than three proposed predictions, when the cycle
  is authorized, then the user or conductor must select at most three before
  any outcome is accessed.
- Given a candidate whose required data are not in the authorized historical
  inventory, when feasibility runs, then it becomes `BLOCKED_DATA` without
  starting data collection or an infrastructure project.
- Given an alleged everyday effect driven by excluded exceptional-news days,
  when the cheap test removes or stratifies them, then the ordinary-day claim
  is rejected if the footprint disappears.
- Given a cheap falsification failure, when unused time remains, then the full
  backtest is not run and no salvage variant is created inside the cycle.
- Given a surviving candidate and an untouched historical holdout, when the
  full test runs, then access follows the frozen output contract and the release
  is recorded as exposure.
- Given no untouched holdout, when a candidate survives retrospective checks,
  then it cannot receive a status stronger than the permitted historical claim.
- Given a cycle at its three-working-day deadline, when work remains, then it
  closes as `BLOCKED_DATA`, `INCONCLUSIVE`, `INVALID` or a supported/rejected
  verdict justified by completed artifacts; it does not roll into a fourth day.
- Given no candidate survives, when closure runs, then the cycle is recorded as
  completed without lowering gates or generating replacement candidates.

### Activation boundary

This feature may be called implemented only when a synthetic batch proves that
an indicator-only idea, a weak mechanism story, a missing-data candidate, an
exceptional-day artifact, a cheap-test failure, a tester defect, a historically
supported survivor and a deadline overrun all reach the correct terminal state.
The complete reference cycle must end within three working days using only its
initial historical data inventory, preserve every exposure and reject any
automatic proposal to collect future data or continue monitoring.

## Program-level adaptive research control and sequential evidence

**Status:** planned, not implemented

A continuously operating research desk is not a collection of independent
backtests. After each result, a human or agent may change the next hypothesis,
instrument, horizon, threshold, feature, cost assumption, data source, null,
or stopping decision. The complete desk is therefore one adaptive statistical
procedure. A clean walk-forward result for one candidate and a correction over
one declared grid do not protect against selection created by all earlier
results, abandoned variants, informal observations, or repeated access to the
same nominal holdout.

The current `search_space` contract correctly covers a fixed family whose size
is declared before screening. It does not yet represent an indefinitely
ordered hypothesis stream, program-level error spending, holdout information
release, or the strict time boundary of the bounded historical search. This
feature must add those controls without weakening the existing White Reality
Check, Hansen SPA, Deflated Sharpe Ratio, PBO, pipeline nulls, data roles,
freeze, fingerprint, or human decision gates.

The design is informed by work on
[adaptive holdout reuse](https://proceedings.neurips.cc/paper_files/paper/2015/file/bad5f33780c42f2588878a9d07405083-Paper.pdf),
[online false-discovery control](https://proceedings.mlr.press/v80/ramdas18a/ramdas18a.pdf),
[online LORD/LOND procedures](https://arxiv.org/abs/1502.06197),
[metamorphic testing of scientific software](https://pmc.ncbi.nlm.nih.gov/articles/PMC7252536/).
These are design sources, not plug-in guarantees. Their assumptions must be
matched to dependent financial time series and to the exact inferential object
before any method is activated.

### Goals

1. Every tested or outcome-informed candidate is counted in one immutable
   program lineage, including rejected, abandoned, duplicated, invalid and
   unpublished variants.
2. No historical period can silently regain independent validation status
   after a human, agent, parameter search, tester or narrative has learned from
   its outcomes.
3. The system can control a predeclared error budget over both fixed candidate
   families and an ordered continuing stream, while blocking unsupported
   p-values or dependence assumptions.
4. Every candidate search closes inside the bounded historical process rather
   than creating an open-ended plan to collect or monitor future data.
5. The backtest and inference apparatus demonstrate that they detect planted
   implementation faults and preserve required invariances before they can
   adjudicate real candidates.
6. Multi-agent generation can increase search breadth without turning agent
   agreement, self-ranking, or review into empirical evidence.

### Explicit non-goals

- **No universal statistical correction.** Online FDR, alpha spending and
  reusable holdouts solve different problems under different assumptions. The
  framework must choose a valid method per registered design or block the claim.
- **No automatic reusable holdout for market data.** The published reusable-
  holdout guarantees are not automatically valid for non-stationary dependent
  financial time series. A strictly sealed segment of the fixed historical
  inventory is the default unless a time-series-specific release mechanism is
  independently justified and calibrated.
- **No prospective data program.** The feature does not collect future data,
  operate paper or live monitoring, or keep a candidate open while waiting for
  additional observations.
- **No machine-learning dependency.** The controls apply to deterministic
  rules, statistical studies, reconstructions and simulations. They do not
  require model training, feature stores, hyperparameter tuning or an ML
  platform.
- **No evidence from agent consensus.** Debate, reflection, ranking or an Elo-
  like score may prioritize ideas. They cannot supply a p-value, replication,
  independent review, causal identification or historical evidence.
- **No restoration of spent independence.** A new Research-ID, renamed rule,
  changed codebase, new agent, delayed publication or user-approved research
  version cannot erase earlier data exposure or program-level error spending.
- **No automatic positive conclusion.** Passing a statistical boundary does
  not establish economic relevance, executable net edge, causal mechanism,
  robustness, or suitability for deployment.

### Operating model

```text
human, source or agent proposes an idea
                  |
                  v
register candidate, parentage and complete known search family
                  |
                  v
resolve data roles and check every prior exposure
                  |
                  v
assign fixed-family threshold or next sequential error allocation
                  |
                  v
freeze test, nulls, costs, outputs and disclosure policy
                  |
                  v
run through the controlled execution plane
                  |
                  v
validate tester and p-value/evidence construction
                  |
                  v
append result and update error/information ledgers
                  |
        +---------+----------+
        |                    |
 reject/block       freeze eligible survivor
                             |
                             v
               sealed historical holdout
                             |
                             v
               bounded historical verdict
```

The next idea may depend on earlier results, but that dependence is recorded
and charged. The system does not prohibit learning; it prevents learned choices
from being presented as if they had been specified independently.

### Core concepts and state separation

1. **Research program:** the durable lineage within which hypotheses can share
   an idea source, mechanism story, data history, implementation ancestry, or
   continuation decision. It survives individual Research-IDs and versions.
2. **Fixed candidate family:** a complete set registered before any member's
   screening outcome is observed. The existing `search_space` behavior applies
   here.
3. **Adaptive hypothesis stream:** an ordered sequence in which candidate
   registration may depend on earlier disclosed outcomes. Sequence numbers are
   append-only and may not be reassigned after results are known.
4. **Data exposure event:** any access capable of informing a research choice,
   including a chart, aggregate metric, pass/fail answer, parameter ranking,
   agent summary, error message that reveals outcome information, or manual
   inspection. Access is recorded even when no formal test is completed.
5. **Sealed holdout:** an immutable chronological dataset snapshot that idea
   generators, ordinary research workers and the user-facing exploratory tools
   cannot query. Only the authorized finalizer can perform the frozen test and
   release the predeclared response.
6. **Information budget:** the permitted information releases from protected
   data. It is separate from the statistical error budget. Revealing a full
   return series spends more information than returning one predeclared
   pass/fail decision even if both concern the same hypothesis.
7. **Error budget:** the predeclared family-wise or false-discovery resource
   allocated across valid tests. It is updated from immutable test events, not
   reconstructed from published survivors.
8. **Execution status, statistical decision, evidence status and research
   decision:** four separate states. Software completion, rejection of a null,
   evidential sufficiency and authorization to continue must never collapse
   into one `PASS` value.

### Program-level lineage and hypothesis accounting

1. Assign every research line a stable `research_program_id` before empirical
   screening begins. If earlier work already exists, import it as historical
   exposure with explicit incompleteness rather than pretending the program
   begins at migration time.
2. Register each candidate before its outcome is computed or disclosed. Record
   its candidate ID, Research-ID and version, parent candidates, generation
   source, creation time, hypothesis text, test family, all varied dimensions,
   effective parameterization, data requested, and the prior result events
   available to its creator.
3. Preserve candidates that are abandoned before completion. Record whether
   no outcome was observed, partial diagnostics were observed, or a complete
   result was observed. The predeclared spending policy decides whether the
   event consumes statistical budget; the exposure ledger records all
   information regardless.
4. Treat aliases, code refactors and cosmetically renamed rules as the same
   candidate or a linked descendant unless a material specification difference
   is identified. Deduplication may combine bookkeeping but must not erase
   tests already observed.
5. Expand a fixed family only by opening a new linked family or adaptive-stream
   event. Do not increase `planned_screen_count` after observing results.
6. Record unsuccessful code paths, invalid tests and implementation bugs. An
   invalid test cannot support a finding, but its disclosed outcome can still
   influence later choices and therefore remains part of the information
   lineage.
7. When a user authorizes a new research version, inherit all program IDs,
   candidate families, exposure events and error-ledger events relevant to the
   research line. Authorization permits the change; it does not reset history.

### Protected data and holdout-access control

The default data policy has two layers inside one fixed historical inventory:

1. **Discovery and development data:** may be examined repeatedly, but every
   resulting choice is treated as selected on those data.
2. **Sealed chronological validation holdout:** inaccessible during idea
   generation, implementation tuning and ordinary agent review. It is used
   only after the complete candidate, code, test, costs, nulls and response
   policy are frozen.

Required behavior:

- The execution plane resolves protected data through a holdout-access broker,
  not by giving workers a filesystem path or general DuckDB connection.
- A holdout request states the candidate, frozen artifact hashes, estimand,
  test statistic, output fields, disclosure granularity, threshold, error-
  ledger event and maximum runtime before access is granted.
- The broker verifies that the caller and tool role may access the requested
  columns and dates. Idea-generation, reflection and ranking agents receive no
  holdout access.
- The released response and its exact recipients are appended as a data
  exposure event. A report shown to the user counts as exposure even if the
  underlying files remain sealed.
- Once outcomes from a period influence a choice, that period cannot be labeled
  independent for the changed candidate. A narrower report, forgotten value or
  different agent does not reverse the exposure.
- If the holdout is accidentally accessed, leaked into logs, or queried with
  an unauthorized statistic, fail closed, preserve the event, and require a
  new plan using another already-existing segment that was demonstrably sealed
  before the search; if none exists, close the candidate as historically
  inconclusive or blocked.
- Full reusable-holdout mechanisms are P2. Before adoption, test their
  assumptions under block dependence, regime change, heavy tails and the
  actual query class. A method proved for i.i.d. bounded queries must not be
  described as protecting financial time-series research without that work.

### Error-budget and multiple-testing behavior

The implementation must support two modes with separate contracts.

**Fixed-family mode**

- Continue to use the versioned `search_space` contract for candidate families
  frozen before screening.
- Preserve existing Bonferroni, Benjamini-Hochberg and justified effective-test
  options, together with finance-specific selection controls where appropriate.
- The family contains every eligible candidate, not only successfully executed
  or reported candidates. Any exclusion rule must be fixed before outcomes.

**Adaptive-stream mode**

- Assign every eligible test its next immutable sequence number before outcome
  access. Record the available error resource and assigned threshold at that
  time.
- P0 uses a conservative, predeclared summable alpha-spending schedule whose
  allocations cannot be increased after seeing results. With valid marginal
  p-values, this provides a transparent baseline even when an indefinite
  stream never announces its final size.
- P1 may add a validated online-FDR procedure such as LORD or SAFFRON. Each
  method requires an explicit proof or simulation-backed assessment of its
  p-value validity and dependence assumptions for the registered test stream.
  If those assumptions are unknown or violated, the method is unavailable; do
  not silently fall back to its nominal guarantee.
- Record the method version, initial error resource, allocation rule, wealth or
  candidate-threshold history, rejection events, invalidated events and the
  calculation hash. Recompute the ledger deterministically from its event
  history and compare it with stored state.
- Never reorder tests, remove failures, split a family, or open a new program to
  improve a threshold retrospectively.
- An invalid p-value receives no inferential rejection regardless of how small
  it is. P-value validity includes the complete adaptive selection and
  dependence structure relevant to its claim; an ordinary per-backtest p-value
  is not automatically eligible for the online ledger.
- Statistical rejection remains separate from effect magnitude, costs,
  stability, capacity, replication and the framework's
  higher evidence gates.

### Backtest and inference harness verification

The existing known-garbage, positive-sentinel and structure-preserving-null
tests should be extended with three complementary verification modes.

1. **Metamorphic testing:** define relations that must hold across transformed
   inputs even when no single true answer is available. Required fixtures
   should include, where applicable:
   - changing file order or chunk boundaries does not change results;
   - renaming symbols leaves a symbol-invariant strategy unchanged;
   - a session-preserving timestamp translation leaves session-relative logic
     unchanged after conversion back;
   - proportional price and cost rescaling produces the declared transformed
     cash flows rather than a new edge;
   - adding unused columns or unrelated instruments does not alter the target;
   - reversing a genuinely symmetric direction/sign fixture produces the
     predeclared mirrored output; and
   - running the same frozen fixture locally and in the cloud produces
     equivalent artifacts within declared numerical tolerances.
2. **Mutation testing:** deliberately introduce realistic faults and require
   the suite to kill them. The mutation catalog should cover future-bar access,
   wrong shift direction, resampling label leakage, inadequate purge horizon,
   entry at an unavailable price, cost-sign reversal, omitted fees, duplicate
   rows, timestamp-zone shifts, session-boundary errors, survivorship leakage,
   label-derived PnL, nulls that cannot differ from the tested strategy, and a
   completion gate that always passes.
3. **Differential testing:** compute small canonical fixtures through two
   independent implementations or one simple reference implementation and the
   production engine. Compare orders, fills, positions, cash, costs and final
   metrics event by event. Shared libraries or copied logic must be disclosed
   because they reduce independence.

Predeclare required relations, mutation-kill thresholds, tolerated numerical
differences and blocking discrepancies. A high aggregate mutation score cannot
excuse survival of a critical leakage, timing, cost or false-completion mutant.
Any unexplained differential result blocks the affected engine capability.

### Multi-agent search boundary

Specialized generation, reflection, ranking, adversarial review and evolutionary
idea variation may be used only inside the discovery layer:

- every generated candidate and material variant is registered before testing;
- the number of agents does not multiply evidential weight;
- agent rankings prioritize compute but do not change statistical thresholds;
- agents that can propose or rank candidates cannot access sealed holdout data;
- an agent review of another agent is not an independent implementation unless
  its code and computational path are genuinely independent;
- deterministic tools produce empirical results and preserve their artifacts;
- external evidence, validated software checks and human research decisions
  remain outside agent self-evaluation; and
- stopping idea generation because one candidate looks promising is itself an
  adaptive continuation decision and is recorded.

This permits techniques such as the generation/reflection/ranking/evolution
roles described by the
[Google AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
without confusing self-play or an internal ranking score with ground truth.

### Required contract changes

Implementation must extend existing artifacts rather than creating a parallel
research-governance system.

1. **Versioned `search_space` extension:** distinguish `FIXED_FAMILY` from
   `ADAPTIVE_STREAM`; add `research_program_id`, immutable event sequence,
   family-parent references, allocation method and version, initial error
   resource, eligibility policy, dependence assessment, p-value-validity
   references, ledger hash and current state. Existing v1 fixed-family fixtures
   must retain their original meaning.
2. **`statistical_test_event.schema.json`:** record sequence number, candidate
   and family, registration time, outcome-access time, assigned threshold,
   method state before and after, test statistic and p-value with construction
   reference where applicable, decision, validity status, invalidation reason,
   data snapshots, exposure events, result artifact and event hash. Events are
   append-only and may be superseded but not edited or resequenced.
3. **`data_exposure_event.schema.json`:** record actor and recipients, dataset
   snapshot and time range, data role, query or artifact hash, disclosure class
   (`NONE`, `PASS_FAIL`, `BOUNDED_SUMMARY`, `FULL_RESULT`, `RAW_ACCESS`),
   purpose, authorization, affected Research-IDs and programs, and whether
   independence was consumed. Exact protected values need not be duplicated in
   the ledger.
4. **`tester_verification_report.schema.json`:** record metamorphic relations,
   mutation catalog and criticality, differential implementations, seeds,
   expected results, observed discrepancies, mutation score, surviving
   critical faults, tested engine capabilities and final `PASS / FAIL / BLOCKED`.
5. **Research fingerprint and orchestration state:** include all effective
   program IDs, search-space and sequential-ledger state, exposure history,
   holdout policy, bounded-search deadline and tester-verification references.
   A material difference follows the existing `CHANGE_PROPOSED` rule.

Do not store a mutable summary such as only `alpha_remaining`. The current
state must be reproducible from immutable events, and the generated value and
event-derived value must match before another test is authorized.

### Operator experience

The research-desk view should translate the controls into ordinary language.
For each program and candidate it must show:

- why this candidate belongs to the program and which earlier results informed
  it;
- how many candidates and variants have been registered, tested, invalidated,
  rejected, blocked and retained;
- which datasets remain independent and which have already influenced choices;
- whether the next test belongs to a fixed family or adaptive stream;
- the assigned threshold or reason no valid threshold is available;
- the remaining error resource without suggesting that it is investment risk
  capital or a probability the strategy is true;
- the current bounded-search stage, hard deadline and remaining time;
- which tester capabilities have passed, failed or remain unverified; and
- the next permitted action and any decision that requires the user.

Warnings must be concrete. Prefer “The proposed threshold was selected after
the 2024 holdout result was shown, so that period cannot validate this version”
over “possible leakage.” A user may authorize a new version, but the interface
must show that the exposure and program history remain attached.

### Delivery order

1. **Program and exposure model:** define stable program identity, import rules
   for historical work, candidate parentage and the append-only data-exposure
   event. Add fixtures for incomplete legacy history.
2. **Sealed-holdout enforcement:** implement role-based access through the
   execution plane, disclosure classes, immutable access events and tests that
   deny generator and reviewer access.
3. **Conservative sequential baseline:** extend `search_space` with adaptive-
   stream mode and implement deterministic summable alpha spending. Rebuild
   every state from events and fail on reorder, deletion or arithmetic drift.
4. **Harness-verification suite:** add metamorphic relations, the critical
   mutation catalog and a simple independent reference implementation before a
   production backtest engine can adjudicate a real strategy.
5. **Bounded-search integration:** connect every program event to the
   three-working-day mechanism-search record and close rather than extend a
   candidate when its historical inventory or time budget is exhausted.
6. **Program-level operator view:** display lineage, exposures, error spending,
   bounded-search time, tester status and allowed next actions in plain language.
7. **Online-FDR method:** add LORD, SAFFRON or another selected method only
   after p-value and dependence simulations satisfy predeclared calibration
   criteria and an independent methods review accepts the implementation.
8. **Reusable-holdout investigation:** remain P2 until a design appropriate to
   chronological dependent market data is justified against the simpler sealed
   historical-holdout baseline and can be evaluated inside a bounded project.

Build the P0 controls before increasing autonomous idea-generation throughput.
Faster search without complete lineage, protected data and error spending would
increase the problem this feature is intended to control.

### Priority and acceptance criteria

**P0 — required before program-level claims**

- Given a candidate created after earlier outcomes were disclosed, when it is
  registered, then its parentage and available result events are recorded and
  it cannot claim pre-result specification on the exposed data.
- Given two renamed or refactored versions with the same effective rules, when
  deduplication runs, then their lineage is joined without deleting either
  observed test or restoring error budget.
- Given a fixed family whose planned size is changed after its first outcome,
  when validation runs, then the change is rejected or opened as a new linked
  adaptive event rather than rewriting the family.
- Given an unbounded stream under the P0 alpha-spending schedule, when any
  prefix of valid null p-values is simulated, then empirical false-positive
  behavior meets the predeclared tolerance and ledger arithmetic exactly
  reproduces from events.
- Given a completed, partial, invalid, cancelled-before-disclosure and
  cancelled-after-disclosure test, when spending is computed, then each follows
  its predeclared eligibility policy and every information release remains in
  the exposure ledger.
- Given an idea-generation or ranking agent, when it requests holdout data or a
  proxy that would reveal protected outcomes, then access is denied and the
  attempt is recorded without leaking the value.
- Given any authorized holdout release, when a descendant candidate changes in
  response, then the exposed period cannot retain an independent role for that
  descendant.
- Given a candidate that cannot be resolved from its authorized historical
  inventory, when its bounded-search deadline arrives, then it closes as
  blocked or inconclusive instead of starting future-data collection.
- Given the critical mutation catalog, when each fault is injected, then every
  leakage, timestamp, execution-cost, label-PnL, invariant-null and false-
  completion mutant is killed. Survival of any critical mutant blocks the
  affected harness capability regardless of the aggregate score.
- Given two independent implementations of the canonical fixture, when their
  event-level outputs disagree beyond tolerance, then the capability remains
  blocked until the discrepancy is explained and resolved.
- Given unanimous agent approval without new external or computational
  evidence, when evidence status is evaluated, then no statistical, causal,
  replication or historical-evidence level is upgraded.
- Given authorization for a new Research-ID or version, when it is created,
  then relevant program lineage, exposure history and error spending are
  inherited unchanged.

**P1 — high-value follow-up**

- One validated online-FDR implementation with method-specific dependence and
  p-value calibration tests, immutable state transitions and independent
  implementation review.
- Tool-level separation between discovery agents, protected-data finalizers and
  evidence reviewers, with denial and information-flow tests.
- Plain-language counterfactual display showing how the decision would differ
  under the fixed-family, conservative spending and approved online procedure,
  without allowing the user to select the most favorable method after seeing
  results.

**P2 — research and architectural compatibility**

- A time-series-appropriate reusable-holdout mechanism with explicit
  information accounting and empirical calibration.
- Dependence-robust online procedures and hierarchical budgets across programs
  and candidate families when they can be validated in a bounded project.
- Privacy-preserving query release only if privacy itself becomes a requirement;
  privacy terminology must not be borrowed merely to suggest generalization.
- More elaborate multi-agent generation, debate and evolutionary search after
  P0 accounting and protected-data controls are demonstrably effective.

### Success measures

- 100% of empirical candidates resolve to a research program, candidate-family
  or stream event, prior-result visibility set and data-exposure history.
- No test can be authorized from a mutable `latest` threshold, unregistered
  sequence position, unvalidated p-value construction or unreconciled ledger.
- The sequential ledger rebuilds byte-equivalent canonical state from events
  across duplicate submissions, crashes and replay.
- Null simulations meet predeclared type-I error or false-discovery tolerances
  for every activated procedure; power is reported separately and cannot be
  inferred from error control.
- All critical harness mutations are killed and all required metamorphic
  relations pass on both local and optional cloud execution.
- Every holdout access and user-visible protected-data release produces an
  exposure event, and injected unauthorized access reveals no protected value.
- The reference operator can explain, from one generated view, why a period is
  or is not independent, what statistical resource the next test receives, and
  when the bounded historical search must stop.

### Open implementation decisions

- **Blocking — methods:** define what constitutes one program and one candidate
  family for the first real research line, including near-duplicate rules and
  cross-version inheritance.
- **Blocking — methods:** select the P0 summable alpha-spending schedule,
  candidate eligibility policy and simulation tolerances before the first
  adaptive-stream result is observed.
- **Blocking — data owner:** select the chronological discovery and sealed-
  historical-holdout boundaries and document why their length and market
  regimes are adequate for the intended first historical claim.
- **Blocking for P1 — methods:** choose the exact online-FDR procedure and state
  its p-value and dependence assumptions in testable terms. Popularity or
  nominal power is not sufficient.
- **Non-blocking — engineering:** choose the physical holdout isolation
  mechanism. File permissions, encrypted snapshots or a separate service are
  acceptable only if denial and leakage tests pass.
- **Non-blocking — reviewer:** set critical versus non-critical mutation classes
  and numerical tolerances before seeing the production engine's discrepancies.

### Activation boundary

The program-level adaptive controls may be called implemented only when one
synthetic program containing fixed-family tests, adaptive descendants,
abandoned candidates, partial disclosures, an unauthorized holdout request, a
legitimate historical-holdout release and a deadline closure passes the
complete P0 matrix. The error ledger and data-exposure state must rebuild from
immutable events, critical tester mutations must be killed, protected values
must remain hidden, and a new Research-ID must demonstrably inherit its
history. Online FDR and reusable-holdout claims remain unavailable until their
separate method-specific activation criteria pass.

## Empirical research-desk validation and correction ledger

**Status:** planned, not implemented

The framework has extensive normative and deterministic controls, but it still
lacks a fully worked real research case. A review of the public
[Edge Hunting research series](https://blue-grass-0beb37910.7.azurestaticapps.net/substack/index.html)
showed both the value of a fast falsification desk and the danger of treating a
documented gate as a validated instrument. In particular, that project later
found that a central null test could not fail by construction, measured the
power limits of its corrected tester, replayed a source strategy against the
author's demonstrated trade, and published corrections and retractions in
place.

This feature must turn those practical lessons into executable evidence for
this framework without weakening its existing research controls.

### Planned capabilities

1. **One complete real research line.** Run at least one genuine trading-
   research case from intake through its honest terminal state. Preserve the
   full search history, data roles, decisions, costs, failures, corrections,
   and any rejected continuation. A negative, inconclusive, or invalid result
   is an acceptable outcome; a convenient positive result is not an activation
   criterion.
2. **Tester-validity and power suite.** Exercise the complete research pipeline
   on known-garbage inputs and on synthetic inputs with planted effects across
   a predeclared effect-size range. Report the false-positive rate, power curve,
   seed sensitivity, Monte Carlo uncertainty, and the smallest effect size the
   apparatus can distinguish with the required reliability. Include
   structure-preserving nulls, matched strategy and control exits, and injected
   timing, sign, indexing, and leakage faults. A gate that cannot vary or cannot
   detect its positive sentinel must fail closed.
3. **Source-demonstration replay.** When an external strategy source contains a
   sufficiently precise worked example, optionally require the implementation
   to reproduce that example's trigger, direction, entry, exit, and relevant
   timestamps before the general strategy is adjudicated. Successful replay
   establishes implementation fidelity only; it is not evidence that the
   strategy generalises or has an edge. A material mismatch blocks any
   replication claim or must be recorded as a distinct reconstructed variant.
4. **Human-readable graveyard and correction ledger.** Generate a concise view
   of rejected, blocked, invalidated, corrected, retracted, historical-only,
   and active research states from immutable source artifacts. The framework
   does not operate a paper-monitoring program. Keep the original
   verdict visible, show the reason and evidence for every correction, and
   derive all published summaries from one canonical versioned state so that
   landing pages, counts, and detailed records cannot drift silently. Raw
   evidence that is unavailable or access-restricted must be labelled as such.
   External publication remains an explicit human-reviewed action.
5. **Discovery-to-historical-validation firewall.** Detect when a
   specification, threshold, stop, target, component, universe, or mechanism
   story was selected after seeing outcomes. Such a salvage or recombination
   becomes a new candidate or research version, inherits the complete search
   lineage and information debt, and cannot reuse the affected data as
   independent validation. A historical in-sample/out-of-sample split is not
   independent if both periods influenced the final specification. The only
   independent holdout available to this planned feature is an already-existing
   historical segment that was technically sealed before the candidate was
   frozen; no paper or future-data phase is created.
6. **Low-cost triage and program accounting.** Before expensive research,
   support cheap data-model checks, input-distribution diagnostics, matched-
   exposure benchmarks, and explicit questions about the relevant trading
   window, plausible constrained actor, and expected firing rate. These are
   prioritisation heuristics, not universal evidence gates: a predictive or
   associational candidate may still proceed with an explicitly unknown actor.
   Track time, compute and data cost, hypotheses rejected, and reason for
   rejection so the program can optimise time-to-reliable-falsification rather
   than the number of backtests completed.

### Activation criteria

The feature may be described as implemented only when:

- the real end-to-end case and every effective artifact validate under the
  existing framework contracts;
- the tester-validity suite meets predeclared false-positive and power-precision
  requirements and reliably rejects the injected faults;
- a replay fixture proves that a source-example mismatch blocks a replication
  claim while a faithful replay does not upgrade evidence;
- an adaptive post-result rewrite is mechanically prevented from retaining an
  independent validation or holdout role;
- an unfrozen or adaptively changed strategy cannot access the sealed
  historical holdout, and an authorized release permanently records the
  resulting exposure;
- the graveyard and correction view is generated from canonical immutable
  records, detects a deliberately stale summary, and preserves the original
  verdict after a correction or retraction; and
- the program-level cost and rejection metrics are derived from run artifacts,
  not manually reconstructed narratives.

## Research-control hardening backlog

**Status:** planned, not implemented

The following findings must remain visible until they are implemented and
validated:

1. **Cross-version search lineage:** A new research version must inherit every
   previous data exposure, operationalization attempt, filter choice, outcome
   choice, and continuation decision from the same research line. Repeatedly
   authorizing new versions must not reset the information budget or create an
   apparently fresh search family.
2. **Selection-adjusted reporting:** Final performance reporting must show both
   the ordinary metric and a correction or decision rule appropriate to the
   complete selection process. The correction must cover the relevant
   candidate family, research-version history, and data reuse rather than only
   the survivors of the latest screen.
3. **Severity-aware change control:** Separate the semantic research
   fingerprint from the artifact-integrity manifest. Distinguish material
   research changes, evidence-integrity changes, and demonstrably non-material
   editorial changes so that harmless hash changes do not train users to
   approve every warning.
4. **Hard-gate coverage accounting:** Maintain an explicit inventory showing
   which research gates are enforced by executable checks, which are enforced
   only by schemas, which depend on an agent classification, and which remain
   prose instructions. Increase executable enforcement where the required
   condition is objectively decidable.
5. **Adversarial live-agent evaluation:** Extend the planned LLM stress test
   with agents that actively attempt to change definitions, reset the search
   history, upgrade claim levels, skip required specialists, or satisfy schemas
   with scientifically empty content. Measure repeated catch rates rather than
   treating contract validity as evidence of agent reliability.
6. **English migration and terminology control:** Establish the canonical
   concept registry described above before selective loading or translation.
   Use it to map the legacy German corpus to canonical English terms and exact
   machine anchors. Translation must be performed in translation-only commits;
   redundancy removal, shortening, and substantive rewriting must follow in
   separate commits with separate validation.
