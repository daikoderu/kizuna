from typing import TYPE_CHECKING

from kizuna.core.assets import ImageAsset
from kizuna.core.datatypes import Vector2, validate_vector2
from kizuna.core.validation import validate_float, validate_type
from kizuna.rendering.batches import DrawBatch
from kizuna.rendering.drawables import SpriteDrawable

if TYPE_CHECKING:
    from kizuna.systems.stage2d.controller import Stage2DController


class SpriteSpec:
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


class Entity2D:
    """Game object controlled by the :class:`kizuna.systems.stage2d.Stage2DController`.
    """
    sprite_specs: list[SpriteSpec] = []

    def __init__(
        self,
        controller: 'Stage2DController',
        *,
        position: Vector2 | None = None,
        rotation: float | None = None,
    ):
        """Creates a new entity.

        The entity must be bound to a :class:`kizuna.systems.stage2d.Stage2DController` instance.
        """
        from kizuna.systems.stage2d.controller import Stage2DController

        # Associate the controller with this entity.
        self.controller = validate_type(controller, Stage2DController)
        self.controller._entities.add(self)  # noqa

        # Set initial position and rotation.
        self.position = validate_vector2(position) if position is not None else Vector2(0.0, 0.0)
        self.rotation = validate_float(rotation) if rotation is not None else 0.0

        # Instantiate sprites.
        self.sprites = [SpriteDrawable(sprite.asset) for sprite in self.sprite_specs]

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}({id(self)}, position="{self.position}", rotation={self.rotation})'

    @property
    def batches(self) -> set[DrawBatch]:
        """Returns a set of the batches used by the sprites.
        """
        return set(sprite.batch for sprite in self.sprite_specs)

    @property
    def is_alive(self) -> bool:
        """Returns whether the entity has not been destroyed yet.
        """
        return self.controller is not None

    def destroy(self) -> None:
        """Destroys the entity from the stage, cleaning up any resources.

        Destroyed entities will not be drawn to the screen and should no longer be processed.
        """
        self.controller._entities.remove(self)  # noqa
        self.controller = None

    def prepare_draw(self):
        if not self.is_alive:
            return
        for spec, sprite in zip(self.sprite_specs, self.sprites):
            sprite.position = self.position + spec.position_offset
            sprite.rotation = self.rotation + spec.rotation_offset
            sprite.on_prepare_draw(spec.batch)
