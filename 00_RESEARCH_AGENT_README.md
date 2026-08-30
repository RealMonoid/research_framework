# 00_RESEARCH_AGENT_README.md

**Version:** 1.7
**Stand:** 2026-08-30  
**Status:** ENTWURF ZUR ÜBERNAHME  
**Zweck:** Verbindliche Lese- und Ausführungsanweisung für AI-Agenten, die Trading-Research-Projekte bearbeiten.

---

## 1. Dokumentpaket und Lesereihenfolge

Ein AI-Agent MUSS die Dateien in dieser Reihenfolge lesen:

1. `00_RESEARCH_AGENT_README.md`
2. `01_RESEARCH_STANDARD.md`
3. `02_RESEARCH_CASE_TEMPLATE.md`
4. `03_RESEARCH_METHODS.md`
5. `04_CAUSAL_TOOLING.md`
6. `05_AGENT_OPERATIONS.md`

Vor einem neuen Research Case wird jede Rohidee als Hypothesen-Intake nach
`schemas/hypothesis_candidate.schema.json` erfasst und gescreent. Erst ein
`PROMOTED`-Intake darf in die Phase-0-Vorprüfung übergehen; Promotion ist keine
Evidenzbestätigung. Für ein konkretes Research-Projekt wird anschließend **eine
eigene Kopie** von `02_RESEARCH_CASE_TEMPLATE.md` angelegt und vollständig befüllt.
Jeder tatsächliche Agentenlauf erhält zusätzlich ein valides Run-Manifest nach
`schemas/run_manifest.schema.json`. Entscheidungsrelevante Aussagen, menschliche
Reviews und Eval-Ergebnisse werden nach `05_AGENT_OPERATIONS.md` als getrennte
operative Artefakte geführt und im Research Case referenziert.

Die Abschnitte `U–Y` dieser Kopie bleiben bis zu einer bestandenen Phänomen-Entscheidung in Abschnitt `T` **inaktiv**. Nach `VALIDATED_PHENOMENON` werden sie nur durch eine ausdrückliche Fortsetzungsentscheidung aktiviert; andernfalls bleibt `VALIDATED_PHENOMENON` ein zulässiger eigenständiger Endzustand und der Block erhält `DEFERRED_AFTER_VALIDATION`. Wird `T` nicht als `VALIDATED_PHENOMENON` abgeschlossen, erhält der Block `NOT_ACTIVATED_BY_T_GATE`. Die einzelnen Felder werden in beiden Fällen nicht mit Serien von `N/A` befüllt. Abschnitt `Z` bleibt von Beginn an aktiv, weil Entscheidungs-, Versions- und Ablehnungsgründe während des gesamten Research-Prozesses protokolliert werden müssen.

Die Dateien erfüllen verschiedene Funktionen:

| Datei | Funktion | Darf übersprungen werden? |
|---|---|---|
| `00_RESEARCH_AGENT_README.md` | Routing, Pflichtlogik, Nicht-Überspringen-Regeln | Nein |
| `01_RESEARCH_STANDARD.md` | Normativer Forschungsstandard | Nein |
| `02_RESEARCH_CASE_TEMPLATE.md` | Operatives Arbeitsartefakt je Research-ID | Nein |
| `03_RESEARCH_METHODS.md` | Methodenauswahl und Einsatzregeln | Nur einzelne nicht relevante Methodenabschnitte; Auswahl muss begründet werden |
| `04_CAUSAL_TOOLING.md` | Verbindlicher Router für Kausalbibliotheken, Umgebungen und Reproduzierbarkeit | Bei rein prädiktivem Research nach dokumentiertem `TOOLING_NOT_REQUIRED`; sonst nein |
| `05_AGENT_OPERATIONS.md` | Run-Provenance, Evidence Chain, Source Verification, Reviews, Evals und operative Freigaben | Bei jedem LLM-/Agentenlauf nein |
| `schemas/` | Maschinenlesbare Verträge für Hypothesen-Intake, Runs, Evidenz, Forecasts und Reviews | Nein, sobald der zugehörige Artefakttyp entsteht |
| `evals/` | Versionierter Eval-Satz und Regression Gate für Agentenänderungen | Vor produktiver Änderung an Prompt, Modell, Retrieval, Tools oder Output-Schema nein |
| `decisions/` | Architekturentscheidungen und ihre Konsequenzen | Nur für nicht betroffene Entscheidungen |

Dieses Paket ersetzt **nicht automatisch** aktive Projektregeln. Eine formale Aktivierung im Trading-Projekt erfolgt erst nach der dafür vorgesehenen Versions- und Freigabelogik.

