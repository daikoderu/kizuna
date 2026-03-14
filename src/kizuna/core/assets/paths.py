import re

from kizuna.core.validation import validate_str
from kizuna.utils import fullname

ASSET_PATH_REGEX = re.compile(r'([a-z_-]+:)?(/[^<>:"`\'\\|?*]*)', flags=re.IGNORECASE)


type AssetPathLike = AssetPath | str
"""Alias for anything that may be converted to an asset path.
"""


class AssetPath:
    """Encapsulation of asset paths.

    Asset paths consist of the path itself and an optional namespace:

    *   Assets from your project: ``/path/to/file.extension`` or ``project:/path/to/file.extension``
    *   Kizuna's built-in assets: ``builtin:/path/to/file.extension``

    Directories are always separated by forward slashes. (``/``), and the path always starts with a forward slash,
    in all platforms. The following characters are disallowed: ``^ < > : ` " ' \\ | ? *``

    :ivar namespace: The namespace of the asset path.
    :ivar path: The absolute path inside the namespace.
    """
    namespace: str
    path: str

    __slots__ = ('namespace', 'path')

    def __init__(self, path: str):
        """Create an asset path from a path string.

        :param path: The path as a string.
        """
        path = validate_str(path)
        match = ASSET_PATH_REGEX.fullmatch(path)
        if match is None:
            raise ValueError(f'Invalid asset path: "{path}".')
        namespace, self.path = match.group(1, 2)
        if namespace is not None:
            self.namespace = namespace[:-1]
        else:
            self.namespace = 'project'
        if self.namespace not in ('project', 'builtin'):
            raise ValueError('Only the "project" and "builtin" namespaces are allowed.')


def validate_asset_path(value: AssetPathLike) -> AssetPath:
    """Validate that the given value is an asset path or can be converted to an asset path.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value is not an asset path or cannot be converted to an asset path.
    :raise ValueError: If the given value is an invalid string.
    """
    if isinstance(value, AssetPath):
        return value
    elif isinstance(value, str):
        return AssetPath(value)
    else:
        raise TypeError(f'Value must be AssetPath or convertible to AssetPath, got {fullname(type(value))}.')
