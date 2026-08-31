# Research Framework – Quickstart

Dieser Kurzpfad ist der einzige verpflichtende Einstieg für jede neue Idee. Die
langen Normdokumente werden erst nach Status und Aufgabe geroutet; sie müssen
nicht mehr vollständig vorab in den Kontext geladen werden.

## 1. Was technisch erzwungen wird – und was nicht

| Ebene | Bedeutung |
|---|---|
| Maschinengeprüft | JSON-Schemas, Schema-Vertragstests, Eval-Scorer, Producer-Protokoll und CI-Checks können objektiv bestehen oder scheitern. |
| Evidenzgeprüft | Ein Status wie `SUPPORTED`, `PASS` oder `COMPLETE` ist nur belastbar, wenn das vorgeschriebene Evidenz-/Run-Artefakt existiert und die zugehörige Maschinenprüfung besteht. |
| Selbstdeklaration | Prosa, Checklistenhaken und ein vom ausführenden Agenten selbst gesetztes `COMPLETE` sind zunächst Behauptungen. Ohne Artefaktprüfung oder unabhängiges Review beweisen sie keine korrekte Durchführung. |

Normative Sprache steuert Verhalten, ersetzt aber keine technische Enforcement.
Das Framework beansprucht nur dort automatische Durchsetzung, wo ein Schema,
Test oder CI-Check benannt ist.

## 2. Optional: Ideen erzeugen

Wenn noch keine Rohidee existiert, darf vor dem Intake der ausführbare
Kurzfristgenerator verwendet werden:

```bash
python scripts/generate_hypotheses.py --output-dir artifacts/ideas-001 \
  --run-id generation:ideas-001 --markets FUTURES --max-candidates 20
```

Grundlage sind
[`generation/mechanism_catalog.v1.json`](generation/mechanism_catalog.v1.json)
und die vier Operatoren `PHASE_PATH`, `EXPECTATION_VIOLATION`,
`MECHANISM_CONNECTION` und `ASSUMPTION_RELAXATION`. Die Erzeugungsrouten sind
Constraint-first, Mikrostrukturzustand, Instrumentenverknüpfung,
Literaturreplikation und Beobachtung. Ein benannter gezwungener Akteur ist keine
universelle Bedingung.

Der Lauf schreibt einen validierten Generation-Run und minimale `INBOX`-Dateien.
Er führt kein Screening, Backtesting, Evidence Grading, Ranking oder Promotion
durch. Details und Filteroptionen stehen in
[`generation/README.md`](generation/README.md).

Der Generation-Run dokumentiert den erzeugten Kandidatenraum. Werden etwa alle
96 Kandidaten datenbasiert gescreent, wird vor dem ersten Ergebnis eine Familie
mit `planned_screen_count = 96` in
[`schemas/search_space.schema.json`](schemas/search_space.schema.json)
fixiert. Die Schwelle jedes
[`noise_screen`](schemas/noise_screen.schema.json) muss der dort hinterlegten
Multiplikitätskorrektur entsprechen.

## 3. Günstiger Intake

Eine neue Idee beginnt als `INBOX` nach
[`schemas/hypothesis_candidate.schema.json`](schemas/hypothesis_candidate.schema.json).
Benötigt werden zunächst nur:

- stabile IDs und Zeitstempel,
- Herkunft,
- ein Rohsatz der Idee,
- bereits verbrauchte Informations-/Datenreferenzen,
- `intake_status = INBOX`,
- ein leeres `transition`-Objekt.

Siehe [`examples/hypothesis_candidate.inbox.json`](examples/hypothesis_candidate.inbox.json).
Wird die Idee beim Screening verworfen, genügt der kurze `REJECTED`-Datensatz mit
Begründung; siehe
[`examples/hypothesis_candidate.rejected.json`](examples/hypothesis_candidate.rejected.json).

Erst `PROMOTED` verlangt vollständigen Scope, einen beobachtbaren
Akteurs-/Zwangs-Record mit konkurrierender Akteurshypothese, einen bestandenen
Noise Screen oder einen begründeten theorie-/event-/replikationsbasierten Waiver,
beobachtbare Footprints, Alternativerklärungen, Datenanforderungen, frühe
Machbarkeit, die drei getrennten Evidenzstufen und einen Record zur
Variablenauswahl. Bei
`PREDEFINED` genügen Begründung und beibehaltene Konstrukte. `DATA_DRIVEN` und
`HYBRID` verlangen zusätzlich Kandidatenuniversum, Selektionsdaten und deren
Rolle, Outcome-Sichtbarkeit, Methode, effektive Kandidatenzahl, Suchraum und
Kontrollen gegen Auswahlbias. SHAP, Impurity- oder andere
Feature-Importance-Verfahren sind mögliche Diagnosen, aber weder Pflicht noch
Kausalitätsnachweis. Promotion bestätigt keine Evidenzstufe.

