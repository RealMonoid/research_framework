# 03_RESEARCH_METHODS.md

**Version:** 1.9
**Stand:** 2026-08-31
**Status:** ENTWURF ZUR ÜBERNAHME  
**Zweck:** Methodenauswahl für AI-Agenten. Dieses Dokument sagt nicht, dass jede Methode immer angewendet werden muss. Es verhindert, dass notwendige Methoden vergessen oder dekorativ genannt werden.

---

# 1. Benutzungsregel

Für jede relevante Methodengruppe muss der Agent im Research-Artefakt dokumentieren:

1. `ANWENDEN`, `N/A + Begründung` oder `BLOCKED + fehlende Information`,
2. warum,
3. welche konkrete Variante,
4. welche Annahmen die Methode benötigt,
5. welche Entscheidung aus dem Ergebnis folgen kann.

Eine Methode darf nicht bloß erwähnt werden.

Sobald die Methode als ausführbarer kausaler Arbeitsschritt implementiert wird, gilt zusätzlich der Bibliotheks- und Reproduzierbarkeitsrouter aus `04_CAUSAL_TOOLING.md`. Eine passende Spezialbibliothek ist der Default; ihr Output bleibt an die hier dokumentierten Annahmen und Claim-Grenzen gebunden.

---

# 2. Phase-0-Power und Stichprobenplanung

## Anwenden wenn

- ein primärer Effekt formal validiert werden soll,
- ein Holdout knapp ist,
- eine Mindeststichprobe benötigt wird,
- die wirtschaftlich relevante Effektgröße vorab definierbar ist.

## Nicht ausreichend

`Wir haben 20 Fälle` oder `das letzte CSV enthält 15 Paare`.

## Pflichtinputs

- `δ_econ`,
- `δ_plan` oder direktes Präzisionsziel,
- explizite Null-/Alternativhypothese beziehungsweise Intervall-Entscheidungsregel,
- Ziel-Power oder Präzisionsziel,
- Fehlerniveau/Entscheidungsregel,
- explorativer Streuungs-Punktschätzer samt Quelle und Unsicherheit,
- konservative Planungsstreuung beziehungsweise Stressszenario,
- Test-/Schätztyp,
- Abhängigkeitsannahme.

## Streuungsplanung

Ein einzelner Punktschätzer aus kleinen, selektierten oder heavy-tailed Discovery-Daten darf nicht ungeprüft als wahre Planungsstreuung verwendet werden.

Mindestens zu rechnen sind:

1. **Basisszenario** – bestmögliche sachlich begründete Streuungsschätzung,
2. **Stressszenario** – konservative, aber noch plausible Planungsstreuung.

Mögliche Grundlagen sind externe oder gepoolte Referenzen, eine unter gültigen Modellannahmen berechnete obere Unsicherheitsgrenze, robuste Skalenmaße mit begründetem Stressaufschlag oder eine vorab definierte Szenariorechnung. Eine Obergrenze ist nur dann vorzuziehen, wenn ihre Verteilungsannahmen zur Datenlage passen.

Die Auswahlregel für das Stressszenario wird vor der Berechnung fixiert. Bei mehreren vorab zulässigen und sachlich übertragbaren Kandidaten verwendet das Gate den konservativsten Wert oder die vollständige Bandbreite. Ein robustes Skalenmaß darf nur nach expliziter Abbildung auf die Stichprobenverteilung des primären Schätzers verwendet werden, bei Bedarf per designspezifischer Simulation.

`δ_econ` ist die wirtschaftliche Grenze; `δ_plan` ist eine angenommene wahre Wirkung für die Planung. Wenn der spätere Erfolg beispielsweise `untere Intervallgrenze > δ_econ` verlangt, muss genau diese Regel simuliert oder über ein passendes Präzisionsziel geplant werden. Eine Powerrechnung für `0` gegen `δ_econ` beantwortet diese strengere Frage nicht.

Quelle und Begründung von `δ_plan` sind Pflicht. Ein Discovery-Punktschätzer wird nicht ungeprüft übernommen; Auswahlverzerrung und Unsicherheit werden durch konservative Szenarien, Shrinkage oder externe Referenzen berücksichtigt.

## Arbeitsdefaults für klassische Tests

Wenn keine sachlich bessere, vorab begründete Entscheidungsregel besteht:

- `α = 0,05`, zweiseitig,
- `Power = 80 %` als Mindest-Arbeitsdefault,
- bei knappem finalem Holdout oder hohen Kosten falsch-negativer Befunde `90 %` oder ein direktes Präzisionsziel prüfen.

Einseitige Tests, geringere Power oder andere Fehlergewichtungen müssen vor Kenntnis des Ergebnisses begründet werden. Diese Werte sind Governance-Defaults, keine universelle Aussage über ausreichende Evidenz.

## Mögliche Verfahren

- analytische Powerrechnung bei einfachen Tests,
- Monte-Carlo-Simulation,
- clusterbasierte Simulation,
- Bootstrap-basierte Präzisionsplanung.

## Entscheidung

- aktuell vorhandene unabhängige Information reicht im konservativen Szenario für den jeweiligen Gate-Zweck → `WEITER`,
- grundsätzlich testbar, aber zu wenig Information → `DATEN BESCHAFFEN`,
- wirtschaftlich/statistisch nicht sinnvoll entscheidbar → `ABBRECHEN`.

Phase 0 wird als frühe Vorprüfung und als formale Re-Kalkulation nach Festlegung von Outcome, Nullmodell, Abhängigkeit, effektivem N und Validation-Plan durchgeführt. Nur die formale Re-Kalkulation darf den Weg zum Freeze öffnen.

---

# 3. Effektive Stichprobengröße

## Problem

Nominelles `N` überschätzt Evidenz bei Autokorrelation, Clustering und korrelierten Symbolen.

## Prüfen

- Autokorrelation von Outcomes/Signalen,
- Signale pro Session/Event,
- gemeinsame Makroevents,
- Korrelationsstruktur der Symbole,
- überlappende Forward-Fenster.

## Mögliche Ausgaben

- effektives N,
- Anzahl unabhängiger Cluster,
- konservative Bandbreite,
- Design Effect.

## Regel

Wenn eine seriöse effektive-N-Schätzung nicht möglich ist, darf `nominelles N` nicht als unabhängige Evidenzzahl ausgegeben werden.

Für Gates werden Methode/Simulation, Punktschätzer, konservative Untergrenze und unabhängige Clusterzahl berichtet. Maßgeblich ist die konservative Untergrenze. Die Planungsreihenfolge lautet:

`benötigtes N_eff/Clusterzahl → designspezifischer DE oder Simulation → benötigtes nominelles N`, jeweils aufgerundet.

## Design Effect

Allgemein:

\[
DE = \frac{Var(\hat\theta\mid tatsächliches\ Design)}{Var(\hat\theta\mid IID\text{-Referenz})},
\qquad N_{eff} \approx \frac{N}{DE}
\]

Nur bei einer einfachen austauschbaren Clusterstruktur mit gleich großen Clustern darf näherungsweise verwendet werden:

\[
DE = 1 + (m-1)\rho
\]

mit mittlerer Clustergröße `m` und Intracluster-Korrelation `ρ`. Bei ungleichen Clustergrößen, zeitlicher Abhängigkeit, mehreren Clusterebenen oder korrelierten Symbolen ist eine passende Erweiterung oder Simulation erforderlich. Ein unbegründeter Default für `DE` ist unzulässig.

Bei weniger als 30 plausibel unabhängigen Clustern wird `SMALL_CLUSTER_WARNING` gesetzt. Das ist kein automatisches FAIL; erforderlich sind jedoch eine Small-Sample-Methode, eine designspezifische Simulation/Kalibrierung oder `BLOCKED`.

Im Stressszenario wird `DE < 1` beziehungsweise `N_eff > N` nur angerechnet, wenn der Informationsgewinn durch externe, übertragbare Evidenz und ein vorab festgelegtes Modell belastbar gestützt ist; andernfalls gilt für die Planung mindestens `DE = 1`.

---

# 4. Block-Bootstrap

## Anwenden wenn

- zeitliche Abhängigkeit innerhalb zusammenhängender Marktperioden besteht,
- einzelne Trades nicht unabhängig resampled werden dürfen.

## Idee

Zusammenhängende Zeitblöcke statt Einzelbeobachtungen resamplen.

## Designfragen

- Blocklänge,
- feste oder variable Blöcke,
- Sessiongrenzen,
- Intraday- versus Mehrtagesstruktur.

## Risiko

Zu kurze Blöcke zerstören Abhängigkeit; zu lange Blöcke liefern wenige effektive Resampling-Einheiten.

---

# 5. Cluster-Bootstrap / clusterrobuste Inferenz

## Anwenden wenn

Beobachtungen sinnvoll in Gruppen zusammengehören, zum Beispiel:

- Handelstag,
- Session,
- Makroevent,
- Impulscluster,
- Symbolgruppe.

## Regel

Die Clustereinheit muss **vor Validation** festgelegt oder aus einer klaren Datenstruktur abgeleitet werden.

Ein Agent darf nicht nach dem Ergebnis die Clustereinheit wählen, die das günstigste Intervall erzeugt.

Bei `SMALL_CLUSTER_WARNING` darf ein gewöhnliches Cluster-Bootstrap- oder asymptotisches Clusterintervall nicht allein aufgrund seines Namens als zuverlässig gelten. Clustergrößen, Leverage, Zahl und Balance der Cluster sowie die konkrete Intervallkonstruktion müssen in einer zum Design passenden Simulation oder Small-Sample-Korrektur berücksichtigt werden. Die Warnung bedeutet nicht automatisch, dass jedes Intervall zu schmal ist.

---

