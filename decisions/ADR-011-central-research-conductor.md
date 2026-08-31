# ADR-011: Zentraler Forschungsleiter mit verbindlichem Spezialisten-Routing

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Das Framework besitzt spezialisierte Rollen für Ideengenerierung,
Wissenschaftsphilosophie und quantitative Bedingungsfragen. Bisher war jedoch
nicht verbindlich geregelt, wer den Gesamtfall führt, den aktuellen Stand über
mehrere Arbeitsschritte hinweg festhält und entscheidet, wann welche Rolle
eingeschaltet werden muss.

Eine bloße Rollenbeschreibung genügt dafür nicht. Ein Sprachmodell kann eine
notwendige Prüfung vergessen, Spezialisten können dieselbe Aufgabe doppelt
bearbeiten, und die Nutzerkommunikation kann in technische Einzelheiten
zerfallen. Besonders kritisch sind zwei Übergänge: die Begriffsprüfung vor der
Operationalisierung einer unvollständigen Buchstrategie und die
wissenschaftsphilosophische Fortsetzungsprüfung nach einem nicht positiven
festgeschriebenen Ergebnis.

## Decision

1. Jede nutzerbezogene Research-Aufgabe wird von genau einem
   `research-conductor` geführt. Er bleibt alleiniger Ansprechpartner des
   Nutzers und trägt die Verantwortung für den nächsten Schritt.
2. Vor jedem wesentlichen Übergang hält der Forschungsleiter den aktuellen
   Stand in einem maschinenprüfbaren Checkpoint fest.
3. Ein deterministischer Router entscheidet aus diesem bereits eingeordneten
   Stand über den nächsten zulässigen Arbeitsschritt. Das Sprachmodell ordnet
   die Bedeutung der Anfrage ein; feste Übergangsregeln werden nicht seinem
   Gedächtnis überlassen.
4. Der `scientific-philosophy-critic` ist vor der Operationalisierung
   unvollständiger Prosastrategien zwingend, sobald die Quellenrekonstruktion
   vorliegt und die Begriffsprüfung noch fehlt.
5. Derselbe Spezialist ist nach `FALSIFIED`, `PRECISE_NULL`, `INCONCLUSIVE` oder
   `INVALID_TEST` zwingend, wenn Ursachen zugerechnet, die Untersuchung
   wesentlich verändert oder empirisch fortgesetzt werden soll.
6. Der `condition-inquiry-analyst` wird erst nach einer vorläufig festgelegten
   Operationalisierung für Messgüte, Definitionsempfindlichkeit oder
   beobachtbare Erfolgsbedingungen eingesetzt.
7. Der Ideengenerator wird nur bei einem tatsächlichen Wunsch nach neuen
   kurzlaufenden Tradingideen eingesetzt. Er ist kein Ersatz für Aufnahme,
   Rekonstruktion oder Rettung einer bestehenden Idee.
8. Spezialisten arbeiten nacheinander mit einem begrenzten Auftrag und einem
   festgelegten Ausgabeformat. Sie sprechen nicht direkt mit dem Nutzer und
   ändern weder Forschungsfrage noch Quellenstrategie oder festgeschriebenes
   Ergebnis.
9. Spezialistenergebnisse werden geprüft, bevor der Forschungsleiter den Stand
   fortschreibt. Ein fehlender oder ungültiger Pflichtbeitrag blockiert den
   Übergang; er wird nicht stillschweigend vom Hauptagenten simuliert.
10. Eine Routingentscheidung erlaubt weder automatisch Datenzugriff noch einen
    Backtest. Empirische Arbeit benötigt weiterhin einen gesonderten Auftrag
    und die dafür geltenden Voraussetzungen.
11. Für Codex und kompatible Agenten ist `AGENTS.md`, für Claude zusätzlich
    `CLAUDE.md` der verbindliche Einstieg in diese Steuerung.
12. Vor und nach jeder Fachagenten-Übergabe auf einem bestehenden Fall werden
    Forschungsfrage, Strategie, Markt, Zeithorizont, Auslöser und Ziel
    verglichen. Nur ein unveränderter Vergleich erlaubt die Annahme des
    Beitrags. Eine Abweichung bleibt unwirksam, wird dem Nutzer verständlich
    erklärt und benötigt für eine Übernahme eine ausdrücklich neue
    Research-Version.

## Rejected Alternatives

- **Jeder Spezialist entscheidet selbst, wann er gebraucht wird:** verworfen,
  weil niemand den Gesamtzustand und die Reihenfolge zuverlässig besitzt.
- **Nur ein freier Hauptagent ohne feste Übergangsregeln:** verworfen, weil
  Pflichtprüfungen vom Promptverständnis und Gedächtnis eines einzelnen Laufs
  abhingen.
- **Vollständig starre Automatik ohne semantische Einordnung:** verworfen, weil
  die Bedeutung einer Nutzerfrage und die Materialität einer Entscheidung nicht
  allein aus Dateiständen hervorgehen.
- **Spezialisten sprechen direkt mit dem Nutzer:** verworfen, weil dadurch
  widersprüchliche Erklärungen, technische Innensicht und unklare
  Gesamtverantwortung entstehen.
- **Parallele Spezialisten als Standard:** verworfen, weil die hier relevanten
  Schritte voneinander abhängen und Agentenübereinstimmung keine Evidenz ist.

## Consequences

- Der Wissenschaftsphilosoph wird an den beiden kritischen Übergängen
  automatisch verpflichtend, statt nur als mögliche Rolle dokumentiert zu
  sein.
- Der Nutzer erhält eine zusammengeführte, allgemeinverständliche Antwort vom
  Forschungsleiter und muss die interne Agentenarbeit nicht koordinieren.
- Wiederaufnahme, Fehleranalyse und Zusammenarbeit mit mehreren
  Schreibwerkzeugen werden durch Checkpoints und eindeutige Zuständigkeiten
  robuster.
- Die feste Steuerung verhindert vergessene Pflichtübergänge, beweist aber
  nicht die inhaltliche Richtigkeit einer Spezialistenantwort.
- Die deterministischen Vertrags- und Routingtests prüfen Aufbau und
  Reihenfolge. Ob ein konkretes Modell die Steuerung im echten Dialog befolgt,
  muss zusätzlich durch einen gekennzeichneten `LIVE_AGENT`-Lauf geprüft
  werden.
- Routing und Rekonstruktion führen selbst keine Strategieprüfung, keinen
  Marktdatenzugriff und keinen Backtest aus.

## Action Items

1. [x] Zentralen Forschungsleiter als Agentenrolle definieren.
2. [x] Checkpoint und Routingentscheidung maschinenprüfbar festlegen.
3. [x] Pflichtübergänge für Begriffsprüfung, Bedingungsanfrage und
   wissenschaftsphilosophische Fortsetzung implementieren.
4. [x] Einstieg für Codex und Claude verbindlich dokumentieren.
5. [x] Positive und negative Routingfälle in Vertrags- und Regressionstests
   aufnehmen.
6. [x] Sechs-Punkte-Driftkontrolle vor Annahme jedes bestehenden
   Research-Handoffs ergänzen.
7. [ ] Das Verhalten eines tatsächlich angeschlossenen Hauptagenten in einem
   `LIVE_AGENT`-Lauf prüfen, bevor eine Modell- oder Promptfreigabe behauptet
   wird.
