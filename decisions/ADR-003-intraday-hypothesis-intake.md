# ADR-003: Scope- und evidenzgestufte Aufnahme von Intraday-Hypothesen

**Status:** Accepted  
**Date:** 2026-08-30  
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Ideen für Intraday-Research werden häufig gleichzeitig als Marktmechanismus,
beobachtetes Muster, Prognosesignal und handelbare Anomalie beschrieben. Dadurch
entstehen unzulässige Sprünge in der Evidenzkette. Beispiele sind:

- aus nachgewiesenem Market-Maker-Hedging unmittelbar eine profitable
  Gamma-Strategie abzuleiten,
- aus einer Index- oder Funding-Regel einen sicheren Preisverlauf zu folgern,
- eine historische Return-Zerlegung als eigenständigen Mechanismus zu behandeln,
- oder einen peer-reviewten Befund ohne projektspezifische Replikation als
  ausführbare Trading-Kante einzustufen.

Zugleich ist der Ausdruck „newsfrei“ mehrdeutig. Er kann den Ausschluss
klassischer Informationsereignisse wie Earnings, CPI oder FOMC meinen, obwohl
weiterhin geplante strukturelle Ereignisse wie Indexumstellungen, Auktionen oder
Funding-Timestamps verwendet werden. Er kann aber auch als unbelegbare Aussage
verstanden werden, dass zu einem Zeitpunkt keinerlei neue Information in den
Markt gelangt sei. Letzteres ist empirisch nicht beobachtbar.

Das Framework benötigt deshalb eine verbindliche Intake-Regel, die den Scope
einer Idee vor ihrer Ausarbeitung festlegt und Mechanismusevidenz strikt von
Forward-Predictability und einer ausführbaren Nettokante trennt.

## Decision

Jede neue Intraday-Hypothese wird vor Datenauswahl, Backtest und Modellierung
klassifiziert. Die Klassifikation ist keine Qualitätsbewertung und keine
Aktivierungsfreigabe.

### 1. Scope-Taxonomie

Jeder Kandidat erhält genau einen primären Scope. Sekundäre Scopes dürfen
ergänzt werden, wenn die Hypothese tatsächlich mehrere Mechanismen verbindet.

| Scope | Definition | Typische Beispiele | Normative Abgrenzung |
|---|---|---|---|
| `INFORMATION_EVENT` | Preisreaktion auf die Veröffentlichung neuer unternehmens-, makro- oder politikbezogener Information | Earnings und PEAD, Guidance, CPI, FOMC, Ad-hoc-Meldungen | Unter einer Policy, die News- oder Makro-Events ausschließt, nicht zulässig |
| `SCHEDULED_STRUCTURAL_EVENT` | Vorab terminierter Markt-, Benchmark-, Abrechnungs- oder Mandatsvorgang, der mechanische Flows erzeugen kann | Index-Rebalancing, Opening/Closing Auction, Funding-Timestamp, Monats-/Quartalsend-Rebalancing | Ist ein Event, auch wenn es nicht auf neue Fundamentalinformation reagiert |
| `CONTINUOUS_ENDOGENOUS_MECHANISM` | Fortlaufend aus Handel, Liquiditätsbereitstellung, Inventar, Hedging oder Interaktion von Märkten entstehender Prozess | Order-Flow-Imbalance, Liquiditätsentzug, Lead-Lag, Execution-Flows, konditionales Gamma-Hedging | Darf nicht allein wegen mechanischer Plausibilität als prognostisch gelten |
| `RETURN_DECOMPOSITION` | Deskriptive Zerlegung beobachteter Renditen nach Zeitfenster, Session, Faktor oder Portfolio | Overnight versus Intraday, Open-to-Close versus Close-to-Open, Session-Saisonalität | Ist zunächst Mess- und Diagnoseperspektive, kein eigenständiger Mechanismus |

Die Taxonomie ist für Scope und Routing abschließend; die darin untersuchten
Mechanismenfamilien sind ausdrücklich **nicht abschließend**. Insbesondere sind
zulässige Kandidaten nicht auf drei oder vier vermeintlich fundamentale
Mechanismen beschränkt.

### 2. Operationalisierung von „newsfrei“

„Newsfrei“ wird nicht als Eigenschaft der Realität behauptet, sondern nur als
dokumentierte Research-Policy operationalisiert. Ein entsprechender Test muss
mindestens festhalten:

1. welche Ereignisklassen ausgeschlossen werden,
2. welche Kalender, Feeds, Anbieter und Versionen diese Ereignisse abdecken,
3. welche instrument- und ereignisspezifischen Ausschlussfenster gelten,
4. wie verspätete, korrigierte oder fehlende Meldungen behandelt werden,
5. und welche bekannten Coverage-Lücken verbleiben.

Die Abwesenheit eines Treffers in den verwendeten Feeds beweist nicht die
Abwesenheit neuer Information. Ergebnisse werden deshalb als „gemäß Policy und
bekannter Feed-Coverage gefiltert“ bezeichnet, nicht als informationsfrei.
Geplante strukturelle Ereignisse sind separat zu deklarieren und dürfen nicht
durch das Label „newsfrei“ unsichtbar werden.

