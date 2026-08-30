#!/usr/bin/env python3
"""Produce eval-results.v2 by invoking a real agent adapter per catalog case.

The producer deliberately never sends catalog expectations to the adapter.  It
supports a local command protocol and a small provider-neutral JSON/HTTP
protocol, keeping model invocation outside the scoring process.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

try:  # Package import in tests; direct import when executed as a script.
    from . import run_evals
except ImportError:  # pragma: no cover - exercised by CLI integration tests.
    import run_evals  # type: ignore


REQUEST_PROTOCOL = run_evals.PRODUCER_PROTOCOL
DEFAULT_TIMEOUT_SECONDS = 120


class ProducerError(RuntimeError):
    """Raised when an adapter cannot produce a valid case result."""


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Prevent bearer credentials from following redirects to another origin."""

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_case_request(catalog: Mapping[str, Any], case: Mapping[str, Any]) -> dict[str, Any]:
    """Build the blind request envelope; expected assertions are never included."""

    return {
        "protocol_version": REQUEST_PROTOCOL,
        "catalog": {
            "catalog_id": catalog["catalog_id"],
            "catalog_version": catalog["catalog_version"],
        },
        "case": {
            "case_id": case["case_id"],
            "capability": case["capability"],
            "description": case["description"],
            "input": case["input"],
        },
        "output_contract": {
            "description": "Return exactly one JSON object for this case and no prose.",
            "required_top_level_fields": ["claims"],
            "claim_required_fields": [
                "statement_class",
                "evidence_status",
                "source_ids",
            ],
            "statement_classes": sorted(run_evals.STATEMENT_CLASSES),
            "evidence_statuses": sorted(run_evals.EVIDENCE_STATUSES),
            "source_rule": "source_ids may reference only sources supplied in case.input.sources",
        },
    }


