# 04_CAUSAL_TOOLING.md

**Version:** 1.0  
**Stand:** 2026-08-27  
**Status:** ENTWURF ZUR ÜBERNAHME  
**Zweck:** Verbindlicher Router für spezialisierte Python-Bibliotheken bei DAG-Prüfung, Identifikation, kausaler Schätzung, Refutation und zeitserienspezifischer Causal Discovery.

---

# 1. Grundregel

Sobald eine kausale Methode als Code ausgeführt wird, verwendet der Agent eine geeignete spezialisierte Bibliothek, sofern eine gepflegte und für das Design passende Implementierung verfügbar ist. Kausale Kernalgorithmen werden nicht ad hoc neu geschrieben.

Ausnahmen sind nur zulässig, wenn:

- keine geeignete Bibliothek die benötigte Methode unterstützt,
- eine kleine Eigenimplementierung ausschließlich als unabhängiger Kontrolltest dient,
- oder eine veröffentlichte Replikation exakt die ursprüngliche Implementierung verlangt.

In jedem Ausnahmefall werden Grund, Tests und Abweichungen dokumentiert.

Der Status je Research-Version lautet:

- `TOOLING_REQUIRED`,
- `TOOLING_NOT_REQUIRED + Begründung`,
- oder `TOOLING_BLOCKED + fehlende Laufzeit/Bibliothek/API/Kompatibilität`.

Ein Tooling-Blocker beendet nicht automatisch rein beschreibende Discovery. Er blockiert jedoch jeden abhängigen kausalen Freeze oder Schätzschritt.

---

# 2. Was Bibliotheken nicht leisten

Eine Bibliothek kann die logischen und numerischen Operationen korrekt ausführen. Sie kann nicht aus Marktbeobachtungen allein garantieren, dass:

- der eingegebene DAG wahr ist,
- kein relevanter latenter Confounder fehlt,
- ein Instrument die Exclusion Restriction erfüllt,
- Positivity/Overlap gegeben ist,
- eine Event-Überraschung exogen ist,
- eine gefundene Kante stabil über Regime bleibt,
- oder der geschätzte Effekt handelbar ist.

Ein erfolgreiches API-Ergebnis erhöht den Claim-Level nicht. `ASSOCIATIONAL_PREDICTIVE`, `INTERVENTIONAL` und `COUNTERFACTUAL` werden ausschließlich nach `01_RESEARCH_STANDARD.md` vergeben.

Für diese Arbeit muss kein eigenes LLM trainiert werden. `EconML`, `DoubleML` und ähnliche Verfahren können im Research Nuisance- oder Effektmodelle fitten; das ist normale statistische Modellschätzung und kein Training eines Sprachmodells.

---

# 3. Verbindlicher Bibliotheksrouter

| Aufgabe | Primärer Default | Geeignet für | Nicht als |
|---|---|---|---|
| Model–Identify–Estimate–Refute | `DoWhy` | expliziter Graph, Identifikation, Schätzeraufruf, Placebos/Refuter/Sensitivität | Oracle für DAG-Wahrheit oder Identifikationsannahmen |
| DAG-, d-Separation- und Adjustierungsprüfung | `pgmpy` | Backdoor-/Frontdoor-Prüfung, Adjustmentsätze, graphische und probabilistische Abfragen | automatische Wahrheitssuche aus beliebigen Marktzeitreihen |
| CATE, Causal Forest, flexible DML-Schätzung | `EconML` | heterogene Effekte und ML-basierte Nuisance-Modelle nach Identifikation | Ersatz für Unconfoundedness, IV-Gültigkeit oder temporale Splitlogik |
| DML in unterstützten formalen Designs | `DoubleML` | orthogonale Scores, Cross-Fitting, PLR/IRM/IV/DID/RDD je unterstützter Modellklasse | universeller Kausalschätzer oder IID-Rechtfertigung für Zeitreihen |
| Zeitreihen-Causal-Discovery | `Tigramite` | PCMCI/PCMCI+, LPCMCI und passende Conditional-Independence-Tests | eindeutiger „wahrer DAG“ ohne Algorithmusannahmen |
| einfaches binäres Treatment | `causalinference` | Overlap, Propensity, Trimming, Matching, Blocking, Weighting, Least Squares | Standard für DML, Zeitreihen-Discovery oder allgemeine graphische Identifikation |

