# 02_RESEARCH_CASE_TEMPLATE.md

**Template-Version:** 1.8
**ANWEISUNG:** Diese Datei pro Research-Projekt kopieren. Kein Pflichtfeld löschen. Nicht anwendbare Felder mit `N/A + Begründung` ausfüllen. Unbekannte Pflichtfelder mit `BLOCKED + fehlende Information` markieren.

**BEDINGTE AKTIVIERUNG:** Die Abschnitte `U–Y` werden erst geöffnet, wenn Abschnitt `T` mit `VALIDATED_PHENOMENON` abgeschlossen **und** Strategy Engineering ausdrücklich als nächster Schritt beschlossen wurde. Bei validiertem, aber nicht fortgesetztem Phänomen erhält der Block `DEFERRED_AFTER_VALIDATION`; ohne validiertes Phänomen erhält er `NOT_ACTIVATED_BY_T_GATE`. In beiden Fällen wird er nicht feldweise mit `N/A` befüllt. Abschnitt `Z` bleibt während des gesamten Projekts aktiv.

**FRÜHER GATE-ABBRUCH:** Beendet ein Gate die aktuelle Research-Version vor Abschnitt `T`, werden alle dadurch nicht mehr erreichbaren späteren Abschnitte einmalig als `NOT_REACHED_DUE_TO_FAILED_GATE` markiert. Sie werden nicht feldweise ausgefüllt; Abschnitt `Z` bleibt aktiv.

**FRÜHES BLOCKED:** `BLOCKED` beendet die Version nicht. Folgeabschnitte bleiben unangetastet, `Z` protokolliert Blocker und fehlende Information, und die Bearbeitung wird erst nach Auflösung in derselben Version fortgesetzt. `NOT_REACHED_DUE_TO_FAILED_GATE` gilt ausschließlich nach `FAIL`.

**GATE-STATUS-MAPPING:** `PASS → PHASENSTATUS COMPLETE`, `FAIL → PHASENSTATUS FAILED`, `BLOCKED → PHASENSTATUS BLOCKED`. Nach `FAIL` oder `BLOCKED` beginnt kein abhängiger Folgeschritt.

---

# A. Research-Metadaten

