from kizuna.core.assets import ImageAsset
from kizuna.core.datatypes import Vector2
from kizuna.rendering import DrawBatch


class SpriteComponent:
    """Specification of a positioned and rotated sprite, as well as the batch it will belong.
    """

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
