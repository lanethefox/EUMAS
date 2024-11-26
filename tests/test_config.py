"""Tests for the configuration module."""

import os
from unittest import mock

import pytest

from eumas.config import Config


def test_config_loads_environment_variables():
    """Test that Config loads environment variables correctly."""
    with mock.patch.dict(os.environ, {
        "OPENAI_API_KEY": "test_key",
        "WEAVIATE_URL": "test_url",
        "LOG_LEVEL": "DEBUG",
        "LOG_FORMAT": "json",
        "ENVIRONMENT": "test"
    }):
        assert Config.OPENAI_API_KEY == "test_key"
        assert Config.WEAVIATE_URL == "test_url"
        assert Config.LOG_LEVEL == "DEBUG"
        assert Config.LOG_FORMAT == "json"
        assert Config.ENVIRONMENT == "test"


def test_config_validation():
    """Test Config validation."""
    # Test with missing API key
    with mock.patch.dict(os.environ, {
        "OPENAI_API_KEY": "",
        "WEAVIATE_URL": "test_url"
    }):
        assert Config.validate() == "OPENAI_API_KEY is not set"

    # Test with missing Weaviate URL
    with mock.patch.dict(os.environ, {
        "OPENAI_API_KEY": "test_key",
        "WEAVIATE_URL": ""
    }):
        assert Config.validate() == "WEAVIATE_URL is not set"

    # Test with all required variables set
    with mock.patch.dict(os.environ, {
        "OPENAI_API_KEY": "test_key",
        "WEAVIATE_URL": "test_url"
    }):
        assert Config.validate() is None
