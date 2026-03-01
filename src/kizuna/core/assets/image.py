import pyglet

from pyglet.image import Texture, TextureRegion

from kizuna.core.assets.base import Asset
from kizuna.core.constants import Alignment


class ImageAsset(Asset):

    def __init__(
        self,
        path: str,
        origin: Alignment = Alignment.CENTER,
    ) -> None:
        self.origin = origin
        super().__init__(path)

    def on_load(self) -> Texture | TextureRegion:
        image = pyglet.resource.image(self.path)
        image.anchor_x, image.anchor_y = (image.width, image.height) * self.origin.value
        return image
