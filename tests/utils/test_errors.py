"""Tests for the error handling module."""

from unittest import mock

import pytest

from eumas.utils.errors import (
    EUMASError,
    ConfigurationError,
    DatabaseError,
    MemoryError,
    ArchetypeError,
    ValidationError,
)


def test_eumas_error_basic():
    """Test basic EUMASError functionality."""
    error = EUMASError("Test error")
    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.code is None
    assert error.details == {}


def test_eumas_error_with_code():
    """Test EUMASError with error code."""
    error = EUMASError("Test error", code="TEST_001")
    assert error.code == "TEST_001"


def test_eumas_error_with_details():
    """Test EUMASError with details."""
    details = {"key": "value"}
    error = EUMASError("Test error", details=details)
    assert error.details == details


def test_eumas_error_logging():
    """Test that EUMASError logs properly."""
    with mock.patch("eumas.utils.errors.logger.error") as mock_logger:
        error = EUMASError(
            "Test error",
            code="TEST_001",
            details={"key": "value"},
        )
        
        mock_logger.assert_called_once_with(
            "Test error",
            extra={
                "error_code": "TEST_001",
                "error_details": {"key": "value"},
                "error_type": "EUMASError",
            },
        )


def test_specific_errors():
    """Test specific error classes."""
    errors = [
        (ConfigurationError, "Config error"),
        (DatabaseError, "Database error"),
        (MemoryError, "Memory error"),
        (ArchetypeError, "Archetype error"),
        (ValidationError, "Validation error"),
    ]
    
    for error_class, message in errors:
        error = error_class(message)
        assert isinstance(error, EUMASError)
        assert str(error) == message
