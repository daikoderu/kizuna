from pathlib import Path
from typing import TYPE_CHECKING, Callable

from kizuna.core.controllers import Controller

if TYPE_CHECKING:
    from kizuna.core.assets import ImageAsset, FontAsset
    from kizuna.config import Settings
    from kizuna.rendering import DrawBatch, TextDrawable, SpriteDrawable


class Backend:

    # ---- KIZUNA LIFECYCLE METHODS ----

    def __init__(self, settings: 'Settings'):
        self.settings = settings

    def initialize(self, base_directory: Path, standalone: bool):
        raise NotImplementedError()

    def launch_game_loop(
        self,
        step_fn: Callable[[float], None],
        draw_fn: Callable[[], None],
        controllers: list[Controller],
    ):
        raise NotImplementedError()

    # ---- ASSET LOADING METHODS ----

    def load_image_asset(self, asset: 'ImageAsset'):
        raise NotImplementedError()

    def load_font_asset(self, asset: 'FontAsset'):
        raise NotImplementedError()

    # ---- PRE-DRAWING METHODS ----

    def prepare_draw_text(self, drawable: 'TextDrawable', batch: 'DrawBatch'):
        raise NotImplementedError()

    def prepare_draw_sprite(self, drawable: 'SpriteDrawable', batch: 'DrawBatch'):
        raise NotImplementedError()

    # ---- DRAWING METHODS ----

    def draw_batch(self, batch: 'DrawBatch'):
        raise NotImplementedError()

    # ---- DRAWABLE DESTRUCTION METHODS ----

    def destroy_text(self, drawable: 'TextDrawable'):
        raise NotImplementedError()

    def destroy_sprite(self, drawable: 'SpriteDrawable'):
        raise NotImplementedError()
