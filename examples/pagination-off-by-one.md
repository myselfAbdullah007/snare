# Pagination off-by-one

## What the dev pastes

> Users on the last page of results are missing the final row. 25 items, page
> size 10 — page 3 should show items 21–25 but shows 21–24. `paginate()` in
> `repo/query.js`.

No stack trace here — it's a wrong-output bug, not a crash. Same rule applies:
the test must fail on the *missing row*, not on anything else.

## What `snare` does

1. Finds the seam: `paginate(page, size)` builds a LIMIT/OFFSET clause. Reproduce
   against the query builder with a fake 25-row dataset — no live DB needed.
2. Matches the repo: `vitest`, `*.test.js` beside the source.
3. Writes ONE test asserting the correct last-page contents.

```js
// query.test.js
// snare: BUG-231 — last page drops the final row (off-by-one in OFFSET)
import { paginate } from "./query.js";

const rows = Array.from({ length: 25 }, (_, i) => i + 1); // 1..25

test("last page includes the final row", () => {
  const page3 = paginate(rows, { page: 3, size: 10 });
  expect(page3).toEqual([21, 22, 23, 24, 25]);
});
```

4. Runs it, red for the reported reason — the missing `25`:

```
- Expected  [21, 22, 23, 24, 25]
+ Received  [21, 22, 23, 24]
```

The diff shows exactly the symptom the report named. A repro that instead threw
`TypeError: rows.slice is not a function` would be reproducing a different bug.

## Handoff

```
Bug:      paginate() computes end = offset + size - 1, drops one row on the tail. query.js:22
Test:     query.test.js › "last page includes the final row"
Red:      Received [21,22,23,24], expected [21,22,23,24,25]
Fix hint: end index is off by one — root cause is the -1, fixing the last page fixes every page
```

Stops there. One test, narrowest case, the fix turns it green.
