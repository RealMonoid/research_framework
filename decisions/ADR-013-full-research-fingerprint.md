# ADR-013: Vollständiger Forschungsfingerabdruck und sichtbare Änderungen

## Status

Angenommen

## Problem

Der bisherige Driftcheck verglich nur Forschungsfrage, Strategie, Markt,
Zeithorizont, Auslöser und Ziel. Diese sechs Punkte konnten gleich bleiben,
während ein Agent etwa einen Lookback, eine Messdefinition, einen Filter, eine
Datenquelle, eine Ausschlussregel oder eine Auswertungsannahme änderte. Solche
Änderungen können das Ergebnis materiell beeinflussen.

## Entscheidung

Jede Research-Version erhält einen vollständigen, kanonisch geordneten
Fingerabdruck. Er enthält alle fachlich wirksamen Festlegungen sowie die
Prüfsummen der zugrunde liegenden materiellen Artefakte. Vor der Annahme eines
materiellen Arbeitsergebnisses wird daraus ein Kandidatenfingerabdruck erzeugt
und vollständig mit dem wirksamen Stand verglichen.

Bei Gleichheit darf die Arbeit nach den übrigen Prüfungen angenommen werden.
Bei jeder Abweichung bleibt der bisherige Fingerabdruck wirksam. Das System
erzeugt einen sichtbaren Änderungsvorschlag mit den exakten abweichenden Pfaden.
Nur eine ausdrückliche Nutzerentscheidung darf daraus eine neue Research-ID
oder Research-Version machen. Ein bestehender Stand wird niemals still
überschrieben.

Die Regel gilt für Fachagenten und für materielle Arbeit des Hauptagenten.

## Folgen

- Änderungen an bisher ungeschützten Details werden erkennbar.
- Umordnungen in ausdrücklich ungeordneten Listen lösen keinen Fehlalarm aus.
- Der Fingerabdruck beurteilt nicht, ob eine Änderung wissenschaftlich gut ist;
  er macht sie sichtbar und verhindert ihre heimliche Übernahme.
- Der Hauptagent muss aus jedem materiellen Ergebnis einen vollständigen
  Kandidatenfingerabdruck ableiten.
- Live-Verhalten von Sprachmodellen bleibt zusätzlich zu testen. Der dafür
  vorgesehene LLM-Stresstest ist in `PLANNED_FEATURES.md` als noch nicht
  implementiert dokumentiert.