# 6. Purging und Embargo

## Anwenden wenn

- Labels/Outcomes über Zeitfenster definiert sind,
- Forward-Horizonte sich überlappen,
- Train- und Testbeobachtungen gemeinsame zukünftige Preisabschnitte enthalten könnten.

## Purging

Beobachtungen entfernen, deren Label-/Outcome-Periode über die Train/Test-Grenze reicht.

## Embargo

Zusätzliche zeitliche Sicherheitszone um die Trennstelle.

## Pflicht

Der Agent muss prüfen, ob die verwendeten Outcomes zeitlich überlappen. `N/A` ist nur mit Begründung zulässig.

---

# 7. Korrelation zwischen Symbolen

## Problem

Mehrere Symbole können denselben Risikofaktor oder dasselbe Makroereignis widerspiegeln.

## Prüfen

- Return-Korrelation,
- Signal-Korrelation,
- Outcome-Korrelation,
- gemeinsame Underlyings/Faktoren,
- zeitgleiche Eventcluster.

## Praktische Behandlung

- Clusterung nach Underlying/Faktor,
- separate Symbolberichte,
- Ergebnis ohne dominantes Symbol,
- keine simple Addition korrelierter Symbole zur Evidenzzahl.

---

# 8. Einflussdiagnostik

## Pflichtdiagnosen

Mindestens:

- Leave-one-out,
- Leave-one-cluster-out,
- ohne dominantes Symbol,
- ohne dominante Periode/Eventgruppe.

## Zusätzliche Maße

Je nach Modell:

- Cook's Distance,
- leverage-artige Maße,
- Anteil an Sum of Squares/Streuung,
- Beitrag zur Gesamtrendite,
- Beitrag zum Punktschätzer.

## Verbindliche Mindestentscheidung

Kippt die wirtschaftliche Schlussfolgerung oder das Vorzeichen beim Entfernen eines einzelnen plausiblen Clusters, ist die Evidenz nicht robust bestätigt.

Weitere numerische Schwellen müssen im Freeze projektspezifisch festgelegt werden.

---

# 9. Heavy-Tail-Outcomes und robuste Lageparameter

## Problem

Trading-Outcomes können schwerschwänzig sein. Ein Mittelwert kann stark von wenigen Extremwerten abhängen.

## Vor Validation festlegen

- primärer Lageparameter,
- robuste Sensitivitätskennzahl,
- Umgang mit Ausreißern,
- Transformationsregeln.

## Mögliche Schätzer

- arithmetischer Mittelwert,
- Median,
- trimmed mean,
- winsorisierter Mittelwert,
- robuste M-Schätzer.

## Empfehlung zur Interpretation

Wenn ökonomische Expectancy der Gegenstand ist, kann der Mittelwert primär bleiben. Dann muss jedoch zusätzlich geprüft werden, wie empfindlich er auf Extremwerte reagiert.

Ein robuster Schätzer darf nicht erst gewählt werden, nachdem das primäre Ergebnis missfällt.

---

# 10. Unsicherheitsintervalle

## Ziel

Nicht nur Punktwerte berichten.

## Mögliche Verfahren

- klassisches Konfidenzintervall bei passenden Annahmen,
- Bootstrap-Intervall,
- Block-/Cluster-Bootstrap-Intervall,
- clusterrobustes Intervall,
- Bayesianisches Posteriorintervall, wenn das gesamte Design darauf ausgelegt ist.

## Auswahlregel

Die Methode muss zur Datenabhängigkeit und Outcome-Verteilung passen.

Bei `SMALL_CLUSTER_WARNING` muss zusätzlich dokumentiert werden, wie die Abdeckung beziehungsweise Fehlerrate für das konkrete Design kalibriert oder warum die Analyse als `BLOCKED` eingestuft wurde.

---

# 11. Wirtschaftliche Relevanz statt nur Null gegen 0

## Kerngedanke

Der relevante Vergleich ist häufig nicht:

`Effekt > 0?`

sondern:

`Effekt > δ_econ?`

oder bei zweiseitiger Fragestellung:

`|Effekt| > δ_econ?`

## Vier Interpretationen

1. klar wirtschaftlich relevant in erwarteter Richtung,
2. klar wirtschaftlich relevant in Gegenrichtung,
3. klar wirtschaftlich irrelevant,
4. unpräzise.

Diese vier Zustände müssen bereits im Freeze definiert werden.

---

# 12. False Discovery Rate (FDR)

## Anwenden wenn

viele Hypothesen parallel getestet werden und der erwartete Anteil falscher Entdeckungen kontrolliert werden soll.

## Geeignet für

- viele Statevariablen,
- viele Features,
- mehrere parallele Hypothesenfamilien.

## Nicht ausreichend wenn

nur der beste Trading-Backtest aus einer stark adaptiven Strategieauswahl beurteilt werden soll. Dafür sind Reality-Check-/SPA-/PBO-artige Verfahren oft näher am Problem.

---

# 13. White's Reality Check

## Anwenden wenn

viele Strategien/Modelle gegen eine Benchmark getestet wurden und beurteilt werden soll, ob der beste historische Sieger mehr leistet, als durch Data Snooping zu erwarten wäre.

## Wichtig

Die tatsächlich getestete Strategiefamilie muss möglichst vollständig abgebildet werden. Nur die überlebenden Modelle einzubeziehen unterschätzt den Suchraum.

---

# 14. Hansen SPA

## Anwenden wenn

mehrere Modelle gegen eine Benchmark verglichen werden und White's Reality Check zu konservativ oder unempfindlich sein könnte.

## Ziel

Superior Predictive Ability der Kandidatenfamilie gegenüber der Benchmark beurteilen.

---

# 15. Deflated Sharpe Ratio

## Anwenden wenn

- Sharpe Ratio zentrale Selektionskennzahl ist,
- viele Varianten getestet wurden,
- Renditen nicht normal sind,
- der beste Backtest ausgewählt wurde.

## Zweck

Die naive Sharpe-Euphorie um Auswahlverzerrung und Verteilungsprobleme reduzieren.

## Nicht verwenden als

alleinige Edge-Validierung. DSR ersetzt kein gutes OOS-Design.

---

# 16. Probability of Backtest Overfitting (PBO)

## Anwenden wenn

viele Strategievarianten existieren und geprüft werden soll, wie häufig In-Sample-Sieger Out-of-Sample enttäuschen.

## Aussage

PBO quantifiziert Auswahlrisiko, nicht Marktkausalität.

---

# 17. Pipeline-Integritäts- und Auswahltests

## 17.1 Pipeline-Negativkontrollen vor Freeze

### Zweck

Prüfen, ob Implementierungsfehler, Leakage, falsches Timing, Vorzeichenfehler, Indexverschiebungen oder eine adaptive Auswahlpipeline auch ohne echten Effekt scheinbare Evidenz erzeugen.

### Pflichtdesign

- Die **vollständige** Feature-, Auswahl-, Filter-, Timing- und Auswertungspipeline wird ausgeführt.
- Null-/Surrogatdaten erhalten die unter dem Nullmodell relevante Zeit-, Cluster-, State- und Volatilitätsstruktur soweit wie methodisch möglich.
- Die Kontrolle wird oft genug wiederholt, um Fehlalarmrate und Null-Effektverteilung mit sinnvoller Monte-Carlo-Unsicherheit zu beurteilen.
- Mindestens ein synthetischer bekannter positiver Effekt mit festem Vorzeichen und Timing dient als Sentinel gegen Vorzeichen-, Indexierungs- und Look-ahead-Fehler.
- Akzeptanzregeln für Fehlalarme, Effektverteilung, Richtung und Timing werden vorab festgelegt.

Kontrollbasis und Datenrolle werden protokolliert. Designbeeinflussende Tests verwenden nur Development-Daten oder rein synthetische Daten. Vorab werden Zielpräzision der Fehlalarmrate und geplantes `B` festgelegt; anschließend werden tatsächliches `B` sowie Monte-Carlo-Standardfehler oder ein binomiales Intervall berichtet. `PASS` setzt die erreichte Zielpräzision voraus.

Naives Label-Shuffling ist unzulässig, wenn es relevante Zeit- oder Clusterabhängigkeit zerstört. Ein volatilitätsangepasster Random Walk kann eine Kontrolle sein, beweist allein aber weder korrekte Kalibrierung noch Fehlerfreiheit. Ein einzelner Kontrolllauf genügt nicht.

### Entscheidung

- Kontrollen innerhalb der vorab definierten Toleranzen und Sentinel korrekt erkannt → `PASS`,
- Fehlalarme, falsches Vorzeichen/Timing oder nicht erklärte Pipeline-Effekte → `FAIL`,
- keine strukturgültige Kontrolle konstruierbar → `BLOCKED`.

Ohne `PASS` kein Freeze.

Status-Mapping: `Gate PASS → Phase COMPLETE`, `Gate FAIL → Phase FAILED`, `Gate BLOCKED → Phase BLOCKED`.

## 17.2 Bootstrap der gesamten Research-Pipeline

### Anwenden wenn

nicht nur die Unsicherheit eines festen Modells interessiert, sondern die Unsicherheit des **Auswahlprozesses**.

### Pipeline

```text
Daten resamplen
→ Kandidaten erneut testen
→ Sieger erneut auswählen
→ Sieger-Performance messen
```

statt nur:

```text
festen Sieger resamplen
```

### Nutzen

Zeigt, wie stark das finale Ergebnis davon abhängt, dass gerade diese Stichprobe gerade diesen Sieger erzeugt hat.

---

# 18. Holdout versus Nested Walk-Forward

## Final Holdout bevorzugen wenn

