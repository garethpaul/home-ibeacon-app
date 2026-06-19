# Reset Unknown Beacon Proximity State

status: completed

## Context

Both maintained app delegates suppress duplicate beacon proximity callbacks by
remembering `lastProximity`. When the nearest beacon reports
`CLProximity.Unknown`, each delegate returns before updating that state.

If the previous callback reported a known proximity, the stale known value is
therefore retained. A later callback at that same known proximity can be
mistaken for a duplicate even though an unknown interval occurred between the
two observations.

## Priority

Beacon proximity is transient occupancy-derived state. Recording the unknown
transition is a focused correctness and privacy improvement that complements
the existing region-exit reset without changing the archival SDK boundary.

## Requirements

- R1. Both `didRangeBeacons` handlers must record
  `CLProximity.Unknown` before returning for an unknown nearest beacon.
- R2. Repeated unknown callbacks must remain harmless, and the existing empty
  beacon-list path must continue to record unknown state.
- R3. Known duplicate suppression and valid known proximity updates must remain
  unchanged.
- R4. Region monitoring, region-scoped ranging, and exit-state clearing counts
  must remain unchanged.
- R5. Network reporting, occupancy logging, local notifications, and standard
  location updates must remain disabled.
- R6. The deterministic baseline must isolate both `didRangeBeacons` methods
  and reject a missing or misplaced unknown-state assignment.

## Implementation Units

### U1. Record unknown transitions

- **Files:** `HomeBeacon/AppDelegate.swift`,
  `HomeBeacon/HomeBeacon/AppDelegate.swift`
- Split duplicate suppression from the unknown branch and assign
  `lastProximity` before returning from the latter.

### U2. Extend static lifecycle contracts

- **Files:** `scripts/check-baseline.py`
- Verify method-scoped unknown handling in both delegates while retaining the
  existing ranging, exit-reset, and privacy contracts.

### U3. Document the state boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that unknown callbacks replace stale known proximity state.

## Scope Boundaries

- Do not re-enable HTTP requests, session payloads, logs, or notifications.
- Do not change beacon UUIDs, identifiers, permissions, monitoring, or ranging
  setup.
- Do not edit vendored frameworks, Pods, lockfiles, Xcode project metadata, or
  hosted workflow configuration.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Hostile mutations removing either unknown-state assignment, moving an
  assignment outside its unknown branch, weakening plan status, or removing
  verification evidence must be rejected.

## Work Completed

- Split known duplicate suppression from unknown proximity handling in both
  maintained `didRangeBeacons` callbacks.
- Recorded `CLProximity.Unknown` before returning from each nearest-beacon
  unknown branch while preserving the existing empty-list transition.
- Added method-scoped static contracts for both delegates and documented the
  transient state boundary without changing monitoring, ranging, project, or
  dependency configuration.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS privacy baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Six isolated hostile mutations were rejected: removal of either delegate's
  unknown-state assignment, restoration of the combined duplicate/unknown
  condition, moving an assignment outside its unknown branch, stale plan
  status, and missing verification evidence.
- Exact-base comparison confirmed vendored frameworks, Pods, lockfiles, Xcode
  project metadata, and hosted workflow configuration remained unchanged.
- Intended-file generated-artifact and secret-pattern scans passed.
- Hosted macOS project validation and CodeQL evidence is recorded separately
  after push; this plan claims only the completed local static verification.
