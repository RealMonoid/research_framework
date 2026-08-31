# Strategien aus Prosa rekonstruieren

Dieser Pfad uebersetzt Strategien aus Buechern, Artikeln, Videos oder Kursen in
eine nachvollziehbare Spezifikation. Er ist eine **Uebersetzungshilfe**, kein
Backtest, kein Strategiegenerator und kein Wirksamkeitsgate.

## Warum ein eigenes Artefakt?

Eine Quelle kann eine erkennbare Strategie beschreiben und trotzdem Begriffe
wie „starkes Volumen“, „klarer Ausbruch“, „der Pullback haelt“ oder „naher
Widerstand“ offenlassen. Werden diese Luecken still gefuellt, ist spaeter nicht
mehr erkennbar, was aus der Quelle und was vom Rekonstruierenden stammt.

[`schemas/strategy_reconstruction.schema.json`](../schemas/strategy_reconstruction.schema.json)
trennt deshalb:

1. den geprueften Quellenausschnitt,
2. quellennahe, paraphrasierte Aussagen,
3. die fuer die Strategieidentitaet unverzichtbaren Aussagen,
4. offene Konstrukte und ihren Quellenstatus,
5. moegliche Operationalisierungen mit Herkunft,
6. eine spaetere, ausdrueckliche Entscheidung.

Bevor eine Rekonstruktion abgeschlossen und eine Definition eingefroren wird,
erstellt der
[`scientific-philosophy-critic`](../agents/scientific-philosophy-critic.md)
zusaetzlich ein
[`strategy_concept_audit`](../schemas/strategy_concept_audit.schema.json). Diese
fruehe Pruefung ist Teil der Rekonstruktion, kein Backtest und kein weiteres
Wirksamkeitsgate.

## Vier Arten von Bedingungen

Das Concept Audit trennt zwingend:

1. **Strategiedefinierende Bedingungen:** Ohne sie waere es nicht mehr dieselbe
   Quellenstrategie.
2. **Von der Quelle genannte Anwendungsbedingungen:** Die Quelle empfiehlt oder
   verlangt sie; damit ist noch nicht gezeigt, dass sie den Erfolg verursacht
   oder notwendig ist.
3. **Vermutete Erfolgsmodifikatoren:** Literatur, Theorie oder Researcher halten
   sie fuer plausibel. Sie bleiben Kandidaten und werden nicht heimlich als
   Filter eingebaut.
4. **Unbekannte Erfolgsbedingungen:** Das Framework behauptet nicht, alle
   Voraussetzungen zu kennen. Diese Unwissenheit wird ausdruecklich erhalten.

## Konstruktionsabhaengigkeiten

Trigger, Zustand, Ziel und Ergebnis werden auf ihre Rohdaten, Fenster und
deterministischen Berechnungen zurueckgefuehrt. Gemeinsame Inputs oder Fenster
koennen einen statistischen Zusammenhang mit erzeugen oder die beantwortete
Frage veraendern. Das ist:

- kein Kausalbeleg,
- nicht automatisch ein Konstruktionsfehler,
- und kein Grund, das quellennahe Ziel still durch ein anderes zu ersetzen.

Das Audit macht nur sichtbar, welcher Teil der beobachtbaren Beziehung aus der
eigenen Konstruktion stammen koennte und deshalb gesondert interpretiert werden
muss.

## Regime- und Zustandsfilter

Ein Filter ist zunaechst ein **vorlaeufiges Messinstrument**. Er beweist weder,
dass ein buchstaeblich realer verborgener Marktzustand existiert, noch dass ein
Akteur oder Mechanismus identifiziert wurde. Auch der Anteil der Beobachtungen,
die ein Filter einer Klasse zuordnet, misst fuer sich allein keine Trennleistung.

Eine spaetere Beurteilung fragt deshalb, ob die feste Einteilung kuenftiges
Verhalten unterscheidet, das nicht bereits in der Filterberechnung steckt, und
ob sie ueber ihre kontinuierlichen Eingangsgroessen oder eine einfache
Vergleichsregel hinaus zusaetzliche Information liefert. Ist der Filter nicht
informativ, faellt der von ihm abhaengige Zustandsclaim. Ein davon trennbarer
Ereignisclaim kann offen bleiben.

## Quellenstatus eines Konstrukts

| Status | Bedeutung |
|---|---|
| `SOURCE_SPECIFIED` | Die Quelle legt eine reproduzierbare Definition fest. |
| `SOURCE_ALTERNATIVES` | Die Quelle bietet mehrere Definitionen oder Handlungswege an. |
| `UNSPECIFIED` | Das Konstrukt wird benannt, aber nicht messbar definiert. |
| `DISCRETIONARY` | Menschliches Kontexturteil ist ausdruecklicher Teil der Methode. |
| `CONTRADICTORY` | Die geprueften Stellen verwenden unvereinbare Definitionen. |

Eine Quellenbehauptung fuehrt zusaetzlich `source_force`. Insbesondere bleibt
`ILLUSTRATIVE` ein Beispiel und wird nicht stillschweigend zur Regel.

## Kandidaten sind keine Auswahl und keine Tests

`operationalization_candidates` darf Definitionen aus der Quelle, aus
Domänenkonventionen, externer Literatur, einem dokumentierten
Researcher-Vorschlag oder einem Human-Protocol enthalten. Die Liste zeigt
Moeglichkeiten. Sie bedeutet nicht:

