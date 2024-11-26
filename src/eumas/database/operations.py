"""Database operations for EUMAS, including graph queries and memory analysis."""

from typing import Dict, List, Optional, Tuple
from datetime import datetime

import weaviate
from weaviate.gql.get import GetBuilder

from eumas.database.schema import (
    Memory,
    ArchetypeMemoryRelation,
    MEMORY_CLASS,
    ARCHETYPE_MEMORY_RELATION_CLASS,
    ARCHETYPES,
)


class MemoryOperations:
    """Handles memory storage and retrieval operations."""

    def __init__(self, client: weaviate.Client):
        """Initialize with a Weaviate client."""
        self.client = client
        self.graphql = client.query.get

    def store_memory(self, memory: Memory) -> str:
        """Store a new memory in the database.
        
        Args:
            memory: Memory instance to store
            
        Returns:
            str: UUID of the stored memory
        """
        return self.client.data_object.create(
            memory.to_weaviate_object()
        )

    def store_memory_relation(self, relation: ArchetypeMemoryRelation) -> str:
        """Store a new memory relation in the database.
        
        Args:
            relation: ArchetypeMemoryRelation instance to store
            
        Returns:
            str: UUID of the stored relation
        """
        return self.client.data_object.create(
            relation.to_weaviate_object()
        )

    def store_memories_batch(self, memories: List[Memory]) -> List[str]:
        """Store multiple memories in batch for better performance.
        
        Args:
            memories: List of Memory instances to store
            
        Returns:
            List[str]: UUIDs of the stored memories
        """
        with self.client.batch as batch:
            batch.configure(batch_size=100, dynamic=True)
            uuids = []
            for memory in memories:
                uuid = batch.add_data_object(
                    memory.to_weaviate_object()
                )
                uuids.append(uuid)
            return uuids

    def store_relations_batch(self, relations: List[ArchetypeMemoryRelation]) -> List[str]:
        """Store multiple memory relations in batch for better performance.
        
        Args:
            relations: List of ArchetypeMemoryRelation instances to store
            
        Returns:
            List[str]: UUIDs of the stored relations
        """
        with self.client.batch as batch:
            batch.configure(batch_size=100, dynamic=True)
            uuids = []
            for relation in relations:
                uuid = batch.add_data_object(
                    relation.to_weaviate_object()
                )
                uuids.append(uuid)
            return uuids

    def get_significant_memories(
        self,
        limit: int = 5,
        min_relationship_strength: float = 0.0,
        archetype_filter: Optional[str] = None
    ) -> List[Dict]:
        """Get the most significant memories based on their relationships.
        
        Args:
            limit: Maximum number of memories to return
            min_relationship_strength: Minimum strength threshold for relationships
            archetype_filter: Optional archetype to filter relationships by
            
        Returns:
            List[Dict]: List of memories with their relationship metrics
        """
        # Build relationship filter
        where_filter = {
            "path": ["relationshipStrength"],
            "operator": "GreaterThan",
            "valueNumber": min_relationship_strength
        }
        
        if archetype_filter:
            if archetype_filter not in ARCHETYPES:
                raise ValueError(f"Invalid archetype: {archetype_filter}")
            where_filter = {
                "operator": "And",
                "operands": [
                    where_filter,
                    {
                        "path": ["archetype"],
                        "operator": "Equal",
                        "valueString": archetype_filter
                    }
                ]
            }

        # Build GraphQL query
        query = (
            self.graphql
            .get(MEMORY_CLASS)
            .with_limit(limit)
            .with_fields(
                "userPrompt",
                "agentReply",
                "contextTags",
                "timestamp",
                "_additional { id }"
            )
            .with_additional(
                "incoming { "
                f"  {ARCHETYPE_MEMORY_RELATION_CLASS} {{ "
                "    relationshipStrength "
                "    archetype "
                "    archetypePriority "
                "    spokenAnnotation "
                "  }} "
                "}"
            )
        )

        result = query.do()
        return result.get("data", {}).get("Get", {}).get(MEMORY_CLASS, [])

    def get_memory_network(
        self,
        memory_id: str,
        max_depth: int = 2,
        min_strength: float = 0.5
    ) -> Dict:
        """Get the network of memories connected to a given memory.
        
        Args:
            memory_id: UUID of the source memory
            max_depth: Maximum depth of relationships to traverse
            min_strength: Minimum relationship strength to include
            
        Returns:
            Dict: Network of related memories and their relationships
        """
        # Build recursive GraphQL query
        fields = [
            "userPrompt",
            "agentReply",
            "contextTags",
            "_additional { id }",
            f"incoming {{ {ARCHETYPE_MEMORY_RELATION_CLASS} {{ "
            "  relationshipStrength "
            "  archetype "
            "  archetypePriority "
            "  spokenAnnotation "
            "  evaluatedMemory { "
            "    ... on Memory { "
            "      userPrompt "
            "      _additional { id } "
            "    } "
            "  } "
            "} }}",
            f"outgoing {{ {ARCHETYPE_MEMORY_RELATION_CLASS} {{ "
            "  relationshipStrength "
            "  archetype "
            "  archetypePriority "
            "  spokenAnnotation "
            "  relatedMemory { "
            "    ... on Memory { "
            "      userPrompt "
            "      _additional { id } "
            "    } "
            "  } "
            "} }}"
        ]

        query = (
            self.graphql
            .get(MEMORY_CLASS)
            .with_id(memory_id)
            .with_fields(*fields)
        )

        result = query.do()
        return result.get("data", {}).get("Get", {}).get(MEMORY_CLASS, [])

    def get_archetype_perspective(
        self,
        archetype: str,
        context_tag: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Get memories and their relationships from a specific archetype's perspective.
        
        Args:
            archetype: The archetype to analyze (e.g., "Ella-M")
            context_tag: Optional context tag to filter memories
            limit: Maximum number of memories to return
            
        Returns:
            List[Dict]: Memories and their relationships from the archetype's perspective
        """
        if archetype not in ARCHETYPES:
            raise ValueError(f"Invalid archetype: {archetype}")

        # Build memory filter
        where_filter = None
        if context_tag:
            where_filter = {
                "path": ["contextTags"],
                "operator": "ContainsAny",
                "valueTextArray": [context_tag]
            }

        # Build GraphQL query
        query = (
            self.graphql
            .get(ARCHETYPE_MEMORY_RELATION_CLASS)
            .with_fields(
                "relationshipStrength",
                "relationshipType",
                "spokenAnnotation",
                "archetypePriority",
                "evaluatedMemory { "
                "  ... on Memory { "
                "    userPrompt "
                "    contextTags "
                "    timestamp "
                "    _additional { id } "
                "  } "
                "}",
                "relatedMemory { "
                "  ... on Memory { "
                "    userPrompt "
                "    contextTags "
                "    timestamp "
                "    _additional { id } "
                "  } "
                "}"
            )
            .with_where({
                "path": ["archetype"],
                "operator": "Equal",
                "valueString": archetype
            })
            .with_limit(limit)
        )

        if where_filter:
            query = query.with_where({
                "operator": "And",
                "operands": [
                    query._where,  # type: ignore
                    where_filter
                ]
            })

        result = query.do()
        return result.get("data", {}).get("Get", {}).get(ARCHETYPE_MEMORY_RELATION_CLASS, [])

    def get_memories_by_timerange(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100
    ) -> List[Dict]:
        """Get memories within a specific time range.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            limit: Maximum number of memories to return
            
        Returns:
            List[Dict]: List of memories within the time range
        """
        query = (
            self.graphql
            .get(MEMORY_CLASS)
            .with_where({
                "operator": "And",
                "operands": [
                    {
                        "path": ["timestamp"],
                        "operator": "GreaterThanEqual",
                        "valueDate": start_time.isoformat()
                    },
                    {
                        "path": ["timestamp"],
                        "operator": "LessThanEqual",
                        "valueDate": end_time.isoformat()
                    }
                ]
            })
            .with_fields(
                "userPrompt",
                "agentReply",
                "contextTags",
                "timestamp",
                "memoryPriority",
                "_additional { id }"
            )
            .with_limit(limit)
        )

        result = query.do()
        return result.get("data", {}).get("Get", {}).get(MEMORY_CLASS, [])

    def get_memories_by_context(
        self,
        context_tags: List[str],
        min_priority: float = 0.0,
        limit: int = 100
    ) -> List[Dict]:
        """Get memories matching specific context tags and minimum priority.
        
        Args:
            context_tags: List of context tags to match
            min_priority: Minimum memory priority threshold
            limit: Maximum number of memories to return
            
        Returns:
            List[Dict]: List of matching memories
        """
        query = (
            self.graphql
            .get(MEMORY_CLASS)
            .with_where({
                "operator": "And",
                "operands": [
                    {
                        "path": ["contextTags"],
                        "operator": "ContainsAny",
                        "valueTextArray": context_tags
                    },
                    {
                        "path": ["memoryPriority"],
                        "operator": "GreaterThanEqual",
                        "valueNumber": min_priority
                    }
                ]
            })
            .with_fields(
                "userPrompt",
                "agentReply",
                "contextTags",
                "timestamp",
                "memoryPriority",
                "_additional { id }"
            )
            .with_limit(limit)
            .with_additional("score")
        )

        result = query.do()
        return result.get("data", {}).get("Get", {}).get(MEMORY_CLASS, [])
