# Home iBeacon Location Log Privacy Plan

status: completed

## Context

The app handles home/away and beacon proximity events. Even with network
reporting disabled, writing those states to device logs can expose sensitive
presence information during debugging, backups, or shared diagnostics.

## Objectives

- Remove active home/away and proximity `NSLog` calls from both checked-in app delegates.
- Preserve the existing disabled network reporting posture.
- Extend the static baseline so location-state logging does not return.
- Document the log privacy guardrail.

## Work Items

1. Removed active `NSLog` calls from `HomeBeacon/AppDelegate.swift`.
2. Removed active `NSLog` calls from `HomeBeacon/HomeBeacon/AppDelegate.swift`.
3. Extended `scripts/check-baseline.py` to scan both app delegates for active location logging.
4. Updated README, VISION, CHANGES, and this plan.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
