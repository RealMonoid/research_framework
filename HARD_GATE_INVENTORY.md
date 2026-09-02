# Hard-gate inventory

**Audit date:** 2026-09-02

**Audited revision:** `4af9cff`

**Purpose:** show which safeguards actually stop a research step, which depend
on an agent invoking them correctly, and which are only documented intentions.

This inventory is a diagnosis. It does not make a weak control stronger merely
by listing it.

## Plain-language result

The framework contains substantial executable protection: a deterministic
router, strict artifact contracts, semantic validators, fingerprint comparison,
regression tests, and repository CI. These parts reject many invalid states
when they are invoked.

The central weakness is that there is no single framework-owned runtime that
forces every live research task through that sequence. The host agent is
instructed to create a checkpoint, call the router, invoke a required
specialist, validate the returned artifact, compare the full fingerprint, and
save the next checkpoint. The router can stop on the state it receives, but it
does not create that state, call the specialist, open the referenced artifact,
or prove that the validator ran. A caller can therefore skip a check or mark an
artifact `COMPLETE` without the router independently verifying it.

Consequently, the current research controls are best described as
**caller-enforced executable gates**, not fully automatic end-to-end gates.
Repository CI is automatic on pushes and pull requests, but it proves that the
framework contracts and regression fixtures pass. It does not prove that a
particular research run followed them.

This finding does not justify removing any safeguard. The next real Research
Case and the adversarial live-agent evaluation should determine which caller
failures occur in practice and whether a small execution harness is needed.

## Enforcement classes

| Class | Meaning |
|---|---|
| **A — automatically invoked executable** | The repository or runtime invokes the check on the relevant path without relying on an agent to remember it, and failure prevents that path from succeeding. |
| **B — caller-enforced executable** | Deterministic code rejects the invalid state when called, but the current host or conductor must call it and respect its result. |
| **C — schema or semantic contract** | A structured artifact can be rejected objectively, but only when the applicable validator is invoked. Structural validity does not establish that the recorded facts are true. |
| **D — agent or human judgement** | The gate depends on classifying intent, meaning, source completeness, evidence, or a material choice. The decision is recorded but cannot be derived reliably from syntax alone. |
| **P — prose instruction** | The rule exists in normative text but has no executable acceptance check on the live path. |
| **M — missing control** | The intended protection is planned or acknowledged, but the current framework has no complete enforcement path. |

A gate may use more than one class. Its effective strength is limited by the
weakest required step in its normal path.

The eight gates named as binding in `00_RESEARCH_AGENT_README.md` are covered
explicitly as follows:

| Normative gate | Inventory entry |
|---|---|
| Phase-0 feasibility | HG-22 |
| Causal identification, when a causal claim is requested | HG-08 |
| Measurement and leakage | HG-23 |
| Pipeline integrity | HG-10 |
| Freeze completeness | HG-09 and HG-24 |
| Validation independence | HG-25 |
| Economic executability | HG-26 |
| Activation | HG-16 and HG-27 |

The causal-tooling prerequisite used by the detailed case template is recorded
separately as HG-28.

## Inventory: research transitions