- genügend Daten vorhanden sind,
- ein wirklich unangetasteter Block reserviert werden kann,
- Strategieentwicklung vor dem finalen Test abgeschlossen werden kann.

## Nested Walk-Forward bevorzugen wenn

- Markt nichtstationär ist,
- laufende Re-Kalibrierung Teil des Designs ist,
- ein großer finaler Holdout zu teuer wäre.

## Regel

Äußere Testfenster dürfen nicht zur Optimierung des inneren Modells verwendet werden.

---

# 19. State-/Regimeanalyse

## Erst kontinuierlich prüfen

Bevor Kategorien wie `Trend`, `Range`, `High Vol` festgelegt werden, untersuchen:

- funktionale Beziehung,
- Monotonie,
- Plateaus,
- U-Formen,
- Übergangsbereiche.

## Danach diskretisieren wenn

- operativ nötig,
- durch die Beziehung begründet,
- nicht nur zur P&L-Maximierung.

## Zusatzinformations-Test

Nicht nur `E[R|P,S]` ansehen, sondern prüfen, ob `P` über `S` hinaus Information liefert.

## 19.1 Filter als Messinstrument, nicht als Marktbeweis

Ein Regime-, State- oder Kontextfilter operationalisiert eine Einteilung. Er
beweist nicht, dass der Markt einen buchstäblich realen verborgenen Zustand mit
dem vergebenen Namen besitzt. Für die Beurteilung werden festgehalten:

- der genaue Zweck des Filters,
- seine Eingangsdaten und deren Beobachtungszeitpunkt,
- zukünftige Zielgrößen, die nicht bereits in seiner Berechnung stecken,
- ein Vergleich mit den kontinuierlichen Eingangsgrößen oder einer einfachen
  Regel ohne Filter,
- und der Claim, der bei fehlender Trennleistung tatsächlich betroffen ist.

Der Anteil `Range`, `Trend` oder einer anderen Klasse ist für sich weder ein
gutes noch ein schlechtes Zeichen. Entscheidend ist, ob die feste Einteilung für
ihren erklärten Zweck zusätzliche Information über späteres Verhalten liefert.
Auch dann bleibt der Befund prädiktiv; er identifiziert weder Akteur noch
Mechanismus.

## 19.2 Konstruktionsabhängigkeiten

Trigger, Filter, Ziel und Outcome werden auf gemeinsame Rohinputs,
Berechnungsfenster und deterministische Transformationen zurückgeführt.
Mathematische Kopplung kann Assoziationen erzeugen, wenn zwei Größen gemeinsame
Bestandteile besitzen. Deterministisch abgeleitete Größen können dafür als
eigene Knoten in einer DAG dargestellt werden. Die Diagnose beantwortet nur,
woher ein statistischer Zusammenhang teilweise stammen kann; sie ist weder
Kausalbeleg noch automatische Widerlegung.

Geeignete Werkzeuge:

- strukturelle Abhängigkeitskarte vor Datenanalyse,
- neutrale oder strukturtreue Simulation, um den allein durch die Konstruktion
  erwartbaren Zusammenhang sichtbar zu machen,
- getrennte Interpretation des verbleibenden empirischen Anteils.

Methodische Anker:

- Archie, *Mathematic coupling of data: a common source of error*,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC1345065/>.
- Tennant et al., *Depicting deterministic variables within directed acyclic
  graphs*, <https://academic.oup.com/aje/article/194/2/469/7698093>.

## 19.3 Empfindlichkeit gegenüber vertretbaren Definitionen

Wenn mehrere Definitionen **vorab fachlich als zulässig** anerkannt wurden,
kann eine Spezifikationskurve oder Multiversum-Analyse zeigen, ob die Aussage
über diese Übersetzungen stabil bleibt. Das Verfahren entdeckt keine wahre
Definition und keine unbekannte Voraussetzung. Es zeigt, welche
Operationalisierungsentscheidungen das Ergebnis tragen.

- Simonsohn, Simmons und Nelson, *Specification Curve Analysis*,
  <https://www.nature.com/articles/s41562-020-0912-z>.
- Steegen et al., *Increasing Transparency Through a Multiverse Analysis*,
  <https://stat.columbia.edu/~gelman/research/published/multiverse_published.pdf>.

## 19.4 Interpretierbare Bedingungserzeugung

Sind plausible Statevariablen vorhanden, aber ihre Wechselwirkungen oder
Schwellen unbekannt, darf Discovery gezielt neue Bedingungshypothesen erzeugen.
Bevorzugt werden zunächst interpretierbare Verfahren:

- modellbasierte rekursive Aufteilung: prüft, bei welcher Variable ein
  Modellparameter instabil wird, teilt dort und wiederholt dies innerhalb der
  entstehenden Gruppen;
- Conditional-Inference-Trees: reduzieren die bekannte Bevorzugung von
  Variablen mit vielen möglichen Trennpunkten;
- Generalized Random Forests nur ergänzend bei vielen Kandidaten und genügend
  Fällen. Ohne identifiziertes Treatment werden ihre Ergebnisse prädiktiv, nicht
  kausal bezeichnet.

Ein datenbasiert erzeugter Split oder Schwellenwert ist ein neuer
`PERFORMANCE_MODIFIER`, keine nachträglich gefundene Quellenregel.

Methodische Anker:

- Zeileis, Hothorn und Hornik, *Model-based Recursive Partitioning*,
  <https://www.zeileis.org/papers/Zeileis%2BHothorn%2BHornik-2008.pdf>.
- Hothorn, Hornik und Zeileis, *Unbiased Recursive Partitioning*,
  <https://www.zeileis.org/papers/Hothorn%2BHornik%2BZeileis-2006.pdf>.
- Athey, Tibshirani und Wager, *Generalized Random Forests*,
  <https://www.gsb.stanford.edu/faculty-research/publications/generalized-random-forests>.

## 19.5 Bedingte Prognosefähigkeit und Wiederkehr

Die praktische Frage lautet nicht nur, welche Variante durchschnittlich besser
war, sondern ob Information, die im Entscheidungszeitpunkt vorlag, erkennen
ließ, wann sich die Prognoseleistung änderte. Dafür ist ein Test bedingter
Prognosefähigkeit geeignet. Eine anschließende Fluktuationsanalyse betrachtet
den gesamten Zeitpfad der relativen Leistung und verhindert, dass ein
Gesamtdurchschnitt zeitliche Instabilität verdeckt.

- Giacomini und White, *Tests of Conditional Predictive Ability*,
  <https://onlinelibrary.wiley.com/doi/10.1111/j.1468-0262.2006.00718.x>.
- Giacomini und Rossi, *Forecast Comparisons in Unstable Environments*,
  <https://onlinelibrary.wiley.com/doi/10.1002/jae.1177>.

Invarianz über vorab definierte Märkte, Instrumente oder Sessionumgebungen kann
die Wiederkehr eines Zusammenhangs stützen. Sie wird ohne die jeweils nötigen
Identifikationsannahmen nicht als universeller Kausalitätstest bezeichnet.

## 19.6 Negativkontrollen und notwendige Bedingungen

Negativkontrollen können eine vermutete oder unerwartete Verzerrungsquelle
sichtbar machen, wenn Exposition oder Outcome nach dem behaupteten Mechanismus
nicht reagieren sollten. Sie sind Diagnostik und erzeugen allein keine
Erfolgsbedingung.

- Lipsitch, Tchetgen Tchetgen und Cohen, *Negative Controls: A Tool for
  Detecting Confounding and Bias in Observational Studies*,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/>.

Necessary Condition Analysis kann explorativ nach einer Bedingung suchen, ohne
die ein hohes Outcome nicht auftritt. Weil „ohne X garantiert kein Erfolg“ in
verrauschten kurzfristigen Märkten eine besonders starke Aussage ist, ist sie
kein Default. Sie benötigt eine eigene Begründung und wird nicht aus einer
leeren Ecke im Streudiagramm allein als Marktgesetz ausgegeben.

- Dul, *Necessary Condition Analysis*,
  <https://repub.eur.nl/pub/90024/>.

---

# 20. Kostenmodellierung

## Phase 0

Konservative grobe Kostenhürde für wirtschaftliche Machbarkeit.

Die Sicherheitsmarge ist als zusätzlicher Betrag oder als eindeutig bezeichnete Gesamtschwelle zu dokumentieren. Ein Multiplikator muss unterscheiden zwischen `Gesamthürde = M × Kosten` und `Sicherheitsmarge = M × Kosten`; einen universellen Multiplikator gibt es nicht.

## Strategy Engineering

Detailliertes Modell, gegebenenfalls:

\[
Kosten=f(State,Volatilität,Liquidität,Größe,Geschwindigkeit,Session,Execution)
\]

## Besonders prüfen

- Breakouts,
- News,
- schnelle Märkte,
- illiquide Zeitfenster,
- Market Orders,
- größere Size.

Ein fixes Slippage-Modell ist nur zulässig, wenn die Daten zeigen oder die Anwendung plausibel macht, dass State-Abhängigkeit vernachlässigbar ist.

---

# 21. Prerequisite Tree / Transition Tree

## Anwenden wann

Nach empirischer Phänomen-Validation, wenn reale Umsetzungsprobleme strukturiert werden müssen.

Eine knappe Effect-Cause-Effect-Map darf bereits in Discovery als optionaler Hypothesengenerator verwendet werden; dafür gelten die Regeln in Abschnitt 25.10. Prerequisite und Transition Tree bleiben dagegen Werkzeuge für reale Umsetzungsengpässe nach der Phänomen-Validation.

## Prerequisite Tree

Frage:

> Welche Hindernisse verhindern eine ausführbare Strategie, und welche Zwischenziele sind notwendig?

## Transition Tree

Frage:

> Welche konkrete Folge von Aktionen führt von der validierten Idee zur überprüften Umsetzung?

