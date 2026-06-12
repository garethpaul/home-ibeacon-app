# Region-Scoped Beacon Ranging

status: completed

## Context

Both checked-in app delegates start beacon monitoring and beacon ranging during
application launch. They also start ranging again when CoreLocation reports a
beacon-region entry and stop it on region exit.

Launching outside the region can therefore leave ranging active without a
matching exit transition, increasing battery use and proximity-data collection
despite the app only needing detailed ranging while inside the monitored
region.

## Priority

Beacon proximity is privacy-sensitive home-presence data. The archival sample
should retain the least continuous CoreLocation behavior needed for its stated
enter/exit workflow.

## Prioritized Engineering Backlog

1. Scope beacon ranging to region entry and exit now.
2. Move authorization and beacon configuration behind an explicit consent flow
   during any future SDK modernization.
3. Replace retired Fabric/TwitterKit dependencies only in a dedicated rewrite.

## Requirements

- R1. Application launch must continue monitoring the configured beacon region.
- R2. Application launch must not start detailed beacon ranging.
- R3. Guarded `didEnterRegion` callbacks must start ranging only for
  `CLBeaconRegion` values.
- R4. Guarded `didExitRegion` callbacks must stop ranging only for
  `CLBeaconRegion` values.
- R5. Both duplicated app delegate sources must retain identical ranging
  lifecycle behavior.
- R6. The static baseline must require exactly the two entry-triggered ranging
  calls and two exit-triggered stop calls.

## Implementation Units

### U1. Remove launch-time ranging

- **Files:** `HomeBeacon/AppDelegate.swift`,
  `HomeBeacon/HomeBeacon/AppDelegate.swift`
- Preserve monitoring and guarded callbacks while deleting unconditional
  launch-time ranging.

### U2. Tighten the privacy baseline

- **Files:** `scripts/check-baseline.py`
- Require monitoring in both delegates and exact region-scoped start/stop
  ranging counts so launch-time ranging cannot return unnoticed.

### U3. Update maintenance documentation

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record the monitoring-versus-ranging lifecycle and privacy rationale.

## Scope Boundaries

- Do not change beacon UUIDs, authorization mode, network reporting, or login.
- Do not modernize Swift syntax, project settings, or dependencies.
- Do not disable region monitoring.

## Verification

- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
- A mutation restoring launch-time `startRangingBeaconsInRegion` must fail the
  baseline.

Completed on 2026-06-12 with the static privacy baseline, Python checker
compilation, diff hygiene, and launch-time ranging mutations rejected for both
app delegate copies.
