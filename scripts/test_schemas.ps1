[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

function Read-JsonText {
    param([Parameter(Mandatory)][string]$RelativePath)

    return Get-Content -LiteralPath (Join-Path $repoRoot $RelativePath) -Raw
}

function Test-ValidFixture {
    param(
        [Parameter(Mandatory)][string]$Example,
        [Parameter(Mandatory)][string]$Schema
    )

    $json = Read-JsonText -RelativePath $Example
    $schemaPath = Join-Path $repoRoot $Schema
    $valid = $json | Test-Json -SchemaFile $schemaPath -ErrorAction SilentlyContinue
    if (-not $valid) {
        throw "Expected valid fixture was rejected: $Example"
    }
    Write-Output "PASS positive: $Example"
}

function Test-RejectedFixture {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][object]$Value,
        [Parameter(Mandatory)][string]$Schema
    )

    $json = $Value | ConvertTo-Json -Depth 100
    $schemaPath = Join-Path $repoRoot $Schema
    $valid = $json | Test-Json -SchemaFile $schemaPath -ErrorAction SilentlyContinue
    if ($valid) {
        throw "Expected invalid fixture was accepted: $Name"
    }
    Write-Output "PASS negative: $Name"
}

$positivePairs = @(
    @('examples\run_manifest.minimal.json', 'schemas\run_manifest.schema.json'),
    @('examples\evidence.minimal.json', 'schemas\evidence.schema.json'),
    @('examples\forecast.minimal.json', 'schemas\forecast.schema.json'),
    @('examples\review.minimal.json', 'schemas\review.schema.json')
)

foreach ($pair in $positivePairs) {
    Test-ValidFixture -Example $pair[0] -Schema $pair[1]
}

$runUnexpected = Read-JsonText -RelativePath 'examples\run_manifest.minimal.json' | ConvertFrom-Json -Depth 100
$runUnexpected | Add-Member -NotePropertyName 'unexpected_field' -NotePropertyValue $true
Test-RejectedFixture -Name 'run rejects additional property' -Value $runUnexpected -Schema 'schemas\run_manifest.schema.json'

$runGateMismatch = Read-JsonText -RelativePath 'examples\run_manifest.minimal.json' | ConvertFrom-Json -Depth 100
$runGateMismatch.operational_release.overall_status = 'FAIL'
Test-RejectedFixture -Name 'SUCCEEDED run requires release PASS' -Value $runGateMismatch -Schema 'schemas\run_manifest.schema.json'

$runHiddenGateFailure = Read-JsonText -RelativePath 'examples\run_manifest.minimal.json' | ConvertFrom-Json -Depth 100
$runHiddenGateFailure.operational_release.gates.evidence_chain = 'FAIL'
Test-RejectedFixture -Name 'release PASS cannot hide failed subgate' -Value $runHiddenGateFailure -Schema 'schemas\run_manifest.schema.json'

$evidenceMissingRevision = Read-JsonText -RelativePath 'examples\evidence.minimal.json' | ConvertFrom-Json -Depth 100
$evidenceMissingRevision.claims[0].PSObject.Properties.Remove('claim_revision')
Test-RejectedFixture -Name 'claim revision is required' -Value $evidenceMissingRevision -Schema 'schemas\evidence.schema.json'

$evidenceMissingLink = Read-JsonText -RelativePath 'examples\evidence.minimal.json' | ConvertFrom-Json -Depth 100
$evidenceMissingLink.claims[0].evidence_links = @()
Test-RejectedFixture -Name 'SOURCE_FACT requires evidence link' -Value $evidenceMissingLink -Schema 'schemas\evidence.schema.json'

$forecastUncalibrated = Read-JsonText -RelativePath 'examples\forecast.minimal.json' | ConvertFrom-Json -Depth 100
$forecastUncalibrated.forecasts[0].prediction.kind = 'PROBABILITY'
$forecastUncalibrated.forecasts[0].prediction.probability = 0.7
$forecastUncalibrated.forecasts[0].prediction.calibration_ref = $null
Test-RejectedFixture -Name 'probability forecast requires calibration' -Value $forecastUncalibrated -Schema 'schemas\forecast.schema.json'

$forecastPrematureResolution = Read-JsonText -RelativePath 'examples\forecast.minimal.json' | ConvertFrom-Json -Depth 100
$forecastPrematureResolution.forecasts[0].resolution = [PSCustomObject]@{
    resolved_at = '2026-09-01T08:00:00Z'
    resolved_by = [PSCustomObject]@{ actor_type = 'HUMAN'; actor_id = 'reviewer-001' }
    actual_value = 'UP'
    source_refs = @('official-close-dataset')
    source_vintage = '2026-08-31'
    applied_rule = 'Demonstrationsregel'
    score = 1
    rationale = 'Aufgelöst.'
}
Test-RejectedFixture -Name 'OPEN forecast cannot contain resolution' -Value $forecastPrematureResolution -Schema 'schemas\forecast.schema.json'

$reviewInvalidApplied = Read-JsonText -RelativePath 'examples\review.minimal.json' | ConvertFrom-Json -Depth 100
$reviewInvalidApplied.reviews[0].audit_trail = @(
    $reviewInvalidApplied.reviews[0].audit_trail | Where-Object { $_.event_type -ne 'APPLIED' }
)
Test-RejectedFixture -Name 'APPLIED review requires APPLIED audit event' -Value $reviewInvalidApplied -Schema 'schemas\review.schema.json'

Write-Output 'Schema contract tests passed: 4 positive, 8 negative.'
