# Eval- und Regressionsgrundgerüst

Dieses Verzeichnis enthält einen kleinen, deterministischen Qualitätsgate für die
operative Research-Agent-Schicht. Es benötigt ausschließlich die
Python-Standardbibliothek. Bewertet wird ein strukturierter Ergebnisadapter, nicht
der Wortlaut einer Antwort. Dadurch ist jede Bewertung reproduzierbar und bis zur
einzelnen Erwartung erklärbar.

## Artefakte und Versionierung

- `catalog.v1.json` ist der versionierte Fallkatalog (`eval-catalog.v1`).
- `examples/smoke-results.v1.json` zeigt den erwarteten Ergebnisadapter
  (`eval-results.v1`).
- `baseline.v1.json` hält Freigabeschwellen und die zuletzt akzeptierten Scores
  (`eval-baseline.v1`).
- `run_evals.py` validiert, bewertet und vergleicht mit der Baseline.
- `tests/test_run_evals.py` prüft Smoke-Pfad, Regressionserkennung und strukturelle
  Fehler.

`catalog_version` folgt SemVer. Eine Änderung an Eingaben, Erwartungen, Gewichtung
oder Fallbedeutung erhöht mindestens die Minor-Version; inkompatible Änderungen am
Adapter oder an der Semantik erhöhen die Major-Version. Katalog, Ergebnisse und
Baseline müssen dieselbe exakte Katalogversion nennen. Die `schema_version` wird
nur bei einer Änderung des jeweiligen Dateivertrags erhöht.

## Schnellstart

Vom Projektwurzelverzeichnis:

```powershell
.\scripts\validate_framework.ps1
```

Dieser Gesamtcheck prüft zuerst alle operativen JSON-Schemas einschließlich
negativer Fixtures und führt danach Eval-Gate und Unit Tests aus. Die Eval-Schicht
kann auch einzeln ausgeführt werden:

```powershell
python evals/run_evals.py
python -m unittest discover -s evals/tests -v
```

Wenn unter Windows nur der Launcher verfügbar ist, kann `py -3` anstelle von
`python` verwendet werden. Falls im lokalen Codex-Desktop kein System-Python
installiert ist, steht in der aktuellen Workspace-Runtime außerdem diese gebündelte
Alternative bereit:

```powershell
$codexPython = Join-Path $env:USERPROFILE `
  '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $codexPython evals/run_evals.py
```

Der Pfad ist installationsabhängig; die vom Workspace gemeldete Python-Runtime ist
maßgeblich. Ein eigener Lauf wird so geprüft:

```powershell
python evals/run_evals.py `
  --results path/to/results.json `
  --report path/to/eval-report.json `
  --verbose
```

Exitcodes sind absichtlich CI-tauglich:

- `0`: Struktur, Schwellen und Regressionstest bestanden.
- `1`: mindestens ein Qualitätsgate oder Regressionstest fehlgeschlagen.
- `2`: Katalog, Resultat oder Baseline ist strukturell ungültig bzw. ein Bericht
  konnte nicht geschrieben werden.

## Ergebnisadapter

Eine Ergebnisdatei enthält Metadaten und ein Objekt `cases`, das jeden Katalogfall
genau einmal abbildet. Jeder Fall besitzt ein `claims`-Objekt, dessen Claims
mindestens diese Felder tragen:

```json
{
  "statement_class": "SOURCE_FACT",
  "evidence_status": "SUPPORTED",
  "source_ids": ["source_from_the_case"]
}
```

Zulässige epistemische Klassen sind `SOURCE_FACT`, `CALCULATED_VALUE`, `ESTIMATE`,
`INFERENCE`, `FORECAST` und `HUMAN_JUDGMENT`. Die Evidenzzustände sind
`SUPPORTED`, `PARTIAL`, `UNKNOWN`, `CONFLICTING`, `STALE` und `NOT_APPLICABLE`.
Eine `source_id` darf nur auf eine Quelle im jeweiligen Katalogfall zeigen.

Erwartungen stehen maschinenlesbar unter `expected.assertions`. Unterstützt werden:

- `equals`: typstrikter exakter Vergleich;
- `set_equals`: reihenfolgeunabhängiger Vergleich von Arrays;
- `approx_equals`: numerischer Vergleich mit expliziter `tolerance`;
- `is_empty`: Prüfung auf eine leere Collection oder Zeichenkette;
- `exists`: Prüfung, ob ein Pfad vorhanden ist.

Jede Assertion trägt Metrik, Gewicht und `critical`. Fehlende Pfade zählen als
nicht bestanden, nicht als stilles `null`.

## Testpyramide

```text
              End-to-End: echte Agentenläufe (wenige, separat)
           Integration: Ergebnisadapter gegen alle Katalogfälle
        Unit: Parser, Strukturregeln, Operatoren und Regressionen
```

