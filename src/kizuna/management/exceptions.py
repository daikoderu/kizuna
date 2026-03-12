"""Project management and initialization exceptions.
"""


class ManagementError(Exception):
    """Base class for exceptions related to project management.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class SettingsNotFoundError(ManagementError):
    """Exception raised when settings are not found.
    """

    def __init__(self, expected_module: str):
        super().__init__(f'Settings file not found at "{expected_module}". Are you in the correct directory?')


class SettingsValidationError(ManagementError):
    """Exception raised when settings are not correct.
    """

    def __init__(self, errors: dict[str, TypeError | ValueError]):
        super().__init__('Errors detected in the settings.')
        self.errors = errors


class BackendNotInstantiatedError(ManagementError):
    """Exception raised when the backend is not instantiated.
    """

    def __init__(self):
        super().__init__(f'The backend is not instantiated.')


class ControllerDependencyInjectionError(ManagementError):
    """Exception raised when instantiating controllers.
    """

    def __init__(self, dependent_controller: type, dependency_controller: type):
        super().__init__(
            f'Cannot instantiate "{dependent_controller.__qualname__}" because it depends on '
            f'"{dependency_controller.__qualname__}", which is not declared in "settings.CONTROLLERS" before.'
        )
