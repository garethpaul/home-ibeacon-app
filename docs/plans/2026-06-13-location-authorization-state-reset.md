# Clear Beacon State After Location Authorization Revocation

status: in_progress

## Context

Both CoreLocation delegates cache the last beacon proximity, and the nested app
also displays the most recent ranged beacons. Region exit and unknown ranging
now reset those states, but a later authorization transition to denied or
restricted has no delegate handling. Stale home/away state can remain cached or
visible after the user removes location access.

## Priority

This is the highest-value remaining isolated privacy transition because the app
must stop treating previously authorized beacon observations as current once
CoreLocation access is unavailable.

## Scope

1. Handle denied and restricted authorization in both app delegates.
2. Clear cached proximity in both delegates.
3. Clear and reload the nested beacon table for revoked authorization.
4. Preserve launch authorization requests, region monitoring/ranging, disabled
   reporting/logging/notifications, and archival dependencies.

## Verification Plan

- Run all four Make gates, checker compilation, workflow parsing,
  `git diff --check`, and intended-file artifact and secret scans. Record the
  local Xcode skip truthfully.
- Remove each delegate reset and remove nested table clearing; every hostile
  mutation must fail.
- Push a stacked pull request and take one bounded exact-head workflow and
  code-scanning snapshot without polling.

## Risk And Rollback

Only denied or restricted authorization transitions change. Authorized ranging
and region callbacks retain their existing behavior. Rollback can leave stale
presence state after revocation; no persisted data migration exists.