---

## 2. Quellen- und Zuständigkeitsregel

Dieses Research-Paket regelt die **Entwicklung und Validierung neuer Marktphänomene, Edge-Hypothesen und Strategien**.

Es ersetzt keine operativen Trading-Regeln aus:

- `Trading_System.md`
- `Projekt-Workflow.md`
- `Chart_Indikator_Settings.md`
- `ACTIVE_DOCUMENTS.md`
- `Masterjournal.md`
- `ChangeLog.md`
- `LLM_README` des nativen Trading-Journals

Bei Konflikten mit aktiven Projektregeln gilt die bestehende Projekthierarchie. Neue Research-Ergebnisse sind **keine aktiven Trading-Regeln**, bis sie nach dem Projektprozess formal aktiviert wurden.

---

## 3. Nicht-Überspringen-Protokoll

Der Agent darf **keine Phase stillschweigend auslassen**.

Für jede Phase muss im Research-Artefakt genau einer der folgenden Zustände stehen:

- `COMPLETE` – vollständig bearbeitet.
- `N/A` – sachlich nicht anwendbar; Begründung ist Pflicht.
- `BLOCKED` – erforderlich, aber aktuell nicht ausführbar; fehlende Information oder Ressource muss benannt werden.
- `FAILED` – Gate oder Kriterium nicht bestanden.

Wird eine aktuelle Research-Version durch ein Gate beendet, erhalten alle dadurch nicht mehr erreichbaren späteren Abschnitte einmalig den Blockstatus `NOT_REACHED_DUE_TO_FAILED_GATE`; sie werden nicht einzeln künstlich ausgefüllt. Abschnitt `Z` bleibt für Abschluss und Begründung aktiv.

`BLOCKED` beendet die Research-Version nicht. Abhängige Folgeabschnitte bleiben unangetastet, Abschnitt `Z` protokolliert Blocker und fehlende Information, und dieselbe Version darf erst nach Auflösung des Blockers fortgesetzt werden. `NOT_REACHED_DUE_TO_FAILED_GATE` wird ausschließlich nach `FAIL` verwendet.

`N/A` ohne Begründung ist unzulässig.

Die einzige Blockausnahme ist der ausdrücklich bedingte Post-T-Bereich `U–Y`: `NOT_ACTIVATED_BY_T_GATE` oder `DEFERRED_AFTER_VALIDATION` ersetzt die Einzelstatus dieser fünf Abschnitte. Das ist kein Überspringen, sondern die vorab definierte Gate-Folge.

Ein Agent darf nicht aus Bequemlichkeit von `BLOCKED` zu einer späteren Phase springen, wenn die blockierte Phase eine Voraussetzung darstellt.

---

## 4. Gate-Regel

Die Research-Pipeline enthält echte Gates. Ein nicht bestandenes Gate darf nicht sprachlich in eine „interessante Beobachtung“ umetikettiert und übersprungen werden.

Gate- und Phasenstatus sind fest gekoppelt:

- `Gate PASS → Phase COMPLETE`
- `Gate FAIL → Phase FAILED`
- `Gate BLOCKED → Phase BLOCKED`

Nach `FAIL` oder `BLOCKED` ist kein abhängiger Folgeschritt zulässig.

Verbindliche Gates sind mindestens:

1. **Phase-0-Machbarkeitsgate**
2. **Kausalitäts-/Identifikationsgate**, sobald eine interventionale oder kontrafaktische Behauptung erhoben wird
3. **Mess-/Leakage-Gate**
4. **Pipeline-Integritätsgate**
5. **Freeze-Vollständigkeitsgate**
6. **Validation-Unabhängigkeitsgate**
7. **Ökonomisches Umsetzbarkeitsgate**
8. **Aktivierungsgate**

Für rein assoziative oder prädiktive Forschung lautet der Identifikationsstatus `NOT_REQUIRED_PREDICTIVE`; das ist kein kausales `PASS` und erlaubt keine kausale Sprache.

Wenn ein Gate `FAILED` ist, endet die aktuelle Research-Version. Eine Fortsetzung erfordert je nach Fall:

- mehr Daten,
- eine neue Research-Version,
- eine neue Hypothese,
- oder einen Abbruch.

---

## 5. Datenrollen sind unveränderlich

Jeder Datensatz muss eine Rolle erhalten:

- `DISCOVERY`
- `DEVELOPMENT`
- `VALIDATION`
- `FINAL_HOLDOUT`
- `FORWARD_OOS`

