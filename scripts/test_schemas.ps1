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
    @('examples\review.minimal.json', 'schemas\review.schema.json'),
    @('examples\constraint_assessment.causal_lever.json', 'schemas\constraint_assessment.schema.json'),
    @('examples\hypothesis_candidate.inbox.json', 'schemas\hypothesis_candidate.schema.json'),
    @('examples\hypothesis_candidate.rejected.json', 'schemas\hypothesis_candidate.schema.json'),
    @('examples\hypothesis_candidate.minimal.json', 'schemas\hypothesis_candidate.schema.json')
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

$causalLeverWithoutIdentification = Read-JsonText -RelativePath 'examples\constraint_assessment.causal_lever.json' | ConvertFrom-Json -Depth 100
$causalLeverWithoutIdentification.stage_gates.identification = 'FAIL'
Test-RejectedFixture -Name 'identified causal lever requires identification gate PASS' -Value $causalLeverWithoutIdentification -Schema 'schemas\constraint_assessment.schema.json'

$causalLeverWithoutEstimand = Read-JsonText -RelativePath 'examples\constraint_assessment.causal_lever.json' | ConvertFrom-Json -Depth 100
$causalLeverWithoutEstimand.estimand_ref = $null
Test-RejectedFixture -Name 'identified causal lever requires estimand reference' -Value $causalLeverWithoutEstimand -Schema 'schemas\constraint_assessment.schema.json'

$implementationConstraintBeforeValidation = Read-JsonText -RelativePath 'examples\constraint_assessment.causal_lever.json' | ConvertFrom-Json -Depth 100
$implementationConstraintBeforeValidation.label = 'IMPLEMENTATION_CONSTRAINT'
$implementationConstraintBeforeValidation.stage_gates.identification = 'NOT_REQUIRED'
$implementationConstraintBeforeValidation.stage_gates.phenomenon_validation = 'NOT_RUN'
$implementationConstraintBeforeValidation.stage_gates.implementation_feasibility = 'PASS'
$implementationConstraintBeforeValidation.estimand_ref = $null
$implementationConstraintBeforeValidation.system_objective = 'Executable risk-adjusted net performance'
$implementationConstraintBeforeValidation.bottleneck_metric = 'Median round-trip latency in milliseconds'
Test-RejectedFixture -Name 'implementation constraint requires validated phenomenon' -Value $implementationConstraintBeforeValidation -Schema 'schemas\constraint_assessment.schema.json'

$candidateUnexpected = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateUnexpected | Add-Member -NotePropertyName 'confidence_score' -NotePropertyValue 0.95
Test-RejectedFixture -Name 'hypothesis candidate rejects additional property' -Value $candidateUnexpected -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateInboxWithoutInformationBudget = Read-JsonText -RelativePath 'examples\hypothesis_candidate.inbox.json' | ConvertFrom-Json -Depth 100
$candidateInboxWithoutInformationBudget.PSObject.Properties.Remove('consumed_data_refs')
Test-RejectedFixture -Name 'INBOX candidate always records consumed information references' -Value $candidateInboxWithoutInformationBudget -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateInboxWithTransitionPayload = Read-JsonText -RelativePath 'examples\hypothesis_candidate.inbox.json' | ConvertFrom-Json -Depth 100
$candidateInboxWithTransitionPayload.transition | Add-Member -NotePropertyName 'screened_at' -NotePropertyValue $null
Test-RejectedFixture -Name 'INBOX candidate cannot pretend that screening already occurred' -Value $candidateInboxWithTransitionPayload -Schema 'schemas\hypothesis_candidate.schema.json'

$candidatePromotedWithoutScope = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidatePromotedWithoutScope.PSObject.Properties.Remove('research_scope')
Test-RejectedFixture -Name 'PROMOTED candidate requires full research scope' -Value $candidatePromotedWithoutScope -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateWithoutInstrument = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateWithoutInstrument.research_scope.instruments = @()
Test-RejectedFixture -Name 'hypothesis candidate scope requires an instrument' -Value $candidateWithoutInstrument -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateWithoutTimezone = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateWithoutTimezone.research_scope.PSObject.Properties.Remove('timezone')
Test-RejectedFixture -Name 'intraday scope requires explicit timezone' -Value $candidateWithoutTimezone -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateFilteredWithoutFeed = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateFilteredWithoutFeed.research_scope.news_event_coverage.feeds = @()
Test-RejectedFixture -Name 'FILTER_KNOWN_EVENTS requires named feed coverage' -Value $candidateFilteredWithoutFeed -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateFilteredWithoutWindow = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateFilteredWithoutWindow.research_scope.news_event_coverage.exclusion_windows = @()
Test-RejectedFixture -Name 'FILTER_KNOWN_EVENTS requires exclusion window' -Value $candidateFilteredWithoutWindow -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateFilteredWithoutProvider = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateFilteredWithoutProvider.research_scope.news_event_coverage.feeds[0].PSObject.Properties.Remove('provider')
Test-RejectedFixture -Name 'event feed coverage requires provider provenance' -Value $candidateFilteredWithoutProvider -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateFilteredWithoutTimestampPolicy = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateFilteredWithoutTimestampPolicy.research_scope.news_event_coverage.PSObject.Properties.Remove('timestamp_convention')
Test-RejectedFixture -Name 'event filtering requires an explicit timestamp convention' -Value $candidateFilteredWithoutTimestampPolicy -Schema 'schemas\hypothesis_candidate.schema.json'

