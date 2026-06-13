# Location-Independent HomeBeacon Verification

status: planned

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

Pending implementation.

## Verification Completed

Pending implementation and validation.
