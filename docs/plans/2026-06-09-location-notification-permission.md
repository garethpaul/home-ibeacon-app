# Home iBeacon Notification Permission Guard

status: completed

## Context

Beacon-state local notifications are disabled because they can reveal home/away
or proximity state on the lock screen. The main app still requested local
notification permission at launch, which exposed an unused privacy-sensitive
permission prompt.

## Objectives

- Remove the unused launch-time local notification permission request.
- Preserve the existing disabled beacon-state notification posture.
- Extend the static baseline so permission prompts do not return while
  notifications are disabled.
- Document the permission boundary alongside the location privacy guardrails.

## Verification

- `make check`
- `git diff --check`
