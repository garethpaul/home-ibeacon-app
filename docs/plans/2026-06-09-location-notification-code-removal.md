# Home iBeacon Notification Scheduling Code Removal

status: completed

## Context

Beacon-state local notifications are disabled because they can reveal home/away
or proximity state on the lock screen. Both app delegates still retained unused
`UILocalNotification` helper methods, leaving notification scheduling code in
place even though all active calls had been disabled.

## Objectives

- Remove unused local notification scheduling helpers from both app delegates.
- Preserve the disabled beacon-state notification posture.
- Extend the static baseline so `UILocalNotification` scheduling code does not
  return while notification behavior is disabled.
- Document the guardrail with the existing location privacy notes.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