### 3. Getrennte Evidenzstufen

Jede Hypothese wird auf genau der höchsten tatsächlich belegten Stufe geführt.
Die Stufen dürfen nicht durch sprachliche Plausibilität übersprungen werden.

#### `mechanism_supported`

Es gibt belastbare Evidenz, dass der behauptete ökonomische oder mechanische
Kanal in einem definierten Setting existieren kann. Dazu können akademische
Primärstudien, Börsenregeln, Indexmethodiken, Fondsprospekte oder direkte
Marktdaten gehören.

Diese Stufe erlaubt die Formulierung einer falsifizierbaren Hypothese. Sie belegt
weder stabile Vorhersagekraft noch Handelbarkeit. Die Richtung eines Signals
muss konditional korrekt formuliert sein, etwa auf das Vorzeichen der
Netto-Gamma-Exponierung oder ein tatsächlich dokumentiertes Rebalancing-Mandat.

#### `forward_predictive_oos`

Die vorab eingefrorene Hypothese zeigt auf zuvor ungesehenen Daten zeitlich
korrekte Vorhersagekraft. Erforderlich sind mindestens:

- decision-time verfügbare Features und point-in-time Daten,
- ein festgelegtes Target und Prognosefenster,
- zeitgerechte Out-of-Sample- oder Walk-forward-Trennung,
- Kontrolle von Auswahl-, Multiple-Testing- und Leakage-Risiken,
- Stabilitäts- und Regimeanalysen,
- sowie die für den Scope festgelegten Event- und Coverage-Filter.

Out-of-Sample-Predictability kann brutto bestehen und dennoch nach Kosten,
Latenz oder Kapazitätsgrenzen unhandelbar sein.

#### `executable_net_edge`

Die Vorhersage lässt sich mit den real verfügbaren Instrumenten und
Entscheidungszeiten als robuste Nettokante umsetzen. Zusätzlich zur vorherigen
Stufe müssen mindestens berücksichtigt werden:

- ausführbare Preise statt nicht handelbarer Referenz- oder Auktionsprints,
- Latenz, Queue-Position und Fill-Wahrscheinlichkeit,
- Spread, Gebühren, Slippage und Market Impact,
- Borrow, Funding, Margin und Liquidationsrisiko, soweit anwendbar,
- Turnover, Kapazität, Positionslimits und Betriebsfehler,
- sowie prospektive Shadow-, Paper- oder Live-Evidenz nach dem Freeze.

Nur diese Stufe kann zusammen mit allen übrigen Risk- und Governance-Gates eine
Aktivierung tragen. Ein Mechanismuspaper ist niemals für sich genommen eine
Trading-Edge. Auch ein Paper mit berichteter Strategieperformance ersetzt keine
point-in-time, kostenbewusste und projektspezifische Replikation.

### 4. Nicht abschließende Mechanismenfamilien

Das Intake muss neue Familien zulassen. Der aktuelle Suchraum umfasst unter
anderem:

- Orderbuch, Order Flow, Marktliquidität und Dealer-Inventar,
- Cross-Market-Preisfindung, Lead-Lag und relative Preisbindung,
- TWAP-, VWAP- und andere Execution-Flows,
- Options-, Futures- und ETF-Hedging einschließlich Gamma- und Delta-Effekten,
- Benchmark-, Fixed-Mix-, Target-Date- und sonstige Mandats-Rebalancings,
- Opening-, Closing- und andere periodische Auktionen sowie Session-Übergänge,
- Funding-, Settlement-, Expiry- und Marginmechanismen,
- Relative Value, Pairs, Cointegration und temporäre Basisabweichungen,
- erzwungene Deleveraging-, Liquidations- und Risikolimit-Flows,
- sowie Teilnehmer-, Zugangs- und Zeitzonen-Segmentierung.

Diese Liste ist ein Rechercheindex, keine Whitelist und keine Behauptung, dass
jede Familie eine Vorhersage oder Nettokante enthält. Akademische Forschung,
Börsendokumente und explorative Datenanalyse sind Quellen beziehungsweise
Methoden der Hypothesenfindung, nicht zusätzliche Mechanismenfamilien.

### 5. Mindestinhalt eines Intake-Records

Vor Weiterleitung in den Research-Prozess werden mindestens dokumentiert:

- präziser Mechanismus- und Prognoseclaim,
- primärer und gegebenenfalls sekundärer Scope,
- Markt, Venue, Instrumente, Session und Zeithorizont,
- decision-time beobachtbare Inputs und vorgesehenes Target,
- News-/Event-Policy, Feed-Coverage und Ausschlussfenster,
- aktuell belegte Evidenzstufe,
- erwartetes Vorzeichen einschließlich aller Konditionen,
- zentrale Alternativerklärungen und Falsifikationstests,
- Ausführungs-, Kosten- und Kapazitätsannahmen,
- sowie Abbruch- und Promotion-Kriterien für die nächste Evidenzstufe.

