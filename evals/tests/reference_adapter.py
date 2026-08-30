#!/usr/bin/env python3
"""Test-only adapter that proves producer plumbing without claiming live quality."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        return 2
    request = json.load(sys.stdin)
    if "expected" in request or "expected" in request.get("case", {}):
        raise RuntimeError("blind adapter request leaked expected assertions")
    reference = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    case_id = request["case"]["case_id"]
    json.dump(reference["cases"][case_id], sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
