from dataclasses import dataclass
from typing import Self, Iterator, Any, TYPE_CHECKING

from kizuna.core.validation import validate_float

if TYPE_CHECKING:
    from kizuna.core.datatypes import IVector2


type Vector2Like = tuple[int | float, int | float] | list[int | float]
"""Alias for a tuple or list that represents a floating-point 2D vector.

Objects that match this type may be passed as function parameters or attributes where a :py:type:`Vector2` is expected,
and are automatically converted.
"""


@dataclass
class Vector2:
    """Tuples of two floats for coordinates ``(x, y)`` and displacements in a 2D space.

    For the sake of brevity and consistency, any function parameter or attribute expected to be of type
    :py:type:`Vector2` can also be set to a tuple or list of two integers and/or floats. It will be converted to an
    instance of this class (see :py:type:`Vector2Like`).

    Let ``u`` and ``v`` be Vector2 instances and ``k`` a scalar (int or float). The following operators are supported:

    ======================== ================================= ======================================
    Operation                Result                            Description
    ======================== ================================= ======================================
    ``u + v``                ``Vector2(u.x + v.x, u.y + v.y)`` Component-wise addition
    ``u - v``                ``Vector2(u.x - v.x, u.y - v.y)`` Component-wise subtraction
    ``+v``                   ``v``                             Unary plus (identity)
    ``-v``                   ``Vector2(-v.x, -v.y)``           Unary minus (opposite vector)
    ``k * v`` or ``v * k``   ``Vector2(k * v.x, k * v.y)``     Multiplication by a scalar
    ``u * v``                ``Vector2(u.x * v.x, u.y * v.y)`` Component-wise multiplication
    ``k / v``                ``Vector2(k / v.x, k / v.y)``     Float division of a scalar by a vector
    ``v / k``                ``Vector2(v.x / k, v.y / k)``     Float division of a vector by a scalar
    ``u / v``                ``Vector2(u.x / v.x, u.y / v.y)`` Component-wise float division
    ``tuple(v)``             ``(v.x, v.y)``                    Convert to tuple
    ``u == v``               ``tuple(u) == tuple(v)``          Equality test
    ``u != v``               ``tuple(u) != tuple(v)``          Inequality test
    ======================== ================================= ======================================

    Additionally, vectors are hashable and support iteration over their two components. This allows easy destructuring:

    ..  code-block::

        x, y = Vector2(3, 1)

    ..  important::

        :py:type:`IVector2` and :py:type:`Vector2` instances cannot be operated together. Use the
        :py:meth:`ivector2_to_vector` method to convert an IVector2 to a Vector2.
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
        :raise TypeError: If ``other`` is not a Vector2D and cannot be converted to a Vector2D.
        """
        other = validate_vector2(other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Self | Vector2Like) -> Self:
        """Component-wise addition of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a Vector2D and cannot be converted to a Vector2D.
        """
        other = validate_vector2(other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __pos__(self) -> Self:
        """Apply the unary plus operator to the vector.

        :return: The same vector.
        """
        return self

    def __sub__(self, other: Self | Vector2Like) -> Self:
        """Component-wise subtraction of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a Vector2D and cannot be converted to a Vector2D.
        """
        other = validate_vector2(other)
        return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: Self | Vector2Like) -> Self:
        """Component-wise subtraction of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a Vector2D and cannot be converted to a Vector2D.
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
        :raise TypeError: If ``other`` is not a scalar, a Vector2D, and cannot be converted to such.
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
        :raise TypeError: If ``other`` is not a scalar, a Vector2D, and cannot be converted to such.
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
        :raise TypeError: If ``other`` is not a scalar, a Vector2D, and cannot be converted to such.
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
        :raise TypeError: If ``other`` is not a scalar, a Vector2D, and cannot be converted to such.
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
    """Validate that the given value is a Vector2D or can be converted to a Vector2D.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a Vector2D and cannot be converted to such.
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
    """Validate that the given value is a Vector2D, can be converted to a Vector2D, or is a scalar.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not a Vector2D and cannot be converted to such.
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


def ivector2_to_vector(value: 'IVector2') -> Vector2:
    """Convert a IVector2 to a Vector2.

    :param value: The value to convert.
    :return: The converted value.
    """
    return Vector2(value.x, value.y)