Ein Datensatz, dessen Ergebnis irgendeine Designentscheidung beeinflusst hat, ist ab diesem Zeitpunkt **Development Data**.

Das gilt auch, wenn nur:

- ein Schwellenwert geändert,
- ein Statefilter angepasst,
- ein Exit modifiziert,
- ein Nullmodell gewechselt,
- ein Outcome geändert,
- ein Datensplit verändert,
- eine neue Robustheitsmetrik gewählt

wurde.

Ein verbrauchtes Validation-Set darf nicht weiter als unabhängige Validation bezeichnet werden.

---

## 6. Kernregel gegen statistische Selbsttäuschung

Der Agent darf niemals aus `Anzahl Trades` automatisch auf `Anzahl unabhängiger Beobachtungen` schließen.

Er muss aktiv prüfen auf:

- serielle Abhängigkeit,
- überlappende Forward-Horizonte,
- wiederholte Signale desselben Marktimpulses,
- Event-/Sessioncluster,
- stark korrelierte Symbole,
- gemeinsame Makroereignisse,
- dominante Einzelbeobachtungen oder Cluster.

Wenn Abhängigkeit plausibel ist, muss die Inferenzmethode angepasst oder die Einschränkung ausdrücklich als `BLOCKED` ausgewiesen werden.

Bei weniger als 30 plausibel unabhängigen Clustern wird zusätzlich `SMALL_CLUSTER_WARNING` gesetzt. Das ist **kein automatisches FAIL** und keine Behauptung, jedes Intervall sei dann zwingend zu schmal. Der Warnstatus verlangt eine für wenige Cluster geeignete Methode, eine designspezifische Simulation/Kalibrierung oder eine ausdrückliche Einstufung als `BLOCKED`.

## 6a. Keine Rohidee ohne Intake und Scope

Eine durch Beobachtung, Paper, LLM, Sekundärquelle oder Marktgeschichte erzeugte
Idee ist zunächst `INBOX`. Der Agent MUSS Herkunft, Scope, vermuteten beobachtbaren
Footprint, Alternativerklärungen, Datenanforderungen, frühe Ausführbarkeitshürde und
bereits verbrauchte Daten protokollieren. Dubletten werden zusammengeführt, nicht
als unabhängige Ideen gezählt.

Für Intraday-Ideen sind Markt/Instrument, Venue/Feed, Handelsphase,
Kalender/Zeitzone/DST, Clock- oder Event-Time-Horizont und Ereignisklasse Pflicht.
Die News-/Makro-Policy wird als `INCLUDED_AS_SIGNAL`, `NOT_USED_AS_SIGNAL`,
`FILTER_KNOWN_EVENTS` oder `SCHEDULED_EVENT_STUDY` deklariert. Nur
`FILTER_KNOWN_EVENTS` mit benannten Feeds, Ausschlussfenstern und Coverage-Lücken
erlaubt eine qualifizierte Aussage über ausgeschlossene bekannte Ereignisse.

Der Agent führt getrennt:

- `mechanism_supported`,
- `forward_predictive_oos`,
- `executable_net_edge`.

Keine dieser Stufen wird aus einer früheren Stufe abgeleitet. Insbesondere ist ein
plausibler oder publizierter Mechanismus keine automatische Forward-Prognose und
keine handelbare Netto-Edge.

---

## 7. Kein Research ohne Phase 0

Bevor unabhängige Validation-Daten verbraucht werden, muss die wirtschaftlich-statistische Machbarkeit geprüft werden.

Phase 0 besteht aus zwei verpflichtenden Prüfungen:

1. **frühe Vorprüfung** mit konservativen Annahmen, bevor umfangreiche Discovery-/Development-Arbeit oder Holdout-Verbrauch gerechtfertigt wird,
2. **formale Re-Kalkulation vor Freeze**, nachdem Outcome, Nullmodell, Abhängigkeit, effektives N und Validation-Plan vollständig spezifiziert sind.

Ein frühes `WEITER` erlaubt nur Discovery und Development. Unabhängige Validation bleibt bis zum `PASS` der formalen Re-Kalkulation gesperrt.

Pflichtfelder:

1. minimale wirtschaftlich relevante Effektgröße,
2. typische Outcome-Skala,
3. explorativer Streuungs-Punktschätzer samt Unsicherheit und Quelle,
4. konservative Planungsstreuung beziehungsweise Stressszenario,
5. vorläufige Kostenhürde,
6. gewünschtes Signifikanz-/Fehlerniveau,
7. Ziel-Power oder äquivalentes Entscheidungsniveau,
8. getrennte Werte für Wirtschaftsgrenze `δ_econ` und angenommene Planungswirkung `δ_plan` beziehungsweise ein direktes Präzisionsziel,
9. benötigtes N beziehungsweise benötigte unabhängige Information im Basis- und Stressszenario,
10. verfügbares nominelles N sowie konservative Untergrenze des effektiven N,
11. Entscheidung `WEITER / DATEN BESCHAFFEN / ABBRECHEN`.

Die Mindeststichprobe darf **niemals** daraus abgeleitet werden, wie viele Fälle der letzte Datenexport zufällig enthält.

Ein einzelner Streuungs-Punktschätzer aus einer kleinen, selektierten oder nicht übertragbaren Discovery-Stichprobe reicht für `WEITER` nicht aus. Zulässig sind je nach Design beispielsweise externe oder gepoolte Referenzen, eine modellgültige obere Unsicherheitsgrenze, robuste Skalenmaße mit begründetem Stressaufschlag oder eine vorab definierte Szenariorechnung. Mindestens Basis- und konservatives Stressszenario müssen ausgewiesen werden.

Die Regel für das Stressszenario wird vor der Berechnung festgelegt. Unter mehreren vorab zulässigen und sachlich übertragbaren Kandidaten verwendet das Gate den konservativsten Wert oder berichtet die vollständige Bandbreite. Ein robustes Skalenmaß darf nur verwendet werden, wenn es nachvollziehbar auf die Stichprobenverteilung des primären Schätzers abgebildet wird. Im Stressszenario wird `DE < 1` beziehungsweise `N_eff > N` nicht angerechnet, sofern dieser Informationsgewinn nicht durch externe, übertragbare Evidenz und ein vorab festgelegtes Modell gestützt ist.

Wenn ein klassischer formaler Test verwendet wird und keine sachlich bessere Entscheidungsgrundlage existiert, gelten `α = 0,05` zweiseitig und `Power = 80 %` als **Arbeitsdefaults**. Bei knappem finalem Holdout oder hohen Kosten eines falsch-negativen Befunds sind `90 %` oder ein direktes Präzisionsziel zu prüfen. Arbeitsdefaults sind keine Qualitätsgarantie; jede Abweichung und jede einseitige Testung muss vor Kenntnis des Ergebnisses begründet werden.

---

## 8. Zeitliche Beobachtbarkeit ist Pflicht

Für jede Prädiktor-, State- und Trigger-Variable muss dokumentiert werden:

- welche Rohdaten sie benötigt,
- wann sie vollständig bekannt ist,
- ob sie zum Entscheidungszeitpunkt tatsächlich verfügbar war,
- welches Leakage-/Look-ahead-Risiko besteht.

Ein zurückgezeichneter oder nachträglich bestätigter Chartmarker gilt erst ab seinem tatsächlichen Bestätigungszeitpunkt als bekannt.

Wenn die Beobachtbarkeit nicht zuverlässig bestimmt werden kann, ist die Variable für den formalen Test nicht zulässig.

## 8a. Kausalstatus und Identifikation sind Pflichtfelder

Jede Research-Version deklariert vor dem Freeze ihre stärkste Behauptung als:

- `ASSOCIATIONAL_PREDICTIVE`,
- `INTERVENTIONAL`,
- oder `COUNTERFACTUAL`.

`ASSOCIATIONAL_PREDICTIVE` ist der Default. Eine interventionale oder kontrafaktische Behauptung benötigt zusätzlich:

- ein präzises kausales Estimand,
- einen versionierten DAG oder ein anderes explizites Strukturmodell,
- eine benannte Identifikationsstrategie,
- deren nicht aus den Daten allein ableitbare Annahmen,
- Negativkontrollen, Placebos oder Sensitivitätsanalysen soweit designspezifisch möglich,
- und ein bestandenes Identifikationsgate.

Ein LLM darf konkurrierende DAGs, Confounder-Kandidaten, Instrument-Kandidaten und testbare Konsequenzen vorschlagen. Es darf Pfeile nicht aufgrund plausibler Prosa als wahr deklarieren.

Die folgenden Ergebnisse sind für sich allein **kein** Kausalitätsnachweis:

- zeitliche Reihenfolge,
- Granger-Vorhersageverbesserung,
- Conditional-Independence- oder Causal-Discovery-Ausgabe,
- In-Sample-Fit,
- OOS-Stabilität,
- Backtest-Profitabilität,
- oder Double Machine Learning.