## Nicht verwenden für

Beweis eines Markt-Edges.

Auch ein korrekt identifiziertes Implementation Constraint beweist keinen Marktmechanismus. Es zeigt nur, was die Ausführbarkeit der bereits validierten Idee begrenzt.

---

# 22. Evaporating Cloud

## Optional anwenden wenn

ein echter Zielkonflikt besteht, zum Beispiel:

- früher Entry versus bestätigter Entry,
- strenger Filter versus ausreichende Tradefrequenz.

## Zweck

Annahmen hinter dem Konflikt sichtbar machen und neue testbare Hypothesen erzeugen.

## Nicht verwenden als

Evidenz für die daraus entstehende Lösung.

---

# 23. Vorhersage-Liste

## Pflicht vor Freeze

Jede Candidate Hypothesis soll zusätzliche Konsequenzen erzeugen.

Beispielstruktur:

```text
Wenn H wahr ist,
dann sollte neben dem Discovery-Muster auch Y auftreten,
insbesondere unter State Z,
aber nicht unter Kontrollbedingung C.
```

Je unabhängiger die Konsequenz von der Discovery-Beobachtung ist, desto informativer ist ihr Scheitern oder Bestehen.

---

# 24. Pre-Mortem

## Pflicht vor Freeze

Annahme:

> Das Research-Ergebnis wird später als falsch oder unbrauchbar entlarvt.

Dann Gründe sammeln und jeden relevanten Grund übersetzen in:

- Check,
- Guardrail,
- Gegenhypothese,
- Ablehnungskriterium.

Ein Pre-Mortem ohne operative Konsequenz ist nur Pessimismus mit Tabellenformat.

---

# 25. Kausale Claims, Event-Schocks und Reaktionsinnovationen

## 25.1 Claim-Router

Vor jeder Methodenauswahl wird die Frage klassifiziert:

Der Router klassifiziert die Zielabfrage, nicht den Formalismus. Graphische
SCMs/DAGs, Potential Outcomes und strukturell-ökonometrische Designs sind
zulässige explizite Darstellungen; keine davon ist für sich ein Beweis oder eine
höhere Claim-Stufe.

### `ASSOCIATIONAL_PREDICTIVE`

Ziel ist eine bedingte Verteilung, Prognose oder handelbare Entscheidung unter beobachteten Bedingungen. Ein kausales Estimand ist nicht erforderlich. Das Identifikationsgate lautet `NOT_REQUIRED_PREDICTIVE`; kausale Sprache und `do(·)` bleiben unzulässig.

### `INTERVENTIONAL`

Ziel ist die Wirkung eines Eingriffs oder eines als strukturell identifizierten Schocks. Treatment/Schock, Outcome, Population, Horizont, Kontrast und Total-/Direkt-/Mediationseffekt müssen vor der Schätzung feststehen.

### `COUNTERFACTUAL`

Ziel ist eine Aussage über denselben konkreten Fall unter einer nicht eingetretenen Intervention. Diese Ebene verlangt ein explizites Strukturmodell und in der Regel stärkere Annahmen als ein durchschnittlicher Interventionseffekt.

Ein Research-Projekt darf zwei getrennte Zielgrößen führen, beispielsweise einen identifizierten durchschnittlichen Eventeffekt und daneben ein prädiktives Trading-Signal. Ihre Evidenz und Endentscheidungen werden getrennt berichtet.

## 25.2 Explizites Identifikationsmodell und Gate

### Pflichtreihenfolge bei kausalem Claim

1. Kausales Estimand definieren.
2. Ein SCM/DAG, Potential-Outcomes-Design, strukturell-ökonometrisches oder
   anderes explizites Identifikationsmodell formulieren.
3. Jede Kante, jedes ausgelassene gemeinsame Elternteil oder – bei
   Potential Outcomes – Konsistenz, Positivity, Assignment/Exchangeability und
   Interferenz beziehungsweise Exposure Mapping als Annahme dokumentieren.
4. Identifikationsstrategie und zulässigen Adjustmentsatz oder die vergleichbare
   Designrestriktion aus dem Modell ableiten.
5. Testbare Implikationen, Negativkontrollen, Placebos und Sensitivitäten festlegen.
6. Erst danach einen geeigneten Schätzer wählen.

Für eine tatsächlich benötigte Graph- und Adjustierungsprüfung werden primär
`pgmpy` oder `DoWhy` verwendet. Ein DAG ist nicht zusätzlich Pflicht, wenn ein
Potential-Outcomes- oder anderes explizites Design das Estimand unter vollständig
dokumentierten Annahmen identifiziert. Das vom Tool akzeptierte Modell ist
weiterhin eine Eingabeannahme; eine erfolgreiche API-Abfrage bestätigt nicht die
Wahrheit des Modells.

Beobachtungsdaten und Conditional-Independence-Strukturen identifizieren ohne Zusatzannahmen häufig nur eine Äquivalenzklasse. Zusätzliche Orientierung kann etwa aus Interventionen, Zeitrestriktionen, nicht-gaussianischen/additiven Strukturannahmen oder Invarianz über Umgebungen kommen. Diese Annahmen werden nicht durch gute Prognosegüte ersetzt.

### Gate

- Estimand aus dokumentiertem Strukturmodell identifizierbar und designspezifische Annahmen/Diagnosen vollständig → `PASS`.
- Rein prädiktive Frage → `NOT_REQUIRED_PREDICTIVE`.
- Behaupteter kausaler Effekt unter den zugelassenen Modellen nicht identifizierbar oder Kernannahme widerlegt → `FAIL`.
- notwendige Information oder Diagnose fehlt → `BLOCKED`.

`FAIL` oder `BLOCKED` verbietet den kausalen Claim. Eine neue prädiktive Version darf die Beziehung weiter untersuchen, ohne die vorhandenen Daten wieder als unabhängig auszugeben.

## 25.3 Granger, Conditional Independence und Causal Discovery

### Granger

Granger-Analyse prüft, ob die Vergangenheit von `X` die Prognose von `Y` relativ zu einem festgelegten Informationssatz verbessert. Das Ergebnislabel lautet `PREDICTIVE_PRECEDENCE`.

Zu dokumentieren sind mindestens:

- Informationssatz,
- Lag-Auswahl,
- Stationaritäts-/Stabilitätsbehandlung,
- Autokorrelation und Innovationsdiagnostik,
- Gleichzeitigkeit innerhalb der Zeitauflösung,
- Multiple Testing,
- mögliche gemeinsame unbeobachtete Treiber.

Ein positives Ergebnis ist weder eine gültige Intervention noch ein Ausschluss von Confounding.

### Causal Discovery

PC-/FCI-, score-basierte, additive-noise-, Invarianz- und PCMCI-artige Verfahren dürfen Kandidaten erzeugen oder Kanten ausschließen. Der Agent dokumentiert algorithmusspezifisch:

- kausale Markov-/Faithfulness-Annahmen,
- kausale Suffizienz oder Modellierung latenter Confounder,
- Stationarität oder Definition der Umgebungen,
- Zeitauflösung und maximale Lags,
- funktionale Form,
- Qualität und Power der Conditional-Independence-Tests,
- Messfehler und Selektionsmechanismus,
- ausgegebene Äquivalenzklasse beziehungsweise unorientierte Kanten.

PCMCI+ ist beispielsweise für lagged und contemporaneous Beziehungen in autokorrelierten Zeitreihen entwickelt, seine grundlegende Konsistenzaussage gilt jedoch unter den im Verfahren gesetzten Annahmen und nicht als universeller Wahrheitsbeweis.

Für PCMCI-/PCMCI+-artige Analysen ist `Tigramite` die primäre spezialisierte Implementierung. Conditional-Independence-Test, `tau_max`, Link-Annahmen, Umgang mit latenten Confoundern, Signifikanz-/Multiplicity-Regel und ausgegebener Graphstatus werden protokolliert. Das Ergebnis bleibt `CAUSAL_HYPOTHESIS`, solange das Identifikationsgate nicht unabhängig bestanden ist.

## 25.4 Double/debiased Machine Learning

DML reduziert Regularisierungs- und Overfitting-Bias bei der Schätzung niedrigdimensionaler Zielparameter durch Neyman-orthogonale Scores und Cross-Fitting. Es identifiziert den Zielparameter nicht selbst.

Vor DML müssen deshalb feststehen:

- das kausale Estimand,
- die Identifikationsannahme, zum Beispiel Unconfoundedness oder eine gültige IV-Struktur,
- der zulässige Covariate-Satz,
- Overlap/Positivity beziehungsweise Instrumentrelevanz,
- die Abhängigkeits- und Splitlogik.

Die Standardtheorie darf nicht ungeprüft mit zufälligem IID-Cross-Fitting auf autokorrelierte Marktzeitreihen übertragen werden. Zeitliche Blöcke, Purging/Embargo, Clusterstruktur und eine dazu passende Inferenz oder Simulation sind erforderlich.

Ein hoher DML-Schätzwert bei ungeklärtem Confounding bleibt ein präzise geschätzter Wert unter ungeklärten Annahmen, kein reparierter Kausalclaim.

Für die Implementierung wird je Estimand **eine** primäre Bibliothek gewählt: `EconML` bei CATE-/Causal-Forest- oder flexiblen DML-Aufgaben, `DoubleML` bei einem von dessen formalen Modellklassen abgedeckten DML-Design. Beide parallel einzusetzen ist nur als vorab definierte Replikation sinnvoll. `DoWhy` kann Identifikation und Refutation orchestrieren; die konkrete DoWhy–EconML-Versionskombination muss wegen möglicher API-Inkompatibilitäten separat getestet werden. Das Paket `causalinference` ist nur für seinen engen binären Matching-/Propensity-/Weighting-Bereich vorgesehen und nicht der allgemeine DML-Default.

