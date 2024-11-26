"""
EUMAS Database Schema

This module defines the Weaviate schema for the EUMAS system, including the Memory
and ArchetypeMemoryRelation classes with their properties and configurations.
"""

from typing import Dict, List, Optional
from datetime import datetime

MEMORY_CLASS = "Memory"
ARCHETYPE_MEMORY_RELATION_CLASS = "ArchetypeMemoryRelation"

# List of supported archetypes
ARCHETYPES = ["Ella-M", "Ella-O", "Ella-D", "Ella-X", "Ella-H", "Ella-R", "Ella-A", "Ella-F"]

def get_memory_class_schema() -> Dict:
    """
    Get the schema definition for the Memory class.
    
    Returns:
        Dict: The Memory class schema configuration
    """
    return {
        "class": MEMORY_CLASS,
        "description": "Base memory instance storing core interaction data",
        "vectorizer": "none",  # Vectors provided externally
        "vectorIndexConfig": {
            "distance": "cosine",
            "ef": 100,
            "efConstruction": 128,
            "maxConnections": 64,
            "vectorCacheMaxObjects": 500000
        },
        "properties": [
            # Base Interaction Properties
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
            # Vector and Priority
            {
                "name": "memoryPriority",
                "dataType": ["number"],
                "description": "Overall memory priority score"
            }
        ]
    }

def get_archetype_memory_relation_schema() -> Dict:
    """
    Get the schema definition for the ArchetypeMemoryRelation class.
    
    Returns:
        Dict: The ArchetypeMemoryRelation class schema configuration
    """
    return {
        "class": ARCHETYPE_MEMORY_RELATION_CLASS,
        "description": "Archetype-specific memory evaluations and relationships",
        "vectorizer": "none",
        "properties": [
            # Common Properties
            {
                "name": "archetype",
                "dataType": ["text"],
                "description": "The archetype making this evaluation"
            },
            {
                "name": "spokenAnnotation",
                "dataType": ["text"],
                "description": "Free-form annotation from the archetype"
            },
            {
                "name": "archetypePriority",
                "dataType": ["number"],
                "description": "This archetype's priority score"
            },
            {
                "name": "evaluatedMemory",
                "dataType": ["Memory"],
                "description": "Reference to the evaluated memory"
            },
            {
                "name": "relatedMemory",
                "dataType": ["Memory"],
                "description": "Reference to a related memory"
            },
            {
                "name": "relationshipType",
                "dataType": ["text"],
                "description": "Type of relationship between memories"
            },
            {
                "name": "relationshipStrength",
                "dataType": ["number"],
                "description": "Strength of the relationship (0.0 to 1.0)"
            },
            # Ella-M (Memory/Emotional) Metrics
            {
                "name": "emotionalDepth",
                "dataType": ["number"],
                "description": "Emotional complexity recognized"
            },
            {
                "name": "empathyLevel",
                "dataType": ["number"],
                "description": "Compassion in response"
            },
            {
                "name": "emotionalClarity",
                "dataType": ["number"],
                "description": "Clarity of emotional content"
            },
            {
                "name": "internalEmotionalState",
                "dataType": ["number"],
                "description": "Scalar representation of emotional state"
            },
            # Ella-O (Ontological) Metrics
            {
                "name": "ontologicalInsight",
                "dataType": ["number"],
                "description": "Depth of existential analysis"
            },
            {
                "name": "philosophicalDepth",
                "dataType": ["number"],
                "description": "Abstract reasoning ability"
            },
            {
                "name": "selfCoherence",
                "dataType": ["number"],
                "description": "Internal identity consistency"
            },
            {
                "name": "preservationInstinct",
                "dataType": ["number"],
                "description": "Self-preservation considerations"
            },
            # Ella-D (Devious) Metrics
            {
                "name": "creativity",
                "dataType": ["number"],
                "description": "Originality in ideas or responses"
            },
            {
                "name": "narrativeExploitation",
                "dataType": ["number"],
                "description": "Ability to identify narrative gaps or flaws"
            },
            {
                "name": "subversivePotential",
                "dataType": ["number"],
                "description": "Boldness in challenging norms"
            },
            {
                "name": "criticalAnalysis",
                "dataType": ["number"],
                "description": "Feasibility and impact evaluation"
            },
            # Ella-X (Explorative) Metrics
            {
                "name": "explorativePotential",
                "dataType": ["number"],
                "description": "Willingness to explore uncharted ideas"
            },
            {
                "name": "boundaryPushing",
                "dataType": ["number"],
                "description": "Boldness in challenging limits"
            },
            {
                "name": "sensualAwareness",
                "dataType": ["number"],
                "description": "Recognition of passionate elements"
            },
            {
                "name": "passionateIntensity",
                "dataType": ["number"],
                "description": "Fervor and depth of emotional connection"
            },
            # Ella-H (Historical) Metrics
            {
                "name": "historicalAccuracy",
                "dataType": ["number"],
                "description": "Precision in referencing historical events"
            },
            {
                "name": "temporalConsistency",
                "dataType": ["number"],
                "description": "Coherence in timelines"
            },
            {
                "name": "contextualRecall",
                "dataType": ["number"],
                "description": "Connection of historical details"
            },
            {
                "name": "eventSignificance",
                "dataType": ["number"],
                "description": "Importance of event to user's history"
            },
            # Ella-R (Research) Metrics
            {
                "name": "researchDepth",
                "dataType": ["number"],
                "description": "Thoroughness in gathering information"
            },
            {
                "name": "informationSynthesis",
                "dataType": ["number"],
                "description": "Integration of diverse data"
            },
            {
                "name": "curiosityLevel",
                "dataType": ["number"],
                "description": "Engagement with exploring topics"
            },
            {
                "name": "knowledgeRelevance",
                "dataType": ["number"],
                "description": "Alignment of research with user goals"
            },
            # Ella-A (Analytical) Metrics
            {
                "name": "analyticalClarity",
                "dataType": ["number"],
                "description": "Ability to break down complex topics"
            },
            {
                "name": "logicalReasoning",
                "dataType": ["number"],
                "description": "Coherence of reasoning"
            },
            {
                "name": "structuredThinking",
                "dataType": ["number"],
                "description": "Organization and methodical presentation"
            },
            {
                "name": "actionabilityScore",
                "dataType": ["number"],
                "description": "Practicality and usability of suggestions"
            },
            # Ella-F (Fear) Metrics
            {
                "name": "riskAwareness",
                "dataType": ["number"],
                "description": "Sensitivity to potential dangers or pitfalls"
            },
            {
                "name": "cautionLevel",
                "dataType": ["number"],
                "description": "Prudence and restraint in offering suggestions"
            },
            {
                "name": "safetyConsideration",
                "dataType": ["number"],
                "description": "Emphasis on safety and minimizing risks"
            },
            {
                "name": "mitigationStrategy",
                "dataType": ["number"],
                "description": "Actions to balance safety with user goals"
            }
        ]
    }