DML und andere flexible Schätzer dürfen erst nach Festlegung des kausalen Estimands und seiner Identifikationsannahmen als Kausalschätzer bezeichnet werden. Der `do(·)`-Operator ist nur zulässig, wenn tatsächlich eine interventionale Größe identifiziert wird.

Bei Event-Research werden Veröffentlichungswert und Schock getrennt. Der Schock wird aus einer vor dem Event verfügbaren Erwartung konstruiert; Erwartungsquelle, Daten-Vintage, Zeitstempel, Skalierung, Eventfenster und konkurrierende Nachrichten werden protokolliert.

Eine Abweichung zwischen erwarteter und tatsächlicher Marktreaktion heißt zunächst `REACTION_INNOVATION` oder `REACTION_ANOMALY`. Sie darf nur dann `CAUSAL_CHAIN_BREAK` heißen, wenn die relevante Kette einschließlich Mediatoren kausal identifiziert und gegen vorab definierte Alternativerklärungen getestet wurde.

Goldratts Effect-Cause-Effect-Logik darf **optional** in Discovery verwendet werden, wenn eine mehrgliedrige Wirkungskette behauptet wird. Sie strukturiert die Vermutung, liefert aber weder einen DAG noch Evidenz für einen Pfeil. Jeder relevante Knoten wird anschließend als direkt messbar, Proxy, latent oder unbrauchbar klassifiziert und in die Pearl-/Identifikationsprüfung überführt.

Für quantitative Event-Analyse ist kein „Goldratt-Constraint-Score“ vorgesehen. Der Default sind:

- wenige ökonomisch begründete Surprise-Faktoren,
- einfache Event-Response-Regressionen,
- vor dem Event bekannte State-Interaktionen,
- zeitlich OOS berechnete Reaktionsinnovationen,
- und ein inkrementeller OOS-Vergleich gegen ein einfacheres Nullmodell.

Ein Kettenglied darf nicht wegen hoher Korrelation, großem `|z|` oder einer plausiblen Geschichte zum „Constraint“ erklärt werden. Das Wort wird nur mit definiertem Systemziel und einem der folgenden Labels verwendet:

- `TRANSMISSION_DIAGNOSTIC` – beschreibender Pass-through oder Residualbefund,
- `INFORMATION_BOTTLENECK_CANDIDATE` – liefert eingefroren und OOS zusätzliche Prognoseinformation für das End-Outcome,
- `IDENTIFIED_CAUSAL_LEVER` – kausales Estimand und Identifikationsgate bestanden,
- `IMPLEMENTATION_CONSTRAINT` – Daten-, Timing-, Liquiditäts-, Kosten- oder Prozessengpass.

Goldratt ist vor allem für `IMPLEMENTATION_CONSTRAINT` und die Ableitung nächster Prozessschritte geeignet. Für Markttransmission bleiben Pearl und die quantitativen Tests zuständig.

## 8b. Spezialisierte Kausalbibliotheken sind bei passender Aufgabe Pflicht

Sobald ausführbarer Code für DAG-Prüfung, Identifikation, kausale Effektschätzung, Refutation oder Causal Discovery benötigt wird, muss der Agent den Router in `04_CAUSAL_TOOLING.md` anwenden. Der Default ist eine spezialisierte, dokumentierte Bibliothek statt einer ad hoc selbst geschriebenen Implementierung:

- `DoWhy` für den Model–Identify–Estimate–Refute-Workflow,
- `pgmpy` für Graph-, d-Separation-, Adjustierungs- und kausale Abfragen,
- `EconML` oder `DoubleML` für DML beziehungsweise heterogene Effekte nach bestandener Identifikation,
- `Tigramite` für zeitserienspezifische Causal Discovery,
- `causalinference` nur optional für seinen engen Matching-/Propensity-Anwendungsbereich.

Es gilt kein Paketzwang für rein prädiktive Eventregressionen oder einfache Reaktionsinnovationen. Der Status lautet je Research-Version `TOOLING_REQUIRED`, `TOOLING_NOT_REQUIRED` oder `TOOLING_BLOCKED` und wird begründet.

Bibliotheksausgaben ändern den Claim-Level nicht. Insbesondere machen ein gefundener Adjustmentsatz, ein DML-Schätzer, ein Refutationstest oder ein Discovery-Graph aus einer nicht identifizierten Frage keinen Kausalclaim. Vor Ausführung werden Python-, Paket- und API-Versionen, Zufallsseed, Splits, Estimand, Graph, Adjustmentsatz und relevante Warnungen protokolliert. Nicht getestete Paketkombinationen benötigen einen Kompatibilitäts-Smoke-Test; bei Fehlschlag gilt `TOOLING_BLOCKED`.

