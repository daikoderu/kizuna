import sys
from pathlib import Path

from kizuna.config import settings


def initialize(base_directory: Path, standalone: bool):
    """Initialize the application.

    This is used to validate settings and initialize anything necessary for Kizuna's CLI to work smoothly with the
    project.

    :param base_directory: The base directory of the project.
    :param standalone: If true, runs the application in standalone mode.
    """
    # Add the base directory to the PYTHONPATH.
    sys.path.insert(0, str(base_directory))

    # Load and validate settings.
    settings.load('src.settings')

    # Create the backend instance and initialize it.
    settings.backend.initialize(base_directory)


def bootstrap(base_directory: Path, standalone: bool):
    """Entrypoint for Kizuna applications.

    :param base_directory: The base directory of the project.
    :param standalone: If true, runs the application in standalone mode.
    """
    initialize(base_directory, standalone)
    settings.backend.launch_game_loop()
