from typing import Any

from kizuna.core.validation import validate_int, clamp_int

type ColorLike = Color | tuple[int, int, int, int] | tuple[int, int, int] | list[int]
"""Alias for a tuple or list that represents a color.
"""


class Color:
    """Tuples of four integers between 0 and 255 to define colors in ``(r, g, b, a)`` format.

    For the sake of brevity and consistency, any function parameter or attribute expected to be of type Color can
    also be set to a tuple or list of four integers. It will be converted to an instance of this class
    (see :type:`ColorLike`).

    Out-of-bounds values are automatically clamped. If the class is called with three values, these correspond to
    red, green, and blue, respectively, and the alpha (opacity) is set to 255 (fully opaque).
    """
    __slots__ = ('_r', '_g', '_b', '_a')

    def __init__(self, r: int, g: int, b: int, a: int = 255):
        """Construct a :type:`Color` instance from its RGBA components.

        :param r: The red component of the color.
        :param g: The green component of the color.
        :param b: The blue component of the color.
        :param a: The alpha component of the color.
        """
        self._r = clamp_int(validate_int(r), 0, 255)
        self._g = clamp_int(validate_int(g), 0, 255)
        self._b = clamp_int(validate_int(b), 0, 255)
        self._a = clamp_int(validate_int(a), 0, 255)

    @property
    def r(self) -> int:
        """Return the red component of the color.
        """
        return self._r

    @property
    def g(self) -> int:
        """Return the green component of the vector.
        """
        return self._g

    @property
    def b(self) -> int:
        """Return the blue component of the color.
        """
        return self._b

    @property
    def a(self) -> int:
        """Return the alpha component of the vector.
        """
        return self._a

    def __iter__(self):
        """Iterator over the color components.

        This allows easy destructuring.
        """
        return iter((self.r, self.g, self.b, self.a))

    def __eq__(self, other: Any) -> bool:
        """Component-wise equality of two colors.

        :param other: The other color.
        :return: True if the two color are equal, false otherwise.
        """
        try:
            return tuple(validate_color(other)) == tuple(self)
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
        return hash(tuple(self))

    def __str__(self):
        """String representation of the color.

        :return: The string representation of the color.
        """
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"


def validate_color(value: ColorLike) -> Color:
    """Validate that the given value is a color or can be converted to a color.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a color or cannot be converted to a color.
    """
    if isinstance(value, Color):
        return value
    elif (
        isinstance(value, tuple | list) and (
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
