# ADR-002: Versions- und integritätsbewusste Governance akademischer Quellen

**Status:** Accepted  
**Date:** 2026-08-30  
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Der bisherige Evidence-Vertrag kennt den Quellentyp `ACADEMIC`, unterscheidet aber
nicht zwischen einer peer-reviewten Journalfassung, einem Accepted Manuscript,
einem Working Paper und einem Preprint. Dadurch könnten unter anderem:

- eine arXiv-Fassung irrtümlich als peer-reviewt behandelt,
- mehrere Fassungen derselben Arbeit als unabhängige Bestätigungen gezählt,
- Korrekturen, Expressions of Concern oder Retraktionen übersehen,
- Journalprestige mit methodischer Qualität verwechselt,
- und Replikations-, Code- oder Datenbehauptungen ohne prüfbare Referenzen geführt
  werden.

Trading-Research benötigt zugleich Zugriff auf wissenschaftliche Primärquellen.
Dazu gehören gezielt Originalarbeiten aus Fachzeitschriften wie *Journal of
Finance* und *Journal of Financial Economics* sowie aktuelle Manuskripte aus den
`q-fin`-Kategorien von arXiv. Diese Kanäle haben unterschiedliche Review- und
Versionszustände und dürfen daher nicht gleich behandelt werden.

## Decision

Wir führen ein explizites Academic-Source-Protokoll ein.

1. Jede akademische Quelle bezeichnet eine konkrete Dokumentfassung und erhält
   vollständige `academic_metadata`.
2. Alle Fassungen derselben Arbeit teilen eine stabile `work_id`. Journalfassung,
   Accepted Manuscript, Working Paper und Preprint sind dadurch eine
   Versionsfamilie und keine voneinander unabhängigen Belege.
3. Der Publikationsstatus ist genau einer von
   `PEER_REVIEWED_VERSION_OF_RECORD`, `ACCEPTED_MANUSCRIPT`, `WORKING_PAPER`,
   `PREPRINT` oder `OTHER`. Peer Review wird aus diesem Status abgeleitet und nicht
   über ein redundantes Boolean-Feld modelliert.
4. `study_type` trennt Originalstudie, Replikationsstudie, systematischen Review,
   Meta-Analyse, Methodenpapier, Kommentar und sonstige Beiträge. Nur der
   akademische Kanal macht eine Quelle nicht automatisch zur Primärstudie.
5. Für arXiv werden ID, konkrete Version, Einreichungs-/Änderungszeit und eine der
   offiziellen Kategorien `q-fin.CP`, `q-fin.EC`, `q-fin.GN`, `q-fin.MF`,
   `q-fin.PM`, `q-fin.PR`, `q-fin.RM`, `q-fin.ST` oder `q-fin.TR` gespeichert.
   `q-fin` ist eine Themenklassifikation, kein Review- oder Gütesiegel.
6. Vor Evidenzverwendung wird der Integritätsstatus über Verlag, Crossmark,
   DOI-Metadaten oder Repository geprüft. Korrektur, Expression of Concern,
   Retraktion oder Withdrawal benötigt eine verlinkte Notice.
7. Code- und Datenverfügbarkeit werden als Zugriffszustände erfasst. Offenheit ist
   für Reproduzierbarkeit relevant, ersetzt aber keine Design- oder
   Identifikationsprüfung; fehlende Offenheit ist umgekehrt nicht automatisch ein
   Beweis für schlechte Forschung.
8. Eine positive, negative oder gemischte Replikationsaussage benötigt Referenzen
   auf tatsächlich unabhängige Arbeiten. Weitere Fassungen derselben `work_id`
   genügen nicht.
9. Journalname, Impact Factor und Zitationszahl sind keine Evidence-Grade-Regeln.
   *Journal of Finance* und *Journal of Financial Economics* werden als gezielte
   Recherchekanäle berücksichtigt, nicht als Whitelist oder Qualitätsgarantie.
10. Ein verifizierter Preprint darf den engen `SOURCE_FACT` tragen, dass die Arbeit
    ein Ergebnis berichtet. Ein alleiniger, nicht unabhängig reproduzierter
    Preprint darf keinen entscheidungstragenden Claim auf `SUFFICIENT` heben und
    keine Aktivierung allein tragen.

Die maschinenlesbare Umsetzung erfolgt mit
`schemas/evidence.schema.json` Version `2.0.0`; die geänderte Grade-Semantik trägt
`evidence_assessment.ruleset_version = 1.1.0`.

## Primary references for the protocol

- [arXiv category taxonomy](https://arxiv.org/category_taxonomy)
- [arXiv versioning help](https://info.arxiv.org/help/versions.html)
- [Crossref Crossmark](https://www.crossref.org/services/crossmark/)

Diese Referenzen definieren Repository-Kategorien, dauerhafte Versionsstände und
die Abfrage von Updates beziehungsweise Integritätshinweisen. Sie bewerten nicht
die inhaltliche Qualität einzelner Forschungsarbeiten.

## Options Considered

### Option A: `ACADEMIC` ohne Unterstruktur beibehalten

Einfach, aber Publikations-, Versions- und Integritätsstatus bleiben implizit. Der
Agent könnte wichtige Unterschiede nur in freiem Text ausdrücken; automatische
Prüfung und Deduplizierung wären nicht zuverlässig möglich.

### Option B: Journal-Whitelist als Qualitätsfilter

Leicht verständlich, aber methodisch falsch. Auch renommierte Journals enthalten
unterschiedliche Designs, spätere Korrekturen und nicht replizierte Ergebnisse;
zugleich können hochwertige Working Papers und Preprints relevante frühe Evidenz
liefern.

### Option C: Explizites Versionsfamilien- und Integritätsmodell

Mehr Metadatenaufwand, dafür werden Reviewstatus, Dokumentversion, Integrität,
Reproduzierbarkeit und Unabhängigkeit getrennt und maschinenprüfbar behandelt.
Diese Option wird gewählt.

## Consequences

- Bestehende `ACADEMIC`-Objekte benötigen eine Migration; deshalb ist das neue
  Evidence-Schema eine Major-Version.
- Nichtakademische Quellen bleiben kompatibel und dürfen keine nicht-null
  `academic_metadata` tragen.
- Neue arXiv-Versionen überschreiben alte Snapshots nicht. Die verwendete Version
  bleibt dauerhaft referenziert und eine neuere Fassung erzeugt ein Source-Delta.
- Eine neue Korrektur, Expression of Concern, Retraktion oder ein bestätigtes
  Replikationsproblem kann einen materiellen beziehungsweise brechenden Delta
  auslösen.
- JSON Schema kann Feldkonsistenz prüfen, aber nicht vollständig feststellen, ob
  zwei `work_id` tatsächlich dieselbe Arbeit bezeichnen oder eine Replikation
  methodisch unabhängig ist. Diese Cross-Object-Regeln bleiben zusätzlich Aufgabe
  von Validator, Eval und Human Review.

## Action Items

1. [x] Evidence-Schema 2.0 mit Academic-Metadaten und bedingten Verträgen ergänzen.
2. [x] Positive und negative Schema-Fixtures für Journal- und q-fin-Quellen anlegen.
3. [x] Academic-Source-Governance in Operationsstandard und Case-Checkliste aufnehmen.
4. [x] Einen Eval-Fall für die korrekte Behandlung eines q-fin-Preprints ergänzen.
5. [ ] Cross-Object-Validator für `work_id`-Deduplizierung und Replikationsreferenzen implementieren.
