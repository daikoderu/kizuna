from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kizuna.config import SettingSpec


class Controller:
    """Class to encapsulate top-level game logic.

    This class is the entrypoint of anything that happens in your application. Each controller manages the full state
    of a different game system.

    Kizuna creates one instance of each controller in the order specified in the ``CONTROLLERS`` setting. Their methods
    are always dispatched in the same order and are running for as long as your application is running.
    This ensures a completely determined and clear control flow of your code, Kizuna's code and any third-party
    libraries you may be using.

    To implement your own game logic, divide that logic in several different systems and create subclasses of
    :type:`Controller`. Then, implement the :meth:`on_init`, :meth:`on_step` and :meth:`on_draw` methods.

    This lightweight layer of inversion of control (IoC) allows you to keep greater control of how your game systems
    interact, and plug in different reusable systems according to your needs. You can choose whether to use Kizuna's
    built-in controllers, make your own, or even customize Kizuna's built-in controllers to your liking.

    :cvar settings: List of settings specific to this controller.

        ..  note:: The required settings in this list will be required only if the controller is listed in the
            ``CONTROLLERS`` setting.
    """
    settings: list['SettingSpec'] = []

    def on_init(self):
        """Called when the controller class is initialized at the start of the game loop.
        """
        ...

    def on_step(self, dt: float):
        """Called at each step of the game loop, to implement the game logic that must happen at each step.

        :param dt: Time step or "delta time", in seconds. This is the actual time passed between time steps. Every
            time-sensitive operation, such as moving a character, should be multiplied by this value to get a
            consistent speed in all devices.
        """
        ...

    def on_draw(self):
        """Called to draw a frame of the game screen.
        """
        ...
