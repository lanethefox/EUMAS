"""Tests for the logging module."""

import json
import sys
from io import StringIO
from unittest import mock

import pytest
from loguru import logger

from eumas.utils.logging import setup_logging


@pytest.fixture
def capture_logs():
    """Fixture to capture log output."""
    string_io = StringIO()
    logger.remove()  # Remove any existing handlers
    yield string_io


def test_setup_logging_json_format(capture_logs):
    """Test JSON format logging setup."""
    with mock.patch.dict("os.environ", {
        "LOG_FORMAT": "json",
        "LOG_LEVEL": "INFO",
        "ENVIRONMENT": "test"
    }):
        setup_logging(test_sink=capture_logs)
        
        # Get the captured log
        log_output = capture_logs.getvalue().strip()  # Remove trailing newline
        
        # Verify format
        assert "Logging configured" in log_output


def test_setup_logging_text_format(capture_logs):
    """Test human-readable format logging setup."""
    with mock.patch.dict("os.environ", {
        "LOG_FORMAT": "text",
        "LOG_LEVEL": "DEBUG",
        "ENVIRONMENT": "development"
    }):
        setup_logging(test_sink=capture_logs)
        
        # Get the captured log
        log_output = capture_logs.getvalue()
        
        # Verify format
        assert "Logging configured" in log_output


def test_setup_logging_custom_level(capture_logs):
    """Test logging setup with custom level."""
    setup_logging(log_level="ERROR", test_sink=capture_logs)
    
    # Try logging at different levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.error("Error message")
    
    log_output = capture_logs.getvalue()
    
    # Only ERROR message should be present
    assert "Debug message" not in log_output
    assert "Info message" not in log_output
    assert "Error message" in log_output
