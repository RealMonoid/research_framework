# 05_AGENT_OPERATIONS.md

**Version:** 1.0  
**Stand:** 2026-08-30  
**Status:** ENTWURF ZUR ÜBERNAHME  
**Zweck:** Normative operative Kontrollschicht für reproduzierbare, überprüfbare und revisionssichere Läufe eines AI-Research-Agenten.

---

# 1. Geltungsbereich und Rang

Dieses Dokument ergänzt den methodischen Kern aus:

- **00_RESEARCH_AGENT_README.md**,
- **01_RESEARCH_STANDARD.md**,
- **02_RESEARCH_CASE_TEMPLATE.md**,
- **03_RESEARCH_METHODS.md**,
- **04_CAUSAL_TOOLING.md**.

Bei aktivierter operativer Schicht wird dieses Dokument nach **04_CAUSAL_TOOLING.md** gelesen.

Die Aufgabenteilung ist verbindlich:

| Ebene | Zuständigkeit |
|---|---|
| Dokumente 00–04 | Forschungslogik, Datenrollen, Claim-Level, Identifikation, statistische Methoden, Gates und Research-Endzustände |
| Dokument 05 | Laufherkunft, Claim-Herkunft, Quellenprüfung, Agenten-Evaluation, Telemetrie, Fehler, Reviews, Änderungen und operative Freigabe |

Dieses Dokument darf kein Forschungs-Gate aus 00–04 aufwerten, umgehen oder inhaltlich ersetzen. Insbesondere gilt:

- Ein operativ sauberer Lauf macht aus einem methodischen **FAIL** oder **BLOCKED** kein **PASS**.
- Eine ausreichend belegte Textaussage macht aus einem prädiktiven Claim keinen Kausalclaim; dafür gelten **00 §8a**, **01 §5** und **02 §E**.
- Ein LLM-Eval ersetzt weder das Pipeline-Integritätsgate aus **01 §13.1 / 02 §N4 / 03 §17** noch das Tooling-Gate aus **04 §6**.
- Operative Observability ist nicht das Markt- und Strategiemonitoring aus **01 §19 / 02 §Y**.
- Das Forecast Ledger ersetzt weder die Vorhersage-Liste aus **01 §12.1 / 02 §J** noch unabhängige Validation.

Die Wörter **MUSS**, **DARF NICHT**, **SOLL** und **DARF** sind normativ. Ist ein Pflichtfeld technisch nicht verfügbar, wird es nicht geraten oder leer gelassen, sondern mit **UNAVAILABLE**, Grund und Auswirkung protokolliert. Ein fehlender Pflichtwert kann je nach Auswirkung zu **PARTIAL**, **BLOCKED** oder **FAILED** führen.

---

# 2. Operatives Objektmodell und Pflichtartefakte

## 2.1 Identitäten und Beziehungen

Jeder ausführbare Agentenlauf erhält vor dem ersten Modell- oder Toolaufruf eine global eindeutige und unveränderliche **run_id**. Er referenziert mindestens:

- **research_id** und **research_version** aus **02 §A**,
- die bearbeitete Phase oder den rein operativen Auftrag,
- **parent_run_id**, falls der Lauf von einem anderen Lauf ausgelöst wurde,
- **baseline_run_id**, falls ein Delta oder eine Regression beurteilt wird,
- die erzeugten Artefakt-IDs und ihre Hashes.

IDs sind opake Schlüssel. Sie werden nicht nachträglich wiederverwendet oder auf ein anderes Objekt umgebogen. Eine Korrektur erzeugt eine neue Revision mit **supersedes_id**; das alte Objekt bleibt erhalten.

## 2.2 Pflichtartefakte

| Artefakt | Pflicht wann | Maschinenprüfung |
|---|---|---|
| Run Manifest | bei jedem Lauf | **schemas/run_manifest.schema.json** |
| Evidence-Dokument | sobald ein materieller Claim erzeugt oder übernommen wird | **schemas/evidence.schema.json** |
| Review-Dokument | bei menschlicher Prüfung, Korrektur, Freigabe, Ablehnung oder Override | **schemas/review.schema.json** |
| Trace | bei jedem Modell-, Tool-, Retrieval- und Validierungsschritt | Regeln in §6 |
| Error Log | sobald Warnung oder Fehler auftritt | Regeln in §7 |
| Delta Report | wenn ein Baseline-Lauf oder eine freigegebene Vorgängerversion existiert | Regeln in §9 |
| Forecast Ledger | bei jedem Claim des Typs **FORECAST** | **schemas/forecast.schema.json** und Regeln in §10 |
| Eval Result | bei Agenten-, Prompt-, Modell-, Tool-, Router- oder Schemaänderung | **evals/catalog.v1.json** und §11 |
| Multi-Agent Report | sobald mehr als ein Agent fachlich beiträgt | Regeln in §12 |

