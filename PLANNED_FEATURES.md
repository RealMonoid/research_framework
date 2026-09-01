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
