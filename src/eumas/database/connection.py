"""Database connection and schema management for EUMAS."""

import weaviate
from weaviate.exceptions import WeaviateBaseError
from typing import Dict

from eumas.config import Config
from eumas.database.schema import (
    get_memory_class_schema,
    get_archetype_memory_relation_schema,
    MEMORY_CLASS,
    ARCHETYPE_MEMORY_RELATION_CLASS,
)


class DatabaseConnection:
    """Manages the connection to the Weaviate database."""

    def __init__(self) -> None:
        """Initialize the database connection."""
        self.client = weaviate.Client(
            url=Config.WEAVIATE_URL,
            additional_headers={
                "X-GraphQL-Introspection": "true"  # Enable GraphQL introspection
            }
        )

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
        if not self.client.schema.exists(MEMORY_CLASS):
            self.client.schema.create_class(get_memory_class_schema())

        # Create ArchetypeMemoryRelation class
        if not self.client.schema.exists(ARCHETYPE_MEMORY_RELATION_CLASS):
            self.client.schema.create_class(get_archetype_memory_relation_schema())

    def delete_schema(self) -> None:
        """Delete the EUMAS schema from Weaviate.
        
        Note: Delete ArchetypeMemoryRelation first to handle reference constraints.
        
        Raises:
            WeaviateBaseError: If schema deletion fails.
        """
        if self.client.schema.exists(ARCHETYPE_MEMORY_RELATION_CLASS):
            self.client.schema.delete_class(ARCHETYPE_MEMORY_RELATION_CLASS)
        if self.client.schema.exists(MEMORY_CLASS):
            self.client.schema.delete_class(MEMORY_CLASS)

    def reset_schema(self) -> None:
        """Reset the EUMAS schema in Weaviate.
        
        This deletes the existing schema and creates a new one.
        
        Raises:
            WeaviateBaseError: If schema reset fails.
        """
        self.delete_schema()
        self.create_schema()
        
    def get_graphql_client(self):
        """Get the GraphQL client for complex graph queries.
        
        Returns:
            weaviate.gql.get.GetBuilder: GraphQL query builder
        """
        return self.client.query.get

    def validate_schema(self) -> bool:
        """Validate that the existing schema matches the expected configuration.
        
        Returns:
            bool: True if schema is valid, False otherwise.
        """
        try:
            for class_name in [MEMORY_CLASS, ARCHETYPE_MEMORY_RELATION_CLASS]:
                if not self.client.schema.exists(class_name):
                    return False
                
                existing = self.client.schema.get(class_name)
                expected = (get_memory_class_schema() if class_name == MEMORY_CLASS 
                          else get_archetype_memory_relation_schema())
                
                # Compare core properties
                existing_props = {p["name"]: p for p in existing["properties"]}
                expected_props = {p["name"]: p for p in expected["properties"]}
                
                if set(existing_props.keys()) != set(expected_props.keys()):
                    return False
                
            return True
        except WeaviateBaseError:
            return False

    def get_batch_client(self, batch_size: int = 100) -> weaviate.batch.Batch:
        """Get a batch client for efficient bulk operations.
        
        Args:
            batch_size: Number of objects to process in each batch
            
        Returns:
            weaviate.batch.Batch: Batch client for bulk operations
        """
        return self.client.batch.configure(
            batch_size=batch_size,
            dynamic=True,
            timeout_retries=3
        )

    def get_schema_status(self) -> Dict[str, bool]:
        """Get the current status of schema classes.
        
        Returns:
            Dict[str, bool]: Status of each schema class
        """
        return {
            MEMORY_CLASS: self.client.schema.exists(MEMORY_CLASS),
            ARCHETYPE_MEMORY_RELATION_CLASS: self.client.schema.exists(ARCHETYPE_MEMORY_RELATION_CLASS)
        }
