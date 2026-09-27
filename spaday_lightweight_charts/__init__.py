import json
from pathlib import Path

from spaday import ComponentPackage, Token

from .components import LightweightChart

__version__ = "0.3.0"

# the exact version of each JS library the package serves, written by its JS build
_VERSIONS = Path(__file__).parent / "extension" / "versions.json"

package = ComponentPackage(
    name="lightweight-charts",
    assets_dir=Path(__file__).parent / "extension",
    assets=(("css", "css/index.css"), ("js", "cdn/index.js")),
    components=(LightweightChart,),
    provides=json.loads(_VERSIONS.read_text(encoding="utf-8")) if _VERSIONS.exists() else {},
)

#: ``css()`` kwarg → (CSS custom property, what it controls).
#:
#: The chart is a canvas and cannot read CSS itself, so it samples the resolved value of each of
#: these when its ``theme`` property is set — theming works the same way as every other package::
#:
#:     LightweightChart(data=d).css(spa_lightweight_charts_grid="#AECEC3")
TOKENS = {
    "spa_lightweight_charts_text": Token("--spa-lightweight-charts-text", "axis and legend text", fallback="--spa-text"),
    "spa_lightweight_charts_grid": Token("--spa-lightweight-charts-grid", "grid line color", fallback="--spa-border"),
    "spa_lightweight_charts_background": Token(
        "--spa-lightweight-charts-background",
        "chart background (transparent by default, so the surface behind shows through)",
    ),
}

__all__ = ["TOKENS", "LightweightChart", "package"]