`causalinference` bezeichnet hier das separate Python-Paket. Es ist nicht mit `pgmpy.inference.CausalInference` zu verwechseln.

Pro Aufgabe wird eine primäre Bibliothek festgelegt. Zwei Bibliotheken für denselben Schritt sind nur sinnvoll, wenn der zweite Lauf vorab als unabhängige Replikation oder Kompatibilitätskontrolle definiert ist.

---

# 4. Auswahl nach Research-Frage

## 4.1 Rein prädiktive Reaktionsinnovation

Beispiel: Ein zeitlich OOS geschätztes Modell prognostiziert die 2Y- oder Nasdaq-Reaktion auf einen CPI-Schock; das Residuum dient als `REACTION_INNOVATION`.

Kausalbibliothek: `TOOLING_NOT_REQUIRED`, sofern kein kausaler Effekt oder DAG-Claim geschätzt wird. Eine gewöhnliche Statistik-/ML-Bibliothek genügt. Die Reaktionsinnovation bleibt prädiktiv.

## 4.2 Identifizierter durchschnittlicher Effekt

1. Estimand und DAG festlegen.
2. Adjustmentsatz/Identifikationsstrategie mit `DoWhy` oder `pgmpy` prüfen.
3. Den einfachsten designspezifisch geeigneten Schätzer wählen.
4. Schätzung und Refutation mit `DoWhy` beziehungsweise designspezifischer Bibliothek ausführen.
5. Mindestens eine unabhängige Diagnose vorsehen, etwa alternative zulässige Adjustierung, Negativkontrolle, Placebo oder Sensitivitätsanalyse.

## 4.3 Heterogene Effekte oder hochdimensionale Controls

1. Identifikation muss bereits bestanden sein.
2. `EconML` **oder** `DoubleML` entsprechend Estimand und unterstütztem Design wählen.
3. Overlap, Effektmodifikatoren, Nuisance-Learner und Splitlogik vor Freeze festlegen.
4. Bei Marktzeitreihen keine zufälligen IID-Folds verwenden, wenn sie zeitliche oder clusterbezogene Abhängigkeit verletzen; externe zeitliche/Cluster-Splits nutzen, soweit die gewählte API dies korrekt unterstützt.
5. CATE-/Policy-Ergebnisse benötigen eigene Multiplicity- und OOS-Regeln.

## 4.4 DAG-Prüfung ohne Effektschätzung

`pgmpy` ist der Default für d-Separation, graphische Struktur, Adjustmentsatzvalidierung und kausale Abfragen auf einem angenommenen Modell. `DoWhy` ist sinnvoll, wenn der Graph direkt in einen vollständigen Identifikations- und Refutationsworkflow übergeht.

## 4.5 Causal Discovery in Zeitreihen

`Tigramite` ist der Default für PCMCI-/PCMCI+-artige Aufgaben. Vor dem Lauf werden mindestens eingefroren:

- Variablen und Zeitauflösung,
- `tau_min`/`tau_max`,
- Conditional-Independence-Test,
- Link-Annahmen,
- Stationaritäts-/Regimelogik,
- Behandlung latenter Confounder,
- Signifikanz- und Multiple-Testing-Regel,
- sowie die zulässige Ausgabe als Kandidatengraph oder Äquivalenzklasse.

Das Ergebnislabel bleibt `CAUSAL_HYPOTHESIS`, solange keine zusätzliche Identifikationsstrategie besteht.

## 4.6 Matching/Propensity bei binärem Treatment

`causalinference` darf verwendet werden, wenn sein enger Funktionsumfang genau passt und die aktuelle Python-/NumPy-/SciPy-Kompatibilität durch Tests bestätigt ist. Bei neuen oder komplexeren Designs werden `DoWhy`, `EconML` oder `DoubleML` bevorzugt. Ein Wechsel darf nicht nur deshalb erfolgen, weil ein Paket einen günstigeren Punktschätzer liefert.

