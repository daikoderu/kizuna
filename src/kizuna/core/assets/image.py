from kizuna.config import settings
from kizuna.core.assets.base import Asset
from kizuna.core.constants import Alignment


class ImageAsset(Asset):
    """Asset encapsulating an image.
    """

    def __init__(
        self,
        path: str,
        origin: Alignment = Alignment.CENTER,
    ) -> None:
        """Define a new asset.

        :param path: Path to the asset, relative to the assets directory of the project.
        :param origin: Origin of the image, used for drawing.
        """
        super().__init__(path)
        self.origin = origin

    def on_load(self) -> None:
        settings.backend.load_image_asset(self)
