from pathlib import Path
from typing import TYPE_CHECKING, Callable

import pyglet

from kizuna.backends.base import Backend

if TYPE_CHECKING:
    from kizuna.core.assets import Asset, AssetPath, ImageAsset, FontAsset
    from kizuna.core.controllers import Controller
    from kizuna.config import Settings
    from kizuna.rendering.batches import DrawBatch
    from kizuna.rendering.drawables import TextDrawable, SpriteDrawable


PYGLET_CONSTANTS_TO_KIZUNA_KEYS = {
    pyglet.window.key.LEFT: 'left',
    pyglet.window.key.RIGHT: 'right',
    pyglet.window.key.UP: 'up',
    pyglet.window.key.DOWN: 'down',
}


def _resolve_path(path: 'AssetPath') -> str:
    return path.path[1:]


class PygletBackend(Backend):
    # Map from Kizuna assets to Pyglet resources.
    assets: dict['Asset', pyglet.image.Texture | pyglet.image.TextureRegion | pyglet.font.base.Font]

    # Maps from Kizuna batches to Pyglet batches.
    batches: dict['DrawBatch', pyglet.graphics.Batch]

    # Maps from Kizuna drawables to Pyglet drawables.
    texts: dict['TextDrawable', pyglet.text.Label]
    sprites: dict['SpriteDrawable', pyglet.sprite.Sprite]

    window: pyglet.window.Window
    standalone: bool

    # ---- KIZUNA LIFECYCLE METHODS ----

    def __init__(self, settings: 'Settings'):
        super().__init__(settings)
        self.assets = {}
        self.batches = {}
        self.sprites = {}
        self.texts = {}

    def initialize(self, base_directory: Path, standalone: bool):
        # Add the assets to the path.
        self.standalone = standalone
        if standalone:
            project_assets_path = base_directory / 'assets' / 'project'
        else:
            project_assets_path = base_directory / 'assets'
        pyglet.resource.path = [str(project_assets_path)]
        pyglet.resource.reindex()

    def launch_game_loop(
        self,
        step_fn: Callable[[float], None],
        draw_fn: Callable[[], None],
        controllers: list['Controller'],
    ):
        from kizuna.systems.input import InputController

        window = pyglet.window.Window()
        window.size = tuple(self.settings.WINDOW_SIZE)
        window.set_caption(self.settings.WINDOW_CAPTION)

        # Schedule update calls.
        pyglet.clock.schedule_interval(lambda dt: step_fn(dt), 1 / self.settings.STEPS_PER_SECOND)

        # Attach the draw event handler.
        @window.event
        def on_draw():
            window.clear()
            draw_fn()

        # Attach the input handlers.
        input_controller = next((ctr for ctr in controllers if isinstance(ctr, InputController)), None)
        if input_controller is not None:
            @window.event
            def on_key_press(symbol: int, modifiers: int):
                kizuna_key_value = PYGLET_CONSTANTS_TO_KIZUNA_KEYS.get(symbol)
                if kizuna_key_value is not None:
                    input_controller.held_keys[kizuna_key_value] = True

            @window.event
            def on_key_release(symbol: int, modifiers: int):
                kizuna_key_value = PYGLET_CONSTANTS_TO_KIZUNA_KEYS.get(symbol)
                if kizuna_key_value is not None:
                    input_controller.held_keys[kizuna_key_value] = False

        # Run the app.
        pyglet.app.run(1 / self.settings.FRAMES_PER_SECOND)

    # ---- ASSET LOADING METHODS ----

    def load_image_asset(self, asset: 'ImageAsset'):
        pyglet_image = pyglet.resource.image(_resolve_path(asset.path))
        pyglet_image.anchor_x, pyglet_image.anchor_y = (pyglet_image.width, pyglet_image.height) * asset.origin
        self.assets[asset] = pyglet_image

    def load_font_asset(self, asset: 'FontAsset'):
        pyglet.resource.add_font(_resolve_path(asset.path))
        self.assets[asset] = pyglet.font.load(name=asset.family_name, size=asset.size)

    # ---- PRE-DRAWING METHODS ----

    def prepare_draw_text(self, drawable: 'TextDrawable', batch: 'DrawBatch'):
        pyglet_font = self.assets[drawable.font]
        pyglet_label = self._get_or_create_text(drawable)
        pyglet_label.visible = drawable.visible
        if drawable.visible:
            pyglet_label.text = drawable.text
            pyglet_label.font_name = pyglet_font.name
            pyglet_label.font_size = drawable.font.size
            pyglet_label.position = drawable.position.x, drawable.position.y, 0.0
            pyglet_label.batch = self._get_or_create_batch(batch)

    def prepare_draw_sprite(self, drawable: 'SpriteDrawable', batch: 'DrawBatch'):
        pyglet_sprite = self._get_or_create_sprite(drawable)
        pyglet_sprite.visible = drawable.visible
        if drawable.visible:
            pyglet_sprite.batch = self._get_or_create_batch(batch)
            pyglet_sprite.position = drawable.position.x, drawable.position.y, 0.0
            pyglet_sprite.rotation = -drawable.rotation

    # ---- DRAWING METHODS ----

    def draw_batch(self, batch: 'DrawBatch'):
        self._get_or_create_batch(batch).draw()

    # ---- DRAWABLE DESTRUCTION METHODS ----

    def destroy_text(self, drawable: 'TextDrawable'):
        pyglet_label = self.texts.get(drawable)
        if pyglet_label is not None:
            pyglet_label.delete()

    def destroy_sprite(self, drawable: 'SpriteDrawable'):
        pyglet_sprite = self.sprites.get(drawable)
        if pyglet_sprite is not None:
            pyglet_sprite.delete()

    # ---- PRIVATE METHODS ----

    def _get_or_create_batch(self, batch: 'DrawBatch'):
        if batch not in self.batches:
            self.batches[batch] = pyglet.graphics.Batch()
        return self.batches[batch]

    def _get_or_create_sprite(self, drawable: 'SpriteDrawable'):
        if drawable not in self.sprites:
            self.sprites[drawable] = pyglet.sprite.Sprite(self.assets[drawable.asset])
        return self.sprites[drawable]

    def _get_or_create_text(self, drawable: 'TextDrawable'):
        if drawable not in self.texts:
            self.texts[drawable] = pyglet.text.Label()
        return self.texts[drawable]
