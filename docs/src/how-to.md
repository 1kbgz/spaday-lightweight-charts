# How to update chart data and appearance

This guide shows how to drive an existing chart from application state.

## Bind a live series

Bind `data` to the store field that owns the series:

```python
from spaday_lightweight_charts import LightweightChart

chart = LightweightChart(type="line").bind("data", "prices")
```

Set `prices` to either an ordered point list or a time-keyed mapping. A transports-backed store can
update the same field without rebuilding the component tree.

```python
store={
    "prices": {
        "2026-01-01": 101.5,
        "2026-01-02": 103.25,
    }
}
```

## Switch series type

Bind `type` when users need to switch renderers:

```python
LightweightChart().bind("type", "series_type").bind("data", "prices")
```

Valid values are `line`, `area`, `candlestick`, `bar`, and `histogram`.

## Match a dark surface

Set or bind `theme`:

```python
LightweightChart(theme="dark", data=prices)
```

The wrapper keeps its background transparent and updates chart text and grid colors.

Refer to the [API reference](reference.md) for exact prop shapes.
