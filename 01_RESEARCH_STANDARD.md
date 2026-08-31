# 01_RESEARCH_STANDARD.md

**Version:** 2.0
**Stand:** 2026-08-31
**Status:** ENTWURF ZUR ÜBERNAHME  
**Zweck:** Normativer Standard für die Entwicklung, Falsifikation, Validierung und Überwachung von Trading-Phänomenen, Edge-Hypothesen und Strategien.

---

# 1. Forschungsziel

Strategy Research soll nicht rückblickend Regeln finden, die eine schöne Equity Curve erzeugen.

Es soll feststellen:

1. ob ein reproduzierbares Marktphänomen existiert,
2. ob dieses Phänomen gegenüber einem expliziten Nullmodell zusätzliche Information liefert,
3. wie groß der Effekt ist,
4. wie unsicher diese Schätzung ist,
5. wie viel tatsächlich unabhängige Evidenz vorhanden ist,
6. unter welchen vorab beobachtbaren Marktstates der Effekt stärker, schwächer, irrelevant oder invertiert ist,
7. ob der Effekt auf wirklich neuen Daten bestehen bleibt,
8. ob er nach Kosten und realer Execution wirtschaftlich nutzbar ist,
9. und ob die daraus gebaute Strategie im Forward-Betrieb stabil bleibt.

Die zentrale Haltung lautet:

> Wir formulieren überprüfbare Vorhersagebehauptungen über bedingte Marktverteilungen und versuchen, sie zu widerlegen. Erst überlebende Behauptungen dürfen in Strategien übersetzt werden.

Die logische Strategiearchitektur bleibt:

`Marktmodell → Edge-Hypothese → Strategie → Setup → Trigger → Trade-Plan → Ausführung/Management → Evaluation`

Der empirische Research-Prozess darf bottom-up beginnen:

`Beobachtung → Beschreibung → Messung → Candidate Hypothesis → Freeze → neue Daten → Evaluation → Entscheidung`

Entdeckung und Bestätigung sind strikt zu trennen.

Zusätzlich sind **Vorhersage und Kausalität** strikt zu trennen. Eine robuste prädiktive Edge kann wirtschaftlich nützlich sein, ohne dass ihr Mechanismus kausal identifiziert ist. Umgekehrt garantiert ein identifizierter kausaler Effekt keine handelbare Vorhersage nach Kosten.

## 1.1 Geltung, Statusrouter und Prüfbarkeit

Vor `PROMOTED` gilt nur der gestaffelte Intake aus `QUICKSTART.md` und
`schemas/hypothesis_candidate.schema.json`. Ein `INBOX`- oder `REJECTED`-Eintrag
ist kein Research Case und muss den Vollstandard nicht laden oder ausfüllen.

Ab `PROMOTED` gelten die Kernregeln dieses Standards vollständig. Methoden- und
Toolingdetails werden jedoch nur für den aktivierten Claim und die ausgewählte
Methode geladen. Nicht ausgewählte optionale Verfahren benötigen keine
N/A-Serien.

Ein vom ausführenden Agenten gesetzter Phasen- oder Gate-Status ist eine
Selbstdeklaration. Maschinenprüfbar wird er nur durch das benannte Schema, den
zugehörigen Run-/Evidence-Verweis und gegebenenfalls ein unabhängiges Review.
Normative Sprache ersetzt diese Nachweise nicht.

---

# 2. Datenrollen und Informationsbudget

Jeder Datensatz erhält genau eine aktuelle Rolle:

- `DISCOVERY`
- `DEVELOPMENT`
- `VALIDATION`
- `FINAL_HOLDOUT`
- `FORWARD_OOS`

Sobald ein Ergebnis eine Designentscheidung beeinflusst, ist der betreffende Datensatz Development Data.

Ein Datensatz kann durch Nutzung seinen unabhängigen Informationswert verlieren. Forschung besitzt damit ein **Informationsbudget**. Holdout-Daten sind eine knappe Ressource und werden nicht verbraucht, bevor das Projekt statistisch und wirtschaftlich testbar ist.

---

# 3. Phase 0 – Machbarkeit und Informationsbudget

## 3.0 Eingangsschwelle vor Phase 0

Eine beobachtungsgetriebene Idee darf Phase 0 erst nach einem frühen
Surrogat-Screen betreten. Vor dem ersten Screen werden vollständiges
Kandidatenuniversum, geplante Testzahl, Familien-Alpha und Korrekturmethode in
`schemas/search_space.schema.json` fixiert. Alle erzeugten Kandidaten zählen zum
Suchraum, sobald sie datenbasiert geprüft werden; nur Überlebende zu zählen ist
unzulässig. Jeder untersuchte Rausch-Kandidat vergrößert diesen Suchraum und
hebt damit die Nachweisschwelle für spätere echte Befunde. Bei mehr als einem
geplanten Screen ist eine
Multiplizitätskorrektur zwingend. `NONE_JUSTIFIED` ist ausschließlich für eine
Ein-Test-Familie zulässig und kein Waiver für einen größeren Suchraum.

Der Screen verwendet `DISCOVERY`- oder `SYNTHETIC`-Daten und erhält relevante
Abhängigkeiten wie Sessionprofil, Autokorrelation oder Volatilitätscluster.
Naive Permutation, die diese Struktur zerstört, ist unzulässig. Die Nullperiode
muss zeitlich und marktstrukturell vergleichbar sein, weil auch sie driftet.
`PASS` bedeutet nur, dass Phase-0-Aufwand gerechtfertigt ist. Es bestätigt weder
Effekt, Mechanismus, OOS-Prognose noch Edge. Theorie-, terminierte Event- und
publizierte Replikationsideen dürfen einen begründeten Waiver verwenden.

## 3.1 Zweck

Phase 0 verhindert, dass wertvolle unabhängige Daten für eine Hypothese verbraucht werden, die mit den verfügbaren Daten oder unter realistischen Kosten gar nicht sinnvoll entscheidbar ist.

Die Phase beginnt, sobald eine grobe Phänomendefinition und Outcome-Skala vorliegen, und wird in zwei Stufen durchgeführt:

1. **Vorprüfung:** konservatives Screening vor umfangreicher Discovery-/Development-Arbeit. Ein `WEITER` öffnet nur Discovery und Development.
2. **Formale Re-Kalkulation:** nach vollständiger Operationalisierung von Outcome, Nullmodell, Abhängigkeit, effektivem N und Validation-Plan, aber vor Pipeline-Integritätsgate und Freeze.

Unabhängige Validation darf erst nach `PASS` der formalen Re-Kalkulation beginnen.

## 3.2 Wirtschaftliche Schwelle

Es wird eine **minimale wirtschaftlich relevante Effektgröße** definiert.

Sie muss in derselben Einheit wie der primäre Outcome formuliert werden.

Bei einem Brutto-Outcome kann konzeptionell gelten:

\[
\delta_{econ} = \text{erwartete Round-Trip-Kosten} + \text{notwendige Sicherheitsmarge}
\]

Bei bereits netto berechneten Outcomes wird die Schwelle entsprechend angepasst.

Die Sicherheitsmarge ist vorab zu begründen. Sie darf nicht nach dem Ergebnis so gesetzt werden, dass ein beobachteter Effekt gerade noch „wirtschaftlich relevant“ erscheint.

Die Sicherheitsmarge bezeichnet einen **zusätzlichen absoluten Betrag** zur Kostenschätzung. Wird mit einem Multiplikator gearbeitet, muss die Notation eindeutig sagen, ob die gesamte Schwelle oder nur die Marge multipliziert wird. Ein universeller Multiplikator für alle Strategien ist nicht zulässig; Unsicherheit von Kosten, Slippage und Capacity ist designspezifisch zu behandeln.

## 3.3 Vorläufiges Kostenmodell

Schon in Phase 0 werden konservative Größen für relevante Kostenkomponenten geschätzt:

- Gebühren,
- Spread,
- Slippage,
- Funding, falls relevant,
- erwartbare Fill-Nachteile.

Das Modell ist bewusst grob. Es soll nur beantworten, ob die gesuchte Effektgröße überhaupt wirtschaftlich interessant sein könnte.

## 3.4 Power / Entscheidbarkeit

Vor dem formalen Test werden festgelegt:

- primärer Test beziehungsweise primäre Schätzgröße,
- gewünschtes Fehlerniveau oder äquivalente Entscheidungsanforderung,
- Ziel-Power oder äquivalente Präzisionsanforderung,
- wirtschaftliche Relevanzgrenze `δ_econ`,
- angenommene wahre Planungswirkung `δ_plan` oder direktes Präzisionsziel,
- explizite Null- und Alternativhypothese beziehungsweise Intervall-Entscheidungsregel,
- angenommene Streuung,
- erwartete Abhängigkeitsstruktur,
- benötigtes N beziehungsweise benötigte unabhängige Information.

Die Mindeststichprobe stammt aus dieser Rechnung oder Simulation, **nicht** aus der Anzahl der bereits vorhandenen Fälle.

Für klassische formale Tests gelten mangels einer sachlich besseren, vorab begründeten Entscheidungsregel `α = 0,05` zweiseitig und `Power = 80 %` als Arbeitsdefaults. Bei knappem finalem Holdout oder hohen Kosten eines falsch-negativen Befunds sind `90 %` oder ein direktes Präzisionsziel zu prüfen. Eine einseitige Testung, geringere Power oder andere Fehlergewichtung ist nur mit vor Kenntnis des Ergebnisses dokumentierter Begründung zulässig. Diese Defaults ersetzen weder Loss-Funktion noch designspezifische Simulation.

Für die Streuung werden getrennt dokumentiert:

- explorativer Punktschätzer,
- Quelle, Stichprobengröße und Übertragbarkeit dieses Schätzers,
- Unsicherheitsbereich,
- konservativer Planungswert oder vorab definiertes Stressszenario.

