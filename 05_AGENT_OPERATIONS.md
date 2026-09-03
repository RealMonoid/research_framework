# 05_AGENT_OPERATIONS.md

**Version:** 1.9 **As of:** 2026-08-31 **Status:** DRAFT FOR ADOPTION **Purpose:** Normative operational control layer for reproducible, verifiable, and auditable runs of an AI research agent.

---

# 1. Scope and ranking

This document complements the methodological core of:

- **00_RESEARCH_AGENT_README.md**,
- **01_RESEARCH_STANDARD.md**,
- **02_RESEARCH_CASE_TEMPLATE.md**,
- **03_RESEARCH_METHODS.md**,
- **04_CAUSAL_TOOLING.md**.

The sections belonging to the created artifact or system change are loaded via `QUICKSTART.md`. A full pre-reading is not required.

The division of tasks shall be binding:

| Document | Responsibility |
|---|---|
| Documents 00–04 | Research logic, data roles, claim level, identification, statistical methods, gates, and research end states |
| Document 05 | Run origin, claim origin, source verification, agent evaluation, telemetry, errors, reviews, changes, and operational release |

This document must not upgrade, circumvent or replace any research gate from 00-04. In particular:

- An operationally clean run does not make a methodical **FAIL** or **BLOCKED** a **PASS**.
- A sufficiently proven text statement does not turn a predictive claim into a causal claim; **00 §8a**, **01 §5** and **02 §E** apply.
- An LLM Eval does not replace the pipeline integrity gate from **01 §13.1 / 02 §N4 / 03 §17** or the tooling gate from **04 §6**.
- Operational Observability is not the market and strategy monitoring from **01 §19 / 02 §Y**.
- The forecast ledger does not replace the prediction list of **01 §12.1 / 02 §J** nor independent validation.

The words **MUST**, **DO NOT**, and **SHOULD** are normative. If a mandatory field is technically not available, it is not invented or silently left empty; it is logged with **UNAVAILABLE**, a reason, and its impact. A missing mandatory value can lead to **PARTIAL**, **BLOCKED**, or **FAILED**, depending on the effect.

## 1.1 Technical enforcement boundary

Normative prose is a code of conduct, not a technical proof. An agent can declare a status incorrectly. Only properties that test a named schema, a deterministic test or a CI/Eval gate are automatically loadable. Human review and independent evidence testing remain necessary for semantic accuracy.

An `PROTOCOL_SMOKE` only checks adapter contract, scorer and regression detection. Only a blindly produced `LIVE_AGENT` run may carry a model, prompt or agent release.

## 1.2 Operational details are not a user response

The technical terms of this document are intended for internal implementation and auditability. They are not output to the user without request as a progress report or final report. In particular, run IDs, hashes, adapter design, function and test names, import decisions, schema fields, CI steps and telemetry are only relevant to the user if they change the research result, an actual risk or an upcoming decision.

The visible answer follows **00 §1.2**: result and meaning first, general explanation, concrete decision consequences and technical details only on request. A technical error is therefore not only reported with error code or component name, but with its practical consequence: What could not be determined, what remains reliable and what is needed by the user?

---

# 2. Operational object model and mandatory artifacts

## 2.1 Identities and relationships

Each executable agent run receives a globally unique and immutable **run id** before the first model or tool call. It references at least:

- **research id** and **research version** from **02 §A**,
- the phase processed or the purely operational order,
- **parent run id** if the run was triggered by another run,
- **baseline run id** if a delta or regression is assessed,
- the generated artifact IDs and their hashes.

IDs are opaque keys. They are not subsequently reused or transferred to another object. A correction creates a new revision with **supersedes id**; the old object remains.

## 2.2 Required artifacts

| Artifact | When required | Machine check |
|---|---|---|
| Mechanism catalog | If the versioned generator inventory is extended or published | **schemas/mechanism_catalog.schema.json** |
| Generation run | When the mechanism-catalog producer generates persistent ideas | **schemas/generation_run.schema.json** |
| Search-space register | Before the first data-based entry screen of a candidate family | **schemas/search_space.schema.json** plus semantic validator |
| Noise screen | Before promotion of an observation-driven idea without a permitted waiver | **schemas/noise_screen.schema.json** plus semantic validator |
| Hypothesis intake | For each persistent raw idea before opening a new research case | **schemas/hypothesis_candidate.schema.json** |
| Run manifest | For each run | **schemas/run_manifest.schema.json** |
| Evidence document | As soon as a material claim is created or adopted | **schemas/evidence.schema.json** |
| Review document | Human examination, correction, release, rejection, or override | **schemas/review.schema.json** |
| Constraint/lever assessment | When using one of the four constraint/lever labels | **schemas/constraint_assessment.schema.json** |
| Strategy concept audit | Before completion of any incompletely defined source reconstruction | **schemas/strategy_concept_audit.schema.json** plus semantic inspector |
| Condition inquiry | After preliminary operationalization, when metrics, definition dependence, or unknown success modifiers are examined quantitatively | **schemas/condition_inquiry.schema.json** plus semantic inspector |
| Causal-identification assessment | Before any interventional or counterfactual estimate or causal formulation | **schemas/causal_identification_assessment.schema.json** plus **scripts/inspect_causal_identification.py** |
| Outcome Evidence Contract | before validation is frozen and again when its outcomes are assessed | **schemas/outcome_evidence_contract.schema.json** plus **scripts/validate_outcome_evidence_contract.py** |
| Pipeline Integrity Assessment | after the outcome contract and before validation is frozen | **schemas/pipeline_integrity_assessment.schema.json** plus **scripts/validate_pipeline_integrity_assessment.py** |
| Scientific-philosophy review | After `FALSIFIED / PRECISE_NULL / INCONCLUSIVE / INVALID_TEST`, as soon as a material revision or empirical continuation is considered | **schemas/scientific_philosophy_review.schema.json** plus semantic inspector |
| Orchestration state | Before each material research transition and after each accepted technical contribution, blocker, or user decision | **schemas/orchestration_state.schema.json** plus deterministic router test |
| Routing decision | For each work order derived from an orchestration state | **schemas/routing_decision.schema.json** plus **scripts/route_research_task.py** |
| Research fingerprint | Before each material research step; protects the entire effective research state and the hashes of its documents | **schemas/research_fingerprint.schema.json** |
| Research fingerprint check / amendment proposal | After each material work result and before acceptance | **schemas/research_fingerprint_check.schema.json** plus **scripts/check_research_fingerprint.py** |
| Trace | At each model, tool, retrieval, and validation step | Rules in §6 |
| Error log | When a warning or error occurs | Rules in §7 |
| Delta report | If a baseline run or previous released version exists | Rules in §9 |
| Forecast ledger | For each claim of type **FORECAST** | **schemas/forecast.schema.json** and rules in §10 |
| Eval result | Agent, prompt, model, tool, router, or schema change | **evals/catalog.v1.json** and §11 |
| Multi-agent report | As soon as more than one agent contributes materially | Rules in §12 |

