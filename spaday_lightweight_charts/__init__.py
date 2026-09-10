import json
from pathlib import Path

from spaday import ComponentPackage

from .components import LightweightChart

__version__ = "0.2.1"

# the exact version of each JS library the package serves, written by its JS build
_VERSIONS = Path(__file__).parent / "extension" / "versions.json"

package = ComponentPackage(
    name="lightweight-charts",
    assets_dir=Path(__file__).parent / "extension",
    assets=(("css", "css/index.css"), ("js", "cdn/index.js")),
    components=(LightweightChart,),
    provides=json.loads(_VERSIONS.read_text(encoding="utf-8")) if _VERSIONS.exists() else {},
)

#: ``css()`` kwarg → (CSS custom property, what it controls), in the shape of
#: :data:`spaday.theme.SHELL_TOKENS`.
#:
#: The chart is a canvas and cannot read CSS itself, so it samples the resolved value of each of
#: these when its ``theme`` property is set — theming works the same way as every other package::
#:
#:     LightweightChart(data=d).css(spa_lightweight_charts_grid="#AECEC3")
TOKENS = {
    "spa_lightweight_charts_text": ("--spa-lightweight-charts-text", "axis and legend text (defaults to --spa-muted)"),
    "spa_lightweight_charts_grid": ("--spa-lightweight-charts-grid", "grid line color (defaults to --spa-border)"),
    "spa_lightweight_charts_background": (
        "--spa-lightweight-charts-background",
        "chart background (transparent by default, so the surface behind shows through)",
    ),
}

__all__ = ["TOKENS", "LightweightChart", "package"]
