# snare

**Reproduce before you fix.** A bug isn't understood until a test fails for it.
`snare` traps the bug in a test so it can't get away.

`snare` turns a bug report, stack trace, or error log into **one failing test**
that reproduces the problem — *before* any fix is written. It finds the real
code path, writes a test in your repo's existing framework, and proves the test
fails for the **reported reason** (not an import error or a typo). Then it stops
and hands you a red test the fix must turn green.

Writing the failing test first is the single highest-leverage debugging habit —
and the one people skip because it's tedious. This automates the tedious part.

## Why "fails for the reported reason" is the whole point

A test that goes red on a missing import, a bad fixture, or the wrong assertion
is worse than no test: it turns green when someone fixes the *wrong* thing, and
the real bug ships anyway. `snare` runs the test and verifies the failure
matches the reported symptom — same exception, same wrong value — before handing
it off.

## Install

```
/plugin marketplace add myselfabdullah007/snare
/plugin install snare
```

## Use

Paste a stack trace or describe the bug, then:

```
/snare
```

or just say "reproduce this" / "write a failing test for this".

You get:

```
Bug:      <what's actually broken and where — file:line>
Test:     <path::testname>
Red:      <the assertion/exception that fires, quoted from the real run>
Fix hint: <the root cause, so the fix step knows where to go>
```

…and then it stops. The fix is a separate step.

## What it deliberately does *not* do

- **Doesn't fix the bug.** Reproduce and fix are separate acts; the red test is
  the deliverable.
- **Doesn't write a suite.** One test, the narrowest case that proves the bug.
- **Doesn't add a test framework.** It uses whatever your repo already has.
- **Doesn't guess.** Can't reproduce from the given info? It names the exact
  missing fact instead of inventing a test.

## Examples

See [examples/](examples/) — a null/underflow bug and an off-by-one pagination
bug, each shown from pasted report to the red test that reproduces it.

## License

MIT — see [LICENSE](LICENSE).