Ein einzelner Schätzer aus einer kleinen, selektierten oder heavy-tailed Discovery-Stichprobe darf nicht ungeprüft als wahre Planungsstreuung eingesetzt werden. Je nach Design kommen externe oder gepoolte Referenzen, eine unter gültigen Modellannahmen berechnete obere Unsicherheitsgrenze, robuste Skalenmaße mit begründetem Stressaufschlag oder eine Szenariorechnung in Betracht. `WEITER` ist nur zulässig, wenn die Machbarkeit auch im konservativen Szenario besteht oder die zusätzlich benötigte Information ausdrücklich beschafft wird.

Die Stressregel wird vor der Berechnung festgelegt. Unter mehreren vorab zulässigen und sachlich übertragbaren Kandidaten verwendet das Gate den konservativsten Wert oder die vollständige Szenariobandbreite. Robuste Skalenmaße dürfen nur nach nachvollziehbarer Abbildung auf die Stichprobenverteilung des primären Schätzers verwendet werden, bei Bedarf per designspezifischer Simulation.

`δ_econ` und `δ_plan` sind nicht austauschbar. Wenn Erfolg beispielsweise verlangt, dass die untere Intervallgrenze über `δ_econ` liegt, muss die Planung genau diese Entscheidungsregel abbilden; eine bloße Powerrechnung für `0` gegen `δ_econ` genügt dafür nicht.

Quelle und Begründung von `δ_plan` werden protokolliert. Ein Discovery-Punktschätzer darf nicht ungeprüft als `δ_plan` übernommen werden; Auswahlverzerrung und Unsicherheit sind durch konservative Szenarien, Shrinkage oder externe Referenzen zu berücksichtigen. `δ_plan` darf nach Kenntnis des Validation-Ergebnisses nicht geändert werden.

## 3.5 Verfügbares N und effektives N

Zu dokumentieren sind:

- nominelle Beobachtungszahl,
- Anzahl unabhängiger Tage/Sessions/Eventcluster,
- Symbolcluster,
- überlappende Label-/Holding-Perioden,
- geschätzte effektive Stichprobengröße oder eine konservative Bandbreite.

Für das Gate maßgeblich sind die konservative Untergrenze des effektiven N und die unabhängige Clusterzahl, nicht nur ein Punktschätzer. Die Berechnungsreihenfolge lautet:

`benötigte unabhängige Information → designspezifischer DE/Simulation → benötigtes nominelles N`, jeweils konservativ aufgerundet.

Im Stressszenario wird ein geschätzter Informationsgewinn `DE < 1` beziehungsweise `N_eff > N` nur angerechnet, wenn er durch externe, übertragbare Evidenz und ein vorab festgelegtes Modell belastbar gestützt ist; andernfalls gilt für die Planung mindestens `DE = 1`.

Bei weniger als 30 plausibel unabhängigen Clustern wird `SMALL_CLUSTER_WARNING` gesetzt. Diese Schwelle ist ein Diagnose- und Eskalationspunkt, kein universelles Bestehenskriterium. Der Warnstatus verlangt eine für wenige Cluster geeignete Inferenz, designspezifische Simulation/Kalibrierung oder `BLOCKED`. Er erlaubt nicht die pauschale Aussage, ein bestimmtes Intervall sei allein wegen der Clusterzahl zwingend zu schmal oder ungültig.

## 3.6 Phase-0-Entscheidung

Es gibt genau drei Hauptentscheidungen:

### `WEITER`

Die aktuell vorhandene unabhängige Information reicht im konservativen Szenario für den jeweils erreichten Gate-Zweck aus. In der Vorprüfung erlaubt `WEITER` nur Discovery/Development; erst die formale Re-Kalkulation kann den Weg zum Freeze öffnen.

### `DATEN BESCHAFFEN`

Die Hypothese ist grundsätzlich testbar, aber die aktuell verfügbare unabhängige Information reicht nicht. Nur künftig realistisch beschaffbare Information führt daher zu `DATEN BESCHAFFEN`, nicht zu `WEITER`.

### `ABBRECHEN / DERZEIT NICHT TESTBAR`

Die ökonomische Schwelle, die verfügbare Datenbasis oder die erwartbare Abhängigkeit machen einen aussagekräftigen Test mit vertretbarem Aufwand nicht möglich.

Ein `DATEN BESCHAFFEN` oder `ABBRECHEN` darf nicht durch das Herabsetzen der wirtschaftlichen Schwelle nach Kenntnis der Daten umgangen werden.

---

# 4. Discovery – beobachten, beschreiben, Fälle sammeln

Research darf mit Theorie oder Beobachtung beginnen.

Eine Theorie ist nicht erforderlich. Ein beobachtetes Muster genügt als Ausgangspunkt.

Die erste Frage lautet nicht:

> Wie trade ich das?

Sondern:

> Was beobachte ich genau?

In Discovery dürfen:

- Charts betrachtet,
- Fälle gesammelt,
- Variablen ausprobiert,
- Definitionen verändert,
- Beziehungen visualisiert,
- Gegenbeispiele gesucht

werden.

Discovery ist absichtlich flexibel. Die dafür verwendeten Daten sind danach jedoch keine unabhängige Bestätigung.

Der Fallkatalog muss nicht nur Gewinner oder „schöne“ Beispiele enthalten, sondern:

- klare Treffer,
- klare Fehlschläge,
- Grenzfälle,
- unterschiedliche Zeitperioden,
- verschiedene Volatilitätszustände,
- gegebenenfalls mehrere vergleichbare Instrumente.

## 4.0 Optionale vorgelagerte Ideenerzeugung

Fehlt eine Rohidee, darf vor dem Intake der Mechanismenkatalog-Producer aus
`generation/` ausgeführt werden. Er kombiniert einen Literatur- oder
Marktmechanismus mit einer Phase und einem beobachtbaren Abdruck. Zulässige
Erzeugungsrouten sind:

- `CONSTRAINT_FIRST`,
- `MICROSTRUCTURE_STATE`,
- `LINKAGE_OR_IDENTITY`,
- `LITERATURE_REPLICATION`,
- `OBSERVATION_DRIVEN`.

Die Operatoren `PHASE_PATH`, `EXPECTATION_VIOLATION`,
`MECHANISM_CONNECTION` und `ASSUMPTION_RELAXATION` erzeugen getrennte
Ideenfamilien. Insbesondere ist ein ausbleibender oder invertierter erwarteter
Abdruck keine nachträgliche Rettung der ursprünglichen Idee, sondern ein neuer
`INBOX`-Candidate mit eigener ID.

Ideenerzeugung ist kein Gate. Sie benötigt weder einen universell benannten
gezwungenen Akteur noch Premortem, Validity-Selbsteinstufung, Backtest,
Confidence, Evidence Grade oder Promotionsentscheidung. Ihr Endzustand ist
ausschließlich ein ungescreenter Intake.

Jeder Katalogeintrag führt mit `entry_origin` seinen Entstehungsweg. Eigene
wiederholte Beobachtungen können über stabile Journalreferenzen als
`INTERNAL_OBSERVATION` neue Mechanismen einspeisen; sie erhalten dadurch keine
höhere Evidenzstufe. Der Generation-Run bleibt als vollständige
Kandidatenuniversums-Referenz erhalten.

## 4.1 Vorgelagerter Hypothesen-Intake

Eine Rohidee ist weder Evidenz noch eine `Candidate Hypothesis`. Sie wird vor der
Phase-0-Vorprüfung als versionierter Intake-Datensatz erfasst und darf erst nach
einem dokumentierten Screening in ein Research Case übergehen.

Für `INBOX` werden nur stabile Identität, Zeit, Ursprung, Rohidee, bereits
verbrauchte Informationsreferenzen und der Status gespeichert. `LLM_IDEA` und
Sekundärquellen sind Ideengeber, keine Evidenz. `MERGED` und `REJECTED` ergänzen
nur die jeweilige Transition und Begründung.

`SCREENED` ergänzt Ideenklasse, Mechanismenfamilie und Alternativerklärungen.
Erst `PROMOTED` protokolliert zusätzlich mindestens:

- Ideenklasse
  (`ASSOCIATIONAL_PATTERN / PREDICTIVE_PRECEDENCE / MECHANISM_CANDIDATE /
  STRUCTURAL_FLOW_CANDIDATE / RELATIVE_VALUE_CANDIDATE /
  EVENT_RESPONSE_CANDIDATE / RETURN_DECOMPOSITION_CANDIDATE / OTHER`),
- Markt, Instrument, Venue, Handelsphase, Zeitzone/Kalender und Prognosehorizont,
- einen benannten Akteur, Zwang, erwartete Handlung, beobachtbaren Bezug und
  mindestens eine konkurrierende Akteurshypothese,
- einen verknüpften Noise Screen oder begründeten zulässigen Waiver,
- den beobachtbaren Footprint, der die Geschichte von bloßer Prosa unterscheidbar
  machen soll,
- mindestens eine konkurrierende Erklärung,
- benötigte Daten, Auflösung, Timestamp-/Clock-Sync-, Venue- und Feed-Coverage,
- frühe Hürden durch Spread, Gebühren, Slippage, Latenz, Queue-Position, Borrow,
  Funding oder Leg-Risk, soweit anwendbar,
- die detaillierte Einordnung bereits betrachteter Daten und ihres
  Informationsbudgets,
- den Modus und die Provenienz der Variablen- und Konstruktauswahl,
- die Promotion-Entscheidung und nächste Research-ID.

Typische Intraday-Kandidaten für den Akteurszwang sind Market Maker unter
Inventarrisiko, Options-Desks beim Hedging, zeitgebundene
Ausführungsalgorithmen, Rebalancing- und Margin-Prozesse sowie Stop-Cluster an
technischen Marken. Die Nennung bleibt eine Plausibilitätsprüfung und ist kein
Mechanismusnachweis.

`PROMOTED` bedeutet ausschließlich, dass eine Idee präzise und grundsätzlich
testbar genug für Phase 0 ist. Es bestätigt weder den Mechanismus noch eine
Prognose oder Trading-Edge. Ablehnung und Merge bleiben mit Begründung erhalten;
eine verworfene Idee wird nicht gelöscht und später als neue unabhängige Idee
wiedereingeführt.

