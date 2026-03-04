import pyglet

from kizuna.config import settings
from kizuna.core.controllers import Controller


def launch():
    """Launch the application's game loop.
    """
    window = pyglet.window.Window()
    window.size = tuple(settings.WINDOW_SIZE)
    window.set_caption(settings.WINDOW_CAPTION)

    # Instantiate the controllers.
    controllers = [controller_class() for controller_class in settings.CONTROLLERS]

    # Call the ``on_init`` method on each controller.
    for controller in controllers:
        controller.on_init()

    # Schedule update calls.
    pyglet.clock.schedule_interval(lambda dt: step(dt, controllers), 1 / settings.STEPS_PER_SECOND)

    # Attach the draw event handler.
    @window.event
    def on_draw():
        draw(window, controllers)

    # Run the app.
    pyglet.app.run(1 / settings.FRAMES_PER_SECOND)


def step(dt: float, controllers: list[Controller]):
    for controller in controllers:
        controller.on_step(dt)


def draw(window: pyglet.window.Window, controllers: list[Controller]):
    window.clear()
    for controller in controllers:
        controller.on_draw()
