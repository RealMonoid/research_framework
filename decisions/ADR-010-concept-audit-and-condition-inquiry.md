# ADR-010: Begriffsprüfung und quantitative Bedingungsanfrage

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Die Quellenrekonstruktion macht offene Definitionen sichtbar, unterschied aber
bisher nicht sauber zwischen vier Dingen: Bestandteilen der Strategie,
quellengenannten Anwendungshinweisen, nur vermuteten Erfolgsbedingungen und
vollständig unbekannten Erfolgsbedingungen. Dadurch konnten plausible
Voraussetzungen vor der Operationalisierung unbemerkt wie Tatsachen behandelt
werden.

Zudem können Trigger, Filter und Outcome gemeinsame Rohgrößen oder Fenster
verwenden. Der daraus mögliche statistische Zusammenhang ist weder automatisch
ein Marktmechanismus noch automatisch ein Fehler. Regimefilter wurden bislang
zwar als Statevariablen behandelt, aber nicht ausdrücklich als vorläufige
Messinstrumente mit begrenzter Aussage.

Schließlich fehlte eine positive Methode zur Erzeugung von
Bedingungshypothesen. Das Framework konnte bekannte Bedingungen dokumentieren,
aber nicht geregelt fragen, unter welchen beobachtbaren Umständen sich ein
Ergebnis verändert.

## Decision

1. Vor Abschluss jeder unvollständig definierten Quellenrekonstruktion erzeugt
   der `scientific-philosophy-critic` ein `strategy_concept_audit`.
2. Das Audit trennt `STRATEGY_DEFINING`, `SOURCE_STATED_APPLICATION`,
   `SUSPECTED_PERFORMANCE_MODIFIER` und `UNKNOWN_SUCCESS_CONDITION`.
3. Vermutete und unbekannte Bedingungen dürfen nicht heimlich als Pflichtfilter
   in die Quellenstrategie eingehen. Das Audit beansprucht keine Vollständigkeit.
4. Gemeinsame Inputs, Fenster und deterministische Transformationen werden als
   Konstruktionsabhängigkeiten erfasst. Sie können Assoziationen mit erzeugen
   oder die beantwortete Frage verändern, sind aber weder Kausalbeleg noch
   automatisch ein Konstruktionsfehler.
5. Regime-, State- und Kontextfilter sind vorläufige Messinstrumente. Ihre
   Klassenhäufigkeit misst keine Trennleistung. Eine Beurteilung verwendet
   zukünftiges Verhalten, das nicht bereits in der Filterkonstruktion steckt,
   und einen inkrementellen Vergleich mit kontinuierlichen Inputs oder einer
   einfachen Baseline.
6. Prognostische Trennung validiert höchstens den erklärten praktischen Zweck
   der Einteilung. Sie beweist weder einen realen verborgenen Marktzustand noch
   Akteur, Absicht, Zwang oder Kausalmechanismus.
7. Ein nicht informativer Filter entwertet den von ihm abhängigen
   Zustandsclaim. Ein davon trennbarer Ereignisclaim kann offen bleiben.
8. Fehlt für eine assoziative oder prädiktive Frage eine belastbare
   Akteurshypothese, wird der Akteursstand ausdrücklich als
   `UNSPECIFIED / NOT_CLAIMED` dokumentiert. Das verhindert eine erfundene
   Mechanismusgeschichte, ohne die engere Frage zu verbieten.
9. Nach vorläufiger Operationalisierung kann der
   `condition-inquiry-analyst` ein `condition_inquiry` für
   Konstruktionsdiagnostik, Definitionssensitivität, interpretierbare
   Bedingungserzeugung, bedingte Prognosefähigkeit oder Zeit-/Umgebungsstabilität
   anlegen.
10. Eine datenbasiert gefundene Bedingung ist eine neue
   Erfolgsmodifikator-Hypothese. Sie wird nicht rückwirkend zur Quellenregel.
11. Ein quellenfestgelegtes Ziel wird nicht unbemerkt durch ein methodisch
    unabhängigeres Ziel ersetzt. Die neue Zielgröße beantwortet eine neue Frage.
12. Necessary Condition Analysis ist nur ein begründeter explorativer
    Spezialfall, kein Default für verrauschte kurzfristige Märkte.

## Rejected Alternatives

- **Jeden plausiblen Kontext sofort als Filter aufnehmen:** verworfen, weil
  Vermutung und Quellenstrategie dadurch ununterscheidbar würden.
- **Einen Filter durch seine Klassenhäufigkeit beurteilen:** verworfen, weil
  Häufigkeit keine Trennleistung misst.
- **Prädiktiv verschiedene Filtergruppen als reale Regime behandeln:**
  verworfen; praktischer Informationswert, Ontologie und Kausalität sind
  verschiedene Aussagen.
- **Gemeinsame Fenster automatisch als Fehler behandeln:** verworfen. Die
  Abhängigkeit muss sichtbar und begrenzt interpretiert werden; ihre sachliche
  Zulässigkeit hängt von der ursprünglichen Frage ab.
- **Unabhängiges Outcome als neutrale Reparatur:** verworfen. Es kann eine
  sinnvolle neue Frage sein, ersetzt aber nicht still die Quellenbehauptung.
- **Bedingungssuche nur als weiteres Schutzgate:** verworfen. Ihr Hauptzweck ist
  die Erzeugung verständlicher, beobachtbarer und später prüfbarer
  Bedingungshypothesen.

## Consequences

- Das Framework kann unbekannte Voraussetzungen nicht vollständig entdecken,
  behauptet diese Vollständigkeit aber auch nicht mehr.
- Versteckte Annahmen werden vor der Operationalisierung sichtbar, ohne
  plausible Ideen voreilig in Tatsachen zu verwandeln.
- Statefilter können zweckbezogen beurteilt werden, ohne ihre Namen zu
  Marktontologie oder Kausalerklärung aufzuwerten.
- Quantitative Bedingungssuche wird ein Generator neuer Research-Fragen und
  bleibt von der Identität der Quellenstrategie getrennt.
- Die synthetischen Beispiele führen keinen Backtest aus und enthalten kein
  Marktergebnis.
