# Location-Independent HomeBeacon Verification

status: completed

## Context

Rooted recipes support external callers, but GNU Make still split an absolute
Makefile path containing spaces before deriving the checkout root.

## Scope

1. Derive the repository root from the single loaded Makefile path while preserving spaces.
2. Invoke the Python checker through its rooted path.
3. Add a recursive-safe spaced-path full gate and synchronized contracts.
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

- Derived `ROOT` from the sole loaded Makefile path, rejected ambiguous Makefile inputs,
  and invoked the checker through its absolute repository path.
- Added exact Makefile, completed-plan, external-run, and guidance contracts.
- Preserved Swift, project, pod, binary SDK, and workflow files.

## Verification Completed

- Root and external-directory Make gates passed for `lint`, `test`, `build`,
  and `check`; every target exercised the complete privacy baseline.
- Spaced-checkout checks passed under GNU Make 4.2 and 4.4.
- Preloaded, overridden, and additional Makefiles failed closed.
- The root-derivation mutation failed.
- The checker-invocation mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Checker compilation, maintained XML/plist parsing, diff hygiene, intended
  path review, secret scanning, and generated-artifact inspection passed.
