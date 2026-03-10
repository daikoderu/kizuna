from kizuna.config import settings
from kizuna.core.assets import Asset


class FontAsset(Asset):
    """Asset encapsulating a font.
    """

    def __init__(
        self,
        path: str,
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
