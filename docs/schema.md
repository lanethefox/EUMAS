# EUMAS Database Schema Documentation

## Overview
The EUMAS (Ella Unified Memory and Archetype System) uses Weaviate as its vector database to store and manage memory instances and their relationships. The schema consists of two main classes: `Memory` and `MemoryRelationship`.

## Memory Class
The `Memory` class represents individual memory instances in the EUMAS system. Each memory captures interaction details, archetype-specific metrics, and prioritization data.

### Basic Properties

#### Interaction Properties
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

### Archetype-Specific Metrics

#### Ella-M (Emotional) Metrics
| Property | Type | Description |
|----------|------|-------------|
| `emotionalDepth` | number | Measures the emotional complexity recognized |
| `empathyLevel` | number | Quantifies the compassion in response |
| `emotionalClarity` | number | Measures clarity of emotional content |
| `internalEmotionalState` | number | Scalar representation of emotional state |
| `ellaMAnnotation` | text | Free-form annotation from Ella-M |

#### Ella-O (Ontological) Metrics
| Property | Type | Description |
|----------|------|-------------|
| `ontologicalInsight` | number | Depth of existential analysis |
| `philosophicalDepth` | number | Abstract reasoning ability |
| `selfCoherence` | number | Internal identity consistency |
| `preservationInstinct` | number | Self-preservation considerations |
| `ellaOAnnotation` | text | Free-form annotation from Ella-O |

### Memory Prioritization
| Property | Type | Description |
|----------|------|-------------|
| `memoryPriority` | number | Overall memory priority score |

## MemoryRelationship Class
The `MemoryRelationship` class represents connections between memory instances, allowing for a rich network of interconnected memories.

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `type` | text | Type of relationship between memories |
| `strength` | number | Strength of the relationship (0.0 to 1.0) |
| `sourceMemory` | Memory | Reference to the source memory |
| `targetMemory` | Memory | Reference to the target memory |
| `archetype` | text | The archetype that created this relationship |

## Vector Configuration
- Both classes use `"vectorizer": "none"`, indicating that vectors are provided externally
- The Memory class uses HNSW (Hierarchical Navigable Small World) for vector indexing
- Vector dimensions and other specific configurations are handled at the application level

## Usage Guidelines

### Memory Creation
When creating a new memory:
1. Ensure all required fields are populated
2. Calculate archetype-specific metrics
3. Generate appropriate embeddings
4. Set a meaningful memory priority

### Relationship Management
When creating relationships:
1. Specify meaningful relationship types
2. Calculate relationship strength based on context
3. Ensure both source and target memories exist
4. Record which archetype created the relationship

### Best Practices
1. Always include session and user IDs for traceability
2. Use consistent context tags for better querying
3. Keep annotations concise and meaningful
4. Regularly update memory priorities based on usage patterns
5. Maintain balanced relationship graphs to prevent isolated memories