## 4.1a Variablenauswahl-Provenienz

Jeder `PROMOTED`-Datensatz deklariert den Auswahlmodus als `PREDEFINED`,
`DATA_DRIVEN` oder `HYBRID`.

- `PREDEFINED` benötigt eine knappe fachliche Begründung und die Referenzen der
  beibehaltenen Variablen oder Konstrukte. Es wird kein künstlicher Suchraum
  erfunden.
- `DATA_DRIVEN` und `HYBRID` benötigen zusätzlich das eingefrorene
  Kandidatenuniversum, alle Selektionsdaten und deren Datenrolle, die
  Sichtbarkeit des Outcomes während der Auswahl, Methodenreferenzen, die
  effektive Kandidatenzahl, einen versionierten Suchraum und konkrete Kontrollen
  gegen Auswahlbias.

Alle Selektionsdaten erscheinen auch in `consumed_data_refs`. Ein Dataset, das
Variablenwahl oder Suchraum beeinflusst hat, ist keine unabhängige Validation und
kein Holdout mehr. Feature Importance, SHAP-/Shapley-, Impurity- oder vergleichbare
Verfahren sind optionale Modell- oder Assoziationsdiagnosen. Sie sind weder
Pflicht noch Beleg für kausale Relevanz.

## 4.1b Rekonstruktion einer Strategie aus Prosa

Stammt eine Idee aus einem Buch, Artikel, Video oder Kurs und fehlen dort
reproduzierbare Definitionen, wird Quelleninterpretation nicht unmittelbar als
fertige Strategie ausgegeben. Vor einer eigenen Spezifikation darf ein
`strategy_reconstruction` nach
`schemas/strategy_reconstruction.schema.json` angelegt werden.

Das Artefakt trennt:

- den tatsächlich geprüften Quellenausschnitt,
- Regel, Empfehlung, Option, Beispiel und ausdrückliche Discretion,
- die für die Strategieidentität unverzichtbaren Quellenbehauptungen,
- quellenfestgelegte, alternative, offene, diskretionäre und
  widersprüchliche Konstrukte,
- mögliche Definitionen und deren wirkliche Herkunft,
- die spätere bewusste Auswahl oder ein Human-Protocol.

Ein Beispiel wird nicht automatisch zur allgemeinen Regel. Eine Liste
möglicher Operationalisierungen ist weder eine Auswahl noch ein Backtest oder
automatisch ein tatsächlich untersuchter Suchraum. Wird Discretion entfernt,
kann das Ergebnis eine `SIMPLIFIED_VARIANT`, aber keine stillschweigende
Replikation sein. `REPLICATION` ist nur zulässig, wenn die Quelle alle
wesentlichen Konstrukte reproduzierbar festlegt. Details und Beispiel stehen in
`reconstruction/README.md`.

## 4.2 Verbindlicher Research Scope

Vor `PROMOTED` wird der Scope so eng angegeben, dass unterschiedliche Designs
nicht unter demselben Etikett vermischt werden. Für `INBOX` genügt die Rohidee;
der vollständige Scope ist Promotionsvoraussetzung. Mindestens festzulegen sind
Markt/Instrument, Venue und Datenfeed, Handelsphase
(`PRE_MARKET / OPENING_AUCTION / CONTINUOUS / CLOSING_AUCTION / POST_MARKET /
OVERNIGHT / CROSS_SESSION / OTHER`),
Kalender/Zeitzone/DST-Regel, Clock- oder Event-Time-Horizont und eine der folgenden
Ereignisklassen:

- `INFORMATION_EVENT`,
- `SCHEDULED_STRUCTURAL_EVENT`,
- `CONTINUOUS_ENDOGENOUS_MECHANISM`,
- `RETURN_DECOMPOSITION`.

Diese Klassen sind ein Designrouter, keine abschließende Taxonomie von
Marktmechanismen.

Die News-/Makro-Policy lautet genau eine der folgenden:

- `INCLUDED_AS_SIGNAL`,
- `NOT_USED_AS_SIGNAL`,
- `FILTER_KNOWN_EVENTS`,
- `SCHEDULED_EVENT_STUDY`.

`NOT_USED_AS_SIGNAL` bedeutet nicht, dass Informationsereignisse aus der Stichprobe
entfernt wurden. `FILTER_KNOWN_EVENTS` benötigt benannte Feeds, Abdeckung,
Zeitstempel, Ausschlussfenster und bekannte Coverage-Lücken. Deshalb ist die
unqualifizierte Behauptung „newsfrei“ unzulässig; zulässig ist nur eine Aussage
über nach dokumentierter Policy und Feed-Abdeckung bekannte Ereignisse.

PEAD, CPI-, FOMC- oder vergleichbare Release-Studien gehören zu
`INFORMATION_EVENT` und dürfen nicht als Beleg für einen strikt gefilterten,
kontinuierlichen Intraday-Mechanismus ausgegeben werden. Indexumstellungen,
Funding-Timestamps und Auktionen sind geplante Strukturereignisse und werden nicht
mit kontinuierlicher Orderbuchmechanik zusammengelegt. Close-to-open- gegenüber
Open-to-close-Renditen sind zunächst `RETURN_DECOMPOSITION`, keine eigenständige
newsfreie Handelsregel.

## 4.3 Drei getrennte Evidenzstufen

Für jede auf einem vermuteten Mechanismus beruhende Idee werden drei Status getrennt
geführt:

1. `mechanism_supported` – der Mechanismus ist für den behaupteten Markt, Akteur
   und Zeitraum ausreichend belegt;
2. `forward_predictive_oos` – der zum Entscheidungszeitpunkt beobachtbare Footprint
   prognostiziert das vorab definierte zukünftige Outcome auf unabhängigen Daten;
3. `executable_net_edge` – die Prognose bleibt zu ausführbaren Preisen nach allen
   relevanten Kosten, Latenz-, Fill-, Queue-, Borrow-, Funding- und Capacity-Effekten
   wirtschaftlich positiv.

Jeder Status lautet unabhängig `UNKNOWN`, `SUPPORTED`, `NOT_SUPPORTED` oder
`BLOCKED`. Es gibt keine automatische Hochstufung: Eine Theorie oder ein Paper zum
Mechanismus setzt die beiden späteren Stufen nicht auf `SUPPORTED`; eine
kontemporäre Beziehung ist keine Forward-Prognose; und ein Midprice-Effekt ist
keine ausführbare Netto-Edge.

## 4.4 Zwei unabhängige Achsen

| Achse | Zulässige Werte | Beantwortete Frage |
|---|---|---|
| Research-Claim-Level | `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL` | Welche Art von Verteilung, Intervention oder Kontrafaktum wird behauptet? |
| Validierungs-/Handelsstatus | `mechanism_supported / forward_predictive_oos / executable_net_edge`, jeweils mit eigenem Status | Welche Mechanismus-, Prognose- und ökonomische Evidenz liegt vor? |

Zwischen den Achsen gibt es keine automatische Inferenz. Ein interventionaler
Effekt mit bestandenem Identifikationsgate kann nach Kosten
`executable_net_edge = NOT_SUPPORTED` sein. Eine assoziative, zeitlich saubere
Prognose kann dagegen eine ausführbare Netto-Edge besitzen, ohne einen kausalen
Mechanismus zu identifizieren.

---

# 5. Claim-Level, Identifikationsmodell und Beobachtbarkeit

## 5.1 Claim-Level

Jede Research-Version deklariert die stärkste beabsichtigte Aussage:

- `ASSOCIATIONAL_PREDICTIVE`: Aussage über beobachtete oder prognostizierte Verteilungen, zum Beispiel `P(Y|X,C)`.
- `INTERVENTIONAL`: Aussage über die Wirkung eines Eingriffs oder strukturell identifizierten Schocks, zum Beispiel `E[Y|do(X=x)]`.
- `COUNTERFACTUAL`: Aussage darüber, was im selben konkreten Fall unter einer anderen Intervention geschehen wäre.

Ohne explizite Deklaration gilt `ASSOCIATIONAL_PREDICTIVE`. Eine prädiktive Edge wird nicht abgewertet, nur weil sie keinen identifizierten Mechanismus besitzt; ihre Beschreibung muss dann aber prädiktiv bleiben.

Der Claim-Level klassifiziert die Frage, nicht die verwendete Notation. Weder ein
DAG noch Potential-Outcome-Symbole noch ein bestimmter Schätzer erhöhen den
Claim-Level ohne bestandenes Identifikationsgate.

## 5.2 Kausales Estimand

Für `INTERVENTIONAL` oder `COUNTERFACTUAL` wird vor der Schätzung ein präzises Estimand festgelegt. Es benennt mindestens:

- Treatment, Intervention oder strukturellen Schock,
- Outcome und Horizont,
- Zielpopulation beziehungsweise Eventklasse,
- Kontrast und Einheit,
- totalen, direkten oder vermittelten Effekt,
- sowie die zeitliche Reihenfolge.

Das Wort „Effekt“ allein ist kein Estimand. Der `do(·)`-Operator darf nicht für eine gewöhnliche bedingte Prognose verwendet werden.

Das Identifikationsmodell wird als `SCM_DAG`, `POTENTIAL_OUTCOMES`,
`STRUCTURAL_ECONOMETRIC` oder `OTHER_EXPLICIT` deklariert. Die Darstellungen sind
für viele Fragen ineinander übersetzbar, müssen aber nicht gemeinsam verwendet
werden. Ein Potential-Outcomes-Design macht insbesondere Konsistenz, Positivity,
die designspezifische Assignment-/Exchangeability-Annahme und Interferenz oder
ein Exposure Mapping explizit. Ein zusätzlicher DAG ist nicht Pflicht, wenn das
gewählte Design Estimand und Identifikationsannahmen vollständig offenlegt.

## 5.3 Zweck und Grenzen des DAG

Ein gerichteter azyklischer Graph kann verwendet werden, um vermutete zeitliche und strukturelle Beziehungen zwischen Variablen explizit zu machen. Er ist ein zulässiger Formalismus, aber nicht für jedes identifizierte Design Pflicht.

