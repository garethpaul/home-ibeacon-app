---
title: "fix: Install location delegates before authorization"
type: fix
date: 2026-06-26
status: completed
---

# fix: Install location delegates before authorization

## Context

Both active app delegates created a `CLLocationManager`, requested Always
authorization, and only then assigned the delegate that handles authorization
revocation. Apple documents that a location manager reports authorization
state to its delegate after initialization and recommends assigning the
delegate immediately during configuration. A callback delivered before the
assignment could bypass the handlers that clear occupancy-derived state.

## Decision

Install `self` as the location manager delegate immediately after manager
creation, before requesting authorization and before starting region
monitoring, in both active app delegates.

Alternatives considered:

- Poll authorization state after the request. Rejected because it duplicates
  Core Location's delegate lifecycle and still leaves an ordering gap.
- Clear state unconditionally at launch. Rejected because it masks rather than
  fixes callback delivery and does not protect later authorization changes.
- Modernize the deprecated delegate API. Deferred because this archival Swift
  1 project needs a separate toolchain migration; the ordering fix is valid for
  its current API surface.

## Requirements

- Both active delegates assign `locationManager!.delegate = self` before
  `requestAlwaysAuthorization()` and `startMonitoringForRegion`.
- The maintained checker rejects missing or reordered setup in either file.
- Existing authorization-reset, ranging, monitoring, privacy, credential, and
  legacy-toolchain contracts remain unchanged.
- Network reporting, local notifications, logging, beacon identifiers, and
  requested permission scope remain unchanged.

## Verification Completed

- The new checker contract failed against both original launch paths with a
  delegate-specific message, then passed after the source reorder.
- Both isolated ordering mutations were rejected, one per active delegate.
- `python3 -m py_compile scripts/check-baseline.py`, all four Make gates, an
  external-directory absolute-Makefile gate, and `git diff --check` passed.
- Local validation reported that `xcodebuild` is unavailable and therefore ran
  the maintained static iOS baseline only.
- Require hosted pull-request checks on the exact delivery SHA before merge and
  verify the post-merge workflow separately.

## Runtime Boundary

Static source verification proves the maintained ordering contract but not
Core Location callback timing, user prompt behavior, or physical beacon
delivery. Local `xcodebuild` is unavailable; hosted macOS remains the Xcode
project parser and device behavior remains a manual boundary.

## Primary Reference

- Apple `CLLocationManager` documentation:
  `https://developer.apple.com/documentation/corelocation/cllocationmanager`
