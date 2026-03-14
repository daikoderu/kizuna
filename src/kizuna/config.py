import logging
from importlib import import_module
from typing import Any, Callable, Iterable

from kizuna.backends import Backend
from kizuna.core.datatypes import validate_ivector2
from kizuna.core.validation import validate_str, validate_list, validate_and_import_module_path, validate_positive_float
from kizuna.management.exceptions import BackendNotInstantiatedError, SettingsNotFoundError, SettingsValidationError
from kizuna.utils import fullname

logger = logging.getLogger(__name__)


class SettingSpec:
    """Specification for a setting.
    """

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

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if self.required:
            return f'SettingSpec("{self.name}", required)'
        else:
            return f'SettingSpec("{self.name}", default={repr(self.default)})'

    def __init__(self, name: str, validator: Callable[[Any], Any], default: Any = None, required: bool = False):
        """Private constructor. Use :meth:`required` or :meth:`default` instead.
        """
        self.name = name.upper()
        self.validator = validator
        self.default = default
        self.required = required


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

    Settings are readonly and a singleton. Use :data:`settings` to access the project settings.
    """

    def __init__(self):
        self._settings = {}
        self.dynamic_imports = []
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

    def __str__(self) -> str:
        return 'Settings'

    def __repr__(self) -> str:
        return f'Settings'

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
            self._validate(setting, errors)  # noqa
            self._register_dynamic_import(self._settings[setting.name])
        if len(errors) > 0:
            raise SettingsValidationError(errors)
        logger.info('Settings loaded.')

        # Validate the controller settings.
        for controller_class in self._settings['CONTROLLERS']:
            for setting in controller_class.settings:
                self._validate(setting, errors)  # noqa
                self._register_dynamic_import(self._settings[setting.name])

        # Create the backend instance.
        self._backend = self.BACKEND_CLASS(self)
        logger.info(f'Backend instantiated: "{fullname(self.BACKEND_CLASS)}".')

    def _register_dynamic_import(self, value: Any):
        if isinstance(value, type | Callable):
            self.dynamic_imports.append('.'.join(fullname(value).split('.')[:-1]))
        elif isinstance(value, list | tuple | set):
            for element in value:
                self._register_dynamic_import(element)
        elif isinstance(value, dict):
            for k, v in value.items():
                self._register_dynamic_import(k)
                self._register_dynamic_import(v)

    def _validate(self, spec: SettingSpec, errors: dict[str, TypeError | ValueError]):
        try:
            self._settings[spec.name] = spec.validator(self._settings[spec.name])
        except (TypeError, ValueError) as e:
            errors[spec.name] = e
        except KeyError:
            if not spec.required:
                self._settings[spec.name] = spec.default
            else:
                errors[spec.name] = TypeError(f'Setting "{spec.name}" not set, but is required.')


settings = Settings()
"""Settings singleton instance.
"""
