import pyglet


class DrawBatch:
    _next_id: int = 0

    def __init__(self, priority: int = 0, name: str | None = None):
        self.name = name if name is not None else f'batch-{DrawBatch._next_id}'
        self.priority = priority
        self._pyglet_instance = None
        DrawBatch._next_id += 1

    @property
    def _pyglet(self):
        if self._pyglet_instance is None:
            self._pyglet_instance = pyglet.graphics.Batch()
        return self._pyglet_instance

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'DrawBatch("{self.name}", priority={self.priority})'

    def __hash__(self):
        return hash(self.name)

    def draw(self):
        self._pyglet.draw()
