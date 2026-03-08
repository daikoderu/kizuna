from importlib import import_module
from typing import Any

from kizuna.backends import Backend
from kizuna.core.datatypes import validate_ivector2
from kizuna.core.validation import validate_str, validate_list, validate_and_import_module_path, validate_positive_float
from kizuna.management.exceptions import BackendNotInstantiatedError, SettingsNotFoundError, SettingsValidationError


class Settings:
    """Container for project settings.

    Settings are readonly and a singleton.
    """

    def __init__(self):
        self._settings = {}
        self._setting_validators = {
            'WINDOW_CAPTION': validate_str,
            'WINDOW_SIZE': validate_ivector2,
            'CONTROLLERS': lambda v: validate_list(v, distinct=True, child=validate_and_import_module_path),
            'STEPS_PER_SECOND': validate_positive_float,
            'FRAMES_PER_SECOND': validate_positive_float,
            'BACKEND_CLASS': validate_and_import_module_path,
        }
        self._setting_defaults = {}
        self._backend = None

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

    @property
    def backend(self) -> Backend:
        """Get the backend instance.

        :raises BackendNotInstantiatedError: If the backend has not been instantiated.
        """
        if self._backend is None:
            raise BackendNotInstantiatedError()
        return self._backend

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
            except KeyError as e:
                if setting in self._setting_defaults:
                    self._settings[setting] = self._setting_defaults[setting]
                else:
                    errors[setting] = TypeError(f'Setting "{setting}" not set, but is required.')
        if len(errors) > 0:
            raise SettingsValidationError(errors)

        # Create the backend instance.
        self._backend = self.BACKEND_CLASS(self)


settings = Settings()
