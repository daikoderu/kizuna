from dataclasses import dataclass
from typing import Self, Iterator


@dataclass
class Vector2:
    """Tuples of two float for coordinates and displacements in a 2D space.
    """
    x: float
    y: float

    @property
    def as_tuple(self) -> tuple[float, float]:
        """Return the vector as a normal tuple.
        """
        return self.x, self.y

    def __add__(self, other: Self) -> Self:
        """Component-wise addition of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        """Component-wise subtraction of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Self | int | float) -> Self:
        """Component-wise multiplication of two vectors or multiplication of a scalar by a vector.

        :param other: The other vector or scalar.
        :return: A new vector with the result.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other: Self | int | float) -> Self:
        """Component-wise multiplication of two vectors or multiplication of a vector by a scalar.

        :param other: The other vector or scalar.
        :return: A new vector with the result.
        """
        self.__mul__(other)

    def __div__(self, other: Self | int | float) -> Self:
        """Component-wise division of two vectors or division of a vector by a scalar.

        :param other: The other vector or scalar.
        :return: A new vector with the result.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __str__(self) -> str:
        """String representation of the vector.
        """
        return f"({self.x}, {self.y})"

    def __iter__(self) -> Iterator[float]:
        """Iterator over the vector components.
        """
        return iter(self.as_tuple)


def validate_vector2(value: Vector2) -> Vector2:
    """Validate that the given value is a 2D vector or can be converted to a 2D vector.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a color or cannot be converted to a color.
    """
    if (
        isinstance(value, tuple)
        and len(value) == 2
        and isinstance(value[0], int | float)
        and isinstance(value[1], int | float)
    ):
        return Vector2(*value)
    if not isinstance(value, Vector2):
        raise TypeError(f'Value must be Vector2 or convertible to Vector2, got {type(value).__qualname__}.')
    return value