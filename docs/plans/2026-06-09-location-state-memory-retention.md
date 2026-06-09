# Location State Memory Retention

status: completed

## Context

Network reporting and beacon-state notifications are disabled, but the active
delegates still retained unused `currentLocation`, message, and sound variables
with home/away text. That dormant state made it easier to accidentally revive
occupancy reporting or lock-screen payloads without a privacy review.

## Completed Scope

- Removed the unused `currentLocation` property from the top-level app delegate.
- Removed dormant home/away message strings and sound flags from both active
  beacon delegates.
- Removed empty Digits session blocks that only assigned the dormant location
  state while network reporting was disabled.
- Extended the static privacy baseline to reject retained memory-only location
  state and unused occupancy text.
- Updated README, VISION, and CHANGES so the guardrail stays visible.

## Verification

- `make check`
- `git diff --check`
