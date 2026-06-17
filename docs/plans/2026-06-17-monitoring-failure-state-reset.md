---
title: "fix: Fail closed after beacon monitoring failures"
type: fix
date: 2026-06-17
status: completed
---

# fix: Fail closed after beacon monitoring failures

## Context

The two archival app delegates now clear occupancy-derived state on region
exit, authorization revocation, unknown proximity, and ranging failure. They do
not implement Core Location's monitoring-failure callback. If region
monitoring fails while ranging is active, the application can retain cached
proximity and continue ranging without a reliable exit boundary.

## Prioritized Engineering Tasks

1. **Selected: fail closed on region-monitoring failure.** Stop beacon ranging,
   clear cached proximity, and clear the nested table state without logging
   location-sensitive error details.
2. **Follow-up: modernize the Core Location delegate surface.** Perform this
   only with the broader Swift/current-Xcode migration because callback
   signatures, authorization APIs, and retired SDK removal are coupled.
3. **Follow-up: add runtime state-machine tests on Apple tooling.** Keep this
   separate from the dependency-free Linux baseline and legacy project parser.

## Requirements

- R1. Both active app delegates must implement the Swift 1-compatible
  `monitoringDidFailForRegion` callback.
- R2. Each callback must guard the `CLRegion` value as a `CLBeaconRegion`, stop
  ranging for that region, and clear `lastProximity` inside the guarded block.
- R3. The nested table sample must also clear displayed beacons and reload its
  table inside the guarded block; the top-level delegate must not reference
  nested table state.
- R4. Neither callback may log the error or any occupancy-derived state.
- R5. The maintained checker must reject callback removal, unguarded beacon
  API use, missing ranging shutdown, misplaced state clearing, weakened nested
  UI clearing, and top-level table coupling.
- R6. Existing entry, exit, authorization, unknown-proximity, ranging-failure,
  privacy, credential, workflow, and legacy toolchain contracts must remain
  unchanged.

## Implementation Units

### Delegate lifecycle handling

Files:

- `HomeBeacon/AppDelegate.swift`
- `HomeBeacon/HomeBeacon/AppDelegate.swift`

Add the monitoring-failure callback to both delegates. Use the existing
optional beacon-region cast pattern, stop ranging before clearing state, and
keep nested UI ownership isolated to the nested sample.

### Verification and maintained guidance

Files:

- `scripts/check-baseline.py`
- `AGENTS.md`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-17-monitoring-failure-state-reset.md`

Extend the structural lifecycle contracts and synchronized privacy guidance.
Record only verification that actually runs; hosted macOS remains the Xcode
project authority because Linux cannot execute Core Location.

## Validation

- Run Python syntax checks, workflow parsing, all four Make gates, and an
  external-directory absolute-Makefile gate.
- Parse both Xcode project files through the maintained checker.
- Reject isolated mutations for callback removal, cast removal, ranging-stop
  removal, cache-reset movement, nested UI-clear removal, top-level table
  coupling, stale plan status, and weakened plan evidence.
- Audit the exact diff, generated artifacts, conflict markers, file modes, and
  credential-shaped additions.
- Require canonical push and pull-request checks on the exact delivery head
  before terminal tracker reconciliation.

## Boundaries

- This change does not modernize Swift, replace CocoaPods or retired SDKs,
  alter beacon identifiers, re-enable network reporting, add logging, or
  change the launch/entry/exit monitoring policy.
- Linux static verification cannot prove Core Location callback delivery,
  table rendering, simulator behavior, signing, or physical beacon behavior.
- The new PR remains stacked on PR #8; no existing PR is merged or closed.

## Primary Reference

- Apple `CLLocationManagerDelegate` documentation:
  `https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate`

## Work Completed

- Added Swift 1-compatible region-monitoring failure callbacks to both active
  app delegates.
- Guarded each failed region as a `CLBeaconRegion`, stopped ranging before
  clearing cached proximity, and kept nested table clearing isolated to the
  nested sample.
- Extended the maintained checker and synchronized privacy guidance without
  adding error logging, network reporting, dependency churn, or project-file
  changes.

## Verification Completed

- All four Make gates passed: `make lint`, `make test`, `make build`, and
  `make check`.
- External-directory `make check` passed through the absolute Makefile path.
- Python checker execution, workflow parsing, project/plist/XML validation,
  and `git diff --check` passed.
- Six isolated implementation mutations were rejected: callback removal,
  guarded-cast removal, ranging-stop removal, stop/reset reordering, nested UI
  clearing removal, and top-level table coupling.
- Plan-aware correctness, testing, maintainability, repository-standards,
  privacy/security, and Swift/Core Location review found no actionable
  findings; artifact:
  `/tmp/compound-engineering/ce-code-review/home-ibeacon-monitoring-failure-20260617T210100Z`.
- `xcodebuild` and Core Location were unavailable on Linux, so no simulator,
  callback-delivery, table-rendering, signing, or physical-beacon behavior is
  claimed.
