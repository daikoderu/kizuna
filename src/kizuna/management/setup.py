import logging
import sys
from pathlib import Path

from kizuna import __version__
from kizuna.config import settings
from kizuna.core.controllers import Controller
from kizuna.management.exceptions import ControllerDependencyInjectionError


logger = logging.getLogger(__name__)


def initialize(base_directory: Path, standalone: bool, enable_kizuna_log: bool):
    """Initialize the application.

    This is used to validate settings and initialize anything necessary for Kizuna's CLI to work smoothly with the
    project.

    :param base_directory: The base directory of the project.
    :param standalone: If true, runs the application in standalone mode.
    :param enable_kizuna_log: If true, configure logging.
    """
    # Create log file.
    if enable_kizuna_log:
        logging.basicConfig(
            filename=str(base_directory / 'kizuna.log'),
            level=logging.INFO if standalone else logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            force=True,
        )
        logger.info(f'===== Kizuna Log File - Version {__version__} =====')

    # Add the base directory to the PYTHONPATH.
    sys.path.insert(0, str(base_directory))

    # Load and validate settings.
    settings.load('src.settings')

    # Create the backend instance and initialize it.
    settings.backend.initialize(base_directory, standalone)


def launch_app():
    controllers = setup_controllers()
    step_fn = lambda dt: step_function(dt, controllers)
    draw_fn = lambda: draw_function(controllers)
    settings.backend.launch_game_loop(step_fn, draw_fn, controllers)


def setup_controllers() -> list[Controller]:
    controllers_dict = {}
    for controller_class in settings.CONTROLLERS:
        # Instantiate the controller.
        controller = controller_class()

        # Apply dependency injection between controllers.
        for variable, annotation in controller_class.__annotations__.items():
            # Skip any annotations of types that do not subclass Controller.
            if not isinstance(annotation, type) or not issubclass(annotation, Controller):
                continue

            # Ensure the dependent controllers have been specified before.
            if annotation not in controllers_dict:
                raise ControllerDependencyInjectionError(controller_class, annotation)

            # Inject the dependency controller instance.
            setattr(controller, variable, controllers_dict[annotation])

        # Add the controller to the dictionary of controller classes to instances.
        controllers_dict[controller_class] = controller

    # Call the ``on_init`` method on each controller.
    controllers_list = list(controllers_dict.values())
    for controller in controllers_list:
        controller.on_init()

    return controllers_list


def step_function(dt: float, controllers: list[Controller]):
    for controller in controllers:
        controller.on_step(dt)


def draw_function(controllers: list[Controller]):
    for controller in controllers:
        controller.on_draw()


def bootstrap(base_directory: Path, standalone: bool, enable_kizuna_log: bool = True):
    """Entrypoint for Kizuna applications.

    :param base_directory: The base directory of the project.
    :param standalone: If true, runs the application in standalone mode.
    :param enable_kizuna_log: If true, configure logging.
    """
    initialize(base_directory, standalone, enable_kizuna_log)
    launch_app()
