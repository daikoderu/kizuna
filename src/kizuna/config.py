from importlib import import_module
from typing import Any, Callable

from kizuna.backends import Backend
from kizuna.core.datatypes import validate_ivector2
from kizuna.core.validation import validate_str, validate_list, validate_and_import_module_path, validate_positive_float
from kizuna.management.exceptions import BackendNotInstantiatedError, SettingsNotFoundError, SettingsValidationError


class SettingSpec:
    """Specification for a setting.
    """

    def __init__(self, name: str, validator: Callable[[Any], Any], default: Any = None, required: bool = False):
        """Private constructor. Use :meth:`required` or :meth:`default` instead.
        """
        self.name = name.upper()
        self.validator = validator
        self.default = default
        self.required = required

    @staticmethod
    def required(name: str, validator: Callable[[Any], Any]):
        """Define a required setting.

        :param name: The name of the setting. Settings names are always uppercase.
        :param validator: The validator to use to validate the setting. This must be a function that takes the set
            value and returns the sanitized value or raises either ``TypeError`` or ``ValueError``.
        """
        return SettingSpec(name, validator, required=True)

    @staticmethod
    def optional(name: str, validator: Callable[[Any], Any], default: Any):
        """Define an optional setting.

        :param name: The name of the setting. Settings names are always uppercase.
        :param validator: The validator to use to validate the setting. This must be a function that takes the set
            value and returns the sanitized value or raises either ``TypeError`` or ``ValueError``.
        :param default: The default value to use if not set.
        """
        return SettingSpec(name, validator, required=False, default=default)

    def validate(self, settings_dict: dict[str, Any], errors: dict[str, TypeError | ValueError]):
        try:
            settings_dict[self.name] = self.validator(settings_dict[self.name])
        except (TypeError, ValueError) as e:
            errors[self.name] = e
        except KeyError:
            if not self.required:
                settings_dict[self.name] = self.default
            else:
                errors[self.name] = TypeError(f'Setting "{self.name}" not set, but is required.')


BASIC_SETTINGS = [
    SettingSpec.required('WINDOW_CAPTION', validate_str),
    SettingSpec.required('WINDOW_SIZE', validate_ivector2),
    SettingSpec.required(
        'CONTROLLERS', lambda v: validate_list(v, distinct=True, child=validate_and_import_module_path),
    ),
    SettingSpec.required('STEPS_PER_SECOND', validate_positive_float),
    SettingSpec.required('FRAMES_PER_SECOND', validate_positive_float),
    SettingSpec.required('BACKEND_CLASS', validate_and_import_module_path),
]


class Settings:
    """Container for project settings.

    Settings are readonly and a singleton.
    """

    def __init__(self):
        self._settings = {}
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

        # Validate the basic settings.
        errors = {}
        for setting in BASIC_SETTINGS:
            setting.validate(self._settings, errors)
        if len(errors) > 0:
            raise SettingsValidationError(errors)

        # Validate the controller settings.
        for controller_class in self._settings['CONTROLLERS']:
            for setting in controller_class.settings:
                setting.validate(self._settings, errors)

        # Create the backend instance.
        self._backend = self.BACKEND_CLASS(self)


settings = Settings()
