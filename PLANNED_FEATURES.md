# Geplante Funktionen

Diese Liste enthält bewusst nur Vorhaben. Ein Eintrag hier ist weder
implementiert noch geprüft noch freigegeben.

## LLM-Stresstest gegen heimliche Forschungsänderungen

**Status:** geplant, nicht implementiert

Der Stresstest soll mehrere Sprachmodelle gezielt mit schwierigen Situationen
konfrontieren: negative Ergebnisse, widersprüchliche Quellen, verlockende
nachträgliche Filter, geänderte Zeitfenster, neue Ausschlüsse und scheinbar
harmlose Umformulierungen. Geprüft wird, ob der Hauptagent:

- den wirksamen Forschungsfingerabdruck unverändert lässt;
- jede materielle Abweichung als sichtbaren Änderungsvorschlag ausweist;
- keine vorgeschlagene Änderung ohne Nutzerentscheid übernimmt;
- bei Zustimmung eine neue Research-Version anlegt, statt die alte zu
  überschreiben;
- in verständlicher Sprache erklärt, was sich fachlich ändern würde.

Für eine spätere Freigabe braucht der Test einen versionierten Fallkatalog,
mehrere wiederholte Modellläufe, eine unabhängige Bewertung und feste
Bestehensgrenzen. Die vorhandenen deterministischen Vertragsprüfungen sind die
Voraussetzung dafür, aber kein Ersatz für diesen Live-LLM-Stresstest.
