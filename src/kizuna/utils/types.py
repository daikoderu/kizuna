from typing import Any


def fullname(obj: Any) -> str:
    """Get the full name of an object.

    :param obj: The object whose full name will be returned.
    :return: The full name.
    """
    return obj.__module__ + '.' + obj.__qualname__
