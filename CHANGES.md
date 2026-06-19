# Changes

## 2026-06-17

- Beacon-ranging failures clear cached proximity in both delegates and remove
  nested table rows so Core Location errors cannot leave stale presence state.
- Region-monitoring failures stop active beacon ranging before clearing cached
  proximity and nested table rows, without logging occupancy-derived state.

## 2026-06-13

- Made every Make verification target derive the checkout root so the privacy
  baseline works from external directories.
- Clear cached beacon proximity and nested table rows when location
  authorization becomes denied or restricted.
- Record unknown beacon proximity in both delegates before returning so stale
  known state cannot suppress the next valid callback at the same distance.
- Reset cached proximity in both delegates and clear the nested beacon table
  after guarded beacon-region exits so stale in-region state does not survive
  after ranging stops.

## 2026-06-12

- Limited both app delegates to region-scoped beacon ranging: launch monitors
  the region, entry starts proximity ranging, and exit stops it.
- Hardened the hosted workflow contract against persisted checkout credentials
  and unreviewed extra steps.
- Fixed Swift comment stripping so plain-HTTP strings cannot evade the privacy
  baseline by containing `//` inside a quoted URL.

## 2026-06-10

- Documented and enforced the legacy SDK modernization boundary for the Swift
  1-era, iOS 8.3, Alamofire 1.2, Fabric, and TwitterKit baseline.
- Removed unused continuous standard location updates from both app delegates
  while preserving beacon monitoring and ranging.
- Added pinned macOS GitHub Actions validation for the privacy baseline and
  current-Xcode project parsing.
## 2026-06-09

- Guarded beacon payload casts in ranging callbacks before updating proximity
  state or status UI.
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
