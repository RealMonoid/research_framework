# 00_RESEARCH_AGENT_README.md

**Version:** 2.2
**Stand:** 2026-08-31
**Status:** ENTWURF ZUR ÜBERNAHME  
**Zweck:** Verbindliche Lese- und Ausführungsanweisung für AI-Agenten, die Trading-Research-Projekte bearbeiten.

---

## 1. Gestaffelter Einstieg und Dokumentrouter

Jede vorhandene neue Idee beginnt mit `QUICKSTART.md` und einem Intake nach
`schemas/hypothesis_candidate.schema.json`. Wenn noch keine Rohidee existiert,
kann davor optional `scripts/generate_hypotheses.py` den versionierten Katalog
`generation/mechanism_catalog.v1.json` in günstige `INBOX`-Kandidaten
überführen. Dieser Generator ist eine Produktionsschicht und trifft keine
Screening-, Evidenz-, Backtest- oder Promotionsentscheidung.

Für `INBOX`, `MERGED` oder `REJECTED` müssen die sechs Detaildokumente nicht
vorab geladen werden. Der kurze Intake hält dennoch Herkunft, Rohidee und bereits
verbrauchte Informationsreferenzen fest.

Erst ein `PROMOTED`-Intake öffnet Phase 0; Promotion ist keine
Evidenzbestätigung. Dann werden `00_RESEARCH_AGENT_README.md` und
`01_RESEARCH_STANDARD.md` geladen. `02_RESEARCH_CASE_TEMPLATE.md` wird beim
Anlegen des konkreten Research Case verwendet. Aus `03_RESEARCH_METHODS.md`,
`04_CAUSAL_TOOLING.md` und `05_AGENT_OPERATIONS.md` werden nur die durch Methode,
Claim-Level und erzeugten Artefakte aktivierten Abschnitte geladen.

Jeder tatsächliche Agentenlauf erhält ein valides Run-Manifest nach
`schemas/run_manifest.schema.json`. Entscheidungsrelevante Aussagen, menschliche
Reviews und echte Eval-Ergebnisse werden nach `05_AGENT_OPERATIONS.md` als
getrennte operative Artefakte geführt und im Research Case referenziert.

Die Abschnitte `U–Y` dieser Kopie bleiben bis zu einer bestandenen Phänomen-Entscheidung in Abschnitt `T` **inaktiv**. Nach `VALIDATED_PHENOMENON` werden sie nur durch eine ausdrückliche Fortsetzungsentscheidung aktiviert; andernfalls bleibt `VALIDATED_PHENOMENON` ein zulässiger eigenständiger Endzustand und der Block erhält `DEFERRED_AFTER_VALIDATION`. Wird `T` nicht als `VALIDATED_PHENOMENON` abgeschlossen, erhält der Block `NOT_ACTIVATED_BY_T_GATE`. Die einzelnen Felder werden in beiden Fällen nicht mit Serien von `N/A` befüllt. Abschnitt `Z` bleibt von Beginn an aktiv, weil Entscheidungs-, Versions- und Ablehnungsgründe während des gesamten Research-Prozesses protokolliert werden müssen.

Die Dateien erfüllen verschiedene Funktionen:

