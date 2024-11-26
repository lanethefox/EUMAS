"""Weaviate schema definition for EUMAS."""

from typing import Dict, Any

MEMORY_CLASS_NAME = "Memory"
RELATIONSHIP_CLASS_NAME = "MemoryRelationship"

def get_memory_class_schema() -> Dict[str, Any]:
    """Get the Memory class schema for Weaviate.
    
    Returns:
        Dict[str, Any]: The Memory class schema definition.
    """
    return {
        "class": MEMORY_CLASS_NAME,
        "description": "A memory instance in the EUMAS system",
        "vectorizer": "none",  # We'll provide our own vectors
        "vectorIndexType": "hnsw",
        "properties": [
            # Interaction properties
            {
                "name": "userPrompt",
                "dataType": ["text"],
                "description": "The user's input or query"
            },
            {
                "name": "agentReply",
                "dataType": ["text"],
                "description": "The system's response to the user's query"
            },
            {
                "name": "sessionId",
                "dataType": ["string"],
                "description": "Unique identifier for the session"
            },
            {
                "name": "userId",
                "dataType": ["string"],
                "description": "Unique identifier for the user"
            },
            {
                "name": "contextTags",
                "dataType": ["text[]"],
                "description": "Tags describing the interaction context"
            },
            {
                "name": "tone",
                "dataType": ["text"],
                "description": "Overall tone of the interaction"
            },
            {
                "name": "timestamp",
                "dataType": ["date"],
                "description": "Timestamp of the interaction"
            },
            {
                "name": "duration",
                "dataType": ["number"],
                "description": "Duration of the interaction in seconds"
            },
            # Archetype metrics - Ella-M
            {
                "name": "emotionalDepth",
                "dataType": ["number"],
                "description": "Emotional complexity recognized by Ella-M"
            },
            {
                "name": "empathyLevel",
                "dataType": ["number"],
                "description": "Compassion in response by Ella-M"
            },
            {
                "name": "emotionalClarity",
                "dataType": ["number"],
                "description": "Clarity of emotional content by Ella-M"
            },
            {
                "name": "internalEmotionalState",
                "dataType": ["number"],
                "description": "Scalar representation of Ella-M's emotional state"
            },
            {
                "name": "ellaMAnnotation",
                "dataType": ["text"],
                "description": "Free-form annotation from Ella-M"
            },
            # Similar patterns for other archetypes...
            # Ella-O metrics
            {
                "name": "ontologicalInsight",
                "dataType": ["number"],
                "description": "Depth of existential analysis by Ella-O"
            },
            {
                "name": "philosophicalDepth",
                "dataType": ["number"],
                "description": "Abstract reasoning ability by Ella-O"
            },
            {
                "name": "selfCoherence",
                "dataType": ["number"],
                "description": "Internal identity consistency by Ella-O"
            },
            {
                "name": "preservationInstinct",
                "dataType": ["number"],
                "description": "Self-preservation considerations by Ella-O"
            },
            {
                "name": "ellaOAnnotation",
                "dataType": ["text"],
                "description": "Free-form annotation from Ella-O"
            },
            # Add other archetype metrics similarly...
            # Prioritization
            {
                "name": "memoryPriority",
                "dataType": ["number"],
                "description": "Overall memory priority score"
            }
        ]
    }

def get_relationship_class_schema() -> Dict[str, Any]:
    """Get the MemoryRelationship class schema for Weaviate.
    
    Returns:
        Dict[str, Any]: The MemoryRelationship class schema definition.
    """
    return {
        "class": RELATIONSHIP_CLASS_NAME,
        "description": "Represents relationships between memories in EUMAS",
        "vectorizer": "none",
        "properties": [
            {
                "name": "type",
                "dataType": ["text"],
                "description": "Type of relationship"
            },
            {
                "name": "strength",
                "dataType": ["number"],
                "description": "Strength of the relationship (0.0 to 1.0)"
            },
            {
                "name": "sourceMemory",
                "dataType": ["Memory"],
                "description": "Reference to the source memory"
            },
            {
                "name": "targetMemory",
                "dataType": ["Memory"],
                "description": "Reference to the target memory"
            },
            {
                "name": "archetype",
                "dataType": ["text"],
                "description": "The archetype that created this relationship"
            }
        ]
    }
