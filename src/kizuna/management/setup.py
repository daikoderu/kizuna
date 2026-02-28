import sys
from pathlib import Path

import pyglet

from kizuna.config import settings


def _setup_assets(assets_path: Path):
    """Set up the assets directory for Pyglet.

    :param assets_path: The path to the asset directory.
    """
    pyglet.resource.path = [str(assets_path)]
    pyglet.resource.reindex()


def _run():
    """Launch the application.
    """
    window = pyglet.window.Window()
    window.size = settings.WINDOW_SIZE.as_tuple
    window.set_caption(settings.WINDOW_CAPTION)

    current_scene = settings.INITIAL_SCENE

    @window.event
    def on_draw():
        window.clear()
        for drawable in current_scene.drawables:
            drawable.on_draw()

    pyglet.app.run()


def initialize(base_directory: Path, standalone: bool):
    """Initialize the application.
    """
    # Add the base directory to the PYTHONPATH.
    sys.path.insert(0, str(base_directory))

    # Set up asset path.
    pyglet.resource.path = [str(base_directory / 'assets')]
    pyglet.resource.reindex()

    # Load and validate settings.
    settings.load('src.settings')


def bootstrap(base_directory: Path, standalone: bool):
    """Entrypoint for Kizuna applications.

    :param base_directory: The base directory of the project.
    :param standalone: If true, runs the application in standalone mode.
    """
    initialize(base_directory, standalone)
    _run()
