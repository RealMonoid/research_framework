# ADR-001: Separate, artifactbasierte Operationsschicht für den Research-Agenten

**Status:** Accepted  
**Date:** 2026-08-30  
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Die Dokumente **00_RESEARCH_AGENT_README.md** bis **04_CAUSAL_TOOLING.md** bilden bereits einen umfangreichen methodischen Kern für Trading-Research. Sie regeln insbesondere Datenrollen, Machbarkeit, Claim-Level, Identifikation, Leakage, statistische Inferenz, Freeze, Validation, Tooling und Research-Endzustände.

Für den Betrieb eines tatsächlichen LLM-Agenten fehlen jedoch eigenständige, maschinenprüfbare Kontrollen für:

- die Herkunft eines einzelnen Agentenlaufs,
- die Trennung von Quellenfakt, Rechnung, Estimate, Inferenz, Forecast und Human Judgment,
- eine Claim-Level Evidence Chain,
- Quellen- und Zitationsprüfung,
- deterministische Evidence Grades,
- Trace, Kosten, Retries und Fehler,
- menschliche Korrekturen und Overrides,
- Delta Detection und ein Forecast Ledger,
- LLM-Evals und eine kontrollierte Improvement Loop,
- den sicheren Einsatz mehrerer Agenten.

Diese Informationen direkt in **02_RESEARCH_CASE_TEMPLATE.md** einzubauen würde das bereits große fallbezogene Arbeitsartefakt mit Laufzeittelemetrie vermischen. Eine konkrete Datenbank- oder Orchestrierungsplattform ist noch nicht ausgewählt und soll nicht vorweggenommen werden.

Constraints:

- Der methodische Kern aus 00–04 darf semantisch nicht dupliziert oder abgeschwächt werden.
- Die operative Schicht muss als Dateien und JSON-Artefakte nutzbar sein, bevor eine Laufzeitplattform existiert.
- Alle entscheidungstragenden Beziehungen müssen auditierbar, versioniert und unveränderlich sein.
- Confidence darf nicht durch freie LLM-Selbsteinschätzung entstehen.
- Ein Multi-Agent-System darf erst nach nachgewiesener Kontrolle eines Einzelagenten freigegeben werden.

## Decision

Wir führen eine getrennte, artifact-first Operationsschicht ein.

