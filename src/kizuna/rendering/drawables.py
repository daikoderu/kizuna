import pyglet.text

from kizuna.core.datatypes import Vector2, Color


class Drawable:
    """Base class for anything that will be rendered on screen.
    """

    def on_draw(self):
        raise NotImplementedError()


class Text(Drawable):
    text: str
    position: Vector2
    color: Color

    def __init__(
        self,
        text: str,
        position: Vector2,
        color: Color,
    ):
        self.text = text
        self.position = position
        self.color = color
        self._pyglet_text = None

    def on_draw(self):
        self._update_element()
        self._pyglet_text.draw()

    def _update_element(self):
        if self._pyglet_text is None:
            self._pyglet_text = pyglet.text.Label()
        self._pyglet_text.text = self.text
        self._pyglet_text.x, self._pyglet_text.y = self.position
        self._pyglet_text.color = self.color.as_tuple


class Image(Drawable):

    def __init__(
        self,
        assets_path: str,
    ):
        self._pyglet_image = pyglet.resource.image(assets_path)

    def on_draw(self):
        self._pyglet_image.blit(0, 0)
