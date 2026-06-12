# Standard Location Update Removal

status: completed

## Context

Both app delegate copies started continuous standard `CLLocationManager`
updates at launch and on beacon entry, disabled automatic pausing, and stopped
those updates on exit. No location-update callback consumes coordinates; the
app only uses beacon monitoring and ranging. The extra updates therefore
expanded privacy exposure and battery use without supporting behavior.

## Completed Scope

- Removed standard location update start/stop calls from both delegates.
- Removed the policy that disabled automatic pausing for unused updates.
- Preserved always-authorization, beacon monitoring, beacon ranging, and
  guarded beacon-region callbacks.
- Extended the static privacy baseline and documentation to preserve the
  beacon-only CoreLocation boundary.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
