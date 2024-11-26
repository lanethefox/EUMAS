"""Tests for the database schema module."""

from eumas.database.schema import (
    get_memory_class_schema,
    get_relationship_class_schema,
    MEMORY_CLASS_NAME,
    RELATIONSHIP_CLASS_NAME,
)


def test_memory_class_schema():
    """Test the Memory class schema structure."""
    schema = get_memory_class_schema()
    
    assert schema["class"] == MEMORY_CLASS_NAME
    assert schema["vectorizer"] == "none"
    assert schema["vectorIndexType"] == "hnsw"
    
    # Check required properties exist
    property_names = {prop["name"] for prop in schema["properties"]}
    required_properties = {
        "userPrompt",
        "agentReply",
        "sessionId",
        "userId",
        "contextTags",
        "tone",
        "timestamp",
        "duration",
        # Ella-M properties
        "emotionalDepth",
        "empathyLevel",
        "emotionalClarity",
        "internalEmotionalState",
        "ellaMAnnotation",
        # Ella-O properties
        "ontologicalInsight",
        "philosophicalDepth",
        "selfCoherence",
        "preservationInstinct",
        "ellaOAnnotation",
        # Prioritization
        "memoryPriority",
    }
    
    assert required_properties.issubset(property_names)


def test_relationship_class_schema():
    """Test the MemoryRelationship class schema structure."""
    schema = get_relationship_class_schema()
    
    assert schema["class"] == RELATIONSHIP_CLASS_NAME
    assert schema["vectorizer"] == "none"
    
    # Check required properties exist
    property_names = {prop["name"] for prop in schema["properties"]}
    required_properties = {
        "type",
        "strength",
        "sourceMemory",
        "targetMemory",
        "archetype",
    }
    
    assert required_properties.issubset(property_names)
    
    # Check cross-references
    memory_refs = [
        prop for prop in schema["properties"]
        if prop["name"] in ["sourceMemory", "targetMemory"]
    ]
    for ref in memory_refs:
        assert ref["dataType"] == ["Memory"]