Ein LLM muss dafür nicht trainiert werden. Manche Schätzer fitten projektspezifisch Nuisance- oder Effektmodelle; das ist gewöhnliche statistische Schätzung innerhalb der Research-Pipeline, kein Training eines neuen Sprachmodells.

---

## 8c. Wissenschaftliche Quellen benötigen Werk-, Versions- und Integritätsprovenienz

Für jede akademische Quelle gilt zusätzlich **05_AGENT_OPERATIONS.md §5.4** und das Academic-Metadata-Objekt aus **schemas/evidence.schema.json**.

Pflichtlogik:

1. Eine **work_id** verbindet Preprint, Working Paper, Accepted Manuscript, Version of Record, Korrektur und weitere Fassungen derselben intellektuellen Arbeit.
2. Jede tatsächlich verwendete Fassung besitzt eine eigene **source_id**, exakte Version, URI, Abrufzeit und Snapshot-Hash.
3. Mehrere Fassungen oder Indizes derselben work_id zählen nie als unabhängige Bestätigungen.
4. Publikationsstatus, DOI und Venue werden verifiziert; ein DOI oder Journalname ist kein Qualitätsbeweis.
5. Bei einschlägigen Finance-Fragen werden **The Journal of Finance** und das **Journal of Financial Economics** gezielt durchsucht. Das ist eine Coverage-Regel, kein Prestige-Gate und kein Ausschluss anderer Primärquellen.
6. Bei arXiv werden q-fin-Unterkategorie und konkrete Versionsnummer gespeichert. Zulässig sind **q-fin.CP / q-fin.EC / q-fin.GN / q-fin.MF / q-fin.PM / q-fin.PR / q-fin.RM / q-fin.ST / q-fin.TR**. Die Kategorie ist Themenklassifikation, kein Peer Review.
7. Vor Freeze, externer Freigabe und Revalidierung werden Correction, Expression of Concern, Retraction und Withdrawal über Publisher/Journal, Crossmark/DOI-Metadaten, Crossref-Retraction-Watch und Repository-Historie geprüft.
8. Code-, Daten- und Replikationsstatus werden getrennt erfasst. Verfügbarkeit ist kein Qualitätsbeweis; technische Reproduktion beweist weder Identifikation noch externe Validität.

Eine zurückgezogene oder retraktierte Arbeit darf den betroffenen Sachclaim nicht weiter positiv tragen. Der Claim wird nach Evidence-Ruleset **1.1.0** **INSUFFICIENT**, und die Änderung ist mindestens ein operatives **BREAKING**-Delta. Eine materielle Korrektur, neue arXiv-Version, geänderte Deduplizierung oder konfligierende Replikation erzwingt eine erneute Claim-, Grade- und Delta-Prüfung.

Ändert die Quellenrevision Hypothese, Design, Gate oder Entscheidung, gelten zusätzlich die Research-Versions- und Datenverbrauchsregeln aus Abschnitt 16. Reine bibliografische Formatkorrekturen ohne semantische Auswirkung bleiben operative **NON_MATERIAL**-Deltas.

---

## 9. Keine heimliche Hypothesenrevision

Ein unerwartetes Ergebnis darf nicht durch semantische Umdeutung zum Erfolg erklärt werden.

Beispiel:

- Hypothese: `Mean Reversion`
- Ergebnis: stabiler `Continuation`-Effekt

Dann gilt:

- ursprüngliche Hypothese falsifiziert,
- mögliche neue Hypothese entdeckt,
- neue Research-ID oder neue Hauptversion erforderlich,
- neue Freeze- und Validation-Sequenz erforderlich.

---

## 10. Pipeline-Integritätsprüfung ist Pflicht

Vor dem Freeze muss die **vollständige ausführbare Research-Pipeline** auf Kontroll-Daten geprüft werden. Mindestens vorzusehen sind:

- wiederholte Null-/Surrogatläufe, die relevante Zeit-, Cluster-, State- und Volatilitätsstruktur soweit wie methodisch möglich erhalten,
- dieselben Auswahl-, Filter- und Auswertungsschritte wie im echten Research,
- mindestens ein synthetischer Test mit bekanntem Vorzeichen und bekanntem Timing, um Vorzeichen-, Indexierungs- und Look-ahead-Fehler aufzudecken,
- vorab definierte Toleranzen für Fehlalarme, Richtung, Timing und erwartete Nullverteilung.

