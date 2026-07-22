# Examples

Illustrative bug-report → failing-test walkthroughs (hand-written, not benchmark
output). Each shows the input a dev pastes and the single red test `snare`
produces, plus the one thing that makes it a *good* repro: **it fails for the
reported reason, not any reason.**

| Example | Bug | Layer reproduced at |
|---|---|---|
| [Order total underflow](order-total-underflow.md) | Negative quantity makes a total go negative | Pure function |
| [Pagination off-by-one](pagination-off-by-one.md) | Last row dropped from the final page | Query builder |

The point of every one: a fix without this red test is how the bug comes back.
