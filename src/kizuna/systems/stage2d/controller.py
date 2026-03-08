from typing import TypeVar

from kizuna.core.controllers import Controller
from kizuna.core.datatypes import Vector2
from kizuna.systems.stage2d.entities import Entity2D


E = TypeVar('E', bound=Entity2D)


class Stage2DController(Controller):
    """Controller to manage a collection of entities representing different game objects.
    """
    _entities: set[Entity2D] = set()

    def on_draw(self):
        for entity in self._entities:
            entity.prepare_draw()
        all_batches = {batch for entity in self._entities for batch in entity.batches}
        for batch in sorted(all_batches, key=lambda b: -b.priority):
            batch.draw()

    def instantiate(
        self,
        entity_class: type[E],
        position: Vector2 | None = None,
        rotation: float | None = None,
    ) -> E:
        instance = entity_class(position, rotation)
        instance._controller = self
        self._entities.add(instance)
        return instance
