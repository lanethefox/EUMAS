# Database Connection System

This document describes the database connection system used in EUMAS for interacting with Weaviate.

## Overview

EUMAS uses Weaviate as its vector database for storing and retrieving memory embeddings. The database connection system provides a robust interface for managing connections and performing operations.

## Components

### DatabaseConnection

The `DatabaseConnection` class manages the connection to Weaviate and provides methods for common operations.

#### Configuration

```python
from eumas.database.connection import DatabaseConnection

# Initialize connection
conn = DatabaseConnection(
    url="http://localhost:8080",
    auth_config=None  # Optional authentication configuration
)

# Check connection health
is_healthy = conn.check_health()

# Get client for direct operations
client = conn.get_client()
```

### Schema Management

The system includes tools for managing the Weaviate schema based on YAML configuration:

```yaml
# ella_schema.yaml
classes:
  - class: Memory
    description: Represents a single memory or interaction
    properties:
      - name: content
        dataType: text
        description: The actual content of the memory
      - name: embedding
        dataType: vector
        dimension: 1536
```

#### Schema Creation

```python
from eumas.database.schema import create_schema

# Create schema from YAML
create_schema("ella_schema.yaml")
```

## Error Handling

The database system includes comprehensive error handling:

1. Connection Errors
   ```python
   try:
       conn = DatabaseConnection(url="invalid-url")
   except DatabaseError as e:
       logger.error(f"Failed to connect: {e}")
   ```

2. Schema Errors
   ```python
   try:
       create_schema("invalid_schema.yaml")
   except SchemaError as e:
       logger.error(f"Invalid schema: {e}")
   ```

## Health Checks

The system includes built-in health checks:

```python
def check_database_health():
    """Check database connection and schema health."""
    try:
        # Check basic connectivity
        if not conn.check_health():
            raise DatabaseError("Database is not healthy")
            
        # Check schema existence
        if not conn.check_schema():
            raise SchemaError("Required schema is missing")
            
        return True
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False
```

## Best Practices

1. Connection Management
   - Use connection pooling for better performance
   - Implement retry logic for transient failures
   - Close connections properly when done

2. Schema Management
   - Version control your schema files
   - Use migrations for schema changes
   - Validate schema before applying changes

3. Error Handling
   - Handle connection timeouts
   - Implement circuit breakers for failing operations
   - Log all database operations for debugging

## Future Improvements

1. Connection Pooling
   - Implement connection pool management
   - Add connection lifecycle hooks
   - Monitor connection health

2. Schema Migrations
   - Add schema version tracking
   - Implement automated migrations
   - Add schema backup/restore

3. Performance Monitoring
   - Add query performance tracking
   - Implement query optimization
   - Add connection metrics