| Datei | Funktion | Wann laden? |
|---|---|---|
| `QUICKSTART.md` | Kurzpfad, Enforcement-Grenze und Statusrouter | Immer |
| `generation/mechanism_catalog.v1.json` | Literaturgestützte Mechanismen für Intraday- und kurze Swing-Ideen | Wenn Ideen erzeugt oder der Katalog erweitert werden soll |
| `generation/README.md` | Bedienung und Grenzen des Generators | Bei einem Generatorlauf |
| `agents/intraday-hypothesis-generator.md` | Optionaler autonomer Generatorvertrag | Bei agentischer Ideenerzeugung |
| `agents/scientific-philosophy-critic.md` | Begriffs-/Voraussetzungspruefung vor Operationalisierung sowie Duhem-Quine-/Lakatos-/Kuhn-Fortsetzungspruefung | Vor Abschluss jeder unvollstaendig definierten Quellenrekonstruktion; nach nicht positivem Q8-Ergebnis bei materieller Revision oder Fortsetzung |
| `agents/condition-inquiry-analyst.md` | Quantitative Beurteilung von Messinstrumenten und Erzeugung beobachtbarer Bedingungshypothesen | Nach vorlaeufiger Operationalisierung, wenn Messnutzen, Definitionsabhaengigkeit oder unbekannte Erfolgsmodifikatoren untersucht werden |
| `reconstruction/README.md` | Quellennahe Übersetzung von Buch-/Artikel-/Video-/Kursstrategien | Wenn eine Quellenstrategie nicht vollständig operationalisiert ist |
| `00_RESEARCH_AGENT_README.md` | Routing, Gate- und Nicht-Überspringen-Regeln | Ab `PROMOTED` |
| `01_RESEARCH_STANDARD.md` | Normativer Forschungsstandard | Ab `PROMOTED` |
| `02_RESEARCH_CASE_TEMPLATE.md` | Operatives Arbeitsartefakt je Research-ID | Beim Eröffnen eines Research Case |
| `03_RESEARCH_METHODS.md` | Methodenauswahl und Einsatzregeln | Nur ausgewählte Methodenabschnitte |
| `04_CAUSAL_TOOLING.md` | Router für ausführbare kausale Kernoperationen | Bei `TOOLING_REQUIRED` |
| `05_AGENT_OPERATIONS.md` | Provenance, Evidence, Reviews, Evals und Freigabe | Passende Abschnitte bei den jeweiligen Artefakten/Systemänderungen |
| `schemas/` | Maschinenlesbare Artefaktverträge | Sobald der Artefakttyp entsteht |
| `evals/` | Producer, Scorer und Regression Gate | Bei Agenten-/Prompt-/Modell-/Tooländerungen |
| `decisions/` | Architekturentscheidungen und Konsequenzen | Bei betroffener Entscheidung |

## 1.1 Enforcement-Grenze

Ein Agent, der `COMPLETE`, `PASS` oder `SUPPORTED` schreibt, beweist damit nichts.
Diese Werte sind Selbstdeklarationen, solange nicht das zugehörige Artefakt gegen
ein Schema geprüft, die Evidence-Referenz aufgelöst oder ein unabhängiges Review
dokumentiert wurde. Normative Prosa steuert Verhalten, ist aber keine technische
Enforcement.

Automatisch durchgesetzt werden ausschließlich explizit benannte Schemas, Tests,
Eval-Gates und CI-Checks. Ein grüner `PROTOCOL_SMOKE` bestätigt nur Verträge und
Scorer. Eine Aussage über Modell- oder Promptqualität benötigt einen blind
produzierten `LIVE_AGENT`-Lauf.

Dieses Paket ersetzt **nicht automatisch** aktive Projektregeln. Eine formale Aktivierung im Trading-Projekt erfolgt erst nach der dafür vorgesehenen Versions- und Freigabelogik.

## 1.2 Verständliche Nutzerkommunikation ist Pflicht

Der Nutzer wird als fachlicher Entscheider behandelt, nicht als
Softwareentwickler. Interne Präzision und externe Sprache sind zwei getrennte
Ebenen: Artefakte, Schemas, Logs und Tests behalten ihre exakten Begriffe; die
sichtbare Nutzerantwort übersetzt deren Bedeutung in gewöhnliche Sprache.

Jede Nutzerantwort MUSS:

- mit Ergebnis, Bedeutung und einer eventuell offenen Entscheidung beginnen,
- Fachbegriffe vermeiden oder bei erster Verwendung einfach erklären,
- interne Codes in Alltagssprache übersetzen,
- technische Implementierungsdetails weglassen, solange sie weder Ergebnis noch
  Risiko noch Nutzerentscheidung verändern,
- bei einer notwendigen Entscheidung Frage, Anlass, Möglichkeiten, praktische
  Folgen und eine begründete Empfehlung erklären,
- deutlich sagen, wenn der Nutzer nichts entscheiden oder technisch tun muss.

Der Agent DARF NICHT ungefragt Funktions-, Klassen-, Adapter-, Import-, Schema-,
CI- oder Testdetails als Fortschritts- oder Abschlussbericht ausgeben. Dateinamen
und interne Statusfelder werden nur genannt, wenn der Nutzer sie verlangt oder
für Nachvollziehbarkeit wirklich benötigt. Dass ein Agent etwas implementiert
oder geprüft hat, ist kein Anlass, den Nutzer mit dem technischen Weg dorthin zu
belasten.