| Feld | Eintrag |
|---|---|
| Research-ID | |
| Research-Titel | |
| Version | |
| Research-Status | `DISCOVERY / DEVELOPMENT / CANDIDATE_HYPOTHESIS / IN_TEST / NO_PHENOMENON / INCONCLUSIVE / VALIDATED_PHENOMENON / ECONOMICALLY_UNTRADEABLE / ACTIVE_STRATEGY_CANDIDATE / ACTIVE / UNDER_OBSERVATION / SUSPENDED / REVALIDATED / REJECTED` |
| Erstellt am | |
| Letzte Änderung | |
| Freeze-Datum | |
| Verantwortlicher Researcher/Agent | |
| Hypothesen-Version | |
| Claim-Level | `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL` |
| Estimand-Version | `N/A bei ASSOCIATIONAL_PREDICTIVE` |
| Identifikationsstatus | `NOT_REQUIRED_PREDICTIVE / PASS / FAIL / BLOCKED` |
| DAG-Version | |
| Tooling-Status | `TOOLING_REQUIRED / TOOLING_NOT_REQUIRED / TOOLING_BLOCKED` |
| Tooling-Manifest-Version | |
| Kostenmodell-Version | |
| Primärer Datensatz | |
| Operational-Governance-Version | |
| Run-Manifest-Register | `Pfad/URI zum Register aller Run-IDs dieser Research-Version` |
| Evidence-Ledger-Version | |
| Review-Ledger-Version | |
| Eval-Suite-Version | |
| Letzter Regression-Gate-Status | `PASS / FAIL / BLOCKED / NOT_RUN_NO_AGENT_CHANGE` |
| Intake-Idea-ID / Intake-Version | |
| Ereignisklasse | `INFORMATION_EVENT / SCHEDULED_STRUCTURAL_EVENT / CONTINUOUS_ENDOGENOUS_MECHANISM / RETURN_DECOMPOSITION` |
| Mechanismus-Evidenz | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` |
| Forward-OOS-Prognose | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` |
| Ausführbare Netto-Edge | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` |

## A1. Aktive Projektquellen zum Startzeitpunkt

| Quelle | Version/Stand | Relevanz für dieses Research |
|---|---|---|
| ACTIVE_DOCUMENTS.md | | |
| Trading_System.md | | |
| Projekt-Workflow.md | | |
| Chart_Indikator_Settings.md | | |
| Masterjournal.md | | |
| Sonstige | | |

## A2. Operatives Artefaktregister

Das Register referenziert die maschinenlesbaren Artefakte nach `05_AGENT_OPERATIONS.md`. Ein Hash bezieht sich auf den unveränderten gespeicherten Inhalt, nicht auf einen später neu erzeugten Export.

| Artefakttyp | ID/Version | Schema-/Formatversion | Pfad/URI | Content-Hash | Status |
|---|---|---|---|---|---|
| Run-Manifest | | | | | `COMPLETE / FAILED / BLOCKED` |
| Evidence Ledger | | | | | `COMPLETE / INCOMPLETE / CONFLICTED / BLOCKED` |
| Review Ledger | | | | | `NO_REVIEW / OPEN / ACCEPTED / REJECTED / SUPERSEDED` |
| Forecast Ledger | | | | | `N/A / OPEN / PARTIALLY_RESOLVED / RESOLVED` |
| Eval-Ergebnis | | | | | `PASS / FAIL / BLOCKED / NOT_RUN` |
| Hypothesen-Intake | | `1.1.0` | | | `INBOX / SCREENED / MERGED / REJECTED / PROMOTED` |

## A3. Academic-Source-Protokoll

**ACADEMIC_SOURCE_STATUS:** `REQUIRED / NOT_RELEVANT + Begründung / BLOCKED + fehlende Information`

Bei `REQUIRED` gelten **05_AGENT_OPERATIONS.md §5.4** und
`schemas/evidence.schema.json` Version 2.0.0. Gesucht und bewertet werden konkrete
Fassungen wissenschaftlicher Arbeiten, nicht nur Suchtreffer oder Zitationsangaben.

### A3.1 Recherche-Coverage

| Kanal | Suchanfrage/Filter | Suchzeitpunkt | Ergebnis | Nachweis/URI |
|---|---|---|---|---|
| The Journal of Finance | | | `SEARCHED_HIT / SEARCHED_NO_HIT / NOT_RELEVANT + Grund / BLOCKED + Grund` | |
| Journal of Financial Economics | | | `SEARCHED_HIT / SEARCHED_NO_HIT / NOT_RELEVANT + Grund / BLOCKED + Grund` | |
| arXiv q-fin | | | `SEARCHED_HIT / SEARCHED_NO_HIT / NOT_RELEVANT + Grund / BLOCKED + Grund` | |
| Weitere Journals/Working-Paper-Reihen/Repositories | | | | |

### A3.2 Quellen-, Versions- und Integritätsregister

| work_id | source_id | Studientyp | Publikationsstatus | konkrete Fassung | Autoren/Jahr | Venue | DOI | arXiv-ID / q-fin-Kategorie / Version | Integrity-Status / geprüft am / Notice | Code | Daten | unabhängige Replikation / source_ids | zulässige Evidenzverwendung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | |

### A3.3 Versionsfamilien und Unabhängigkeit

| geprüfte source_ids | Entscheidung | work_id(s) | Begründung | Prüfer/Zeitpunkt |
|---|---|---|---|---|
| | `SAME_WORK / DISTINCT_WORK / UNCERTAIN` | | | |

Journalname, DOI, Zitationszahl und q-fin-Kategorie erhöhen den Evidence Grade
nicht automatisch. `PREPRINT`, `WORKING_PAPER` und `OTHER` werden als vorläufig
gekennzeichnet; eine konkrete arXiv-Fassung wird mit Versionssuffix eingefroren.
Correction, Expression of Concern, Retraction, Withdrawal sowie Code-, Daten- und
Replikationsstatus werden vor Freeze und Freigabe erneut geprüft.

## A4. Research Scope

| Feld | Eintrag |
|---|---|
| Markt und Instrument(e) | |
| Venue(s) und konkrete Datenfeeds | |
| Book-Sicht | `VENUE_DIRECT / CONSOLIDATED / TOP_OF_BOOK / L2 / L3 / N/A + Grund` |
| Handelsphase | `PRE_MARKET / OPENING_AUCTION / CONTINUOUS / CLOSING_AUCTION / POST_MARKET / OVERNIGHT / CROSS_SESSION / OTHER` |
| Venue-Kalender, Zeitzone und DST-Regel | |
| Primäre Zeitbasis | `CLOCK_TIME / EVENT_TIME / TRADING_DAY / ANDERE + Definition` |
| Prognose-/Outcome-Horizont | |
| Ereignisklasse | `INFORMATION_EVENT / SCHEDULED_STRUCTURAL_EVENT / CONTINUOUS_ENDOGENOUS_MECHANISM / RETURN_DECOMPOSITION` |
| News-/Makro-Policy | `INCLUDED_AS_SIGNAL / NOT_USED_AS_SIGNAL / FILTER_KNOWN_EVENTS / SCHEDULED_EVENT_STUDY` |
| verwendete News-/Eventfeeds und Abdeckungszeitraum | `Pflicht bei FILTER_KNOWN_EVENTS; sonst N/A + Grund` |
| Ausschlussfenster und Timestamp-Konvention | `Pflicht bei FILTER_KNOWN_EVENTS; sonst N/A + Grund` |
| bekannte Coverage-Lücken | |
| explizit ausgeschlossene Research-Fragen | |

**Scope-Regel:** `NOT_USED_AS_SIGNAL` bedeutet nicht, dass Ereignisse aus der
Stichprobe entfernt wurden. Der Ausdruck „newsfrei“ wird nur als Kurzform einer
dokumentierten `FILTER_KNOWN_EVENTS`-Policy verwendet und immer zusammen mit
Feed-Abdeckung und bekannten Lücken berichtet.

## A5. Vorgelagerte Hypothesen-Inbox

Die Rohidee wird vor `B` gegen `schemas/hypothesis_candidate.schema.json`
persistiert. `PROMOTED` öffnet ausschließlich die Phase-0-Vorprüfung; es ist kein
positiver Evidenzbefund.

| Feld | Eintrag |
|---|---|
| Idea-ID / Version | |
| Intake-Status | `INBOX / SCREENED / MERGED / REJECTED / PROMOTED` |
| Herkunft / konkrete Quelle | |
| Ideenklasse | `ASSOCIATIONAL_PATTERN / PREDICTIVE_PRECEDENCE / MECHANISM_CANDIDATE / STRUCTURAL_FLOW_CANDIDATE / RELATIVE_VALUE_CANDIDATE / EVENT_RESPONSE_CANDIDATE / RETURN_DECOMPOSITION_CANDIDATE / OTHER` |
| Mechanismenfamilie | nicht abschließendes Routerlabel oder `UNCLASSIFIED` |
| vermuteter Akteur / Zwang / Marktstruktur | |
| beobachtbarer Footprint | |
| erwartetes Outcome und Horizont | |
| wichtigste Alternativerklärungen | |
| benötigte Auflösung / Datenfelder / Venue-Coverage | |
| Clock-Sync-, Sequenz- und Beobachtbarkeitsanforderungen | |
| frühe Kosten-, Latenz-, Queue-, Borrow-, Funding- oder Leg-Risk-Hürde | |
| bereits betrachtete Dataset-IDs / aktuelle Datenrolle | |
| Dublette / merged_into_id | |
| Screening-Entscheidung und Grund | |
| bei PROMOTED: nächste Research-ID und Phase-0-Frage | |

### A5.1 Getrennte Evidenzstufen

| Stufe | Status | tragende Evidenz/Run-IDs | Begründung / nächster Test |
|---|---|---|---|
| `mechanism_supported` | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` | | |
| `forward_predictive_oos` | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` | | |
| `executable_net_edge` | `UNKNOWN / SUPPORTED / NOT_SUPPORTED / BLOCKED` | | |

Die Stufen werden nicht kaskadenartig hochgestuft. Insbesondere belegt ein
Mechanismuspaper keine Forward-Prognose, ein kontemporärer Zusammenhang keine
zukünftige Rendite und ein Midquote-Effekt keine ausführbare Netto-Edge.

---

# B. Phase 0 – Machbarkeit und Informationsbudget

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

## B1. Vorläufige Beobachtung

**Was wurde beobachtet?**

...

**Warum ist es forschungswürdig?**

...

**Was soll ausdrücklich noch NICHT behauptet werden?**

...

## B2. Primäre Outcome-Skala

| Feld | Eintrag |
|---|---|
| Primärer Outcome | |
| Einheit | z. B. R, ATR-normalisierter Return, Basispunkte, Ereigniswahrscheinlichkeit |
| Typischer Horizont | |
| Explorative Streuung aus zulässigen Discovery-/Development-Daten | |
| Stichprobengröße und effektive Clusterzahl dieser Schätzung | |
| Unsicherheit/Bandbreite der Streuungsschätzung | |
| Quelle und Übertragbarkeit auf Validation-Markt/-State | |
| Schwere Tails bereits sichtbar? | `JA / NEIN / UNKLAR` |

## B3. Vorläufige Kostenhürde

| Kostenkomponente | Schätzung | Quelle | State-abhängig? |
|---|---:|---|---|
| Gebühren Round Trip | | | |
| Spread | | | |
| Slippage | | | |
| Funding/Finanzierung | | | |
| Sonstige | | | |

**Gesamte konservative Round-Trip-Kosten in Outcome-Einheit:** ...

**Zusätzliche Sicherheitsmarge:** ...

**Minimale wirtschaftlich relevante Effektgröße `δ_econ`:** ...

**Begründung der Sicherheitsmarge:** ...

## B4. Power-/Präzisionsplanung

| Feld | Eintrag |
|---|---|
| Primärer Test/Schätzer | |
| Fehlerniveau / α / äquivalente Schwelle | Arbeitsdefault bei klassischem Test: `α = 0,05`, zweiseitig; Abweichung vorab begründen |
| Ziel-Power / Präzisionsziel | Arbeitsdefault: `80 %`; bei knappem finalem Holdout oder hohen Kosten falsch-negativer Befunde `90 %` oder direktes Präzisionsziel prüfen |
| Wirtschaftliche Relevanzgrenze | `δ_econ = ...` |
| Angenommene wahre Planungswirkung | `δ_plan = ...`; nicht mit `δ_econ` gleichsetzen |
| Quelle/Begründung von `δ_plan` | inklusive Umgang mit Discovery-Bias, Unsicherheit und gegebenenfalls Shrinkage |
| Null-/Alternativhypothese | `H0: ... / H1: ...` |
| Intervall-/Entscheidungsregel | z. B. `untere Grenze > δ_econ`; exakt hierfür planen |
| Basis-Streuungsannahme | |
| Konservative Planungsstreuung / Stressszenario | |
| Herleitung der konservativen Annahme | `externe/gepoolte Referenz / modellgültige Obergrenze / robuste Skala + Stressaufschlag / Szenariorechnung / ANDERE` |
| Abhängigkeitsannahme | |
| Power-/Simulationsmethode | |
| Benötigtes nominelles N – Basisszenario | |
| Benötigtes effektives N / Clusterzahl – Basisszenario | |
| Benötigtes nominelles N – Stressszenario | |
| Benötigtes effektives N / Clusterzahl – Stressszenario | |

**Pflichtregel:** Ein einzelner Streuungs-Punktschätzer aus einer kleinen, selektierten oder nicht übertragbaren Discovery-Stichprobe reicht nicht als konservative Planungsannahme. `WEITER` setzt voraus, dass die Machbarkeit auch im Stressszenario besteht oder die zusätzlich benötigte Information ausdrücklich beschafft wird.

## B5. Verfügbare Information

| Größe | Wert |
|---|---:|
| Nominelle Ereignisse | |
| Handelstage | |
| Sessions | |
| Eventcluster | |
| Symbole | |
| Grobe Korrelationsgruppen | |
| Methode/Simulation für effektives N | |
| Verwendeter Design Effect samt Annahmen | |
| Geschätztes effektives N | |
| Konservative Untergrenze des effektiven N | |
| Plausibel unabhängige Clusterzahl | |
| Realistisch zusätzlich beschaffbare unabhängige Daten | |

## B6. Machbarkeitsentscheidung

**Fachentscheidung:** `WEITER / DATEN BESCHAFFEN / ABBRECHEN`

**Begründung:** ...

**Besteht die Entscheidung auch unter der konservativen Planungsstreuung?** `JA / NEIN / BLOCKED`

**Falls DATEN BESCHAFFEN:** Welche Daten, wie viel und warum? ...

**Falls ABBRECHEN:** Welches Gate macht das Projekt unbrauchbar? ...

### B-Gate

`PASS / FAIL / BLOCKED`

**Festes Mapping:** `WEITER → PASS`, `DATEN BESCHAFFEN → BLOCKED bis Daten vorliegen`, `ABBRECHEN → FAIL`. `BLOCKED` ist kein vierter Fachentscheid.

**Reichweite:** Ein `PASS` hier öffnet nur Discovery/Development. Vor Freeze ist die formale Phase-0-Re-Kalkulation in `N3` zwingend.

**Nächster zulässiger Schritt:** ...

---

# C. Dateninventar und Rollen

**PHASENSTATUS:** `COMPLETE / BLOCKED`

| Dataset-ID | Datei/Quelle | Zeitraum | Märkte/Symbole | Rolle | Schon angesehen? | Designentscheidung beeinflusst? | Aktuelle Rolle korrekt? |
|---|---|---|---|---|---|---|---|
| | | | | `DISCOVERY / DEVELOPMENT / VALIDATION / FINAL_HOLDOUT / FORWARD_OOS` | | | |

## C1. Kontaminationslog

| Datum | Dataset | Welche Information wurde gesehen? | Welche Designentscheidung wurde beeinflusst? | Konsequenz für Datenrolle |
|---|---|---|---|---|
| | | | | |

**Regel:** Sobald ein Dataset eine Designentscheidung beeinflusst, darf es nicht weiter als unabhängige Validation/Holdout gelten.

---

# D. Discovery und Fallkatalog

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED`

