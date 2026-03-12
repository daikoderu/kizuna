"""Compilation of various validation functions used throughout the entire framework.

All validations raise either :class:`ValueError` or :class:`TypeError`.
"""

import re
from importlib import import_module
from types import UnionType
from typing import Any, Callable


# ---- TYPE VALIDATORS ----

def validate_type(value: Any, expected_type: type | UnionType) -> Any:
    """Validate that the given value is a valid type.

    :param value: The value to validate.
    :param expected_type: The expected type of the value.
    :return: The validated value.
    :raise TypeError: If the value is not a valid type.
    """
    if not isinstance(value, expected_type):
        if isinstance(expected_type, UnionType):
            type_options = [t.__qualname__ for t in expected_type.__args__]
            if len(type_options) == 2:
                type_options_str = f'{type_options[0]} or {type_options[1]}'
            else:
                options_except_last = ', '.join(type_options[:-1])
                type_options_str = f'{options_except_last}, or {type_options[-1]}'
        else:
            type_options_str = expected_type.__qualname__
        raise TypeError(f'Value must be {type_options_str}, got {type(value).__qualname__}.')
    return value


# ---- INTEGER VALIDATORS ----

def validate_int(value: int) -> int:
    """Validate that the given value is an integer.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value is not an integer.
    """
    return validate_type(value, int)


def clamp_int(value: int, min_value: int, max_value: int) -> int:
    """Clamp the given value to an integer.

    :param value: The value to clamp.
    :param min_value: The minimum value to clamp to.
    :param max_value: The maximum value to clamp to.
    """
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value


def validate_float(value: int | float) -> float:
    """Validate that the given value is a float or can be converted to a float.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value cannot be converted to a float.
    """
    if not isinstance(value, int | float):
        raise TypeError(f'Value must be int or float, got {type(value).__qualname__}.')
    return float(value)

def validate_positive_float(value: int | float) -> float:
    """Validate that the given value is a positive floating-point number.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value cannot be converted to a float.
    :raise TypeError: If the value is not positive.
    """
    value = validate_float(value)
    if value <= 0:
        raise ValueError(f'Value must be positive.')
    return value


# ---- STRING VALIDATORS ----

IDENTIFIER_REGEX = re.compile(r'[a-z][a-z0-9_]*', flags=re.IGNORECASE)


def validate_str(value: str) -> str:
    """Validate that the given value is a string.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value is not a string.
    """
    return validate_type(value, str)


def validate_identifier(value: str) -> str:
    """Validate that the given value is a valid identifier.

    Identifiers follow the format: (1 ASCII letter) + (0 or more ASCII letters, digits and/or underscores).

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value is not a string.
    :raise ValueError: If the value is not a valid identifier.
    """
    value = validate_str(value)
    if re.fullmatch(IDENTIFIER_REGEX, value) is None:
        raise ValueError(
            f'"{value}" is not a valid identifier. Identifiers must follow the format: '
            f'(1 ASCII letter) + (0 or more ASCII letters, digits and/or underscores)'
        )
    return value


def validate_and_import_module_path(value: str) -> Any:
    """Validate that the given value is an existing module path and import it.

    A module path is a series of at least two identifiers separated by dots. The last element corresponds to the
    element that will be imported.

    :param value: The value to validate.
    :return: The imported object.
    :raise TypeError: If the value is not a string.
    :raise ValueError: If the value is not a valid module path.
    """
    value = validate_str(value)
    try:
        module_path, element = value.rsplit('.', 1)
    except ValueError as e:
        raise ValueError(f'"{value}" does not look like a module path.') from e

    try:
        module = import_module(module_path)
    except ImportError as e:
        raise ValueError(f'Could not import "{module_path}": {e}') from e

    try:
        return getattr(module, element)
    except AttributeError as e:
        raise ValueError(f'Module "{module_path}" does not define "{element}".') from e


# ---- COLLECTION VALIDATORS ----

def validate_set(value: set, element_validation: Callable[[Any], Any] | None = None) -> set:
    """Validate that the given value is a set.

    Optionally, another validation function can be passed to apply it to each element of the set.

    :param value: The value to validate.
    :param element_validation: The function that validates the elements of the input set.
    :return: The validated value.
    :raise TypeError: If the value is not a set, or if one of the elements does not satisfy validation.
    :raise ValueError: If one of the elements does not satisfy validation.
    """
    value = validate_type(value, set)

    # Validate each element.
    if element_validation is not None:
        validated = set()
        for element in value:
            try:
                validated.add(element_validation(element))
            except TypeError as e:
                raise TypeError(f'Invalid element "{repr(element)}": {e}') from e
            except ValueError as e:
                raise ValueError(f'Invalid element "{repr(element)}": {e}') from e
        return validated

    return value

def validate_list(value: list, distinct: bool = False, child: Callable[[Any], Any] | None = None) -> list:
    """Validate that the given value is a list.

    Optionally, another validation function can be passed to apply it to each element of the set.

    :param value: The value to validate.
    :param distinct: If True, the elements of the input list must be distinct from each other. This constraint
        requires the elements to be hashable.
    :param child: The function that validates the elements of the input list.
    :return: The validated value.
    :raise TypeError: If the value is not a list, or if one of the elements does not satisfy validation.
    :raise ValueError: If ``distinct`` is true and the list contains duplicates, or if one of the elements does not
        satisfy validation.
    """
    value = validate_type(value, list)

    # Check for duplicates.
    if distinct and len(value) >= 2:
        sorted_list = sorted(value, key=hash)
        for i in range(len(value) - 1):
            if sorted_list[i] == sorted_list[i + 1]:
                raise ValueError(f'List cannot contain duplicate elements.')

    # Validate each element.
    if child is not None:
        validated = []
        for element in value:
            try:
                validated.append(child(element))
            except TypeError as e:
                raise TypeError(f'Invalid element "{repr(element)}": {e}') from e
            except ValueError as e:
                raise ValueError(f'Invalid element "{repr(element)}": {e}') from e
        return validated

    return value

def validate_dict(value: dict) -> dict:
    """Validate that the given value is a dictionary.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value is not a dictionary."""
    return validate_type(value, dict)
