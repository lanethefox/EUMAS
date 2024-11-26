# Database Operations

This document describes the database operations available in EUMAS for managing memories and their relationships.

## Memory Operations

### Basic Operations

- `store_memory`: Store a single memory instance
- `store_memory_relation`: Store a single memory relation
- `store_memories_batch`: Store multiple memories in batch for better performance
- `store_relations_batch`: Store multiple relations in batch for better performance

### Query Operations

#### Time-Based Queries
- `get_memories_by_timerange`: Retrieve memories within a specific time range
  - Parameters:
    - `start_time`: Start of time range
    - `end_time`: End of time range
    - `limit`: Maximum number of memories to return (default: 100)

#### Context-Based Queries
- `get_memories_by_context`: Get memories matching specific context tags and minimum priority
  - Parameters:
    - `context_tags`: List of context tags to match
    - `min_priority`: Minimum memory priority threshold
    - `limit`: Maximum number of memories to return (default: 100)

#### Relationship Queries
- `get_significant_memories`: Get the most significant memories based on their relationships
  - Parameters:
    - `limit`: Maximum number of memories to return (default: 5)
    - `min_relationship_strength`: Minimum strength threshold
    - `archetype_filter`: Optional archetype to filter by

- `get_memory_network`: Get the network of memories connected to a given memory
  - Parameters:
    - `memory_id`: UUID of the source memory
    - `max_depth`: Maximum depth of relationships to traverse
    - `min_strength`: Minimum relationship strength to include

- `get_archetype_perspective`: Get memories from a specific archetype's perspective
  - Parameters:
    - `archetype`: The archetype to analyze (e.g., "Ella-M")
    - `context_tag`: Optional context tag filter
    - `limit`: Maximum number of memories to return

## Database Connection

### Connection Management
- `is_healthy`: Check database connection health
- `validate_schema`: Validate schema integrity
- `get_schema_status`: Check existence of schema classes
- `get_batch_client`: Get client for batch operations

### Schema Management
- `create_schema`: Create the EUMAS schema
- `delete_schema`: Delete the EUMAS schema
- `reset_schema`: Reset (delete and recreate) the schema

## Best Practices

1. **Batch Operations**
   - Use batch operations when storing multiple items
   - Configure batch size based on your data size (default: 100)
   - Handle batch operation errors appropriately

2. **Query Optimization**
   - Use appropriate filters to limit result sets
   - Consider memory priority when querying
   - Use batch operations for bulk data processing

3. **Error Handling**
   - Always check connection health before operations
   - Validate schema integrity periodically
   - Handle WeaviateBaseError exceptions

4. **Performance Tips**
   - Use batch operations for bulk inserts
   - Index frequently queried properties
   - Monitor and optimize query performance

## Examples

### Storing Memories in Batch
```python
memories = [
    Memory(user_prompt="Hello", agent_reply="Hi", ...),
    Memory(user_prompt="How are you?", agent_reply="I'm good", ...)
]
uuids = memory_ops.store_memories_batch(memories)
```

### Querying by Time Range
```python
start_time = datetime.now() - timedelta(days=7)
end_time = datetime.now()
recent_memories = memory_ops.get_memories_by_timerange(
    start_time=start_time,
    end_time=end_time,
    limit=50
)
```

### Getting Archetype Perspective
```python
memories = memory_ops.get_archetype_perspective(
    archetype="Ella-M",
    context_tag="conversation",
    limit=10
)
```
