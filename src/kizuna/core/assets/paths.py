import re

from kizuna.core.validation import validate_str
from kizuna.utils import fullname

ASSET_PATH_REGEX = re.compile(r'([a-z_-]+:)?(/[^<>:"`\'\\|?*]*)', flags=re.IGNORECASE)


type AssetPathLike = AssetPath | str
"""Alias for anything that may be converted to an :type:`AssetPath`.
"""


class AssetPath:
    """Encapsulation of asset paths that are resolved to files in the Kizuna Engine.

    Asset paths consist of the path itself and an optional namespace:

    *   Assets from your project: ``/path/to/file.extension`` or ``project:/path/to/file.extension``
    *   Kizuna's built-in assets: ``builtin:/path/to/file.extension``

    Directories are always separated by forward slashes. (``/``), and the path always starts with a forward slash,
    in all platforms. The following characters are disallowed: ``^ < > : ` " ' \\ | ? *``
    """
    __slots__ = ('_namespace', '_path')

    def __init__(self, path: str):
        """Create an asset path from a path string.

        :param path: The path as a string.
        """
        path = validate_str(path)
        match = ASSET_PATH_REGEX.fullmatch(path)
        if match is None:
            raise ValueError(f'Invalid asset path: "{path}".')
        namespace, self._path = match.group(1, 2)
        if namespace is not None:
            self._namespace = namespace[:-1]
        else:
            self._namespace = 'project'
        if self._namespace not in ('project', 'builtin'):
            raise ValueError('Only the "project" and "builtin" namespaces are allowed.')

    @property
    def namespace(self) -> str:
        """Get the namespace of the asset path.
        """
        return self._namespace

    @property
    def path(self) -> str:
        """The absolute path inside the namespace.
        """
        return self._path

    def __str__(self) -> str:
        return f'{self.namespace}:{self.path}'

    def __repr__(self) -> str:
        return f'AssetPath("{self.namespace}:{self.path}")'


def validate_asset_path(value: AssetPathLike) -> AssetPath:
    """Validate that the given value is or can be converted to an :type:`AssetPath`.

    :param value: The value to validate.
    :return: The validated value.
    :raise TypeError: If the given value cannot be converted to an :type:`AssetPath`.
    :raise ValueError: If the given value is an invalid string.
    """
    if isinstance(value, AssetPath):
        return value
    elif isinstance(value, str):
        return AssetPath(value)
    else:
        raise TypeError(f'Value must be AssetPath or convertible to AssetPath, got {fullname(type(value))}.')
