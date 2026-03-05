from kizuna.core.assets import ImageAsset
from kizuna.core.datatypes import Vector2
from kizuna.rendering.batches import DrawBatch
from kizuna.rendering.drawables import ImageDrawable


class Sprite:

    def __init__(
        self,
        asset: ImageAsset,
        batch: DrawBatch | None = None,
        position_offset: Vector2 | None = None,
        rotation_offset: float | None = None,
    ):
        self.asset = asset
        self.batch = batch if batch is not None else DrawBatch()
        self.position_offset = position_offset if position_offset is not None else Vector2(0.0, 0.0)
        self.rotation_offset = rotation_offset if rotation_offset is not None else 0.0


class Entity2D:
    sprites: list[Sprite] = []

    def __init__(
        self,
        position: Vector2 | None = None,
        rotation: float | None = None,
    ):
        self.position = position.copy() if position is not None else Vector2(0.0, 0.0)
        self.rotation = rotation if rotation is not None else 0.0
        self._controller = None
        self._drawables = [ImageDrawable(sprite.asset) for sprite in self.sprites]

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}({id(self)}, position="{self.position}", rotation={self.rotation})'

    @property
    def is_instantiated(self) -> bool:
        return self._controller is not None

    @property
    def batches(self) -> set[DrawBatch]:
        return set(sprite.batch for sprite in self.sprites)

    def prepare_draw(self):
        for sprite, drawable in zip(self.sprites, self._drawables):
            drawable.position = self.position + sprite.position_offset
            drawable.rotation = self.rotation + sprite.rotation_offset
            drawable.prepare_draw(sprite.batch)
