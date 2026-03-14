from kizuna.core.assets.paths import validate_asset_path, AssetPathLike, AssetPath


class Asset:
    """Any resource of a game that is stored in files (e.g. images, audio).

    Kizuna expects the files to be placed in an ``assets`` directory inside the project root directory. Then, you
    can reference those files using platform-independent asset paths :type:`kizuna.core.assets.paths.AssetPathLike`.

    You can subclass ``Asset`` to define your own ``Asset`` types, which may be specific to your game (e.g. levels,
    item databases). Use the :meth:`on_load` and :meth:`on_unload` methods to implement how this is done.
    """

    def __init__(self, path: AssetPathLike, eager: bool = False):
        """Define a new asset.

        :param path: Path to the asset.
        :param eager: Whether this asset should be loaded immediately upon definition (``True``) or only until
            required by Kizuna (``False``).
        """
        self._path = validate_asset_path(path)
        self._is_loaded = False
        if eager:
            self.load()

    @property
    def path(self) -> AssetPath:
        """Get the path where the asset is stored.
        """
        return self._path

    @property
    def is_loaded(self) -> bool:
        """Get whether this asset is stored in memory.
        """
        return self._is_loaded

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}", loaded={self.is_loaded})'

    def load(self):
        """Load the asset if it is not loaded yet.
        """
        if self.is_loaded:
            return
        self.on_load()
        self._is_loaded = True

    def unload(self):
        """Unload the asset if it is loaded.

        Make sure the asset is no longer being used before unloading.
        """
        if not self.is_loaded:
            return
        self.on_unload()
        self._is_loaded = False

    def on_load(self):
        """Implement this method to handle loading the asset into memory.
        """
        raise NotImplementedError()

    def on_unload(self):
        """Implement this method to handle unloading the asset from memory.
        """
        raise NotImplementedError()
