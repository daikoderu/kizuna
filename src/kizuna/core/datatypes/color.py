from dataclasses import dataclass
from typing import Any

from kizuna.core.validation import validate_int, clamp_int


type ColorTuple = tuple[int, int, int, int] | tuple[int, int, int]
"""Alias for a tuple that represents a color.
"""


@dataclass
class Color:
    """Tuples of four integers between 0 and 255 to define colors in ``(r, g, b, a)`` format.

    For the sake of brevity and consistency, any function parameter or attribute expected to be of type Color can
    also be set to a tuple of four integers. It will be converted to an instance of this class.

    Out-of-bounds values are automatically clamped. If the class is called with three values, these correspond to
    red, green, and blue, respectively, and the alpha (transparency) is set to 255 (fully opaque).
    """
    r: int
    g: int
    b: int
    a: int = 255

    def __post_init__(self):
        """Validate color components.
        """
        self.r = clamp_int(validate_int(self.r), 0, 255)
        self.g = clamp_int(validate_int(self.g), 0, 255)
        self.b = clamp_int(validate_int(self.b), 0, 255)
        self.a = clamp_int(validate_int(self.a), 0, 255)

    @property
    def as_tuple(self) -> tuple[int, int, int, int]:
        """Return the color as a normal tuple.
        """
        return self.r, self.g, self.b, self.a

    def __iter__(self):
        """Iterator over the color components.

        This allows easy destructuring.
        """
        return iter(self.as_tuple)

    def __eq__(self, other: Any) -> bool:
        """Component-wise equality of two colors.

        :param other: The other color.
        :return: True if the two color are equal, false otherwise.
        """
        try:
            return validate_color(other).as_tuple == self.as_tuple
        except TypeError:
            return False

    def __ne__(self, other: Any) -> bool:
        """Component-wise inequality of two colors.

        :param other: The other colors.
        :return: True if the two colors are not equal, false otherwise.
        """
        return not self == other

    def __hash__(self) -> int:
        """Hash code of the color.

        :return: The hash code of the color.
        """
        return hash(self.as_tuple)

    def __str__(self):
        """String representation of the color.
        """
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"


def validate_color(value: Color | ColorTuple) -> Color:
    """Validate that the given value is a color or can be converted to a color.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a color or cannot be converted to a color.
    """
    if isinstance(value, Color):
        return value
    elif (
        isinstance(value, tuple) and (
            (
                len(value) == 4
                and isinstance(value[0], int)
                and isinstance(value[1], int)
                and isinstance(value[2], int)
                and isinstance(value[3], int)
            )
            or (
                len(value) == 3
                and isinstance(value[0], int)
                and isinstance(value[1], int)
                and isinstance(value[2], int)
            )
        )
    ):
        return Color(*value)
    else:
        raise TypeError(f'Value must be Color or convertible to Color, got {type(value).__qualname__}.')