Beispiel:

`Informationsstand(t−) → Schockerwartung(t−) → Event-Schock(t) → 2Y-Reaktion(t+) → Equity-Reaktion(t+)`

Der DAG ist kein Kausalitätsbeweis. Jeder Pfeil und jedes ausgelassene gemeinsame Elternteil sind Annahmen. Wo die Daten mehrere Strukturen nicht unterscheiden, werden konkurrierende DAGs oder eine Äquivalenzklasse dokumentiert. Zeitliche Reihenfolge schließt Rückwirkung auf die Vergangenheit aus, beseitigt aber weder latente Confounder noch Messfehler, Selektion oder Gleichzeitigkeit innerhalb der gewählten Zeitauflösung.

Der DAG dient insbesondere dazu:

- Confounder, Collider, Mediatoren und post-treatment Variablen auseinanderzuhalten,
- unzulässige Adjustierungen sichtbar zu machen,
- konkurrierende Erklärungen zu formulieren,
- testbare Implikationen und Negativkontrollen abzuleiten,
- und zu prüfen, ob das gewünschte Estimand überhaupt identifizierbar ist.

## 5.4 Identifikationsgate

Für `INTERVENTIONAL` oder `COUNTERFACTUAL` sind mindestens zu dokumentieren:

- Identifikationsstrategie, beispielsweise Randomisierung, natürliche Variation, Backdoor-/Frontdoor-Kriterium, Instrumentvariable, Regression Discontinuity, Difference-in-Differences oder begründete High-Frequency-Identifikation,
- nicht testbare und testbare Annahmen der Strategie,
- Auswahl des Adjustmentsatzes oder der vergleichbaren Designrestriktionen aus dem Identifikationsmodell statt aus rein prädiktiver Feature-Selektion,
- Positivity/Overlap beziehungsweise Instrumentrelevanz, soweit einschlägig,
- mögliche latente Confounder, Selektion, Messfehler und Interferenz,
- Negativkontrollen, Placebos und Sensitivitätsanalysen, soweit designspezifisch möglich,
- sowie das Ergebnis `PASS / FAIL / BLOCKED`.

Für `ASSOCIATIONAL_PREDICTIVE` lautet der Status `NOT_REQUIRED_PREDICTIVE`. Das ist kein Identifikationsnachweis.

Ohne `PASS` darf kein kausaler Claim eingefroren werden. Eine Fortsetzung als prädiktives Research benötigt eine entsprechend deklarierte neue Research-Version; die bereits angesehenen Daten behalten ihre verbrauchte Rolle.

## 5.5 Causal Discovery und Zeitreihen

Conditional-Independence-, Score-, Invarianz- und Zeitreihenverfahren dürfen DAG-Kandidaten einschränken oder Hypothesen erzeugen. Ihre Ausgabe wird nur unter den dokumentierten Algorithmusannahmen interpretiert, beispielsweise:

- kausale Markov- und Faithfulness-Annahmen,
- kausale Suffizienz oder expliziter Umgang mit latenten Variablen,
- Stationarität beziehungsweise definierte Umgebungen,
- korrekte Lag-Länge und Zeitauflösung,
- geeignete funktionale Form und Messqualität,
- gültige Conditional-Independence-Tests unter Autokorrelation.

Aus bedingten Unabhängigkeiten folgt häufig nur eine Markov-Äquivalenzklasse. Stärkere Orientierung erfordert zusätzliche strukturelle Annahmen oder Interventionen.

Granger-Tests beantworten, ob die Vergangenheit von `X` die Prognose von `Y` relativ zu einem gewählten Informationssatz verbessert. Sie liefern ohne zusätzliche Identifikationsannahmen keinen Pearl-interventionalen Effekt und werden als `PREDICTIVE_PRECEDENCE` gekennzeichnet.

## 5.6 Rolle des LLM

Ein LLM darf:

- alternative DAGs und Mechanismen formulieren,
- Confounder-, Instrument- und Negativkontroll-Kandidaten vorschlagen,
- Annahmen in prüfbare Konsequenzen übersetzen,
- und Widersprüche zwischen Hypothese, Datenzeitpunkt und Estimand markieren.

Es darf nicht:

- einen plausibel klingenden Pfeil als empirisch bewiesen behandeln,
- aus Literaturtext oder Korrelation eigenmächtig Instrumentvalidität ableiten,
- eine Causal-Discovery-Ausgabe in einen eindeutigen „wahren DAG“ umetikettieren,
- oder eine Schätzmethode mit einer Identifikationsstrategie verwechseln.

## 5.7 Beobachtbarkeitstabelle

Für jede Variable ist zwingend festzuhalten:

- Name,
- Berechnung,
- benötigte Rohdaten und Daten-Vintage,
- frühester Zeitpunkt vollständiger Verfügbarkeit,
- Verwendung als Prädiktor/State/Treatment/Schock/Mediator/Outcome,
- Leakage-/Look-ahead-Risiko.

Ein Signal darf im formalen Test nur als Prädiktor verwendet werden, wenn es zum Entscheidungszeitpunkt vollständig bekannt war. Confounder müssen vor dem Treatment beziehungsweise Schock bestimmt sein; post-treatment Variablen dürfen nicht versehentlich als gewöhnliche Controls in einen Total-Effekt eingehen.

Zurückgezeichnete Pivots, nachträglich bestätigte Extrempunkte, revidierte Makrodaten oder nach Sessionende berechnete Profilgrößen dürfen nicht rückwirkend so behandelt werden, als seien sie früher bekannt gewesen.

## 5.8 DAG- und Identifikationsversionierung

Sobald ein DAG, Claim-Level, Estimand oder eine Identifikationsannahme eine Designentscheidung beeinflusst, wird die betreffende Version protokolliert.

Materielle Änderungen nach Freeze erzeugen eine neue Research-Version.

## 5.9 Maschinenprüfbare Constraint- und Lever-Labels

Für Markttransmission werden direkt DAGs, Alternativerklärungen und quantitative
Response-Gleichungen verwendet; eine vorgelagerte ECE-Map ist kein Standardteil
des Pfads.

Wer eines der Labels `TRANSMISSION_DIAGNOSTIC`,
`INFORMATION_BOTTLENECK_CANDIDATE`, `IDENTIFIED_CAUSAL_LEVER` oder
`IMPLEMENTATION_CONSTRAINT` verwendet, erzeugt ein Artefakt nach
`schemas/constraint_assessment.schema.json`. Insbesondere gilt:

- `IDENTIFIED_CAUSAL_LEVER` benötigt `identification = PASS`, ein Estimand und tragende Evidenz.
- `IMPLEMENTATION_CONSTRAINT` benötigt ein validiertes Phänomen, bestandene Umsetzbarkeitsprüfung, ein definiertes Systemziel und eine messbare Engpassgröße.

Goldratts Fokuslogik darf nach Phänomen-Validation optional helfen, einen bereits
belegten Implementation-Engpass zu priorisieren. Sie ist keine Markt-, Schätz-
oder Identifikationsmethode.

## 5.10 Tooling-Router für kausale Analysen

Für jede Research-Version wird einer der folgenden Status gesetzt:

- `TOOLING_REQUIRED`: ausführbarer Code für Graphprüfung, Identifikation, kausale Schätzung, Refutation oder Causal Discovery ist Teil des Designs.
- `TOOLING_NOT_REQUIRED`: das Research enthält keine ausführbare kausale Kernoperation, etwa weil es rein assoziativ/prädiktiv bleibt; Begründung ist Pflicht.
- `TOOLING_BLOCKED`: eine notwendige Bibliothek, kompatible Laufzeit oder validierte API ist nicht verfügbar.

Bei `TOOLING_REQUIRED` wird nach `04_CAUSAL_TOOLING.md` eine primäre Bibliothek je Aufgabe gewählt. Spezialisierte Implementierungen sind der Default; selbst geschriebene kausale Kernalgorithmen sind nur zulässig, wenn keine geeignete Bibliothek existiert oder wenn sie ausschließlich als unabhängiger Test dienen. Der Grund und zusätzliche synthetische Tests werden dokumentiert.

Die Aufgaben bleiben getrennt:

- Graph- und Adjustierungsprüfung: primär `pgmpy` oder `DoWhy`,
- Model–Identify–Estimate–Refute-Workflow: primär `DoWhy`,
- DML/CATE nach Identifikation: `EconML` oder `DoubleML`, nicht automatisch beide,
- zeitserienspezifische Discovery: `Tigramite`,
- einfaches binäres Treatment mit Matching/Propensity: `causalinference` nur als enger optionaler Fall.

Eine Bibliothek darf mehrere Rollen übernehmen, aber kein API-Output ersetzt Domänenannahmen oder das Identifikationsgate. Ein Tool- oder Modellwechsel nach Freeze ist materiell. Vor Freeze werden Laufzeit, exakte Paketversionen, Lockfile/Environment, Hauptklassen oder -funktionen, Seed, Splitlogik, Strukturmodell-/Design-/Estimand-Version, Adjustmentsatz oder vergleichbare Designrestriktion, Warnungen und Kompatibilität protokolliert. Nicht getestete Paketkombinationen und Major-Version-Wechsel benötigen einen Smoke-Test auf einem bekannten synthetischen Fall.

---

# 6. Operationalisierung

Liegt eine nicht vollständig operationalisierte Quellenstrategie zugrunde,
wird vor dieser Phase die Quellenrekonstruktion aus §4.1b referenziert. Abschnitt
6 dokumentiert anschließend die tatsächlich gewählte Spezifikation; er darf
nicht rückwirkend verschleiern, welche Definition aus der Quelle stammt und
welche erst bei der Rekonstruktion ergänzt wurde.

Begriffe wie:

- Trend,
- Expansion,
- Überdehnung,
- Buildup,
- Rejection,
- starke Bewegung,
- hoher Druck,
- geringe Persistence

sind vor Validation zu operationalisieren.

