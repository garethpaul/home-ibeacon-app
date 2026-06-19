## Home iBeacon App Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Home iBeacon App is an iOS sample that detects entry and exit from a configured
region and can send HTTP requests when the device is home or away.

The repository is useful as a legacy CoreLocation, iBeacon, Alamofire, and
Fabric/TwitterKit-era sample with a small status UI.

The goal is to keep the proximity workflow understandable while making
credentials, beacon configuration, and location privacy explicit.

The current focus is:

Priority:

- Preserve the home/away region status flow
- Keep beacon UUID, endpoint, and credential assumptions visible
- Avoid committing Fabric/Twitter credentials, signing material, or location data
- Maintain the CocoaPods workspace and iOS 8-era dependency context
- Keep `scripts/check-baseline.py` passing for credential placeholders, plist
  metadata, CocoaPods lockfiles, source inventory, disabled device logs, and
  removed notification scheduling code, disabled notification permission
  prompts, memory-only location state, stale status UI reads, and network posts
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates
- Keep beacon-region casts guarded before CoreLocation callbacks call
  beacon-only ranging APIs
- Keep beacon payload casts guarded before ranging callbacks update proximity
  state or status UI
- Keep standard coordinate updates off while the app only consumes beacon
  monitoring and ranging events
- Keep region-scoped beacon ranging between guarded region entry and exit
  callbacks instead of starting detailed ranging at launch
- Keep small UI helpers deterministic on malformed input

Next priorities:

- Move server endpoint and beacon values into documented local configuration
- Modernize Swift, CoreLocation, Alamofire, and Fabric/Twitter dependencies in a
  dedicated pass
- Add tests or manual checklists around enter/exit behavior

Contribution rules:

- One PR = one focused beacon, endpoint, build, or documentation change.
- Verify region behavior on a physical device when changing CoreLocation code.
- Keep real credentials and signing files out of git.
- Document privacy impact for any new location behavior.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Beacon region state can reveal whether someone is home. Do not log, upload, or
persist home/away data without explicit purpose and user control.

Remote requests should use HTTPS and local configuration.

Current baseline: `make lint`, `make test`, `make build`, and `make check`
run `scripts/check-baseline.py` without Xcode.
GitHub Actions runs the privacy/credential baseline and current-Xcode project
listing on macOS; functional beacon behavior remains device-only.
The hosted workflow uses read-only permissions without persisted checkout
credentials and is checked as a complete contract.
It verifies that Fabric/Twitter credentials use local build-setting
placeholders, phone-number debug logging and dormant phone-number payloads stay
removed, CocoaPods lockfiles stay in sync, and home/away network reporting
remains disabled until privacy and consent are documented. Beacon proximity and
home/away state must also stay out of device logs and local notifications.
Region-scoped beacon ranging preserves launch-time monitoring while deferring
detailed proximity scans until CoreLocation reports region entry.
Guarded beacon exits clear cached proximity in both delegates and remove nested
beacon-table rows so transient ranging state ends with the region lifecycle.
Unknown proximity replaces stale known state during ranging so later valid
callbacks are evaluated after the indeterminate interval.
Unused local notification permission prompts stay disabled while those
notifications are off. Local notification scheduling helpers should stay out of
the delegates while notification scheduling is disabled.
Memory-only location state and unused home/away message strings should stay out
of active delegates while reporting and notifications are disabled.
Stale status UI code must not read removed `AppDelegate.currentLocation` state.
Beacon-region casts should stay guarded before enter/exit callbacks call
beacon-only ranging APIs.
Beacon payload casts should stay guarded before ranged beacon arrays update
status UI or proximity state.
Standard `CLLocationManager` coordinate updates should remain disabled until a
documented feature consumes that data with an explicit privacy purpose.
Invalid hex color strings must return the gray fallback instead of partially
scanned colors.

## Modernization Boundary

The current repository preserves a Swift 1-era, iOS 8.3 application with an
iOS 8.0 CocoaPods platform, Alamofire 1.2, and retired Fabric/TwitterKit
artifacts. Modernization must replace retired integrations, migrate networking,
then convert Swift and Core Location behavior in independently verifiable
stages; it is not a single project-file upgrade.

## What We Will Not Merge (For Now)

- Hardcoded private endpoints, beacon IDs, or credentials
- Background tracking beyond the stated region behavior
- Silent home/away reporting without documentation
- Broad dependency migration mixed with location behavior changes

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
