# Legacy SDK modernization boundary

status: completed

## Current boundary

This snapshot uses Swift 1-era syntax, an iOS 8.3 deployment target, CocoaPods
with an iOS 8.0 platform, and Alamofire 1.2. It also contains vendored Fabric
and TwitterKit binaries. Current Xcode and iOS SDK releases cannot be treated as
drop-in build environments for this code.

## Modernization sequence

1. Preserve the current static baseline and privacy checks before changing build metadata.
2. Replace retired Fabric/TwitterKit authentication and analytics integrations.
3. Migrate Alamofire and networking call sites through supported releases with focused tests.
4. Convert Swift syntax and UIKit/Core Location APIs in reviewable stages.
5. Raise the deployment target only after permission, beacon-ranging, and home-state behavior is verified on supported devices.

Until that work is scheduled, changes should remain compatible with the
archival baseline and must not imply that the app builds with a current SDK.
