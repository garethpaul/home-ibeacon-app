# Hosted Workflow Integrity

status: completed

## Context

The macOS project check used read-only repository permissions, but checkout
credentials remained persisted and the baseline only searched for expected
tokens. A workflow could therefore add a credential-bearing checkout override
or an unrelated command while still passing validation.

## Completed Scope

- Set `persist-credentials: false` on checkout.
- Kept the checkout action pinned to its immutable commit.
- Enforced the complete bounded macOS workflow as a canonical contract.
- Enforced the Make aliases used by hosted CI as a canonical contract.
- Made Swift line-comment stripping preserve quoted URL strings so transport
  checks evaluate the actual source.
- Added hostile mutations for credential overrides and extra workflow steps.

## Verification

- `make check`
- mutations adding `persist-credentials: true`, an extra workflow step, or a
  Make target override must fail
- a mutation adding a quoted plain-HTTP endpoint must fail
- `git diff --check`
