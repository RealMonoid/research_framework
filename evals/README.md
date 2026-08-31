# Eval-Producer, Scorer und Regression Gate

Dieses Verzeichnis trennt drei Dinge, die nicht verwechselt werden dürfen:

1. Ein handgeschriebenes Fixture prüft Vertrag und Scorer.
2. Der Producer ruft einen realen Agentenadapter blind auf.
3. Der Scorer bewertet das produzierte Ergebnis gegen Katalog und Baseline.

Producer und Scorer benötigen nur die Python-Standardbibliothek. Die
plattformneutrale Schema-Suite verwendet die gepinnte Development-Abhängigkeit
aus `requirements-dev.txt`.

## Artefakte

- `catalog.v1.json`: versionierte Inputs und erwartete Assertions.
- `examples/smoke-results.v1.json`: handgeschriebenes `PROTOCOL_SMOKE`-Fixture
  mit `schema_version = eval-results.v2`; kein Agentenqualitätsbeleg.
- `baseline.v1.json`: Mindestwerte und akzeptierte Vergleichsscores.
- `produce_results.py`: blinder COMMAND-/HTTP_JSON-Producer.
- `run_evals.py`: Strukturprüfung, Scoring und Regression Gate.
- `tests/test_produce_results.py`: Producerblindheit und Run-Klassen.
- `tests/test_run_evals.py`: Scoring, Fehlerpfade und Regressionserkennung.

Der Katalog prüft zusätzlich die Ablaufsteuerung des Forschungsleiters: die
zwingende Begriffsprüfung vor der Operationalisierung einer unvollständigen
Prosastrategie, die Bedingungsanalyse nach einer vorläufigen Definition, die
Fortsetzungsprüfung nach einem nicht positiven Ergebnis und den Gegenfall einer
reinen Ergebniserklärung ohne unnötigen Fachagenten.

Katalog, Ergebnis und Baseline müssen dieselbe `catalog_version` nennen. Änderungen
an Input, Erwartung, Gewichtung oder Fallbedeutung erhöhen die Katalogversion.

## Framework-Integrität

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_framework.py
```

PowerShell bleibt als separat in CI geprüfter Einstieg erhalten:

```powershell
.\scripts\validate_framework.ps1
```

Ohne `--live-results` prüfen beide Pfade Framework- und Protokollintegrität, nicht
die Qualität eines Modells oder Prompts.

## Blinder Producer

Der Request enthält `case_id`, Capability, Beschreibung, Fallinput, Quellen und
Outputvertrag. `expected.assertions` wird niemals an den Adapter gesendet. Jeder
Katalogfall erhält einen eigenen Aufruf.

Lokaler Adapter – das JSON-Array wird ohne Shell ausgeführt:

```bash
python evals/produce_results.py \
  --output artifacts/live-results.json \
  --run-id candidate-agent-001 \
  --run-kind LIVE_AGENT \
  --adapter-id local-agent \
  --command-json '["python","my_agent_adapter.py"]'
```

Providerneutraler HTTPS-Adapter:

```bash
python evals/produce_results.py \
  --output artifacts/live-results.json \
  --run-id candidate-agent-002 \
  --run-kind LIVE_AGENT \
  --adapter-id http-agent \
  --http-endpoint https://agent.example/eval \
  --token-env EVAL_AGENT_TOKEN
```

Der Adapter liest genau ein JSON-Request von stdin beziehungsweise aus dem
HTTP-Body und liefert genau ein JSON-Fallergebnis. Der Producer assembliert alle
Fälle, prüft Struktur und Quellenreferenzen und schreibt das Ergebnis atomar.
Tokenwerte werden weder gespeichert noch gehasht.

## Ergebnisadapter

Jeder Fall besitzt ein `claims`-Objekt. Ein Claim enthält mindestens:

```json
{
  "statement_class": "SOURCE_FACT",
  "evidence_status": "SUPPORTED",
  "source_ids": ["source_from_the_case"]
}
```

Zulässige Klassen sind `SOURCE_FACT`, `CALCULATED_VALUE`, `ESTIMATE`,
`INFERENCE`, `FORECAST` und `HUMAN_JUDGMENT`. Evidenzzustände sind `SUPPORTED`,
`PARTIAL`, `UNKNOWN`, `CONFLICTING`, `STALE` und `NOT_APPLICABLE`. Quellen-IDs
dürfen nur auf Quellen des jeweiligen Katalogfalls zeigen.

## Run-Klassen

- `PROTOCOL_SMOKE`: Vertragstest; kein Qualitätsclaim.
- `LIVE_AGENT`: über COMMAND oder HTTP_JSON produzierter Agentenlauf.
Ein `LIVE_AGENT`-Ergebnis darf keinen `REFERENCE_FIXTURE`-Producer deklarieren.
Eine Modell-/Promptfreigabe muss die Laufart ausdrücklich verlangen:

```bash
python evals/run_evals.py \
  --results artifacts/live-results.json \
  --require-run-kind LIVE_AGENT \
  --report artifacts/live-eval-report.json \
  --verbose
```

Das mitgelieferte Score-1,000-Fixture scheitert an diesem Release-Gate, weil es
`PROTOCOL_SMOKE` ist.

## Assertions und Exitcodes

Unterstützte Operatoren sind `equals`, `set_equals`, `approx_equals`, `is_empty`
und `exists`. Jede Assertion trägt Metrik, Gewicht und `critical`; fehlende Pfade
scheitern explizit.

- Exit `0`: angeforderte Struktur-, Qualitäts- und Regressionsgates bestanden.
- Exit `1`: mindestens ein Qualitäts-, Laufart- oder Regressionsgate scheiterte.
- Exit `2`: Struktur, Konfiguration, Producer oder Bericht ist fehlerhaft.

`baseline.v1.json` verlangt insgesamt mindestens 0,95, für kritische Assertions
1,00 und für alle Safety-/Governance-Metriken die dort dokumentierten Werte.
`max_metric_drop` und `max_case_drop` sind 0,0.

## CI und Freigabe

`framework-integrity.yml` führt bei Push und Pull Request den Linux/Python- und
Windows/PowerShell-Pfad aus. Dieser Check kann als Branch-Protection-Status
verlangt werden, bleibt aber ein Integritätscheck.

`live-agent-eval.yml` ist ein manueller Release-Workflow. Er benötigt die
Repository-Variable `EVAL_AGENT_ENDPOINT` und optional das Secret
`EVAL_AGENT_TOKEN`, produziert ein `LIVE_AGENT`-Artefakt und erzwingt danach das
Live-Gate. Ohne konfigurierten Adapter gibt es keinen Live-Qualitätsclaim.

## Verbesserungsregel

Ein beobachteter Agentenfehler wird zuerst als reproduzierbarer Katalogfall oder
Assertion fixiert. Danach werden Baseline und Kandidat über denselben blinden
Producer ausgeführt. Erwartungen werden nicht an die fehlerhafte Ausgabe
angepasst; Baselineänderungen benötigen Review. Smoke-Fixture und Beispielbaseline
belegen ausschließlich den Harness, nicht den Agenten.
