import asyncio
import math
from datetime import date, timedelta
from typing import Any

import transports
import uvicorn
from pydantic import BaseModel
from spaday import SetField, ToggleField, cond, element, field
from spaday.backends.starlette import serve
from starlette.routing import WebSocketRoute

from spaday_lightweight_charts import LightweightChart, package

days = [date(2026, 6, 16) + timedelta(days=index) for index in range(60)]
closes = [round(176 + index * 0.42 + math.sin(index / 3) * 5.5, 2) for index in range(60)]
prices = [{"time": day.isoformat(), "value": close} for day, close in zip(days, closes, strict=True)]
volume = [
    {
        "time": day.isoformat(),
        "value": 1_100_000 + int(abs(math.cos(index / 4)) * 900_000),
        "color": "#6366f1" if index == 0 or close >= closes[index - 1] else "#f43f5e",
    }
    for index, (day, close) in enumerate(zip(days, closes, strict=True))
]
candles = [
    {
        "time": day.isoformat(),
        "open": round(close - math.sin(index) * 2.1, 2),
        "high": round(close + 2.4 + abs(math.cos(index)), 2),
        "low": round(close - 2.8 - abs(math.sin(index)), 2),
        "close": close,
    }
    for index, (day, close) in enumerate(zip(days, closes, strict=True))
]


class ChartFeed(BaseModel):
    data: list[dict[str, Any]]
    last_price: str
    change: str


feed = ChartFeed(
    data=prices,
    last_price=f"${closes[-1]:,.2f}",
    change=f"+{closes[-1] - closes[0]:.2f}",
)
session = transports.Session()
session.host(feed)
server = transports.Server(session)


async def stream_prices() -> None:
    index = len(prices)
    while True:
        await asyncio.sleep(1)
        close = round(176 + index * 0.42 + math.sin(index / 3) * 5.5, 2)
        point = {"time": (days[0] + timedelta(days=index)).isoformat(), "value": close}
        feed.data = [*feed.data[1:], point]
        feed.last_price = f"${close:,.2f}"
        feed.change = f"{close - float(feed.data[0]['value']):+.2f}"
        index += 1


def chart(component: LightweightChart) -> LightweightChart:
    return component.compute("theme", cond(field("dark"), "dark", "light"))


price_chart = chart(LightweightChart(data=prices, style="height: 24rem").bind("data", "data").bind("type", "series_type"))
candle_chart = chart(LightweightChart(type="candlestick", data=candles, style="height: 20rem"))
volume_chart = chart(LightweightChart(type="histogram", data=volume, style="height: 20rem"))

page = element(
    "main",
    element(
        "header",
        element("div", element("p", class_="eyebrow").text("MARKET OVERVIEW"), element("h1").text("Lightweight Charts dashboard")),
        element("button", class_="theme-button").text("Toggle theme").on("click", ToggleField("dark")),
        class_="page-header",
    ),
    element(
        "section",
        element("article", element("span").text("Last price"), element("strong").bind("textContent", "last_price")),
        element("article", element("span").text("60-day change"), element("strong").bind("textContent", "change")),
        element(
            "article", element("span").text("Peak volume"), element("strong").text(f"{max(point['value'] for point in volume) / 1_000_000:.1f}M")
        ),
        class_="metrics",
    ),
    element(
        "section",
        element(
            "div",
            element("div", element("h2").text("Price history"), element("p").text("Switch the same live series between renderers.")),
            element(
                "div",
                element("button").text("Area").on("click", SetField("series_type", "area")),
                element("button").text("Line").on("click", SetField("series_type", "line")),
                element("button").text("Histogram").on("click", SetField("series_type", "histogram")),
                class_="segmented",
            ),
            class_="chart-heading",
        ),
        price_chart,
        class_="chart-card featured",
    ),
    element(
        "section",
        element(
            "article",
            element("h2").text("OHLC candles"),
            element("p").text("Sixty daily open, high, low, and close records."),
            candle_chart,
            class_="chart-card",
        ),
        element(
            "article",
            element("h2").text("Trading volume"),
            element("p").text("Per-bar colors are passed through with each data point."),
            volume_chart,
            class_="chart-card",
        ),
        class_="chart-grid",
    ),
).compute("class", cond(field("dark"), "dashboard dark", "dashboard"))

styles = """
<style>
  :root { color-scheme: light dark; }
  body { margin: 0; background: #eef2ff; }
  .dashboard { min-height: 100vh; box-sizing: border-box; padding: 2.5rem; color: #172033;
    background: radial-gradient(circle at top right, #dbeafe, transparent 35%), #f8fafc;
    font-family: Inter, ui-sans-serif, system-ui, sans-serif; transition: .2s ease; }
  .dashboard.dark { color: #e5e7eb; background: radial-gradient(circle at top right, #312e81, transparent 35%), #0f172a; }
  .page-header, .chart-heading { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
  .page-header, .metrics, .chart-grid, .chart-card { max-width: 78rem; margin-inline: auto; }
  h1 { margin: .2rem 0 0; font-size: clamp(2rem, 5vw, 3.25rem); letter-spacing: -.04em; }
  h2 { margin: 0; font-size: 1.1rem; } p { color: #64748b; margin: .4rem 0 0; }
  .dark p { color: #94a3b8; }
  .eyebrow { color: #4f46e5; font-size: .75rem; font-weight: 800; letter-spacing: .16em; }
  button { border: 1px solid #c7d2fe; border-radius: .65rem; padding: .6rem .9rem; background: #fff; color: #3730a3; cursor: pointer; font-weight: 700; }
  button:hover { background: #eef2ff; } .dark button { background: #1e293b; border-color: #475569; color: #e0e7ff; }
  .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-block: 2rem; }
  .metrics article, .chart-card { border: 1px solid rgba(148,163,184,.25); border-radius: 1rem; background: rgba(255,255,255,.88); box-shadow: 0 12px 30px rgba(15,23,42,.06); }
  .dark .metrics article, .dark .chart-card { background: rgba(15,23,42,.8); border-color: #334155; }
  .metrics article { padding: 1.1rem 1.25rem; } .metrics span { display: block; color: #64748b; font-size: .8rem; }
  .metrics strong { display: block; margin-top: .35rem; font-size: 1.4rem; }
  .chart-card { box-sizing: border-box; padding: 1.25rem; min-width: 0; }
  .featured { margin-bottom: 1rem; } .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .segmented { display: flex; gap: .4rem; }
  @media (max-width: 760px) { .dashboard { padding: 1rem; } .page-header, .chart-heading { align-items: flex-start; flex-direction: column; }
    .metrics, .chart-grid { grid-template-columns: 1fr; } }
</style>
"""

app = serve(
    page,
    packages=[package],
    wire="transports",
    routes=[WebSocketRoute("/ws", transports.ws_endpoint(server))],
    background=[transports.autosync(server), stream_prices()],
    store={"series_type": "area", "dark": False},
    head=styles,
    title="spaday-lightweight-charts example",
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8011)
