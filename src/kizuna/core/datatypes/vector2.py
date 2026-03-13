import math
from typing import Self, Iterator, Any, TYPE_CHECKING

from kizuna.core.validation import validate_float
from kizuna.utils import fullname

if TYPE_CHECKING:
    from kizuna.core.datatypes import IVector2


type Vector2Like = Vector2 | tuple[int | float, int | float] | list[int | float]
"""Alias for a tuple or list that represents a floating-point 2D vector.

Objects that match this type may be passed as function parameters or attributes where a :type:`Vector2` is expected,
and are automatically converted.
"""


class Vector2:
    """Tuples of two floats for coordinates ``(x, y)`` and displacements in a 2D space.

    For the sake of brevity and consistency, any function parameter or attribute expected to be of type
    :type:`Vector2` can also be set to a tuple or list of two integers and/or floats. It will be converted to an
    instance of this class (see :type:`Vector2Like`).

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

        :type:`Vector2` and :type:`~kizuna.core.datatypes.ivector2.IVector2` instances cannot be operated together.
        Use the :meth:`ivector2_to_vector` method to convert an IVector2 to a Vector2.
    """
    __slots__ = ('_x', '_y')

    def __init__(self, x: float, y: float):
        self._x = validate_float(x)
        self._y = validate_float(y)

    @staticmethod
    def lendir(length: float, direction: float) -> 'Vector2':
        """Create a :type:`Vector2` with the given :meth:`length` and :meth:`direction`.

        :param length: The length of the vector.
        :param direction: The direction of the vector, with respect to the positive side of the X-axis,
            counterclockwise in degrees.
        :return: A new vector with the result.
        """
        direction_rad = direction * math.pi / 180
        return length * Vector2(math.cos(direction_rad), math.sin(direction_rad))

    @property
    def x(self) -> float:
        """Return the *x*-component of the vector.

        Negative *x* is to the left, positive *x* to the right.
        """
        return self._x

    @property
    def y(self) -> float:
        """Return the *y*-component of the vector.

        Negative *y* is downwards, positive *y* is upwards.
        """
        return self._y

    @property
    def length(self) -> float:
        """Return the length of the vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def length_squared(self) -> float:
        """Return the length of the vector squared.

        If the length itself is not required (e.g. when comparing distances), this method is more efficient since it
        does not need to compute the square root.
        """
        return self.x ** 2 + self.y ** 2

    @property
    def direction(self) -> float:
        """Get the angle of the vector with respect to the positive side of the X-axis, counterclockwise in degrees.

        For the zero vector, this returns 0.0.
        """
        return math.atan2(self.y, self.x) * 180 / math.pi

    def __add__(self, other: Vector2Like) -> Self:
        """Component-wise addition of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a Vector2D and cannot be converted to a Vector2D.
        """
        other = validate_vector2(other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Vector2Like) -> Self:
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

    def __sub__(self, other: Vector2Like) -> Self:
        """Component-wise subtraction of two vectors.

        :param other: The other vector.
        :return: A new vector with the result.
        :raise TypeError: If ``other`` is not a Vector2D and cannot be converted to a Vector2D.
        """
        other = validate_vector2(other)
        return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: Vector2Like) -> Self:
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

    def __mul__(self, other: Vector2Like | int | float) -> Self:
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

    def __rmul__(self, other: Vector2Like | int | float) -> Self:
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

    def __truediv__(self, other: Vector2Like | int | float) -> Self:
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

    def __rtruediv__(self, other: Vector2Like | int | float) -> Self:
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
        return hash(tuple(self))

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Vector2({self.x}, {self.y})'


def validate_vector2(value: Vector2Like) -> Vector2:
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
        raise TypeError(f'Value must be Vector2 or convertible to Vector2, got {fullname(type(value))}.')


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
            f'Value must be int, float, Vector2 or convertible to Vector2, got {fullname(type(value))}.'
        )


def ivector2_to_vector(value: 'IVector2') -> Vector2:
    """Convert a IVector2 to a Vector2.

    :param value: The value to convert.
    :return: The converted value.
    """
    return Vector2(value.x, value.y)
