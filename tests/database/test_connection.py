"""Tests for the database connection module."""

from unittest.mock import MagicMock, patch

import pytest
from weaviate.exceptions import WeaviateBaseError

from eumas.database.connection import DatabaseConnection
from eumas.database.schema import MEMORY_CLASS_NAME, RELATIONSHIP_CLASS_NAME


@pytest.fixture
def mock_client():
    """Create a mock Weaviate client."""
    with patch("weaviate.Client") as mock:
        yield mock.return_value


def test_database_connection_initialization(mock_client):
    """Test database connection initialization."""
    connection = DatabaseConnection()
    assert connection.client == mock_client


def test_health_check_success(mock_client):
    """Test successful health check."""
    mock_client.is_ready.return_value = True
    connection = DatabaseConnection()
    assert connection.is_healthy() is True


def test_health_check_failure(mock_client):
    """Test failed health check."""
    mock_client.is_ready.side_effect = WeaviateBaseError("Connection failed")
    connection = DatabaseConnection()
    assert connection.is_healthy() is False


def test_create_schema_success(mock_client):
    """Test successful schema creation."""
    # Mock schema existence checks
    mock_client.schema.exists.side_effect = [False, False]
    
    connection = DatabaseConnection()
    connection.create_schema()
    
    # Verify schema creation calls
    assert mock_client.schema.create_class.call_count == 2
    create_calls = mock_client.schema.create_class.call_args_list
    memory_schema = create_calls[0][0][0]
    relationship_schema = create_calls[1][0][0]
    
    assert memory_schema["class"] == MEMORY_CLASS_NAME
    assert relationship_schema["class"] == RELATIONSHIP_CLASS_NAME


def test_create_schema_already_exists(mock_client):
    """Test schema creation when classes already exist."""
    # Mock schema existence checks
    mock_client.schema.exists.return_value = True
    
    connection = DatabaseConnection()
    connection.create_schema()
    
    # Verify no creation attempts were made
    mock_client.schema.create_class.assert_not_called()


def test_delete_schema_success(mock_client):
    """Test successful schema deletion."""
    # Mock schema existence checks
    mock_client.schema.exists.return_value = True
    
    connection = DatabaseConnection()
    connection.delete_schema()
    
    # Verify deletion calls
    assert mock_client.schema.delete_class.call_count == 2
    delete_calls = [call[0][0] for call in mock_client.schema.delete_class.call_args_list]
    assert RELATIONSHIP_CLASS_NAME in delete_calls
    assert MEMORY_CLASS_NAME in delete_calls


def test_delete_schema_not_exists(mock_client):
    """Test schema deletion when classes don't exist."""
    # Mock schema existence checks
    mock_client.schema.exists.return_value = False
    
    connection = DatabaseConnection()
    connection.delete_schema()
    
    # Verify no deletion attempts were made
    mock_client.schema.delete_class.assert_not_called()


def test_reset_schema(mock_client):
    """Test schema reset."""
    # Mock schema existence checks for delete and create operations
    mock_client.schema.exists.side_effect = [
        True,   # Memory class exists (delete)
        True,   # Relationship class exists (delete)
        False,  # Memory class doesn't exist (create)
        False,  # Relationship class doesn't exist (create)
    ]
    
    connection = DatabaseConnection()
    connection.reset_schema()
    
    # Verify delete and create were called
    assert mock_client.schema.delete_class.call_count == 2
    assert mock_client.schema.create_class.call_count == 2
