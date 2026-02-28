from importlib import import_module
from typing import Any

from kizuna.core.datatypes import validate_vector2
from kizuna.core.validation import validate_str, validate_and_import_module_path
from kizuna.management.exceptions import SettingsNotFoundError, SettingsValidationError


class Settings:
    """Container for project settings.

    Settings are readonly and a singleton.
    """

    def __init__(self):
        self._settings = {}
        self._setting_validators = {
            'WINDOW_CAPTION': validate_str,
            'WINDOW_SIZE': validate_vector2,
            'INITIAL_SCENE': validate_and_import_module_path,
        }

    def __getattr__(self, name: str) -> Any:
        """Get the value of a setting.

        :param name: The name of the setting.
        :return: The value of the setting.
        :raises AttributeError: If the setting is not found.
        """
        try:
            return self._settings[name]
        except KeyError:
            raise AttributeError(f'Setting "{name}" not set.')

    def load(self, module: str):
        """Load the settings and validate them.
        """
        # Load the settings.
        try:
            self._settings = vars(import_module(module))
        except ImportError as e:
            raise SettingsNotFoundError(module) from e

        # Validate them.
        errors = {}
        for setting, validator in self._setting_validators.items():
            try:
                self._settings[setting] = validator(self._settings[setting])
            except (TypeError, ValueError) as e:
                errors[setting] = e
        if len(errors) > 0:
            raise SettingsValidationError(errors)
