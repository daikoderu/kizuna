import pyglet.text

from kizuna.core.assets import ImageAsset
from kizuna.core.datatypes import Vector2
from kizuna.rendering.batches import DrawBatch


class Drawable:

    def __init__(self, visible: bool = True):
        self.visible = visible

    def prepare_for_batch(self, batch: DrawBatch):
        raise NotImplementedError()


class ImageDrawable(Drawable):

    def __init__(
        self,
        asset: ImageAsset,
        position: Vector2 | None = None,
        rotation: float | None = None,
        visible: bool = True,
    ):
        super().__init__(visible)
        self.asset = asset
        self.position = position if position is not None else Vector2(0, 0)
        self.rotation = rotation if rotation is not None else 0
        self._pyglet_instance = None

    @property
    def _pyglet(self):
        if self._pyglet_instance is None:
            self._pyglet_instance = pyglet.sprite.Sprite(self.asset._pyglet)
        return self._pyglet_instance

    def prepare_draw(self, batch: DrawBatch):
        if not self.visible:
            return
        self._pyglet.batch = batch._pyglet if self.visible else None
        self._pyglet.position = self.position.x, self.position.y, 0.0
        self._pyglet.rotation = -self.rotation
