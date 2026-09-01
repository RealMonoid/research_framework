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
6. **English migration and terminology control:** Move the normative corpus to
   English and establish one canonical glossary. Translation must be performed
   in translation-only commits; redundancy removal, shortening, and substantive
   rewriting must follow in separate commits with separate validation.
