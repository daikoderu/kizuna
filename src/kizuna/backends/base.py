from pathlib import Path
from typing import TYPE_CHECKING, Callable

from kizuna.core.controllers import Controller

if TYPE_CHECKING:
    from kizuna.core.assets import ImageAsset, FontAsset
    from kizuna.config import Settings
    from kizuna.rendering.batches import DrawBatch
    from kizuna.rendering.drawables import SpriteDrawable


class Backend:

    def __init__(self, settings: 'Settings'):
        self.settings = settings

    def initialize(self, base_directory: Path):
        raise NotImplementedError()

    def launch_game_loop(
        self,
        step_fn: Callable[[float], None],
        draw_fn: Callable[[], None],
        controllers: list[Controller],
    ):
        raise NotImplementedError()

    def load_image_asset(self, asset: 'ImageAsset'):
        raise NotImplementedError()

    def load_font_asset(self, asset: 'FontAsset'):
        raise NotImplementedError()

    def draw_batch(self, batch: 'DrawBatch'):
        raise NotImplementedError()

    def prepare_draw_sprite(self, drawable: 'SpriteDrawable', batch: 'DrawBatch'):
        raise NotImplementedError()