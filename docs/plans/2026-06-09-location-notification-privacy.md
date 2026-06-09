# Home iBeacon Location Notification Privacy

status: completed

## Context

Beacon proximity and home/away state can reveal occupancy. Prior guardrails
disabled active device logs and network reporting, but the nested legacy app
delegate still displayed local notifications for enter, exit, and proximity
events.

## Objectives

- Disable active local notifications that expose beacon proximity or
  home/away state.
- Preserve the existing disabled network reporting posture.
- Extend the static baseline so active state notifications do not return.
- Document the lock-screen notification privacy guardrail.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
