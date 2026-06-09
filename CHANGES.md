# Changes

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static privacy baseline.
- Removed a stale status UI read of the removed `AppDelegate.currentLocation`
  state and added a static guardrail for it.
- Disabled remaining beacon-state local notifications in the nested legacy app
  delegate so home/away and proximity state are not exposed on the lock screen.
- Removed the unused local notification permission request while beacon-state
  local notifications remain disabled.
- Removed unused local notification scheduling helpers from both app delegates
  while beacon-state notification scheduling remains disabled.
- Removed unused memory-only location state and dormant home/away message
  strings from active beacon delegates while reporting and notifications remain
  disabled.
- Guarded beacon-region casts before CoreLocation enter/exit callbacks call
  beacon-only ranging APIs.

## 2026-06-08

- Removed committed Fabric/Twitter credential literals from the current tree and replaced them with build-setting placeholders.
- Parameterized the Fabric build phase so local builds can opt in with `FABRIC_API_KEY` and `FABRIC_BUILD_SECRET`.
- Removed Digits phone-number debug logging from the login flow and dormant home/away payload assembly.
- Removed active beacon proximity and home/away logging from device logs.
- Hardened the UI hex color helper so invalid hex strings return the gray fallback.
- Added `make check` and a static iOS privacy baseline for project metadata, plist configuration, lockfiles, source inventory, and documentation guardrails.
