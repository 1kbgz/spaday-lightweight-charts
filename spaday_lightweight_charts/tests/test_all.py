import ast
from pathlib import Path

from spaday import generate
from spaday.bootstrap import bootstrap

from spaday_lightweight_charts import LightweightChart, package


def _generated_ast(source: str) -> str:
    class Normalize(ast.NodeTransformer):
        def visit_ImportFrom(self, node):
            if node.module == "typing":
                node.names = [name for name in node.names if name.name != "Optional"]
            return node

        def visit_Subscript(self, node):
            node = self.generic_visit(node)
            if isinstance(node.value, ast.Name) and node.value.id == "Optional":
                return ast.BinOp(left=node.slice, op=ast.BitOr(), right=ast.Constant(value=None))
            return node

        def visit_Assign(self, node):
            node = self.generic_visit(node)
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                node.value.elts.sort(key=ast.unparse)
            return node

    return ast.dump(Normalize().visit(ast.parse(source)))


def test_chart_serializes_series_props():
    node = LightweightChart(type="area", data=[{"time": "2026-01-01", "value": 4}], theme="dark").to_node()
    assert node["tag"] == "lightweight-chart"
    assert node["props"]["type"] == {"Str": "area"}
    assert node["props"]["theme"] == {"Str": "dark"}


def test_package_drives_bootstrap_asset_url():
    assert package.name == "lightweight-charts"
    assert [(schema.tag, schema.class_name) for schema in package.catalog] == [("lightweight-chart", "LightweightChart")]
    assert 'src="/components/lightweight-charts/cdn/index.js"' in bootstrap(packages=[package])


def test_generated_component_is_current():
    root = Path(__file__).parent.parent
    fresh = generate(str(root / "components.cem.json"))
    assert _generated_ast(fresh) == _generated_ast((root / "components.py").read_text(encoding="utf-8"))