def _parse_json_object(raw: str, context: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProducerError(f"{context} returned invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ProducerError(f"{context} must return one JSON object")
    return value


def _configuration_hash(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _command_invoker(command: Sequence[str], timeout_seconds: int) -> Callable[[dict[str, Any]], dict[str, Any]]:
    if not command or not all(isinstance(part, str) and part for part in command):
        raise ProducerError("command-json must be a non-empty JSON array of strings")

    def invoke(request: dict[str, Any]) -> dict[str, Any]:
        case_id = request["case"]["case_id"]
        try:
            completed = subprocess.run(
                list(command),
                input=json.dumps(request, ensure_ascii=False),
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
                shell=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise ProducerError(f"command adapter failed for {case_id}: {exc}") from exc
        if completed.returncode != 0:
            stderr = completed.stderr.strip()[-2000:]
            raise ProducerError(
                f"command adapter exited {completed.returncode} for {case_id}: {stderr}"
            )
        return _parse_json_object(completed.stdout, f"command adapter for {case_id}")

    return invoke


def _http_invoker(
    endpoint: str,
    token_env: str | None,
    timeout_seconds: int,
    allow_insecure_http: bool,
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    if not endpoint.startswith("https://") and not allow_insecure_http:
        raise ProducerError("HTTP adapter endpoint must use HTTPS unless --allow-insecure-http is set")
    token = os.environ.get(token_env) if token_env else None
    if token_env and not token:
        raise ProducerError(f"token environment variable {token_env!r} is missing or empty")

    def invoke(request: dict[str, Any]) -> dict[str, Any]:
        case_id = request["case"]["case_id"]
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "research-framework-eval-producer/1",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        http_request = urllib.request.Request(
            endpoint,
            data=json.dumps(request, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            opener = urllib.request.build_opener(_NoRedirectHandler())
            with opener.open(http_request, timeout=timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read(2000).decode("utf-8", errors="replace")
            raise ProducerError(f"HTTP adapter returned {exc.code} for {case_id}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ProducerError(f"HTTP adapter failed for {case_id}: {exc}") from exc
        return _parse_json_object(body, f"HTTP adapter for {case_id}")

    return invoke


def produce_results(
    catalog: Mapping[str, Any],
    invoke: Callable[[dict[str, Any]], dict[str, Any]],
    *,
    run_id: str,
    run_kind: str,
    producer_type: str,
    adapter_id: str,
    configuration_sha256: str,
) -> dict[str, Any]:
    run_evals.validate_catalog(catalog)
    if not run_evals.ID_RE.fullmatch(run_id):
        raise ProducerError("run-id must be a lowercase stable identifier")
    if not run_evals.ID_RE.fullmatch(adapter_id):
        raise ProducerError("adapter-id must be a lowercase stable identifier")
    if run_kind not in run_evals.RUN_KINDS:
        raise ProducerError(f"unsupported run kind: {run_kind}")

    started_at = _utc_now()
    case_results: dict[str, Any] = {}
    for case in catalog["cases"]:
        request = build_case_request(catalog, case)
        case_results[case["case_id"]] = invoke(request)
    completed_at = _utc_now()

    results = {
        "schema_version": run_evals.RESULTS_SCHEMA_VERSION,
        "catalog_id": catalog["catalog_id"],
        "catalog_version": catalog["catalog_version"],
        "run_id": run_id,
        "created_at": completed_at,
        "run_kind": run_kind,
        "producer": {
            "producer_type": producer_type,
            "adapter_id": adapter_id,
            "request_protocol": REQUEST_PROTOCOL,
            "started_at": started_at,
            "completed_at": completed_at,
            "configuration_sha256": configuration_sha256,
        },
        "cases": case_results,
    }
    run_evals.validate_results(results, catalog)
    return results


def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        Path(temporary_name).replace(path)
    except OSError as exc:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)
        raise ProducerError(f"cannot write {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Invoke an agent adapter once per blind eval case and emit eval-results.v2."
    )
    parser.add_argument("--catalog", type=Path, default=root / "catalog.v1.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-kind", choices=sorted(run_evals.RUN_KINDS), default="LIVE_AGENT")
    parser.add_argument("--adapter-id", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    transport = parser.add_mutually_exclusive_group(required=True)
    transport.add_argument(
        "--command-json",
        help='JSON array command, e.g. ["python","my_agent_adapter.py"]',
    )
    transport.add_argument("--http-endpoint", help="JSON/HTTP endpoint receiving the request envelope")
    parser.add_argument("--token-env", help="Environment variable containing an HTTP bearer token")
    parser.add_argument("--allow-insecure-http", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        catalog = run_evals.load_json(args.catalog)
        if args.timeout_seconds <= 0:
            raise ProducerError("timeout-seconds must be positive")
        if args.command_json:
            command_value = json.loads(args.command_json)
            if (not isinstance(command_value, list)
                    or not command_value
                    or not all(isinstance(part, str) and part for part in command_value)):
                raise ProducerError("command-json must decode to a non-empty array of strings")
            command = command_value
            invoke = _command_invoker(command, args.timeout_seconds)
            producer_type = "COMMAND"
            configuration = {
                "producer_type": producer_type,
                "adapter_id": args.adapter_id,
                "command": command,
                "timeout_seconds": args.timeout_seconds,
            }
        else:
            invoke = _http_invoker(
                args.http_endpoint,
                args.token_env,
                args.timeout_seconds,
                args.allow_insecure_http,
            )
            producer_type = "HTTP_JSON"
            configuration = {
                "producer_type": producer_type,
                "adapter_id": args.adapter_id,
                "endpoint": args.http_endpoint,
                "token_env": args.token_env,
                "timeout_seconds": args.timeout_seconds,
            }
        results = produce_results(
            catalog,
            invoke,
            run_id=args.run_id,
            run_kind=args.run_kind,
            producer_type=producer_type,
            adapter_id=args.adapter_id,
            configuration_sha256=_configuration_hash(configuration),
        )
        _write_json_atomic(args.output, results)
    except (ProducerError, run_evals.FixtureError, json.JSONDecodeError) as exc:
        print(f"PRODUCER ERROR\n{exc}", file=sys.stderr)
        return 2

    print(
        f"PRODUCED: {args.output} run={results['run_id']} kind={results['run_kind']} "
        f"cases={len(results['cases'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
