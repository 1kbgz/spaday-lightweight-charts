from pathlib import Path

from spaday import ComponentPackage

from .components import LightweightChart

__version__ = "0.1.0"

package = ComponentPackage(
    name="lightweight-charts",
    assets_dir=Path(__file__).parent / "extension",
    assets=(("js", "cdn/index.js"),),
)

__all__ = ["LightweightChart", "package"]
