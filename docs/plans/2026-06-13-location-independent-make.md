# Location-Independent HomeBeacon Verification

status: completed

## Context

The maintained privacy baseline passes from the checkout, but an absolute
Makefile invocation from another directory resolves the checker relative to
the caller.

## Scope

1. Derive the repository root from `MAKEFILE_LIST`.
2. Invoke the Python checker through its rooted path.
3. Add completed-plan, external-run, guidance, and mutation contracts.
4. Preserve Swift, project, pod, binary SDK, and workflow files.

## Verification Plan

- Run all four Make gates from the checkout and a temporary directory.
- Run checker compilation, maintained XML/plist parsing, and diff checks.
- Reject root, checker, plan status/evidence, and documentation mutations.
- Inspect exact paths, secrets, and generated artifacts.

## Risk And Rollback

Verification path resolution only; rollback restores the caller-relative
recipe with no runtime state or migration.

## Work Completed

- Derived `ROOT` from the loaded Makefile and invoked the checker through its
  absolute repository path.
- Added exact Makefile, completed-plan, external-run, and guidance contracts.
- Preserved Swift, project, pod, binary SDK, and workflow files.

## Verification Completed

- Root and external-directory Make gates passed for `lint`, `test`, `build`,
  and `check`; every target exercised the complete privacy baseline.
- The root-derivation mutation failed.
- The checker-invocation mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Checker compilation, maintained XML/plist parsing, diff hygiene, intended
  path review, secret scanning, and generated-artifact inspection passed.