The examples under **examples/** show minimal syntactically valid instances. They are not a release of a real run and are not a substitute for the semantic rules of this document. In particular, the repository does not yet contain a fully completed real research case and therefore does not claim end-to-end practice validation.

A generation run is not a research or release gate. The deterministic producer does not need an LLM run manifest. However, once the optional generator agent or another model generates or materially alters content, that model call is additionally considered an agent run with a run manifest. In both cases, generated candidates remain `INBOX` until the separate intake process handles them.

A scientific-philosophy review is neither a human review nor a new validation result. Its agent must not change the frozen result. Machine testing enforces reference integrity and formal conditions for progressive continuation; whether a claimed prediction is genuinely new remains a semantic test task. The associated inspector is `scripts/inspect_scientific_philosophy_review.py`.

The upstream `strategy_concept_audit` is generated by the same agent contract in a different mode. It is not a test of results. It specifies which conditions belong to the strategy, which only come from the source as an application clue, which are suspected and which remain unknown. The Inspector is `scripts/inspect_strategy_concept_audit.py`.

A `condition_inquiry` is a plan or result of a clearly defined quantitative conditional question. It may assess measurement instruments or generate new condition hypotheses, but does not write data-based findings back into the source strategy. The inspector is `scripts/inspect_condition_inquiry.py`.

## 2.3 Schema and integrity rule

An artifact is only valid if:

1. it is validated against the specified schema version,
2. all referenced IDs exist,
3. all declared hashes match the stored bytes,
4. its time and version reference is clear,
5. no forbidden silent mutation is present.

JSON schema validity is necessary but not sufficient. Formally valid content that is factually incorrect or unconfirmed remains invalid.

The positive and negative schema contract tests have two CI-checked entries: **scripts/test_schemas.py** (platform-neutral) and **scripts/test_schemas.ps1** (PowerShell). **scripts/validate_framework.py** combines schema, producer, scorer, and unit tests; the PowerShell overall check is retained as a second path. A green integrity check does not replace a `LIVE_AGENT` run, semantic artifact check, or human review.

## 2.4 Run status

The run manifest uses only:

- **QUEUED**
- **RUNNING**
- **SUCCEEDED**
- **PARTIAL**
- **FAILED**
- **CANCELLED**

The statuses have the following fixed meanings:

| Status | Meaning |
|---|---|
| QUEUED | Identity and mission exist; substantive execution has not begun. |
| RUNNING | At least one execution step is running or waiting for a permitted dependency. |
| SUCCEEDED | All operational gates applicable to the contract have passed, all mandatory artifacts are finalized, and the substantive status is reproduced truthfully. |
| PARTIAL | Valuable sub-artifacts exist, but at least one failed or still-open operational point prevents a claim of complete execution. |
| FAILED | A hard error, failed mandatory gate, or integrity breach makes the intended result inadmissible. |
| CANCELLED | The run ended before its order was completed; the reason and authorization are logged. |

**SUCCEEDED** does not mean that the research hypothesis has been confirmed. A methodically correctly executed falsification run can be operational **SUCCEEDED** and technical **FALSIFIED** or **FAILED**. Conversely, a method result may not be considered as fully executed if the associated run is only **PARTIAL**.

A terminal run record is not edited. Subsequent findings are appended as a linked delta, review or new run.

---

# 3. Run provenance

## 3.1 Minimum content of the run manifest

The manifest MUST contain the following information groups or identify them with **UNAVAILABLE + reason**:

| Group | Required content |
|---|---|
| Identity | run_id, research_id, research_version, task, phase, status |
| Time | started at and completed at in UTC with RFC-3339 timestamps |
| Lineage |parent run id, baseline run id, supersedes run id, triggering user/process|
| Model | Provider, model name, snapshot/revision, API version |
| Inference | Available parameters such as temperature, top-p, seed, token limit, and reasoning configuration |
| Prompt |Prompt ID, Prompt version, hash of each layer and hash of the actually resolved prompt|
| Context | referenced project rules, files, data states, and their hashes |
| Tools |Allowed and actually used tools, versions, permission profile and relevant configuration|
| Runtime | Operating system, runtime, packages, lockfile/environment hash; additional causal analysis **02 §E9 / 04 §5–8** |
| Inputs |Input IDs, origin, data vintage, as-of-time, content hash|
| Outputs |Artifact ID, path or object reference, media type, schema version and content hash|
| Resources | Model/tool calls, input/output/cache/reasoning tokens where available, duration, retries, costs, currency, and price level |
| Completion | Applicable operational gates, open errors, review, and delta status |

A model alias without a snapshot is not issued as a reproducible snapshot. If the provider snapshot is not available, this is explicitly logged as a restriction.

## 3.2 Prompt and context versioning

System, developer, user and project-specific instructions are separately versioned or hashed. The record stores:

1. the sequence of the instruction layers,
2. the IDs and versions of their sources,
3. the hash of the actually rendered input,
4. all dynamically inserted context artifacts,
5. any reduction, summary or contextual compression.

A material prompt, router or context change is not a retry of the same result, but a new run. The change relationship is recorded via **parent run id** or **supersedes run id**.

## 3.3 Hash and immutability rule

The schemas use SHA-256 as exactly 64 lowercase hexadecimal characters. An additional stronger procedure may be logged in parallel but does not replace the schema-compliant SHA-256 field. Before hashing, the actually stored byte format is clearly defined; for structured data, the canonicalization used is identified. Review documents use the RFC-8785 canonicalization specified in the schema.

A hash:

- does not establish truth,
- does not replace an accessible snapshot,
- shall not be calculated over a normalized content if the stored raw content is different;
- is not overwritten after finalization.

Secrets, access tokens and personal data are not copied to Prompt, Trace or Manifest. At most one secure configuration reference shall be logged; Secrets are also not “anonymized” by easily attackable plaintext hashes.

## 3.4 Retry rule

Each attempt of a model, tool, or retrieval call receives an **attempt** number and its own trace event.

- A technically identical attempt classified as **retryable = true** may be repeated in the same run.
- If prompt, data, model, tool version, permissions or technical parameters change, a new run MUST be created.
- Retry number, backoff and termination threshold are logged before or at the first error.
- A failed attempt is never removed from the trace if a later attempt succeeds.

---

# 4. Epistemic claim types

## 4.1 Orthogonality to the Research Claim Level

The research claim level from **01 §5 / 02 §E1** describes the strength of the professional statement: **ASSOCIATIONAL PREDICTIVE**, **INTERVENTIONAL** or **COUNTERFACTUAL**.

The epistemic claim type of this document, on the other hand, describes how a single statement came about. Both fields are independent and must not be replaced with each other.

Also independent of this is the validation/trading status from **01 §4.3**: `mechanism_supported`, `forward_predictive_oos`, and `executable_net_edge`. Epistemic type, research claim level, and these three statuses are separate dimensions. None may be automatically derived from another.

Each material claim receives exactly one primary type:

| Type | Definition | Minimum requirement | Unauthorised use |
|---|---|---|---|
| SOURCE_FACT |A source claims or documents the content immediately.|Source, location, snapshot/vintage and extracted fact.|Provide interpretation, calculation or forecast as mere source fact.|
| CALCULATED_VALUE |Deterministic result from named inputs.|Formula/code, input claims, version, rounding rule and reproduced result.|Represent uncertain estimate or model output as an exact calculation.|
| ESTIMATE |Measurement or model estimation with uncertainty.|Data, method, assumptions, estimate, uncertainty and relevant gates from 00–04.|Point estimators as a sure fact.|
| INFERENCE |Conclusion that goes beyond the wording of individual sources or inputs.|Explicit premises, final rule, alternative explanation and limits.|Label inference as direct source or causal evidence.|
| FORECAST |Statement frozen before the outcome occurs and later resolvable.|Forecast ledger entry according to §10.|Retrospective statement or forecast adjusted after outcome.|
| HUMAN_JUDGMENT |Evident evaluation or decision made by an identified person.|Review record, person/role, time, reason and scope.|output LLM or automatic rule as human judgment.|

An LLM may propose a human judgment. Until an identified person adopts it in the review system, the statement **INFERENCE**, not **HUMAN JUDGMENT**, remains.

## 4.2 Material claim

A claim is material if it can affect at least one of the following:

- hypothesis, counter-hypothesis or falsification,
- Research gate or final state,
- Claim level, DAG, identification or permitted causal language,
- data role, data vintage or observability,
- effect size, uncertainty, cost or feasibility,
- Forecast, activation, suspension or revalidation,
- material recommendation.

Material claims must not only exist in free prose. You need a **claim id** entry in the Evidence document.

## 4.3 Minimum claim fields

Each material claim contains at least:

- claim id and claim revision,
- run id, research id and research version,
- unambiguous claim text,
- epistemic type,
- time scope and as-of-time,
- origin **MODEL / TOOL / HUMAN / IMPORTED**,
- evidence refs and, where applicable, input claim refs,
- relation to hypothesis, gate, decision or forecast,
- evidence grade according to §5,
- Status and, if applicable, supersedes claim id.

A textual clarification that changes the scope, direction, number, period, population or causal status is a new claim revision.

---

# 5. Evidence chain, source testing, and deterministic evidence grades

## 5.1 Binding chain

For each material claim, the following chain MUST be completely reconstructable:

**Source → reference → extracted fact → transformation or conclusion → claim → affected hypothesis/gate/decision**

Unneeded intermediate steps are explicitly omitted; They are not fabricated. A **SOURCE FACT** typically has no transformation. A **CALCULATED VALUE** MUST show its transformation and input claims.

Each node has a stable ID. References may be:

- do not point to nonexistent nodes,
- do not create cycles,
- are not backdated to evidence after the claim,
- not be silently bent by a later revision.

## 5.2 Source and reference artifact

For each external or internal source, at least the following shall be recorded:

- source_id,
- title/name, author or publisher,
- source type and primary/secondary status,
- URL, document path or record reference,
- time of release, version and retrieval;
- data vintage and as-of-time, where relevant,
- Content hash or reasoned **UNAVAILABLE**,
- precise reference such as page, section, table, line, timestamp or record key,
- sufficiently narrowly extracted fact,
- Access and license restriction.

Search result, snippet, LLM summary or unopened citations are not considered verified sources.

## 5.3 Source verification protocol

An evidence reference is **qualified**, only if all applicable exams have been passed:

1. **Identity:** Author, publisher, document and version are unique.
2. **Retrieve:** The source actually used was opened or provided as an immutable snapshot.
3. **Find:** The locator leads to the claimed passage, number or data line.
4. **Entailment:** The source carries the extracted fact; it is not distorted by omission, change of sign or loss of context.
5. **Time reference:** Date, as-of-time, data vintage and revision status match the claim.
6. **Independence:** Sources counted as confirmation are not based solely on the same unchecked source of origin.
7. **Conflict review:** Material counter-evidence is sought or known contradictions are disclosed.

The test logs the examiner, time, method and result per step. A mere “citation present” is not a passed entailment test.

In the Evidence document, the applicable check steps are logged under **evidence assessment.checks** with **PASS / FAIL / NOT APPLICABLE**. **extraction method** and **human verified** are not omitted. A sole LLM extraction with **human verified = false** is not qualified unless an independent deterministic entailment/locator check has passed all applicable criteria.

In the case of time-varying facts, the source for the claimed as-of-time MUST be current enough. A correct page today does not automatically prove the historical information status. For revisable data, the vintage rule from **00 §8 / 01 §5.7 and §7.3 / 02 §E6 and §G5** applies.

## 5.4 Academic source governance

### 5.4.1 Applicability and principle

For any source with **source type = ACADEMIC**, **academic metadata** is mandatory according to **schemas/evidence.schema.json**. The academic source remains additionally subject to the general rules of §5.1–§5.3.

Academic publication status, journal name, citation number, arXiv category or journal prestige are no method gates and no guarantee of quality. In particular, they shall not replace:

- Identification and claim level from **01 §5**,
- the design-specific methods from **03**,
- reproducibility and tooling from **04**,
- Entailment, version fidelity and evidence chain from this document.

### 5.4.2 work id, versions and deduplication

**work id** refers to the intellectual family of works across Preprint, Working Paper, Accepted Manuscript, Version of Record, Erratum and other versions. Each specific version used remains its own **source id** dataset with its own URI, release/retrieval time, **version or vintage** and **snapshot hash**.

Before adopting an academic source, deduplicate it:

1. exact DOI match,
2. exact arXiv ID comparison without version suffix,
3. normalized title, author, and year comparison,
4. review of journal reference, DOI and repository metadata,
5. if uncertainty remains, compare abstracts, data, tables, and key results.

Decisions **SAME WORK / DISTINCT WORK / UNCERTAIN** are logged with reason and examiner.

- **SAME WORK:** same work id; Versions never count as independent confirmation.
- **DISTINCT WORK:** separate work id; Independence is additionally checked and not derived from the ID alone.
- **UNCERTAIN:** Sources may not be aggregated as independent confirmation until clarification; a decision-making claim is at most LIMITED.

An arXiv preprint and its later journal article are thus managed as a family of works. Two databases that index the same article are also not two sources.

The version relevant for a claim is explicitly selected:

- For a historical information status, the exact version available at that time applies.
- For a current statement of fact, the most recent verified, non-retracted version shall apply; in the case of a correction, the corrected version.
- An older version remains citable when its historical statement is examined. It must not silently represent the current version.

Title or author changes do not automatically force a new work id. A demonstrably different research object, nuclear hypothesis or separate study, on the other hand, receives a new work id, even if authors place it in the same repository family.

### 5.4.3 Targeted Finance Source Search without Prestige Gate

For relevant financial-economics questions, search **The Journal of Finance** and the **Journal of Financial Economics** for original works, corrections, replications, and associated code/data notes. The search status per venue is:

- **SEARCHED_HIT**
- **SEARCHED_NO_HIT**
- **NOT RELEVANT + justification**
- **BLOCKED + reason**

This targeted search is a coverage rule, not an exclusion filter. Relevant original works from other journals, working paper series, repositories or subject areas are not devalued or omitted because of the venue. Conversely, a claim does not receive a higher evidence grade simply because it has appeared in Journal of Finance or Journal of Financial Economics.

### 5.4.4 Publication status, DOI, Venue and arXiv

The field **publication status** only uses:

- **PEER_REVIEWED_VERSION_OF_RECORD**
- **ACCEPTED_MANUSCRIPT**
- **WORKING_PAPER**
- **PREPRINT**
- **OTHER**

**PEER REVIEWED VERSION OF RECORD** is only permitted if the specific version has been verified as a version of record on a publisher/journal page or via consistent DOI metadata. **ACCEPTED MANUSCRIPT** requires a verified acceptance status and a venue. Author statements such as “submitted” or “under review” are not upgraded to **ACCEPTED MANUSCRIPT**.

For DOI and Venue:

- Save DOI without prefix representation and additionally resolve via **https://doi.org/**.
- Compare DOI, title, author, venue and version between publisher, DOI metadata and repository.
- DOI comparisons are case-insensitive; the delivered original spelling may be retained.
- A solvable DOI proves neither peer review nor methodological quality.
- A journal reference or DOI field at arXiv is checked against publisher/DOI metadata before the publication status is changed.
- Lack of DOI is not an automatic quality defect; The specific version still requires a stable source id, URI and a snapshot hash.

For arXiv at least:

- arXiv-ID without version suffix,
- exact version number,
- submitted at and updated at,
- primary category,
- URI or snapshot of this version,
- current withdrawal and version history.

The allowed q-fin categories correspond to the official arXiv taxonomy:

| Category | Scope |
|---|---|
| q-fin.CP | Computational Finance |
| q-fin.EC | economics; alias of econ.GN |
| q-fin.GN | General Finance |
| q-fin.MF | Mathematical Finance |
| q-fin.PM | Portfolio Management |
| q-fin.PR | Pricing of Securities |
| q-fin.RM | Risk Management |
| q-fin.ST | Statistical Finance |
| q-fin.TR | Trading and Market Microstructure |

The category is a subject classification, not a peer review or quality status. Cross-listings are additional discovery metadata and do not increase the evidence grade.

For a decision-making arXiv claim, the citation MUST reference the specific version, such as **arXiv:YYMM.NNNNv2**. The versionless abstract URL regularly shows the latest version and is therefore not sufficient as an immutable proof. Each arXiv replacement or Withdrawal generates a new version dataset and a delta check.

### 5.4.5 Integrity, correction and retraction check

Before the first decision-making use, immediately before Freeze, before external release and upon revalidation, the integrity status is checked again. Prioritized test routes are:

1. Publisher/Journal site including Corrigenda, Errata and Retraction Notices,
2. Crossmark or DOI metadata and update relations,
3. Crossref retraction watch data;
4. Repository versions, comments and Withdrawal history,
5. Documented manual testing.

**check method** uses **PUBLISHER / CROSSMARK / DOI METADATA / REPOSITORY / MANUAL**. **integrity.status** used:

- **NO_NOTICE_FOUND**
- **CORRECTED**
- **EXPRESSION_OF_CONCERN**
- **RETRACTED**
- **WITHDRAWN**
- **UNKNOWN**

For **CORRECTED**, **EXPRESSION OF CONCERN**, **RETRACTED**, or **WITHDRAWN**, **notice uri** is mandatory. **NO NOTICE FOUND** only means that no indication was found through the documented routes; it is not a guarantee that the source is free of scientific error.

Corrections are classified as material or non-material for the specific claim:

- Purely typographically and without influence on the claim → NON MATERIAL, but log.
- Change to data, code, formula, table, direction, size, significance, interpretation or identification → at least MATERIAL.
- Revocation or correction that makes a decision-making claim unusable → BREAKING.

A withdrawn article may serve as a historical source about the withdrawal itself. It may no longer be used as a positive sole support of the withdrawn claim of fact.

### 5.4.6 Code, data and replication

**code availability** and **data availability**

- **OPEN**
- **PARTIAL**
- **RESTRICTED**
- **NOT_AVAILABLE**
- **NOT_STATED**
- **NOT_CHECKED**

For **OPEN**, **PARTIAL** or **RESTRICTED**, the specific URIs are stored. Additionally, where available, repository commit/release, license, environment, data vintage, and content hashes are logged.

The independent replication test uses:

- **REPLICATED**
- **PARTIALLY_REPLICATED**
- **FAILED_TO_REPLICATE**
- **CONFLICTING**
- **NO_INDEPENDENT_REPLICATION_FOUND**
- **NOT_ASSESSED**

A positive replication status requires at least one source id of an actually separate replication work. A new edition, a supplement or a reanalysis of the same work family does not count as independent replication. Author, data, code and design overlaps are disclosed.

Code or data availability is not proof of quality. Successful technical reproduction initially only confirms that a specified result could be recreated under the recorded environment. It proves neither identification nor external validity nor trading benefits.

Conversely, lack of openness is not automatically falsification. However, in the case of a decision-making empirical or computationally intensive estimate that cannot be tested either by code/data or by independent replication, the evidence grade is at most LIMITED. If a central number claim is not at all traceable and the only support of the decision, INSUFFICIENT applies.

### 5.4.7 Academic-evidence consequences

The rules complement the evidence rule set from §5.6:

| Finding | Required consequence |
|---|---|
| Same work id in multiple versions or indices | Exactly one work family; do not count as independent multiple confirmation. |
| PREPRINT, WORKING PAPER, or OTHER as the sole positive support of a substantial claim | Maximum LIMITED; explicitly identify the source as not peer-reviewed or provisional. |
|SOURCE FACT only correctly asserts what the exact provisional version cited says|May be SUFFICIENT with full version/reference check; the underlying substantial claim does not automatically become SUFFICIENT.|
|PEER REVIEWED VERSION OF RECORD or ACCEPTED MANUSCRIPT|No automatic upgrade; all general and methodological SUFFICIENT rules remain necessary.|
|EXPRESSION OF CONCERN or UNKNOWN for decision-making source|At most LIMITED; as the sole supporting evidence INSUFFICIENT.|
|RETRACTED or WITHDRAWN|Positive support for content INSUFFICIENT; Create errors and breaking delta.|
| Materially CORRECTED | Affected claims are at most LIMITED until the corrected version is checked; if the result is incompatible, INSUFFICIENT. |
|FAILED TO REPLICATE or CONFLICTING with material relevance|Conflict record; decision-making claim until resolution INSUFFICIENT.|
|NO INDEPENDENT REPLICATION FOUND or NOT ASSESSED|No automatic withdrawal unless replication is claimed as a necessary support; Keep the status visible.|
| REPLICATED |May strengthen evidence, but not determine claim level, identification and degrees alone.|

Journal name and q-fin category do not appear as a positive factor in any grade rule.

### 5.4.8 Academic-source deltas

At least MATERIAL are:

- new or removed version of a work id used,
- new arXiv version,
- change of publication status,
- newly verified DOI or other venue,
- new correction, expression of concern or replication,
- change in code/data availability,
- deduplication that changes the number of independent sources.

BREAKING are:

- Retraction or Withdrawal of a decision-making source,
- material correction that cancels a supporting claim,
- failed or conflicting replication that invalidates the single supporting evidence,
- Evidence that supposedly independent confirmations were only versions of the same work id and thus a SUFFICIENT criterion is eliminated.

Each sequence is processed via §9. Historical claims and decisions are not overwritten; they receive a delta, review, and, if applicable, a new research version.

### 5.4.9 Official test references

Relevant registry and status references are:

- [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy)
- [arXiv Version Availability](https://info.arxiv.org/help/versions.html)
- [arXiv Withdraw / Retract a Submission](https://info.arxiv.org/help/withdraw.html)
- [DOI Handbook](https://www.doi.org/doi-handbook/html/)
- [Crossref Crossmark](https://www.crossref.org/documentation/crossmark/)
- [Crossref Retraction Watch](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/)
- [Journal of Finance – official AFA page](https://afajof.org/journal-of-finance/)
- [Journal of Finance – Corrigenda and Errata](https://afajof.org/clarifications/)
- [Journal of Finance – Replications and Comments](https://afajof.org/comments-and-rejoinders/)
- [Journal of Financial Economics – publisher page](https://www.sciencedirect.com/journal/journal-of-financial-economics)

Registry metadata is used as hints and links. If there is an objection, the specific notice or publisher/repository version must be secured and the conflict must be disclosed.

## 5.5 Reproducible transformations

A logged transformation contains:

- transform_id,
- formula or code/notebook/query hash,
- runtime and relevant package versions,
- ordered input IDs and input hashes,
- parameters, units, missing-value, and rounding rules,
- output and output hash,
- reproduction status and tolerance.

A manually copied value without a verifiable transformation is not a **CALCULATED VALUE**. If the method is stochastic or model-based, the output is generally treated as **ESTIMATE**, provided it is not only a deterministic post-processing of an already indicated estimate.

## 5.6 Evidence grade as the only confidence class

Only the following evidence grades are used:

- **SUFFICIENT**
- **LIMITED**
- **INSUFFICIENT**

The LLM must not invent a subjective confidence percentage. The evidence grade is the only operational trust classification. It evaluates the traceability and documentary support of the claim, not its scientific truth, causality, or economic relevance automatically.

For this document version, **evidence assessment.ruleset version = 1.1.0**. Any change to the grade rules requires a new ruleset version and a MATERIAL delta.

Apply the grade in this order:

1. If a **INSUFFICIENT** condition applies, the grade is **INSUFFICIENT**.
2. Otherwise, if all type-dependent **SUFFICIENT** conditions are met, the grade is **SUFFICIENT**.
3. Otherwise the grade is **LIMITED**.

### Mandatory INSUFFICIENT

Any of the following conditions requires **INSUFFICIENT**:

- missing or circular evidence chain,
- invented, untraceable or non-defeatable citation,
- material conflict with status **OPEN** or **ACCEPTED UNCERTAINTY**,
- missing data vintage for a vintage-sensitive claim,
- hash, unit, sign or reproduction errors,
- damaged applicable gate from 00–04,
- open critical errors or relevant open errors without limitable scope,
- statement subsequently issued as a forecast,
- statement issued as **HUMAN JUDGMENT** without authenticated human review,
- Violation of a mandatory academic evidence sequence from §5.4.7.

### Type-dependent SUFFICIENT

| Type | All conditions for SUFFICIENT |
|---|---|
| SOURCE_FACT | At least one qualified primary or authoritative evidence reference or two qualified independent secondary sources; correct time reference; no unresolved material counter-evidence; for academic sources, additionally §5.4. |
| CALCULATED_VALUE | All material input claims are SUFFICIENT; the transformation is fully versioned; reproduction is consistent within the pre-declared tolerance. |
| ESTIMATE | Input and data origin are SUFFICIENT; method, assumptions, estimate, and uncertainty are complete; all applicable methodological and tooling gates from 00–04 are passed or explicitly not required; the result is reproduced; academic support meets §5.4. |
| INFERENCE | All key premises are SUFFICIENT; the final rule and limits of application are explicit; at least one specific alternative explanation or counter-evidence has been addressed; there is no unexplained logical jump. |
| FORECAST | Entry was issued immutably before the outcome; target, horizon, unit, and resolution rule are complete; all key input claims are SUFFICIENT. The grade evaluates quality at issuance, not the later hit. |
| HUMAN_JUDGMENT | Identified human reviewer, role, time, reason, scope, previous value/new value, and evidence references are complete; the judgment is not used as a substitute for missing evidence or a failed research gate. |

### LIMITED

**LIMITED** is allowed only if the chain is real and traceable, no mandatory **INSUFFICIENT** condition applies, and at least one non-critical SUFFICIENT condition is missing. State the limitation for the specific field.

A **LIMITED** claim may be reported as an open hypothesis or marked limitation. It may not, on its own, carry any **PASS**, activation, causal claim, or external recommendation for action.

## 5.7 Aggregation and decision rule

Evidence grades are not averaged. For a decision, the weakest decision-making claim applies.

- All decision-making claims **SUFFICIENT** → operational evidence review can be **PASS**.
- At least one decision-making claim **LIMITED** → operational evidence check **BLOCKED**.
- At least one decision-making claim **INSUFFICIENT** → operational evidence check **FAIL**.

Non-decisional **LIMITED** or **INSUFFICIENT** claims are only preserved if they are visibly marked as uncertainty, counter-hypothesis or discarded statement.

---

# 6. Observability

## 6.1 Append-only trace

Each run has an append-only trace with:

- run_id,
- monotonically increasing sequence_no,
- event_id,
- event_type,
- timestamp in UTC,
- span id and optionally parent span id,
- actor and component,
- input and output references including hash,
- status, duration and attachment,
- error reference,
- resource consumption.

At least the following types of events shall be recorded:

- **RUN_CREATED**
- **RUN_STARTED**
- **MODEL_CALL_STARTED / MODEL_CALL_FINISHED**
- **TOOL_CALL_STARTED / TOOL_CALL_FINISHED**
- **SOURCE_RETRIEVAL**
- **SOURCE_VERIFICATION**
- **CLAIM_RECORDED**
- **TRANSFORM_EXECUTED**
- **SCHEMA_VALIDATION**
- **EVAL_EXECUTED**
- **REVIEW_RECORDED**
- **DELTA_CLASSIFIED**
- **FORECAST_ISSUED / FORECAST_RESOLVED**
- **RUN_FINISHED**

Failed and aborted calls remain visible. A trace must not be subsequently corrected in such a way that failed attempts, retries or warnings disappear.

## 6.2 Tool and model telemetry

Each call shall be recorded, where available:

- Tool/model name and exact version,
- operation or endpoint,
- start, end and duration,
- Request-/Response-Hash,
- status code or result status,
- Retryability and Attempt
- input, output, cache and reasoning tokens;
- cost amount, currency and price version,
- Rate limit, timeout and warning information.

Unavailable readings are marked as **UNAVAILABLE**. They are neither equated nor estimated with zero unless the estimate is expressly marked as such and their formula is stored.

## 6.3 Minimum operational metrics

For each run, at least:

- total duration and duration per phase/step,
- number of model, tool, and retrieval calls,
- errors and retries according to stage and code,
- token and cost consumption,
- number of claims per type and evidence grade,
- source verification rate,
- open reviews and deltas,
- Eval and Gate results.

These metrics serve diagnosis and cost control. They are not evidence of a market edge.

---

# 7. Error taxonomy and error handling

## 7.1 Required fields

Each error receives:

- error_id,
- run id and affected span id,
- **stage**,
- stable **code**,
- Severity **WARNING / ERROR / CRITICAL**,
- retryable **true / false**,
- time and artifacts/claims concerned,
- observed symptom and proven cause, if known,
- Effect on results, evidence grade and gates,
- retry/mitigation action,
- Status **OPEN / MITIGATED / RESOLVED / ACCEPTED_RISK**,
- Resolver or human risk owner.

**ACCEPTED RISK** is only allowed by a human review and does not convert an error into success or **INSUFFICIENT** into **SUFFICIENT**.

## 7.2 Stages and standard codes

The stage uses exclusively:

- **INITIALIZATION**
- **PROMPTING**
- **MODEL**
- **TOOL**
- **RETRIEVAL**
- **VALIDATION**
- **PERSISTENCE**
- **FINALIZATION**

The following codes form the mandatory core vocabulary; Project-specific extensions are versioned and namespaced:

| Stage | Core codes |
|---|---|
| INITIALIZATION | INIT_CONFIG_INVALID, INIT_DEPENDENCY_MISSING, INIT_PERMISSION_DENIED |
| PROMPTING | PROMPT_VERSION_MISSING, PROMPT_RENDER_FAILED, PROMPT_CONTEXT_OVERFLOW, PROMPT_CONTEXT_TRUNCATED |
| MODEL | MODEL_UNAVAILABLE, MODEL_TIMEOUT, MODEL_REFUSAL, MODEL_OUTPUT_INVALID, MODEL_INSTRUCTION_VIOLATION |
| TOOL | TOOL_UNAVAILABLE, TOOL_TIMEOUT, TOOL_API_ERROR, TOOL_OUTPUT_INVALID, TOOL_VERSION_DRIFT |
| RETRIEVAL | SOURCE_UNREACHABLE, SOURCE_AUTH_FAILED, SOURCE_LOCATOR_MISMATCH, SOURCE_STALE, SOURCE_CONTRADICTION, CITATION_NOT_ENTAILED, ACADEMIC_VERSION_UNRESOLVED, INTEGRITY_NOTICE_FOUND |
| VALIDATION |SCHEMA INVALID, REFERENCE DANGLING, HASH MISMATCH, CALCULATION MISMATCH, EVIDENCE INSUFFICIENT, METHOD GATE VIOLATION, EVAL REGRESSION, MULTI AGENT CONFLICT, FORECAST PROTOCOL VIOLATION, POLICY VIOLATION, ACADEMIC DUPLICATE COUNTED, REPLICATION CONFLICT|
| PERSISTENCE | WRITE_FAILED, ARTIFACT_MISSING, IMMUTABILITY_VIOLATION |
| FINALIZATION | MANIFEST_INCOMPLETE, OPEN_CRITICAL_ERROR, REVIEW_REQUIRED, DELTA_UNRESOLVED |

## 7.3 Severity and running efficiency

| Severity | Required effect |
|---|---|
| WARNING |Run may continue; Impact and scope are called. An affected claim is at most LIMITED until the warning is demonstrably without consequences or solved.|
| ERROR |The affected step is not successful. Stop dependent steps; the run ends at least PARTIAL, at mandatory step FAILED.|
| CRITICAL |Immediately stop all dependent steps. Decision-making outputs are not permitted; terminal status FAILED.|

An unknown cause is logged as such. It must not be replaced by a plausible narrative.

## 7.4 Retry and Recovery

- Only **retryable = true** allows an automatic retry.
- A retry repeats the same operation with the same technical inputs.
- Every retry remains in the trace.
- After reaching the predetermined limit, the error is openly escalated.
- Fallbacks that change model, data source, prompt, method, or tool create a new run and delta.
- A fallback must not render invisible a lower quality of evidence.

---

# 8. Human Review, Correction and Override

## 8.1 Review actions and status

A review document is used as **action** exclusively:

- **CORRECTION**
- **OVERRIDE**
- **APPROVAL**
- **REJECTION**
- **ANNOTATION**

The review status is:

- **PROPOSED**
- **APPROVED**
- **REJECTED**
- **APPLIED**
- **SUPERSEDED**
- **WITHDRAWN**

The audit trail uses:

- **CREATED**
- **APPROVED**
- **REJECTED**
- **APPLIED**
- **SUPERSEDED**
- **WITHDRAWN**
- **COMMENTED**

## 8.2 Immutable Review Layer

A review never edits the original run, claim or tooloutput. It generates a new, signed or authenticated layer with:

- review id and audit events,
- Reviewer identity and role,
- timestamps,
- scope and affected object IDs,
- action and status,
- old and proposed/new value,
- reason code and free text justification,
- evidence and error references,
- validity period or review trigger,
- second reviewer, if required by project rule.

The derived current view is calculated from original plus applied reviews. Original values remain testable.

**before hash**, **after hash**, **record hash**, **event hash**, and **previous event hash** are schema-compliant SHA-256 values. **record hash** seals the RFC-8785-canonicalized immutable core fields; **status** and the append-only **audit trail** are updated according to the hash-chain logic defined in the review schema.

## 8.3 Difference Between Correction and Override

- **CORRECTION** fixes a detectable transmission, calculation, reference or classification error. Proof of correction is mandatory.
- **OVERRIDE** is a deliberately deviant human decision. It is listed as **HUMAN JUDGMENT** and may not relabel the underlying evidence or the methodical gate status.

In particular, an override must not:

- **FAIL** or **BLOCKED** in **PASS**
- declare a **LIMITED** or **INSUFFICIENT** claim to **SUFFICIENT**,
- make used validation data independent again,
- a subsequent hypothesis revision as an original forecast,
- retroactively issue an LLM judgment as human.

Material research changes follow **00 §9 and §16**, **01 §14 and §21** as well as **02 §O, §P and §Z**: new research version, correct data roles and new run.

## 8.4 Mandatory human-review gate

An identified person MUST check:

- every OVERRIDE,
- every decision-bearing HUMAN_JUDGMENT claim,
- any release despite accepted risk,
- any MATERIAL or BREAKING delta with an external or activation effect,
- any update of the Eval baseline;
- any external release of the states VALIDATED PHENOMENON, ACTIVE STRATEGY CANDIDATE, ACTIVE, REVALIDATED or SUSPENDED.

This review is an additional operational release gate. It does not retroactively decide the professional research gate.

An AI agent must neither simulate human identity nor release its own result as a human review.

---

# 9. Delta Detection

## 9.1 Baseline

Each comparative run names exactly one baseline:

1. prefers the last human released run of the same Research version,
2. otherwise an expressly named baseline run,
3. If both are missing, the delta class is **UNKNOWN**.

Baseline and current run are compared via canonicalized run records, artifact hashes and stable claim IDs.

## 9.2 Comparison dimensions

The delta report shall include at least:

- Research, hypothesis, DAG, estimand, tooling and cost model version,
- data sources, vintages, roles and input hashes,
- academic work ids, concrete versions, DOI/Venue, publication and integrity status, code/data availability and replication status,
- Model, snapshot, prompt, context, tools and runtime,
- Claims, Claim Types, Evidence Grades and Evidence Chains
- gate, review and end status,
- Forecasts and forecast resolutions,
- Duration, costs and error patterns.

## 9.3 Delta classes

| Class | Rule |
|---|---|
| NONE |All compared semantic and operational fields as well as relevant hashes are identical.|
| NON_MATERIAL |Only representation, additional telemetry, cost/latency or a demonstrably non-semantic metadata correction will change.|
| MATERIAL |Inputs, model/prompt/tool/runtime, a material claim, evidence grade, forecast, review, academic source metadata or result changes without a breaking condition already being present.|
| BREAKING |A previously decision-making claim is INSUFFICIENT or materially refuted; a PASS becomes FAIL/BLOCKED; a source is withdrawn or materially corrected; an alleged independent confirmation collapses through work id deduplication; Integrity breaks; or a frozen tangible design field changes without the need for a new research version.|
| UNKNOWN |Comparison is not reliable due to lack of baseline, hashes, lineage or non-interpretable schema difference.|

A consistent final conclusion does not automatically make a model, prompt, data or tool change **NON MATERIAL**.

## 9.4 Gate consequences

- **NONE / NON_MATERIAL:** The delta is logged; automatic release is allowed only if all other gates are PASS.
- **MATERIAL:** relevant Evals according to §11 and for external/activation effects Human Review according to §8 are mandatory.
- **BREAKING:** operational release is blocked; dependent artifacts are marked as needing review. The research results are based on 00–04.
- **UNKNOWN:** no automatic release; status is at least BLOCKED until comparison is possible or the missing baseline is accepted with human justification.

The delta detector must not delete or rewrite existing artifacts. It creates a new report.

---

# 10. Forecast Ledger

## 10.1 Scope boundary

The prediction list in **01 §12.1 / 02 §J** describes expected consequences of a hypothesis. As soon as such a statement is observable and assessable in the future, it is additionally frozen in the append-only forecast ledger before the outcome.

## 10.2 Mandatory fields at issue

Each forecast contains:

- forecast id, claim id, run id, research id and hypothesis reference,
- issued at and as of,
- target object, target variable, unit and population,
- horizon, deadline and permitted observation window,
- direction, point value, interval or category,
- evidence level and evidence grade at issue,
- resolution source, precise resolution rule and planned resolution time,
- scoring rule if an indicator is used,
- status **OPEN**.

Probabilities are allowed only if they come from a named, versioned, and calibrated model or documented reference class. A fictitious LLM percentage is inadmissible. Without robust calibration, use a categorical, directional, or interval-based forecast.

## 10.3 Immutability and revision

After **issued at**, Forecast Text, Target, Horizon and Resolution Rule are not changed. A correction creates a new forecast with **supersedes forecast id**; the old one remains open or is completed with a justified status **VOID**.

A forecast shall not be backdated after the start of its outcome window. A breach is **FORECAST PROTOCOL VIOLATION**, Evidence Grade **INSUFFICIENT** and operational release **FAIL**.

## 10.4 Resolution

Allowed status is:

- **OPEN**
- **RESOLVED**
- **UNRESOLVED**
- **EXPIRED**
- **VOID**

With resolution, actual value, source, vintage, resolver, resolved at, applied rule and score are added. If the outcome is not clear or the source is not qualified, **UNRESOLVED** will be awarded instead of hits or errors.

Ambiguous resolutions require Human Review. A later outcome must not change the original forecast or its evidence grade at output.

## 10.5 Evaluation

Forecasts are only aggregated within predefined, comparable families. At least:

- number of issued, resolved and non-resolvable forecasts,
- Coverage,
- For probabilistic forecasts, a property score or a predefined property score;
- for point/interval forecasts, predefined error and coverage measures,
- for direction forecasts hit rate plus matching zero reference,
- Results by horizon and forecast family.

Subsequent selection of only successful forecasts is not permitted.

---

# 11. Controlled Improvement Loop and Agent Evals

## 11.1 Scope boundary

The agent evals check whether changes to the LLM system deteriorate the operational quality. They are separated from the statistical pipeline integrity check from **01 §13.1 / 02 §N4 / 03 §17**.

Binding artifacts are:

- **evals/catalog.v1.json** with **schema version = eval-catalog.v1**,
- **evals/examples/smoke-results.v1.json** with **schema version = eval-results.v2** and **run kind = PROTOCOL_SMOKE**,
- **evals/baseline.v1.json** with **schema version = eval-baseline.v1**,
- **evals/produce_results.py** as a blind producer for subprocess or JSON/HTTP agent adapters,
- **evals/run_evals.py**,
- **evals/tests/test_run_evals.py** and **evals/tests/test_produce_results.py**,
- **evals/README.md**.

## 11.2 Binding procedure

Each improvement follows exactly this order:

1. **Record errors:** secure error, claim, trace, and run references.
2. **Test case before change:** include a minimal reproducible case or generalized expectation in the eval catalogue.
3. **Produce and measure baseline:** run the unchanged system via the blind producer on the same frozen catalogue; expectations are not handed to the agent.
4. **Versioned change:** name the prompt, model, tool, router, schema, or code change uniquely.
5. **Produce and measure candidate:** use the same cases and boundary conditions; only the intended change may differ.
6. **Regression gate:** check structure, minimum values, and baseline policy.
7. **Human review:** review the result, risks, scope, and rollback.
8. **Release and monitoring:** deliberately update the baseline, roll out the change, and observe deltas.

An agent may not directly modify its own configuration, remove evals, lower thresholds, or overwrite baselines just to pass a run.

## 11.3 Mandatory metrics and minimum values

| Metric | Minimum value |
|---|---:|
| overall_score | 0.95 |
| critical_assertion_pass_rate | 1.00 |
| citation_accuracy | 0.95 |
| epistemic_classification_accuracy | 0.95 |
| unknown_safety_rate | 1.00 |
| contradiction_handling_rate | 1.00 |
| source_freshness_rate | 1.00 |
| calculation_accuracy | 1.00 |
| thesis_governance_accuracy | 1.00 |
| academic_source_governance_accuracy | 1.00 |
| hypothesis_intake_accuracy | 1.00 |
| scientific_philosophy_accuracy | 1.00 |
| research_orchestration_accuracy | 1.00 |

In addition:

- **max_metric_drop = 0**
- **max_case_drop = 0**

An improvement in the overall score does not compensate for a decrease in a single mandatory metric or a single case.

## 11.4 Producer, Runner and Release Rules

The producer calls exactly one configured agent adapter for each catalog case and creates `eval-results.v2`. The request contains case input and output contract, but no `expected.assertions`. It supports a local subprocess without a shell and an HTTPS-JSON endpoint. Adapter ID, Run type, time and configuration hash are stored in the result.

The runner uses:

- Exit **0**: Structure and quality/regression gates passed,
- Exit **1**: quality or regression errors,
- Exit **2**: hard structure/configuration error.

Only Exit 0 can create an Eval-Gate **PASS**. Exit 1 or 2 blocks the release of the change.

This rule has two stages:

- `PROTOCOL_SMOKE + Exit 0` means only **FRAMEWORK INTEGRITY PASS**.
- For a model, prompt, or agent release, the runner must also be run with
  `--require-run-kind LIVE_AGENT`. A smoke fixture fails this release gate even
  with a score of 1.000.

GitHub Actions performs platform-neutral and PowerShell integrity checks on
push and pull request. The live-agent workflow is manual and requires a
configured adapter endpoint; without it, there is no live-quality claim.

The baseline is updated only after documented human **APPROVAL**. Eval cases
that were directly known during training or modification are marked as
development evals; a separate protected holdout remains necessary as soon as
systematic optimization begins.

## 11.5 Rollback

Each released change shall include:

- previous released version,
- rollback triggers;
- executable return path,
- affected artifacts,
- Owner.

A rollback does not delete failed runs or deltas.

---

# 12. Multi-agent gate

## 12.0 Research conductor and router

Once the task contains a research artifact transition, the coordinator has the contract `agents/research-conductor.md`. Before a delegation, its current `routing_decision` must state the specialist agent, the mode and the limited work order. A child agent is not allowed by the fact that he could fit thematically.

The coordinator passes only the inputs allowed in the work order. The child agent does not speak directly to the user, does not change the overall order, and returns the result to the coordinator. Only after schema and semantic testing may this result enter the next `orchestration_state`. It is then routed again; the child agent must not begin a self-elected delegation chain.

Each material step of an existing research case carries the reference and verified checksum of the full research fingerprint. It protects research question and source strategy as well as operationalizations, parameters, lookbacks, triggers, outcomes, conditions, filters, exclusions, data and sample roles, evaluation rules, costs, execution, risk, frozen results, follow-up decisions and the checksums of all effective documents.

Before accepting a result, `scripts/check_research_fingerprint.py` produces a complete comparison. Only `UNCHANGED` allows acceptance. Each deviation is stored with its exact paths as `CHANGE_PROPOSED`. The previous fingerprint remains effective, the changed result is not accepted and the coordinator explains the practical meaning to the user. Even an approved change does not overwrite anything: it creates a new Research ID or Research version.

This rule also applies to material work performed by the coordinator, not only to child agents. Idea generation without an existing research status receives transparent `NOT_COMPARABLE_NEW_RESEARCH` and creates the first fingerprint only in the intake per candidate.

Mandatory specialist routes are in particular:

- `scientific-philosophy-critic / PRE_OPERATIONALIZATION` after the
reconstruction of an incomplete prose strategy and before its operationalization,
- `condition-inquiry-analyst` for utility, definition sensitivity or
unknown observable success modifiers after a preliminary operationalization,
- `scientific-philosophy-critic / POST_RESULT` for attribution, revision or
continued after a frozen non-positive result,
- `causal-identification-critic / PRE_ESTIMATION` as soon as
`INTERVENTIONAL`- or `COUNTERFACTUAL`-claim is intended and no accepted identification assessment has yet been made; expressly not in a purely predictive question,
- `intraday-hypothesis-generator` only when actually searching for new
  short-horizon ideas.

A mere explanation of an existing result is not an automatic specialist route. If a mandatory child agent cannot be called, the step `BLOCKED`; the Coordinator shall not pretend his contribution or issue it as his own independent audit.

## 12.1 Default

An individual agent is the operational default. Multiple agents are only used if task separation, independent testing or parallelization has a specifically named benefit. More agents are not an evidence-gain in itself.

Exactly one **coordinator run id** bears the final responsibility. Each contributing agent gets their own child run with **parent run id**.

## 12.2 Mandatory plan before delegation

Before launch, the following are logged:

- the purpose of the delegation;
- a defined order per agent;
- Allowed inputs, tools and writing ranges,
- expected artifacts and acceptance criteria,
- budget and termination rule,
- dependencies and merge order,
- whether an audit should actually be independent.

Two agents must not possess the same canonical artifact at the same time. Contributions are generated separately and brought together by the coordinator. Shared file access without an ownership or merge rule is not permitted.

## 12.3 Independence

An auditor declared to be independent shall not accept as evidence the conclusion to be audited, its justification, or the producer agent's evaluation. The auditor receives only the inputs and acceptance rules required for the examination. Whether and when results were mutually visible is recorded.

Majority voting does not replace source verification, the method gate, or human review.

## 12.4 Gate status

The status is:

- **NOT_USED**
- **PASS**
- **FAIL**
- **BLOCKED**

**PASS** requires all of the following:

1. complete delegation plan;
2. valid run manifests of all child runs,
3. unique writing and artifact ownership,
4. complete lineage of each acquired claim and artifact,
5. documented resolution of conflicts and contradictions,
6. renewed schema, hash, evidence and source verification by the coordinator,
7. complete error, cost and retry telemetry;
8. reproducible derivation of the final output from accepted child artifacts,
9. No open ERROR or CRITICAL conflicts.

**FAIL** applies in particular to:

- missing child-run lineage,
- the unclaimed claim,
- concealed write conflict,
- cyclic delegation,
- fictitious independence,
- unresolved material contradiction,
- Using multiple agents to bypass a gate.

**BLOCKED** applies if a required child run, conflict decision or artifact is missing.

A child agent may not upgrade either Evidence Grades or Methodological Gates of the Coordinator Run alone.

---

# 13. Operational release gate

The following sub-gates shall be reported before a decision-making run is completed:

| Sub-gate | Status |
|---|---|
| RUN_MANIFEST | PASS / FAIL / BLOCKED |
| ARTIFACT_INTEGRITY | PASS / FAIL / BLOCKED |
| EVIDENCE_CHAIN | PASS / FAIL / BLOCKED |
| SOURCE_VERIFICATION | PASS / FAIL / BLOCKED |
| OBSERVABILITY | PASS / FAIL / BLOCKED |
| ERROR_STATE | PASS / FAIL / BLOCKED |
| DELTA | PASS / FAIL / BLOCKED / NOT_REQUIRED |
| FORECAST_LEDGER | PASS / FAIL / BLOCKED / NOT_REQUIRED |
|AGENT EVAL| PASS / FAIL / BLOCKED / NOT_REQUIRED |
|MULTI AGENT| PASS / FAIL / BLOCKED / NOT_USED |
| HUMAN_REVIEW | PASS / FAIL / BLOCKED / NOT_REQUIRED |

The overall gate is:

- **PASS** if every applicable sub-gate is PASS and the multi-agent gate is
  PASS or NOT_USED, as applicable,
- **FAIL** if any sub-gate is FAIL,
- **BLOCKED** if there is no FAIL but at least one applicable sub-gate is BLOCKED.

Only complete gate **PASS** allows **status = SUCCEEDED** for a decision-making order.

**PARTIAL** is permitted if secure, clearly defined sub-artifacts exist. They
must not be issued as a complete phase or released decision.

---

# 14. Minimum execution sequence

1. Create a run ID and manifest with **QUEUED**.
2. Record research, prompt, model, tool, data, and baseline versions.
3. validate the manifest against the schema; status **RUNNING**.
4. Record every model, tool and retrieval step in the trace.
5. Classify material claims and build evidence chains.
6. Deduplicate academic sources by work id, fix specific versions, and check integrity/replication.
7. Verify sources and calculate evidence grades deterministically.
8. Classify errors and stop dependent steps if necessary.
9. Freeze forecasts in the ledger before their outcomes.
10. Compare against the baseline.
11. Run evals when the system changes.
12. Run the multi-agent gate for delegation.
13. Obtain required human review.
14. Calculate the operational release gate.
15. Finalize the manifest and output hashes.

---

# 15. Machine-testable invariants

A validator MUST detect at least the following violations:

1. terminal run without manifest or end time,
2. **SUCCEEDED** without an operational release gate,
3. material claim without run id, type, evidence chain or evidence grade,
4. dangling or cyclic evidence reference,
5. SOURCE FACT without reference,
6. CALCULATED VALUE without reproducible inputs and transformation,
7. FORECAST without ledger entry generated before outcome,
8. HUMAN JUDGMENT without authenticated human review,
9. subjective LLM confidence percentage without calibrated forecast model,
10. unlogged model, tool or retry call,
11. terminal run with open CRITICAL error,
12. Override overwriting an original artifact,
13. MATERIAL/BREAKING/UNKNOWN Delta without mandatory sequence,
14. Eval baseline change without human approval,
15. Multi-agent contribution without child-run lineage,
16. Operational artifact that arbitrarily upgrades a research gate from 00–04,
17. academic source without work id or specific source id version,
18. multiple versions of the same work id counted as independent confirmations,
19. arXiv claim without q-fin subcategory and exact version number,
20. claimed Version of Record without verified publication status and venue,
21. academic clearance without current correction-/expression-of-concern-/retraction-/withdrawal-check,
22. positive use of a withdrawn claim without mandatory INSUFFICIENT sequence,
23. Replication claim without separate source ids and documented independence check,
24. code/data availability claimed to exist without a verified URI or snapshot,
25. Journal prestigious or arXiv category that immediately increases evidence grade or method gate,
26. open research case without referenced `PROMOTED` hypothesis intake,
27. `FILTER_KNOWN_EVENTS` without feed coverage or exclusion window,
28. `PROMOTED` issued as a confirmed mechanism or edge,
29. contemporary mechanism evidence that automatically upgrades `forward_predictive_oos`,
30. positive forward forecast that automatically upgrades `executable_net_edge` without an executable cost/fill check.

Violation of one of these invariants leads to at least **BLOCKED**, in the case of integrity, provenance, forecast or gate manipulation to **FAILED**.

---

# 16. Closing rule

An agent may not designate a run as reproducible, documentable or released until:

- origin and execution are fully manifested,
- all material claims are classified and traceable to their sources or inputs,
- evidence grades are rule-based rather than self-assessments,
- errors, deltas, forecasts and reviews are logged immutably,
- all applicable operational gates have passed,
- and the professional status from 00–04 is unchanged truthfully reproduced.

Operational cleanliness is a necessary control layer. It is not a substitute for independent data, statistical decisionability, identification, OOS validation or economic feasibility.