---

# 5. Reproduzierbare Umgebung

Keine Bibliothek wird stillschweigend in eine globale oder gemeinsam genutzte Python-Umgebung installiert. Für ein ausführbares Projekt wird eine isolierte, projektspezifische Umgebung oder das bereits freigegebene Projekt-Environment verwendet.

Vor der ersten Analyse sind zu protokollieren:

- Python- und Betriebssystemversion,
- Paketname und exakte installierte Version,
- Installationsquelle,
- Lockfile beziehungsweise vollständiger Environment-Export,
- Hauptklasse/-funktion und relevante Parameter,
- Zufallsseeds,
- Graph-, Estimand- und Datenversions-ID,
- Split-/Cross-Fitting-Logik,
- relevante Runtime-Warnungen und Deprecations,
- sowie Pfad oder Hash der erzeugten Konfiguration und Ergebnisse.

Ein unversioniertes `pip install <paket>` ist kein reproduzierbarer Freeze. Die konkrete Version wird erst nach Kompatibilitätsprüfung im Projekt-Lockfile fixiert; dieses Framework friert absichtlich keine universelle Paketkombination ein.

---

# 6. Kompatibilitäts- und Integritätsgate

Vor Freeze muss bei `TOOLING_REQUIRED` Folgendes `PASS` sein:

1. Import aller benötigten Pakete.
2. Ausgabe der tatsächlichen Versionen.
3. Ausführung der konkret verwendeten Haupt-API ohne unerklärte Warnung.
4. Synthetischer DAG mit bekanntem zulässigem Adjustmentsatz.
5. Synthetischer positiver Effekt mit bekanntem Vorzeichen.
6. Synthetischer Nullfall, in dem die Pipeline keinen stabilen Effekt erfinden darf.
7. Mindestens ein Collider-/post-treatment-Sentinel, wenn Adjustierung Teil der Analyse ist.
8. Zeit-/Leakage-Sentinel, wenn Marktzeitreihen oder Eventfenster verwendet werden.
9. Bei gekoppelten Bibliotheken ein End-to-End-Smoke-Test genau dieser Versionskombination.

Die Entscheidung lautet:

- `PASS`: nur für die protokollierte Versionskombination und API.
- `FAIL`: Implementierung oder Konfiguration ist falsch; kein Freeze.
- `BLOCKED`: notwendige Laufzeit, kompatible Version oder Diagnose fehlt; kein abhängiger kausaler Schritt.
- `NOT_REQUIRED`: keine ausführbare kausale Methode im Design.

Warnungen werden nicht pauschal unterdrückt. Sie werden zuerst klassifiziert und nur dann gezielt gefiltert, wenn ihre Ursache verstanden und im Artefakt dokumentiert ist.

---

# 7. Tool-spezifische Mindestregeln

## 7.1 DoWhy

- Graph, Treatment, Outcome und Estimand werden explizit versioniert.
- `identify_effect` oder die entsprechende aktuelle API wird vor `estimate_effect` ausgeführt.
- Die vom Identifikator verwendete Strategie und der Adjustmentsatz werden gespeichert.
- Refuter sind Falsifikationsversuche, keine Bestätigung der Wahrheit.
- Placebo-, Negativkontroll- und Sensitivitätstests werden designspezifisch ausgewählt; nicht jeder Refuter ist für jedes Design sinnvoll.

## 7.2 pgmpy

- Modelltyp und Kantenliste werden versioniert.
- Backdoor-/Frontdoor- und Adjustierungsabfragen werden gegen das konkrete Estimand geprüft.
- Ein technisch gültiger Adjustmentsatz ist nur relativ zum angenommenen Graph gültig.
- Probabilistische Query und interventionale Query werden sprachlich getrennt.

## 7.3 EconML und DoubleML