Festgelegt werden mindestens:

- Variable,
- Formel/Berechnung,
- Lookback,
- Session,
- Timeframe,
- Beobachtungszeitpunkt,
- Outcome-Horizont.

Wo möglich, werden Variablen zunächst kontinuierlich untersucht.

Harte Schwellen werden erst später eingeführt, wenn sie durch die Form der Beziehung, praktische Umsetzbarkeit oder einen vorab begründeten Designzweck gerechtfertigt sind.

---

# 7. Zielvariable und Nullmodell

## 7.1 Zielvariable

In früher Forschung muss das Outcome nicht bereits vollständiges Trade-P&L sein.

Mögliche Outcomes:

- Forward Return,
- volatilitätsnormalisierter Forward Return,
- MFE,
- MAE,
- Zeit bis Ereignis,
- Wahrscheinlichkeit eines Reclaims,
- Wahrscheinlichkeit eines neuen Extremums,
- zukünftige Volatilität.

## 7.2 Nullmodell

Jede Hypothese benötigt einen expliziten Vergleich.

Mögliche Nullmodelle:

- unbedingter Forward Return,
- zeitlich gematchte Zufallszeitpunkte,
- volatilitätsgematchte Nicht-Events,
- randomisierte Signale bei gleicher Handelsfrequenz,
- identische Exitlogik mit randomisiertem Entry,
- einfacher Momentum-/Mean-Reversion-Benchmark,
- passende passive Marktdrift.

Die relevante Größe ist häufig eher:

\[
\Delta E = E[R\mid X] - E[R\mid Null]
\]

als nur `E[R|X]`.

## 7.3 Event-Schocks und Reaktionsinnovationen

Bei geplanten Veröffentlichungen reagiert der Markt typischerweise auf die neue Information relativ zum vorherigen Informationsstand, nicht auf den Rohwert allein. Deshalb werden mindestens getrennt gespeichert:

- veröffentlichter Wert einschließlich Daten-Vintage,
- vor dem Event verfügbare Markterwartung und deren Quelle/Zeitstempel,
- vorab definierte Surprise-Konstruktion und Skalierung,
- exakter Veröffentlichungszeitpunkt,
- vorab festgelegtes Reaktionsfenster,
- gleichzeitig oder überlappend veröffentlichte Nachrichten,
- Liquiditäts-, Volatilitäts- und Aufmerksamkeitsstate vor dem Event.

Eine typische deskriptive Schockvariable lautet:

\[
S_t = \frac{A_t-E_{t^-}[A_t]}{q},
\]

wobei `q` eine vorab auf Development-Daten oder aus externer Evidenz festgelegte Skala ist. Eine standardisierte Überraschung ist erst dann ein struktureller Schock, wenn die dafür notwendige Identifikationsstrategie bestanden ist.

Für Asset oder Kettenglied `j` wird die erwartete Reaktion ausschließlich aus vor dem jeweiligen Event zulässigen Daten geschätzt:

\[
u_{j,t}=R_{j,t}-\widehat m_j(S_t,C_t;\mathcal D_{<t}),
\qquad
z_{j,t}=\frac{u_{j,t}}{\widehat\sigma_{j,t}},
\]

mit ausschließlich vor dem Event bekannten Controls `C_t`. Modelltraining, Skalierung und Unsicherheitsprognose müssen zeitlich OOS sein. `u` beziehungsweise `z` heißen `REACTION_INNOVATION` oder `REACTION_ANOMALY`; sie sind weder automatisch Fehlbewertung noch `CAUSAL_CHAIN_BREAK`.

Bei einer Reaktionskette werden Schock und jedes Kettenglied separat gemessen. Eine gemeinsame „Chain Integrity“-Kennzahl benötigt vorab definierte Gewichte, Kovarianzbehandlung und Multiple-Testing-Regel. Post-event Mediatoren dürfen für die Prognose eines nachgelagerten Kettenglieds verwendet werden, aber nicht stillschweigend als Controls eines behaupteten Total-Effekts. Direkte und vermittelte Effekte erfordern ein eigenes Mediationsestimand und zusätzliche Identifikationsannahmen.

Bei Zentralbankevents ist insbesondere zu prüfen, ob eine beobachtete Überraschung reine Policy-News, Informationen über den wirtschaftlichen Ausblick, Risk-Premium-News oder mehrere Komponenten zugleich enthält. Ein enges Eventfenster reduziert Fremdnachrichten, garantiert aber keine Exogenität.

Ein einzelner Surprise-Wert ist nicht vorgeschrieben. Wenn die Veröffentlichung mehrere unabhängige Informationsdimensionen enthält, wird ein kleiner, ökonomisch interpretierbarer Faktorvektor `F_t` verwendet, beispielsweise Target-, Path- und Information-Komponente. Anzahl, Rotation, Vorzeichen, Orthogonalisierung und Interpretation der Faktoren werden auf Development-Daten festgelegt. Ein datengetrieben erzeugter Faktor ist nicht automatisch ein struktureller Schock.

## 7.4 Quantitative Shock-Response-Map

Die quantitative Standardlösung für eine vermutete Wirkungskette ist keine automatische Constraint-Suche, sondern eine Reihe messbarer Response-Gleichungen. Für Asset oder Kettenglied `j` und Horizont `h` kann als Ausgangspunkt gelten:

\[
R_{j,t,h}
=\alpha_{j,h}
+\beta_{j,h}^{\top}F_t
+\gamma_{j,h}^{\top}C_t
+\delta_{j,h}^{\top}(F_t\otimes C_t)
+\varepsilon_{j,t,h},
\]

wobei `F_t` die vorab definierten Surprise-Faktoren und `C_t` ausschließlich pre-event bekannte States enthält.

Methodischer Default:

1. Für unmittelbare Marktreaktionen eine einfache High-Frequency-Eventregression.
2. Für mehrere spätere Horizonte bei ausreichendem N separate horizon-spezifische Regressionen beziehungsweise Local Projections.
3. State-Abhängigkeit über wenige vorab begründete kontinuierliche Interaktionen.
4. Komplexere VAR-/SVAR-, Change-Point-, ML- oder gemeinsame Anomaliemodelle nur, wenn sie eine konkret benannte Frage beantworten und gegenüber dem einfachen Modell zusätzlichen OOS-Wert liefern.

Die vermutete verbale Kette muss nicht als streng sequenzielle Regression geschätzt werden. Bei nahezu gleichzeitiger Preisfindung werden die Assetreaktionen als gemeinsamer Response-Vektor auf `F_t` modelliert. Eine Reihenfolge zwischen Reaktionen wird nur behauptet, wenn Zeitauflösung und Identifikationsdesign sie tragen.

### Inkrementeller Test eines Kettenglieds

Soll Kettenglied `j` als Informationsengpass dienen, wird vor Freeze ein verschachtelter Vergleich festgelegt:

```text
M0: End-Outcome ~ Surprise-Faktoren + pre-event States
M1: End-Outcome ~ Surprise-Faktoren + pre-event States + rechtzeitig verfügbare Innovation von Glied j
```

Nur eine zeitlich OOS stabile Verbesserung einer vorab definierten Loss-, Kalibrierungs- oder Netto-Utility-Größe macht `j` zum `INFORMATION_BOTTLENECK_CANDIDATE`. Sie beweist keinen kausalen Hebel.

### Zulässige Labels

- `TRANSMISSION_DIAGNOSTIC`: Pass-through, Response-Koeffizient oder Residuum ohne Constraint-Claim.
- `INFORMATION_BOTTLENECK_CANDIDATE`: inkrementeller OOS-Prognosewert für das definierte End-Outcome.
- `IDENTIFIED_CAUSAL_LEVER`: interventionale Zielgröße identifiziert und E-Gate bestanden.
- `IMPLEMENTATION_CONSTRAINT`: begrenzt ausführbare Netto-Performance durch Daten, Latenz, Liquidität, Kosten oder Prozess.

Die Auswahl des „dominanten“ Glieds gehört zum Research-Suchraum. Werden mehrere Glieder, Horizonte oder States verglichen, gelten Multiple-Testing- und Datenverbrauchsregeln.

---

# 8. Effektgröße, Unsicherheit und Präzision

## 8.1 Effektgröße vor Signifikanz

Ein Effekt kann statistisch auffällig und wirtschaftlich irrelevant sein.

Berichtet werden deshalb mindestens:

- Punktschätzer,
- Vergleich zum Nullmodell,
- wirtschaftliche Relevanzschwelle,
- Unsicherheitsintervall,
- robuste Sensitivitätsschätzung.

## 8.2 Vier Ergebniszustände

Validation wird nicht nur als `signifikant / nicht signifikant` interpretiert.

### A. Erwarteter wirtschaftlich relevanter Effekt präzise gestützt

Der Effekt liegt mit der vorab definierten Unsicherheitslogik klar auf der erwarteten Seite der wirtschaftlichen Relevanzgrenze.

### B. Entgegengesetzter wirtschaftlich relevanter Effekt präzise gestützt

Die ursprüngliche Hypothese ist falsifiziert. Das Ergebnis darf eine **neue** Hypothese erzeugen, aber nicht die alte retten.

### C. Wirtschaftlich irrelevanter beziehungsweise Null-Effekt präzise gestützt

Die Daten schließen die vorab definierte wirtschaftlich relevante Effektgröße ausreichend aus. Die Hypothese wird verworfen oder beendet.

### D. Unpräzise / unentscheidbar

Die Unsicherheit umfasst mehrere wirtschaftlich unterschiedliche Zustände. Es darf keine ergebnisgetriebene Parameterrevision erfolgen.

Zulässig sind nur:

- mehr unabhängige Daten,
- bereits vorab definierte Zusatzanalyse,
- oder Abschluss als `INCONCLUSIVE`.

## 8.3 Testbündel, Fehlerzurechnung und Anschlussrevision