## D1. Neutrale Beschreibung des Phänomens

...

## D2. Falltypen

| Falltyp | Anzahl | Bemerkung |
|---|---:|---|
| klare Treffer | | |
| klare Fehlschläge | | |
| Grenzfälle | | |
| unklassifiziert | | |

## D3. Explorativ getestete Variablen und Varianten

**WICHTIG:** Auch verworfene Varianten eintragen.

| ID | Variable/Idee | Lookback/Parameter | Ergebnis grob | Beibehalten? | Hat Hypothese beeinflusst? |
|---|---|---|---|---|---|
| | | | | | |

## D4. Discovery-Entscheidungen

Welche Begriffe wurden verworfen, geändert oder präzisiert? ...

---

# E. Claim-Level, temporaler DAG, Identifikation und Beobachtbarkeit

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

## E1. Claim-Level und Zielgröße

**Stärkster beabsichtigter Claim:** `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`

**Prädiktive Zielgröße, falls anwendbar:** `P(...) / E[...] / Quantil / sonstige Größe`

**Kausales Estimand:** ... / `N/A + Begründung: ASSOCIATIONAL_PREDICTIVE`

| Bestandteil | Definition |
|---|---|
| Treatment/Intervention/struktureller Schock | |
| Outcome und Horizont | |
| Zielpopulation/Eventklasse | |
| Kontrast und Einheit | |
| Total-/Direkt-/Mediationseffekt | |
| Zeitliche Reihenfolge | |

## E2. DAG oder konkurrierende DAGs

**DAG:** `ANWENDEN / N/A + Begründung`

**DAG-Version:** ... / `N/A`

**Grafische/textuelle Struktur:**

```text
...
```

**Welche Kanten bleiben nur als Äquivalenzklasse oder wegen latenter Variablen unorientiert?** ...

## E3. Pfeilannahmen und Alternativerklärungen

| Pfeil/Kante | Annahme | mögliche Confounder/Collider/Messfehler | Alternative Erklärung | Testbare Konsequenz/Negativkontrolle |
|---|---|---|---|---|
| | | | | |

## E4. Identifikationsstrategie

**Strategie:** `Randomisierung / natürliche Variation / Backdoor / Frontdoor / IV / RD / DiD / High-Frequency-Identifikation / sonstige / NOT_REQUIRED_PREDICTIVE`

**Warum identifiziert diese Strategie genau das Estimand?** ...

| Annahme | testbar? | Evidenz/Diagnose | Verletzungsrisiko | Sensitivität/Placebo/Negativkontrolle |
|---|---|---|---|---|
| | `JA/NEIN/TEILWEISE` | | | |

**Adjustmentsatz und graphische Begründung:** ...

**Positivity/Overlap oder Instrumentrelevanz, falls einschlägig:** ...

**Welche post-treatment Variablen/Mediatoren dürfen nicht als gewöhnliche Controls eingehen?** ...

## E5. Causal-Discovery-/Zeitreihenverfahren, falls verwendet

| Verfahren | Ausgabe darf behaupten | Ausgabe darf NICHT behaupten | benötigte Annahmen | Ergebnislabel |
|---|---|---|---|---|
| Granger | zusätzliche Prognoseinformation relativ zum Informationssatz | interventionale Kausalität | Stationarität/Modellspezifikation/Informationssatz | `PREDICTIVE_PRECEDENCE` |
| CI-/Score-/Invarianz-/Zeitreihen-Discovery | DAG-Kandidaten/Äquivalenzklasse unter Annahmen | „wahrer DAG“ ohne Zusatzannahmen | konkret dokumentieren | `CAUSAL_HYPOTHESIS` |

## E6. Beobachtbarkeitstabelle

| Variable | Rolle | Rohdaten + Vintage | Berechnung | Frühester vollständig bekannter Zeitpunkt | Zum Entscheidungszeitpunkt verfügbar? | Delay | Leakage-/Revisionsrisiko | Zulässig? |
|---|---|---|---|---|---|---|---|---|
| | `Prädiktor / State / Treatment / Schock / Mediator / Trigger / Outcome` | | | | `JA/NEIN` | | | `JA/NEIN` |

### E7-Gate – Kausalität/Identifikation

`PASS / FAIL / BLOCKED / NOT_REQUIRED_PREDICTIVE`

- `PASS`: Nur für den eingefrorenen kausalen Claim und unter den dokumentierten Annahmen.
- `NOT_REQUIRED_PREDICTIVE`: Research darf fortfahren, aber nur mit prädiktiver/assoziativer Sprache.
- `FAIL/BLOCKED`: Kein kausaler Freeze. Eine Fortsetzung als prädiktives Research benötigt eine neue entsprechend deklarierte Version.

### E8-Gate – Leakage/Beobachtbarkeit

`PASS / FAIL / BLOCKED`

## E9. Tooling-Router und reproduzierbare Umgebung

**Tooling-Status:** `TOOLING_REQUIRED / TOOLING_NOT_REQUIRED / TOOLING_BLOCKED`

**Begründung:** ...

| Aufgabe | primäre Bibliothek | exakte Version | Hauptklasse/-funktion | zulässige Aussage | unzulässige Aussage | unabhängige Prüfung |
|---|---|---|---|---|---|---|
| Graph/Adjustierung | `DoWhy / pgmpy / N/A` | | | | | |
| Effektschätzung | `DoWhy / EconML / DoubleML / causalinference / sonstige / N/A` | | | | | |
| Refutation/Sensitivität | `DoWhy / designspezifisch / N/A` | | | | | |
| Zeitreihen-Discovery | `Tigramite / sonstige / N/A` | | | | | |

| Reproduzierbarkeitsfeld | Eintrag |
|---|---|
| Python-/Runtime-Version | |
| Environment-/Lockfile-Pfad oder Hash | |
| Paketquelle | `offizieller Release / begründete andere Quelle` |
| Seed(s) | |
| zeitliche/Cluster-Splitlogik | |
| Graph-/Estimand-Version | |
| Adjustmentsatz | |
| Import-/API-/Kompatibilitäts-Smoke-Test | `PASS / FAIL / BLOCKED / NOT_REQUIRED` |
| relevante Warnungen/Deprecations | |

**E9-Gate – Tooling-Reproduzierbarkeit:** `PASS / FAIL / BLOCKED / NOT_REQUIRED`

**Phasen-Mapping:** `E7 PASS oder NOT_REQUIRED_PREDICTIVE`, `E8 PASS` und `E9 PASS oder NOT_REQUIRED` → `COMPLETE`. Jedes `FAIL` → `FAILED`; jedes `BLOCKED` → `BLOCKED`.

**Falls FAIL:** Research-Version beenden oder Variable neu definieren. Keine rückwirkende Reparatur innerhalb derselben Validation-Version.

---

# F. Operationalisierung

**PHASENSTATUS:** `COMPLETE / BLOCKED`

| Konzept | Exakte Messdefinition | Einheit | Lookback | Session | Timeframe | Zeitpunkt | kontinuierlich oder diskret? |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Welche Schwellen wurden noch NICHT festgelegt und warum?** ...

**Welche Schwellen sind bereits sachlich begründet?** ...