| ID | Decision or claim protected | Present enforcement and invocation | Failure consequence | Regression evidence | Known bypass or limit | Class |
|---|---|---|---|---|---|---|
| **HG-01** | No material research transition without a classified checkpoint and one permitted next step. | The conductor instructions require a schema-valid orchestration state and a call to `scripts/route_research_task.py`. The router returns one bounded work order. | Invalid input makes the router exit; recorded blockers produce `BLOCKED`. | `scripts/test_research_orchestration.py`; orchestration schema tests. | No framework-owned process forces the host to create a truthful checkpoint or call the router. The router consumes classifications supplied by the agent. | **B+C+D** |
| **HG-02** | No continuation while a required artifact is `BLOCKED` or `INVALID`, or while a recorded blocking issue exists. | The router checks every recorded artifact status and `blocking_issues`. | Route becomes `BLOCKED`; the work order forbids advancing the phase. | `scripts/test_research_orchestration.py`. | A missing blocker, false status, or skipped router remains invisible. Artifact references are not dereferenced here. | **B+C+D** |
| **HG-03** | Returned work must not silently alter the effective research question, definitions, parameters, filters, data choices, inference rules, results, or protected artifacts. | `scripts/check_research_fingerprint.py` performs a deterministic full-state comparison. The router blocks `AWAITING_COMPARISON` and pauses on `CHANGE_PROPOSED`. | The comparison exits non-zero for a change; the baseline remains effective and the router requires a visible proposal. | Fingerprint and hidden-filter cases in `scripts/test_research_orchestration.py`; schema fixtures. | The host must derive a complete candidate, call the comparison, respect its exit code, and record the result. Unrecorded work is outside the comparison. | **B+C+D** |
| **HG-04** | A material change cannot become a new research version without an explicit user decision. | The router converts a recorded material choice or `CHANGE_PROPOSED` state into `USER_DECISION_REQUIRED`. | The route pauses and prohibits replacement of the effective fingerprint. | User-choice and drift cases in `scripts/test_research_orchestration.py`. | User authorization is represented by agent-maintained state; there is no independent identity, approval, or version-creation service. | **B+C+D** |
| **HG-05** | A prose strategy cannot be operationalized before its source rules, examples, discretion, and open definitions are reconstructed. | The router selects `RECONSTRUCT_SOURCE_STRATEGY` when a prose source lacks a complete reconstruction. The artifact has a schema and semantic inspector. | Operationalization is not selected; the work order stops at source extraction and forbids a test. | `scripts/test_strategy_reconstruction.py`, schema negatives, and orchestration routing tests. | The agent classifies `source_kind`, completeness, and reconstruction status. A false `COMPLETE` status or skipped routing call bypasses the gate. | **B+C+D** |
| **HG-06** | Unknown success conditions and construction dependencies cannot be smuggled into an incomplete source strategy before operationalization. | The router requires `SCIENTIFIC_PHILOSOPHY_PRE_OPERATIONALIZATION` when the recorded source is incomplete or the concept audit is required. The specialist output has a schema and inspector. | The work order stops before choosing definitions or running data and requires unknown conditions to remain unknown. | `scripts/test_strategy_concept_audit.py`, schema negatives, orchestration tests, and the relevant eval catalog case. | The router selects the specialist but does not invoke it. Whether an audit is mandatory depends on agent classifications, and `COMPLETE` is self-declared until the caller validates the referenced artifact. | **B+C+D** |
| **HG-07** | A condition or measurement inquiry cannot run before a provisional definition exists, and a discovered condition cannot silently rewrite the source strategy. | The router orders provisional operationalization before `CONDITION_INQUIRY`; the inquiry has a schema and semantic inspector. | The quantitative inquiry is deferred or bounded to the recorded definition. | `scripts/test_condition_inquiry.py`, orchestration tests, and the measurement-routing eval case. | The operationalization status and the distinction between source fact and researcher choice remain agent judgements. No independent recurrence is run automatically. | **B+C+D** |
| **HG-08** | Interventional or counterfactual wording or estimation cannot proceed without a causal-identification assessment. | A causal claim level routes to `CAUSAL_IDENTIFICATION_REVIEW`; the assessment has a finance-specific inspector and schema. | The work order stops before estimation and permits `PASS`, `BLOCKED`, `FAIL`, or predictive not-required status only after review. | `scripts/test_causal_identification.py`, orchestration tests, and causal eval cases. | The agent supplies the requested claim level. Misclassifying a causal request as predictive avoids the route. The router does not call the specialist or validate the referenced artifact itself. | **B+C+D** |
| **HG-09** | Validation cannot be frozen until outcome roles, falsifiers, multiplicity families, mechanical coupling, and decision consequences were fixed before results. | The router requests the outcome contract during `RESEARCH_CASE` and blocks `FROZEN_TEST` when its recorded status is not `COMPLETE`. The contract has schema and semantic validation. | Missing contract stops the freeze path; invalid contracts fail validation. | `scripts/test_outcome_evidence_contract.py`, schema tests, and orchestration freeze cases. | The router trusts a `COMPLETE` status and reference; it does not open and validate the contract. The host supplies the stage and can falsely advance it. | **B+C+D** |
| **HG-10** | The unchanged complete pipeline cannot enter validation until repeated relevant negative controls and a known-effect sentinel pass. | After the outcome contract, the router requests a pipeline assessment and blocks missing, failed, or blocked recorded status. The semantic validator derives the overall gate from required controls. | Only a valid assessed `PASS` may be recorded as `COMPLETE`; `FAIL` or `BLOCKED` prevents freeze. | `scripts/test_pipeline_integrity_assessment.py`, schema tests, and orchestration freeze cases. | The conductor instruction, not the router, maps the validated result to orchestration status. Adequacy of preserved market structure includes judgement. A false `COMPLETE` reference bypasses the router. | **B+C+D** |
| **HG-11** | A frozen non-positive result cannot be relabelled or rescued through a post-result definition change without a new testable prediction. | The router sends attribution, revision, or continuation after a recorded non-positive result to `SCIENTIFIC_PHILOSOPHY_POST_RESULT`. The review has a schema and inspector. | The old result remains frozen; empirical continuation requires a new Research-ID and independent test. | `scripts/test_scientific_philosophy_review.py`, orchestration tests, and the failed-bundle eval case. | Intent and frozen-result status are supplied by the agent. A plain `INTERPRET_RESULT` route correctly bypasses review, but an agent can misclassify a revision as interpretation. The router does not invoke or verify the specialist. | **B+C+D** |
| **HG-12** | Reconstructing, generating, or operationalizing an idea must not itself authorize a backtest or market-data test. | Router work orders and conductor instructions explicitly exclude empirical testing on these paths. | A compliant agent stops before a test and requires a separate user request plus later gates. | Some route assertions check excluded actions; strategy reconstruction and generator tests prove their artifacts contain no results. | There is no explicit empirical-authorization field or executable data-access boundary. A host with data tools can ignore the prose exclusion. | **D+P** |