- dass eine Variante gewaehlt wurde,
- dass alle Varianten getestet werden sollen,
- dass ihre Anzahl bereits statistische Multiplizitaet ist,
- dass eine vorgeschlagene Definition in der Quelle stand.

Erst eine spaetere Entscheidung setzt `decision.status`. Werden Varianten
spaeter ergebnisabhaengig verglichen, greift der dann tatsaechlich untersuchte
Suchraum. Das Rekonstruktionsartefakt selbst greift keinen Marktdaten zu.

## Moegliche Endergebnisse

- `REPLICATION`: nur wenn alle wesentlichen Definitionen wirklich aus der
  Quelle stammen.
- `DOCUMENTED_RECONSTRUCTION`: offene Stellen wurden sichtbar und begruendet
  ergaenzt.
- `SIMPLIFIED_VARIANT`: wesentliche diskretionaere oder optionale Teile wurden
  bewusst entfernt.
- `PLAYBOOK_ONLY`: die Quelle bleibt ein Entscheidungsrahmen, keine eindeutige
  ausfuehrbare Regel.

Ein mechanischer Teilnachbau einer diskretionaeren Quelle wird daher nicht als
Replikation bezeichnet.

## Arbeitsablauf

1. Nur die tatsaechlich gelesenen Abschnitte in `locators_reviewed` erfassen.
2. Aussagen paraphrasieren und Regel, Empfehlung, Option und Beispiel trennen.
3. `strategy_identity_claim_refs` festhalten: Was darf nicht verschwinden, ohne
   dass eine andere Strategie entsteht?
4. Jedes Konstrukt klassifizieren und offene Fragen notieren.
5. Moegliche Definitionen mit ihrer echten Herkunft erfassen.
6. Zunaechst `decision.status = UNDECIDED` belassen.
7. Vor der Auswahl das Concept Audit abschliessen: Bedingungen klassifizieren,
   Konstruktionsabhaengigkeiten erfassen, Messinstrumente abgrenzen und
   unbekannte Erfolgsbedingungen erhalten.
8. Erst danach bei einer wirklichen Rekonstruktion Definitionen waehlen oder
   ein Human-Protocol festlegen und das Fidelity-Label setzen.

## Quantitative Suche nach Bedingungen

Nach einer vorlaeufigen Operationalisierung kann der
[`condition-inquiry-analyst`](../agents/condition-inquiry-analyst.md) ein
[`condition_inquiry`](../schemas/condition_inquiry.schema.json) anlegen. Dieses
Artefakt dient nicht nur der Kontrolle, sondern kann neue, pruefbare
Bedingungshypothesen erzeugen:

- Konstruktionsabhaengigkeiten und neutrale Simulationen fuer moeglicherweise
  eingebaute Zusammenhaenge,
- Multiversum oder Spezifikationskurve fuer die Abhaengigkeit von vertretbaren
  Messdefinitionen,
- interpretierbare Aufteilungen und bedingte Prognosepruefung fuer die Frage,
  unter welchen beim Entscheid bekannten Bedingungen sich das Ergebnis
  veraendert,
- Zeit- und Umgebungsstabilitaet fuer die Frage, ob eine Bedingung wiederkehrt.

Eine datenbasiert gefundene Bedingung wird als **neue
Erfolgsmodifikator-Hypothese** festgehalten. Sie wird nicht nachtraeglich zur
angeblich schon immer vorhandenen Voraussetzung der Quellenstrategie.

## Wenn die spaetere Validation scheitert

Ein Fehlschlag beweist nicht automatisch, dass gerade die selbst gewaehlte
Operationalisierung falsch war; getestet wurde das gesamte Buendel aus
Kernhypothese und Hilfsannahmen. Er erlaubt aber ebenso wenig, nach dem Ergebnis
eine guenstigere Definition aus der Kandidatenliste zu waehlen und den alten
Test zu retten.

Wird eine Fortsetzung erwogen, erstellt der
[`scientific-philosophy-critic`](../agents/scientific-philosophy-critic.md) ein
[`scientific_philosophy_review`](../schemas/scientific_philosophy_review.schema.json).
Das alte Ergebnis bleibt bestehen. Eine alternative Definition darf nur unter
neuer Research-ID empirisch weiterverfolgt werden, wenn sie eine neue,
widerlegbare und auf unabhaengigen Daten pruefbare Vorhersage erzeugt.

Das durchgearbeitete Quellenbeispiel ist
[`examples/strategy_reconstruction.vwap_wave_price_discovery.json`](../examples/strategy_reconstruction.vwap_wave_price_discovery.json).
Es endet bewusst bei `SOURCE_EXTRACTION`: keine Definition ist gewaehlt.

## Pruefen und zusammenfassen

```bash
python scripts/inspect_strategy_reconstruction.py \
  examples/strategy_reconstruction.vwap_wave_price_discovery.json
```

Der Inspector prueft Schema, IDs, Referenzen, Auswahlkonsistenz und unzulaessige
Replikationslabels. Er waehlt nichts aus und testet keine Marktstrategie.

Die beiden zusaetzlichen Vertraege lassen sich getrennt pruefen:

```bash
python scripts/inspect_strategy_concept_audit.py \
  examples/strategy_concept_audit.synthetic.json

python scripts/inspect_condition_inquiry.py \
  examples/condition_inquiry.synthetic_measurement.json
```

Beide Beispiele sind synthetisch und enthalten kein Marktergebnis.
