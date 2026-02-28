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
