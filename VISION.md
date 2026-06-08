## Home iBeacon App Vision

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

Next priorities:

- Add README setup, beacon configuration, and device verification notes
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

## What We Will Not Merge (For Now)

- Hardcoded private endpoints, beacon IDs, or credentials
- Background tracking beyond the stated region behavior
- Silent home/away reporting without documentation
- Broad dependency migration mixed with location behavior changes

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
