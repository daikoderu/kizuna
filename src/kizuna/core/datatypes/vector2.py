from dataclasses import dataclass
from typing import Self, Iterator, Any

from kizuna.core.validation import validate_float

type Vector2Like = tuple[int | float, int | float] | list[int | float]
"""Alias for a tuple or list that represents a floating-point float 2D vector.
"""


@dataclass
class Vector2:
    """Tuples of two floats for coordinates ``(x, y)`` and displacements in a 2D space.

    For the sake of brevity and consistency, any function parameter or attribute expected to be of type Vector2 can
    also be set to a tuple or list of two integers and/or floats. It will be converted to an instance of this class.

    Multiplication and division with the ``*`` and ``/`` operators is component-wise or by a scalar (int or float).
    """
    x: float
    y: float

    def __post_init__(self):
        """Validate color components.
        """
        self.x = validate_float(self.x)
        self.y = validate_float(self.y)

    def __add__(self, other: Self | Vector2Like) -> Self:
        """Component-wise addition of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a float 2D vector and cannot be converted to a float 2D vector.
        """
        other = validate_vector2(other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Self | Vector2Like) -> Self:
        """Component-wise addition of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a float 2D vector and cannot be converted to a float 2D vector.
        """
        other = validate_vector2(other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self | Vector2Like) -> Self:
        """Component-wise subtraction of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a float 2D vector and cannot be converted to a float 2D vector.
        """
        other = validate_vector2(other)
        return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: Self | Vector2Like) -> Self:
        """Component-wise subtraction of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a float 2D vector and cannot be converted to a float 2D vector.
        """
        other = validate_vector2(other)
        return Vector2(other.x - self.x, other.y - self.y)

    def __neg__(self) -> Self:
        """Get the opposite of the vector.
        
        :return: A new vector with the signs changed component-wise.
        """
        return Vector2(-self.x, -self.y)

    def __mul__(self, other: Self | Vector2Like | int | float) -> Self:
        """Component-wise multiplication of two vectors or multiplication of a vector by a scalar.

        :param other: The other vector or scalar.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a scalar, a float 2D vector, and cannot be converted to a float 2D
            vector.
        """
        other = validate_vector2_or_scalar(other)
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other: Self | Vector2Like | int | float) -> Self:
        """Component-wise multiplication of two vectors or multiplication of a scalar by a vector.

        :param other: The other vector or scalar.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a scalar, a float 2D vector, and cannot be converted to a float 2D
            vector.
        """
        other = validate_vector2_or_scalar(other)
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: Self | Vector2Like | int | float) -> Self:
        """Component-wise division of two vectors or division of a vector by a scalar.

        :param other: The other vector or scalar.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a scalar, a float 2D vector, and cannot be converted to a float 2D
            vector.
        """
        other = validate_vector2_or_scalar(other)
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __rtruediv__(self, other: Self | Vector2Like | int | float) -> Self:
        """Component-wise division of two vectors or division of a scalar by a vector.

        :param other: The other vector or scalar.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a scalar, a float 2D vector, and cannot be converted to a float 2D
            vector.
        """
        other = validate_vector2_or_scalar(other)
        if isinstance(other, Vector2):
            return Vector2(other.x / self.x, other.y / self.y)
        else:
            return Vector2(other / self.x, other / self.y)

    def __iter__(self) -> Iterator[float]:
        """Iterator over the vector components.

        This allows easy destructuring.
        """
        return iter((self.x, self.y))

    def __eq__(self, other: Any) -> bool:
        """Component-wise equality of two vectors.

        :param other: The other vector.
        :return: True if the two vectors are equal, false otherwise.
        """
        try:
            return tuple(validate_vector2(other)) == tuple(self)
        except TypeError:
            return False

    def __ne__(self, other: Any) -> bool:
        """Component-wise inequality of two vectors.

        :param other: The other vector.
        :return: True if the two vectors are not equal, false otherwise.
        """
        return not self == other

    def __hash__(self) -> int:
        """Hash code of the vector.

        :return: The hash code of the vector.
        """
        return hash(tuple(self))

    def __str__(self) -> str:
        """String representation of the vector.

        :return: The string representation of the color.
        """
        return f"({self.x}, {self.y})"


def validate_vector2(value: Vector2 | Vector2Like) -> Vector2:
    """Validate that the given value is a float 2D vector or can be converted to a float 2D vector.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a float 2D vector and cannot be converted to a float 2D vector.
    """
    if isinstance(value, Vector2):
        return value
    elif (
        isinstance(value, tuple | list) and len(value) == 2
        and isinstance(value[0], int | float)
        and isinstance(value[1], int | float)
    ):
        return Vector2(*value)
    else:
        raise TypeError(f'Value must be Vector2 or convertible to Vector2, got {type(value).__qualname__}.')


def validate_vector2_or_scalar(value: Vector2 | Vector2Like | int | float) -> Vector2 | int | float:
    """Validate that the given value is a float 2D vector, can be converted to a float 2D vector, or is a scalar.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a float 2D vector and cannot be converted to a float 2D vector.
    """
    if isinstance(value, int | float | Vector2):
        return value
    elif (
        isinstance(value, tuple | list) and len(value) == 2
        and isinstance(value[0], int | float)
        and isinstance(value[1], int | float)
    ):
        return Vector2(*value)
    else:
        raise TypeError(
            f'Value must be int, float, Vector2 or convertible to Vector2, got {type(value).__qualname__}.'
        )
