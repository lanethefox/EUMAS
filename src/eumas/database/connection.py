"""Database connection and schema management for EUMAS."""

import weaviate
from weaviate.exceptions import WeaviateBaseError

from eumas.config import Config
from eumas.database.schema import (
    get_memory_class_schema,
    get_relationship_class_schema,
    MEMORY_CLASS_NAME,
    RELATIONSHIP_CLASS_NAME,
)


class DatabaseConnection:
    """Manages the connection to the Weaviate database."""

    def __init__(self) -> None:
        """Initialize the database connection."""
        self.client = weaviate.Client(Config.WEAVIATE_URL)

    def is_healthy(self) -> bool:
        """Check if the database connection is healthy.
        
        Returns:
            bool: True if the connection is healthy, False otherwise.
        """
        try:
            return self.client.is_ready()
        except WeaviateBaseError:
            return False

    def create_schema(self) -> None:
        """Create the EUMAS schema in Weaviate.
        
        Raises:
            WeaviateBaseError: If schema creation fails.
        """
        # Create Memory class
        if not self.client.schema.exists(MEMORY_CLASS_NAME):
            self.client.schema.create_class(get_memory_class_schema())

        # Create MemoryRelationship class
        if not self.client.schema.exists(RELATIONSHIP_CLASS_NAME):
            self.client.schema.create_class(get_relationship_class_schema())

    def delete_schema(self) -> None:
        """Delete the EUMAS schema from Weaviate.
        
        Raises:
            WeaviateBaseError: If schema deletion fails.
        """
        if self.client.schema.exists(RELATIONSHIP_CLASS_NAME):
            self.client.schema.delete_class(RELATIONSHIP_CLASS_NAME)
        if self.client.schema.exists(MEMORY_CLASS_NAME):
            self.client.schema.delete_class(MEMORY_CLASS_NAME)

    def reset_schema(self) -> None:
        """Reset the EUMAS schema in Weaviate.
        
        This deletes the existing schema and creates a new one.
        
        Raises:
            WeaviateBaseError: If schema reset fails.
        """
        self.delete_schema()
        self.create_schema()
