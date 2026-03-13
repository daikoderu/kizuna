from kizuna.core.assets.paths import validate_asset_path, AssetPathLike


class Asset:
    """Any resource (e.g. images, audio, data) that is displayed to the user.

    Kizuna expects assets to be placed in an ``assets`` directory inside the project root directory. The ``Asset``
    class manages loading asset data into memory and unloading it when no longer needed. Use the :meth:`on_load`
    and :meth:`on_unload` methods to load and unload asset data.

    :ivar str path: Path of the asset.
    :ivar bool is_loaded: Whether the asset is loaded on memory.
    """

    def __init__(self, path: AssetPathLike):
        """Define a new asset.

        :param path: Path to the asset.
        """
        self.path = validate_asset_path(path)
        self.is_loaded = False

    def load(self):
        """Load the asset if it is not loaded yet.
        """
        if self.is_loaded:
            return
        self.on_load()
        self.is_loaded = True

    def unload(self):
        """Unload the asset if it is loaded.

        Make sure the asset is no longer being used before unloading.
        """
        if not self.is_loaded:
            return
        self.on_unload()
        self.is_loaded = False

    def on_load(self):
        """Implement this method to handle loading the asset into memory.
        """
        raise NotImplementedError()

    def on_unload(self):
        """Implement this method to handle unloading the asset from memory.
        """
        raise NotImplementedError()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}", loaded={self.is_loaded})'
