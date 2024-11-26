"""Tests for the embedding generator module."""

from dataclasses import dataclass
from typing import List
from unittest import mock

import pytest
from openai import OpenAIError, BadRequestError
from openai.types import CreateEmbeddingResponse, Embedding

from eumas.embeddings.generator import EmbeddingGenerator
from eumas.utils.errors import EmbeddingError


@dataclass
class MockEmbeddingData:
    """Mock OpenAI embedding data response."""
    embedding: List[float]
    index: int = 0
    object: str = "embedding"


@dataclass
class MockEmbeddingResponse:
    """Mock OpenAI embedding response."""
    data: List[MockEmbeddingData]
    model: str
    object: str = "list"
    usage: dict = None

    def __post_init__(self):
        if self.usage is None:
            self.usage = {"prompt_tokens": 8, "total_tokens": 8}


@pytest.fixture
def mock_openai():
    """Mock OpenAI API responses."""
    with mock.patch("eumas.embeddings.generator.OpenAI") as mock_client:
        # Create mock embedding vector of correct size (1536)
        mock_embedding = [0.1] * 1536

        # Mock response data
        mock_response = MockEmbeddingResponse(
            data=[
                MockEmbeddingData(embedding=mock_embedding, index=0),
                MockEmbeddingData(embedding=mock_embedding, index=1),
            ],
            model="text-embedding-ada-002",
        )

        # Create mock client instance with embeddings property
        mock_instance = mock.MagicMock()
        mock_instance.embeddings.create.return_value = mock_response
        mock_client.return_value = mock_instance

        yield mock_client


def test_embedding_generator_init():
    """Test EmbeddingGenerator initialization."""
    generator = EmbeddingGenerator()
    assert generator.model == "text-embedding-ada-002"

    generator = EmbeddingGenerator(model="custom-model")
    assert generator.model == "custom-model"


def test_generate_single_text(mock_openai):
    """Test generating embeddings for a single text."""
    generator = EmbeddingGenerator()
    embedding = generator.generate("test text")
    
    assert isinstance(embedding, list)
    assert len(embedding) == 1536  # OpenAI's embedding dimension
    assert all(isinstance(x, float) for x in embedding)
    
    mock_instance = mock_openai.return_value
    mock_instance.embeddings.create.assert_called_once_with(
        input=["test text"],
        model="text-embedding-ada-002"
    )


def test_generate_multiple_texts(mock_openai):
    """Test generating embeddings for multiple texts."""
    generator = EmbeddingGenerator()
    texts = ["text1", "text2"]
    embeddings = generator.generate(texts)
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == 2
    assert all(isinstance(x, list) for x in embeddings)
    assert all(len(x) == 1536 for x in embeddings)  # OpenAI's embedding dimension
    
    mock_instance = mock_openai.return_value
    mock_instance.embeddings.create.assert_called_once_with(
        input=texts,
        model="text-embedding-ada-002"
    )


def test_generate_with_metadata():
    """Test generating embeddings with metadata."""
    generator = EmbeddingGenerator()
    
    with mock.patch.object(generator, "generate") as mock_generate:
        mock_embedding = [0.1] * 1536  # OpenAI's embedding dimension
        mock_generate.return_value = mock_embedding
        
        result = generator.generate_with_metadata(
            "test text",
            metadata={"source": "test"}
        )
        
        assert result == {
            "embedding": mock_embedding,
            "text": "test text",
            "metadata": {"source": "test"},
            "model": "text-embedding-ada-002"
        }


def test_generate_error():
    """Test handling of API errors."""
    with mock.patch("eumas.embeddings.generator.OpenAI") as mock_client:
        mock_instance = mock.MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.embeddings.create.side_effect = OpenAIError("API error")

        generator = EmbeddingGenerator()
        with pytest.raises(EmbeddingError) as exc_info:
            generator.generate("test text")
        
        assert "Failed to generate embeddings" in str(exc_info.value)


def test_generate_bad_request():
    """Test handling of bad request errors."""
    with mock.patch("eumas.embeddings.generator.OpenAI") as mock_client:
        mock_instance = mock.MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.embeddings.create.side_effect = BadRequestError(
            message="Bad request",
            response=mock.MagicMock(status_code=400),
            body={"error": {"message": "Bad request"}}
        )

        generator = EmbeddingGenerator()
        with pytest.raises(EmbeddingError) as exc_info:
            generator.generate("")
        
        assert "Failed to generate embeddings" in str(exc_info.value)