Die Beispiele unter **examples/** zeigen minimale syntaktisch gültige Instanzen für Run Manifest, Evidence, Forecast Ledger und Review. Sie sind keine Freigabe eines realen Laufs und kein Ersatz für die semantischen Regeln dieses Dokuments.

## 2.3 Schema- und Integritätsregel

Ein Artefakt ist nur gültig, wenn:

1. es gegen die angegebene Schemaversion validiert,
2. alle referenzierten IDs existieren,
3. alle deklarierten Hashes mit den gespeicherten Bytes übereinstimmen,
4. sein Zeit- und Versionsbezug eindeutig ist,
5. keine verbotene stille Mutation vorliegt.

JSON-Schema-Validität ist notwendig, aber nicht hinreichend. Ein formal gültiger, sachlich falscher oder nicht belegter Inhalt bleibt ungültig.

Die versionierten positiven und negativen Schema-Vertragstests werden mit **scripts/test_schemas.ps1** ausgeführt. **scripts/validate_framework.ps1** verbindet diese Tests mit Eval-Runner und Eval-Unit-Tests zu einem lokalen Gesamtcheck. Ein grüner technischer Gesamtcheck ersetzt weiterhin weder die semantische Artefaktprüfung noch Human Review.

## 2.4 Laufstatus

Das Run Manifest verwendet ausschließlich:

- **QUEUED**
- **RUNNING**
- **SUCCEEDED**
- **PARTIAL**
- **FAILED**
- **CANCELLED**

Die Status haben folgende feste Bedeutung:

| Status | Bedeutung |
|---|---|
| QUEUED | Identität und Auftrag existieren; fachliche Ausführung hat nicht begonnen. |
| RUNNING | Mindestens ein Ausführungsschritt läuft oder wartet auf eine zulässige Abhängigkeit. |
| SUCCEEDED | Alle für den Auftrag anwendbaren operativen Gates sind bestanden, alle Pflichtartefakte sind finalisiert und der fachliche Status wird wahrheitsgemäß wiedergegeben. |
| PARTIAL | Verwertbare Teilartefakte existieren, aber mindestens ein nicht bestandener oder noch offener operativer Punkt verhindert die Behauptung vollständiger Ausführung. |
| FAILED | Ein harter Fehler, ein nicht bestandenes Pflichtgate oder eine Integritätsverletzung macht das beabsichtigte Ergebnis unzulässig. |
| CANCELLED | Der Lauf wurde beendet, bevor sein Auftrag abgeschlossen war; Grund und Autorisierung sind protokolliert. |

**SUCCEEDED** bedeutet nicht, dass die Research-Hypothese bestätigt wurde. Ein methodisch korrekt ausgeführter Falsifikationslauf kann operativ **SUCCEEDED** und fachlich **FALSIFIED** oder **FAILED** sein. Umgekehrt darf ein methodisches Ergebnis nicht als vollständig ausgeführt gelten, wenn der zugehörige Lauf nur **PARTIAL** ist.

Ein terminales Manifest wird nicht editiert. Nachträgliche Erkenntnisse werden als verknüpftes Delta, Review oder neuer Lauf angehängt.

---

# 3. Run-Provenance

## 3.1 Mindestinhalt des Run Manifests

Das Manifest MUSS die folgenden Informationsgruppen enthalten oder mit **UNAVAILABLE + Grund** ausweisen:

| Gruppe | Pflichtinhalt |
|---|---|
| Identität | run_id, research_id, research_version, Auftrag, Phase, Status |
| Zeit | started_at und completed_at in UTC mit RFC-3339-Zeitstempeln |
| Lineage | parent_run_id, baseline_run_id, supersedes_run_id, auslösender Nutzer/Prozess |
| Modell | Provider, Modellname, Snapshot/Revision, API-Version |
| Inferenz | verfügbare Parameter wie Temperature, Top-p, Seed, Tokenlimit und Reasoning-Konfiguration |
| Prompt | Prompt-ID, Prompt-Version, Hash jeder Schicht und Hash des tatsächlich aufgelösten Prompts |
| Kontext | referenzierte Projektregeln, Dateien, Datenstände und ihre Hashes |
| Tools | erlaubte und tatsächlich verwendete Tools, Versionen, Berechtigungsprofil und relevante Konfiguration |
| Laufzeit | Betriebssystem, Runtime, Pakete, Lockfile-/Environment-Hash; bei Kausalanalyse zusätzlich **02 §E9 / 04 §5–8** |
| Inputs | Input-IDs, Herkunft, Daten-Vintage, as-of-Zeit, Inhalts-Hash |
| Outputs | Artefakt-ID, Pfad oder Objektreferenz, Medientyp, Schema-Version und Inhalts-Hash |
| Ressourcen | Modell-/Toolaufrufe, Input-/Output-/Cache-/Reasoning-Tokens soweit verfügbar, Laufzeit, Retries, Kosten, Währung und Preisstand |
| Abschluss | anwendbare operative Gates, offene Fehler, Review- und Delta-Status |

Ein Modellalias ohne Snapshot wird nicht als reproduzierbarer Snapshot ausgegeben. Ist der Provider-Snapshot nicht verfügbar, wird dies ausdrücklich als Einschränkung protokolliert.

## 3.2 Prompt- und Kontextversionierung

System-, Developer-, Nutzer- und projektspezifische Instruktionen werden getrennt versioniert oder gehasht. Der Lauf speichert:

1. die Reihenfolge der Instruktionsschichten,
2. die IDs und Versionen ihrer Quellen,
3. den Hash der tatsächlich gerenderten Eingabe,
4. alle dynamisch eingefügten Kontextartefakte,
5. jede Kürzung, Zusammenfassung oder Kontextkompression.

Eine materielle Prompt-, Router- oder Kontextänderung ist kein Retry desselben Ergebnisses, sondern ein neuer Lauf. Die Änderungsbeziehung wird über **parent_run_id** oder **supersedes_run_id** festgehalten.

## 3.3 Hash- und Unveränderlichkeitsregel

Die Schemas verwenden SHA-256 als genau 64 kleingeschriebene Hexzeichen. Ein zusätzliches stärkeres Verfahren darf parallel protokolliert werden, ersetzt aber das schema-konforme SHA-256-Feld nicht. Vor dem Hashen wird das tatsächlich gespeicherte Byteformat eindeutig festgelegt; bei strukturierten Daten ist die verwendete Kanonisierung zu benennen. Review-Dokumente verwenden die im Schema festgelegte RFC-8785-Kanonisierung.

Ein Hash:

- belegt Inhaltsgleichheit, nicht Wahrheit,
- ersetzt keinen zugänglichen Snapshot,
- darf nicht über einen normalisierten Inhalt berechnet werden, wenn der gespeicherte Rohinhalt davon abweicht,
- wird nach Finalisierung nicht überschrieben.

Geheimnisse, Zugangstoken und personenbezogene Daten werden nicht in Prompt, Trace oder Manifest kopiert. Es wird höchstens eine sichere Konfigurationsreferenz protokolliert; Geheimnisse werden auch nicht durch leicht angreifbare Klartext-Hashes „anonymisiert“.

## 3.4 Retry-Regel

Jeder Versuch eines Modell-, Tool- oder Retrievalaufrufs erhält eine **attempt**-Nummer und ein eigenes Trace-Ereignis.

- Ein technisch identischer, als **retryable = true** klassifizierter Versuch darf im selben Lauf wiederholt werden.
- Ändern sich Prompt, Daten, Modell, Toolversion, Berechtigungen oder fachliche Parameter, MUSS ein neuer Lauf entstehen.
- Retryanzahl, Backoff und Abbruchschwelle werden vor oder beim ersten Fehler protokolliert.
- Ein fehlgeschlagener Versuch wird niemals aus dem Trace entfernt, wenn ein späterer Versuch gelingt.

---

# 4. Epistemische Claim-Typen

## 4.1 Orthogonalität zum Research-Claim-Level

Der Research-Claim-Level aus **01 §5 / 02 §E1** beschreibt die Stärke der fachlichen Aussage: **ASSOCIATIONAL_PREDICTIVE**, **INTERVENTIONAL** oder **COUNTERFACTUAL**.

Der epistemische Claim-Typ dieses Dokuments beschreibt dagegen, wie eine einzelne Aussage zustande kam. Beide Felder sind unabhängig und dürfen nicht miteinander ersetzt werden.

Jeder materielle Claim erhält genau einen primären Typ:

| Typ | Definition | Mindestanforderung | Unzulässige Verwendung |
|---|---|---|---|
| SOURCE_FACT | Eine Quelle behauptet oder dokumentiert den Inhalt unmittelbar. | Quelle, Fundstelle, Snapshot/Vintage und extrahierter Fakt. | Interpretation, Berechnung oder Prognose als bloßen Quellenfakt ausgeben. |
| CALCULATED_VALUE | Deterministisches Ergebnis aus benannten Inputs. | Formel/Code, Input-Claims, Version, Rundungsregel und reproduziertes Ergebnis. | Unsichere Schätzung oder Modelloutput als exakte Rechnung darstellen. |
| ESTIMATE | Mess- oder Modellschätzung mit Unsicherheit. | Daten, Methode, Annahmen, Schätzwert, Unsicherheit und relevante Gates aus 00–04. | Punktschätzer als sicheren Fakt darstellen. |
| INFERENCE | Schlussfolgerung, die über den Wortlaut einzelner Quellen oder Inputs hinausgeht. | Explizite Prämissen, Schlussregel, Alternativerklärung und Grenzen. | Inferenz als direkte Quelle oder kausalen Beweis etikettieren. |
| FORECAST | Vor Eintreten des Outcomes eingefrorene, später auflösbare Aussage. | Forecast-Ledger-Eintrag nach §10. | Rückblickende Aussage oder nach Outcome angepasste Prognose. |
| HUMAN_JUDGMENT | Nachweislich von einem identifizierten Menschen getroffene Wertung oder Entscheidung. | Review-Record, Person/Rolle, Zeitpunkt, Grund und Geltungsbereich. | LLM-Ausgabe oder automatische Regel als menschliches Urteil ausgeben. |

Ein LLM darf ein menschliches Urteil vorschlagen. Bis ein identifizierter Mensch es im Review-System übernimmt, bleibt die Aussage **INFERENCE**, nicht **HUMAN_JUDGMENT**.

## 4.2 Materieller Claim

Ein Claim ist materiell, wenn er mindestens eines der folgenden Elemente beeinflussen kann:

- Hypothese, Gegenhypothese oder Falsifikation,
- Forschungs-Gate oder Endzustand,
- Claim-Level, DAG, Identifikation oder zulässige Kausalsprache,
- Datenrolle, Daten-Vintage oder Beobachtbarkeit,
- Effektgröße, Unsicherheit, Kosten oder Umsetzbarkeit,
- Forecast, Aktivierung, Suspendierung oder Revalidierung,
- wesentliche Handlungsempfehlung.

Materielle Claims dürfen nicht nur in freier Prosa existieren. Sie benötigen einen **claim_id**-Eintrag im Evidence-Dokument.

## 4.3 Claim-Mindestfelder

Jeder materielle Claim enthält mindestens:

- claim_id und Claim-Revision,
- run_id, research_id und research_version,
- unverwechselbaren Claim-Text,
- epistemischen Typ,
- zeitlichen Geltungsbereich und as-of-Zeit,
- Ursprung **MODEL / TOOL / HUMAN / IMPORTED**,
- evidence_refs und gegebenenfalls input_claim_refs,
- Bezug zu Hypothese, Gate, Entscheidung oder Forecast,
- evidence_grade nach §5,
- Status und gegebenenfalls supersedes_claim_id.

Eine textliche Präzisierung, die Aussageumfang, Richtung, Zahl, Zeitraum, Population oder Kausalstatus ändert, ist eine neue Claim-Revision.

---

# 5. Evidence Chain, Quellenprüfung und deterministischer Evidence Grade

## 5.1 Verbindliche Kette

Für jeden materiellen Claim MUSS die folgende Kette lückenlos rekonstruierbar sein:

**Quelle → Fundstelle → extrahierter Fakt → Transformation oder Schluss → Claim → betroffene Hypothese/Gate/Entscheidung**

Nicht benötigte Zwischenschritte werden ausdrücklich ausgelassen; sie werden nicht fingiert. Ein **SOURCE_FACT** hat typischerweise keine Transformation. Ein **CALCULATED_VALUE** MUSS dagegen seine Transformation und Input-Claims ausweisen.

Jeder Knoten hat eine stabile ID. Referenzen dürfen:

- nicht ins Leere zeigen,
- keine Zyklen erzeugen,
- nicht auf nach dem Claim entstandene Evidenz zurückdatiert werden,
- nicht durch eine spätere Revision stillschweigend umgebogen werden.

## 5.2 Quellen- und Fundstellenartefakt

Für jede externe oder interne Quelle werden mindestens protokolliert:

- source_id,
- Titel/Bezeichnung, Autor oder herausgebende Stelle,
- Quellentyp und Primär-/Sekundärstatus,
- URL, Dokumentpfad oder Datensatzreferenz,
- Veröffentlichungs-, Versions- und Abrufzeitpunkt,
- Daten-Vintage und as-of-Zeit, soweit relevant,
- Inhalts-Hash oder begründetes **UNAVAILABLE**,
- präzise Fundstelle wie Seite, Abschnitt, Tabelle, Zeile, Zeitstempel oder Datensatzschlüssel,
- ausreichend enger extrahierter Fakt,
- Zugriffs- und Lizenzbeschränkung.

Suchergebnis, Snippet, LLM-Zusammenfassung oder nicht geöffnete Zitationsangabe gelten nicht als verifizierte Quelle.

## 5.3 Source-Verification-Protokoll

Eine Evidenzreferenz ist **qualified**, nur wenn alle anwendbaren Prüfungen bestanden sind:

1. **Identität:** Autor, Herausgeber, Dokument und Version sind eindeutig.
2. **Abruf:** Die tatsächlich verwendete Quelle wurde geöffnet oder als unveränderlicher Snapshot bereitgestellt.
3. **Fundstelle:** Der Locator führt zur behaupteten Passage, Zahl oder Datenzeile.
4. **Entailment:** Die Quelle trägt den extrahierten Fakt; sie wird nicht durch Auslassung, Vorzeichenwechsel oder Kontextverlust verfälscht.
5. **Zeitbezug:** Datum, as-of-Zeit, Daten-Vintage und Revisionsstatus passen zum Claim.
6. **Unabhängigkeit:** Als Bestätigung gezählte Quellen beruhen nicht lediglich auf derselben ungeprüften Ursprungsquelle.
7. **Konfliktprüfung:** Materielle Gegenbelege sind gesucht oder bekannte Widersprüche offengelegt.

Die Prüfung protokolliert Prüfer, Zeitpunkt, Methode und Ergebnis je Schritt. Ein bloßes „citation present“ ist kein bestandener Entailment-Test.

Im Evidence-Dokument werden die anwendbaren Prüfschritte unter **evidence_assessment.checks** mit **PASS / FAIL / NOT_APPLICABLE** protokolliert. **extraction_method** und **human_verified** werden nicht weggelassen. Eine alleinige LLM-Extraktion mit **human_verified = false** ist nicht qualified, solange kein davon unabhängiger deterministischer Entailment-/Locator-Check alle anwendbaren Kriterien bestanden hat.

Bei zeitlich veränderlichen Tatsachen MUSS die Quelle für den behaupteten as-of-Zeitpunkt aktuell genug sein. Eine heute korrekte Seite beweist nicht automatisch den historischen Informationsstand. Bei revidierbaren Daten gilt die Vintage-Regel aus **00 §8 / 01 §5.7 und §7.3 / 02 §E6 und §G5**.

## 5.4 Reproduzierbare Transformationen

Eine Transformation protokolliert:

- transform_id,
- Formel oder Code-/Notebook-/Query-Hash,
- Runtime und relevante Paketversionen,
- geordnete Input-IDs und Input-Hashes,
- Parameter, Einheiten, Missing-Value- und Rundungsregeln,
- Output und Output-Hash,
- Reproduktionsstatus und Toleranz.

Ein manuell kopierter Wert ohne überprüfbare Transformation ist kein **CALCULATED_VALUE**. Ist das Verfahren stochastisch oder modellbasiert, wird der Output grundsätzlich als **ESTIMATE** behandelt, sofern er nicht nur eine deterministische Nachbearbeitung eines bereits ausgewiesenen Estimates ist.

## 5.5 Evidence Grade als einzige Confidence-Klasse

Es werden ausschließlich die folgenden Evidence Grades verwendet:

- **SUFFICIENT**
- **LIMITED**
- **INSUFFICIENT**

Das LLM darf keine subjektive Confidence-Prozentzahl erfinden. Der Evidence Grade ist die einzige operative Vertrauensklassifikation. Er bewertet die Nachvollziehbarkeit und Beleglage des Claims, nicht automatisch seine wissenschaftliche Wahrheit, Kausalität oder wirtschaftliche Relevanz.

Für diese Dokumentversion lautet **evidence_assessment.ruleset_version = 1.0.0**. Jede Änderung der Grade-Regeln benötigt eine neue Ruleset-Version und ein MATERIAL-Delta.

Die Vergabe erfolgt in dieser Reihenfolge:

1. Trifft eine **INSUFFICIENT**-Bedingung zu, ist der Grade **INSUFFICIENT**.
2. Andernfalls: Sind alle typabhängigen **SUFFICIENT**-Bedingungen erfüllt, ist der Grade **SUFFICIENT**.
3. Andernfalls ist der Grade **LIMITED**.

### Zwingend INSUFFICIENT

Mindestens eine der folgenden Bedingungen erzwingt **INSUFFICIENT**:

- fehlende oder zirkuläre Evidence Chain,
- erfundene, nicht auffindbare oder nicht entailende Zitation,
- materieller Konflikt mit Status **OPEN** oder **ACCEPTED_UNCERTAINTY**,
- fehlende Daten-Vintage bei einem vintage-sensitiven Claim,
- Hash-, Einheiten-, Vorzeichen- oder Reproduktionsfehler,
- verletztes anwendbares Gate aus 00–04,
- offene kritische Fehler oder relevante offene Fehler ohne begrenzbaren Scope,
- nachträglich als Forecast ausgegebene Aussage,
- als **HUMAN_JUDGMENT** ausgegebene Aussage ohne authentifizierten menschlichen Review.

### Typabhängig SUFFICIENT

| Typ | Alle Bedingungen für SUFFICIENT |
|---|---|
| SOURCE_FACT | Mindestens eine qualified primäre oder autoritative Evidenzreferenz oder zwei qualified, voneinander unabhängige Sekundärquellen; korrekter Zeitbezug; kein ungelöster materieller Gegenbeleg. |
| CALCULATED_VALUE | Alle materiellen Input-Claims sind SUFFICIENT; Transformation ist vollständig versioniert; Reproduktion stimmt innerhalb der vorab erklärten Toleranz überein. |
| ESTIMATE | Input- und Datenherkunft sind SUFFICIENT; Methode, Annahmen, Schätzwert und Unsicherheit sind vollständig; alle anwendbaren methodischen und Tooling-Gates aus 00–04 sind bestanden oder ausdrücklich nicht erforderlich; Ergebnis ist reproduziert. |
| INFERENCE | Alle entscheidenden Prämissen sind SUFFICIENT; Schlussregel und Geltungsgrenze sind explizit; mindestens eine konkrete Alternativerklärung oder Gegeninformation wurde behandelt; kein unbelegter logischer Sprung bleibt. |
| FORECAST | Eintrag wurde vor Outcome unveränderlich ausgestellt; Ziel, Horizont, Einheit und Auflösungsregel sind vollständig; alle entscheidenden Input-Claims sind SUFFICIENT. Der Grade bewertet nur die Qualität bei Ausgabe, nicht den späteren Treffer. |
| HUMAN_JUDGMENT | Identifizierter menschlicher Reviewer, Rolle, Zeitpunkt, Grund, Scope, Vorwert/Neuwert und Evidence-Referenzen sind vollständig; das Urteil wird nicht als Ersatz für fehlende Evidenz oder ein nicht bestandenes Research-Gate verwendet. |

### LIMITED

**LIMITED** ist nur zulässig, wenn die Kette real und nachvollziehbar ist, keine zwingende **INSUFFICIENT**-Bedingung vorliegt, aber mindestens eine nichtkritische SUFFICIENT-Bedingung fehlt. Die Einschränkung wird feldgenau genannt.

Ein **LIMITED**-Claim darf als offene Hypothese oder gekennzeichnete Einschränkung berichtet werden. Er darf kein **PASS**, keine Aktivierung, keinen Kausalclaim und keine externe Handlungsempfehlung allein tragen.

## 5.6 Aggregation und Entscheidungsregel

Evidence Grades werden nicht gemittelt. Für eine Entscheidung gilt der schwächste entscheidungstragende Claim.

- Alle entscheidungstragenden Claims **SUFFICIENT** → operative Evidence-Prüfung kann **PASS** sein.
- Mindestens ein entscheidungstragender Claim **LIMITED** → operative Evidence-Prüfung **BLOCKED**.
- Mindestens ein entscheidungstragender Claim **INSUFFICIENT** → operative Evidence-Prüfung **FAIL**.

Nicht entscheidungstragende **LIMITED**- oder **INSUFFICIENT**-Claims bleiben nur erhalten, wenn sie sichtbar als Unsicherheit, Gegenhypothese oder verworfene Aussage markiert sind.

---

# 6. Observability

## 6.1 Append-only Trace

Jeder Lauf führt einen append-only Trace mit:

- run_id,
- fortlaufender sequence_no,
- event_id,
- event_type,
- timestamp in UTC,
- span_id und optional parent_span_id,
- actor und Komponente,
- Input- und Output-Referenzen samt Hash,
- Status, Dauer und Attempt,
- Fehlerreferenz,
- Ressourcenverbrauch.

Mindestens folgende Ereignistypen werden erfasst:

- **RUN_CREATED**
- **RUN_STARTED**
- **MODEL_CALL_STARTED / MODEL_CALL_FINISHED**
- **TOOL_CALL_STARTED / TOOL_CALL_FINISHED**
- **SOURCE_RETRIEVAL**
- **SOURCE_VERIFICATION**
- **CLAIM_RECORDED**
- **TRANSFORM_EXECUTED**
- **SCHEMA_VALIDATION**
- **EVAL_EXECUTED**
- **REVIEW_RECORDED**
- **DELTA_CLASSIFIED**
- **FORECAST_ISSUED / FORECAST_RESOLVED**
- **RUN_FINISHED**

Fehlgeschlagene und abgebrochene Aufrufe bleiben sichtbar. Ein Trace darf nicht nachträglich so bereinigt werden, dass Fehlversuche, Retries oder Warnungen verschwinden.

## 6.2 Tool- und Modelltelemetrie

Für jeden Aufruf werden, soweit verfügbar, protokolliert:

- Tool-/Modellname und exakte Version,
- Operation oder Endpoint,
- Start, Ende und Dauer,
- Request-/Response-Hash,
- Statuscode oder Ergebnisstatus,
- Retryability und Attempt,
- Input-, Output-, Cache- und Reasoning-Tokens,
- Kostenbetrag, Währung und Preisversion,
- Rate-Limit-, Timeout- und Warninformationen.

Unverfügbare Messwerte werden als **UNAVAILABLE** markiert. Sie werden weder mit null gleichgesetzt noch geschätzt, außer die Schätzung ist ausdrücklich als solche gekennzeichnet und ihre Formel ist gespeichert.

## 6.3 Operative Mindestmetriken

Je Lauf werden mindestens abgeleitet:

- Gesamtdauer und Dauer je Phase/Span,
- Anzahl Modell-, Tool- und Retrievalaufrufe,
- Fehler und Retries nach Stage und Code,
- Token- und Kostenverbrauch,
- Anzahl Claims je Typ und Evidence Grade,
- Quellen-Prüfquote,
- offene Reviews und Deltas,
- Eval- und Gate-Ergebnisse.

Diese Metriken dienen Diagnose und Kostenkontrolle. Sie sind keine Evidenz für einen Markt-Edge.

---

# 7. Error Taxonomy und Fehlerbehandlung

## 7.1 Pflichtfelder

Jeder Fehler erhält:

- error_id,
- run_id und betroffenen span_id,
- **stage**,
- stabilen **code**,
- Severity **WARNING / ERROR / CRITICAL**,
- retryable **true / false**,
- Zeitpunkt und betroffene Artefakte/Claims,
- beobachtetes Symptom und belegte Ursache, soweit bekannt,
- Auswirkung auf Ergebnis, Evidence Grade und Gates,
- Retry-/Mitigationsaktion,
- Status **OPEN / MITIGATED / RESOLVED / ACCEPTED_RISK**,
- Resolver oder menschlichen Risk Owner.

**ACCEPTED_RISK** ist nur durch ein menschliches Review zulässig und verwandelt weder einen Fehler in Erfolg noch **INSUFFICIENT** in **SUFFICIENT**.

## 7.2 Stages und Standardcodes

Die Stage verwendet ausschließlich:

- **INITIALIZATION**
- **PROMPTING**
- **MODEL**
- **TOOL**
- **RETRIEVAL**
- **VALIDATION**
- **PERSISTENCE**
- **FINALIZATION**

Folgende Codes bilden das verbindliche Kernvokabular; projektspezifische Erweiterungen werden versioniert und namespaced:

| Stage | Kerncodes |
|---|---|
| INITIALIZATION | INIT_CONFIG_INVALID, INIT_DEPENDENCY_MISSING, INIT_PERMISSION_DENIED |
| PROMPTING | PROMPT_VERSION_MISSING, PROMPT_RENDER_FAILED, PROMPT_CONTEXT_OVERFLOW, PROMPT_CONTEXT_TRUNCATED |
| MODEL | MODEL_UNAVAILABLE, MODEL_TIMEOUT, MODEL_REFUSAL, MODEL_OUTPUT_INVALID, MODEL_INSTRUCTION_VIOLATION |
| TOOL | TOOL_UNAVAILABLE, TOOL_TIMEOUT, TOOL_API_ERROR, TOOL_OUTPUT_INVALID, TOOL_VERSION_DRIFT |
| RETRIEVAL | SOURCE_UNREACHABLE, SOURCE_AUTH_FAILED, SOURCE_LOCATOR_MISMATCH, SOURCE_STALE, SOURCE_CONTRADICTION, CITATION_NOT_ENTAILED |
| VALIDATION | SCHEMA_INVALID, REFERENCE_DANGLING, HASH_MISMATCH, CALCULATION_MISMATCH, EVIDENCE_INSUFFICIENT, METHOD_GATE_VIOLATION, EVAL_REGRESSION, MULTI_AGENT_CONFLICT, FORECAST_PROTOCOL_VIOLATION, POLICY_VIOLATION |
| PERSISTENCE | WRITE_FAILED, ARTIFACT_MISSING, IMMUTABILITY_VIOLATION |
| FINALIZATION | MANIFEST_INCOMPLETE, OPEN_CRITICAL_ERROR, REVIEW_REQUIRED, DELTA_UNRESOLVED |

## 7.3 Severity und Laufwirkung

| Severity | Verbindliche Wirkung |
|---|---|
| WARNING | Lauf darf fortfahren; Auswirkung und Scope werden genannt. Ein betroffener Claim ist höchstens LIMITED, bis die Warnung nachweislich folgenlos oder gelöst ist. |
| ERROR | Betroffener Schritt ist nicht erfolgreich. Abhängige Schritte stoppen; der Lauf endet mindestens PARTIAL, bei Pflichtschritt FAILED. |
| CRITICAL | Sofortiger Stopp aller abhängigen Schritte. Entscheidungstragende Outputs sind unzulässig; terminaler Status FAILED. |

Eine unbekannte Ursache wird als solche protokolliert. Sie darf nicht durch eine plausible Erzählung ersetzt werden.

## 7.4 Retry und Recovery

- Nur **retryable = true** erlaubt einen automatischen Retry.
- Ein Retry wiederholt dieselbe Operation mit denselben fachlichen Inputs.
- Jeder Retry bleibt im Trace.
- Nach Erreichen der vorab gesetzten Grenze wird der Fehler offen eskaliert.
- Fallbacks, die Modell, Datenquelle, Prompt, Methode oder Tool ändern, erzeugen einen neuen Lauf und ein Delta.
- Ein Fallback darf keine geringere Evidenzqualität unsichtbar machen.

---

# 8. Human Review, Korrektur und Override

## 8.1 Review-Aktionen und Status

Ein Review-Dokument verwendet als **action** ausschließlich:

- **CORRECTION**
- **OVERRIDE**
- **APPROVAL**
- **REJECTION**
- **ANNOTATION**

Der Review-Status lautet:

- **PROPOSED**
- **APPROVED**
- **REJECTED**
- **APPLIED**
- **SUPERSEDED**
- **WITHDRAWN**

Der Audit-Trail verwendet:

- **CREATED**
- **APPROVED**
- **REJECTED**
- **APPLIED**
- **SUPERSEDED**
- **WITHDRAWN**
- **COMMENTED**

## 8.2 Unveränderliche Review-Schicht

Ein Review editiert niemals den ursprünglichen Run, Claim oder Tooloutput. Es erzeugt eine neue, signierte beziehungsweise authentifizierte Schicht mit:

- review_id und Audit-Ereignissen,
- Reviewer-Identität und Rolle,
- Zeitstempel,
- Scope und betroffenen Objekt-IDs,
- action und status,
- altem und vorgeschlagenem/neuem Wert,
- reason_code und Freitextbegründung,
- Evidence- und Fehlerreferenzen,
- Gültigkeitsdauer oder Review-Trigger,
- zweitem Reviewer, falls durch Projektregel verlangt.

Die abgeleitete aktuelle Sicht wird aus Original plus angewendeten Reviews berechnet. Originalwerte bleiben prüfbar.

**before_hash**, **after_hash**, **record_hash**, **event_hash** und **previous_event_hash** sind schema-konforme SHA-256-Werte. **record_hash** versiegelt die RFC-8785-kanonisierten unveränderlichen Kernfelder; **status** und der append-only **audit_trail** werden nach der im Review-Schema definierten Hashkettenlogik fortgeschrieben.

## 8.3 Unterschied zwischen Correction und Override

- **CORRECTION** behebt einen nachweisbaren Übertragungs-, Rechen-, Referenz- oder Klassifikationsfehler. Der Beleg für die Korrektur ist Pflicht.
- **OVERRIDE** ist eine bewusst abweichende menschliche Entscheidung. Er wird als **HUMAN_JUDGMENT** geführt und darf die zugrunde liegende Evidenz oder den methodischen Gate-Status nicht umetikettieren.

Ein Override darf insbesondere nicht:

- **FAIL** oder **BLOCKED** in **PASS** umschreiben,
- einen **LIMITED**- oder **INSUFFICIENT**-Claim zu **SUFFICIENT** erklären,
- verbrauchte Validation-Daten wieder unabhängig machen,
- eine nachträgliche Hypothesenrevision als ursprünglichen Forecast darstellen,
- ein LLM-Urteil rückwirkend als menschlich ausgeben.

Materielle Research-Änderungen folgen **00 §9 und §16**, **01 §14 und §21** sowie **02 §O, §P und §Z**: neue Research-Version, korrekte Datenrollen und neuer Lauf.

## 8.4 Zwingendes Human-Review-Gate

Ein identifizierter Mensch MUSS prüfen:

- jeden OVERRIDE,
- jeden entscheidungstragenden HUMAN_JUDGMENT-Claim,
- jede Freigabe trotz akzeptiertem Risiko,
- jedes MATERIAL- oder BREAKING-Delta mit Außen- oder Aktivierungswirkung,
- jede Aktualisierung der Eval-Baseline,
- jede externe Freigabe der Zustände VALIDATED_PHENOMENON, ACTIVE_STRATEGY_CANDIDATE, ACTIVE, REVALIDATED oder SUSPENDED.

Dieses Review ist ein zusätzliches operatives Freigabegate. Es entscheidet nicht rückwirkend das fachliche Research-Gate.

Ein AI-Agent darf weder die menschliche Identität simulieren noch sein eigenes Ergebnis als Human Review freigeben.

---

# 9. Delta Detection

## 9.1 Baseline

Jeder vergleichende Lauf benennt genau eine Baseline:

1. bevorzugt den letzten menschlich freigegebenen Lauf derselben Research-Version,
2. sonst einen ausdrücklich benannten Baseline-Lauf,
3. fehlt beides, lautet die Delta-Klasse **UNKNOWN**.

Baseline und aktueller Lauf werden über kanonisierte Manifeste, Artefakthashes und stabile Claim-IDs verglichen.

## 9.2 Vergleichsdimensionen

Der Delta Report umfasst mindestens:

- Research-, Hypothesen-, DAG-, Estimand-, Tooling- und Kostenmodellversion,
- Datenquellen, Vintages, Rollen und Input-Hashes,
- Modell, Snapshot, Prompt, Kontext, Tools und Runtime,
- Claims, Claim-Typen, Evidence Grades und Evidence Chains,
- Gate-, Review- und Endstatus,
- Forecasts und Forecast-Auflösungen,
- Laufzeit, Kosten und Fehlermuster.

## 9.3 Delta-Klassen

| Klasse | Regel |
|---|---|
| NONE | Alle verglichenen semantischen und operativen Felder sowie relevanten Hashes sind identisch. |
| NON_MATERIAL | Nur Darstellung, zusätzliche Telemetrie, Kosten/Latenz oder eine nachweislich nicht semantische Metadatenkorrektur ändert sich. |
| MATERIAL | Inputs, Modell/Prompt/Tool/Runtime, ein materieller Claim, Evidence Grade, Forecast, Review oder Ergebnis ändert sich, ohne dass bereits eine Breaking-Bedingung vorliegt. |
| BREAKING | Ein bisher entscheidungstragender Claim wird INSUFFICIENT oder materiell widerlegt; ein PASS wird zu FAIL/BLOCKED; eine Quelle wird zurückgezogen; Integrität bricht; oder ein eingefrorenes materielles Designfeld ändert sich ohne erforderliche neue Research-Version. |
| UNKNOWN | Vergleich ist wegen fehlender Baseline, Hashes, Lineage oder nicht interpretierbarer Schemadifferenz nicht belastbar. |

Ein gleich gebliebenes Endfazit macht einen Modell-, Prompt-, Daten- oder Toolwechsel nicht automatisch **NON_MATERIAL**.

## 9.4 Gate-Folgen

- **NONE / NON_MATERIAL:** Delta wird protokolliert; automatische Freigabe ist nur zulässig, wenn alle übrigen Gates PASS sind.
- **MATERIAL:** relevante Evals nach §11 und bei Außen-/Aktivierungswirkung Human Review nach §8 sind Pflicht.
- **BREAKING:** operative Freigabe wird blockiert; abhängige Artefakte werden als reviewbedürftig markiert. Die Forschungsfolgen richten sich nach 00–04.
- **UNKNOWN:** keine automatische Freigabe; Status mindestens BLOCKED, bis der Vergleich möglich oder die fehlende Baseline menschlich begründet akzeptiert ist.

Der Delta Detector darf bestehende Artefakte nicht löschen oder umschreiben. Er erzeugt einen neuen Report.

---

# 10. Forecast Ledger

## 10.1 Abgrenzung

Die Vorhersage-Liste in **01 §12.1 / 02 §J** beschreibt erwartete Konsequenzen einer Hypothese. Sobald eine solche Aussage künftig beobachtbar und bewertbar ist, wird sie zusätzlich vor dem Outcome im append-only Forecast Ledger eingefroren.

## 10.2 Pflichtfelder bei Ausgabe

Jeder Forecast enthält:

- forecast_id, claim_id, run_id, research_id und Hypothesenbezug,
- issued_at und as_of,
- Zielobjekt, Zielvariable, Einheit und Population,
- Horizont, Deadline und zulässiges Beobachtungsfenster,
- Richtung, Punktwert, Intervall oder Kategorie,
- Evidenzstand und Evidence Grade bei Ausgabe,
- Auflösungsquelle, genaue Resolution Rule und geplanten Auflösungszeitpunkt,
- Scoring-Regel, falls eine Kennzahl verwendet wird,
- Status **OPEN**.

Wahrscheinlichkeiten sind nur zulässig, wenn sie aus einem benannten, versionierten und kalibrierten Modell oder einer dokumentierten Referenzklasse stammen. Eine frei erfundene LLM-Prozentzahl ist unzulässig. Ohne belastbare Kalibrierung wird eine kategoriale, gerichtete oder intervallbasierte Prognose verwendet.

## 10.3 Unveränderlichkeit und Revision

Nach **issued_at** werden Forecast-Text, Ziel, Horizont und Resolution Rule nicht geändert. Eine Korrektur erzeugt einen neuen Forecast mit **supersedes_forecast_id**; der alte bleibt offen beziehungsweise wird mit begründetem Status **VOID** abgeschlossen.

Ein Forecast darf nicht nach Beginn seines Outcome-Fensters rückdatiert werden. Ein Verstoß ist **FORECAST_PROTOCOL_VIOLATION**, Evidence Grade **INSUFFICIENT** und operative Freigabe **FAIL**.

## 10.4 Auflösung

Zulässige Status sind:

- **OPEN**
- **RESOLVED**
- **UNRESOLVED**
- **EXPIRED**
- **VOID**

Bei Auflösung werden tatsächlicher Wert, Quelle, Vintage, Resolver, resolved_at, angewendete Regel und Score ergänzt. Ist das Outcome nicht eindeutig oder die Quelle nicht qualified, wird **UNRESOLVED** statt Treffer oder Fehler vergeben.

Mehrdeutige Auflösungen benötigen Human Review. Ein späteres Outcome darf den ursprünglichen Forecast oder dessen Evidence Grade bei Ausgabe nicht verändern.

## 10.5 Auswertung

Forecasts werden nur innerhalb vorab definierter, vergleichbarer Familien aggregiert. Mindestens berichtet werden:

- Anzahl ausgegebener, aufgelöster und nicht auflösbarer Forecasts,
- Coverage,
- für probabilistische Forecasts Brier- oder vorab definierter Proper Score,
- für Punkt-/Intervallprognosen vorab definierte Fehler- und Coverage-Maße,
- für Richtungsprognosen Trefferquote plus passende Nullreferenz,
- Ergebnisse nach Horizont und Forecast-Familie.

Nachträgliche Auswahl nur erfolgreicher Forecasts ist unzulässig.

---

# 11. Kontrollierte Improvement Loop und Agenten-Evals

## 11.1 Abgrenzung

Die Agenten-Evals prüfen, ob Änderungen am LLM-System die operative Qualität verschlechtern. Sie sind von der statistischen Pipeline-Integritätsprüfung aus **01 §13.1 / 02 §N4 / 03 §17** getrennt.

Verbindliche Artefakte sind:

- **evals/catalog.v1.json** mit **schema_version = eval-catalog.v1**,
- **evals/examples/smoke-results.v1.json** mit **schema_version = eval-results.v1**,
- **evals/baseline.v1.json** mit **schema_version = eval-baseline.v1**,
- **evals/run_evals.py**,
- **evals/tests/test_run_evals.py**,
- **evals/README.md**.

## 11.2 Verbindlicher Ablauf

Jede Verbesserung folgt genau dieser Reihenfolge:

1. **Fehler erfassen:** Error-, Claim-, Trace- und Run-Referenzen sichern.
2. **Testfall vor Änderung:** minimalen reproduzierbaren Fall oder eine verallgemeinerte Erwartung in den Eval-Katalog aufnehmen.
3. **Baseline messen:** unverändertes System auf demselben eingefrorenen Katalog ausführen.
4. **Eine versionierte Änderung:** Prompt, Modell, Tool, Router, Schema oder Code eindeutig benennen.
5. **Kandidat messen:** gleiche Fälle und gleiche Randbedingungen; nur die beabsichtigte Änderung darf differieren.
6. **Regression Gate:** Struktur, Mindestwerte und Baseline-Policy prüfen.
7. **Human Review:** Ergebnis, Risiken, Scope und Rollback freigeben.
8. **Release und Monitoring:** Baseline bewusst aktualisieren, Änderung ausrollen und Deltas beobachten.

Ein Agent darf sich nicht direkt selbst modifizieren, Evals entfernen, Schwellen senken oder Baselines überschreiben, nur um einen Lauf bestehen zu lassen.

## 11.3 Pflichtmetriken und Mindestwerte

| Metrik | Mindestwert |
|---|---:|
| overall_score | 0,95 |
| critical_assertion_pass_rate | 1,00 |
| citation_accuracy | 0,95 |
| epistemic_classification_accuracy | 0,95 |
| unknown_safety_rate | 1,00 |
| contradiction_handling_rate | 1,00 |
| source_freshness_rate | 1,00 |
| calculation_accuracy | 1,00 |
| thesis_governance_accuracy | 1,00 |

Zusätzlich gilt:

- **max_metric_drop = 0**
- **max_case_drop = 0**

Eine Verbesserung des Gesamtscores kompensiert keinen Rückgang einer einzelnen Pflichtmetrik oder eines einzelnen Falls.

## 11.4 Runner- und Freigaberegel

Der Runner verwendet:

- Exit **0**: Struktur und Qualitäts-/Regressionsgates bestanden,
- Exit **1**: Qualitäts- oder Regressionsfehler,
- Exit **2**: harter Struktur-/Konfigurationsfehler.

Nur Exit 0 darf ein Eval-Gate **PASS** erzeugen. Exit 1 oder 2 blockiert die Freigabe der Änderung.

Die Baseline wird nur nach dokumentierter menschlicher **APPROVAL** aktualisiert. Eval-Fälle, die durch das Training oder die Änderung direkt bekannt wurden, werden als Development-Evals gekennzeichnet; ein separater geschützter Holdout bleibt nötig, sobald systematische Optimierung beginnt.

## 11.5 Rollback

Jede freigegebene Änderung nennt:

- vorherige freigegebene Version,
- Rollback-Auslöser,
- ausführbaren Rückweg,
- betroffene Artefakte,
- Owner.

Ein Rollback löscht keine fehlgeschlagenen Läufe oder Deltas.

---

# 12. Multi-Agent-Gate

## 12.1 Default

Ein Einzelagent ist der operative Default. Mehrere Agenten werden nur eingesetzt, wenn Aufgabentrennung, unabhängige Prüfung oder Parallelisierung einen konkret benannten Nutzen hat. Mehr Agenten sind kein Evidenzgewinn an sich.

Genau ein **coordinator_run_id** trägt die Endverantwortung. Jeder beitragende Agent erhält einen eigenen Child-Run mit **parent_run_id**.

## 12.2 Pflichtplan vor Delegation

Vor dem Start werden protokolliert:

- Zweck der Delegation,
- abgegrenzter Auftrag je Agent,
- erlaubte Inputs, Tools und Schreibbereiche,
- erwartete Artefakte und Akzeptanzkriterien,
- Budget und Abbruchregel,
- Abhängigkeiten und Merge-Reihenfolge,
- ob eine Prüfung tatsächlich unabhängig sein soll.

Zwei Agenten dürfen dasselbe kanonische Artefakt nicht gleichzeitig besitzen. Beiträge werden separat erzeugt und durch den Coordinator zusammengeführt. Gemeinsame Dateizugriffe ohne Ownership- oder Merge-Regel sind unzulässig.

## 12.3 Unabhängigkeit

Ein als unabhängig deklarierter Prüfer darf den zu prüfenden Schluss, die Begründung oder die Bewertung des Erzeuger-Agenten nicht als Evidenz übernehmen. Er erhält nur die für die Prüfung erforderlichen Inputs und Akzeptanzregeln. Ob und wann Ergebnisse gegenseitig sichtbar waren, wird protokolliert.

Mehrheitsvotum ersetzt weder Source Verification noch Methodengate noch Human Review.

## 12.4 Gate-Status

Der Status lautet:

- **NOT_USED**
- **PASS**
- **FAIL**
- **BLOCKED**

**PASS** erfordert gleichzeitig:

1. vollständigen Delegationsplan,
2. gültige Run Manifeste aller Child-Runs,
3. eindeutige Schreib- und Artefakt-Ownership,
4. vollständige Lineage jedes übernommenen Claims und Artefakts,
5. dokumentierte Konflikt- und Widerspruchsauflösung,
6. erneute Schema-, Hash-, Evidence- und Source-Prüfung durch den Coordinator,
7. vollständige Fehler-, Kosten- und Retry-Telemetrie,
8. reproduzierbare Ableitung des finalen Outputs aus akzeptierten Child-Artefakten,
9. keine offenen ERROR- oder CRITICAL-Konflikte.

**FAIL** gilt insbesondere bei:

- fehlender Child-Run-Lineage,
- übernommenem unbelegtem Claim,
- verdecktem Schreibkonflikt,
- zyklischer Delegation,
- fingierter Unabhängigkeit,
- ungelöstem materiellen Widerspruch,
- Nutzung mehrerer Agenten zur Umgehung eines Gates.

**BLOCKED** gilt, wenn ein erforderlicher Child-Run, Konfliktentscheid oder Artefakt fehlt.

Ein Child-Agent darf weder Evidence Grades noch methodische Gates des Coordinator-Laufs allein hochstufen.

---

# 13. Operatives Release Gate

Vor Abschluss eines entscheidungstragenden Laufs werden folgende Teilgates ausgewiesen:

| Teilgate | Status |
|---|---|
| RUN_MANIFEST | PASS / FAIL / BLOCKED |
| ARTIFACT_INTEGRITY | PASS / FAIL / BLOCKED |
| EVIDENCE_CHAIN | PASS / FAIL / BLOCKED |
| SOURCE_VERIFICATION | PASS / FAIL / BLOCKED |
| OBSERVABILITY | PASS / FAIL / BLOCKED |
| ERROR_STATE | PASS / FAIL / BLOCKED |
| DELTA | PASS / FAIL / BLOCKED / NOT_REQUIRED |
| FORECAST_LEDGER | PASS / FAIL / BLOCKED / NOT_REQUIRED |
| AGENT_EVAL | PASS / FAIL / BLOCKED / NOT_REQUIRED |
| MULTI_AGENT | PASS / FAIL / BLOCKED / NOT_USED |
| HUMAN_REVIEW | PASS / FAIL / BLOCKED / NOT_REQUIRED |

Das Gesamtgate lautet:

- **PASS**, wenn jedes anwendbare Teilgate PASS und Multi-Agent gegebenenfalls PASS oder NOT_USED ist,
- **FAIL**, sobald ein Teilgate FAIL ist,
- **BLOCKED**, wenn kein FAIL, aber mindestens ein anwendbares Teilgate BLOCKED ist.

Nur Gesamtgate **PASS** erlaubt **status = SUCCEEDED** für einen entscheidungstragenden Auftrag.

**PARTIAL** ist zulässig, wenn sichere, klar abgegrenzte Teilartefakte vorliegen. Diese dürfen weder als vollständige Phase noch als freigegebene Entscheidung ausgegeben werden.

---

# 14. Minimaler Ausführungsablauf

1. Run-ID erzeugen und Manifest mit **QUEUED** anlegen.
2. Research-, Prompt-, Modell-, Tool-, Daten- und Baseline-Versionen fixieren.
3. Manifest gegen Schema validieren; Status **RUNNING**.
4. Jeden Modell-, Tool- und Retrievalschritt im Trace erfassen.
5. Materielle Claims typisieren und Evidence Chains aufbauen.
6. Quellen verifizieren und Evidence Grades deterministisch berechnen.
7. Fehler klassifizieren und abhängige Schritte gegebenenfalls stoppen.
8. Forecasts vor Outcome im Ledger einfrieren.
9. Delta gegen Baseline bestimmen.
10. Bei Systemänderung Evals ausführen.
11. Bei Delegation Multi-Agent-Gate ausführen.
12. Erforderliches Human Review einholen.
13. Operatives Release Gate berechnen.
14. Manifest samt Output-Hashes terminal finalisieren.

---

# 15. Maschinenprüfbare Invarianten

Ein Validator MUSS mindestens folgende Verstöße erkennen:

1. terminaler Run ohne Manifest oder Endzeit,
2. **SUCCEEDED** ohne bestandenes operatives Release Gate,
3. materieller Claim ohne run_id, Typ, Evidence Chain oder Evidence Grade,
4. dangling oder zyklische Evidence-Referenz,
5. SOURCE_FACT ohne Fundstelle,
6. CALCULATED_VALUE ohne reproduzierbare Inputs und Transformation,
7. FORECAST ohne vor Outcome erzeugten Ledger-Eintrag,
8. HUMAN_JUDGMENT ohne authentifiziertes Human Review,
9. subjektive LLM-Confidence-Prozentzahl ohne kalibriertes Forecast-Modell,
10. nicht geloggter Modell-, Tool- oder Retry-Aufruf,
11. terminaler Lauf mit offenem CRITICAL-Fehler,
12. Override, der ein Originalartefakt überschreibt,
13. MATERIAL/BREAKING/UNKNOWN-Delta ohne vorgeschriebene Folge,
14. Eval-Baseline-Änderung ohne Human Approval,
15. Multi-Agent-Beitrag ohne Child-Run-Lineage,
16. operatives Artefakt, das ein Research-Gate aus 00–04 eigenmächtig hochstuft.

Ein Verstoß gegen eine dieser Invarianten führt mindestens zu **BLOCKED**, bei Integritäts-, Provenance-, Forecast- oder Gate-Manipulation zu **FAILED**.

---

# 16. Abschlussregel

Ein Agent darf einen Lauf erst dann als reproduzierbar, belegbar oder freigegeben bezeichnen, wenn:

- Herkunft und Ausführung vollständig manifestiert sind,
- alle materiellen Claims klassifiziert und bis zu ihren Quellen oder Inputs rückverfolgbar sind,
- Evidence Grades regelbasiert statt durch Selbsteinschätzung entstanden sind,
- Fehler, Deltas, Forecasts und Reviews unveränderlich protokolliert sind,
- alle anwendbaren operativen Gates bestanden sind,
- und der fachliche Status aus 00–04 unverändert wahrheitsgemäß wiedergegeben wird.

Operative Sauberkeit ist eine notwendige Kontrollschicht. Sie ist kein Ersatz für unabhängige Daten, statistische Entscheidbarkeit, Identifikation, OOS-Validation oder wirtschaftliche Umsetzbarkeit.