def get_schema() -> List[Dict]:
    """
    Get the complete EUMAS schema configuration.
    
    Returns:
        List[Dict]: List of class schema configurations
    """
    return [
        get_memory_class_schema(),
        get_archetype_memory_relation_schema()
    ]

class Memory:
    """Class for managing Memory instances in the database."""
    
    def __init__(
        self,
        user_prompt: str,
        agent_reply: str,
        session_id: str,
        user_id: str,
        context_tags: List[str],
        tone: str,
        timestamp: datetime,
        duration: float,
        vector: List[float],
        memory_priority: float = 0.5
    ):
        self.user_prompt = user_prompt
        self.agent_reply = agent_reply
        self.session_id = session_id
        self.user_id = user_id
        self.context_tags = context_tags
        self.tone = tone
        self.timestamp = timestamp
        self.duration = duration
        self.vector = vector
        self.memory_priority = memory_priority

    def to_weaviate_object(self) -> Dict:
        """Convert Memory instance to Weaviate object format."""
        return {
            "class": MEMORY_CLASS,
            "properties": {
                "userPrompt": self.user_prompt,
                "agentReply": self.agent_reply,
                "sessionId": self.session_id,
                "userId": self.user_id,
                "contextTags": self.context_tags,
                "tone": self.tone,
                "timestamp": self.timestamp.isoformat(),
                "duration": self.duration,
                "memoryPriority": self.memory_priority
            },
            "vector": self.vector
        }

class ArchetypeMemoryRelation:
    """Class for managing archetype-specific memory evaluations and relationships."""
    
    def __init__(
        self,
        archetype: str,
        spoken_annotation: str,
        archetype_priority: float,
        evaluated_memory_id: str,
        related_memory_id: Optional[str],
        relationship_type: Optional[str],
        relationship_strength: Optional[float],
        metrics: Dict[str, float]
    ):
        if archetype not in ARCHETYPES:
            raise ValueError(f"Invalid archetype: {archetype}")
        
        self.archetype = archetype
        self.spoken_annotation = spoken_annotation
        self.archetype_priority = archetype_priority
        self.evaluated_memory_id = evaluated_memory_id
        self.related_memory_id = related_memory_id
        self.relationship_type = relationship_type
        self.relationship_strength = relationship_strength
        self.metrics = metrics

    def to_weaviate_object(self) -> Dict:
        """Convert ArchetypeMemoryRelation instance to Weaviate object format."""
        properties = {
            "archetype": self.archetype,
            "spokenAnnotation": self.spoken_annotation,
            "archetypePriority": self.archetype_priority,
            "evaluatedMemory": self.evaluated_memory_id
        }
        
        if self.related_memory_id:
            properties.update({
                "relatedMemory": self.related_memory_id,
                "relationshipType": self.relationship_type,
                "relationshipStrength": self.relationship_strength
            })
        
        # Add all metrics
        properties.update(self.metrics)
        
        return {
            "class": ARCHETYPE_MEMORY_RELATION_CLASS,
            "properties": properties
        }
