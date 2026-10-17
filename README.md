<div align="center">

<img src="assets/banner.svg" alt="snare — reproduce before you fix" width="100%">

<br>

[![release](https://img.shields.io/github/v/release/myselfAbdullah007/snare?color=3fb950&label=release)](https://github.com/myselfAbdullah007/snare/releases)
[![license](https://img.shields.io/github/license/myselfAbdullah007/snare?color=58a6ff)](LICENSE)
![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-8b5cf6)
![zero dependencies](https://img.shields.io/badge/deps-0-6e7681)

**Turn a bug report or stack trace into _one failing test_ that reproduces it — before any fix.**

</div>

---

## The problem

Everyone knows you should write a failing test before fixing a bug. Almost nobody does — it's tedious, and "I can see the bug right there" wins. So the fix lands with no test, the next refactor quietly brings the bug back, and you debug it twice.

Worse are the tests people *do* rush out, which fail in two useless ways:

- **Failing for the wrong reason** — a missing import, a bad fixture, a typo'd assertion. It goes green the moment someone fixes something unrelated, and the real bug ships anyway.
- **Not failing at all** — the reported wrong value gets written straight into the assertion (`assert total == -200`). The test passes today, passes forever, and pins the bug in place.

`snare` exists to rule out both before it hands anything over.

## What it does

Paste a stack trace or describe the bug. `snare`:

1. **Reads the evidence** and traces from the top frame down to the line that's actually wrong — including one level up, where the bug usually lives.
2. **Finds the lowest seam** that still shows the failure. A pure function beats an HTTP round-trip beats a full E2E flow.
3. **Writes ONE test** in your repo's existing framework, arranging the reported state and asserting the *correct* behavior — so it fails today.
4. **Runs that one test** — not the suite — and triages the output against a fixed table: same symptom means hand off; anything else means fix the test, never the source.
5. **Stops.** It does not fix the bug. The red test is the deliverable; the fix must turn it green.

## Install

```
/plugin marketplace add myselfAbdullah007/snare
/plugin install snare
```

## Use

Paste a stack trace or describe the bug, then:

```
/snare
```

…or just say *"reproduce this"* / *"write a failing test for this"*. You get back:

```
Bug:      what's actually broken and where — file:line
Test:     path::testname
Red:      the assertion/exception that fires, quoted from the real run
Fix hint: the root cause, so the fix step knows where to go
```

…and then it stops.

## What counts as a valid repro

The run output decides. `snare` won't report until it lands in the first row:

| What the test run printed | Verdict |
|---|---|
| Same exception / wrong value as reported | **Valid** — hand off |
| Test passed | Repro is wrong — the assertion encodes the bug, not the contract |
| `ImportError`, `SyntaxError`, collection error | The test is broken, not the code |
| Fixture or setup error | Wrong seam, or incomplete arrange |
| A different exception or unrelated wrong value | Wrong code path — re-trace |

## Examples

| Example | Bug | Reproduced at |
|---|---|---|
| [Order total underflow](examples/order-total-underflow.md) | Negative quantity drives a total below zero | Pure function |
| [Pagination off-by-one](examples/pagination-off-by-one.md) | Last row dropped from the final page | Query builder |

Each shows the input a dev pastes and the exact red test `snare` produces.

## What it deliberately won't do

- **Won't fix the bug.** Reproduce and fix are separate acts; the red test is the handoff.
- **Won't write a suite.** One test, the narrowest case that proves the bug.
- **Won't add a framework.** It uses whatever your repo already has — no installs.
- **Won't touch anything else.** No edits to source, no edits to existing tests.
- **Won't guess.** Can't reproduce from the given info? It names the exact missing fact instead of inventing a test.

## Repo layout

```
.claude-plugin/
  plugin.json        plugin manifest
  marketplace.json   self-hosted marketplace entry
skills/snare/
  SKILL.md           the skill — model-invoked, the whole implementation
commands/
  snare.toml         /snare — the same procedure, user-invoked
examples/            bug report → red test walkthroughs
scripts/check.py     manifest + frontmatter validator (stdlib only)
.github/workflows/   runs the validator on push
assets/              banner and logo
```

`snare` is a *triggered* skill, not a background mode — it fires when you call it and gets out of the way. No hooks, no persistent state, no dependencies. The skill is a single prompt file; everything else is manifest, command, and docs.

## License

[MIT](LICENSE) © Abdullah Chaudhary
