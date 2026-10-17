# Order total underflow

## What the dev pastes

> Customer reported a $-12.00 order total. Support says they edited a line item
> quantity to a negative number in the cart and the total went negative instead
> of rejecting it. Code is in `cart.py`.

```
Actual:   cart_total([{"price": 400, "qty": -3}, {"price": 500, "qty": 2}]) -> -200
Expected: negative qty is not a valid line; total should never go below 0
```

## What `snare` does — not fix, reproduce

1. Reads `cart.py`, finds the seam: `cart_total()` is a pure function. No need
   to spin up the checkout flow — reproduce right there.
2. Matches the repo: tests live in `tests/`, `pytest`, files named `test_*.py`.
3. Writes ONE test asserting the **correct** behavior, so it fails today.

```python
# tests/test_cart.py
# snare: issue #418 — negative qty makes total go negative instead of being rejected
from cart import cart_total

def test_negative_qty_does_not_underflow_total():
    total = cart_total([{"price": 400, "qty": -3}, {"price": 500, "qty": 2}])
    assert total >= 0, f"negative qty underflowed the total: {total}"
```

4. Runs it, confirms it's red **for the reported reason**:

```
E   AssertionError: negative qty underflowed the total: -200
E   assert -200 >= 0
```

That `-200` is the exact symptom from the report — not an import error, not a
missing fixture. If the assertion had fired on `KeyError: 'price'`, the repro
would be wrong and `snare` fixes the test, not the code.

## Handoff

```
Bug:      cart_total() sums price*qty with no floor; negative qty subtracts. cart.py:14
Test:     tests/test_cart.py::test_negative_qty_does_not_underflow_total
Red:      AssertionError: negative qty underflowed the total: -200
Fix hint: reject or clamp qty < 0 before summing — root cause is the missing guard, not the sum
```

Then it stops. The fix is a separate step; this red test is the deliverable it
must turn green.