Ein Validation-Ergebnis prüft nie nur einen isolierten Satz. Es betrifft ein
Bündel aus Kernhypothese, Hilfsannahmen, Operationalisierung, Messverfahren,
Datenqualität, Scope, Modell, Inferenz und Implementierung. Ein negatives oder
unentscheidbares Ergebnis bestimmt daher ohne ein unterscheidendes Design nicht
eindeutig, welches Bündelglied falsch ist. Diese Duhem-Quine-Unterbestimmtheit
ändert den Ergebniszustand aus §8.2 nicht.

Nach `FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE` oder `INVALID_TEST` gilt bei
einer erwogenen materiellen Revision:

1. Das eingefrorene Ergebnis und seine Research-ID bleiben unverändert.
2. Der getestete Kern und die tatsächlich benötigten Hilfsannahmen werden in
   einem `scientific_philosophy_review` getrennt ausgewiesen.
3. Eine eindeutige Fehlerzurechnung ist nur mit Evidenz zulässig, die das
   verdächtige Bündelglied gegen die Alternativen unterscheidet.
4. Eine **progressive** Anschlussrevision erzeugt eine zuvor nicht implizierte,
   widerlegbare Vorhersage, benennt ihren Falsifikator, friert einen unabhängigen
   Evaluationsplan ein und erhält eine neue Research-ID.
5. Eine **degenerative** Revision erklärt hauptsächlich den bereits gesehenen
   Misserfolg weg, restauriert das gewünschte Vorzeichen oder verengt die
   Stichprobe nachträglich ohne neuen empirischen Gehalt. Sie autorisiert keinen
   neuen Bestätigungstest.
6. **Diagnostik** darf Mess-, Daten- oder Implementierungsprobleme lokalisieren.
   Sie ist weder Bestätigung noch Rettung der ursprünglichen Hypothese.

Im Sinne Lakatos' darf ein Forschungsprogramm trotz einer Anomalie vorläufig
beibehalten werden; das macht den fehlgeschlagenen Einzeltest nicht erfolgreich.
Im Sinne Kuhns werden isolierte, wiederkehrende und programmweite Anomalien sowie
verfügbare Rivalen protokolliert. Das Fehlen eines besseren Rivalen ist keine
positive Evidenz für die getestete Hypothese.

---

# 9. Abhängigkeit und effektive Stichprobengröße

Trading-Daten sind häufig nicht IID.

Zu prüfen sind:

- zeitliche Autokorrelation,
- wiederholte Signale desselben Marktimpulses,
- Event-/Sessioncluster,
- überlappende Forward-Horizonte,
- korrelierte Symbole,
- gemeinsame Makroereignisse.

Je nach Struktur kommen in Betracht:

- Block-Bootstrap,
- Cluster-Bootstrap,
- clusterrobuste Inferenz,
- Event-Clustering,
- Purging,
- Embargo,
- symbol- oder faktorbasierte Clusterung.

Der Grundsatz lautet:

> Das Unsicherheitsmodell muss zur tatsächlichen Abhängigkeitsstruktur der Daten passen.

Wenn dies mit den verfügbaren Informationen nicht möglich ist, darf die Analyse nicht mit einer falschen IID-Annahme „fertiggerechnet“ werden. Der Status lautet `BLOCKED` oder die Unsicherheit wird ausdrücklich konservativ behandelt.

Der Design Effect ist grundsätzlich definiert als:

\[
DE = \frac{Var(\hat\theta\mid tatsächliches\ Design)}{Var(\hat\theta\mid IID\text{-Referenz})}
\]

und kann näherungsweise zu `N_eff ≈ N / DE` übersetzt werden. Die bekannte Näherung `DE = 1 + (m−1)ρ` gilt nur für eine einfache austauschbare Clusterstruktur mit gleich großen Clustern. Bei ungleichen Clustergrößen, zeitlicher Abhängigkeit, mehreren Clusterebenen oder korrelierten Symbolen muss eine passende Erweiterung oder Simulation verwendet werden. Ein Default für `DE` ohne geschätzte Abhängigkeitsparameter ist unzulässig.

---

# 10. Einflussdiagnostik und Heavy Tails

## 10.1 Einflussdiagnostik

Vor Validation werden mindestens geplant:

- Leave-one-out oder Leave-one-cluster-out,
- Ergebnis ohne dominantes Symbol,
- Ergebnis ohne dominante Zeit-/Eventgruppe,
- Dominanzmaß der größten Beobachtung/des größten Clusters.

Die konkrete Dominanzschwelle wird im Freeze festgelegt.

Mindestregel:

> Kippt durch Entfernen eines einzelnen plausiblen Clusters das Vorzeichen oder die wirtschaftliche Schlussfolgerung, gilt die Evidenz nicht als robust bestätigt.

## 10.2 Heavy Tails

Bei schwerschwänzigen Outcomes werden vor Validation festgelegt:

- primärer Lageparameter,
- robuste Sensitivitätskennzahl,
- Umgang mit extremen Beobachtungen,
- Zulässigkeit von Trimming/Winsorisierung,
- primäre versus sekundäre Analyse.

Der Schätzer wird nicht nach dem Validation-Ergebnis ausgetauscht.

---

# 11. State- und Regimeforschung

Ein Regime ist kein metaphysischer Marktmodus, sondern ein beobachtbarer State, der die bedingte Verteilung eines konkreten Phänomens verändert.

Die zentrale Frage lautet:

> Welche vor dem Outcome beobachtbaren Marktvariablen verändern Effekt oder Risiko dieses Phänomens?

State-Variablen werden zunächst möglichst kontinuierlich untersucht.

Mindestens zu vergleichen sind, soweit sachlich passend:

\[
E[R\mid P]
\]

\[
E[R\mid S]
\]

\[
E[R\mid P,S]
\]

Damit wird geprüft, ob das Phänomen **zusätzliche** Information über den State hinaus liefert.

Gewinner und Verlierer werden gemeinsam analysiert. Winner-only-Regimeforschung ist unzulässig.

Übergangszustände wie `Balance → Expansion` oder `Trend → Balance` dürfen eigenständig untersucht werden. `Unklassifiziert` ist ein zulässiger Outcome eines State-Klassifikators.

Für Event-Reaktionen wird zusätzlich geprüft, ob sich Sensitivität, Varianz oder Vorzeichen mit einem **vor dem Event beobachtbaren** State verändern. Ein nach der Reaktion abgeleiteter „Regime“-Name ist kein zulässiger Conditioner. Unterschiedliche Reaktionen können unter anderem Aufmerksamkeit, Positionierung, Liquidität, Risikoprämien, konkurrierende Nachrichten oder echte Parameterdrift widerspiegeln; ein Mechanismuswechsel ist nur eine Gegenhypothese unter mehreren.

Invarianz über vorab definierte Umgebungen kann einen Kausalmechanismus stützen oder Kandidaten verwerfen. Sie ersetzt nur unter den jeweiligen Modellannahmen ein Identifikationsdesign und darf nicht als universeller Kausalitätstest verwendet werden.

---

# 12. Candidate Hypothesis, Vorhersage-Liste und Pre-Mortem

Nach Discovery und grundlegender Messung entsteht eine präzise Candidate Hypothesis.

Sie muss enthalten:

- Phänomen,
- Claim-Level `ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`,
- bei kausalem Claim: Estimand, Identifikationsstrategie und Identifikationsstatus,
- bei behaupteter Wirkungskette: Strukturmodell-/Identifikationsdesign-Version,
- bei Constraint-Sprache: definiertes Endziel, zulässiges Constraint-Label und Entscheidungskriterium,
- erwartete Richtung,
- primären Outcome,
- relevanten State, falls Teil der Hypothese,
- Nullmodell,
- wirtschaftliche Effektgrenze,
- Falsifikationsbedingung.

Danach folgen zwei adversariale Schritte.

## 12.1 Vorhersage-Liste

Frage:

> Welche zusätzlichen beobachtbaren Konsequenzen müssten eintreten, wenn die Hypothese stimmt?

Eine gute Hypothese muss mehr leisten als die Discovery-Daten nachzuerzählen.

## 12.2 Pre-Mortem

Annahme:

> Das Ergebnis sieht überzeugend aus, erweist sich später aber als falsch, instabil oder wirtschaftlich unbrauchbar. Warum?

Risiken werden übersetzt in:

- Checks,
- Gegenhypothesen,
- Guardrails,
- Ablehnungskriterien.

Mindestens zu prüfen sind:

- Leakage,
- Selection Bias,
- latente Confounder und unbeabsichtigte Collider-Konditionierung,
- post-treatment Controls beziehungsweise nicht identifizierte Mediation,
- kontaminierte Eventfenster oder falsche Erwartungs-Vintages,
- Vermischung mehrerer Nachrichtenschocks,
- Reaktionsänderung durch Aufmerksamkeit, Positionierung, Liquidität oder Parameterdrift,
- State erst nach Outcome definierbar,
- zu großer Research-Suchraum,
- Dominanz einzelner Instrumente/Ereignisse,
- zu wenig unabhängige Evidenz,
- unterschätzte Kosten,
- verspätete Live-Verfügbarkeit von Variablen.

---

# 13. Multiple Testing und Research Degrees of Freedom

Zum Suchraum gehören nicht nur Parameter, sondern jede Designentscheidung:

- Hypothesen,
- Indikatoren,
- Lookbacks,
- Timeframes,
- Sessions,
- Symbole,
- Long/Short,
- Outcomes,
- Exits,
- Statevariablen,
- Filter,
- Schwellenwerte.

Die Anzahl und Art der getesteten Varianten wird dokumentiert.

Generatorläufe gelten als Kandidatenuniversum. Werden alle 96 Kandidaten eines
Laufs gescreent, ist die vorab fixierte Familiengröße 96 und nicht die Zahl der
späteren Überlebenden. `scripts/validate_entry_thresholds.py` rechnet
Bonferroni-/Effective-Tests-Schwellen nach; Benjamini–Hochberg entscheidet erst
nach vollständigem Batch.

Je nach Umfang werden geeignete Verfahren gewählt, beispielsweise:

- False Discovery Rate,
- White's Reality Check,
- Hansen SPA,
- Deflated Sharpe Ratio,
- Probability of Backtest Overfitting,
- Bootstrap der gesamten Auswahlpipeline.

Je größer der Suchraum, desto strenger muss die Auswahlverzerrung berücksichtigt werden.

## 13.1 Pipeline-Integritätsprüfung vor dem Freeze

Die Unsicherheit einer Auswahlpipeline und die technische Integrität ihrer Implementierung sind getrennte Fragen. Vor dem Freeze muss die vollständige ausführbare Pipeline deshalb zusätzlich auf Kontroll-Daten geprüft werden.

Pflichtbestandteile:

- wiederholte Null-/Surrogatläufe mit soweit wie möglich erhaltener Zeit-, Cluster-, State- und Volatilitätsstruktur,
- identische Feature-, Auswahl-, Filter-, Timing- und Auswertungsschritte wie im echten Research,
- mindestens ein synthetischer bekannter positiver Effekt mit festem Vorzeichen und Timing als Sentinel gegen Vorzeichen-, Indexierungs- und Look-ahead-Fehler,
- bei `TOOLING_REQUIRED`: Import-/Versions- und API-Smoke-Test sowie ein synthetischer Kausaltest, der mindestens korrekte Richtung und zulässigen Adjustmentsatz prüft,
- vorab definierte Akzeptanzregeln für Fehlalarmrate, Effektverteilung, Richtung und Timing.

Zusätzlich werden Kontrollbasis und Datenrolle protokolliert. Pipeline-Tests, die Designentscheidungen beeinflussen, verwenden nur Development-Daten oder rein synthetische Daten. Für die geschätzte Fehlalarmrate werden geplante und tatsächliche Wiederholungszahl sowie Zielpräzision und Monte-Carlo-Unsicherheit dokumentiert. `PASS` setzt voraus, dass diese Zielpräzision erreicht wurde.

Ein einzelner permutierter Lauf oder ein einzelner Random Walk ist keine ausreichende Kalibrierung. Naive Permutation ist unzulässig, wenn sie die unter dem Nullmodell relevante Abhängigkeit zerstört. Das Pipeline-Integritätsgate lautet `PASS / FAIL / BLOCKED`; ohne `PASS` darf der Test Freeze nicht bestätigt werden.

---

# 14. Test Freeze

Vor formaler Validation werden mindestens eingefroren:

- Research-ID und Version,
- Candidate Hypothesis,
- Gegenhypothese,
- Claim-Level,
- kausales Estimand oder `N/A + Begründung: ASSOCIATIONAL_PREDICTIVE`,
- Identifikationsstrategie, Annahmen und Gate-Status oder `NOT_REQUIRED_PREDICTIVE`,
- Strukturmodell-/Identifikationsdesign-Version oder `N/A + Begründung: ASSOCIATIONAL_PREDICTIVE`,
- Tooling-Status, primäre Bibliothek je Aufgabe, exakte Laufzeit-/Paketversionen, Haupt-API und reproduzierbares Environment oder begründetes `TOOLING_NOT_REQUIRED`,
- Beobachtbarkeitstabelle,
- Markt/Instrument/Session/Timeframe,
- Datenrollen,
- Phänomendefinition,
- Statevariablen,
- Ausschlüsse,
- primärer Outcome,
- sekundäre Outcomes,
- Nullmodell,
- bei Event-Research: Erwartungsquelle/Vintage, Surprise-Formel, Skalierung, Eventfenster und Kontaminationsregel,
- bei mehrdimensionalen Events: Zahl, Konstruktion, Rotation/Orthogonalisierung und Interpretation der Surprise-Faktoren,
- bei Reaktionsinnovationen: erwartetes Reaktionsmodell, zeitliche Trainingsregel, Unsicherheitsskalierung und Benennung als nicht-kausales Residuum,
- bei Informationsengpass-Claim: End-Outcome, Verfügbarkeitszeitpunkt des Kettenglieds und eingefrorener `M0`-gegen-`M1`-OOS-Vergleich,
- erwartete Richtung,
- wirtschaftliche Effektgrenze,
- primärer Schätzer,
- robuste Sensitivitätsschätzung,
- Unsicherheitsmethode,
- Abhängigkeits-/Clusterlogik,
- effektive-N-Methode,
- Purging-/Embargo-Regel, falls nötig,
- Einflussdiagnostik,
- Heavy-Tail-Regel,
- Multiple-Testing-Methode,
- vollständiger Validation-Plan einschließlich Datensplit, Mindest-N und Entscheidungsregeln,
- bestandene formale Phase-0-Re-Kalkulation,
- Pipeline-Integritätsdesign und bestandenes Pipeline-Integritätsgate,
- bei `TOOLING_REQUIRED`: bestandener Import-/API-/Kompatibilitäts-Smoke-Test und synthetischer Kausal-Sentinel,
- Datensplit,
- Mindeststichprobe aus Phase 0,
- Erfolgskriterien,
- Ablehnungskriterien,
- Inconclusive-Regel,
- Warn-/Suspendierungskriterien für späteren Forward-Betrieb.

Das Freeze-Vollständigkeitsgate muss `PASS` sein, bevor Validation beginnt.

Gate- und Phasenstatus sind eindeutig gekoppelt: `PASS → COMPLETE`, `FAIL → FAILED`, `BLOCKED → BLOCKED`. Nach `FAIL` oder `BLOCKED` darf kein abhängiger Folgeschritt beginnen.

---

# 15. Validation und Final Holdout

## 15.1 Validation

Validation nutzt Daten, die die aktuelle Research-Version nicht beeinflusst haben.

Wird das Ergebnis zur Anpassung verwendet, ist der Datensatz verbraucht und ab dann Development Data.

## 15.2 Final Holdout

Wenn die Datenlage es zulässt, bleibt ein finaler Holdout vollständig unangetastet, bis:

- Discovery abgeschlossen,
- Development abgeschlossen,
- Candidate Hypothesis eingefroren,
- normale Validation abgeschlossen

ist.

## 15.3 Nested Walk-Forward

Wenn ein großer finaler Holdout nicht praktikabel ist, kann ein verschachteltes Walk-Forward-Design verwendet werden:

- inneres Fenster für Entwicklung/Modellwahl,
- äußeres Fenster für ungesehene Evaluation.

Bei überlappenden Labels sind Purging/Embargo entsprechend zu berücksichtigen.

## 15.4 Bedeutung von OOS-Evidenz für kausale Claims

OOS-Stabilität, Replikation und Backtest-Profitabilität testen Prognose- und Handlungsnutzen. Sie beweisen weder die Gültigkeit des DAG noch die Identifikation eines Interventionseffekts.

Bei einem kausalen Claim werden deshalb zusätzlich die eingefrorenen designspezifischen Identifikationsdiagnosen ausgewertet, beispielsweise:

- Overlap/Positivity und Covariate Balance,
- Pre-Trends und Placebos,
- Instrumentrelevanz sowie Plausibilität von Exclusion/Independence,
- Negativkontrollen,
- Sensitivität gegenüber unbeobachtetem Confounding,
- alternative zulässige DAGs beziehungsweise partielle Identifikationsgrenzen.

Double/debiased Machine Learning, flexible Outcome-Modelle oder Causal Forests ersetzen diese Voraussetzungen nicht. Sie schätzen Zielgrößen unter einer bereits begründeten Identifikationsstruktur.

---

# 16. Robustheit und Replikation

Ein Effekt wird nicht nur an seinem besten Punkt bewertet.

Zu prüfen sind:

- benachbarte Parameter,
- andere Zeitperioden,
- andere vergleichbare Instrumente,
- verschiedene Statebereiche,
- verschiedene Forward-Horizonte,
- Entfernung dominanter Cluster,
- Entfernung dominanter Symbole.

Gesucht wird ein stabiler Bereich, kein historischer Nadelstich.

Cross-Symbol-Tests werden nur dann als zusätzliche Evidenz gewertet, wenn die Abhängigkeitsstruktur dies zulässt. Stark korrelierte Märkte sind nicht automatisch unabhängige Replikationen.

---

# 17. Ökonomische Umsetzbarkeit und Strategy Engineering

Ein validiertes Phänomen ist noch keine Strategie.

`VALIDATED_PHENOMENON` ist ein zulässiger eigenständiger Endzustand. Der Status
bezeichnet ausschließlich ein gemäß eingefrorenem Design validiertes Phänomen.
Er bestätigt weder einen kausalen Mechanismus oder Claim-Level noch eine
ausführbare Netto-Edge. Strategy Engineering beginnt nur nach einer ausdrücklichen
Fortsetzungsentscheidung. Wird es nicht sofort fortgesetzt, bleiben die
nachgelagerten Engineering-, Aktivierungs- und Monitoring-Schritte als
`DEFERRED_AFTER_VALIDATION` geschlossen; das Phänomen verliert dadurch nicht
seinen validierten Status.

Nach Phänomen-Validation wird geprüft, ob es tatsächlich handelbar ist.

Zu entwickeln sind:

- Setup,
- Trigger,
- Invalidation,
- Entry,
- Stop,
- Target,
- Management,
- Position Size,
- Orderart,
- Execution-Modell.

## 17.1 Detailliertes Kostenmodell

Jetzt wird die frühe Phase-0-Kostenschätzung durch ein realistisches Modell ersetzt.

Kosten dürfen vom State abhängen:

\[
Kosten=f(State,Volatilität,Liquidität,Größe,Geschwindigkeit,Session,Execution)
\]

Besonders kritisch:

- Breakouts,
- News,
- Volatilitätsschocks,
- illiquide Zeitfenster,
- größere Positionsgrößen.

## 17.2 Entry und Exit getrennt diagnostizieren

Zu speichern sind, soweit möglich:

- MFE,
- MAE,
- Zeit bis MFE,
- Zeit bis MAE,
- Zeit bis Stop,
- Zeit bis Target,
- Exit-Grund.

Damit kann unterschieden werden zwischen:

- schwachem Signal,
- schlechtem Entry,
- falschem Stop,
- schlechtem Exit,
- Kostenproblem.

