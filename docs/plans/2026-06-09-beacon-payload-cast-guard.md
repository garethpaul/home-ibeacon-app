# Beacon Payload Cast Guard

status: completed

## Context

The active ranging delegates already guarded `CLRegion` values before calling
beacon-only APIs, but they still force-cast ranged beacon payloads and the
nested status view controller. If CoreLocation delivered an unexpected payload
or the app launched with a different root controller, the callback could crash
before ignoring the malformed event.

## Completed Scope

- Replaced forced `CLBeacon` casts in both active ranging delegates with
  optional casts.
- Replaced the nested status view controller and beacon array force casts with
  optional casts.
- Kept the proximity state and table reload behavior unchanged for expected
  beacon payloads.
- Extended the static privacy baseline so beacon payload casts stay guarded.
- Updated README, VISION, SECURITY, and CHANGES with the new guardrail.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