## 25.5 High-Frequency-Eventdesign

### Surprise statt Rohwert

Für geplante Veröffentlichung `A_t` wird die neue Information relativ zur vor dem Event verfügbaren Erwartung definiert:

\[
S_t=\frac{A_t-E_{t^-}[A_t]}{q}.
\]

Wenn eine Veröffentlichung mehrere Informationsdimensionen enthält, wird `S_t` durch einen kleinen Faktorvektor `F_t` ersetzt. Bei FOMC-Events zeigen hochfrequente Studien beispielsweise, dass ein einzelner Target-Faktor nicht genügt und zusätzlich ein Path-Faktor benötigt wird. Das rechtfertigt keinen universellen Zwei-Faktor-Default: Faktorzahl, Inputkontrakte, Rotation, Orthogonalisierung, Vorzeichen und ökonomische Interpretation werden eventklassenspezifisch auf Development-Daten festgelegt.

Pflichtfelder:

- offizielle Release-Zeit und Zeitzone,
- Echtzeit-Vintage des veröffentlichten Werts,
- Erwartungsquelle, Stichprobe, Aggregationsregel und Zeitstempel,
- vorab fixierte Skalierung `q`,
- exakte Preisquellen und Synchronisierung,
- primäres und sekundäres Eventfenster,
- überlappende Veröffentlichungen und sonstige Nachrichten,
- Regeln für Ausfälle, Revisionen, Illiquidität und Ausreißer.

Eine enge Zeitspanne verbessert die zeitliche Isolation, garantiert jedoch weder Exogenität noch einen einzelnen strukturellen Schock. Wenn die gemessene Surprise aus pre-event Information vorhersagbar ist, muss die Konsequenz für Exogenität dokumentiert und gegebenenfalls eine vorab definierte Orthogonalisierung geprüft werden.

Bei Zentralbankevents werden mindestens folgende konkurrierende Komponenten erwogen:

- reine Policy-Überraschung,
- Information über den wirtschaftlichen Ausblick,
- Risk-Premium-/Kommunikationsschock,
- gleichzeitig eintreffende Fremdnachricht.

Eine Vorzeichenzerlegung mehrerer Assetreaktionen ist selbst eine Identifikationsstrategie mit Annahmen und wird nicht als beobachtete Wahrheit behandelt.

## 25.6 Erwartete Reaktion versus tatsächliche Reaktion

Für jedes Asset oder Kettenglied `j` wird ein nur mit zeitlich zulässigen Daten trainiertes Modell verwendet. Mit mehreren Surprise-Faktoren und pre-event States lautet die allgemeine Form:

\[
\widehat R_{j,t,h}=\widehat m_{j,h}(F_t,C_t,F_t\otimes C_t;\mathcal D_{<t}),
\]

\[
u_{j,t,h}=R_{j,t,h}-\widehat R_{j,t,h},
\qquad
z_{j,t,h}=\frac{u_{j,t,h}}{\widehat\sigma_{j,t,h}}.
\]

`C_t` enthält ausschließlich vor dem Event bekannte Zustände. `\widehat\sigma_{j,t}` stammt aus einem eingefrorenen und OOS kalibrierten Unsicherheitsmodell. Wird stattdessen `Expected − Actual` verwendet, ändert sich nur das Vorzeichen; die Konvention wird vor Freeze festgelegt.

### Mindestdiagnostik

- OOS-Kalibrierung von Mittelwert und Prognoseintervallen,
- Verteilung, Heavy Tails und Autokorrelation von `u`/`z`,
- Sensitivität gegenüber Eventfenster und Pre-event States gemäß Freeze,
- concurrent-news- und Liquiditätskontrollen,
- Leave-one-event/leave-one-cluster-out,
- Multiple Testing über Assets, Kettenglieder, Horizonte und States.

Für einen Vektor von Kettengliedern kann vorab eine gemeinsame Anomaliegröße definiert werden:

\[
Q_t=u_t^\top\widehat\Sigma_t^{-1}u_t.
\]

Gewichte, Regularisierung von `\widehat\Sigma_t`, Referenzverteilung und Schwellen werden auf Development-Daten eingefroren. Ein nachträglich gewähltes auffälliges Kettenglied ist Multiple Testing.

Eine gemeinsame Anomaliegröße ist optional und nicht der Default. Häufig sind getrennte, einfach interpretierbare Response-Gleichungen mit vorab festgelegten Horizonten ausreichend. Für unmittelbare Reaktionen werden High-Frequency-Eventregressionen bevorzugt; Local Projections sind eine mögliche Erweiterung für mehrere spätere Horizonte. VAR-/SVAR-, Change-Point- oder ML-Modelle benötigen eine konkrete Zusatzfrage und nachgewiesenen inkrementellen OOS-Nutzen.

### Zulässige Interpretation

Ein großes `|z|` oder `Q` bedeutet zunächst:

- schlechte Kalibrierung,
- ungewöhnliche Reaktion,
- ausgelassene Nachricht oder Statevariable,
- Liquiditäts-/Positionierungseffekt,
- Parameterdrift,
- oder erst als weitere Möglichkeit einen veränderten Mechanismus.

Das zulässige Label lautet `REACTION_INNOVATION` oder `REACTION_ANOMALY`. `CAUSAL_CHAIN_BREAK` ist nur bei einem identifizierten Ketten-/Mediationsmodell und bestandenem vorab definiertem Test zulässig.

## 25.7 Mediation und post-treatment Variablen

Bei einer Kette wie

`Schock → 2Y Yield → Dollar/Equity`

sind die Zwischenreaktionen post-treatment Mediatoren. Für den Total-Effekt des Schocks auf Equity werden sie nicht wie gewöhnliche pre-treatment Confounder kontrolliert. Wer direkten und vermittelten Effekt trennen will, definiert ein eigenes Mediationsestimand und dokumentiert die zusätzlichen Annahmen, insbesondere Confounding zwischen Mediator und Outcome.

Für reine Prognose darf eine bereits beobachtete Zwischenreaktion zur Prognose eines späteren Kettenglieds verwendet werden. Das resultierende Signal bleibt prädiktiv, sofern kein separates Mediationsdesign besteht.

## 25.8 Validation, Backtest und Monitoring

### Getrennte Entscheidungen

1. **Identifikation:** Ist der behauptete kausale Parameter unter den festgelegten Annahmen identifiziert?
2. **Schätzung:** Wie groß und unsicher ist er?
3. **Prognose:** Ist die Reaktion auf wirklich neuen Daten kalibriert und stabil?
4. **Trading:** Liefert die Reaktionsinnovation inkrementelle Netto-Performance nach Kosten?

Ein Backtest kann Punkt 4 stützen und OOS-Prognosen können Punkt 3 stützen. Beides entscheidet Punkt 1 nicht rückwirkend.

Live werden Surprise-Verteilung, Modellkalibrierung, `u`/`z`, Eventkontamination und Reaktionskoeffizienten überwacht. Eine Überschreitung vorab definierter Schwellen löst Diagnose, Revalidierung oder Suspendierung aus; das System benennt die Ursache nicht automatisch.

## 25.9 Rolle eines LLM

### Zulässig

- Kandidaten für Mechanismen, DAGs, Confounder, Instrumente und Negativkontrollen sammeln,
- alternative Erklärungen und Falsifikationen formulieren,
- Annahmen explizieren,
- Literatur und Datendokumentation strukturieren,
- Code- und Pipeline-Konsistenz prüfen.

### Unzulässig

- Pfeile anhand sprachlicher Plausibilität bestätigen,
- Instrument-Exclusion oder Unconfoundedness behaupten, weil sie „vernünftig“ klingt,
- ein Discovery-Verfahren als Oracle behandeln,
- p-Werte, Backtests oder DML als Ersatz für Identifikation ausgeben,
- eine ungewöhnliche Reaktion automatisch zum handelbaren Regime- oder Kausalbruch erklären.

## 25.10 Constraint- und Lever-Labels

Für Markttransmission sind DAG, Alternativerklärungen, Surprise-Faktoren und
Response-Gleichungen der direkte Standardpfad. Es gibt keine vorgelagerte
Goldratt-/ECE-Pflicht.

Die vier zulässigen Labels werden in
`schemas/constraint_assessment.schema.json` gespeichert:

- `TRANSMISSION_DIAGNOSTIC`: deskriptiver Pass-through oder Residualbefund.
- `INFORMATION_BOTTLENECK_CANDIDATE`: rechtzeitig beobachtbare Innovation mit vorab eingefrorenem inkrementellem OOS-Wert.
- `IDENTIFIED_CAUSAL_LEVER`: Interventions-/Mediationsestimand und Identifikationsgate bestanden.
- `IMPLEMENTATION_CONSTRAINT`: belegter Daten-, Timing-, Liquiditäts-, Kosten- oder Prozessengpass nach Phänomen-Validation und Umsetzbarkeitsprüfung.

Ein großer Koeffizient, ein ungewöhnliches Residuum oder OOS-Prognosewert genügt
nicht für einen Kausal- oder Constraint-Status. Wenn ein einfacher M0/M1-Vergleich
die Zusatzinformation nicht bestätigt, wird das Glied verworfen.

Goldratts Fokuslogik darf ausschließlich nach Phänomen-Validation optional zur
Priorisierung mehrerer bereits belegter `IMPLEMENTATION_CONSTRAINT`-Kandidaten
dienen. Sie erzeugt kein Label, kein Estimand und keinen Gate-Status.

## 25.11 Wissenschaftliche Grundlage

Primärquellen für die in diesem Abschnitt verwendeten Grenzen und Verfahren:

