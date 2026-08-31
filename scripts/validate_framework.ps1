[CmdletBinding()]
param(
    [string]$PythonExecutable
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

if (-not $PythonExecutable) {
    $systemPython = Get-Command python -ErrorAction SilentlyContinue
    if ($systemPython) {
        $PythonExecutable = $systemPython.Source
    }
}

if (-not $PythonExecutable) {
    $codexPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $codexPython) {
        $PythonExecutable = $codexPython
    }
}

if (-not $PythonExecutable -or -not (Test-Path -LiteralPath $PythonExecutable)) {
    throw 'Keine Python-Laufzeit gefunden. Mit -PythonExecutable einen Python-3-Pfad übergeben.'
}

Write-Output '== Schema contracts =='
& (Join-Path $PSScriptRoot 'test_schemas.ps1')

Write-Output '== Strategy reconstruction =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_strategy_reconstruction.py')
if ($LASTEXITCODE -ne 0) {
    throw "Strategy-Reconstruction-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Strategy concept audit =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_strategy_concept_audit.py')
if ($LASTEXITCODE -ne 0) {
    throw "Strategy-Concept-Audit-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Condition inquiry =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_condition_inquiry.py')
if ($LASTEXITCODE -ne 0) {
    throw "Condition-Inquiry-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Scientific-philosophy review =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_scientific_philosophy_review.py')
if ($LASTEXITCODE -ne 0) {
    throw "Wissenschaftsphilosophie-Review-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Research orchestration =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_research_orchestration.py')
if ($LASTEXITCODE -ne 0) {
    throw "Research-Orchestration-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Entry thresholds =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_entry_thresholds.py')
if ($LASTEXITCODE -ne 0) {
    throw "Entry-Threshold-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Data snapshot contract =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_data_snapshot.py')
if ($LASTEXITCODE -ne 0) {
    throw "Data-Snapshot-Vertragstests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Hypothesis generator =='
& $PythonExecutable (Join-Path $repoRoot 'scripts\test_generator.py')
if ($LASTEXITCODE -ne 0) {
    throw "Hypothesen-Generator fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Eval smoke and regression gate =='
& $PythonExecutable (Join-Path $repoRoot 'evals\run_evals.py')
if ($LASTEXITCODE -ne 0) {
    throw "Eval-Runner fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Eval unit tests =='
& $PythonExecutable -m unittest discover -s (Join-Path $repoRoot 'evals\tests') -v
if ($LASTEXITCODE -ne 0) {
    throw "Eval-Unit-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output '== Ingest adapter offline tests =='
& $PythonExecutable -m unittest discover -s (Join-Path $repoRoot 'ingest\tests') -v
if ($LASTEXITCODE -ne 0) {
    throw "Ingest-Adapter-Tests fehlgeschlagen (Exit $LASTEXITCODE)."
}

Write-Output 'Framework integrity passed. LIVE_AGENT release gate was NOT run; use scripts/validate_framework.py --live-results <path> for a model or prompt release claim.'
