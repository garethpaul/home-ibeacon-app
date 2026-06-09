# HomeBeacon Hex Parser Invalid Input Guard

status: completed

## Context

`HomeBeacon/Hex.swift` converts static UI hex strings into `UIColor` values for
the navigation appearance. The helper already trims whitespace and falls back to
gray for the wrong length, but it ignored the `NSScanner.scanHexInt` result.
Malformed six-character strings could therefore produce a partially scanned
color instead of the documented fallback.

## Objectives

- Keep valid six-character RGB strings working.
- Return `UIColor.grayColor()` when scanning fails or leaves trailing input.
- Add a static baseline guard so partial hex scanning does not return.
- Document the parser behavior in the repo maintenance notes.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
