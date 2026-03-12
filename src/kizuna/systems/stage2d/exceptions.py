from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kizuna.systems.stage2d import Entity2D


class EntityDestroyedException(Exception):
    """Exception raised when trying to perform an operation on a destroyed entity.
    """

    def __init__(self, entity: 'Entity2D'):
        super().__init__(f'Trying to use a destroyed entity: {repr(entity)}')