- Judea Pearl et al., *Probabilistic and Causal Inference: The Works of Judea Pearl* – Kausalhierarchie, DAGs und Identifikation per do-calculus: <https://ftp.cs.ucla.edu/pub/stat_ser/ACMBook-published-2022.pdf>
- Guido Imbens (2020), *Potential Outcome and Directed Acyclic Graph Approaches to Causality: Relevance for Empirical Practice in Economics* – Vergleich und Übersetzbarkeit der beiden Kausaltraditionen: <https://www.nber.org/papers/w26104>
- Dominik Janzing, Lenon Minorics und Patrick Blöbaum (2020), *Feature Relevance Quantification in Explainable AI: A Causal Problem* – Grenzen rein beobachtungsbasierter Feature-Relevanz für kausale Aussagen: <https://proceedings.mlr.press/v108/janzing20a.html>
- C. W. J. Granger (1969), *Investigating Causal Relations by Econometric Models and Cross-spectral Methods*: <https://doi.org/10.2307/1912791>
- Jonas Peters et al. (2014), *Causal Discovery with Continuous Additive Noise Models* – Identifikation nur unter zusätzlicher Struktur: <https://jmlr.org/papers/v15/peters14a.html>
- Jonas Peters, Peter Bühlmann und Nicolai Meinshausen, *Causal inference using invariant prediction*: <https://arxiv.org/abs/1501.01332>
- Jakob Runge (2020), *Discovering contemporaneous and lagged causal relations in autocorrelated nonlinear time series datasets* – PCMCI+: <https://proceedings.mlr.press/v124/runge20a.html>
- Victor Chernozhukov et al. (2018), *Double/debiased machine learning for treatment and structural parameters*: <https://academic.oup.com/ectj/article/21/1/C1/5056401>
- DoWhy User Guide – Modellierung, Identifikation, Schätzung und Refutation: <https://www.pywhy.org/dowhy/v0.14/user_guide/>
- pgmpy Causal Identification Guide – Identifikation und Prüfung von Adjustmentsätzen: <https://pgmpy.org/guides/causal_identification.html>
- EconML Documentation – DML- und CATE-Schätzer: <https://econml.azurewebsites.net/>
- DoubleML User Guide – orthogonale Scores, Cross-Fitting und unterstützte Designs: <https://docs.doubleml.org/stable/guide/guide.html>
- Tigramite Documentation – PCMCI/PCMCI+ und zeitserienspezifische Conditional-Independence-Tests: <https://jakobrunge.github.io/tigramite/>
- Causalinference Documentation – enger Funktionsumfang für Propensity, Matching, Blocking, Weighting und Least Squares: <https://causalinferenceinpython.org/>
- John Cochrane und Monika Piazzesi (2002), *The Fed and Interest Rates – A High-Frequency Identification*: <https://www.aeaweb.org/articles?id=10.1257/000282802320189069>
- Roberto Rigobon und Brian Sack (2002), *The Impact of Monetary Policy on Asset Prices* – Endogenität und Identifikation über Heteroskedastizität: <https://www.federalreserve.gov/econres/feds/the-impact-of-monetary-policy-on-asset-prices.htm>
- Marek Jarociński und Peter Karadi (2020), *Deconstructing Monetary Policy Surprises—The Role of Information Shocks*: <https://www.aeaweb.org/articles?id=10.1257%2Fmac.20180090>
- Michael Bauer und Eric Swanson (2022/2023), *A Reassessment of Monetary Policy Surprises and High-Frequency Identification* – Vorhersagbarkeit aus pre-event Information: <https://www.nber.org/papers/w29939>
- T. Niklas Kroner (2025), *How Markets Process Macro News: The Importance of Investor Attention* – zeitvariable CPI-Reaktionsstärke: <https://www.federalreserve.gov/econres/feds/how-markets-process-macro-news-the-importance-of-investor-attention.htm>
- Refet Gürkaynak, Brian Sack und Eric Swanson (2004/2005), *Do Actions Speak Louder Than Words?* – Target- und Path-Faktoren statt eines eindimensionalen FOMC-Schocks: <https://www.federalreserve.gov/econres/feds/do-actions-speak-louder-than-words-the-response-of-asset-prices-to-monetary-policy-actions-and-statements.htm>
- Torben Andersen, Tim Bollerslev, Francis Diebold und Clara Vega (2006), *Real-Time Price Discovery in Global Stock, Bond and Foreign Exchange Markets* – standardisierte News und dynamische Cross-Asset-Response-Gleichungen: <https://www.federalreserve.gov/econres/ifdp/real-time-price-discovery-in-global-stock-bond-and-foreign-exchange-markets.htm>
- Linda Goldberg und Christian Grisse (2013), *Time Variation in Asset Price Responses to Macro Announcements* – zustands- und zeitabhängige Reaktionskoeffizienten: <https://www.nber.org/papers/w19523>
- Òscar Jordà (2005), *Estimation and Inference of Impulse Responses by Local Projections* – horizon-spezifische Impulsantworten als robuste Alternative zu vollständig spezifizierten VARs: <https://www.aeaweb.org/articles?id=10.1257%2F0002828053828518>
- James Stock und Mark Watson (2018), *Identification and Estimation of Dynamic Causal Effects in Macroeconomics Using External Instruments* – Relevanz- und Exogenitätsbedingungen für strukturelle dynamische Effekte: <https://www.nber.org/papers/w24216>

Diese Quellen rechtfertigen keine konkrete Trading-Edge. Sie begründen die methodischen Schranken und die Pflicht, Identifikation, Prognose und Handelsnutzen getrennt zu prüfen.

---

# 25a. Mechanismenbasierte Ideenerzeugung

Dieser Abschnitt wird nur aktiviert, wenn neue Intraday- oder kurze Swing-Ideen
erzeugt werden sollen. Er ist kein Teil des nachgelagerten Screenings.

Der ausführbare Producer unter `scripts/generate_hypotheses.py` liest
`generation/mechanism_catalog.v1.json`. Jeder Katalogeintrag enthält
Mechanismusgeschichte, mögliche Akteure oder Regeln, erwartete Handlungen,
beobachtbare Signaturen, natürliche Phasen, alternative Observablen,
Widerspruchshypothesen, Verbindungstags, Primärquellen und einen expliziten
`entry_origin`. Interne Beobachtungen dürfen den Katalog nur über stabile
Beobachtungs- oder Journalreferenzen erweitern.

Die Grundgrammatik lautet:

```text
Mechanismus × Phase × beobachtbare Reaktion → ungescreenter INBOX-Candidate
```

Aus derselben Quelle werden unterschiedliche Kandidaten erzeugt:

- `PHASE_PATH`: Antizipation, aktive Phase, Absorption, Transmission,
  Erschöpfung oder Unwind,
- `EXPECTATION_VIOLATION`: der erwartete Abdruck bleibt aus oder kehrt sich um;
  daraus entsteht eine separate Hypothese über Absorption, einen konkurrierenden
  Flow, einen anderen Übertragungspfad oder eine Zustandsänderung,
- `MECHANISM_CONNECTION`: zwei Mechanismen teilen einen Takt, Venue, Flow,
  Hedge-Pfad oder Payoff,
- `ASSUMPTION_RELAXATION`: der Abdruck wird von Preisrichtung auf Tiefe, Spread,
  Basis, Volumen, Volatilität, Timing oder ein verknüpftes Instrument verlagert.

Die Akteursfrage ist eine produktive Route, aber keine allgemeine
Zulassungsbedingung. Sie passt besonders zu Rolls, Auktionen, Verfall,
Benchmarking, Hedging, Funding und Liquidationen. Orderbuchzustände,
Instrumentenverknüpfungen und Clock-Time-Wiederholungen dürfen ohne eindeutig
identifizierten gezwungenen Akteur erzeugt werden.

Nicht Bestandteil dieser Methode sind Portfolioallokation, langfristige
Faktorideen, Premortem, Validity-Labels, Ablehnungsstatistik, Noise Screen,
Backtest, Ranking oder Promotion. Diese Trennung ist in
`decisions/ADR-006-mechanism-first-hypothesis-generator.md` festgehalten.

Der Generatorlauf ist jedoch die Kandidatenuniversums-Referenz für spätere
Screens. Der nachgelagerte Entry Screen zählt jede tatsächlich datenbasiert
geprüfte Idee und verwendet die vorab fixierte Korrektur aus dem
Search-Space-Register; das macht den Screen nicht zu einem Generatoroperator.

---

# 26. Intraday-Hypothesenrouter

## 26.1 Benutzungsgrenze

Der Router ordnet Rohideen einem geeigneten ersten Prüfdesign zu. Er ist keine
abschließende Liste aller Intraday-Mechanismen und kein Beleg, dass die eingeordnete
Geschichte wahr oder handelbar ist. Jede Idee beginnt grundsätzlich mit
`ASSOCIATIONAL_PREDICTIVE`, sofern nicht ein eigenes Identifikationsdesign das
höhere Claim-Level rechtfertigt.

Vor jeder Detailanalyse werden drei Fragen getrennt:

1. Ist der behauptete Mechanismus im konkreten Markt ausreichend belegt?
2. Prognostiziert sein ex ante beobachtbarer Footprint ein zukünftiges Outcome OOS?
3. Bleibt dieser Effekt zu ausführbaren Preisen nach Kosten positiv?

Die Antworten werden unabhängig als `mechanism_supported`,
`forward_predictive_oos` und `executable_net_edge` geführt. Ein positives Ergebnis
auf einer früheren Stufe setzt keine spätere Stufe auf `SUPPORTED`.

## 26.2 Router-Matrix

