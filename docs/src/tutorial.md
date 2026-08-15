# Build a live chart

In this tutorial, we will serve an area chart and replace its data from browser state.

## Install the packages

```bash
pip install "spaday[examples]" spaday-lightweight-charts
```

## Create the chart

Save this as `chart_app.py`:

```python
import uvicorn

from spaday import SetField, element
from spaday.backends.starlette import serve
from spaday_lightweight_charts import LightweightChart

initial = [
    {"time": "2026-01-01", "value": 10},
    {"time": "2026-01-02", "value": 14},
]

chart = LightweightChart(
    type="area",
    data=initial,
    style="height: 24rem",
).bind("data", "series")

replace = element("button").text("Replace data").on(
    "click",
    SetField(
        "series",
        [
            {"time": "2026-01-01", "value": 18},
            {"time": "2026-01-02", "value": 12},
        ],
    ),
)

app = serve(
    element("main", chart, replace),
    packages=["lightweight-charts"],
    store={"series": initial},
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Run the app:

```bash
python chart_app.py
```

Open the printed local URL. You should see an area chart spanning two dates. Click **Replace data**;
the same canvas updates without replacing the custom element.

You now have a chart driven by serializable spaday state. Continue with
[Update chart data and appearance](how-to.md) for production update patterns.

For a larger application with three chart types, server-streamed prices, renderer controls, and theming, run the
[complete dashboard example](../../spaday_lightweight_charts/example.py).
