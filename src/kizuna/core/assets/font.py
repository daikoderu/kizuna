from kizuna.config import settings
from kizuna.core.assets.base import Asset
from kizuna.core.assets.paths import AssetPathLike


class FontAsset(Asset):
    """Asset encapsulating a font.
    """

    def __init__(
        self,
        path: AssetPathLike,
        family_name: str,
        size: int,
    ) -> None:
        """Define a new asset.

        :param path: Path to the asset, relative to the assets directory of the project.
        """
        super().__init__(path)
        self.family_name = family_name
        self.size = size

    def on_load(self) -> None:
        settings.backend.load_font_asset(self)


DEFAULT_FONT_ASSET = FontAsset('builtin:/fonts/mplus-1p/MPLUS1p-Regular.ttf', family_name='M PLUS 1p', size=12)