| Ideenfamilie | Zulässiger Anfangsclaim | Mindestdaten und Integrität | Typische Artefakte / Alternativerklärungen | Mindestfalsifikation | Frühe Machbarkeitshürde |
|---|---|---|---|---|---|
| Limit-Orderbuch / OFI / Queue Imbalance | Ein vorab definierter Buchzustand verbessert die Prognose eines zukünftigen Quote-/Execution-Outcomes; keine automatische Kausal- oder Edge-Aussage | exaktes Instrument und Venue; Event-Feed mit Trades, Adds, Cancels und Sequenzprüfung; Book-Tiefe; Tick Size; Timestamp- und Clock-Sync; dokumentiertes Trade Signing; bekannte Hidden-Liquidity-Grenze | kontemporäre Preisreaktion statt Forward-Effekt; mechanischer Tick-Wechsel; Tageszeit, Volatilität, Tiefe; Feed-Gap; Cross-Venue-Liquidität | Event-Time und Clock-Time getrennt; inkrementell über Tiefe/Spread/Volatilität/Tageszeit; neue Daten; ausführbare Bid-/Ask-Outcomes statt nur Midquote | Feed-Auflösung und Latenz müssen kürzer als der Effekt sein; Queue-/Fill-Modell, Gebühren, Spread und Slippage dürfen `δ_econ` nicht aufzehren |
| Spread-Ausweitung | Zunächst Volatilitäts- oder Liquiditätsrisiko-Prognose; Richtung nur mit zusätzlichem ex-ante Signal | tickgenaue Quotes, Book-Tiefe, Cancels, Trades, Venue-Regeln und Tageszeit | 1→2 Ticks erscheint als „Verdopplung“; Volatilität, geringe Aktivität, Queue-Depletion, Inventory oder Adverse Selection sind nicht aus Spread allein identifizierbar | absolute Ticks und relative Änderung getrennt; Matching/Controls; inkrementeller OOS-Wert; keine Richtung aus Spread allein | der breitere Spread ist selbst Teil der Kostenhürde |
| Cross-Market / Lead-Lag | Markt A verbessert rollierend und OOS die Prognose des zukünftigen effizienten Preises von B | direkte, synchronisierte Quotes; Clock-Audit; Vertrags-/Instrument-Mapping; Futures-Basis, Dividenden, Zins und Laufzeit; Session-Overlap | stale/asynchrone Quotes, gemeinsamer Faktor, Bid-Ask-Bounce, Feed- oder Venue-Latenz; zeitvariable Führungsrichtung | A-vs.-B und B-vs.-A; rollierende Information-Share-/VECM- oder einfachere OOS-Benchmarks; Regime- und Placebotests | ausführbare Basisabweichung nach zwei Spreads, Gebühren, Latenz, Queue und Leg-Risk |
| Execution-/Metaorder-Signatur | Öffentliche Daten erlauben höchstens eine kalibrierte Metaorder-Wahrscheinlichkeit; kein sicher erkannter TWAP/VWAP | Trades und Quotes über relevante Venues; Orderzeichen; Interarrival Times; Größen; Participation Rate; Tagesvolumenkurve; möglichst Order-/Teilnehmer-IDs | Round Lots, Batching, Icebergs, Fragmentierung, mehrere Akteure, adaptive/randomisierte Algorithmen | Klassifikation gegen ein Nullmodell, das Tageszeit, Volumenkurve und Größenhäufigkeit erhält; danach separater OOS-Returntest | ohne Identifikatoren bleibt Mechanismus latent; angeblicher „Boden“ muss durch ausführbare, kostenbereinigte Returns separat belegt werden |
| Relative Value / Pairs / Kointegration | Ein vorab gebildeter Spread besitzt OOS eine stabile bedingte Mean-Reversion; Branchenähnlichkeit allein genügt nicht | point-in-time Universum; corporate-action-bereinigte synchrone Quotes; Integrationseigenschaften; geschätzter Hedge-Koeffizient; Borrow-/Short-Daten | bloße Korrelation; instabiles Beta; gemeinsamer Faktor; Earnings/Corporate Actions; Strukturbruch; Data Snooping über viele Paare | Formation und Trading strikt trennen; Unit-Root-/Cointegration-/Error-Correction-Diagnostik; Breaktests; Pair-Selection-Multiplicity; Factor-Exposure OOS | zweibeinige Fills, Leg-Risk, Spread/Slippage, Borrow, Capacity und Restfaktor-Risiko müssen in `δ_econ` eingehen |
| Derivate-Hedging / Gamma | Konditional auf Vorzeichen und Größe einer dokumentierten oder robust geschätzten Intermediärsexponierung; keine universelle Momentum-Richtung | Optionskette, Greeks/Vol-Surface, Underlying/Futures, OI/Volumen, mehrere Dealer-Side-Annahmen, Eventfilter | Open Interest identifiziert die Dealer-Seite nicht; Long Gamma kann dämpfen, Short Gamma verstärken; Trend kann Ursache statt Hedge-Folge sein | Vorzeichen-symmetrische Predictions; Sensitivität über Dealer-Side-Annahmen; Long- vs. Short-Gamma-Tage; Earnings/Makro/Indexevents filtern | Ergebnis darf nicht nur unter einer unbeobachtbaren Positionsannahme bestehen; Hedgeinstrument und Kosten müssen umsetzbar sein |
| Rebalancing / Benchmark- oder Fixed-Mix-Flow | Nur für belegte Mandate, Indexregeln oder Holdings; kein allgemeiner gesetzlicher Zwang | versionierte Benchmark-/Prospektregel; Announcement und Effective Date getrennt; Gewichtsdifferenz, Tracking-AUM/Holdings, Auction Imbalance | Antizipation, aktive Fonds, andere Corporate Events, Mittelzuflüsse, Derivate, abweichende Trackingmethoden | gematchte Kontrollen; erwarteter Flow-Querschnitt; Announcement-vs.-Effective-Fenster; Reversal/Bestandseffekt getrennt | Timing, verfügbare Auktionsliquidität, Impact, Borrow und Antizipation können Edge eliminieren |
| Session / Opening-/Closing-Auction | Venue-spezifische Änderung von Liquidität, Imbalance oder Preisverteilung; kein universelles „Power-Hour“-Muster | versionierter Venue-Kalender, Auktionstyp, Imbalance-Publikationszeiten, Zeitzone/DST/Feiertage, Continuous und Auction getrennt | simultan hohes Volumen und breite Spreads; harte lokale Uhrzeiten; Regeländerungen; Closing-Print nicht garantiert ausführbar | venue- und regimespezifische Nullmodelle; Auction/Continuous getrennt; Momentum und Reversion als konkurrierende Richtungen | Ordertyp, Cutoffs, Imbalance-Zugriff, Fill/Impact und tatsächlicher Auktionspreis |
| Crypto-Funding | Funding-, Basis-, OI- oder Volumenänderung rund um kontraktspezifischen Timestamp; keine automatische gerichtete Spotrendite | Venue, Kontrakt, Regelversion, exakter Funding-Timestamp, ex ante sichtbare Rate, Spot/Perpetual Quotes, OI/Liquidationen | Intervalle sind nicht universell acht Stunden; finalisierte Rate kann Leakage enthalten; Liquidationen oder News treiben beide Größen | Outcomes Basis/OI/Volumen primär, Spotreturn sekundär; Rate-Richtung und -Höhe; Placebo-Timestamps; Regelwechsel | Fees, Funding, Basis, Slippage, Margin, Liquidation und Venue-Risk |
| Geplantes Informationsereignis | Surprise-/Response-Claim nach §25.5; gehört zu `INFORMATION_EVENT` | Release-Zeit, point-in-time Erwartung/Vintage, Eventfeed, Kontaminationsregel | Rohwert statt Überraschung; mehrere News-Dimensionen; Fremdnachrichten | Surprise-Modell und Fenster einfrieren; Placebos/Controls; zeitlich OOS | nicht als „newsfreier“ Intraday-Mechanismus klassifizieren |
| Endogenes Preis-/Volumenereignis | Bedingte Prognose nach beobachtbarem Trigger; nicht automatisch exogener Event-Schock | Trigger-Bestätigungszeit, vollständige Pfadabhängigkeit, pre-trigger States, ausführbare Quotes | Selection on outcome, Look-ahead, Volatilitätsstate, Stop-Kaskaden nur erzählt | gematchte Nicht-Events, randomisierte/strukturtreue Trigger-Placebos, purged OOS-Test | Trigger muss live rechtzeitig feststehen; Kosten und Crowd-/Impact-Risiko |
| Overnight vs. Intraday | Zunächst Renditezerlegung, nicht Mechanismus oder Edge | offizielle und ausführbare Open-/Close-Definition, Corporate Actions, Kalender, Finanzierung/Borrow | Earnings, Makro- und sonstige Overnight-News; nicht handelbarer offizieller Print; sampleabhängige Mittelwerte | Subperioden/Märkte, Kosten und Gap-Risiko; getrennte Mechanismushypothese erforderlich | passt nicht in reinen Continuous-Intraday-Scope und trägt keine newsfreie Regel allein |

## 26.3 Datenintegrität bei sehr kurzen Horizonten

Für Orderbuch- und Lead-Lag-Ideen ist ein positiver statistischer Test unzulässig,
solange mindestens einer der folgenden Punkte materiell ungeklärt ist:

- Venue-direct versus konsolidierte Sicht,
- Sequenzlücken, Drop-/Recovery-Verhalten und Book-Rekonstruktion,
- Exchange-, Feed-, Capture- und Strategy-Clock samt Synchronisationsfehler,
- Trade-Signing-Regel und Behandlung von Cancels/Corrections,
- Tick-Size-, Lot-Size-, Auction- oder Matching-Regelversion,
- Hidden-/Iceberg-Liquidität und nicht beobachtete Venues,
- Queue-Position, Ordertyp, Fill- und Cancel-Latenz,
- sowie der Unterschied zwischen beobachtetem Midquote und ausführbarem Preis.