## 17.3 Prerequisite Tree / Transition Tree

Nach empirischer Validation können Prerequisite Tree und Transition Tree genutzt werden, um reale Umsetzungsprobleme und ihre Reihenfolge zu strukturieren.

Diese Werkzeuge erzeugen keine zusätzliche Edge-Evidenz.

---

# 18. Vollständige Strategie erneut Out-of-Sample testen

Die entwickelte Handelsstrategie muss nach Festlegung von Entry, Exit, Stop, Management und Execution erneut auf ungesehenen Daten beziehungsweise im kontrollierten Forward-Paper-Test bestehen.

Eine gute Phänomen-Validation schützt nicht vor Overfitting in der späteren Strategieumsetzung.

---

# 19. Forward-OOS, Monitoring und Degradation

Paper-/Live-Betrieb ist erneut Out-of-Sample.

Zu überwachen sind vier Degradationsarten:

## Statistisch

- Expectancy,
- Trefferquote,
- R-Verteilung,
- Drawdown,
- Streuung,
- Verlustcluster.

## Wirtschaftlich

- Gebühren,
- Spread,
- Slippage,
- Funding,
- Capacity/Liquidität.

## Statebezogen

- Häufigkeit des validierten States,
- Veränderung seiner Wirkung,
- Fehlklassifikation,
- State-Transitions.

## Mechanismus-/Eventbezogen, falls anwendbar

- Kalibrierung der erwarteten Reaktion,
- Verteilung und Autokorrelation der `REACTION_INNOVATION`,
- Häufigkeit vorab definierter Kettenabweichungen,
- Surprise-Verteilung und Qualität der Erwartungsquelle,
- Stabilität und Interpretierbarkeit eingefrorener Surprise-Faktoren,
- Eventfenster-Kontamination,
- Stabilität der vorab definierten Reaktionskoeffizienten und Unsicherheitsintervalle,
- fortbestehender inkrementeller OOS-Wert eines `INFORMATION_BOTTLENECK_CANDIDATE` gegenüber `M0`.

Eine Häufung großer Reaktionsinnovationen löst Diagnose oder Revalidierung aus. Sie wird nicht automatisch als neuer Marktmechanismus oder handelbarer Regimewechsel klassifiziert.

## Prozessual

- Erkennbarkeit,
- Trigger-Reproduzierbarkeit,
- Regelkonformität,
- Execution.

Warn-, Suspendierungs- und Verwerfungskriterien werden **vor Aktivierung** festgelegt.

---

# 20. Research-Endzustände

Ein Research-Projekt muss nicht in einer aktiven Strategie enden.

Zulässige Zustände:

- `NO_PHENOMENON`
- `INCONCLUSIVE`
- `CANDIDATE_HYPOTHESIS`
- `IN_TEST`
- `VALIDATED_PHENOMENON`
- `ECONOMICALLY_UNTRADEABLE`
- `ACTIVE_STRATEGY_CANDIDATE`
- `ACTIVE`
- `UNDER_OBSERVATION`
- `SUSPENDED`
- `REVALIDATED`
- `REJECTED`

Ein falsifiziertes Vorzeichen kann eine neue Hypothese erzeugen. Es wandelt den ursprünglichen Test nicht rückwirkend in einen Erfolg um.

---

# 21. Verbindliche Kernregeln

1. Phänomen vor fertiger Strategie.
2. Explizites Nullmodell vor Edge-Behauptung.
3. Phase-0-Machbarkeit vor Verbrauch unabhängiger Validation-Daten.
4. Mindeststichprobe aus Power-/Präzisionsrechnung, nie aus dem letzten Datenlauf.
5. Alle Prädiktoren müssen zum Entscheidungszeitpunkt vollständig beobachtbar sein.
6. Discovery-Daten bestätigen ihre eigene Hypothese nicht.
7. Jede Designentscheidung verbraucht Daten.
8. Anzahl Trades ist nicht automatisch Anzahl unabhängiger Beobachtungen.
9. Effektgröße und Unsicherheit sind gemeinsam zu berichten.
10. Präziser Null-Effekt und unpräzises Ergebnis sind unterschiedliche Befunde.
11. Unerwartetes Vorzeichen erzeugt höchstens eine neue Hypothese.
12. State-Variablen zunächst möglichst kontinuierlich untersuchen.
13. Gewinner und Verlierer gemeinsam analysieren.
14. Ein Regimefilter muss zusätzlichen Informationswert liefern.
15. Multiple Testing umfasst die gesamte Research-Pipeline.
16. Einflussdiagnostik wird vor Validation festgelegt.
17. Heavy-Tail-Behandlung wird vor Validation festgelegt.
18. Validation-Daten werden nicht wiederverwendet, nachdem sie Designentscheidungen beeinflusst haben.
19. Kosten werden früh als Machbarkeitshürde und später detailliert/executionnah modelliert.
20. Die vollständige Pipeline besteht vor Freeze wiederholte strukturtreue Nullkontrollen und einen bekannten positiven Sentinel.
21. Risk Management erzeugt keine Edge.
22. Ein validiertes Phänomen ist noch keine validierte Strategie.
23. Die vollständige Strategie braucht erneut OOS-/Forward-Evidenz.
24. Aktive Strategien bleiben falsifizierbar.
25. Materielle Änderungen erzeugen neue Versionen.
26. Jeder Claim wird als prädiktiv, interventional oder kontrafaktisch deklariert.
27. Kausale Sprache benötigt ein Estimand und ein bestandenes Identifikationsgate.
28. Granger- und Causal-Discovery-Ausgaben sind ohne Zusatzannahmen Hypothesengeneratoren, keine Kausalbeweise.
29. DML und andere flexible Schätzer lösen kein Identifikationsproblem.
30. Eine erwartete minus tatsächliche Reaktion ist zunächst eine Reaktionsinnovation, kein Kausalbruch.
31. Event-Schocks benötigen vorab verfügbare Erwartungen, Daten-Vintages, Zeitstempel und Kontaminationsregeln.
32. Backtest- oder OOS-Erfolg validiert nicht rückwirkend den behaupteten Kausalmechanismus.
33. Post-treatment Mediatoren werden nicht als gewöhnliche Controls eines Total-Effekts verwendet.
34. Constraint-/Lever-Labels folgen dem Maschinenvertrag; Goldratt ist höchstens ein optionales Priorisierungswerkzeug für belegte Implementation Constraints.
35. Quantitativer Default ist die einfachste messbare Shock-Response-Map, nicht ein automatischer Constraint-Score.
36. Ein Informationsengpass benötigt ein definiertes End-Outcome und inkrementellen zeitlich OOS-Prognosewert.
37. Ein identifizierter kausaler Hebel, ein prädiktiver Informationsengpass und ein operativer Implementierungsengpass sind verschiedene Aussagen.
38. Mehrere Surprise-Faktoren, Kettenglieder, Horizonte und States zählen vollständig zum Research-Suchraum.
39. Bei ausführbarer kausaler Analyse ist der Tooling-Router aus `04_CAUSAL_TOOLING.md` verbindlich; passende Spezialbibliotheken sind der Default.
40. Ein Bibliotheksoutput ersetzt weder Identifikation noch Domänenannahmen und erhöht den Claim-Level nicht.
41. Exakte Laufzeit-, Paket-, API-, Seed- und Splitinformationen werden vor Freeze reproduzierbar protokolliert.
42. `EconML`/`DoubleML` werden erst nach Identifikation eingesetzt; `Tigramite`-Discovery bleibt ein Kandidatengenerator.
43. Eine Rohidee wird vor Phase 0 versioniert gescreent; `PROMOTED` bedeutet testbar, nicht bestätigt.
44. Mechanismusevidenz, Forward-OOS-Prognose und ausführbare Netto-Edge sind drei getrennte Status.
45. Intraday-Research fixiert Venue, Handelsphase, Kalender, Zeitbasis, Feed-Coverage und Ereignisklasse.
46. „Newsfrei“ wird nie pauschal behauptet, sondern nur als dokumentierte News-/Makro-Policy mit bekannten Coverage-Grenzen operationalisiert.
47. Mechanismenfamilien und Intraday-Router sind nicht abschließend und erzeugen keine Edge durch Klassifikation.
48. Ein Generation-Run erzeugt nur `INBOX`-Kandidaten; Mechanismenkatalog, Operator oder Literaturquelle bestätigen weder Hypothese noch Edge.

---

# 22. Verbindliche Pipeline

```text
G. OPTIONALE IDEENGENERATION AUS MECHANISMENKATALOG → INBOX
0. HYPOTHESEN-INTAKE + SCOPE + SCREENING
1. Vorläufige Beobachtung / Outcome-Skala
2. PHASE-0-VORPRÜFUNG
3. Discovery / Fallkatalog + optionale Effect-Cause-Effect-Map
4. Claim-Level + explizites Identifikationsmodell + Beobachtbarkeit + Tooling-Router
5. Operationalisierung
6. Zielvariable + Nullmodell + gegebenenfalls Surprise-Faktoren/Shock-Response-Map
7. Effektgröße + Unsicherheit
8. Abhängigkeit + effektives N
9. State-/Regimeanalyse
10. Candidate Hypothesis
11. Vorhersage-Liste + Pre-Mortem
12. Multiple-Testing-/Einfluss-/Heavy-Tail-Plan
13. FORMALE PHASE-0-RE-KALKULATION + VALIDATION-PLAN
14. PIPELINE-INTEGRITÄTSGATE
15. FREEZE
16. Unabhängige Validation
17. Final Holdout oder äußeres Walk-Forward
18. Robustheit / Replikation
19. Ökonomische Umsetzbarkeit
20. Strategy Engineering
21. Vollständige Strategie erneut OOS
22. Forward-OOS
23. Monitoring / Degradation
24. Revalidieren / Suspendieren / Verwerfen
```

Kein AI-Agent darf einen Schritt stillschweigend überspringen. Nicht anwendbare Schritte müssen als `N/A` mit Begründung markiert werden.
