import ast
from pathlib import Path

from spaday import generate
from spaday.bootstrap import bootstrap

from spaday_lightweight_charts import LightweightChart, package


def test_chart_serializes_series_props():
    node = LightweightChart(type="area", data=[{"time": "2026-01-01", "value": 4}], theme="dark").to_node()
    assert node["tag"] == "lightweight-chart"
    assert node["props"]["type"] == {"Str": "area"}
    assert node["props"]["theme"] == {"Str": "dark"}


def test_package_drives_bootstrap_asset_url():
    assert package.name == "lightweight-charts"
    assert 'src="/components/lightweight-charts/cdn/index.js"' in bootstrap(packages=[package])


def test_generated_component_is_current():
    root = Path(__file__).parent.parent
    fresh = generate(str(root / "components.cem.json"))
    assert ast.dump(ast.parse(fresh)) == ast.dump(ast.parse((root / "components.py").read_text(encoding="utf-8")))
