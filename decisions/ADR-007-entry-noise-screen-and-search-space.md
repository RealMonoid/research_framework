# ADR-007: Entry Noise Screen und vorab fixierter Suchraum

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Der Generator macht die Erzeugung vieler Hypothesen billig. Er macht deren
statistische Prüfung nicht billig und beseitigt keine Multiplizität. Ein Lauf
mit 96 datenbasiert gescreenten Kandidaten ist eine Familie von 96 Tests, auch
wenn später nur wenige davon in einem Research Case erscheinen.

Das bisherige §13-Gebot verlangte zwar die Dokumentation des Suchraums, besaß
aber kein Entry-Artefakt, das Familiengröße und Schwelle vor dem ersten Ergebnis
fixierte. Ein einzelner Screen bei fünf Prozent hätte deshalb aus einer großen
Nullfamilie erwartbar falsche Überlebende erzeugen können.

Außerdem war der Ursprung neuer Katalogeinträge nicht explizit. Dadurch konnte
der Mechanismenkatalog nicht sauber zwischen Literatur, Marktregel und eigener
Beobachtung unterscheiden und systematisch aus neuen Beobachtungen wachsen.

## Decision

1. Jeder Mechanismus führt ein `entry_origin` mit Ursprungstyp, stabilen
   Referenzen, Kurzbegründung und Erfassungszeitpunkt. Eigene Beobachtungen
   verwenden `INTERNAL_OBSERVATION` und eine Journal-/Beobachtungsreferenz.
2. Ein Generatorlauf ist eine Kandidatenuniversums-Referenz. Vor dem ersten
   datenbasierten Entry Screen wird die tatsächlich geplante Testfamilie in
   `schemas/search_space.schema.json` fixiert.
3. Das Register enthält registrierte Kandidaten, geplante und durchgeführte
   Screens, Familien-Alpha, Korrekturmethode und wirksames Perzentil.
4. `schemas/noise_screen.schema.json` speichert Statistik, Surrogatverfahren,
   erhaltene Struktur, vorab gesetzte Schwelle, Exceedance-Zahl, Datenrolle und
   Search-Space-Referenz.
5. Ein beobachtungsgetriebener Candidate benötigt vor `PROMOTED` einen Screen.
   Theorie-, terminierte Event- und publizierte Replikationsideen dürfen einen
   begründeten Waiver verwenden.
6. `PROMOTED` verlangt einen `actor_constraint` mit Akteur, Zwang, erwarteter
   Handlung, Beobachtbarkeit und konkurrierender Akteurshypothese. Das ist eine
   Plausibilitätsanforderung, kein Mechanismusnachweis.
7. `scripts/validate_entry_thresholds.py` prüft die Regeln, die JSON Schema
   nicht ausdrücken kann: Datumsreihenfolge, Quotienten, Zählergrenzen,
   Cross-Artifact-Referenzen und die nachgerechnete Korrekturschwelle.
8. Bonferroni verwendet die vorab geplante Familiengröße. Ein
   Effective-Tests-Ansatz benötigt eine Evidenzreferenz. Benjamini–Hochberg darf
   erst nach vollständigem Batch mit dokumentiertem Rang entscheiden.
   `NONE_JUSTIFIED` ist nur bei `planned_screen_count = 1` zulässig; bei mehreren
   geplanten Screens kann die Korrektur nicht wegbegründet werden.
9. Noise Screens verwenden nur `DISCOVERY`- oder `SYNTHETIC`-Daten. `PASS`
   berechtigt zu Phase-0-Aufwand und ist keine Evidenz für Effekt, Mechanismus,
   Prognose oder Netto-Edge.

## Rejected Alternatives

- **Fester universeller p-Wert:** verworfen, weil Familiengröße und
  Abhängigkeitsstruktur variieren und die Markt-Nullverteilung driftet.
- **Naive Permutation als Standard:** verworfen, wenn sie Sessionstruktur,
  Autokorrelation oder Volatilitätscluster zerstört.
- **Nur überlebende Kandidaten zählen:** verworfen, weil dies den tatsächlichen
  Suchraum nach Ergebnissicht verkleinert.
- **Familiengröße nach jedem Screen erhöhen:** verworfen, weil dadurch bereits
  getroffene Entscheidungen nachträglich eine andere Schwelle erhielten.
- **Benjamini–Hochberg als laufender Einzeltest-Cutoff:** verworfen, weil der
  BH-Rang die vollständige sortierte p-Wert-Familie voraussetzt.
- **Noise Screen für jede Idee ohne Ausnahme:** verworfen zugunsten eng
  definierter Waiver für Theorie, terminierte Events und Replikation.
- **Actor Constraint schon bei `INBOX`:** verworfen, damit Rohideen weiterhin
  billig und ohne nachträgliche Herkunftsverluste erfasst werden können.
- **Schema-Prosa als angebliche Rechenprüfung:** verworfen; die semantischen
  Invarianten werden ausführbar validiert.

## Consequences

- Ein großer Generatorlauf kann nicht mehr stillschweigend als Folge
  unabhängiger Fünf-Prozent-Screens behandelt werden.
- Der Katalog kann aus internen Beobachtungen wachsen, ohne Beobachtung mit
  Evidenz zu verwechseln.
- `INBOX` bleibt unverändert klein; die zusätzlichen Pflichten beginnen erst
  beim datenbasierten Screen beziehungsweise bei Promotion.
- Das Framework wird dadurch nicht end-to-end praxiserprobt. Die bekannte Lücke
  eines vollständig durchgearbeiteten realen Research Case bleibt bestehen.

## Action Items

1. [x] Katalogherkunft ergänzen und vorhandene Einträge migrieren.
2. [x] Search-Space- und Noise-Screen-Schemas anlegen.
3. [x] Semantischen Cross-Artifact-Validator implementieren.
4. [x] `PROMOTED`-Intake und Actor Constraint verschärfen.
5. [x] Positive, negative, arithmetische und plattformübergreifende Tests ergänzen.