## 4. Dokumentrouter nach Promotion

Nach `PROMOTED` wird nicht pauschal alles geladen:

1. [`00_RESEARCH_AGENT_README.md`](00_RESEARCH_AGENT_README.md) für Gate- und Routinglogik.
2. [`01_RESEARCH_STANDARD.md`](01_RESEARCH_STANDARD.md) für den verbindlichen Research-Pfad.
3. [`02_RESEARCH_CASE_TEMPLATE.md`](02_RESEARCH_CASE_TEMPLATE.md) erst beim Anlegen des konkreten Research Case.
4. Aus [`03_RESEARCH_METHODS.md`](03_RESEARCH_METHODS.md) nur die durch den Methodenrouter ausgewählten Abschnitte.
5. [`04_CAUSAL_TOOLING.md`](04_CAUSAL_TOOLING.md) nur bei ausführbarer kausaler Kernoperation; sonst dokumentiertes `TOOLING_NOT_REQUIRED`.
6. Aus [`05_AGENT_OPERATIONS.md`](05_AGENT_OPERATIONS.md) die zum erzeugten Artefakt oder Systemwechsel gehörenden Abschnitte.

Das Nicht-Überspringen-Protokoll gilt innerhalb des aktivierten Pfads. Nicht
aktivierte optionale Methoden erzeugen keine Serien begründeter `N/A`-Einträge.

## 5. Nicht verhandelbare Kernregeln

- Beobachtung, Mechanismus, Forward-OOS-Prognose und ausführbare Netto-Edge bleiben getrennte Aussagen.
- Claim-Level (`ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`) und Validierungs-/Handelsstatus (`mechanism_supported / forward_predictive_oos / executable_net_edge`) sind unabhängige Achsen. Keine Achse stuft die andere automatisch hoch.
- Kausale Identifikation darf als SCM/DAG, Potential-Outcomes-Design, strukturell-ökonometrisches oder anderes explizites Identifikationsmodell formuliert werden. Die Notation entscheidet nicht über den Claim-Level.
- Bereits betrachtete Daten werden im Informationsbudget erfasst.
- Erzeugte und tatsächlich gescreente Kandidaten werden vollständig im Search-Space-Register gezählt; ein Noise-Screen-`PASS` ist keine Evidenz.
- Prädiktoren müssen zum Entscheidungszeitpunkt tatsächlich verfügbar sein.
- Materielle Regeln werden vor unabhängiger Evaluation eingefroren.
- Kosten, Latenz, Fills und gegebenenfalls Queue/Borrow werden vor einem Netto-Edge-Claim geprüft.
- `IDENTIFIED_CAUSAL_LEVER` erfordert ein bestandenes Identifikationsgate und ein Estimand-Artefakt.
- `IMPLEMENTATION_CONSTRAINT` erfordert ein validiertes Phänomen und bestandene Umsetzbarkeitsprüfung.

Die letzten beiden Regeln sind in
[`schemas/constraint_assessment.schema.json`](schemas/constraint_assessment.schema.json)
maschinenprüfbar.

## 6. Framework-Integrität prüfen

Plattformneutral:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_framework.py
```

Windows/PowerShell bleibt als zweiter, in CI geprüfter Einstieg erhalten:

```powershell
.\scripts\validate_framework.ps1
```

Beide Pfade prüfen Framework-Verträge. Der mitgelieferte 1,000-Eval-Lauf ist nur
`PROTOCOL_SMOKE` und kein Qualitätsbeleg für einen Live-Agenten.

## 7. Echten Agenten evaluieren

`evals/produce_results.py` sendet jedem Agentenadapter nur Fallinput und
Outputvertrag – niemals die erwarteten Assertions. Es unterstützt einen lokalen
Subprozess oder einen JSON/HTTP-Endpunkt. Anschließend muss der Release-Check
explizit `LIVE_AGENT` verlangen:

```bash
python evals/produce_results.py --output artifacts/live-results.json \
  --run-id candidate-model-001 --run-kind LIVE_AGENT \
  --adapter-id local-agent --command-json '["python","my_agent_adapter.py"]'

python scripts/validate_framework.py \
  --live-results artifacts/live-results.json \
  --report artifacts/live-eval-report.json
```

Ohne produziertes `LIVE_AGENT`-Artefakt ist nur die Framework-Integrität geprüft,
nicht die Qualität einer Modell- oder Promptänderung.

## 8. Bekannte offene Validierungslücke

Das Repository enthält derzeit keinen vollständig durchgearbeiteten realen
Research Case. Schema-Fixtures und Eval-Fälle testen Verträge, nicht die
praktische Bewährung des gesamten Research-Prozesses. Bis ein geeigneter Fall
vorliegt, darf das Framework deshalb nicht als end-to-end praxiserprobt
bezeichnet werden.
