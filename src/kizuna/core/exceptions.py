"""General custom exceptions.
"""

class KizunaError(Exception):
    """Base class for all Kizuna Framework exceptions.

    All Kizuna exceptions should inherit from this class and provide a short message explaining the cause of the error
    and providing a hint to solve it.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
