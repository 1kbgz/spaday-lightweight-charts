from pathlib import Path

from spaday import ComponentPackage

from .components import LightweightChart

__version__ = "0.2.0"

package = ComponentPackage(
    name="lightweight-charts",
    assets_dir=Path(__file__).parent / "extension",
    assets=(("js", "cdn/index.js"),),
    components=(LightweightChart,),
)

__all__ = ["LightweightChart", "package"]
