from typing import Any


class Asset:

    def __init__(self, path: str):
        self.path = path
        self._resource = self.on_load()

    def on_load(self) -> Any:
        raise NotImplementedError()
