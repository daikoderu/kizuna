class Asset:

    def __init__(self, path: str):
        self.path = path

    def on_load(self) -> None:
        raise NotImplementedError()
