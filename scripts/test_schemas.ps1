[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$script:PositiveCount = 0
$script:NegativeCount = 0

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
    $validationErrors = @()
    $valid = $json | Test-Json -SchemaFile $schemaPath -ErrorAction SilentlyContinue -ErrorVariable +validationErrors
    if (-not $valid) {
        $details = $validationErrors -join [Environment]::NewLine
        throw "Expected valid fixture was rejected: $Example`n$details"
    }
    $script:PositiveCount++
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
    $script:NegativeCount++
    Write-Output "PASS negative: $Name"
}

$positivePairs = @(
    @('examples\run_manifest.minimal.json', 'schemas\run_manifest.schema.json'),
    @('examples\evidence.minimal.json', 'schemas\evidence.schema.json'),
    @('examples\evidence.academic.json', 'schemas\evidence.schema.json'),
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

$evidenceInvalidUuid = Read-JsonText -RelativePath 'examples\evidence.minimal.json' | ConvertFrom-Json -Depth 100
$evidenceInvalidUuid.evidence_set_id = 'not-a-uuid'
Test-RejectedFixture -Name 'evidence set id requires UUID syntax' -Value $evidenceInvalidUuid -Schema 'schemas\evidence.schema.json'

$evidenceMissingLink = Read-JsonText -RelativePath 'examples\evidence.minimal.json' | ConvertFrom-Json -Depth 100
$evidenceMissingLink.claims[0].evidence_links = @()
Test-RejectedFixture -Name 'SOURCE_FACT requires evidence link' -Value $evidenceMissingLink -Schema 'schemas\evidence.schema.json'

$evidenceSufficientWithFailedCheck = Read-JsonText -RelativePath 'examples\evidence.minimal.json' | ConvertFrom-Json -Depth 100
$evidenceSufficientWithFailedCheck.overall_evidence_assessment.grade = 'SUFFICIENT'
$evidenceSufficientWithFailedCheck.overall_evidence_assessment.checks[0].outcome = 'FAIL'
Test-RejectedFixture -Name 'SUFFICIENT evidence rejects failed check' -Value $evidenceSufficientWithFailedCheck -Schema 'schemas\evidence.schema.json'

$academicMissingMetadata = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicMissingMetadata.sources[0].PSObject.Properties.Remove('academic_metadata')
Test-RejectedFixture -Name 'ACADEMIC source requires academic metadata' -Value $academicMissingMetadata -Schema 'schemas\evidence.schema.json'

$academicInvalidStatus = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicInvalidStatus.sources[0].academic_metadata.publication_status = 'FAMOUS_JOURNAL'
Test-RejectedFixture -Name 'academic publication status is controlled' -Value $academicInvalidStatus -Schema 'schemas\evidence.schema.json'

$academicInvalidArxivId = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicInvalidArxivId.sources[1].academic_metadata.arxiv.id = 'not-an-arxiv-id'
Test-RejectedFixture -Name 'arXiv id must be version-compatible' -Value $academicInvalidArxivId -Schema 'schemas\evidence.schema.json'

$academicNonQFinCategory = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicNonQFinCategory.sources[1].academic_metadata.arxiv.primary_category = 'cs.AI'
Test-RejectedFixture -Name 'arXiv category must be q-fin taxonomy' -Value $academicNonQFinCategory -Schema 'schemas\evidence.schema.json'

$academicMissingArxivVersion = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicMissingArxivVersion.sources[1].academic_metadata.arxiv.PSObject.Properties.Remove('version')
Test-RejectedFixture -Name 'arXiv source requires exact version' -Value $academicMissingArxivVersion -Schema 'schemas\evidence.schema.json'

$academicInvalidArxivMonth = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicInvalidArxivMonth.sources[1].academic_metadata.arxiv.id = '2699.12345'
Test-RejectedFixture -Name 'modern arXiv id requires valid month' -Value $academicInvalidArxivMonth -Schema 'schemas\evidence.schema.json'

$academicRetractionWithoutNotice = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicRetractionWithoutNotice.sources[0].academic_metadata.integrity.status = 'RETRACTED'
$academicRetractionWithoutNotice.sources[0].academic_metadata.integrity.notice_uri = $null
Test-RejectedFixture -Name 'retraction requires notice URI' -Value $academicRetractionWithoutNotice -Schema 'schemas\evidence.schema.json'

$academicOpenCodeWithoutUri = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicOpenCodeWithoutUri.sources[0].academic_metadata.code_availability.uris = @()
Test-RejectedFixture -Name 'open academic code requires URI' -Value $academicOpenCodeWithoutUri -Schema 'schemas\evidence.schema.json'

$academicInvalidCodeUri = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicInvalidCodeUri.sources[0].academic_metadata.code_availability.uris = @('not a uri')
Test-RejectedFixture -Name 'academic code URI requires a URI scheme' -Value $academicInvalidCodeUri -Schema 'schemas\evidence.schema.json'

$academicUnavailableCodeWithUri = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicUnavailableCodeWithUri.sources[0].academic_metadata.code_availability.status = 'NOT_AVAILABLE'
Test-RejectedFixture -Name 'unavailable academic code cannot expose resource URI' -Value $academicUnavailableCodeWithUri -Schema 'schemas\evidence.schema.json'

$academicNoNoticeWithUri = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicNoNoticeWithUri.sources[0].academic_metadata.integrity.notice_uri = 'https://example.org/notices/none'
Test-RejectedFixture -Name 'no-notice integrity status rejects notice URI' -Value $academicNoNoticeWithUri -Schema 'schemas\evidence.schema.json'

$academicInvalidTimestamp = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicInvalidTimestamp.sources[0].academic_metadata.integrity.checked_at = 'not-a-date'
Test-RejectedFixture -Name 'academic integrity check requires ISO timestamp' -Value $academicInvalidTimestamp -Schema 'schemas\evidence.schema.json'

$academicReplicationWithoutSource = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$academicReplicationWithoutSource.sources[0].academic_metadata.independent_replication.status = 'REPLICATED'
$academicReplicationWithoutSource.sources[0].academic_metadata.independent_replication.checked_at = '2026-08-30T08:10:00Z'
$academicReplicationWithoutSource.sources[0].academic_metadata.independent_replication.source_ids = @()
Test-RejectedFixture -Name 'positive replication status requires source reference' -Value $academicReplicationWithoutSource -Schema 'schemas\evidence.schema.json'

$nonAcademicWithMetadata = Read-JsonText -RelativePath 'examples\evidence.minimal.json' | ConvertFrom-Json -Depth 100
$academicTemplate = Read-JsonText -RelativePath 'examples\evidence.academic.json' | ConvertFrom-Json -Depth 100
$nonAcademicWithMetadata.sources[0] | Add-Member -NotePropertyName 'academic_metadata' -NotePropertyValue $academicTemplate.sources[0].academic_metadata
Test-RejectedFixture -Name 'non-academic source rejects academic metadata' -Value $nonAcademicWithMetadata -Schema 'schemas\evidence.schema.json'

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

Write-Output "Schema contract tests passed: $script:PositiveCount positive, $script:NegativeCount negative."