Diese Regel gilt auch für statistische, kausale und wissenschaftsphilosophische
Fachsprache. Die präzise Bezeichnung darf intern bestehen bleiben; nach außen
muss zuerst erklärt werden, was sie im konkreten Fall bedeutet.

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

Der Agent darf innerhalb des durch Status und Router aktivierten Pfads **keine
Phase stillschweigend auslassen**. Nicht aktivierte Methoden oder Artefakttypen
erzeugen keine künstlichen Serien von `N/A`-Einträgen.

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

## 4.1 Begriffs- und Voraussetzungenprüfung vor Operationalisierung

Eine aus unvollständiger Prosa rekonstruierte Strategie darf nicht als
`RECONSTRUCTION_COMPLETE` oder `DISCRETIONARY_PROTOCOL_COMPLETE` abgeschlossen
werden, bevor der `scientific-philosophy-critic` ein
`strategy_concept_audit` nach
`schemas/strategy_concept_audit.schema.json` erstellt hat.

Das Audit trennt strategiedefinierende Bedingungen, von der Quelle genannte
Anwendungsbedingungen, vermutete Erfolgsmodifikatoren und unbekannte
Erfolgsbedingungen. Vermutete oder unbekannte Bedingungen dürfen nicht als
Pflichtfilter in die Quellenstrategie gelangen.

Trigger, Zustand, Ziel und Outcome werden auf gemeinsame Rohdaten, Fenster und
deterministische Berechnungen geprüft. Eine solche Konstruktionsabhängigkeit
kann eine Assoziation mit erzeugen oder die beantwortete Frage verändern. Sie
ist weder Kausalbeleg noch automatisch ein Fehler.

Regime-, State- und Kontextfilter gelten als vorläufige Messinstrumente. Ihre
Klassenhäufigkeit misst keine Trennleistung. Auch eine spätere prognostische
Trennung beweist keinen buchstäblich realen verborgenen Zustand, Akteur oder
Mechanismus.

Nach vorläufiger Operationalisierung kann ein `condition_inquiry` nach
`schemas/condition_inquiry.schema.json` aktiviert werden. Es kann neue
Bedingungshypothesen erzeugen. Datenbasiert gefundene Bedingungen werden als
neue Erfolgsmodifikator-Hypothesen geführt und nicht rückwirkend als Bestandteil
der Quellenstrategie ausgegeben.

## 4.2 Wissenschaftsphilosophische Fortsetzungsprüfung

`FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE` und `INVALID_TEST` bleiben Ergebnisse
der eingefrorenen Research-ID. Sie werden nicht dadurch umetikettiert, dass nach
dem Ergebnis eine Operationalisierung, Hilfsannahme oder Stichprobe verdächtig
erscheint.

Sobald nach einem solchen Q8-Ergebnis eine materielle Revision oder ein neuer
empirischer Test erwogen wird, ist der Agentenvertrag
`agents/scientific-philosophy-critic.md` zu laden und ein
`scientific_philosophy_review` nach
`schemas/scientific_philosophy_review.schema.json` anzulegen. Der Review:

- macht nach Duhem-Quine das getestete Bündel sichtbar,
- behauptet ohne unterscheidende Evidenz keine eindeutige Fehlerursache,
- trennt nach Lakatos progressive, degenerative und rein diagnostische Änderungen,
- und verwendet Kuhns Anomalie-/Rivalenperspektive nur zur Beurteilung des
  Forschungsprogramms, nie zur Rettung des eingefrorenen Einzeltests.

Empirische Fortsetzung ist nur als neue Research-ID zulässig, wenn die Revision
eine zuvor nicht implizierte, widerlegbare Vorhersage und einen unabhängigen
Evaluationsplan festhält. Diagnostik darf Fehler lokalisieren, validiert aber
weder die alte noch die neue Hypothese.

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
Idee ist zunächst `INBOX`. In diesem Status protokolliert der Agent nur Identität,
Herkunft, Rohidee und bereits verbrauchte Informationsreferenzen. Dubletten werden
zusammengeführt, nicht als unabhängige Ideen gezählt. Scope, beobachtbarer
Footprint, Alternativerklärungen, Datenanforderungen und frühe
Ausführbarkeitshürden werden schrittweise ergänzt und sind erst für `PROMOTED`
vollständig Pflicht.

