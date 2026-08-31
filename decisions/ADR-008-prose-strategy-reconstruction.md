# ADR-008: Quellennahe Rekonstruktion unvollstaendig operationalisierter Strategien

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Handelsbuecher und andere Sekundaerquellen liefern haeufig erkennbare Setups,
aber keine eindeutigen ausfuehrbaren Regeln. Sie mischen Regeln, Beispiele,
Alternativen und ausdrueckliche Trader-Discretion. Die bisherige
Operationalisierungstabelle im Research Case erfasste spaeter die gewaehlte
Messdefinition, aber nicht die vorgelagerte Uebersetzung: Welche Bestandteile
stammen aus der Quelle, welche sind offen und welche wurden ergaenzt?

Das Problem ist keine fehlende Backtestregel. Ohne eine Quellenrekonstruktion
laesst sich schon vor jedem Test nicht unterscheiden, ob eine spaetere
Spezifikation die publizierte Strategie repliziert, dokumentiert rekonstruiert
oder wesentlich veraendert.

## Decision

1. `schemas/strategy_reconstruction.schema.json` wird als eigenes
   vorgelagertes Artefakt eingefuehrt.
2. Der gepruefte Quellenausschnitt wird explizit begrenzt; ein Ausschnitt darf
   nicht als vollstaendig gelesenes Werk ausgegeben werden.
3. Quellenbehauptungen werden paraphrasiert und als erforderlich, empfohlen,
   optional, illustrativ oder unklar markiert. Ein Beispiel ist keine Regel.
4. Konstrukte erhalten einen der Status `SOURCE_SPECIFIED`,
   `SOURCE_ALTERNATIVES`, `UNSPECIFIED`, `DISCRETIONARY` oder
   `CONTRADICTORY`.
5. Operationalisierungskandidaten behalten ihre Herkunft. Ein Vorschlag aus
   Domain Convention, externer Literatur oder eigener Rekonstruktion wird nicht
   der Quelle zugeschrieben.
6. Kandidaten werden nicht automatisch gewaehlt. Ihre Erfassung ist weder ein
   Marktdatenzugriff noch automatisch ein statistischer Test oder Suchraum.
7. Ausdrueckliche Discretion darf als Human-Protocol erhalten bleiben. Ihre
   Entfernung erzeugt gegebenenfalls eine `SIMPLIFIED_VARIANT`, keine
   Replikation.
8. `REPLICATION` ist unzulaessig, solange ein wesentliches Konstrukt alternativ,
   unbestimmt, diskretionaer oder widerspruechlich bleibt.
9. `scripts/inspect_strategy_reconstruction.py` prueft Schema- und
   Referenzintegritaet sowie die Fidelity-Grenze. Es fuehrt keine Strategie aus.

## Rejected Alternatives

- **Direkt eine Backtestregel schreiben:** verworfen, weil dadurch
  Quelleninterpretation und Strategiedesign unsichtbar vermischt werden.
- **Jedes Beispiel als Default verwenden:** verworfen, weil Beispiele Regeln
  illustrieren koennen, ohne sie allgemein festzulegen.
- **Alle plausiblen Definitionen automatisch testen:** verworfen, weil ein
  Uebersetzungskatalog keine Testanweisung ist.
- **Diskretion vollstaendig entfernen:** verworfen als allgemeiner Default;
  dies kann eine legitime vereinfachte Variante sein, muss aber so benannt
  werden.
- **Sofort ein globaler Konstruktkatalog:** vorerst verworfen. Das erste reale
  Buchbeispiel zeigt, welche wiederkehrenden Definitionen tatsaechlich
  katalogwuerdig sind. Der Artefaktvertrag funktioniert ohne vorgetaeuschte
  Vollstaendigkeit eines solchen Katalogs.

## Consequences

- Strategien aus Prosa koennen als Ideenquelle genutzt werden, ohne dass offene
  Begriffe unbemerkt zu angeblichen Autorenregeln werden.
- Eine Dokumented Reconstruction bleibt von Replication und Simplified Variant
  unterscheidbar.
- Das Artefakt generiert noch keine fertige Strategie. Die spaetere Auswahl
  bleibt eine bewusste fachliche Aufgabe.
- Der VWAP-Buchfall ist ein durchgearbeitetes Rekonstruktionsbeispiel, aber kein
  durchgelaufener Research Case und kein Backtest.

## Action Items

1. [x] Schema und semantischen Inspector implementieren.
2. [x] Buchausschnitte als quellennahe Source Extraction erfassen.
3. [x] Positive und negative Vertragstests ergaenzen.
4. [x] Kurzpfad und Research-Standard um den optionalen Router erweitern.
5. [ ] Erst nach weiteren realen Rekonstruktionen entscheiden, welche
   Konstrukte in einen wiederverwendbaren Katalog gehoeren.