1. **05_AGENT_OPERATIONS.md** wird der normative Standard für Run-Provenance, epistemische Claim-Typen, Evidence Chains, Source Verification, Evidence Grades, Observability, Fehler, Human Review, Deltas, Forecasts, Evals und Multi-Agent-Gates.
2. **schemas/run_manifest.schema.json**, **schemas/evidence.schema.json**, **schemas/forecast.schema.json** und **schemas/review.schema.json** definieren die maschinenprüfbaren Kernartefakte. Jede Schemaversion besitzt eine stabile ID; Änderungen erfolgen versioniert.
3. **examples/** enthält minimale gültige Beispiele. Beispiele sind keine inhaltliche Freigabe.
4. **evals/** enthält einen versionierten Katalog, eine bewusste Baseline, einen deterministischen Runner und Tests für LLM-/Agentenregressionen.
5. Lauf-, Evidence- und Review-Artefakte sind append-only beziehungsweise revisionsbasiert. Eine Änderung erzeugt ein neues Objekt mit expliziter Vorgängerbeziehung; freigegebene Originalartefakte werden nicht überschrieben.
6. Die epistemischen Klassen **SOURCE_FACT**, **CALCULATED_VALUE**, **ESTIMATE**, **INFERENCE**, **FORECAST** und **HUMAN_JUDGMENT** sind orthogonal zum Research-Claim-Level aus **01 §5**.
7. Die einzige operative Confidence-Klasse ist der deterministisch ermittelte Evidence Grade **SUFFICIENT**, **LIMITED** oder **INSUFFICIENT**. Er ersetzt keine methodische Validierung.
8. Human Overrides bilden eine separate Review-Schicht. Sie dürfen weder Evidenz noch methodische Gate-Resultate umetikettieren.
9. Ein Einzelagent bleibt der Default. Multi-Agent-Ausführung benötigt eigene Child-Runs, eindeutige Artefakt-Ownership, Konfliktauflösung und ein bestandenes Multi-Agent-Gate.
10. Die Schicht bleibt runtime-neutral. Dateibasierte Artefakte können später in eine Datenbank oder Observability-Plattform gespiegelt werden, solange IDs, Hashes, Lineage und Unveränderlichkeit erhalten bleiben.

Die normative Abgrenzung lautet:

**00–04 entscheiden, was methodisch zulässig ist; 05 und die operativen Artefakte belegen, wie ein Agent zu seinem Ergebnis gelangt ist und ob dieses Ergebnis freigegeben werden darf.**

## Options Considered

### Option A: Alle operativen Felder in das Research-Case-Template integrieren

| Dimension | Assessment |
|---|---|
| Complexity | Mittel in der Erstimplementierung, hoch in der laufenden Nutzung |
| Cost | Niedrig technisch, hoch durch manuelle Pflege |
| Scalability | Niedrig; ein Markdown-Dokument wird zum Laufzeitlog |
| Team familiarity | Hoch; bestehendes Template bleibt der einzige Einstieg |

**Pros:**

- Nur ein sichtbares Arbeitsartefakt pro Research Case.
- Keine neue Artefaktschicht zum Einstieg erforderlich.
- Menschlich direkt lesbar.

**Cons:**

- Vermischt langlebigen Research Case mit vielen kurzlebigen Agentenläufen.
- Erhöht Umfang und Konfliktrisiko des bereits großen Templates.
- JSON-Schema-Validierung, Hashing, append-only Audit und automatisierte Evals werden unhandlich.
- Mehrere Runs und parallele Agenten lassen sich nur schwer sauber abbilden.

### Option B: Separate, artifact-first Operationsschicht

| Dimension | Assessment |
|---|---|
| Complexity | Mittel |
| Cost | Mittel initial, niedrig bis mittel im Betrieb |
| Scalability | Hoch; Runs und Claims sind eigenständige versionierte Objekte |
| Team familiarity | Mittel; neue Artefakte und Gates müssen gelernt werden |

**Pros:**

- Klare Trennung von Forschungssubstanz und Agentenbetrieb.
- Maschinenprüfbare Provenance, Evidence und Reviews.
- Mehrere Runs, Regressionen und Multi-Agent-Lineage bleiben vergleichbar.
- Runtime- und providerneutral.
- Bestehende Dokumente 00–04 bleiben weitgehend stabil.

**Cons:**

- Mehr Artefakte müssen gemeinsam verwaltet werden.
- Referentielle Integrität und Hashing benötigen Validatoren.
- Menschliche Leser benötigen eine abgeleitete, zusammengeführte Sicht.

### Option C: Sofort eine zentrale Datenbank und Observability-Plattform einführen

| Dimension | Assessment |
|---|---|
| Complexity | Hoch |
| Cost | Hoch |
| Scalability | Hoch |
| Team familiarity | Niedrig bis mittel, abhängig von der gewählten Plattform |

**Pros:**

- Gute Abfrage-, Dashboard- und Zugriffskontrollmöglichkeiten.
- Append-only Events und große Laufzahlen lassen sich effizient verwalten.
- Spätere Automatisierung kann direkt integriert werden.

**Cons:**

- Frühe Bindung an Technologie und Datenmodell.
- Infrastrukturaufwand, bevor Agentenablauf und Felder stabil validiert sind.
- Migrationen und Plattformbetrieb können die methodische Arbeit dominieren.
- Lokale, überprüfbare Nutzung des Frameworks wird erschwert.

### Option D: Keine zusätzliche operative Schicht

| Dimension | Assessment |
|---|---|
| Complexity | Niedrig kurzfristig |
| Cost | Niedrig kurzfristig, hoch bei Fehleranalyse |
| Scalability | Sehr niedrig |
| Team familiarity | Hoch |

**Pros:**

- Keine neuen Dateien, Schemas oder Prozesse.
- Sofortige Fortsetzung mit dem bestehenden Dokumentpaket.

**Cons:**

- Einzelne LLM-Runs sind nicht reproduzierbar.
- Claim- und Zitationsfehler bleiben schwer lokalisierbar.
- Prompt-, Modell- oder Tooländerungen können unbemerkt regressieren.
- Human Overrides, Forecasts und Multi-Agent-Beiträge sind nicht revisionssicher.

## Trade-off Analysis

Option A erscheint zunächst einfach, macht aber ein fallbezogenes Markdown-Dokument gleichzeitig zum Research Record, Telemetrielog, Evidence Graph und Review-System. Diese Kopplung erschwert sowohl menschliche Arbeit als auch automatische Validierung.

Option C wäre bei sehr hoher Laufzahl langfristig leistungsfähig, fixiert jedoch Infrastruktur, bevor die fachlichen Artefakte durch reale Nutzung stabilisiert sind. Die zentrale fachliche Entscheidung ist zunächst das Daten- und Kontrollmodell, nicht die Speichertechnologie.

Option B fügt mehr Artefakte hinzu, hält ihre Verantwortlichkeiten aber klein und explizit. JSON Schemas ermöglichen frühe Automatisierung, während Markdown die normativen Regeln lesbar hält. Content-Hashes und stabile IDs schaffen eine spätere Migrationsgrenze: Eine Datenbank kann hinzukommen, ohne das fachliche Modell neu zu erfinden.

Der zusätzliche Aufwand ist gerechtfertigt, weil Run-Provenance, Evidence Chain und unveränderliches Review keine redaktionellen Zusatzfelder sind. Sie sind Voraussetzungen dafür, Agentenfehler, Regressionen und menschliche Eingriffe zuverlässig zu erkennen.

## Consequences

- Methodische Research-Dokumente und operative Laufartefakte werden getrennt gepflegt und über research_id, research_version und run_id verknüpft.
- Jeder entscheidungstragende Run benötigt ein validiertes Manifest und Evidence-Dokument; menschliche Eingriffe benötigen ein Review-Dokument.
- Aussagen können auf Claim-Ebene geprüft und zurückgezogen werden, ohne historische Läufe umzuschreiben.
- Prompt-, Modell-, Tool-, Daten- und Schemaänderungen werden als Deltas sichtbar und lösen bei Materialität Evals oder Reviews aus.
- Die Improvement Loop wird messbar; eine Gesamtscore-Verbesserung darf keine kritische Einzelregression verdecken.
- Multi-Agent-Arbeit wird möglich, erfordert aber zusätzliche Lineage-, Ownership- und Merge-Kontrollen.
- Die Zahl der Dateien und Referenzen steigt. Validatoren und eine spätere zusammengeführte Lesesicht werden wichtig.
- SHA-256 und Dateiartefakte sichern Inhaltsintegrität, aber keine Wahrheit, Verfügbarkeit oder Langzeitarchivierung; Retention und Storage bleiben gesondert zu entscheiden.
- Laufzeit-, Kosten- und Trace-Daten können sensible Informationen enthalten und benötigen projektbezogene Aufbewahrungs- und Zugriffskontrollen.
- Die Entscheidung über eine konkrete Datenbank, Event-Store-, Signatur- oder Observability-Plattform wird vertagt, bis reale Laufzahlen und Abfragebedarfe vorliegen.

## Action Items

1. [x] Normativen Operationsstandard in **05_AGENT_OPERATIONS.md** anlegen.
2. [x] ADR für die Trennung von methodischem Kern und operativer Schicht dokumentieren.
3. [x] Run-, Evidence-, Forecast- und Review-Schemas gegen positive und negative Fixtures validieren.
4. [x] Minimale Beispiele für alle vier Schemas automatisiert prüfen.
5. [x] Eval-Katalog, Baseline, Runner und Unit Tests technisch ausführen.
6. [ ] Initiale Eval-Baseline durch einen identifizierten Menschen fachlich freigeben.
7. [ ] Validator für referentielle Integrität, Hashes, Evidence-Grade-Regeln und Release-Gate vollständig implementieren.
8. [ ] Projektweite Retention-, Zugriffskontroll- und Signaturregeln festlegen.
9. [ ] Nach realen Pilotläufen prüfen, ob eine Datenbank oder Observability-Plattform erforderlich ist.