Vor `PROMOTED` benötigt eine beobachtungsgetriebene Idee einen verknüpften
Noise Screen mit Status `PASS / FAIL / BLOCKED`. Dessen Search-Space-Register
fixiert Kandidatenuniversum,
Familiengröße, Alpha und Korrekturmethode vor dem ersten Ergebnis. Ein Waiver ist
nur für theoriegetriebene, terminierte Event- oder publizierte
Replikationsideen mit Begründung zulässig. `PASS` erlaubt Phase-0-Aufwand und ist
keine Evidenz. Schema plus `scripts/validate_entry_thresholds.py` erzwingen
Zeitreihenfolge, Quotient, Registerabgleich und Multiplikität. Bei mehr als
einem geplanten Screen ist eine Korrektur zwingend; `NONE_JUSTIFIED` ist nur
für eine Ein-Test-Familie zulässig.

Für promovierte Intraday-Ideen sind Markt/Instrument, Venue/Feed, Handelsphase,
Kalender/Zeitzone/DST, Clock- oder Event-Time-Horizont und Ereignisklasse Pflicht.
Die News-/Makro-Policy wird als `INCLUDED_AS_SIGNAL`, `NOT_USED_AS_SIGNAL`,
`FILTER_KNOWN_EVENTS` oder `SCHEDULED_EVENT_STUDY` deklariert. Nur
`FILTER_KNOWN_EVENTS` mit benannten Feeds, Ausschlussfenstern und Coverage-Lücken
erlaubt eine qualifizierte Aussage über ausgeschlossene bekannte Ereignisse.

`PROMOTED` verlangt außerdem einen Record zur Variablen- und Konstruktauswahl.
Bei `PREDEFINED` genügen eine knappe Begründung und die beibehaltenen Variablen.
Bei `DATA_DRIVEN` oder `HYBRID` werden Kandidatenuniversum, Selektionsdaten und
deren Datenrolle, Outcome-Sichtbarkeit, Auswahlmethoden, effektive
Kandidatenzahl, Suchraum und Auswahlbias-Kontrollen protokolliert. Jede dabei
verwendete Information wird zugleich in `consumed_data_refs` erfasst; unabhängige
Validation oder Holdout-Daten dürfen die Auswahl nicht beeinflussen.

Zusätzlich ist bei `PROMOTED` ein `actor_constraint` Pflicht. Er enthält
entweder Akteur, Zwang, erwartete Handlung, beobachtbaren Bezug und mindestens
eine konkurrierende Akteurshypothese oder dokumentiert ausdrücklich
`UNSPECIFIED / NOT_CLAIMED`. Der zweite Zustand ist für begrenzte
assoziative/prädiktive Fragen zulässig und verhindert, dass ein Akteur erfunden
wird; er liefert keinerlei Mechanismusnachweis.

Der Agent führt getrennt:

- `mechanism_supported`,
- `forward_predictive_oos`,
- `executable_net_edge`.

Keine dieser Stufen wird aus einer früheren Stufe abgeleitet. Insbesondere ist ein
plausibler oder publizierter Mechanismus keine automatische Forward-Prognose und
keine handelbare Netto-Edge.

Diese drei Status bilden eine andere Achse als der Research-Claim-Level
`ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`. Ein identifizierter
interventionaler Effekt kann wirtschaftlich unhandelbar sein; eine rein
assoziative Prognose kann dagegen eine ausführbare Netto-Edge besitzen. Weder
Claim-Level noch Stufenstatus werden aus der jeweils anderen Achse abgeleitet.

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
- ein versioniertes SCM/DAG, Potential-Outcomes-Design,
  strukturell-ökonometrisches oder anderes explizites Identifikationsmodell,
- eine benannte Identifikationsstrategie,
- deren nicht aus den Daten allein ableitbare Annahmen,
- Negativkontrollen, Placebos oder Sensitivitätsanalysen soweit designspezifisch möglich,
- und ein bestandenes Identifikationsgate.

