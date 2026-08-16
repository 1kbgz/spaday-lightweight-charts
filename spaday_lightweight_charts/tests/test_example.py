import asyncio

import httpx
import pytest

from spaday_lightweight_charts import example


async def request(method: str, path: str, **kwargs):
    transport = httpx.ASGITransport(app=example.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://example") as client:
        return await client.request(method, path, **kwargs)


def test_example_serves_dashboard_and_streams_prices(monkeypatch):
    response = asyncio.run(request("GET", "/tree.json"))
    assert response.status_code == 200
    assert "lightweight-chart" in response.text

    initial_point = example.feed.data[-1]
    sleeps = 0

    class StreamComplete(Exception):
        pass

    async def one_tick(_delay):
        nonlocal sleeps
        sleeps += 1
        if sleeps > 1:
            raise StreamComplete

    monkeypatch.setattr(example.asyncio, "sleep", one_tick)
    with pytest.raises(StreamComplete):
        asyncio.run(example.stream_prices())

    assert example.feed.data[-1] != initial_point
    assert example.feed.last_price.startswith("$")
