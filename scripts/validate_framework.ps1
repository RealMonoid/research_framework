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

Write-Output 'Framework validation passed.'
