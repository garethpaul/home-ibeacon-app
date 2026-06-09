# Beacon Region Cast Guard

status: completed

## Context

Both app delegates receive CoreLocation enter and exit callbacks as `CLRegion`.
The previous code force-cast those values to `CLBeaconRegion` before calling
beacon-only ranging APIs. If a non-beacon region reached the delegate, the app
would crash before it could ignore the unexpected callback.

## Completed Scope

- Replaced forced `CLBeaconRegion` casts in both active app delegates with
  optional casts.
- Kept ranging and location updates unchanged for expected beacon regions.
- Extended the static privacy baseline so forced beacon-region casts stay out
  of active delegate code.
- Updated README, VISION, and CHANGES to document the guardrail.

## Verification

- `make check`
- `git diff --check`