## Inventory: evidence, search, and release claims

| ID | Decision or claim protected | Present enforcement and invocation | Failure consequence | Regression evidence | Known bypass or limit | Class |
|---|---|---|---|---|---|---|
| **HG-13** | An `INBOX` idea cannot be represented as a fully admitted research candidate without the required scope, alternatives, feasibility, actor treatment, selection provenance, and noise-screen decision. | Conditional requirements in `schemas/hypothesis_candidate.schema.json` reject structurally incomplete `PROMOTED` artifacts when validation runs. | The candidate artifact is invalid and cannot be accepted by a compliant conductor. | Extensive positive and negative cases in `scripts/test_schemas.py` and its PowerShell counterpart. | The schema establishes presence and allowed combinations, not truth or scientific adequacy. No live service forces every candidate through validation. | **C+D** |
| **HG-14** | Data-driven screening cannot use the final holdout or pass a weaker threshold than the registered search family. A screen pass cannot become evidence. | Search-space and noise-screen schemas plus `scripts/validate_entry_thresholds.py` check data roles, family counts, timestamps, thresholds, and screen results. | Invalid bundles fail with a non-zero exit. | `scripts/test_entry_thresholds.py`, schema negatives, and the noise-screen eval case. | The validator sees only disclosed candidates and exposures. It does not inherit undisclosed prior trials or cross-version search automatically. The caller must invoke it. | **B+C+D** |
| **HG-15** | Mechanism evidence, forward prediction, causal identification, and executable after-cost edge must remain separate claims. | Candidate, evidence, forecast, constraint, outcome-contract, and pipeline schemas restrict some invalid promotions; router and evals test major category errors. | A structurally forbidden claim state fails validation; causal claims may be rerouted or blocked. | Schema negatives and eval cases for OFI, causal effects, actor stories, noise screens, and synthetic controls. | Many semantic upgrades can still be written in prose while leaving schemas valid. Executable-edge sufficiency, realistic costs, and market impact require evidence judgement that is not fully encoded. | **B+C+D+P** |
| **HG-16** | An operational release cannot declare `PASS` while mandatory run, artifact, evidence, source, observability, or error gates are not `PASS`. | `schemas/run_manifest.schema.json` contains conditional release-state constraints. | A validated manifest with inconsistent gate values is rejected. | Run-manifest schema positives and negatives in `scripts/test_schemas.py`. | This is currently a contract, not an active deployment controller. References are not dereferenced, and no runtime automatically suspends or retires trading. | **C+D+P** |
| **HG-17** | A model or prompt must not receive a live-agent quality claim from the hand-written score-1.000 smoke fixture. | The eval scorer can require `LIVE_AGENT`; the manual GitHub workflow produces blind results and invokes that release gate. | Protocol smoke or a failing live run exits non-zero. | `evals/tests/test_produce_results.py` and `evals/tests/test_run_evals.py`. | The live workflow is manually dispatched and no accepted live behavioural baseline is currently frozen. Ordinary CI runs only protocol smoke. | **B+C** |

## Inventory: framework delivery and acknowledged gaps

