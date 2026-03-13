from kizuna.config import settings
from kizuna.core.assets.base import Asset
from kizuna.core.assets.paths import AssetPathLike
from kizuna.core.constants import Alignment
from kizuna.core.datatypes import Vector2Like, validate_vector2


class ImageAsset(Asset):
    """Asset encapsulating an image.
    """

    def __init__(
        self,
        path: AssetPathLike,
        origin: Alignment | Vector2Like = Alignment.CENTER,
    ) -> None:
        """Define a new asset.

        :param path: Path to the asset, relative to the assets directory of the project.
        :param origin: Origin of the image, used for drawing.
        """
        super().__init__(path)
        self.origin = origin.value if isinstance(origin, Alignment) else validate_vector2(origin)

    def on_load(self) -> None:
        settings.backend.load_image_asset(self)
