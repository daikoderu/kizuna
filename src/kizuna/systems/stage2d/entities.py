from typing import TYPE_CHECKING

from kizuna.core.datatypes import Vector2, validate_vector2, Vector2Like
from kizuna.core.validation import validate_float, validate_type
from kizuna.rendering.batches import DrawBatch
from kizuna.rendering.drawables import SpriteDrawable
from kizuna.systems.stage2d.components import SpriteComponent
from kizuna.systems.stage2d.exceptions import EntityDestroyedException

if TYPE_CHECKING:
    from kizuna.systems.stage2d.controller import Stage2DController


class Entity2D:
    """Game object controlled by the :class:`kizuna.systems.stage2d.controller.Stage2DController`.

    Entities have 2D position and rotation attributes.

    Existing entities in the scene must always be bound to the Stage2DController.

    To define different types of entities that will appear in the scene, subclass this class and define the following:

    *   The ``sprites`` class attribute is a list of :class:`kizuna.systems.stage2d.components.SpriteComponent` objects
        that define the sprite or sprites that will appear.

    Entities are instantiated calling the entity class with the controller, its position and optionally a rotation,
    along with any additional arguments you may add specific to a subclass, and can be destroyed to free resources
    when no longer needed, either for performance or gameplay purposes.

    ..  important::

        Beware of keeping references to destroyed entities! Use :attr:`is_alive` to check whether the entity is alive.

        Do not store references to such entities to let the garbage collector free the memory used by them.
    """
    sprites: list[SpriteComponent] = []

    def __init__(self, controller: 'Stage2DController', position: Vector2Like, rotation: float = 0.0):
        """Creates a new entity.

        The entity must be bound to a :class:`kizuna.systems.stage2d.Stage2DController` instance.
        """
        from kizuna.systems.stage2d.controller import Stage2DController

        # Associate the controller with this entity.
        self.controller = validate_type(controller, Stage2DController)
        self.controller._entities.add(self)  # noqa

        # Set initial position and rotation.
        self.position = validate_vector2(position) if position is not None else Vector2(0.0, 0.0)
        self.rotation = validate_float(rotation)

        # Instantiate sprite components as drawables.
        self._drawables = [
            SpriteDrawable(component.asset, component.position_offset, component.rotation_offset)
            for component in self.sprites
        ]

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        text = f'{self.__class__.__qualname__}({id(self)}, position="{self.position}", rotation={self.rotation})'
        if not self.is_alive:
            text += '[DESTROYED]'
        return text

    @property
    def batches(self) -> set[DrawBatch]:
        """Returns a set of the batches used by the sprites.
        """
        if not self.is_alive:
            return set()
        return set(sprite.batch for sprite in self.sprites)

    @property
    def is_alive(self) -> bool:
        """Returns whether the entity has not been destroyed yet.
        """
        return self.controller is not None

    def get_drawable(self, index: int) -> SpriteDrawable:
        """Return the drawable corresponding to the given index in the ``sprites`` attribute.

        :param index: The index of the drawable to return.
        :raise IndexError: If the index is not in the ``sprites`` attribute.
        :raise EntityDestroyedException: If the entity has been destroyed.
        """
        return self._drawables[index]

    def destroy(self) -> None:
        """Destroys the entity from the stage, cleaning up any resources.

        Destroyed entities will not be drawn to the screen and should no longer be processed.
        """
        # Unlink the controller.
        self.controller._entities.remove(self)  # noqa
        self.controller = None

        # Destroy the associated drawables.
        for sprite in self._drawables:
            sprite.on_destroy()

    def prepare_draw(self):
        if not self.is_alive:
            return
        for component, sprite in zip(self.sprites, self._drawables):
            sprite.position = self.position + component.position_offset
            sprite.rotation = self.rotation + component.rotation_offset
            sprite.on_prepare_draw(component.batch)

    def _ensure_alive(self):
        if not self.is_alive:
            raise EntityDestroyedException(self)
