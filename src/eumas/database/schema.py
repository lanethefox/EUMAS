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
            # Archetype metrics - Ella-M (Memory/Emotional)
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
            # Ella-O (Ontological) metrics
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
            # Ella-R (Rational) metrics
            {
                "name": "logicalCoherence",
                "dataType": ["number"],
                "description": "Measure of logical consistency by Ella-R"
            },
            {
                "name": "analyticalDepth",
                "dataType": ["number"],
                "description": "Depth of analytical reasoning by Ella-R"
            },
            {
                "name": "factualAccuracy",
                "dataType": ["number"],
                "description": "Assessment of factual correctness by Ella-R"
            },
            {
                "name": "problemSolvingEfficiency",
                "dataType": ["number"],
                "description": "Efficiency in problem-solving approach by Ella-R"
            },
            {
                "name": "ellaRAnnotation",
                "dataType": ["text"],
                "description": "Free-form annotation from Ella-R"
            },
            # Ella-C (Creative) metrics
            {
                "name": "creativityLevel",
                "dataType": ["number"],
                "description": "Level of creative thinking by Ella-C"
            },
            {
                "name": "innovationScore",
                "dataType": ["number"],
                "description": "Assessment of innovative ideas by Ella-C"
            },
            {
                "name": "aestheticValue",
                "dataType": ["number"],
                "description": "Aesthetic quality evaluation by Ella-C"
            },
            {
                "name": "divergentThinking",
                "dataType": ["number"],
                "description": "Measure of non-conventional thinking by Ella-C"
            },
            {
                "name": "ellaCAnnotation",
                "dataType": ["text"],
                "description": "Free-form annotation from Ella-C"
            },
            # Ella-S (Social) metrics
            {
                "name": "socialAwareness",
                "dataType": ["number"],
                "description": "Understanding of social dynamics by Ella-S"
            },
            {
                "name": "culturalSensitivity",
                "dataType": ["number"],
                "description": "Cultural awareness and adaptation by Ella-S"
            },
            {
                "name": "interpersonalEffectiveness",
                "dataType": ["number"],
                "description": "Effectiveness in social interactions by Ella-S"
            },
            {
                "name": "communicationClarity",
                "dataType": ["number"],
                "description": "Clarity of social communication by Ella-S"
            },
            {
                "name": "ellaSAnnotation",
                "dataType": ["text"],
                "description": "Free-form annotation from Ella-S"
            },
            # Ella-E (Ethical) metrics
            {
                "name": "ethicalAwareness",
                "dataType": ["number"],
                "description": "Recognition of ethical implications by Ella-E"
            },
            {
                "name": "moralConsistency",
                "dataType": ["number"],
                "description": "Consistency in moral reasoning by Ella-E"
            },
            {
                "name": "valueAlignment",
                "dataType": ["number"],
                "description": "Alignment with core values by Ella-E"
            },
            {
                "name": "responsibleDecisionMaking",
                "dataType": ["number"],
                "description": "Assessment of decision responsibility by Ella-E"
            },
            {
                "name": "ellaEAnnotation",
                "dataType": ["text"],
                "description": "Free-form annotation from Ella-E"
            },
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
