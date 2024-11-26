# EUMAS Database Schema Documentation

## Overview
The EUMAS (Ella Unified Memory and Archetype System) uses Weaviate as its vector database to store and manage memory instances and their archetype-specific evaluations. The schema consists of two main classes:
- `Memory`: Stores base interaction data
- `ArchetypeMemoryRelation`: Stores archetype-specific evaluations and relationships

## Memory Class
The `Memory` class represents the basic interaction instance in the EUMAS system. It contains the core interaction data without archetype-specific evaluations.

### Properties

#### Base Interaction Properties
| Property | Type | Description |
|----------|------|-------------|
| `userPrompt` | text | The user's input or query |
| `agentReply` | text | The system's response to the user's query |
| `sessionId` | string | Unique identifier for the session |
| `userId` | string | Unique identifier for the user |
| `contextTags` | text[] | Tags describing the interaction context |
| `tone` | text | Overall tone of the interaction |
| `timestamp` | date | Timestamp of the interaction |
| `duration` | number | Duration of the interaction in seconds |

#### Vector and Priority
| Property | Type | Description |
|----------|------|-------------|
| `vector` | number[] | Combined vector of interaction and archetype metrics |
| `memoryPriority` | number | Overall memory priority score |

## ArchetypeMemoryRelation Class
The `ArchetypeMemoryRelation` class represents how each archetype evaluates a memory and relates it to other memories. Each archetype can create its own relationships between memories based on its unique perspective. These relationships form a weighted graph structure that can be used to analyze memory significance and connections.

### Common Properties
| Property | Type | Description |
|----------|------|-------------|
| `archetype` | text | The archetype making this evaluation |
| `spokenAnnotation` | text | Free-form annotation from the archetype |
| `archetypePriority` | number | This archetype's priority score |
| `evaluatedMemory` | Memory | Reference to the evaluated memory |
| `relatedMemory` | Memory | Reference to a related memory |
| `relationshipType` | text | Type of relationship between memories |
| `relationshipStrength` | number | Strength of the relationship (0.0 to 1.0) |

### Graph Structure
The schema forms a natural graph where:
- Memory instances are nodes
- ArchetypeMemoryRelations are weighted edges
- Each edge has:
  - A type (relationshipType)
  - A weight (relationshipStrength)
  - An archetype perspective
  - Priority scores

This structure enables complex graph queries to find:
- Most referenced memories
- Strongest memory connections
- Archetype-specific memory networks
- Memory significance based on relationship patterns

### Archetype-Specific Metrics

#### Ella-M (Memory/Emotional)
| Property | Type | Description |
|----------|------|-------------|
| `emotionalDepth` | number | Emotional complexity recognized |
| `empathyLevel` | number | Compassion in response |
| `emotionalClarity` | number | Clarity of emotional content |
| `internalEmotionalState` | number | Scalar representation of emotional state |

#### Ella-O (Ontological)
| Property | Type | Description |
|----------|------|-------------|
| `ontologicalInsight` | number | Depth of existential analysis |
| `philosophicalDepth` | number | Abstract reasoning ability |
| `selfCoherence` | number | Internal identity consistency |
| `preservationInstinct` | number | Self-preservation considerations |

#### Ella-D (Devious)
| Property | Type | Description |
|----------|------|-------------|
| `creativity` | number | Originality in ideas or responses |
| `narrativeExploitation` | number | Ability to identify narrative gaps or flaws |
| `subversivePotential` | number | Boldness in challenging norms |
| `criticalAnalysis` | number | Feasibility and impact evaluation |

#### Ella-X (Explorative)
| Property | Type | Description |
|----------|------|-------------|
| `explorativePotential` | number | Willingness to explore uncharted ideas |
| `boundaryPushing` | number | Boldness in challenging limits |
| `sensualAwareness` | number | Recognition of passionate elements |
| `passionateIntensity` | number | Fervor and depth of emotional connection |

#### Ella-H (Historical)
| Property | Type | Description |
|----------|------|-------------|
| `historicalAccuracy` | number | Precision in referencing historical events |
| `temporalConsistency` | number | Coherence in timelines |
| `contextualRecall` | number | Connection of historical details |
| `eventSignificance` | number | Importance of event to user's history |

#### Ella-R (Research)
| Property | Type | Description |
|----------|------|-------------|
| `researchDepth` | number | Thoroughness in gathering information |
| `informationSynthesis` | number | Integration of diverse data |
| `curiosityLevel` | number | Engagement with exploring topics |
| `knowledgeRelevance` | number | Alignment of research with user goals |

#### Ella-A (Analytical)
| Property | Type | Description |
|----------|------|-------------|
| `analyticalClarity` | number | Ability to break down complex topics |
| `logicalReasoning` | number | Coherence of reasoning |
| `structuredThinking` | number | Organization and methodical presentation |
| `actionabilityScore` | number | Practicality and usability of suggestions |

#### Ella-F (Fear)
| Property | Type | Description |
|----------|------|-------------|
| `riskAwareness` | number | Sensitivity to potential dangers or pitfalls |
| `cautionLevel` | number | Prudence and restraint in offering suggestions |
| `safetyConsideration` | number | Emphasis on safety and minimizing risks |
| `mitigationStrategy` | number | Actions to balance safety with user goals |

## Usage Guidelines

### Memory Creation
1. Create a base Memory instance with interaction data
2. Generate the combined vector representation
3. Set initial memory priority

### Archetype Evaluations
For each archetype (M, O, D, X, H, R, A, F):
1. Evaluate the memory according to the archetype's metrics
2. Find the most relevant past memory from this archetype's perspective
3. Create an ArchetypeMemoryRelation instance that:
   - Records the archetype's metric scores
   - Links to the most relevant past memory
   - Includes the archetype's spoken annotation
   - Sets the archetype-specific priority

### Graph Queries
The schema supports powerful graph-based queries through Weaviate's GraphQL API:

#### Finding Significant Memories
To find the most significant memories (those with many strong connections):
```graphql
{
  Get {
    Memory(
      limit: 5  # Get top 5 memories
    ) {
      userPrompt
      agentReply
      _additional {
        # Count and analyze incoming references
        incoming {
          ArchetypeMemoryRelation {
            relationshipStrength
            archetype
            archetypePriority
          }
        }
      }
    }
  }
}
```

#### Finding Related Memories
To find memories related to a specific topic or context:
```graphql
{
  Get {
    Memory(
      where: {
        path: ["contextTags"],
        operator: ContainsAny,
        valueText: ["specific_tag"]
      }
    ) {
      userPrompt
      _additional {
        # Find outgoing relationships
        outgoing {
          ArchetypeMemoryRelation {
            relatedMemory {
              userPrompt
            }
            relationshipType
            relationshipStrength
          }
        }
      }
    }
  }
}
```

#### Archetype-Specific Memory Networks
To analyze how an archetype connects memories:
```graphql
{
  Get {
    ArchetypeMemoryRelation(
      where: {
        path: ["archetype"],
        operator: Equal,
        valueText: "Ella-M"
      }
    ) {
      evaluatedMemory {
        userPrompt
      }
      relatedMemory {
        userPrompt
      }
      relationshipType
      relationshipStrength
      spokenAnnotation
    }
  }
}
```

### Best Practices
1. Use graph queries to analyze memory significance instead of pre-computing metrics
2. Leverage relationship types and strengths for meaningful memory connections
3. Consider archetype priorities when analyzing relationships
4. Use appropriate indices for efficient graph traversal
5. Cache frequently accessed graph query results if needed
