---
title: "fix: Clear stale beacon state after ranging failures"
type: fix
date: 2026-06-17
status: completed
---

# fix: Clear stale beacon state after ranging failures

## Summary

Handle Core Location beacon-ranging failures in both archival app delegates so
the application does not retain a stale home-presence state after ranging has
stopped producing trustworthy observations.

## Problem

The delegates clear cached state on region exit, unknown proximity, and
authorization revocation, but they do not implement Core Location's
`rangingBeaconsDidFailForRegion` callback. A ranging error can therefore leave
the last proximity cached and the nested sample's beacon rows visible even
though the observations are no longer current.

## Requirements

- R1. Both app delegates must handle beacon-ranging failures.
- R2. The failure callback must clear `lastProximity` without logging the
  location-sensitive error or beacon state.
- R3. The nested table sample must also clear displayed beacons and reload its
  table; the top-level app must not invent table state it does not own.
- R4. Maintained static checks must reject missing callbacks, misplaced state
  resets, weakened nested UI clearing, or top-level table coupling.
- R5. Existing launch monitoring, entry/exit ranging, authorization handling,
  unknown-proximity behavior, and privacy boundaries must remain unchanged.

## Implementation

1. Add the Swift 1-compatible Core Location ranging-failure delegate method to
   both `AppDelegate.swift` copies.
2. Clear cached proximity in each callback and clear/reload nested table state
   only in the nested sample.
3. Extend `scripts/check-baseline.py`, lifecycle documentation, and the
   changelog with mutation-sensitive contracts and completed evidence.

## Verification

- Run all four Make aliases from the repository root and `make check` through
  an absolute Makefile path from an external directory.
- Parse both Xcode project files and syntax-check the maintained Python gate.
- Reject isolated mutations that remove a failure callback, move the reset
  outside it, remove nested UI clearing, or add top-level table coupling.
- Use the existing hosted macOS workflow as the authoritative Xcode project
  validation because Xcode and Core Location are unavailable on Linux.

## Scope

This change does not modernize Swift, replace retired dependencies, alter
beacon identifiers, add logging/network reporting, or change the existing
monitoring and ranging lifecycle.

## Source

- [Apple CLLocationManagerDelegate documentation](https://developer.apple.com/documentation/corelocation/cllocationmanagerdelegate?language=objc)
  states that applications should implement potential failure handlers and
  lists `locationManager:rangingBeaconsDidFailForRegion:withError:`.

## Work Completed

- Added Swift 1-compatible beacon-ranging failure callbacks to both active app
  delegates.
- Cleared cached proximity in both callbacks and cleared/reloaded displayed
  beacon rows only in the nested table sample.
- Extended the maintained privacy baseline and lifecycle documentation without
  adding failure logging or changing region monitoring and ranging behavior.

## Verification Completed

- All four Make gates passed: `make lint`, `make test`, `make build`, and
  `make check`.
- The external-directory absolute-Makefile check passed from `/tmp`.
- `xcodebuild` was unavailable locally, so the maintained checker completed
  static project, source, plist, lockfile, workflow, privacy, and plan checks.
- Python checker compilation, workflow YAML parsing, and `git diff --check`
  passed.
- Six isolated hostile mutations were rejected for top-level callback removal,
  top-level reset weakening, nested UI-clear removal, top-level table coupling,
  stale plan status, and removed plan evidence.
