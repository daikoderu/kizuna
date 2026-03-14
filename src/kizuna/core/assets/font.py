from kizuna.config import settings
from kizuna.core.assets.base import Asset
from kizuna.core.assets.paths import AssetPathLike


class FontAsset(Asset):
    """Asset encapsulating a font, including properties such as weight, style and size.

    In addition to the path to the font file, in order to load a font asset the family name must be provided as well.
    """

    def __init__(
        self,
        path: AssetPathLike,
        family_name: str,
        size: int,
        eager: bool = False,
    ) -> None:
        """Define a new asset.

        :param path: Path to the asset, relative to the assets directory of the project.
        :param family_name: The family name of the font.
        :param size: The base size the font will be rendered at.
        :param eager: Whether this asset should be loaded immediately upon definition (``True``) or only until
            required by Kizuna (``False``).
        """
        super().__init__(path, eager)
        self.family_name = family_name
        self.size = size

    def on_load(self) -> None:
        settings.backend.load_font_asset(self)


DEFAULT_FONT_ASSET = FontAsset(
    'builtin:/fonts/mplus-1p/MPLUS1p-Regular.ttf',
    family_name='M PLUS 1p',
    size=12,
)
"""The default, platform-independent font set by Kizuna.
"""
