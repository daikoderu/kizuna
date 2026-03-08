

class InputState:
    held_keys: dict[str, bool]

    def __init__(self):
        self.held_keys = {}

    def is_key_held(self, key: str) -> bool:
        return key in self.held_keys and self.held_keys[key]


inputstate = InputState()