---

# G. Zielvariable und Nullmodell

**PHASENSTATUS:** `COMPLETE / BLOCKED`

## G1. Primärer Outcome

**Definition:** ...

**Horizont:** ...

**Warum dieser Outcome?** ...

## G2. Sekundäre Outcomes

| Outcome | Zweck | Primär/diagnostisch |
|---|---|---|
| | | |

## G3. Primäres Nullmodell

**Definition:** ...

**Warum ist dies der richtige Vergleich?** ...

## G4. Sekundäre Benchmarks

| Benchmark | Zweck |
|---|---|
| | |

## G5. Event-/Surprise-Definition

**Anwendbarkeit:** `ANWENDEN / N/A + Begründung`

| Feld | Festlegung |
|---|---|
| Eventklasse | |
| offizieller Veröffentlichungszeitpunkt und Zeitzone | |
| veröffentlichter Wert + Daten-Vintage | |
| vor dem Event verfügbare Erwartungsquelle | |
| Erwartungs-Zeitstempel/Vintage | |
| Surprise-Formel | |
| vorab definierte Skalierung | |
| Anzahl Surprise-Faktoren | `1 / mehrere + Begründung` |
| Faktorbildung/Rotation/Orthogonalisierung | |
| ökonomische Interpretation und Vorzeichenkonvention je Faktor | |
| primäres Eventfenster | |
| sekundäre Eventfenster | |
| Regel für gleichzeitige/überlappende Nachrichten | |
| Regel für illiquide/technisch fehlerhafte Fenster | |
| struktureller Schock identifiziert? | `JA + E7 PASS / NEIN, nur deskriptive Surprise` |

## G6. Erwartetes Reaktionsmodell

**Anwendbarkeit:** `ANWENDEN / N/A + Begründung`

| Feld | Festlegung |
|---|---|
| Trainingsdaten und Datenrolle | |
| strikt zeitliche Trainingsregel `D_<t` | |
| nur pre-event bekannte Controls `C_t` | |
| Modell `m̂_j(F_t,C_t,F_t⊗C_t)` | |
| Refit-/Update-Regel | |
| Unsicherheitsmodell `σ̂_j,t` | |
| Kalibrierungsdiagnose | |
| primäres Residuum `u_j,t` | `R_j,t - m̂_j(F_t,C_t,F_t⊗C_t;D_<t)` |
| standardisierte Innovation `z_j,t` | `u_j,t / σ̂_j,t` |
| zulässiges Label | `REACTION_INNOVATION / REACTION_ANOMALY` |

**Warum ist die Modellabweichung nicht automatisch Fehlbewertung oder Kausalbruch?** ...

**Einfachstes angemessenes Modell gewählt?** `JA / NEIN + konkrete Zusatzfrage, die die Komplexität rechtfertigt`

## G7. Reaktionskette und Mediatoren

| Kettenglied | Messfenster | erwartete Richtung/Form | Rolle `Outcome/Mediator` | post-event? | Verwendung im Total-Effekt zulässig? | Identifikationsstatus |
|---|---|---|---|---|---|---|
| | | | | | | |

**Gemeinsame Chain-Integrity-Kennzahl:** `N/A als Default / ANWENDEN nur mit vorab definierten Gewichten, Kovarianz, Referenzverteilung und Multiple-Testing-Regel`

**Kriterium für die Bezeichnung `CAUSAL_CHAIN_BREAK`:** ... / `NICHT ZULÄSSIG, weil Kette nicht kausal identifiziert`

---

