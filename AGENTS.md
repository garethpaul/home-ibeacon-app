# AGENTS.md

## Repository purpose

`garethpaul/home-ibeacon-app` is a Apple platform application or Objective-C/Swift sample. A home beacon service. Sends a HTTP request to a server if you enter or leave a "region".

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `Podfile` - CocoaPods dependency definition
- `HomeBeacon.xcodeproj` - Xcode project
- `HomeBeacon.xcworkspace` - Xcode workspace
- `Fabric.framework` - repository source or sample assets
- `HomeBeacon` - repository source or sample assets
- `HomeBeaconTests` - repository source or sample assets
- `TwitterKit.framework` - repository source or sample assets

## Development commands

- Install dependencies: `pod install`
- Full baseline: `make check`
- Make gates support absolute checkout paths containing spaces; preserve the encoded `MAKEFILE_LIST` root derivation and recursive regression.
- Local Apple development: `open HomeBeacon.xcworkspace`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: C/C++ headers (96), Swift (8).
- Use the CocoaPods workspace when present; update `Podfile.lock` only with an intentional dependency change.
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `HomeBeacon/HomeBeaconTests/HomeBeaconTests.swift`, `HomeBeaconTests/HomeBeaconTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- The current tree uses build-setting placeholders for Fabric and Twitter credentials. Do not replace `$(FABRIC_API_KEY)`, `$(TWITTER_CONSUMER_KEY)`, or `$(TWITTER_CONSUMER_SECRET)` with real values in tracked files.
- The Fabric upload build phase reads `FABRIC_API_KEY` and `FABRIC_BUILD_SECRET` locally and skips the upload when either value is unset.
- The sample beacon UUID and identifier are still checked into `HomeBeacon/AppDelegate.swift`; treat them as demo configuration and move private beacon values to local configuration before production use.
- Beacon enter/exit state can reveal home occupancy. Do not re-enable network reporting until the endpoint, consent model, retention behavior, and HTTPS transport are documented.
- Do not re-enable home/away or proximity `NSLog` calls; device logs can expose occupancy during debugging or shared diagnostics.
- Clear cached beacon proximity and displayed rows when location authorization becomes denied or restricted.
- Install each location manager delegate before requesting authorization or starting monitoring.
- Clear cached beacon proximity and displayed rows when beacon ranging fails; do not log the failure or occupancy-derived state.
- Stop active beacon ranging and clear cached/displayed state when region monitoring fails; do not log the error or occupancy-derived state.
- `Pods/` is vendored dependency code; do not hand-edit it unless intentionally updating dependencies.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
