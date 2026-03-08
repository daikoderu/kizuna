from pathlib import Path
from typing import TYPE_CHECKING

import pyglet

from kizuna.backends.base import Backend

if TYPE_CHECKING:
    from kizuna.core.assets import Asset, ImageAsset
    from kizuna.core.controllers import Controller
    from kizuna.management.settings import Settings
    from kizuna.rendering.batches import DrawBatch
    from kizuna.rendering.drawables import ImageDrawable


def _step(dt: float, controllers: list['Controller']):
    for controller in controllers:
        controller.on_step(dt)


def _draw(window: pyglet.window.Window, controllers: list['Controller']):
    window.clear()
    for controller in controllers:
        controller.on_draw()


class PygletBackend(Backend):
    batches: dict['DrawBatch', pyglet.graphics.Batch]
    assets: dict['Asset', pyglet.image.Texture | pyglet.image.TextureRegion]
    sprites: dict['ImageDrawable', pyglet.sprite.Sprite]

    def __init__(self, settings: 'Settings'):
        super().__init__(settings)
        self.batches = {}
        self.assets = {}
        self.sprites = {}

    def initialize(self, base_directory: Path):
        # Add the assets to the path.
        pyglet.resource.path = [str(base_directory / 'assets')]
        pyglet.resource.reindex()

    def launch_game_loop(self):
        window = pyglet.window.Window()
        window.size = tuple(self.settings.WINDOW_SIZE)
        window.set_caption(self.settings.WINDOW_CAPTION)

        # Instantiate the controllers.
        controllers = [controller_class() for controller_class in self.settings.CONTROLLERS]

        # Call the ``on_init`` method on each controller.
        for controller in controllers:
            controller.on_init()

        # Schedule update calls.
        pyglet.clock.schedule_interval(lambda dt: _step(dt, controllers), 1 / self.settings.STEPS_PER_SECOND)

        # Attach the draw event handler.
        @window.event
        def on_draw():
            _draw(window, controllers)

        # Run the app.
        pyglet.app.run(1 / self.settings.FRAMES_PER_SECOND)

    def load_image_asset(self, asset: 'ImageAsset'):
        pyglet_image = pyglet.resource.image(asset.path)
        pyglet_image.anchor_x, pyglet_image.anchor_y = (pyglet_image.width, pyglet_image.height) * asset.origin.value
        self.assets[asset] = pyglet_image

    def draw_batch(self, batch: 'DrawBatch'):
        self._get_or_create_batch(batch).draw()

    def prepare_draw_sprite(self, drawable: 'ImageDrawable', batch: 'DrawBatch'):
        sprite = self._get_or_create_sprite(drawable)
        sprite.batch = self._get_or_create_batch(batch)
        sprite.position = drawable.position.x, drawable.position.y, 0.0
        sprite.rotation = -drawable.rotation

    def _get_or_create_batch(self, batch: 'DrawBatch'):
        if batch not in self.batches:
            self.batches[batch] = pyglet.graphics.Batch()
        return self.batches[batch]

    def _get_or_create_image_asset(self, asset: 'ImageAsset'):
        if asset not in self.assets:
            pyglet_image = pyglet.resource.image(asset.path)
            pyglet_image.anchor_x = pyglet_image.width * asset.origin.value.x
            pyglet_image.anchor_y = pyglet_image.height * asset.origin.value.y
        return self.assets[asset]

    def _get_or_create_sprite(self, drawable: 'ImageDrawable'):
        if drawable not in self.sprites:
            self.sprites[drawable] = pyglet.sprite.Sprite(self._get_or_create_image_asset(drawable.asset))
        return self.sprites[drawable]
