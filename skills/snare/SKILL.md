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

## Two rules, in order

**1. Assert the behavior that SHOULD happen, never the behavior you observed.**
This is the mistake that ruins the task. The report hands you a wrong value;
writing it into the assertion produces a test that passes today and never
catches anything.

```python
assert total == -200   # WRONG — pins the bug in place, green forever
assert total >= 0      # RIGHT — encodes the contract, red until it's fixed
```

**2. The test must fail for the REPORTED reason, not any reason.** A test that
fails on an import error, a bad fixture, or a typo goes green when someone
fixes something unrelated, and the real bug ships anyway. Prove the failure
matches the symptom before handing it over.

## Steps

1. **Read the evidence fully.** Stack trace, error message, repro steps,
   expected vs actual. The top frame is the symptom; trace down to the line
   that is actually wrong. Grep the failing function and its callers — the bug
   often lives one level up from where it throws.

2. **Find the seam.** Locate the smallest unit that exercises the bug: a pure
   function beats an HTTP round-trip beats a full E2E flow. Reproduce at the
   lowest layer that still shows the reported failure. If the bug only appears
   through a seam you cannot reach cheaply (real network, real clock, real
   ordering), say so and pin the non-determinism explicitly rather than
   skipping to a higher layer.

3. **Match the repo.** Detect the existing framework, test directory, naming
   convention, and fixtures before writing a line. Put the test where its
   siblings live. Never introduce or install a framework — if the repo has no
   tests at all, say so and use the language's stdlib test tool.

4. **Write ONE test.** Arrange the exact state from the report, act, assert the
   correct behavior (rule 1). Name it for the bug, not the function —
   `test_negative_qty_does_not_underflow_total`, not `test_cart_total`. Add one
   comment line linking the issue or trace. Touch nothing else: no edits to
   source, no edits to existing tests, no new helpers.

5. **Run that one test — not the suite.** Use the narrowest invocation the
   framework offers:

   | Framework | Run one test |
   |---|---|
   | pytest | `pytest path/test_x.py::test_name -x` |
   | jest | `npx jest path/x.test.js -t "test name"` |
   | vitest | `npx vitest run path/x.test.js -t "test name"` |
   | go test | `go test ./pkg -run '^TestName$'` |
   | cargo | `cargo test test_name -- --exact` |
   | rspec | `bundle exec rspec path/x_spec.rb:LINE` |
   | maven / gradle | `mvn test -Dtest=Class#method` / `gradle test --tests Class.method` |
   | dotnet | `dotnet test --filter FullyQualifiedName~TestName` |

   Prefer the repo's own wrapper if it has one (`make test`, `npm test --`,
   `./scripts/test`) with the single-test filter passed through.

6. **Triage the output before you report.** Match what you got against this
   table and act on it — do not hand over a repro you haven't cleared:

   | What the run printed | Verdict |
   |---|---|
   | Same exception / same wrong value as the report | **Correct.** Hand off. |
   | Test **passed** | Repro is wrong. You asserted the observed value (rule 1), arranged state the bug doesn't trigger on, or picked a seam that bypasses it. Re-read the report. |
   | `ImportError`, `ModuleNotFoundError`, `SyntaxError`, collection error | Test is broken, not the code. Fix the test. |
   | Fixture / setup / teardown error | Wrong seam or incomplete arrange. Fix the test. |
   | Different exception type, or a wrong value that isn't the reported one | You're on a different code path. Re-trace from step 1. |

   Every verdict but the first means fix the **test**, never the source.

## Output

Report in this shape, nothing more:

```
Bug: <one line — what's actually broken and where: file:line>
Test: <path::testname>
Red: <the assertion/exception that fires, quoting the actual run output>
Fix hint: <one line — the root cause, so the next step knows where to go>
```

Then stop. Do not edit the source to make it pass unless the user explicitly
asks for the fix too. Handing over a green test is task failure.

## Boundaries

- One test, not a suite. The narrowest case that proves the bug. YAGNI on edge
  cases the report didn't mention.
- Reproduce, don't fix. If the bug is environmental (network, clock, ordering)
  and can't be made deterministic, write the closest deterministic test and
  state what you had to pin.
- Can't reproduce from the given info? Name the exact missing fact — a value, a
  version, a step — instead of guessing a test into existence. A named gap is a
  useful answer; an invented repro is not.
