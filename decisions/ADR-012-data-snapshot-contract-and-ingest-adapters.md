# ADR-012: Unveränderlicher Datensnapshot als Vertrag und anbieterspezifische Ingest-Adapter

**Status:** Angenommen
**Datum:** 2026-08-31

## Kontext

Das Framework kannte bisher zwei Enden einer Kette, aber nicht deren Mitte.
`data_requirements` beschreibt im promovierten Intake, *welche* Daten nötig sind
— Mindestauflösung, Venue-Abdeckung, Tiefe, Historie. `consumed_data_refs`
sammelt, *welche* Daten eine Idee bereits beeinflusst haben, allerdings als
freie Liste von Bezeichnern ohne jeden Vertrag.

Damit war die am strengsten geregelte Kette des Frameworks ausgerechnet an der
Stelle offen, an der die Daten eintreten. Ein eingefrorener Suchraum, ein vorab
gesetzter Noise-Screen-Schwellenwert und eine deklarierte IS/VAL/OOS-Aufteilung
verlieren ihre Aussagekraft, wenn der Datenstand darunter unbemerkt wechseln
kann. Eine Referenz wie `csv:SYMBOL:60:2024..2026` ist weder auflösbar noch
prüfbar; zwei verschiedene Dateien können denselben Bezeichner tragen.

Zugleich zeigte die Praxis, dass Chart-Werkzeuge als Datenquelle nicht
ausreichen: Exportgrenzen, lückenhafte Indikatorspalten und undokumentierte
Warmup-Logik machen einen Export nicht reproduzierbar. Ein Wechsel auf
Bulk-Archive externer Anbieter war damit absehbar — und mit ihm die Frage, ob
solche Beschaffungslogik in ein governance-first formuliertes, venue-neutrales
Framework gehört.

## Entscheidung

1. Ein neues Schema `data_snapshot` (Version `1.0.0`) definiert die
   unveränderliche Referenz auf einen konkreten Datenstand. Pflichtangaben sind
   Herkunft mit Anbieter, Zugriffsart und Nutzungsbedingungen, Instrument mit
   Venue, Symbol, Kontraktklasse und Auflösung, Abdeckung mit Grenzen,
   Zeilenzahl und Lücken sowie eine Dateiliste mit `sha256` je Datei.
2. Zeitstempel eines Snapshots sind ausnahmslos UTC. Das Schema erlaubt für
   `coverage.timezone` keinen anderen Wert.
3. Wer Kontinuität nicht geprüft hat, darf keine Lückenzahl behaupten und muss
   die Einschränkung in `known_limitations` deklarieren.
4. Berechnete Spalten werden als `derivations` mit Name, Formel und
   Eingangsspalten geführt. Eine Ableitung ohne Formel ist unzulässig.
5. Enthält ein Snapshot eine `split_declaration`, muss deren `declared_at` vor
   `source.retrieved_at` liegen. Eine nach dem Datenabruf festgelegte Aufteilung
   ist keine Vorab-Festlegung und wird maschinell abgewiesen.
6. Anbieterspezifische Beschaffung liegt in `ingest/` und ist ausdrücklich
   nicht-normativ. Ein Adapter erzeugt einen vertragskonformen Snapshot; er
   entscheidet nichts über Hypothesen, Evidenz oder Promotion.
7. Adapter trennen reine Planungs-, Parsing- und Analysefunktionen vom
   Netzwerkzugriff. Die CI prüft ausschließlich die reinen Anteile gegen
   Fixtures und bleibt netzwerkfrei.
8. Ein Snapshot belegt Herkunft, Abdeckung und Integrität. Er belegt weder
   Datenqualität noch Eignung für eine bestimmte Hypothese.

## Folgen

- `scripts/test_data_snapshot.py` prüft den Vertrag mit 2 positiven und 19
  negativen Invarianten und läuft in beiden Validierungspfaden.
- `ingest/binance_public_data.py` ist der erste Adapter. Er nutzt ausschließlich
  öffentlich zugängliche Archive ohne API-Key oder Account und verifiziert die
  vom Anbieter mitgelieferten Prüfsummen.
- `ingest/tests/` prüft Planung, Prüfsummen-Parsing, Abdeckungsanalyse und
  insbesondere, dass der erzeugte Snapshot dem Schema genügt.
- `consumed_data_refs` kann künftig auf `snapshot:`-Bezeichner zeigen, deren
  Auflösung und Integrität nachprüfbar sind.
- Die bekannte end-to-end Validierungslücke bleibt bestehen. Ein Datensnapshot
  ersetzt keinen durchgearbeiteten realen Research Case.

## Verworfene Alternativen

### Downloader direkt im Framework-Kern

Verworfen, weil das Regelwerk dadurch an die URL-Struktur einer einzelnen Börse
gekoppelt würde. Eine Layout-Änderung beim Anbieter wäre dann ein Defekt des
Normdokuments und könnte dessen CI brechen.

### Nur ein Downloader ohne Vertrag

Verworfen, weil die eigentliche Lücke nicht die Beschaffung ist, sondern die
fehlende Nachprüfbarkeit der Referenz. Ohne Schema bliebe `consumed_data_refs`
ein freies Textfeld, und ein zweiter Anbieter erzeugte ein zweites Format.

### Prüfsummen als optionale Angabe

Verworfen, weil eine Referenz ohne Prüfsumme genau die Eigenschaft nicht hat,
derentwegen sie eingeführt wurde. Eine Datei, deren Inhalt sich unbemerkt ändern
darf, ist kein Snapshot.

### Zeitzone frei wählbar

Verworfen, weil Sessionanker, Aufteilungsgrenzen und Lückenzählung sonst
zwischen Snapshots unvergleichbar werden. Die Umrechnung gehört in den Adapter,
nicht in den Vertrag.
