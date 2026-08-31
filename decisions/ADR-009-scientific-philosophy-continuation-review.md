# ADR-009: Wissenschaftsphilosophische Prüfung von Fehlerzurechnung und Fortsetzung

**Status:** Accepted; pre-operationalization scope amended by ADR-010
**Date:** 2026-08-31
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Ein Test betrifft nicht nur eine Hypothese, sondern auch Hilfsannahmen,
Operationalisierung, Messung, Datenqualität, Scope, Modell und Implementierung.
Nach einem negativen Ergebnis ist daher logisch nicht automatisch bestimmt,
welches Glied scheiterte. Besonders bei aus Prosa rekonstruierten Strategien
entsteht sonst ein falsches Dilemma: entweder die Kernidee vorschnell verwerfen
oder die Operationalisierung nach dem Ergebnis so lange ändern, bis das
gewünschte Resultat erscheint.

Die bestehende Viererentscheidung und die Regel „unerwartetes Vorzeichen erzeugt
höchstens eine neue Hypothese“ schützen das eingefrorene Ergebnis. Es fehlte aber
ein eigener Vertrag für die Frage, welche Anschlussänderung wissenschaftlich
neuen Gehalt besitzt.

## Decision

1. `agents/scientific-philosophy-critic.md` wird als dauerhafter Agentenvertrag
   eingeführt.
2. `schemas/scientific_philosophy_review.schema.json` trennt Kernclaim,
   Hilfsannahmen, Fehlerzurechnung, Forschungsprogramm, Anomaliestatus und
   Revisionsvorschläge.
3. Duhem-Quine wird als Zurechnungsgrenze verwendet: Ohne unterscheidende
   Evidenz bleibt die Fehlerursache `NON_UNIQUE` oder `UNRESOLVED`.
4. Das Q8-Ergebnis der alten Research-ID bleibt unverändert.
5. Lakatos klassifiziert Anschlussänderungen als `PROGRESSIVE`, `DEGENERATIVE`,
   `DIAGNOSTIC_ONLY` oder `UNRESOLVED`.
6. `PROGRESSIVE` verlangt eine zuvor nicht implizierte Vorhersage, einen
   Falsifikator, einen unabhängigen Evaluationsplan und eine neue Research-ID.
7. Degenerative Änderungen und Diagnostik autorisieren keinen neuen
   Bestätigungstest. Diagnostik kann einen Fehler lokalisieren, aber keinen
   alten Claim retten.
8. Kuhns Perspektive wird auf den Status des Forschungsprogramms begrenzt.
   Isolierte oder wiederkehrende Anomalien und verfügbare Rivalen werden
   erfasst; das Fehlen eines Rivalen zählt nicht als positive Evidenz.

## Rejected Alternatives

- **Jeden Fehlschlag eindeutig der Hypothese zurechnen:** verworfen, weil der
  Test das gesamte Bündel betrifft.
- **Jede alternative Operationalisierung erneut testen:** verworfen, weil eine
  nachträgliche Variante ohne neuen empirischen Gehalt nur den Misserfolg
  umgeht.
- **Neue Research-ID als alleinige Lösung:** verworfen; neue Benennung erzeugt
  keine neue Vorhersage.
- **Kuhn als Rechtfertigung zum Ignorieren der Anomalie:** verworfen; die
  Programmebene ändert den Befund des Einzeltests nicht.
- **Wissenschaftsphilosophie als Pflichtblock für jede Rohidee:** verworfen.
  ADR-010 verlangt die frühe Begriffsprüfung gezielt bei unvollständig
  definierten Quellenstrategien; gewöhnliche Rohideen werden damit nicht
  belastet.

## Consequences

- Ein negatives Ergebnis kann ehrlich unterbestimmt bleiben, ohne beliebige
  nachträgliche Rettung zu erlauben.
- Quellenstrategien dürfen mit einer begründeten neuen Übersetzung weiter
  untersucht werden, wenn diese eine eigenständige riskante Vorhersage erzeugt.
- Das Artefakt ist kein Backtest, kein Ergebnisgenerator und kein Human Review.
- Der synthetische VWAP-Fall demonstriert nur den Vertrag; er behauptet keinen
  realen Test oder Edge.
