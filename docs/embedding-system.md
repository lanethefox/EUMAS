# EUMAS Embedding System

This document describes the embedding system used in EUMAS for vectorizing and managing memory content.

## Overview

The embedding system is responsible for converting textual information into vector representations that can be efficiently stored and retrieved. It uses OpenAI's text-embedding-ada-002 model to generate high-quality embeddings.

## Components

### EmbeddingGenerator

The `EmbeddingGenerator` class is the core component responsible for generating embeddings. It provides a clean interface for converting text into vector representations.

#### Usage

```python
from eumas.embeddings.generator import EmbeddingGenerator

# Initialize the generator
generator = EmbeddingGenerator()

# Generate embedding for a single text
embedding = generator.generate("some text")

# Generate embeddings for multiple texts
embeddings = generator.generate(["text1", "text2"])

# Generate embedding with metadata
result = generator.generate_with_metadata(
    "text",
    metadata={"source": "user", "timestamp": "2024-01-01"}
)
```

#### Configuration

- Default model: `text-embedding-ada-002`
- Embedding dimension: 1536
- Model can be customized during initialization: `EmbeddingGenerator(model="custom-model")`

### Error Handling

The system provides robust error handling through custom exceptions:

- `EmbeddingError`: Base exception for all embedding-related errors
  - Raised when embedding generation fails
  - Includes detailed error messages from the OpenAI API
  - Properly logged for debugging

### Testing

The embedding system includes comprehensive tests covering:

1. Basic functionality:
   - Single text embedding generation
   - Multiple text embedding generation
   - Metadata handling

2. Error cases:
   - API errors
   - Bad requests
   - Connection issues

## Best Practices

1. Input Text:
   - Clean and preprocess text before generating embeddings
   - Keep text concise and relevant
   - Handle empty strings appropriately

2. Batch Processing:
   - Use the multiple text input feature for batch processing
   - Consider rate limits when processing large batches

3. Error Handling:
   - Always wrap embedding generation in try-except blocks
   - Log errors for debugging
   - Provide meaningful error messages to users

## Future Improvements

1. Memory Retrieval System:
   - Implement efficient similarity search
   - Add support for filtering and ranking

2. Memory Decay:
   - Implement time-based decay mechanisms
   - Add relevance scoring