- Identifikationsannahme und Estimand stehen vor der Modellklasse fest.
- Treatment-, Outcome-, Confounder-, Instrument- und Effektmodifikatorrollen werden nicht vertauscht.
- Nuisance-Learner, Hyperparameter, Tuningraum und Cross-Fitting werden eingefroren.
- Overlap/Instrumentrelevanz und Abhängigkeit werden diagnostiziert.
- Ein flexibler Schätzer wird gegen eine einfachere, identisch identifizierte Baseline geprüft.
- Unsicherheitsangaben werden nur verwendet, wenn ihre Voraussetzungen zur Split-/Clusterstruktur passen.

## 7.4 Tigramite

- Conditional-Independence-Test und seine Verteilungsannahmen passen zu den Daten.
- Lag-Suche und Kantenraum zählen zum Multiple Testing.
- Gleichzeitige Kanten werden nicht durch bloße Reihenfolge innerhalb grober Bars kausal orientiert.
- Regime- oder Kontextverfahren benötigen vorab definierte Umgebungen oder eine eigene Validationslogik.

## 7.5 causalinference

- Nur für binäres Treatment und die tatsächlich unterstützten Propensity-/Matching-/Weighting-Schritte verwenden.
- Overlap, Trimming, Balance und Schätzervariante berichten.
- Vor Einsatz gegen die aktuelle Laufzeit testen.
- Nicht als Ersatz für Graphidentifikation, DML oder Zeitreihenverfahren verwenden.

---

# 8. Pflichtartefakt im Research Case

Abschnitt `E9` von `02_RESEARCH_CASE_TEMPLATE.md` enthält mindestens:

```text
TOOLING_STATUS:
TASK:
PRIMARY_LIBRARY:
PACKAGE_VERSION:
PYTHON_VERSION:
MAIN_API:
GRAPH_VERSION:
ESTIMAND_VERSION:
ADJUSTMENT_SET:
SEED:
SPLIT_LOGIC:
LOCKFILE_OR_ENV_HASH:
COMPATIBILITY_SMOKE_TEST:
SYNTHETIC_CAUSAL_SENTINEL:
WARNINGS:
INDEPENDENT_CHECK:
ALLOWED_CLAIM:
FORBIDDEN_CLAIM:
```

Ohne dieses Artefakt ist `E9 PASS` bei `TOOLING_REQUIRED` unzulässig.

---

# 9. Anti-Popanz-Regel

Der minimale ausreichende Stack gewinnt:

- keine Causal-Discovery-Bibliothek für eine bereits identifizierte einfache Eventregression,
- kein Causal Forest, wenn ein vorab spezifizierter linearer Effekt die Frage beantwortet,
- nicht DoWhy, pgmpy, EconML und DoubleML gleichzeitig ohne getrennte Aufgabe,
- kein GCM-/Counterfactual-Modell für einen rein prädiktiven Residualalarm,
- kein Paketwechsel nach Blick auf Validation-Ergebnisse.

Komplexität wird nur hinzugefügt, wenn sie eine vorher benannte Identifikations-, Schätz-, Heterogenitäts-, Refutations- oder Discovery-Frage beantwortet und inkrementell validiert werden kann.

---

# 10. Offizielle Dokumentation

- DoWhy User Guide: <https://www.pywhy.org/dowhy/v0.14/user_guide/>
- DoWhy Refutation Guide: <https://www.pywhy.org/dowhy/v0.14/user_guide/refuting_causal_estimates/index.html>
- pgmpy Causal Identification Guide: <https://pgmpy.org/guides/causal_identification.html>
- pgmpy `CausalInference` API: <https://pgmpy.org/api/generated/causal_inference/pgmpy.inference.CausalInference.CausalInference.html>
- EconML Documentation: <https://econml.azurewebsites.net/>
- DoubleML User Guide: <https://docs.doubleml.org/stable/guide/guide.html>
- Tigramite Documentation: <https://jakobrunge.github.io/tigramite/>
- Causalinference Documentation: <https://causalinferenceinpython.org/>

Vor jeder neuen Projektumgebung wird die aktuelle offizielle Dokumentation erneut geprüft. APIs, optionale Dependencies und getestete Paketkombinationen können sich ändern.
