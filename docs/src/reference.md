# API reference

## `LightweightChart`

Tag: `<lightweight-chart>`.

| Prop    | Type                  | Default   | Description                                      |
| ------- | --------------------- | --------- | ------------------------------------------------ |
| `type`  | `str`                 | `"line"`  | Series renderer.                                 |
| `data`  | list or mapping       | `[]`      | Points accepted by the selected series renderer. |
| `theme` | `"light"` or `"dark"` | `"light"` | Text and grid color mode.                        |

A mapping passed to `data` is converted from `{time: value}` to sorted `{time, value}` points. An
array is passed to Lightweight Charts unchanged.

Supported series types are `line`, `area`, `candlestick`, `bar`, and `histogram`.

```{eval-rst}
.. autoclass:: spaday_lightweight_charts.LightweightChart
   :members:
```

## `package`

`spaday_lightweight_charts.package` is a `spaday.ComponentPackage` named `lightweight-charts`. It serves
the self-contained registration bundle at `cdn/index.js`. Its `components` collection contains
`LightweightChart`; `catalog` returns the component's property, event, and slot schema.

Select it by descriptor or entry-point name:

```python
serve(chart, packages=[package])
serve(chart, packages=["lightweight-charts"])
```
