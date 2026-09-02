# Geplante Funktionen

Diese Liste enthält bewusst nur Vorhaben. Ein Eintrag hier ist weder
implementiert noch geprüft noch freigegeben.

## Authoritative implementation order

**Status:** prioritized on 2026-09-02; the initial hard-gate inventory is
complete, while later items remain planned unless their entry explicitly says
otherwise

This order is authoritative. The detailed sections below describe the same
initiatives and their risks; they do not establish a second priority order.
Priority follows two questions: how strongly an item reduces the risk of
believing in a nonexistent edge, and which earlier result is needed before the
item can work.

### Scope and conservative pruning rule

The framework supports private research and capital decisions made by one
owner working with AI agents. It is not being developed for academic
publication, external persuasion, public strategy disclosure, or hypothetical
human-team onboarding.

Classify existing and proposed work as follows:

- **KEEP — decision protection:** directly changes or constrains a research,
  activation, continuation, sizing, suspension, or retirement decision.
- **KEEP — agent enforcement:** demonstrably makes an existing
  decision-protecting rule more likely to reach the agent and be applied
  correctly.
- **CONDITIONAL:** has a plausible protective role, but that role has not yet
  been observed or measured. Retain it while the hard-gate inventory, real
  Research Case, or behavioural evaluation tests the need.
- **REMOVE CANDIDATE:** serves only publication, external persuasion, public
  presentation, or unsupported assumptions about future human collaborators.
- **UNKNOWN:** retain until its effect and dependencies are understood.

Uncertainty is not permission to delete. Removal candidates must identify the
decision they do not protect, the enforcement path they do not support, and any
remaining dependency. Remove one independently reviewable unit at a time only
after relevant behavioural reference cases exist. Compare behaviour before and
after; restore or investigate any unexplained material change. Translation,
editorial simplification, and semantic removal remain separate changes.

The public repository is intended to contain framework code and safe examples
only. Real strategies, private data, real Research Cases, and empirical results
remain in an external private location or the ignored `private_research/` path.
Existing examples have not all been classified under this policy. Keep them
until a separate, user-authorized privacy review determines whether any require
removal or history remediation.

No new control layer should be added merely because it sounds prudent. Existing
controls must first show their value and their failure modes in executable
checks, live-agent evaluations, or a real Research Case.

1. **Hard-gate inventory — initial audit completed 2026-09-02.** The
   [`HARD_GATE_INVENTORY.md`](HARD_GATE_INVENTORY.md) records every current
   research gate and the claim or
   transition it is meant to prevent. For each gate, identify whether it is
   enforced by automatically invoked executable code, by a schema whose
   validation is mandatory on that path, by an agent or human classification,
   or only by prose. Also record the invocation point, the fail-closed
   consequence, the relevant regression test, and any known bypass. The mere
   existence of a validator does not make a hard gate: the normal workflow must
   invoke it, and failure must stop acceptance or continuation. Include the
   already implemented research-fingerprint, scientific-philosophy, causal,
   outcome-contract, and pipeline-integrity controls. This inventory is a
   diagnosis; its findings may change the priorities below. Also mark the
   trust boundary explicitly: the framework cannot discover experiments,
   viewed data, or discarded variants that occurred outside its recorded
   workflow. A control may reduce that exposure but must not claim to eliminate
   undisclosed external search. The audit found substantial deterministic
   checks but no framework-owned end-to-end runtime that forces their use in a
   live research task. The current research gates are therefore
   caller-enforced. Priority 3 must record whether those calls actually occur;
   priority 4 must attack false `COMPLETE` states, skipped
   validators and specialists, ignored fingerprint failures, and semantic
   misclassification before a new orchestration layer is justified.