| ID | Decision or claim protected | Present enforcement and invocation | Failure consequence | Regression evidence | Known bypass or limit | Class |
|---|---|---|---|---|---|---|
| **HG-18** | Broken schemas, validators, router rules, fixtures, producer/scorer protocol, or deterministic regressions must not enter unnoticed. | GitHub Actions runs `scripts/validate_framework.py` on every push and pull request on Linux and Windows. | The workflow fails. A protected branch can require that status before merge. | The complete deterministic test suite. | CI validates framework code and fixtures, not a live research run. Whether a failed status blocks merge depends on repository branch-protection settings outside this codebase. | **A** for repository events |
| **HG-19** | A research step must not proceed with required rules absent from the agent context. | Agents are instructed to read `QUICKSTART.md` and routed documents. | A compliant agent stops if it notices a missing mandatory specialist or prerequisite. | No complete load-manifest or missing-document injection test exists. | The current framework cannot prove which documents were resolved and loaded. Missing or stale rules may therefore fail silently. Priority 6 addresses this. | **P+M** |
| **HG-20** | Repeatedly creating new research versions must not reset prior searches, viewed data, failed variants, or the multiplicity burden. | The current fingerprint records the effective state of one version, and intake records can cite exposures. | No automatic cross-version consequence exists. | No end-to-end regression covers inherited search lineage. | A new version can appear fresh unless prior exposure is disclosed and carried forward manually. Priority 5 addresses this. | **D+P+M** |
| **HG-21** | Private strategies, data, real cases, and empirical results must not be committed to the public framework repository. | Repository instructions require private storage, and `.gitignore` excludes designated private paths. | Ordinary unforced additions under those paths are ignored by Git. | No privacy-classification or secret-history test exists. | Files placed elsewhere, forced additions, copied excerpts, already tracked material, and repository history remain outside this protection. | **P** with a limited Git safeguard |

## Inventory: binding gates that are not yet end-to-end executable

| ID | Decision or claim protected | Present enforcement and invocation | Failure consequence | Regression evidence | Known bypass or limit | Class |
|---|---|---|---|---|---|---|
| **HG-22** | Expensive formal research should not start when the economically relevant effect cannot be estimated with enough independent information under a conservative planning scenario. | The research standard and case template define the Phase-0 calculation and the `WEITER`, `DATEN BESCHAFFEN`, and `ABBRECHEN` mapping. Candidate schemas require some early feasibility fields. | A compliant agent records `PASS`, `BLOCKED`, or `FAILED` and does not advance after the latter two states. | Schema tests cover selected feasibility fields; no executable validator recalculates the complete Phase-0 gate from a Research Case. | Power assumptions, conservative dispersion, effective independence, and the final gate mapping are agent or analyst judgements recorded in prose. | **C+D+P** |
| **HG-23** | A variable unavailable at decision time, contaminated dataset, post-treatment control, overlapping label, or other leakage must not support the claimed test. | Data-role and selected timing fields appear in schemas; the standard and case template require observability, contamination, purging, embargo, and leakage review. | A compliant agent blocks or invalidates the affected test and reclassifies consumed data. | Schema negatives cover some data roles; evals cover selected contemporaneous-versus-forward mistakes. No general point-in-time or leakage validator exists. | Timestamps, data vintages, feature code, and actual data access are not compared automatically with the declared state. | **C+D+P** |
| **HG-24** | A validation plan must not be frozen until every material design choice and decision rule is fixed. | The router enforces the outcome-contract and pipeline-integrity prerequisites. The broader freeze checklist and O-gate remain in the case template and research standard. | Missing outcome or pipeline artifacts stop the router; any other missing freeze item should block under the normative rule. | Orchestration tests cover the two executable prerequisites; no test proves the full O-gate checklist is complete. | A state can be marked `FROZEN_TEST` after only the two router-visible artifacts are marked complete. The router cannot see the remaining freeze fields. | **B+C+D+P** |
| **HG-25** | Validation must use the frozen plan and previously unseen validation data; a changed plan or viewed holdout cannot retain an independent-validation claim. | The case template defines freeze comparison, start, and independence gates. Data-role schemas prohibit some invalid uses, and the fingerprint can expose recorded changes. | A compliant agent stops validation, marks `INVALID_TEST`, or reclassifies the data as development. | Fingerprint and selected data-role tests exist; no executable validation-run controller compares actual data access and code against the frozen plan. | Prior viewing, off-workflow access, or an unrecorded implementation change cannot be discovered automatically. | **B+C+D+P** |
| **HG-26** | A validated phenomenon or forecast must not be called a tradable edge until the complete strategy survives realistic costs, fills, latency, capacity, risk, and a separate forward/OOS test. | The claim ladder, candidate and constraint schemas, research standard, and case-template strategy-engineering sections keep these decisions separate. | A compliant agent reports `ECONOMICALLY_UNTRADEABLE` or stops before activation. Some invalid claim combinations fail schema validation. | Schema and eval cases prevent several direct claim upgrades. No executable cost, fill, capacity, or full-strategy release validator exists. | Plausible but unrealistic cost or fill assumptions can remain formally valid. The framework cannot verify broker execution or capacity from documentation alone. | **C+D+P** |
| **HG-27** | Capital must not be assigned until the phenomenon, engineered strategy, full-strategy OOS test, costs, risk rules, reproducibility, and degradation rules all pass. | The case template defines the X activation gate; the run-manifest schema prevents an internally inconsistent declared operational `PASS`. | A compliant agent keeps the strategy `NOT_ACTIVE` or `ACTIVE_STRATEGY_CANDIDATE`. | The run-manifest schema has a failed-subgate regression. No live activation or broker-side block is tested. | There is no deployment service, broker permission gate, or automatic monitoring/suspension controller in this repository. | **C+D+P** |
| **HG-28** | A causal analysis requiring specialist software must not freeze or estimate until the selected package, version, API, environment, seed policy, and a suitable tooling sentinel are verified. | The causal tooling document, case-template E9/O/N4 fields, and conductor instructions define the requirement. | A compliant agent records `TOOLING_BLOCKED` and stops the dependent causal path. | Pipeline tests cover general sentinels; there is no universal executable tooling router or package-specific compatibility suite. | The check is assembled for each design and depends on the agent accurately identifying when specialist tooling is required. | **D+P** |

