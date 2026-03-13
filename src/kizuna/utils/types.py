def fullname(type_object: type) -> str:
    """Get the full name of a type.

    :param type_object: The type whose full name will be returned.
    :return: The full name.
    """
    return type_object.__module__ + '.' + type_object.__qualname__