# H. Explorative Effekt- und State-Analyse

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED / FAILED`

## H1. Unkonditionaler oder vorab konditionaler Baseline-Effekt

| Größe | Schätzung |
|---|---:|
| E[Outcome \| Phänomen] | |
| E[Outcome \| Nullmodell] | |
| Differenz | |
| Unsicherheit | |

**Ist die Baseline von Anfang an konditional?** `JA / NEIN`

**Falls JA: Warum war der State Bestandteil der ursprünglichen Phänomendefinition und nicht nachträglicher Filter?** ...

## H2. State-Variablen zunächst kontinuierlich

| State | Zusammenhang mit Outcome | Form der Beziehung | stabiler Bereich? | Kandidat für Hypothese? |
|---|---|---|---|---|
| | | | | |

## H3. Phänomen vs. State vs. Interaktion

| Größe | Ergebnis |
|---|---|
| E[R \| P] | |
| E[R \| S] | |
| E[R \| P,S] | |
| Zusatzinformation von P über S hinaus | |

## H4. Gewinner und Verlierer gemeinsam analysiert?

`JA / NEIN`

Falls NEIN: `FAILED`.

## H5. Explorative Event- und Reaktionsanalyse

**Anwendbarkeit:** `ANWENDEN / N/A + Begründung`

| Größe | Ergebnis | zulässige Interpretation |
|---|---|---|
| Reaktion auf Rohwert | | deskriptiv |
| Reaktion auf Surprise | | prädiktiv oder kausal nur gemäß E7 |
| zeitlich OOS geschätzte Reaction Innovation | | Prognosefehler/Anomalie |
| Kettenglied-Abweichungen | | leg-spezifische Anomalien |
| State-/Aufmerksamkeitsinteraktion | | Gegenhypothese, bis unabhängig validiert |
| konkurrierende News-/Liquiditätserklärung | | Alternativerklärung |

## H6. Quantitative Shock-Response-Map

**Anwendbarkeit:** `ANWENDEN bei mehrgliedriger Event-/Wirkungskette / N/A + Begründung`

| Glied/Asset | Horizont | Surprise-Faktoren | pre-event State-Interaktionen | Response-Koeffizient + Unsicherheit | Innovation rechtzeitig verfügbar? | zulässiges Label |
|---|---|---|---|---|---|---|
| | | | | | | `TRANSMISSION_DIAGNOSTIC` |

### Inkrementeller Test eines Informationsengpass-Kandidaten

**Definiertes End-Outcome:** ...

**M0:** `End-Outcome ~ Surprise-Faktoren + pre-event States`

**M1:** `M0 + rechtzeitig verfügbare Innovation des vorab gewählten Kettenglieds`

| Feld | Festlegung/Ergebnis |
|---|---|
| Kandidat und Auswahlbegründung | |
| Zeitpunkt realer Verfügbarkeit | |
| primäre OOS-Loss-/Kalibrierungs-/Netto-Utility-Größe | |
| M0 OOS | |
| M1 OOS | |
| inkrementelle Verbesserung + Unsicherheit | |
| Multiple-Testing-Behandlung | |
| zulässige Entscheidung | `INFORMATION_BOTTLENECK_CANDIDATE / KEIN ZUSATZWERT / INCONCLUSIVE` |

---

# I. Candidate Hypothesis

**PHASENSTATUS:** `COMPLETE / BLOCKED`

## I1. Primäre Hypothese

> ...

**Claim-Level:** `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`

**Falls kausal: Estimand-Version und E7-Gate:** ...

**Falls Constraint-Sprache verwendet wird:**

**Constraint-Assessment-ID nach `schemas/constraint_assessment.schema.json`:** ...

| Feld | Festlegung |
|---|---|
| definiertes End-Outcome/Systemziel | |
| Label | `TRANSMISSION_DIAGNOSTIC / INFORMATION_BOTTLENECK_CANDIDATE / IDENTIFIED_CAUSAL_LEVER / IMPLEMENTATION_CONSTRAINT` |
| vorab definiertes Entscheidungskriterium | |
| warum das Label nicht aus Korrelation oder großem Residuum abgeleitet wurde | |

## I2. Gegenhypothese

> ...

## I3. Erwartete Richtung

`POSITIV / NEGATIV / ZWEISEITIG`

## I4. Wirtschaftlich relevante Grenze

`δ_econ = ...`

## I5. Falsifikationsbedingung

...

## I6. Regel für unerwartetes Vorzeichen

Wenn ein ausreichend präziser Effekt mit entgegengesetztem Vorzeichen beobachtet wird:

- alte Hypothese = `FALSIFIED`,
- neue Hypothese = neue Version/Research-ID,
- keine semantische Umetikettierung.

## I7. Zielstufe dieses Tests

**Primär getestete Stufe:**
`mechanism_supported / forward_predictive_oos / executable_net_edge`

**Welche stärkere Stufe darf aus diesem Design ausdrücklich NICHT abgeleitet
werden?** ...

**Falls ein kontemporärer Zusammenhang untersucht wird:** Warum ist das Outcome
nicht als Forward-Prognose beschriftet? ...

---

# J. Vorhersage-Liste

**PHASENSTATUS:** `COMPLETE / BLOCKED`

| ID | Zusätzliche Vorhersage | Datengrundlage | Testmethode | Ergebnis darf Hypothese wie beeinflussen? |
|---|---|---|---|---|
| P1 | | | | |
| P2 | | | | |

---

# K. Pre-Mortem und Guardrails

**PHASENSTATUS:** `COMPLETE / BLOCKED`

**Annahme:** Das Ergebnis sieht gut aus, scheitert später OOS oder live. Warum?

| Risiko | Warum plausibel? | Vorab-Check | Guardrail | Ablehnungskriterium |
|---|---|---|---|---|
| Leakage | | | | |
| Selection Bias | | | | |
| latenter Confounder/Collider | | | | |
| post-treatment Control/nicht identifizierte Mediation | | | | |
| falsche Erwartungs-Vintage/Eventfenster-Kontamination | | | | |
| vermischte Nachrichtenschocks | | | | |
| Aufmerksamkeit/Positionierung/Liquidität statt Mechanismusbruch | | | | |
| zu wenig unabhängige Evidenz | | | | |
| dominantes Symbol/Event | | | | |
| Multiple Testing | | | | |
| Kosten/Slippage | | | | |
| Midquote-Effekt ohne ausführbaren Fill | | | | |
| Feed-Latenz/Clock-Desynchronisation/stale Quote | | | | |
| öffentliche Tape-Signatur identifiziert latenten Akteur nicht | | | | |
| Strukturbruch/Kalender- oder Venue-Regeländerung | | | | |
| Live-Variable zu spät verfügbar | | | | |
| Sonstiges | | | | |

---

# L. Abhängigkeit, effektives N und Inferenz

**PHASENSTATUS:** `COMPLETE / BLOCKED`

## L1. Abhängigkeitsdiagnose

| Risiko | Vorhanden? | Messung/Begründung |
|---|---|---|
| serielle Autokorrelation | | |
| mehrere Signale pro Impuls | | |
| überlappende Labels | | |
| korrelierte Symbole | | |
| gemeinsame Makroevents | | |
| dominante Session-/Eventcluster | | |

## L2. Clusterdefinition

**Primäre Clustereinheit:** ...

**Sekundäre Clustereinheit:** ...

## L3. Gewählte Inferenzmethode

`IID / BLOCK_BOOTSTRAP / CLUSTER_BOOTSTRAP / CLUSTER_ROBUST / ANDERE`

**Warum passend?** ...

## L4. Purging / Embargo

**Überlappen Label-/Outcome-Fenster über Train/Test-Grenzen?** `JA / NEIN`

**Purging-Regel:** ...

**Embargo-Regel:** ...

## L5. Effektives N

**Methode:** ...

**Nominelles N:** ...

**Effektives N / Clusterzahl:** ...

**Design Effect `DE = Var(tatsächliches Design) / Var(IID-Referenz)`:** ...

**Verwendete DE-Formel/Simulation und ihre Annahmen:** ...

**Weniger als 30 unabhängige Cluster?** `JA / NEIN / UNKLAR`

**Falls JA:** Status `SMALL_CLUSTER_WARNING`; verwendete Small-Sample-Methode oder Kalibrierung: ...

---

# M. Heavy Tails und Einflussdiagnostik

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

`N/A` ist nur für die Heavy-Tail-spezifischen Unterfelder zulässig, wenn Heavy Tails sachlich ausgeschlossen wurden. Einflussdiagnostik `M3` bleibt Pflicht.

## M1. Primärer Lageparameter

`MEAN / MEDIAN / TRIMMED_MEAN / ROBUSTER_M_SCHÄTZER / ANDERE`

**Begründung:** ...

## M2. Robuste Sensitivität

**Sekundärer Schätzer:** ...

**Trimming/Winsorisierung erlaubt?** ...

**Falls ja: exakt wie und nur als primär oder Sensitivität?** ...

## M3. Vorab definierte Einflussdiagnostik

| Diagnose | Schwelle/Entscheidungsregel |
|---|---|
| Leave-one-out-Spanne | |
| Leave-one-cluster-out-Spanne | |
| Anteil größte Beobachtung | |
| Anteil größter Cluster | |
| Ergebnis ohne dominantes Symbol | |
| Ergebnis ohne dominante Periode/Eventgruppe | |

**Mindestregel:** Wenn das Entfernen eines einzelnen plausiblen Clusters das Vorzeichen oder die wirtschaftliche Schlussfolgerung kippt, keine robuste Bestätigung.

---

# N. Multiple Testing / Research Search Space

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

Eine konkrete Multiple-Testing-Korrektur in `N2` kann begründet `N/A` sein. Die formale Phase-0-Re-Kalkulation und das Pipeline-Integritätsgate sind niemals `N/A`.

## N1. Tatsächlich untersuchte Freiheitsgrade

| Dimension | Anzahl/Varianten |
|---|---|
| Hypothesen | |
| Prädiktoren | |
| Statevariablen | |
| Lookbacks | |
| Schwellen | |
| Timeframes | |
| Sessions | |
| Symbole/Universen | |
| Outcomes/Horizonte | |
| Entries/Exits | |

## N2. Gewählte Korrektur-/Bewertungsmethode

`FDR / WHITE_REALITY_CHECK / HANSEN_SPA / DEFLATED_SHARPE / PBO / PIPELINE_BOOTSTRAP / N/A / ANDERE`

**Warum diese Methode?** ...

## N3. Formale Phase-0-Re-Kalkulation und Validation-Spezifikation

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

| Feld | Eingefrorener Wert |
|---|---|
| finaler primärer Outcome und Nullmodell | |
| `δ_econ` | |
| `δ_plan` oder direktes Präzisionsziel | |
| `H0 / H1` beziehungsweise Intervall-Entscheidungsregel | |
| finale Streuungs- und Abhängigkeitsannahme | |
| benötigtes effektives N / Clusterzahl im Stressszenario | |
| daraus per DE/Simulation benötigtes nominelles N | |
| aktuell vorhandene konservative Untergrenze des effektiven N | |
| Validation-Dataset, Zeitraum, Rolle und Unangesehen-Status | |
| Datensplit / äußeres Testfenster | |
| Erfolgskriterium A | |
| Gegenrichtungsregel B | |
| Präzise-Null-Regel C | |
| Inconclusive-Regel D | |

**Fachentscheidung:** `WEITER / DATEN BESCHAFFEN / ABBRECHEN`

### N3-Gate – Formale Machbarkeit vor Freeze

`PASS / FAIL / BLOCKED`

**Festes Mapping:** `WEITER → PASS`, `DATEN BESCHAFFEN → BLOCKED bis Daten vorliegen`, `ABBRECHEN → FAIL`. Nur dieses `PASS` kann den Weg zum Pipeline-Integritätsgate und Freeze öffnen.

## N4. Pipeline-Integritätsprüfung vor Freeze

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

| Test-ID | Kontrolltyp | Kontrollbasis | Empirisches Dataset + gültige Rolle | Null-/Synthetic-Design | Erhaltene Zeit-/Cluster-/State-/Volatilitätsstruktur | geplantes B | tatsächliches B | Zielpräzision + Monte-Carlo-SE/Intervall | Vorab-Akzeptanzregel | Ergebnis |
|---|---|---|---|---|---|---:|---:|---|---|---|
| PI-NULL | wiederholte Null-/Surrogatkontrolle | `empirisch abgeleitet / rein synthetisch` | nur bei empirischer Basis: `DEVELOPMENT` | | | | | | | |
| PI-SENTINEL | bekannter Effekt mit festem Vorzeichen und Timing | `rein synthetisch` | kein empirisches Dataset | | | | | | | |
| PI-CAUSAL-TOOL | bei `TOOLING_REQUIRED`: bekannter DAG/Adjustmentsatz und bekannter Effekt | `rein synthetisch` | kein empirisches Dataset | | | | | | | |

- [ ] Vollständige Feature-, Auswahl-, Filter-, Timing- und Auswertungspipeline ausgeführt.
- [ ] Nullkontrolle zerstört keine für das Nullmodell relevante Abhängigkeit; jede ungeklärte relevante Strukturabweichung erzwingt `N4-Gate: BLOCKED`.
- [ ] Fehlalarmrate beziehungsweise Null-Effektverteilung liegt innerhalb der vorab definierten Toleranz.
- [ ] Vorab definierte Zielpräzision der Fehlalarmrate wurde erreicht.
- [ ] Sentinel wurde mit korrektem Vorzeichen, Index und Timing erkannt.
- [ ] Bei `TOOLING_REQUIRED` wurden Import, Version, Haupt-API und Paketkompatibilität geprüft; der kausale Sentinel lieferte zulässigen Adjustmentsatz und korrekte Richtung.

### N4-Gate – Pipeline-Integrität

`PASS / FAIL / BLOCKED`

**Status-Mapping:** `PASS → COMPLETE`, `FAIL → FAILED`, `BLOCKED → BLOCKED`.

Ein einzelner Shuffle- oder Random-Walk-Lauf genügt nicht.

---

# O. FREEZE

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

## O1. Freeze-Checkliste

Jeder Punkt muss `YES` sein. `N/A + Begründung` ist nur dort zulässig, wo die Tabellenzeile dies ausdrücklich erlaubt.

| Punkt | Status |
|---|---|
| Research-ID/Version fest | |
| Candidate Hypothesis fest | |
| Gegenhypothese fest | |
| Claim-Level fest | |
| kausales Estimand fest oder `N/A: ASSOCIATIONAL_PREDICTIVE` | |
| Identifikationsstrategie/-annahmen fest oder `NOT_REQUIRED_PREDICTIVE` | |
| E7-Identifikationsgate bestanden oder `NOT_REQUIRED_PREDICTIVE` | |
| DAG-Version fest oder DAG `N/A + Begründung` | |
| E9-Tooling-Gate bestanden oder `NOT_REQUIRED` | |
| primäre Bibliothek je kausaler Aufgabe und Haupt-API fest oder `TOOLING_NOT_REQUIRED + Begründung` | |
| Python-/Paketversionen, Lockfile/Environment, Seeds und Splitlogik fest | |
| Beobachtbarkeit vollständig | |
| Phänomendefinition fest | |
| State-Variablen fest | |
| Ausschlüsse fest | |
| primärer Outcome fest | |
| Nullmodell fest | |
| Event-/Surprise-Konstruktion fest oder `N/A + Begründung` | |
| Erwartungsquelle, Vintage, Zeitstempel und Eventfenster fest oder `N/A` | |
| Zahl/Rotation/Orthogonalisierung/Interpretation der Surprise-Faktoren fest oder `N/A` | |
| Regel für Eventfenster-Kontamination fest oder `N/A` | |
| Reaktionsmodell/zeitliche Trainingsregel/Unsicherheit fest oder `N/A` | |
| Reaktionsabweichung korrekt als nicht-kausales Residuum gelabelt oder kausale Kette identifiziert | |
| bei Informationsengpass-Claim: End-Outcome, Kandidat, Verfügbarkeitszeitpunkt und M0/M1-OOS-Test fest oder `N/A` | |
| Constraint-Label und Entscheidungskriterium fest oder `N/A` | |
| erwartete Richtung fest | |
| δ_econ fest | |
| δ_plan oder direktes Präzisionsziel fest | |
| H0/H1 beziehungsweise Intervall-Entscheidungsregel fest | |
| primärer Schätzer fest | |
| robuste Sensitivität fest | |
| Abhängigkeitsmethode fest | |
| effektives-N-Methode fest | |
| Purging/Embargo fest oder N/A | |
| Einflussdiagnostik fest | |
| Heavy-Tail-Regel fest | |
| Multiple-Testing-Methode fest | |
| formale Phase-0-Re-Kalkulation `N3` bestanden | |
| Validation-Datensplit/-fenster fest | |
| Mindest-N aus konservativem Stressszenario fest | |
| Validation-Plan und A/B/C/D-Entscheidungsregeln vollständig | |
| Pipeline-Integritätsgate bestanden | |
| bei `TOOLING_REQUIRED`: kausaler Tool-Sentinel und Kompatibilitäts-Smoke-Test bestanden | |
| Datenrollen fest | |
| Validation-Dataset unangesehen | |
| Final Holdout unangesehen oder `N/A + Begründung` bei äußerem Walk-Forward | |
| Erfolgskriterium fest | |
| Gegenrichtung-Regel fest | |
| Null-/Ineffekt-Regel fest | |
| Inconclusive-Regel fest | |
| Kostenmodell-Version fest | |

## O2. Freeze-Erklärung

> Ab diesem Zeitpunkt werden keine materiellen Designänderungen anhand der laufenden Validation-Ergebnisse vorgenommen. Jede materielle Änderung erzeugt eine neue Research-Version und verbraucht die bis dahin angesehenen Daten für diese neue Version als Development Data.

**Freeze bestätigt am:** ...

### O-Gate

`PASS / FAIL / BLOCKED`

---

# P. Validation-Ausführung des eingefrorenen Plans

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

## P1. Freeze-Abgleich

**Referenz auf eingefrorenen Plan in N3/O:** ...

**Wurde seit Freeze irgendein Designfeld geändert?** `JA / NEIN`

Falls `JA`: Validation nicht starten beziehungsweise als `INVALID_TEST` beenden; betroffene Daten auf `DEVELOPMENT` umklassifizieren.

## P2. Tatsächlich verwendete Datenarchitektur

| Dataset | Rolle | Zeitraum | Unangesehen bestätigt? | entspricht N3/O? |
|---|---|---|---|---|
| | VALIDATION | | | |

**Final Holdout weiterhin vollständig reserviert und unangetastet?** `JA / NEIN / N/A + Begründung`

Falls `NEIN`: normale Validation nicht beginnen beziehungsweise Final-Holdout-Status verwerfen und Datenrolle neu klassifizieren.

## P3. Stichproben- und Startgate

**Eingefrorenes Mindest-N aus N3/O:** ...

**Tatsächlich verfügbares nominelles N:** ...

**Tatsächlich verfügbare konservative Untergrenze des effektiven N / Clusterzahl:** ...

### P-Gate – Validation darf starten

`PASS / FAIL / BLOCKED`

Nur `PASS` erlaubt die Ausführung. `FAIL → FAILED`, `BLOCKED → BLOCKED`.

---

# Q. Validation-Ergebnis

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

## Q1. Unabhängigkeit bestätigt?

`JA / NEIN / UNKLAR`

Falls NEIN: Welche Designentscheidung wurde beeinflusst? ...

**Konsequenz:** Dataset auf `DEVELOPMENT` umklassifizieren; unabhängige Validation nicht behaupten.

### Q1-Gate – Validation-Unabhängigkeit

`PASS / FAIL / BLOCKED`

**Mapping:** `JA → PASS`, `NEIN → FAIL + INVALID_TEST`, `UNKLAR → BLOCKED`. Ohne `PASS` dürfen Q2–Q8 nicht als unabhängige Validation interpretiert werden.

## Q2. Primärer Effekt

| Größe | Ergebnis |
|---|---:|
| Punktschätzer | |
| Nullmodell | |
| Differenz | |
| Unsicherheitsintervall | |
| δ_econ | |
| Primäre Entscheidung A/B/C/D | |

## Q3. Robuste Sensitivität

| Schätzer/Analyse | Ergebnis | Ändert Schlussfolgerung? |
|---|---:|---|
| | | |

## Q4. Einflussdiagnostik

| Diagnose | Ergebnis | Gate bestanden? |
|---|---|---|
| Leave-one-out | | |
| Leave-one-cluster-out | | |
| ohne dominantes Symbol | | |
| ohne dominante Periode/Eventgruppe | | |

## Q5. Multiple-Testing-adjustierte Evidenz

...

## Q6. Identifikationsdiagnostik bei kausalem Claim

**Anwendbarkeit:** `ANWENDEN / N/A: ASSOCIATIONAL_PREDICTIVE`

| eingefrorene Annahme/Diagnose | Ergebnis | bestanden? | Konsequenz für kausalen Claim |
|---|---|---|---|
| Overlap/Positivity oder Instrumentrelevanz | | | |
| Balance/Pre-Trends/Placebo, falls einschlägig | | | |
| Negativkontrolle | | | |
| Sensitivität gegenüber latentem Confounding | | | |
| alternative zulässige DAGs/partielle Identifikation | | | |

| Tooling-Ausführung | protokollierter Wert |
|---|---|
| Runtime, Pakete und Versionen | |
| tatsächlich verwendete Klassen/Funktionen | |
| Seeds und tatsächliche Split-/Cross-Fitting-Logik | |
| Warnungen, Deprecations oder Kompatibilitätsabweichungen | |
| Artefakt-/Konfigurationspfad oder Hash | |
| unabhängige Reproduktion/Sensitivität | |

**Kausaler Claim gemäß eingefrorenem Gate weiterhin zulässig?** `JA / NEIN / BLOCKED`

## Q7. Event-/Reaktionsinnovation, falls anwendbar

| Größe | OOS-Ergebnis | Kalibrierung/Unsicherheit | Interpretation |
|---|---|---|---|
| Surprise-Faktoren einschließlich Rotations-/Vorzeichenstabilität | | | |
| erwartete Reaktion | | | |
| `REACTION_INNOVATION` | | | |
| Kettenglied-Abweichungen | | | |
| M0 gegen M1 für vorab gewählten Informationsengpass-Kandidaten | | | `inkrementeller Prognosewert, kein Kausalbeweis` |
| konkurrierende News-/Liquiditätserklärung | | | |

**Wurde eine Reaktionsanomalie ohne bestandenes Ketten-Identifikationsdesign als `CAUSAL_CHAIN_BREAK` bezeichnet?** `NEIN / JA → INVALID_CAUSAL_CLAIM`

**Zulässiges Constraint-/Diagnoselabel nach OOS:** `TRANSMISSION_DIAGNOSTIC / INFORMATION_BOTTLENECK_CANDIDATE / IDENTIFIED_CAUSAL_LEVER / KEIN LABEL / N/A`

## Q8. Validation-Entscheidung

`VALIDATED / FALSIFIED / PRECISE_NULL / INCONCLUSIVE / INVALID_TEST`

**Begründung:** ...

---

# R. Final Holdout / äußeres Walk-Forward

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED`

