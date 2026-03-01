from enum import Enum

from kizuna.core.datatypes import Vector2


class Alignment(Enum):
    BOTTOM_LEFT = Vector2(0.0, 0.0)
    BOTTOM_CENTER = Vector2(0.5, 0.0)
    BOTTOM_RIGHT = Vector2(1.0, 0.0)
    MIDDLE_LEFT = Vector2(0.0, 0.5)
    CENTER = Vector2(0.5, 0.5)
    MIDDLE_RIGHT = Vector2(1.0, 0.5)
    TOP_LEFT = Vector2(0.0, 1.0)
    TOP_CENTER = Vector2(0.5, 1.0)
    TOP_RIGHT = Vector2(1.0, 1.0)