Kontrollbasis und Datenrolle werden protokolliert. Designbeeinflussende Pipeline-Tests dürfen keine unabhängigen Validation- oder Holdout-Daten verbrauchen. Für die Nullkontrollen wird vorab eine Zielpräzision der geschätzten Fehlalarmrate festgelegt; `PASS` setzt ausreichende Monte-Carlo-Präzision voraus.

Ein einzelner Shuffle- oder Random-Walk-Lauf genügt nicht. Zerstört eine Kontrolle die für den Test relevante Abhängigkeitsstruktur, muss sie angepasst oder als unzureichend markiert werden.

Das Ergebnis lautet `PASS / FAIL / BLOCKED`. Ohne `PASS` darf der Freeze nicht bestätigt werden.

---

## 11. Vier Ergebniszustände statt „signifikant / nicht signifikant“

Ein Validation-Ergebnis muss mindestens in einen dieser Zustände eingeordnet werden:

1. **Erwarteter wirtschaftlich relevanter Effekt ausreichend präzise gestützt**
2. **Entgegengesetzter wirtschaftlich relevanter Effekt ausreichend präzise gestützt**
3. **Kein wirtschaftlich relevanter Effekt ausreichend präzise gestützt**
4. **Unpräzise / unentscheidbar**

Zustand 4 erlaubt **keine ergebnisgetriebene Revision**. Zulässig sind nur:

- mehr unabhängige Daten,
- methodisch bereits vorab definierte Zusatzanalyse,
- oder Abbruch als unentscheidbar.

---

## 12. Einflussdiagnostik ist Pflicht

Vor Validation wird festgelegt, wie geprüft wird, ob einzelne Beobachtungen oder Cluster das Ergebnis dominieren.

Mindestens vorzusehen:

- Leave-one-out oder Leave-one-cluster-out,
- Ergebnis ohne dominantes Symbol,
- Ergebnis ohne dominante Zeit-/Eventgruppe,
- Anteil der größten Beobachtung/des größten Clusters an einer vorab definierten Ergebnis- oder Streuungsgröße.

Wenn das Entfernen eines einzelnen Clusters das Vorzeichen oder die wirtschaftliche Schlussfolgerung kippt, gilt die Evidenz grundsätzlich als **nicht robust bestätigt**, sofern der Freeze nicht ausdrücklich eine andere, sachlich begründete Regel vorsieht.

---

## 13. Heavy-Tail-Regel

Bei schwerschwänzigen Outcomes muss vor Validation festgelegt werden:

- primärer Lageparameter,
- robuste Sensitivitätskennzahl,
- Umgang mit Ausreißern,
- ob Winsorisierung/Trimming zulässig ist,
- und ob diese Transformation Teil der primären oder nur der Sensitivitätsanalyse ist.

Der Schätzer darf nicht nach Kenntnis des Validation-Ergebnisses gewechselt werden.

---

## 14. Kostenlogik in zwei Stufen

Kosten werden zweimal geprüft:

### Früh: Phase-0-Machbarkeit

Grobe, konservative Kostenhürde, damit keine knappen Holdout-Daten für einen Effekt verbraucht werden, der wirtschaftlich ohnehin zu klein wäre.

### Spät: Strategy Engineering

Detailliertes, möglichst zustandsabhängiges Modell:

`Kosten = f(State, Volatilität, Liquidität, Größe, Geschwindigkeit, Session, Execution)`

Das frühe Kostengate ersetzt die spätere Execution-Prüfung nicht.

Die Sicherheitsmarge ist ein **zusätzlicher Betrag** zur konservativen Kostenschätzung. Wird stattdessen ein Multiplikator verwendet, muss ausdrücklich unterschieden werden zwischen `Gesamthürde = Multiplikator × Kosten` und `Sicherheitsmarge = Multiplikator × Kosten`. Es gibt keinen universellen Kostenmultiplikator für alle Strategien.

---

## 15. Agenten-Ausgabeformat nach jedem Arbeitsschritt

Nach jeder bearbeiteten Phase muss der Agent festhalten:

```text
PHASE:
STATUS: COMPLETE / N/A / BLOCKED / FAILED
INPUTS:
ENTSCHEIDUNGEN:
OFFENE PUNKTE:
GATE-ERGEBNIS:
NÄCHSTER ZULÄSSIGER SCHRITT:
```

Keine Phase endet mit bloßer Prosa ohne Status.

---

## 16. Versionierung

Jede Research-Datei benötigt mindestens:

