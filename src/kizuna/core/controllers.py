class Controller:
    """Class to encapsulate top-level game logic.

    Each controller manages state of a different game system.

    Kizuna creates one instance of each controller in the order specified in the ``CONTROLLERS`` setting. Their methods
    are always dispatched in the same order.
    """

    def on_init(self):
        """Called when the controller class is initialized at the start of the game loop.
        """
        raise NotImplementedError()

    def on_step(self, dt: float):
        """Called at each step of the game loop, to implement the game logic that must happen at each step.

        :param dt: Time step or "delta time", in seconds. This is the time passed between time steps. Every time
            sensitive operation, such as moving a character, should be multiplied by this value to get a consistent
            speed.
        """
        raise NotImplementedError()

    def on_draw(self):
        """Called at the end of each step of the game loop, to draw the game.
        """
        raise NotImplementedError()