Fehlt die für den behaupteten Horizont nötige Auflösung, wird die Idee im Intake
`REJECTED` oder `BLOCKED`, nicht mit gröberen Daten scheinbar bestätigt.

## 26.4 Interpretationsregeln für typische Übertreibungen

- Eine OFI- oder Multi-Level-OFI-Regression auf die gleichzeitige Midprice-Änderung
  ist `mechanism_supported`-Evidenz oder Messdiagnostik, keine 5–60-Sekunden-Prognose.
- „Spread verdoppelt“ ist bei einem Wechsel von einem auf zwei Ticks kein
  universeller Informationsschock und liefert ohne Zusatzsignal keine Richtung.
- Futures führen ETFs nicht definitionsgemäß; Führungsrichtung und Stärke werden
  geschätzt und können sich nach Periode, Liquidität und Volatilität umkehren.
- Wiederkehrende Printgrößen/-abstände identifizieren weder einen bestimmten
  Algorithmus noch einen Preisboden.
- Gleiche Branche, hoher Gleichlauf oder ein 2–3-Sigma-Abstand beweisen keine
  Kointegration und keine Marktneutralität.
- Dealer-Hedging verstärkt bei negativer Netto-Gamma-Exponierung potenziell die
  Bewegung und wirkt bei positiver Exponierung potenziell entgegen; die Position
  ist meist nur proxybasiert bekannt.
- Index- oder Fixed-Mix-Flows beruhen auf konkreten Regeln und Mandaten, nicht auf
  einer universellen gesetzlichen Pflicht zum Schlusskurs.
- Fundingintervalle, Auktionszeiten und Sessions werden aus versionierten
  Venue-Regeln geladen und nicht als universelle Uhrzeiten hart codiert.

## 26.5 Primärquellen als methodische Anker

Die folgenden Arbeiten begründen einzelne Mechanismen oder Prüfgrenzen, aber keine
fertige Trading-Edge:

- Cont, Kukanov und Stoikov, *The Price Impact of Order Book Events*,
  <https://doi.org/10.1093/jjfinec/nbt003> – OFI und kontemporäre
  Kurzfrist-Preisänderungen.
- Chen, Chung und Lien, *Price Discovery in the S&P 500 Index Derivatives
  Markets*, <https://doi.org/10.1016/j.iref.2016.07.008> –
  zeit-/stateabhängige Preisfindungsbeiträge statt universeller Führungsrichtung.
- van Kervel und Menkveld, *High-Frequency Trading around Large Institutional
  Orders*, <https://doi.org/10.1111/jofi.12759> – Reaktionen auf Parent Orders sind
  dynamisch und nicht gleichbedeutend mit einem festen Preisboden.
- Engle und Granger, *Co-Integration and Error Correction*,
  <https://doi.org/10.2307/1913236> – Definition und Prüfung von Kointegration.
- Do und Faff, *Are Pairs Trading Profits Robust to Trading Costs?*,
  <https://doi.org/10.1111/j.1475-6803.2012.01317.x> – Kosten- und
  Periodenabhängigkeit historischer Pairs-Befunde.
- Baltussen et al., *Hedging Demand and Market Intraday Momentum*,
  <https://doi.org/10.1016/j.jfineco.2021.04.029> – konditionale Rolle von
  Short-Gamma-Hedging.
- Parker, Schoar und Sun, *Retail Financial Innovation and Stock Market Dynamics:
  The Case of Target Date Funds*,
  <https://doi.org/10.1111/jofi.13258> – Rebalancing klar identifizierter
  Target-Date-Fonds statt pauschaler Pensionskassenannahmen.
- Wu und Jegadeesh, *Closing Auctions: Nasdaq versus NYSE*,
  <https://doi.org/10.1016/j.jfineco.2021.12.003> – venue- und designspezifische
  Schlussauktionsbefunde.

Jede konkrete Research-Version erfasst die tatsächlich verwendete Fassung dieser
oder anderer Arbeiten zusätzlich im Academic-Source-Protokoll; diese Liste ersetzt
weder Source Verification noch Version-/Integrity-Prüfung.

---

# 27. Methoden-Matrix für AI-Agenten

| Problem | Mindestprüfung | Typische Methode |
|---|---|---|
| zu wenig Daten | Phase-0-Power/Präzision | Powerrechnung/Simulation |
| serielle Abhängigkeit | Autokorrelation/Cluster | Block-Bootstrap |
| gemeinsame Events | Eventcluster | Cluster-Bootstrap |
| überlappende Labels | Zeitfenster prüfen | Purging/Embargo |
| korrelierte Symbole | Korrelation/Faktoren | Symbol-/Faktorcluster |
| Heavy Tails | Einfluss/Verteilung | robuste Schätzer + Sensitivität |
| einzelne dominante Fälle | LOO/LOCO | Influence Diagnostics |
| viele Hypothesen | Suchraum dokumentieren | FDR |
| viele Strategien vs Benchmark | Modellfamilie | Reality Check / SPA |
| ausgewählte hohe Sharpe | Auswahlverzerrung | Deflated Sharpe |
| viele Backtest-Varianten | IS/OOS-Ranginstabilität | PBO |
| unsicherer Auswahlprozess | komplette Pipeline | Pipeline-Bootstrap |
| Pipeline findet Effekte unter Null / möglicher Timing- oder Indexierungsfehler | vollständige Pipeline auf strukturtreuen Null-/Surrogatdaten plus bekannter positiver Sentinel | Pipeline-Integritätsgate |
| knappe unabhängige Daten | Datenrollen | Holdout oder nested WF |
| Kosten variieren mit Signal | State prüfen | zustandsabhängiges Kostenmodell |
| unklarer Nutzen eines Regimefilters | zukünftige, nicht im Filter enthaltene Zielgröße + inkrementeller Vergleich | Measurement Assessment + Conditional Predictive Ability |
| Trigger und Outcome teilen Inputs oder Fenster | deterministische Herkunftskarte | Structural Dependency Map + optional neutrale Simulation |
| Ergebnis hängt möglicherweise an vertretbaren Definitionen | vorab begrenzte Definitionsfamilie | Spezifikationskurve / Multiversum |
| unbekannte beobachtbare Erfolgsmodifikatoren | interpretierbare Discovery, danach getrennte Wiederkehrprüfung | Model-based Recursive Partitioning / Conditional Inference Tree |
| Bedingung möglicherweise nur zeitweise | gesamter Zeitpfad statt Gesamtdurchschnitt | Performance Fluctuation Test |
| Bedingung soll marktübergreifend gelten | vorab definierte Umgebungen und begrenzte Interpretation | Invarianzanalyse |
| kausale Behauptung | Estimand + DAG + Identifikationsannahmen | Identifikationsgate vor Schätzerwahl |
| Granger-/Discovery-Signal | Informationssatz + Algorithmusannahmen + Äquivalenzklasse | `Tigramite` für PCMCI-artige Zeitreihen-Discovery; als Hypothesengenerator/Predictive Precedence labeln |
| hochdimensionale Confounder unter gültiger Identifikation | Overlap + Split-/Abhängigkeitsdesign | `EconML` oder `DoubleML` mit zeitlich gültigem Cross-Fitting |
| DAG-/Adjustierungsprüfung | versionierter Graph + Estimand | `pgmpy` oder `DoWhy`; Toolergebnis bestätigt nicht die DAG-Wahrheit |
| Refutation eines identifizierten Schätzers | designspezifische Placebos/Negativkontrollen/Sensitivitäten | `DoWhy` plus mindestens eine unabhängige designspezifische Prüfung |
| geplantes Makroevent | Erwartungs-Vintage + Release-Zeit + Eventfenster + Fremdnachrichten | Surprise-/High-Frequency-Eventdesign |
| Event enthält mehrere News-Dimensionen | Faktorzahl/Rotation/Interpretation vorab festlegen | kleiner Surprise-Faktorvektor statt Rohwert |
| tatsächliche Reaktion weicht ab | OOS-Kalibrierung + News-/Liquiditätskontrollen | standardisierte `REACTION_INNOVATION` |
| mehrere Kettenglieder auffällig | Kovarianz + vorab definierte Gewichte + Multiplicity | gemeinsamer `Q`-Score und leg-spezifische Diagnostik |
| direkter/vermittelter Effekt behauptet | post-treatment Rollen + Mediator-Outcome-Confounding | explizites Mediationsestimand |
| mehrgliedrige verbale Wirkungskette | End-Outcome + messbare/latente Knoten + Alternativpfade | konkurrierende DAGs und Response-Gleichungen |
| behaupteter Informationsengpass | reale Verfügbarkeit + eingefrorener M0/M1-OOS-Vergleich | `INFORMATION_BOTTLENECK_CANDIDATE` oder verwerfen |
| Strategie scheitert an Ausführbarkeit | Systemziel + belegter Daten-/Timing-/Kostenengpass | `IMPLEMENTATION_CONSTRAINT` + Prerequisite/Transition Tree |

---

# 28. Abschlussregel

Der Agent darf keine Methode als „erledigt“ betrachten, nur weil ihr Name im Bericht vorkommt.

Eine Methode ist erst erledigt, wenn dokumentiert ist:

- warum sie passt,
- wie sie parametrisiert wurde,
- welche Annahmen gelten,
- welches Ergebnis sie liefert,
- und welche Entscheidung daraus folgt.

Die Research-Pipeline selbst gilt erst als ausführbar, wenn das Pipeline-Integritätsgate vor Freeze `PASS` ist.
