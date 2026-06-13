# Beacon Exit State Reset

status: completed

## Context

Both maintained app delegates stop beacon ranging when CoreLocation reports a
beacon-region exit, but they retain the last proximity value. The nested sample
also leaves its last ranged beacon array displayed in the table.

After an exit, cached in-region state can therefore survive until another
ranging callback arrives. Re-entry at the same proximity may also be treated as
unchanged because the previous proximity was never cleared.

## Priority

Beacon state can reveal occupancy. Clearing transient ranging state at the
region boundary is a focused correctness and privacy improvement that does not
revive network reporting or modernize the archival SDK stack.

## Requirements

- R1. A guarded beacon-region exit must stop ranging and reset
  `lastProximity` in both maintained app delegates.
- R2. The nested app delegate must clear its cached beacon list and reload the
  table after a guarded beacon-region exit.
- R3. Non-beacon region callbacks must not clear beacon state or call
  beacon-specific APIs.
- R4. Region entry, launch-time monitoring, and region-scoped ranging counts
  must remain unchanged.
- R5. Network reporting, occupancy logging, local notifications, and standard
  location updates must remain disabled.
- R6. The deterministic baseline must isolate both `didExitRegion` methods and
  reject missing, unguarded, or stale-state behavior.

## Implementation Units

### U1. Reset exit state

- **Files:** `HomeBeacon/AppDelegate.swift`,
  `HomeBeacon/HomeBeacon/AppDelegate.swift`
- Reset proximity in both guarded exit handlers and clear the nested table's
  beacon source before reloading it.

### U2. Extend static lifecycle contracts

- **Files:** `scripts/check-baseline.py`
- Verify exit-method scope, guarded region handling, reset counts, and nested
  UI clearing without relying on the unavailable legacy runtime.

### U3. Document the privacy boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that region exit clears transient beacon-derived state.

## Scope Boundaries

- Do not re-enable HTTP requests, session payloads, logs, or notifications.
- Do not change beacon UUIDs, identifiers, permissions, or monitoring setup.
- Do not edit vendored frameworks, Pods, lockfiles, or Xcode project metadata.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- Hostile mutations removing either proximity reset, moving a reset outside the
  beacon guard, retaining the nested beacon list, weakening plan status, or
  removing verification evidence must be rejected.

## Work Completed

- Reset `lastProximity` inside both guarded beacon-region exit handlers after
  ranging stops.
- Cleared the nested sample's beacon array and reloaded its table inside the
  same guarded exit boundary.
- Added method-scoped static contracts so unrelated assignments elsewhere in a
  delegate cannot satisfy the lifecycle guard.
- Updated README, security, vision, and change documentation.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS privacy baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Seven isolated hostile mutations were rejected: removal of either proximity
  reset, removal of nested beacon clearing or table reload, moving a reset
  outside the beacon guard, stale plan status, and missing verification
  evidence.
