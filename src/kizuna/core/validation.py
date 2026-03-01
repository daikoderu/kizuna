"""Compilation of various validation functions used throughout the entire framework.
"""

import re
from importlib import import_module
from typing import Any


# ---- TYPE VALIDATORS ----

def validate_type(value: Any, expected_type: type) -> Any:
    """Validate that the given value is a valid type.

    :param value: The value to validate.
    :param expected_type: The expected type of the value.
    :return: The validated value.
    :raise TypeError: If the value is not a valid type.
    """
    if not isinstance(value, expected_type):
        raise TypeError(f'Value must be {expected_type.__qualname__}, got {type(value).__qualname__}.')
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
    """Validate that the given value can be converted to a float.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value cannot be converted to a float.
    """
    if not isinstance(value, int | float):
        raise TypeError(f'Value must be int or float, got {type(value).__qualname__}.')
    return float(value)


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
        return getattr(module, element)
    except ImportError as e:
        raise ValueError(f'Could not import "{value}".') from e
    except AttributeError as e:
        raise ValueError(f'Module "{module_path}" does not define "{element}".') from e

    return module


# ---- COLLECTION VALIDATORS ----

def validate_dict(value: dict) -> dict:
    """Validate that the given value is a dictionary.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the value is not a dictionary."""
    return validate_type(value, dict)
