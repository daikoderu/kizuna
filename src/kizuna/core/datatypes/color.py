from dataclasses import dataclass

from kizuna.core.validation import validate_int, clamp_int


@dataclass
class Color:
    """Tuples of two integers between 0 and 255 to define colors in RGBA format.
    """
    r: int
    g: int
    b: int
    a: int = 255

    @property
    def as_tuple(self) -> tuple[int, int, int, int]:
        """Return the color as a normal tuple.
        """
        return self.r, self.g, self.b, self.a

    def __post_init__(self):
        """Validate color components
        """
        self.r = clamp_int(validate_int(self.r), 0, 255)
        self.g = clamp_int(validate_int(self.g), 0, 255)
        self.b = clamp_int(validate_int(self.b), 0, 255)
        self.a = clamp_int(validate_int(self.a), 0, 255)

    def __str__(self):
        """String representation of the vector.
        """
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"

    def __iter__(self):
        """Iterator over the color components.
        """
        return iter(self.as_tuple)


def validate_color(value: Color | tuple[int, int, int] | tuple[int, int, int, int]) -> Color:
    """Validate that the given value is a color or can be converted to a color.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a color or cannot be converted to a color.
    """
    if (
        isinstance(value, tuple)
        and (
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
    if not isinstance(value, Color):
        raise TypeError(f'Value must be Color or convertible to Color, got {type(value).__qualname__}.')
    return value