## R1. Holdout niemals zuvor angesehen?

`JA / NEIN`

Falls NEIN: kein Final Holdout.

## R2. Ergebnis

...

## R3. Schlussfolgerung

...

---

# S. Robustheit und Replikation

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED`

| Test | Ergebnis | Schlussfolgerung stabil? |
|---|---|---|
| benachbarte Parameter | | |
| andere Perioden | | |
| andere Symbole | | |
| Statebereiche | | |
| Forward-Horizonte | | |
| alternative zulässige DAGs/Identifikationsannahmen, falls kausal | | |
| andere Eventfenster gemäß Freeze | | |
| Erwartungsquelle/Vintage-Sensitivität | | |
| Reaction-Innovation-Kalibrierung | | |
| ohne dominanten Cluster | | |
| ohne dominantes Symbol | | |

---

# T. Phänomen-Entscheidung

`NO_PHENOMENON / INCONCLUSIVE / CANDIDATE_HYPOTHESIS / VALIDATED_PHENOMENON / REJECTED`

**Begründung:** ...

**Wichtig:** Erst bei `VALIDATED_PHENOMENON` darf Strategy Engineering als regulärer nächster Schritt beginnen.

**Strategy Engineering als nächster Schritt ausdrücklich beschlossen?** `JA / NEIN`

**POST-T-BLOCKSTATUS:** `ACTIVATED / DEFERRED_AFTER_VALIDATION / NOT_ACTIVATED_BY_T_GATE`

`ACTIVATED` ist nur bei `VALIDATED_PHENOMENON + JA` zulässig. Bei `VALIDATED_PHENOMENON + NEIN` gilt `DEFERRED_AFTER_VALIDATION`; ohne validiertes Phänomen gilt `NOT_ACTIVATED_BY_T_GATE`. In den beiden nicht aktivierten Zuständen werden `U–Y` nicht feldweise bearbeitet; Abschnitt `Z` wird fortgeführt.

---

# U. Strategy Engineering

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED`

