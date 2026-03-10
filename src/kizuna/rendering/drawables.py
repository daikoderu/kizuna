from kizuna.config import settings
from kizuna.core.assets import ImageAsset, FontAsset
from kizuna.core.datatypes import Vector2, validate_vector2, Vector2Like
from kizuna.core.validation import validate_float, validate_type
from kizuna.rendering.batches import DrawBatch


class Drawable:
    """Representation of anything that can be drawn to the screen.
    """

    def __init__(self, visible: bool = True):
        self.visible = visible

    def on_prepare_draw(self, batch: DrawBatch):
        """Implement this method to prepare this drawable to be drawn as part of a batch.

        :param batch: The :class:`DrawBatch` that will be drawn to.
        """
        raise NotImplementedError()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.__class__.__name__


class TextDrawable(Drawable):
    """Text to be drawn to the screen.
    """

    def __init__(
        self,
        text: str,
        font: FontAsset,
        position: Vector2Like | None = None,
        visible: bool = True,
    ):
        super().__init__(visible)
        self.text = str(text)
        self.font = validate_type(font, FontAsset)
        font.load()
        self.position = validate_vector2(position) if position is not None else Vector2(0, 0)

    def on_prepare_draw(self, batch: DrawBatch):
        settings.backend.prepare_draw_text(self, batch)

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.text}", asset={repr(self.font)})'


class SpriteDrawable(Drawable):
    """Encapsulation of an image that can be drawn to the screen.
    """

    def __init__(
        self,
        asset: ImageAsset,
        position: Vector2Like | None = None,
        rotation: float | None = None,
        visible: bool = True,
    ):
        super().__init__(visible)
        self.asset = validate_type(asset, ImageAsset)
        asset.load()
        self.position = validate_vector2(position) if position is not None else Vector2(0, 0)
        self.rotation = validate_float(rotation) if rotation is not None else 0
        self.visible = True

    def on_prepare_draw(self, batch: DrawBatch):
        settings.backend.prepare_draw_sprite(self, batch)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.asset)})'
