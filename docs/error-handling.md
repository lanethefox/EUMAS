# Error Handling System

This document describes the error handling system used throughout EUMAS.

## Overview

EUMAS uses a hierarchical error handling system with custom exceptions for different types of errors. All exceptions include detailed error messages and are properly logged for debugging purposes.

## Exception Hierarchy

```
BaseError
└── EumasError
    ├── ConfigError
    │   └── EnvironmentError
    ├── DatabaseError
    │   ├── ConnectionError
    │   └── SchemaError
    └── EmbeddingError
```

### Base Classes

#### BaseError
The root exception class for all EUMAS errors. Provides basic error logging and formatting.

```python
class BaseError(Exception):
    """Base class for all EUMAS errors."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.error_code = error_code
        super().__init__(message)
```

#### EumasError
Main error class for EUMAS-specific errors. Adds structured logging and error type information.

```python
class EumasError(BaseError):
    """Main error class for EUMAS-specific errors."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, error_code)
```

### Specific Exceptions

#### ConfigError
Raised for configuration-related errors.
- Missing configuration files
- Invalid configuration values
- Environment variable issues

#### DatabaseError
Raised for database-related errors.
- Connection failures
- Schema validation errors
- Query execution errors

#### EmbeddingError
Raised for embedding generation errors.
- API errors
- Invalid input
- Rate limiting issues

## Error Logging

Errors are logged using the structured logging system with the following information:
- Error type
- Error message
- Error code (if applicable)
- Stack trace
- Additional context (when available)

Example log entry:
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "ERROR",
  "error_type": "EmbeddingError",
  "message": "Failed to generate embeddings: API error",
  "error_code": "EMB001",
  "error_details": {
    "input_length": 100,
    "model": "text-embedding-ada-002"
  }
}
```

## Best Practices

1. Exception Handling
   - Always catch specific exceptions rather than using bare except
   - Include context in error messages
   - Log errors at appropriate levels

2. Error Messages
   - Be descriptive but concise
   - Include actionable information
   - Follow consistent formatting

3. Error Codes
   - Use consistent prefix for each subsystem
   - Include in logs for easy searching
   - Document in code comments

## Example Usage

```python
try:
    embedding = generator.generate("some text")
except EmbeddingError as e:
    logger.error(f"Failed to generate embedding: {e}")
    # Handle error appropriately
except DatabaseError as e:
    logger.error(f"Database operation failed: {e}")
    # Handle database error
except EumasError as e:
    logger.error(f"Unexpected error: {e}")
    # Handle other EUMAS errors
```