- Research-ID,
- Version,
- Status,
- Erstellungsdatum,
- Freeze-Datum,
- Datenrollen,
- DAG-Version,
- Tooling-Manifest mit Laufzeit-, Paket- und API-Versionen oder `TOOLING_NOT_REQUIRED`,
- Hypothesenversion,
- Entscheidungsprotokoll.

Materielle Änderungen erzeugen eine neue Version.

Materiell sind insbesondere Änderungen an:

- Hypothese,
- Claim-Level oder kausalem Estimand,
- Identifikationsstrategie oder deren Kernannahmen,
- primäre Kausalbibliothek, Haupt-API, Versionskombination oder Split-/Seed-Logik,
- Surprise-Konstruktion, Eventfenster oder Reaktionsmodell,
- Surprise-Faktoren, optionale ECE-/Mechanism-Map oder Constraint-Definition,
- Richtung des erwarteten Effekts,
- Nullmodell,
- Outcome,
- Datenuniversum,
- Session,
- Timeframe,
- Statefilter,
- Trigger,
- Invalidation,
- Stop,
- Target,
- Management,
- Kostenmodell,
- Datensplit,
- primärer Auswertungsmethode.

Bei akademischen Quellen sind eine neue Fassung, ein geänderter Publikations-/Integritätsstatus, eine materielle Correction, eine Retraction/Withdrawal, ein Replikationskonflikt oder eine Deduplizierung mit veränderter unabhängiger Evidenz zunächst operative Deltas nach **05 §5.4.8 und §9**. Sobald dadurch Hypothese, Methode, Gate, Evidenzschluss oder Endentscheidung verändert wird, ist die Research-Änderung materiell und erzeugt eine neue Version.

---

## 16a. Operative Agentenartefakte und Regression Gate

Research-Version und Agentenlauf sind verschiedene Identitäten:

- Die **Research-ID/Research-Version** bezeichnet den fachlichen Forschungsstand.
- Die **Run-ID** bezeichnet genau eine konkrete Ausführung dieses Stands mit einem bestimmten Modell, Prompt, Tool- und Datenzustand.

Für jeden LLM-/Agentenlauf gelten zusätzlich die Verträge aus `05_AGENT_OPERATIONS.md` und `schemas/`:

1. Vor Eröffnung eines Research Case wird ein valider Hypothesen-Intake persistiert und auf `PROMOTED` gescreent.
2. Vor der Ausführung wird eine eindeutige Run-ID erzeugt; das Run-Manifest wird spätestens bei Laufabschluss vollständig persistiert.
3. Entscheidungsrelevante Aussagen erhalten eine epistemische Klasse und eine Claim-ID.
4. Fakten benötigen eine konkrete Quelle und Fundstelle; berechnete Werte und Inferenzclaims referenzieren ihre Inputs.
5. Akademische Quellen erhalten work_id, konkrete Fassung, Publikations-/Integritätsstatus sowie Code-, Daten- und Replikationsstatus; Fassungen derselben Arbeit werden dedupliziert.
6. Fehlende Evidenz wird als `UNKNOWN` beziehungsweise blockierender Evidenzstatus ausgewiesen und nicht durch plausible Prosa ersetzt.
7. Menschliche Korrekturen und Overrides werden append-only gespeichert und dürfen nicht still überschrieben werden.
8. Änderungen an System-/Task-Prompt, Modell oder Snapshot, Retrieval, Toolbeschreibung, Orchestrierung oder Output-Schema benötigen vor produktiver Freigabe einen bestandenen Eval- und Regressionslauf.
9. Ein syntaktisch oder semantisch ungültiges Pflichtartefakt, eine ungeklärte kritische Quellenkollision oder eine nicht akzeptierte Regression blockiert die operative Freigabe, auch wenn das Research-Ergebnis inhaltlich plausibel klingt.

Ein einzelnes Run-Manifest ersetzt weder das Research Case noch dessen Gates. Umgekehrt macht ein methodisch vollständiges Research Case einen nicht reproduzierbaren Agentenlauf nicht operativ freigabefähig.

---

## 17. Abschlussregel

Ein AI-Agent darf eine Research-Idee nur dann als `VALIDATED_PHENOMENON` oder `ACTIVE_STRATEGY_CANDIDATE` bezeichnen, wenn das zugehörige Research-Artefakt die vorgeschriebenen Gates bestanden hat.

Fehlende Daten, nicht geprüfte Abhängigkeiten, ein verbrauchtes Validation-Set oder eine ungeprüfte entscheidungstragende akademische Quellenfassung sind keine redaktionellen Kleinigkeiten, sondern Zustandsfehler des Research-Prozesses.
