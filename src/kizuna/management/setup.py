import sys
from pathlib import Path

import pyglet

from kizuna.config import settings
from kizuna.management.game_loop import launch


def initialize(base_directory: Path, standalone: bool):
    """Initialize the application.

    This is used to validate settings and initialize anything necessary for Kizuna's CLI to work smoothly with the
    project.

    :param base_directory: The base directory of the project.
    :param standalone: If true, runs the application in standalone mode.
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
    launch()