$candidatePromotedWithoutAlternative = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidatePromotedWithoutAlternative.alternative_explanations = @()
Test-RejectedFixture -Name 'PROMOTED candidate requires alternative explanation' -Value $candidatePromotedWithoutAlternative -Schema 'schemas\hypothesis_candidate.schema.json'

$candidatePromotedWithoutResolution = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidatePromotedWithoutResolution.data_requirements.minimum_resolution = $null
Test-RejectedFixture -Name 'PROMOTED candidate requires concrete data resolution' -Value $candidatePromotedWithoutResolution -Schema 'schemas\hypothesis_candidate.schema.json'

$candidatePromotedWithUnknownQueue = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidatePromotedWithUnknownQueue.early_feasibility.queue.status = 'UNKNOWN'
$candidatePromotedWithUnknownQueue.early_feasibility.queue.model = 'UNKNOWN'
Test-RejectedFixture -Name 'PROMOTED candidate requires queue applicability screening' -Value $candidatePromotedWithUnknownQueue -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateFeasibleWithBlockedLatency = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateFeasibleWithBlockedLatency.early_feasibility.latency.status = 'BLOCKED'
$candidateFeasibleWithBlockedLatency.early_feasibility.blockers = @('End-to-end latency has not been measured.')
Test-RejectedFixture -Name 'FEASIBLE assessment cannot contain a blocked component' -Value $candidateFeasibleWithBlockedLatency -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateBlockedWithoutBlockedComponent = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateBlockedWithoutBlockedComponent.early_feasibility.assessment_status = 'BLOCKED'
$candidateBlockedWithoutBlockedComponent.early_feasibility.blockers = @('Generic blocker without a mapped component.')
Test-RejectedFixture -Name 'BLOCKED assessment requires a blocked feasibility component' -Value $candidateBlockedWithoutBlockedComponent -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateMergedWithoutTarget = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateMergedWithoutTarget.intake_status = 'MERGED'
$candidateMergedWithoutTarget.transition.merged_into_idea_id = $null
$candidateMergedWithoutTarget.transition.promotion_conditions = @()
$candidateMergedWithoutTarget.transition.promoted_research_id = $null
Test-RejectedFixture -Name 'MERGED candidate requires target idea' -Value $candidateMergedWithoutTarget -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateRejectedWithoutReason = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateRejectedWithoutReason.intake_status = 'REJECTED'
$candidateRejectedWithoutReason.transition.rejection_reasons = @()
$candidateRejectedWithoutReason.transition.promotion_conditions = @()
$candidateRejectedWithoutReason.transition.promoted_research_id = $null
Test-RejectedFixture -Name 'REJECTED candidate requires rejection reason' -Value $candidateRejectedWithoutReason -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateInvalidStage = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateInvalidStage.epistemic_stage_status.forward_predictive_oos.status = 'PROBABLY'
Test-RejectedFixture -Name 'epistemic stage status uses controlled independent states' -Value $candidateInvalidStage -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateSupportedStageWithoutEvidence = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateSupportedStageWithoutEvidence.epistemic_stage_status.mechanism_supported.status = 'SUPPORTED'
Test-RejectedFixture -Name 'supported epistemic stage requires evidence reference' -Value $candidateSupportedStageWithoutEvidence -Schema 'schemas\hypothesis_candidate.schema.json'

$candidateNetEdgeWithoutForwardSupport = Read-JsonText -RelativePath 'examples\hypothesis_candidate.minimal.json' | ConvertFrom-Json -Depth 100
$candidateNetEdgeWithoutForwardSupport.epistemic_stage_status.forward_predictive_oos.status = 'NOT_SUPPORTED'
$candidateNetEdgeWithoutForwardSupport.epistemic_stage_status.forward_predictive_oos.evidence_refs = @('validation:forward-oos-negative')
$candidateNetEdgeWithoutForwardSupport.epistemic_stage_status.executable_net_edge.status = 'SUPPORTED'
$candidateNetEdgeWithoutForwardSupport.epistemic_stage_status.executable_net_edge.evidence_refs = @('validation:net-edge-positive')
Test-RejectedFixture -Name 'supported executable net edge requires supported forward OOS evidence' -Value $candidateNetEdgeWithoutForwardSupport -Schema 'schemas\hypothesis_candidate.schema.json'

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
