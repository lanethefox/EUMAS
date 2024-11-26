"""
Module for generating embeddings using OpenAI's API.
"""

from typing import List, Union, Dict, Any

from openai import OpenAI
from loguru import logger

from eumas.utils.errors import EmbeddingError


class EmbeddingGenerator:
    """Class for generating embeddings using OpenAI's API."""

    def __init__(self, model: str = "text-embedding-ada-002"):
        """Initialize the embedding generator.

        Args:
            model (str): The OpenAI model to use for generating embeddings.
                Defaults to "text-embedding-ada-002".
        """
        self.model = model
        self.client = OpenAI()

    def generate(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Generate embeddings for the given text(s).

        Args:
            text (Union[str, List[str]]): The text(s) to generate embeddings for.
                Can be a single string or a list of strings.

        Returns:
            Union[List[float], List[List[float]]]: The generated embeddings.
                If input is a single string, returns a single embedding vector.
                If input is a list of strings, returns a list of embedding vectors.

        Raises:
            EmbeddingError: If the embedding generation fails.
        """
        try:
            # Convert single string to list for consistent handling
            texts = [text] if isinstance(text, str) else text

            # Generate embeddings using OpenAI API
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )

            # Extract embeddings from response
            embeddings = [data.embedding for data in response.data]

            # Return single embedding if input was single string
            return embeddings[0] if isinstance(text, str) else embeddings

        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            raise EmbeddingError(f"Failed to generate embeddings: {str(e)}")

    def generate_with_metadata(
        self,
        text: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate embeddings for text and include metadata.

        Args:
            text (str): The text to generate embeddings for.
            metadata (Dict[str, Any], optional): Additional metadata to include.
                Defaults to None.

        Returns:
            Dict[str, Any]: Dictionary containing the embedding, text, metadata,
                and model information.
        """
        embedding = self.generate(text)
        return {
            "embedding": embedding,
            "text": text,
            "metadata": metadata or {},
            "model": self.model
        }
