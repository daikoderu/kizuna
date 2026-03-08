from kizuna.config import settings
from kizuna.core.assets import ImageAsset
from kizuna.core.datatypes import Vector2, validate_vector2
from kizuna.core.validation import validate_float, validate_type
from kizuna.rendering.batches import DrawBatch


class Drawable:
    """Representation of anything that can be drawn to the screen.
    """

    def on_prepare_draw(self, batch: DrawBatch):
        """Implement this method to prepare this drawable to be drawn as part of a batch.

        :param batch: The :class:`DrawBatch` that will be drawn to.
        """
        raise NotImplementedError()


class ImageDrawable(Drawable):
    """Encapsulation of an image that can be drawn to the screen.
    """

    def __init__(
        self,
        asset: ImageAsset,
        position: Vector2 | None = None,
        rotation: float | None = None,
    ):
        self.asset = validate_type(asset, ImageAsset)
        self.asset.load()
        self.position = validate_vector2(position) if position is not None else Vector2(0, 0)
        self.rotation = validate_float(rotation) if rotation is not None else 0

    def on_prepare_draw(self, batch: DrawBatch):
        settings.backend.prepare_draw_sprite(self, batch)
