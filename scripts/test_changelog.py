#!/usr/bin/env python3
"""Strukturpruefung des Aenderungsprotokolls.

Geprueft wird ausschliesslich die Struktur: Ueberschriftsform, Pflichtfelder,
Uebereinstimmung von Signaturname und Agent, Uebereinstimmung von Signaturdatum
und Ueberschriftsdatum sowie absteigende Datumsordnung.

Nicht geprueft wird, ob ein Eintrag inhaltlich zutrifft. Ein Protokolleintrag
bleibt Selbstdeklaration im Sinne der Enforcement-Grenze aus QUICKSTART
Abschnitt 1; diese Pruefung stellt nur sicher, dass die Deklaration vollstaendig
und zuordenbar ist.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"

MARKER = "<!-- EINTRAEGE -->"
HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — (.+)$")
FIELD = re.compile(r"^- \*\*([^:*]+):\*\* (.*)$")

REQUIRED = ("Agent", "Commit", "Was", "Warum", "Berührt", "Signatur")


def parse_entries(text: str) -> list[dict[str, Any]]:
    if MARKER not in text:
        raise SystemExit(f"FAIL: Marker {MARKER} fehlt in CHANGELOG.md")
    body = text.split(MARKER, 1)[1]

    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for number, line in enumerate(body.splitlines(), start=1):
        heading = HEADING.match(line)
        if heading:
            current = {
                "date": heading.group(1),
                "title": heading.group(2).strip(),
                "line": number,
                "fields": {},
            }
            entries.append(current)
            continue
        field = FIELD.match(line)
        if field and current is not None:
            current["fields"][field.group(1).strip()] = field.group(2).strip()
    return entries


def check(entries: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    if not entries:
        problems.append("kein Eintrag gefunden")
        return problems

    for entry in entries:
        label = f"Eintrag {entry['date']} '{entry['title']}'"
        fields = entry["fields"]

        for key in REQUIRED:
            if key not in fields:
                problems.append(f"{label}: Pflichtfeld '{key}' fehlt")
            elif not fields[key]:
                problems.append(f"{label}: Pflichtfeld '{key}' ist leer")

        try:
            date.fromisoformat(entry["date"])
        except ValueError:
            problems.append(f"{label}: Ueberschriftsdatum ist kein gueltiges Datum")

        agent = fields.get("Agent", "")
        signature = fields.get("Signatur", "")
        if agent and signature:
            name = agent.split("(")[0].strip()
            if not name:
                problems.append(f"{label}: Agent enthaelt keinen Namen")
            elif name not in signature:
                problems.append(
                    f"{label}: Signatur nennt nicht den Agenten '{name}'"
                )
            if entry["date"] not in signature:
                problems.append(
                    f"{label}: Signaturdatum weicht vom Ueberschriftsdatum ab"
                )

    dates = [entry["date"] for entry in entries]
    if dates != sorted(dates, reverse=True):
        problems.append("Eintraege stehen nicht in absteigender Datumsordnung")
    return problems


def main() -> int:
    if not CHANGELOG.exists():
        print("FAIL: CHANGELOG.md fehlt")
        return 1

    entries = parse_entries(CHANGELOG.read_text(encoding="utf-8"))
    problems = check(entries)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1

    print(f"PASS: {len(entries)} Protokolleintraege strukturell vollstaendig")
    print("PASS: jede Signatur nennt ihren Agenten und das Eintragsdatum")
    print("PASS: Eintraege stehen in absteigender Datumsordnung")
    signers = sorted({e["fields"]["Agent"] for e in entries})
    print(f"Changelog tests passed: {len(entries)} Eintraege, {len(signers)} Agent(en).")
    print("HINWEIS: Geprueft ist die Struktur, nicht der Wahrheitsgehalt eines Eintrags.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