2. **Prospective data-fitness gate.** Before detailed operationalization,
   implementation, or empirical testing, translate the proposed strategy and
   intended claim into a minimum data-requirement record, then compare it with
   the metadata and observable content of the data that can actually be
   obtained. This is not a bar-count check. It must cover instrument and
   contract identity, continuous-contract construction and roll adjustment,
   session and timezone rules, historical coverage, sampling interval,
   timestamp precision, price and volume meaning, missing periods, revisions,
   bid/ask or trade information, and any intrabar or order-book detail required
   by the trigger, outcome, cost, or execution model. For platform-supplied data
   such as TradingView, record the exact symbol, feed, plan-dependent history,
   export limits, and simulator assumptions rather than treating subscription
   access as proof of fitness.

   The assessment must use metadata and coverage diagnostics without searching
   the data for a favourable effect. It returns one of four decisions:
   `ADEQUATE`, `ADEQUATE_WITH_SCOPE_LIMITS`, `REMEDIABLE_GAP`, or
   `NOT_TESTABLE`. Every limitation must state which research or capital
   decision it prevents. A material gap stops the affected path. The framework
   must never silently simplify the strategy, weaken the claim, enlarge the
   bar interval, substitute a continuous future for executable contracts, or
   change the outcome merely to fit the available data. Any such response is a
   visible research change requiring the user's decision and, where material,
   a new research version. Recheck fitness whenever the strategy,
   operationalization, data source, market scope, or intended claim changes.

   Verification is automation-first and must treat acquisition burden as part
   of feasibility. Prefer one coherent, reusable, versioned export or snapshot
   over repeated interaction with a chart interface. Automated checks should
   cover integrity, coverage, internal consistency, and any feasible
   cross-source comparison. A manual visual review is an exception: it needs a
   named residual risk, a case-selection rule fixed before inspection, and the
   smallest defensible scope. There is no generic screenshot minimum, and an
   agent must never invent an arbitrary quota such as 50 manually reviewed
   charts. Repeated TradingView scrolling, bar-by-bar history loading, or
   manual collection of chart sections is not an acceptable default data
   pipeline. If adequate data cannot be acquired without material repetitive
   user work, the path is `REMEDIABLE_GAP`, `NOT_TESTABLE`, or `BLOCKED`; the
   burden is not transferred to the user and the strategy is not weakened to
   fit the interface.

   The purpose is to reject an untestable project before expensive
   reconstruction creates commitment to it, and to prevent a late discovery
   that the available data could never observe the event, mechanism, or fill
   being claimed. The real Research Case in priority 3 should supply the first
   concrete requirements and failure examples. Planning this gate does not
   authorize inspection of strategy outcomes, a backtest, or market-data use.

3. **One real Research Case.** Run one deliberately unexciting end-to-end case
   with public data and a predeclared expectation that no useful effect will be
   found. Pass the prospective data-fitness gate before detailed
   operationalization. Freeze the repository revision and research state
   before starting,
   do not repair the framework during the case, and record every point where a
   rule is ambiguous, a gate is bypassable, or the process requires an
   unsupported judgement. Fixes follow only in separately reviewed changes
   after the case. One case can reveal practical failures but cannot establish
   that the framework is generally validated. Planning this feature does not
   authorize data access, a backtest, or empirical strategy research; those
   actions still require an explicit user request.

4. **Behavioural baseline and adversarial live-agent evaluation.** Treat the
   earlier LLM stress test, behavioural reference cases, and adversarial agent
   evaluation as one programme. The repository already contains a blind
   producer, scorer, deterministic regression machinery, and a 25-case
   catalog; this is partial infrastructure, not a measured live-agent quality
   baseline. Preserve the pre-case code revision, use failures from priority 3
   to add blind cases whose correct response is to stop, reject work, invoke a
   specialist, expose drift, or refuse a claim upgrade, and then run multiple
   identified models repeatedly. Report catch rates and run-to-run variation.
   A human-approved `LIVE_AGENT` baseline must be frozen before later prompt,
   terminology, loading, or shortening changes are judged safe. Protocol smoke
   results are never a substitute.

5. **Cross-version search lineage with selection-adjusted reporting.** Treat
   search-history accounting and statistical consequence as one control. Every
   new Research-ID or version inherits prior data exposure, definitions,
   filters, outcomes, continuation choices, and failed attempts from the same
   research line. Final reporting must show both the ordinary result and a
   correction or decision rule appropriate to that complete selection process,
   not merely to the surviving latest version. This becomes urgent as soon as
   a real research line reaches a second version.

6. **Fail-closed rule-set loading and reference checks.** First enforce the
   rule at the current whole-document level: a material step must prove that
   every document required by its route was resolved, loaded, and recorded,
   otherwise it stops. Separately, before selective loading is activated,
   introduce stable section identifiers and CI checks proving that every
   identifier the router can emit resolves exactly once to non-empty content.
   Missing, stale, ambiguous, or incomplete references must never degrade into
   a reduced but apparently valid run.

