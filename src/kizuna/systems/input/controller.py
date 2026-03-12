from kizuna.core.controllers import Controller
from kizuna.systems.input.constants import Key


class InputController(Controller):
    held_keys: dict[str, bool]

    def __init__(self):
        self.held_keys = {}

    def is_key_held(self, key: Key) -> bool:
        return key.value in self.held_keys and self.held_keys[key.value]