## Rejected Blanket Alternatives

### Alternative A: Der Intraday-Markt lasse sich vollständig auf drei oder vier Mechanismen reduzieren

Verworfen. Solche Listen sind nützliche Einstiege, aber weder vollständig noch
stabil über Märkte, Produkte und Marktstrukturänderungen. Sie begünstigen zudem
Scope-Laundering, wenn Quellen, Messperspektiven und Mechanismen gleichgesetzt
werden.

### Alternative B: Ein mechanischer oder geplanter Vorgang sei automatisch newsfrei

Verworfen. Indexänderungen benötigen beispielsweise eine Ankündigung;
Eröffnungen verarbeiten Overnight-Information; Funding- und Auktionsfenster
können mit Nachrichten zusammenfallen. Der mechanische Teil bleibt untersuchbar,
muss aber durch Policy, Coverage und Ausschlussfenster isoliert werden.

### Alternative C: Peer Review oder Journalprestige belege eine aktuelle Trading-Kante

Verworfen. Publikationsstatus und Quellenqualität werden nach ADR-002 erfasst,
ersetzen aber weder Replikation noch aktuelle Out-of-Sample- und
Ausführungsevidenz.

### Alternative D: Ein statistisch signifikantes Muster belege seinen Mechanismus

Verworfen. Dasselbe Muster kann durch Information, institutionelle Zwänge,
Liquidität, Messfehler oder mehrere überlagerte Kanäle entstehen. Mechanismusclaim
und Prognoseclaim werden separat getestet.

### Alternative E: Out-of-Sample-Predictability sei bereits eine Nettokante

Verworfen. Nicht handelbare Preise, Latenz, geringe Fill-Raten, Kosten, Borrow,
Funding, Impact und Kapazität können eine valide Prognose vollständig aufzehren.

### Alternative F: Kein Treffer im Ereignisfeed beweise die Abwesenheit von News

Verworfen. Feeds haben Coverage-, Timestamp-, Klassifikations- und
Revisionsgrenzen. Der verbleibende Informationsanteil ist unbekannt und wird
nicht auf null gesetzt.

## Consequences

- Eingehende Intraday-Ideen werden als Hypothesenkandidaten aufgenommen, nicht
  als bereits validierte Strategien.
- PEAD, Earnings, CPI und FOMC werden als `INFORMATION_EVENT` geführt und sind in
  einem news-/makroausschließenden Forschungszweig unzulässig.
- Index-Rebalancing, Funding, Monats-/Quartalsende und Auktionen bleiben als
  `SCHEDULED_STRUCTURAL_EVENT` sichtbar; sie dürfen in einem entsprechend
  definierten strukturellen Event-Modul untersucht werden.
- Order-Flow-, Execution- und Gamma-Hypothesen können als
  `CONTINUOUS_ENDOGENOUS_MECHANISM` untersucht werden, benötigen aber
  konditionale Positions- beziehungsweise Vorzeichenannahmen und Event-Filter.
- Overnight-/Intraday-Befunde werden zunächst als `RETURN_DECOMPOSITION`
  behandelt. Eine solche Zerlegung darf nicht ohne separaten Mechanismus- und
  Ausführungstest zur Strategie erklärt werden.
- Ein Research Case kann mehrere Scopes enthalten, muss Ergebnisse und Gates
  jedoch scopeweise ausweisen; Evidenz aus einem Scope darf einen anderen nicht
  stillschweigend freigeben.
- Das Evidence Grade aus der Operationsschicht bleibt von den drei hier
  definierten Entwicklungsstufen getrennt. Quellenstärke, Reife einer Hypothese
  und Aktivierungsfähigkeit sind unterschiedliche Dimensionen.
- Jede Promotion auf `forward_predictive_oos` oder `executable_net_edge` erzeugt
  einen prüfbaren, versionierten Entscheidungsnachweis. Rückstufungen bei
  Replikationsfehlern, Regimebruch oder Kostenänderungen bleiben möglich.
- Der zusätzliche Intake-Aufwand reduziert die Zahl schnell aktivierbarer Ideen,
  verhindert dafür die Gleichsetzung von plausibler Marktgeschichte,
  publiziertem Befund und belastbarer Nettokante.

## Action Items

1. [x] Scope-Taxonomie und Evidenzstufen in den normativen Research-Workflow aufgenommen.
2. [x] Intake-Felder in Case-Template und maschinenlesbares Intake-Artefakt integriert.
3. [x] Positive und negative Contract-Tests für Scope, News-Policy und Promotionspfade ergänzt.
4. [x] Eval-Fälle für Mechanismus-zu-Edge-Übertreibung, anonyme Execution-Signaturen und unvollständige News-Coverage ergänzt.
5. [ ] Bestehende Intraday-Hypothesen nach der neuen Taxonomie neu klassifizieren; im vorliegenden Repository sind noch keine konkreten Research Cases vorhanden, daher bleibt dies als Migrationsschritt für die ersten importierten Cases offen.