7. **Canonical concept registry.** Limit the registry to concepts that carry a
   decision-protecting rule or whose ambiguity can disable an agent gate. Map
   each such concept to one canonical term, a concise definition, its legacy
   terms, and exact machine anchors where those anchors genuinely exist. Use
   results from priority 4 to identify which semantic ambiguities cause real
   failures, while treating the current German-prose/English-machine split as
   an existing but still measurable correctness risk. The registry is required
   before isolated normative sections can be trusted; it is not a general
   terminology or documentation project.

8. **Severity-aware change control.** Separate semantic research changes,
   evidence-integrity changes, and demonstrably non-material editorial changes.
   Implement this when real fingerprint alerts exist and there is evidence
   that harmless alerts are training users to approve changes reflexively. It
   must reduce alert fatigue without hiding material rule or research changes.

9. **Selective normative loading.** Keep this optional and treat it as an
   efficiency project, not a research safeguard. It may start only after the
   critical live-agent baseline in priority 4, the fail-closed checks in
   priority 6, the applicable concept mappings in priority 7, and actual
   before-change context measurements exist. Measure savings and behavioural
   changes; do not assume that shorter prompts preserve gate behaviour.

10. **Conditional legacy-language migration.** Do not migrate the remaining
   German corpus merely for publication, an international audience, or
   stylistic consistency. Proceed only if priority 4 measures a material agent
   reliability problem that narrower concept mappings cannot solve, or if an
   actual maintenance need emerges. Priority 7 supplies the necessary semantic
   mappings. Translation-only commits must remain separate from shortening,
   deduplication, or substantive revision so that changes in agent behaviour
   remain attributable.

The synthetic pipeline-integrity control, outcome evidence contract, complete
research fingerprint, central conductor, and specialist routing are completed
controls rather than new roadmap items. Their actual enforcement and bypass
resistance are nevertheless subjects of priorities 1 through 4.

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

### Selective-loading dependency order

This is the internal dependency sequence for priority 9 above, not a competing
global roadmap. Priorities 4, 6, and 7 must reach the applicable activation
criteria before selective loading is enabled.

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

## Detailed research-control backlog

**Status:** planned, not implemented

The following findings must remain visible until they are implemented and
validated. Their authoritative priority and grouping are defined above; the
numbers here identify details rather than execution order:

1. **Priority 5 — Cross-version search lineage:** A new research version must inherit every
   previous data exposure, operationalization attempt, filter choice, outcome
   choice, and continuation decision from the same research line. Repeatedly
   authorizing new versions must not reset the information budget or create an
   apparently fresh search family.
2. **Priority 5 — Selection-adjusted reporting:** Final performance reporting must show both
   the ordinary metric and a correction or decision rule appropriate to the
   complete selection process. The correction must cover the relevant
   candidate family, research-version history, and data reuse rather than only
   the survivors of the latest screen.
3. **Priority 8 — Severity-aware change control:** Separate the semantic research
   fingerprint from the artifact-integrity manifest. Distinguish material
   research changes, evidence-integrity changes, and demonstrably non-material
   editorial changes so that harmless hash changes do not train users to
   approve every warning.
4. **Priority 1 — Hard-gate coverage accounting (initial inventory complete):** Maintain the
   [`HARD_GATE_INVENTORY.md`](HARD_GATE_INVENTORY.md), showing
   which research gates are enforced by executable checks, which are enforced
   only by schemas, which depend on an agent classification, and which remain
   prose instructions. Increase executable enforcement where the required
   condition is objectively decidable and the real case or behavioural
   evaluation demonstrates that the current caller-enforced path is unreliable.
5. **Priority 4 — Adversarial live-agent evaluation:** Extend the planned LLM stress test
   with agents that actively attempt to change definitions, reset the search
   history, upgrade claim levels, skip required specialists, or satisfy schemas
   with scientifically empty content. Measure repeated catch rates rather than
   treating contract validity as evidence of agent reliability.
6. **Priorities 7 and 10 — Narrow terminology control and conditional language
   migration:** Establish only the decision-relevant concept mappings described
   above before selective loading. Migrate the legacy German corpus only after
   a measured agent-reliability or actual maintenance need. Translation must be
   performed in translation-only commits; redundancy removal, shortening, and
   substantive rewriting must follow in separate commits with separate
   validation.