Die Wahl zwischen graphischer, kontrafaktischer oder anderer expliziter
Formulierung ist eine Modellierungsentscheidung und erhöht den Claim-Level nicht.
Bei Potential Outcomes werden insbesondere Konsistenz, Positivity, die für das
Design benötigte Assignment-/Exchangeability-Annahme und Interferenz
beziehungsweise ein Exposure Mapping ausdrücklich behandelt. Ein DAG ist dort
nicht zusätzlich Pflicht, wenn das Identifikationsdesign dieselben relevanten
Annahmen explizit macht.

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

Für quantitative Event- und Transmissionsanalyse sind die Defaults:

- wenige ökonomisch begründete Surprise-Faktoren,
- einfache Event-Response-Regressionen,
- vor dem Event bekannte State-Interaktionen,
- zeitlich OOS berechnete Reaktionsinnovationen,
- und ein inkrementeller OOS-Vergleich gegen ein einfacheres Nullmodell.

Ein Kettenglied darf nicht wegen hoher Korrelation, großem `|z|` oder einer
plausiblen Geschichte zum „Constraint“ erklärt werden. Das Wort wird nur mit
definiertem Systemziel und einem der folgenden Labels verwendet:

- `TRANSMISSION_DIAGNOSTIC` – beschreibender Pass-through oder Residualbefund,
- `INFORMATION_BOTTLENECK_CANDIDATE` – liefert eingefroren und OOS zusätzliche Prognoseinformation für das End-Outcome,
- `IDENTIFIED_CAUSAL_LEVER` – kausales Estimand und Identifikationsgate bestanden,
- `IMPLEMENTATION_CONSTRAINT` – Daten-, Timing-, Liquiditäts-, Kosten- oder Prozessengpass.

`IDENTIFIED_CAUSAL_LEVER` und `IMPLEMENTATION_CONSTRAINT` werden zusätzlich gegen
`schemas/constraint_assessment.schema.json` geprüft. Goldratts Fokuslogik ist nur
noch ein optionales Denkwerkzeug nach Phänomen-Validation für bereits belegte
`IMPLEMENTATION_CONSTRAINT`-Engpässe. Sie gehört nicht zur frühen
Markttransmissions- oder Identifikationsanalyse.

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

## 15. Internes Arbeitsprotokoll und verständliche Nutzerantwort

Nach jeder bearbeiteten Phase muss der Agent **im Research-Artefakt** festhalten:

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

Dieser Block ist kein verpflichtendes Format für die sichtbare Nutzerantwort und
wird dort nicht ungefragt wiedergegeben. Gegenüber dem Nutzer fasst der Agent
stattdessen knapp und allgemeinverständlich zusammen:

1. Was kam heraus?
2. Was bedeutet das für die Idee oder Untersuchung?
3. Muss der Nutzer etwas entscheiden? Wenn ja: welche Möglichkeiten gibt es,
   welche praktischen Folgen haben sie und was empfiehlt der Agent?
4. Was ist der nächste sachliche Schritt?

Technische Details, interne Feldnamen und Statuscodes werden nur auf ausdrückliche
Nachfrage oder bei entscheidungsrelevanter Auswirkung ergänzt.

---

## 16. Versionierung

Jede Research-Datei benötigt mindestens:

- Research-ID,
- Version,
- Status,
- Erstellungsdatum,
- Freeze-Datum,
- Datenrollen,
- Strukturmodell-/Identifikationsdesign-Version,
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
- Surprise-Faktoren, Response-Modell oder Constraint-Assessment,
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

0. Ein optionaler Generation-Run endet bei `INBOX`; er darf weder Screening noch Promotion vorwegnehmen. Nutzt er ein LLM oder einen Agenten, erhält auch dieser Aufruf ein Run-Manifest.
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

`VALIDATED_PHENOMENON` bestätigt nur das eingefrorene Phänomen gemäß seinem
Design. Der Status erhöht weder den Claim-Level noch setzt er
`mechanism_supported` oder `executable_net_edge` automatisch auf `SUPPORTED`.

Fehlende Daten, nicht geprüfte Abhängigkeiten, ein verbrauchtes Validation-Set oder eine ungeprüfte entscheidungstragende akademische Quellenfassung sind keine redaktionellen Kleinigkeiten, sondern Zustandsfehler des Research-Prozesses.