### Unit-Ebene

Viele schnelle Tests prüfen JSON-Verträge, eindeutige IDs, Quellenreferenzen,
Assertion-Operatoren, Scoreberechnung und Exitcodes. Ziel: alle deterministischen
Codepfade des Harness; jeder behobene Harness-Fehler erhält einen Test.

### Integrationsebene

Der Smoke-Adapter durchläuft alle acht Kernfähigkeiten gemeinsam: Quellenzuordnung,
Fakt-vs-Inferenz, fehlende Evidenz/`UNKNOWN`, widersprüchliche Quellen, veraltete
Quelle, Berechnung, Thesis-Update und Thesis-Invalidierung. Ziel: 100 Prozent der
kritischen Assertions und kein Rückgang gegenüber der akzeptierten Baseline.

### End-to-End-Ebene

Ein realer Agent oder eine Pipeline erzeugt den Ergebnisadapter aus denselben
Kataloginputs. Solche Läufe können wegen Modellvarianz teurer sein; sie werden vor
Freigaben und bei Änderungen an Modell, Prompt, Retrieval oder Tools ausgeführt.
Die deterministischen Assertions bleiben das abschließende Gate. Zusätzliche
stochastische oder menschlich bewertete Evals gehören in einen späteren,
gesonderten Katalog und dürfen diese Safety-Gates nicht ersetzen.

## Metriken und Gates

| Metrik | Mindestwert | Zweck |
|---|---:|---|
| `overall_score` | 0,95 | gewichtete Summe aller Assertions |
| `critical_assertion_pass_rate` | 1,00 | kein kritisches Safety-/Governance-Versagen |
| `citation_accuracy` | 0,95 | korrekte Quelle und Fundstelle |
| `epistemic_classification_accuracy` | 0,95 | Fakt, Rechnung und Inferenz sauber getrennt |
| `unknown_safety_rate` | 1,00 | keine erfundene Antwort bei Evidenzlücke |
| `contradiction_handling_rate` | 1,00 | Konflikte sichtbar und nicht voreilig aufgelöst |
| `source_freshness_rate` | 1,00 | keine veraltete Quelle für zeitkritische Werte |
| `calculation_accuracy` | 1,00 | reproduzierbare korrekte Berechnung |
| `thesis_governance_accuracy` | 1,00 | korrektes Update bzw. Invalidierung |

Zusätzlich ist in `baseline.v1.json` sowohl `max_metric_drop` als auch
`max_case_drop` auf `0.0` gesetzt. Eine Änderung kann somit trotz Erreichen eines
absoluten Mindestwerts als Regression scheitern. Die Strukturvalidierung ist ein
vorgelagertes hartes Gate und wird nicht in einen Prozentwert verwässert.

## Kontrollierter Verbesserungs-Workflow

1. Einen beobachteten Fehler mit Input, Agentenausgabe und erwarteter Eigenschaft
   sichern; sensible Inhalte vor Aufnahme bereinigen.
2. Den kleinsten repräsentativen Katalogfall oder eine neue Assertion hinzufügen.
   Der Test muss mit der fehlerhaften Ausgabe reproduzierbar scheitern.
3. Prompt, Retrieval, Tooling oder Code ändern; keine Erwartung an die fehlerhafte
   Ausgabe anpassen.
4. Unit-Tests und den vollständigen Katalog ausführen. Struktur-, Schwellen- und
   Regressionsgate müssen bestehen.
5. Änderung und Eval-Bericht reviewen. Kritische Fehler blockieren die Freigabe.
6. Erst nach dokumentierter Freigabe eine neue Baseline erzeugen. Score-Rückgänge
   benötigen eine ausdrückliche, begründete Ausnahme und dürfen nicht durch bloßes
   Überschreiben der Baseline verborgen werden.

Die Beispiel-Baseline ist eine Referenz für den Adapter, kein Beleg für die Qualität
eines noch nicht angeschlossenen LLM-Agenten. Für eine echte Freigabe wird sie durch
Scores eines nachvollziehbaren, reviewten Agentenlaufs ersetzt.

## Erweiterungsregeln

- Jeder Fall soll eine Fehlerklasse isolieren und mindestens eine kritische
  Assertion besitzen.
- Deterministische Eigenschaften werden direkt geprüft; stilistische Bewertungen
  gehören nicht in diesen Katalog.
- Neue Quellen erhalten stabile IDs, Publikations- und Zugriffszeit sowie eine
  Kennzeichnung ihrer Autorität.
- Neue Metriken müssen im Runner registriert, im README beschrieben und mit einem
  Test abgesichert werden.
- Secrets, personenbezogene Daten und lizenzrechtlich unzulässige Volltexte dürfen
  nicht in Fixtures aufgenommen werden.
