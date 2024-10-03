# pandis/exceptions.py
class PandisError(Exception):
    """Base exception class for Pandis."""
    pass

class KeyNotFoundError(PandisError):
    """Exception raised when a key is not found in the store."""
    pass

class InvalidOperationError(PandisError):
    """Exception raised for invalid operations."""
    pass