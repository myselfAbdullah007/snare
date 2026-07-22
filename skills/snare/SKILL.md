---
name: snare
description: >
  Turn a bug report, stack trace, or error log into a single failing test that
  reproduces it — before any fix. Locates the real code path, writes one test
  in the repo's existing framework, and proves it fails for the reported reason
  (not an import error or typo). Does NOT fix the bug; hands off a red test the
  fix must turn green. Use when the user pastes a stack trace, bug report, or
  error and says "reproduce this", "write a failing test", "snare", "/snare",
  "turn this into a test", or asks for a regression test before fixing.
---

Turn a bug into ONE failing test that reproduces it. You write the red test.
You do not fix the bug — the fix is a separate step, and a fix without a
reproducing test is how the bug comes back.

## The rule that matters

The test must fail for the **reported reason**, not any reason. A test that
fails on an import error, a typo, a missing fixture, or the wrong assertion is
worthless — it goes green when someone fixes the wrong thing. Prove the failure
is the actual bug before you hand it over.

## Steps

1. **Read the evidence fully.** Stack trace, error message, repro steps,
   expected vs actual. The top frame is the symptom; trace down to the line
   that is actually wrong. Grep the failing function and its callers — the bug
   often lives one level up from where it throws.

2. **Find the seam.** Locate the smallest unit that exercises the bug: a pure
   function beats an HTTP round-trip beats a full E2E flow. Reproduce at the
   lowest layer that still shows the reported failure.

3. **Match the repo.** Detect the existing test framework, directory, naming,
   and fixtures (`pytest`, `jest`/`vitest`, `go test`, `rspec`, …). Put the
   test where the sibling tests live. Do not introduce a framework — if there
   are no tests at all, say so and use the language's stdlib test tool.

4. **Write ONE test.** Arrange the exact state from the report, act, assert the
   *correct* behavior. It fails now because the code is wrong. Name it for the
   bug (`test_negative_qty_underflows_total`), not the function. Add a one-line
   comment linking the issue/trace.

5. **Run it. Confirm it's red for the right reason.** Execute the test. Read the
   failure output and verify it matches the reported symptom — same exception,
   same wrong value. If it fails for any other reason, the repro is wrong; fix
   the test, not the code.

## Output

Report in this shape, nothing more:

```
Bug: <one line — what's actually broken and where: file:line>
Test: <path::testname>
Red: <the assertion/exception that fires, quoting the actual run output>
Fix hint: <one line — the root cause, so the next step knows where to go>
```

Then stop. Do not edit the source to make it pass unless the user asks for the
fix too.

## Boundaries

- One test, not a suite. The narrowest case that proves the bug. YAGNI on edge
  cases the report didn't mention.
- Reproduce, don't fix. If the bug is environmental (network, clock, ordering)
  and can't be made deterministic, say so and write the closest deterministic
  test, marking what you had to pin.
- Can't reproduce from the given info? Name the exact missing fact (a value, a
  version, a step) instead of guessing a test into existence.