## U1. Validiertes Phänomen, das umgesetzt werden soll

...

## U2. Setup

...

## U3. Trigger

...

## U4. Invalidation

...

## U5. Entry

...

## U6. Stop

...

## U7. Target

...

## U8. Management

...

## U9. Positionsgröße / Risikomodell

...

## U10. Detailliertes zustandsabhängiges Kostenmodell

| State/Execution-Bedingung | Gebühren | Spread | Slippage | Funding | Gesamtkosten |
|---|---:|---:|---:|---:|---:|
| | | | | | |

## U11. Capacity/Liquidität

...

## U12. Entry-/Exit-Diagnostik geplant

| Größe | Speichern? |
|---|---|
| MFE | |
| MAE | |
| Zeit bis MFE | |
| Zeit bis MAE | |
| Zeit bis Stop | |
| Zeit bis Target | |
| Exit-Grund | |

---

# V. Prerequisite Tree / Transition Tree

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED`

## V1. Implementation-Constraint-Register

**Definiertes Systemziel:** `ausführbare risikoadjustierte Netto-Performance / konkretisieren`

| Kandidat | Typ | Wie begrenzt er das Systemziel? | Evidenz | beeinflussbar? | nächste Aktion | Widerlegungskriterium |
|---|---|---|---|---|---|---|
| | `Daten/Latenz/Liquidität/Kosten/Prozess` | | | | | |

**Aktuelles `IMPLEMENTATION_CONSTRAINT`:** ... / `KEINES IDENTIFIZIERT`

## V2. Umsetzungshindernisse

| Hindernis | notwendiges Zwischenziel |
|---|---|
| | |

## V3. Transition Tree

| Schritt | Aktion | erwarteter neuer Zustand | Prüfung |
|---|---|---|---|
| | | | |

---

# W. Vollständige Strategie – erneuter OOS-/Forward-Test

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED`

| Feld | Eintrag |
|---|---|
| OOS-/Forward-Dataset | |
| Datenrolle | |
| Kostenmodell-Version | |
| Anzahl nomineller Trades | |
| effektive Clusterzahl | |
| Net Expectancy | |
| Drawdown | |
| MFE/MAE-Diagnostik | |
| Prozessabweichungen | |
| Ergebnis | |

---

# X. Aktivierungsgate

**PHASENSTATUS:** `COMPLETE / BLOCKED / FAILED`

| Gate | PASS/FAIL/BLOCKED |
|---|---|
| Phänomen validiert | |
| Strategy Engineering eingefroren | |
| Vollständige Strategie OOS bestanden | |
| Kosten realistisch | |
| Risiko-/Positionsgrößenlogik vollständig | |
| Prozess reproduzierbar | |
| Degradationsregeln vorab definiert | |

**Entscheidung:** `ACTIVE_STRATEGY_CANDIDATE / ACTIVE / NOT_ACTIVE`

---

# Y. Forward-OOS und Degradation

**PHASENSTATUS:** `COMPLETE / N/A / BLOCKED`

## Y1. Vorab definierte Warn-/Suspendierungsregeln

| Ebene | Warnschwelle | Suspendierungsschwelle | Revalidierungskriterium |
|---|---|---|---|
| statistisch | | | |
| wirtschaftlich | | | |
| State/Regime | | | |
| Event/Reaction Innovation | | | |
| Identifikationsdiagnostik, falls kausal | | | |
| Prozess | | | |

## Y2. Laufende Monitoring-Ergebnisse

| Zeitraum | N | effektives N/Cluster | Expectancy | Kosten | Drawdown | State-Mix | Reaction-Innovation-Kalibrierung | Eventkontamination | Prozessqualität | Status |
|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| | | | | | | | | | | |

---

# Z. Entscheidungs- und Versionsprotokoll

| Datum | Research-Version | Phase | Entscheidung | Begründung | Daten, die dadurch verbraucht wurden | Neuer Status |
|---|---|---|---|---|---|---|
| | | | | | | |

## Z1. Vorab notierte Ablehnungsgründe

Diese Gründe werden **vor** dem relevanten Test notiert.

1. ...
2. ...
3. ...

## Z2. Endentscheidung

**Aktueller/Endstatus:** `NO_PHENOMENON / INCONCLUSIVE / CANDIDATE_HYPOTHESIS / IN_TEST / VALIDATED_PHENOMENON / ECONOMICALLY_UNTRADEABLE / ACTIVE_STRATEGY_CANDIDATE / ACTIVE / UNDER_OBSERVATION / SUSPENDED / REVALIDATED / REJECTED`

**Nächste Prozessentscheidung:** `WEITER / NEUE_VERSION / MEHR_DATEN / ABBRECHEN / N/A`

**Begründung:** ...

---

# Abschluss-Check für den AI-Agenten

Der Agent darf den jeweils aktivierten Teil des Research-Artefakts nicht als vollständig bezeichnen, bevor er die zutreffenden Fragen explizit beantwortet hat. Nach einem frühen `FAIL` gelten Checkpunkte hinter dem abgebrochenen Gate gesammelt als `NOT_REACHED_DUE_TO_FAILED_GATE`; sie benötigen keine künstlichen Einzelantworten.

