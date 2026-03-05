import pyglet

from kizuna.core.assets.base import Asset
from kizuna.core.constants import Alignment


class ImageAsset(Asset):

    def __init__(
        self,
        path: str,
        origin: Alignment = Alignment.CENTER,
    ) -> None:
        super().__init__(path)
        self.origin = origin
        self._pyglet = None
        self.on_load()

    def on_load(self) -> None:
        image = pyglet.resource.image(self.path)
        image.anchor_x, image.anchor_y = (image.width, image.height) * self.origin.value
        self._pyglet = image
