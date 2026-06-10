# Hosted Project Validation

status: completed

## Context

The repository had extensive static privacy, credential, plist, dependency, and
cast-safety checks, but merely printed a reminder when Xcode was installed.
Hosted validation can parse the checked-in app project without Fabric/Twitter
credentials or live beacon/location behavior.

## Changes

- Changed the installed-Xcode path to list `HomeBeacon.xcodeproj`.
- Added pinned, least-privilege `macos-15` GitHub Actions validation with
  concurrency cancellation and a timeout.
- Kept workspace builds and device behavior as explicit follow-up validation
  because they require legacy dependencies, credentials, and beacon hardware.

## Verification

- `make check`
- Workflow YAML parse
- Hosted `macos-15` GitHub Actions run
