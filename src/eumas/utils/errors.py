"""Error handling utilities for EUMAS."""

from typing import Optional, Any, Dict

from loguru import logger


class EUMASError(Exception):
    """Base exception class for EUMAS."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.
        
        Args:
            message: Human-readable error message
            code: Optional error code for programmatic handling
            details: Optional dictionary of additional error details
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
        
        # Log the error
        logger.error(
            self.message,
            extra={
                "error_code": self.code,
                "error_details": self.details,
                "error_type": self.__class__.__name__,
            },
        )


class ConfigurationError(EUMASError):
    """Raised when there is a configuration-related error."""
    pass


class DatabaseError(EUMASError):
    """Raised when there is a database-related error."""
    pass


class MemoryError(EUMASError):
    """Raised when there is a memory-related error."""
    pass


class ArchetypeError(EUMASError):
    """Raised when there is an archetype-related error."""
    pass


class ValidationError(EUMASError):
    """Raised when there is a validation error."""
    pass


class EmbeddingError(EUMASError):
    """Exception raised for embedding generation errors."""

    def __init__(self, message: str):
        """Initialize the error.

        Args:
            message (str): The error message.
        """
        super().__init__(f"Embedding error: {message}")
