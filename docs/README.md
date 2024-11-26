# EUMAS Documentation

This directory contains the documentation for the Ella Unified Memory and Archetype System (EUMAS). The documentation is organized by component and functionality.

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Components](#components)
4. [Development Guide](#development-guide)

## Project Overview

EUMAS (Ella Unified Memory and Archetype System) is a sophisticated system designed to manage and process conversational memories using vector embeddings and archetype-based evaluation. The system integrates with OpenAI's API for embedding generation and Weaviate for vector storage.

## System Architecture

### Core Components
- **Embedding System**: Converts text to vector representations
- **Database Layer**: Manages persistent storage using Weaviate
- **Error Handling**: Custom exception hierarchy
- **Logging**: Structured logging with JSON support

### Directory Structure
```
eumas/
├── src/
│   └── eumas/
│       ├── embeddings/     # Embedding generation and management
│       ├── database/       # Database connection and operations
│       └── utils/          # Common utilities and helpers
├── tests/                  # Test suite
└── docs/                   # Documentation
```

## Components

### Currently Implemented

1. [Embedding System](./embedding-system.md)
   - Vector generation for text
   - Batch processing support
   - Metadata handling
   - Comprehensive error handling

2. [Error Handling](./error-handling.md)
   - Custom exception hierarchy
   - Structured error logging
   - Error code management

3. [Database Connection](./database-connection.md)
   - Weaviate integration
   - Connection management
   - Health checks

## Development Guide

### Environment Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Required environment variables
OPENAI_API_KEY=your-api-key
WEAVIATE_URL=your-weaviate-url
```

### Running Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src/eumas
```

### Code Style

The project follows PEP 8 guidelines with some modifications:
- Line length: 88 characters (Black formatter)
- Import ordering: isort
- Type hints: Required for all public functions and methods
