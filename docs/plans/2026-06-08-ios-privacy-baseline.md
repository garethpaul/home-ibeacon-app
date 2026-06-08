# Home iBeacon App Privacy Baseline Plan

status: completed

## Context

`home-ibeacon-app` is a legacy Swift iOS 8-era CoreLocation/iBeacon app with checked-in CocoaPods, Fabric, and TwitterKit artifacts. This Linux host does not provide Xcode, so local verification needs a static baseline while full app builds remain a macOS/Xcode responsibility.

## Objectives

- Remove credential literals and private phone-number debug logging from the current tree.
- Keep the Fabric/Twitter credential contract explicit through local build settings instead of checked-in secrets.
- Add a local `make check` baseline for plist parsing, Xcode/CocoaPods metadata, source inventory, and privacy guardrails.
- Document the legacy Xcode, CocoaPods, beacon, location, and Fabric/Twitter expectations for future rebuilds.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