## Erreichter Research-Pfad `A–T` und immer aktives Protokoll `Z`

- [ ] Wurde die Rohidee mit Herkunft, Scope, Alternativerklärungen, Datenbedarf und verbrauchtem Informationsbudget in der Hypothesen-Inbox erfasst?
- [ ] War der Intake vor Phase 0 `PROMOTED`, ohne Promotion als Evidenzbestätigung auszugeben?
- [ ] Sind Venue, Handelsphase, Kalender/DST, Zeitbasis, Horizont und Ereignisklasse eindeutig?
- [ ] Ist die News-/Makro-Policy operationalisiert und sind bei `FILTER_KNOWN_EVENTS` Feeds, Ausschlussfenster und Coverage-Lücken dokumentiert?
- [ ] Werden `mechanism_supported`, `forward_predictive_oos` und `executable_net_edge` getrennt geführt und nicht automatisch hochgestuft?
- [ ] Wurde Phase 0 durchgeführt?
- [ ] Stammt Mindest-N aus Power/Präzision statt aus vorhandenem N?
- [ ] Wurde eine konservative Planungsstreuung samt Stressszenario statt nur eines Discovery-Punktschätzers verwendet?
- [ ] Sind alle Dataset-Rollen korrekt und Kontaminationen geloggt?
- [ ] Ist der Claim-Level ausdrücklich als prädiktiv, interventional oder kontrafaktisch deklariert?
- [ ] Existieren bei kausalem Claim ein präzises Estimand, eine Identifikationsstrategie, dokumentierte Annahmen und `E7 PASS`?
- [ ] Wurden Granger-/Causal-Discovery-Ergebnisse nur innerhalb ihrer Annahmen und nicht als automatischer Kausalbeweis interpretiert?
- [ ] Wurde der Tooling-Router angewendet und `TOOLING_REQUIRED / TOOLING_NOT_REQUIRED / TOOLING_BLOCKED` begründet?
- [ ] Wurde bei ausführbarer kausaler Analyse eine passende Spezialbibliothek statt einer ungeprüften Eigenimplementierung verwendet?
- [ ] Sind Runtime, exakte Paketversionen, Haupt-APIs, Seeds, Splits, Warnungen und Environment reproduzierbar protokolliert?
- [ ] Wurde ein Bibliotheksoutput nicht als Ersatz für Identifikation oder als automatisches Upgrade des Claim-Levels behandelt?
- [ ] Existiert ein temporaler DAG oder eine begründete N/A-Entscheidung?
- [ ] Ist für jede Prädiktorvariable der Beobachtbarkeitszeitpunkt dokumentiert?
- [ ] Sind Confounder vor dem Schock/Treatment bekannt und post-treatment Mediatoren nicht versehentlich als Total-Effekt-Controls verwendet?
- [ ] Sind bei Event-Research Erwartungsquelle, Vintage, Surprise-Formel, Zeitstempel, Eventfenster und Kontaminationsregel eingefroren?
- [ ] Sind Anzahl, Konstruktion und Interpretation der Surprise-Faktoren eingefroren und zum Research-Suchraum gezählt?
- [ ] Wurde zunächst die einfachste angemessene Shock-Response-Regression verwendet?
- [ ] Beruht ein `INFORMATION_BOTTLENECK_CANDIDATE` auf einem vorab festgelegten zeitlichen M0/M1-OOS-Vergleich?
- [ ] Wurden Informationsengpass, kausaler Hebel und Implementation Constraint sprachlich getrennt?
- [ ] Wird `Expected − Actual` als Reaktionsinnovation und nur bei identifizierter Kette als Kausalbruch bezeichnet?
- [ ] Ist das Nullmodell explizit?
- [ ] Sind Effektgröße und Unsicherheit angegeben?
- [ ] Wurde effektives N statt nur nominelles N beurteilt?
- [ ] Wurden Cluster/Überlappung/Korrelation geprüft?
- [ ] Wurde bei weniger als 30 unabhängigen Clustern `SMALL_CLUSTER_WARNING` ausgelöst und methodisch behandelt?
- [ ] Sind Influence Diagnostics vorab definiert?
- [ ] Ist Heavy-Tail-Behandlung vorab definiert?
- [ ] Ist Multiple Testing dokumentiert?
- [ ] Hat die vollständige Pipeline vor Freeze das Integritätsgate bestanden?
- [ ] Sind Vorhersage-Liste und Pre-Mortem abgeschlossen?
- [ ] Ist der Freeze vollständig?
- [ ] War Validation wirklich unabhängig?
- [ ] Wurden OOS-/Backtest-Erfolg und kausale Identifikation getrennt beurteilt?
- [ ] Wurde ein unpräzises Ergebnis nicht als Anlass zur ergebnisgetriebenen Revision benutzt?
- [ ] Wurde ein entgegengesetztes Vorzeichen als neue Hypothese behandelt?
- [ ] Wurde Abschnitt `Z` während des gesamten Research-Prozesses geführt?

## Nur bei `POST-T-BLOCKSTATUS: ACTIVATED` – Strategy Engineering `U–Y`

- [ ] Wurde die ökonomische Umsetzbarkeit nach Phänomen-Validation detailliert geprüft?
- [ ] Wurde die vollständige Strategie erneut OOS/Forward geprüft?
- [ ] Sind Degradations- und Abschaltregeln vor Aktivierung definiert?

## Operative Agentenartefakte

- [ ] Besitzt jede persistierte Rohidee ein valides, versioniertes Hypothesen-Intake-Artefakt?
- [ ] Besitzt jeder tatsächliche LLM-/Agentenlauf eine eindeutige Run-ID und ein valides Run-Manifest?
- [ ] Sind Modell/Snapshot, Prompts, Parameter, Tools, Datenstände, Quellenstände und Output-Hashes je Run reproduzierbar referenziert?
- [ ] Besitzt jede entscheidungsrelevante Aussage eine Claim-ID und eine epistemische Klasse?
- [ ] Sind `SOURCE_FACT`-Claims mit konkreter Quelle und Fundstelle belegt?
- [ ] Wurde bei einschlägigem Finance-Research die Coverage von Journal of Finance, Journal of Financial Economics, arXiv `q-fin` und weiteren relevanten Primärquellen dokumentiert?
- [ ] Besitzt jede akademische Quelle eine `work_id`, eine eigene `source_id` für die konkret verwendete Fassung sowie Publikationsstatus, Studientyp, Autoren, Venue/DOI oder arXiv-ID/-Kategorie/-Version?
- [ ] Wurden Fassungen und Indizes derselben `work_id` dedupliziert und nicht als unabhängige Bestätigungen gezählt?
- [ ] Sind Preprints und Working Papers als vorläufig gekennzeichnet, ohne aus arXiv-Kategorie oder Journalprestige ein Qualitätsupgrade abzuleiten?
- [ ] Wurden Correction, Expression of Concern, Retraction und Withdrawal mit Prüfmethode, Zeitpunkt und gegebenenfalls Notice-URI geprüft?
- [ ] Sind Code-, Daten- und unabhängiger Replikationsstatus samt Referenzen protokolliert?
- [ ] Referenzieren `CALCULATED_VALUE`, `ESTIMATE`, `INFERENCE` und `FORECAST` ihre Eingangsclaims und Methoden?
- [ ] Sind Quellenkonflikte, fehlende Evidenz und `UNKNOWN` sichtbar, ohne sie sprachlich zu glätten?
- [ ] Sind menschliche Reviews und Overrides append-only protokolliert und gegen stilles Überschreiben geschützt?
- [ ] Wurde nach materiellen Agentenänderungen das versionierte Eval- und Regression Gate bestanden?
- [ ] Stimmen alle Einträge im operativen Artefaktregister mit ihren gespeicherten Hashes und Statuswerten überein?

## Gate-Konsistenz

- [ ] Bei einem frühen Gate-Abbruch: Wurden alle nicht mehr erreichbaren Folgeabschnitte einmalig als `NOT_REACHED_DUE_TO_FAILED_GATE` markiert und `Z` abgeschlossen?
- [ ] Bei `BLOCKED`: Blieben Folgeabschnitte unangetastet und wurden Blocker/fehlende Information in `Z` protokolliert?
- [ ] Wurden `U–Y` nur nach bestandenem T-Gate aktiviert?
- [ ] Bei `DEFERRED_AFTER_VALIDATION` oder `NOT_ACTIVATED_BY_T_GATE`: Wurden `U–Y` geschlossen gelassen, statt künstlich mit Einzel-`N/A` befüllt zu werden?
