# Stale View Location State

status: completed

## Context

The previous privacy cleanup removed `AppDelegate.currentLocation`, but the
top-level status view still read that property after a delay to switch between
home and away images. That made the active Swift source inconsistent with the
removed state and would fail once the app target was compiled with the legacy
toolchain.

## Completed Scope

- Removed the obsolete `AppDelegate` dependency from the top-level view
  controller.
- Removed the delayed status-image update that read the removed location state.
- Extended the static privacy baseline to reject stale status UI reads of
  `AppDelegate.currentLocation`.
- Updated README, VISION, and CHANGES so the guardrail stays visible.

## Verification

- `make check`
- `git diff --check`