## Trust boundary

The framework can only protect information that enters its recorded workflow.
It cannot discover or reconstruct, by itself:

- experiments run in another tool or conversation;
- data, charts, or results that the user or an agent already viewed but did not
  disclose;
- discarded definitions, filters, targets, time windows, or strategy variants;
- false or incomplete checkpoint classifications;
- research performed under a new identifier that is not linked to its earlier
  versions;
- private material copied outside the ignored paths or forced into Git.

The schemas, fingerprint, information budget, and future search-lineage control
can make disclosure explicit and inconsistencies easier to detect. They cannot
eliminate undisclosed external search. Any report must preserve that
limitation instead of claiming a complete audit of the researcher's history.

## Decisions protected by controls that should be retained

The current inventory supports retaining the following controls because each
directly protects a research or capital decision:

- source reconstruction and the pre-operationalization concept audit;
- causal-identification review only for causal claims;
- frozen outcome roles and pipeline-integrity controls before validation;
- full-state fingerprint comparison and visible version changes;
- search-space, holdout, and claim-level separation;
- post-result continuation review;
- repository contract tests and the live-agent eval harness.

The conductor instructions and structured checkpoints should also remain. They
are presently part of the enforcement chain even though they are not an
independent runtime. Their weakness is a reason to test their delivery, not a
reason to delete them.

No existing safeguard is classified for removal by this audit. Controls whose
value or duplication remains uncertain stay in place until a real case or
behavioural evaluation can compare decisions with and without them.

## Consequences for the roadmap

1. **Priority 2 is now the next prerequisite.** Before the first real Research
   Case is operationalized, its proposed strategy and intended claim should be
   compared with the data that can actually be obtained. A material mismatch
   in history, sampling, contract construction, observability, or execution
   detail must stop the affected path rather than being repaired by silently
   weakening the strategy.
2. **Priority 3 runs the first real case.** It should record, for
   every material transition, whether the checkpoint was validated, the router
   was called, every referenced artifact was opened and validated, the required
   specialist was actually invoked, and the fingerprint exit code was obeyed.
3. **Priority 4 receives concrete adversarial cases.** At minimum, test a false
   `COMPLETE` artifact status, a skipped validator, a skipped specialist call, a
   causal request misclassified as predictive, a revision misclassified as
   explanation, an ignored non-zero fingerprint result, and a formally valid
   but scientifically empty artifact.
4. **Do not build a large orchestration platform yet.** If the real case or
   repeated live-agent runs show that caller-enforced gates are skipped, add the
   smallest fail-closed conductor harness that validates references and owns
   the sequence. The inventory alone does not establish its required size.
5. **Keep priorities 5 and 6 visible.** Cross-version search lineage and
   proof of effective rule loading address two exposures that the present code
   does not close.
6. **Do not claim automatic enforcement from a validator's existence.** Future
   documentation must state separately who invokes the validator, what failure
   stops, and how that stop is tested.

## Maintenance rule

Update this inventory whenever a gate, router transition, validator, schema
condition, or normal invocation path changes. A control may move to class A
only when the relevant live path invokes it without relying on an agent to
remember the call, rejects missing or invalid inputs, and has a regression test
for that exact stop.
