The v4 Weaviate Python client API is a complete rewrite, aimed at an improved overall user experience. It is therefore also very different to the v3 API, and will require re-learning of changed patterns in the way you interact with Weaviate.

While this may introduce some overhead, we believe the v4 API is a significant improvement to your developer experience. For instance, using the v4 client will allow you to take full advantage faster speeds through the gRPC API, and additional static analysis for IDE assistance through strong typing.

Due to the extensive API surface changes, this guide does not cover every change. Instead, this guide is designed to help you understand the major changes and how to migrate your code at a high level.

For code examples, refer to the documentation throughout the site, starting with these suggested sections.

https://weaviate.io/developers/weaviate/client-libraries/python/v3_v4_migration

Instantiate a client
The v4 client is instantiated by the WeaviateClient object. The WeaviateClient object is the main entry point for all API operations.

You can instantiate the WeaviateClient object directly. However, in most cases it is easier to use a connection helper function such as connect_to_local or connect_to_weaviate_cloud.


```python
# Create a Collection
import weaviate

client = weaviate.connect_to_local()  # Connect with default parameters
```

Major changes
The v4 client API is very different from the v3 API. Major user-facing changes in the v4 client include:

Extensive use of helper classes
Interaction with collections
Removal of builder patterns
Helper classes
The v4 client makes extensive use of helper classes. These classes provide strong typing and thus static type checking. It also makes coding easier through your IDE's auto-completion feature.

When you are coding, check the auto-complete frequently. It provides useful guidance for API changes and client options.

```python
import weaviate
import weaviate.classes.config as wvcc

client = weaviate.connect_to_local()

try:
    # Note that you can use `client.collections.create_from_dict()` to create a collection from a v3-client-style JSON object
    collection = client.collections.create(
        name="TestArticle",
        vectorizer_config=wvcc.Configure.Vectorizer.text2vec_cohere(),
        generative_config=wvcc.Configure.Generative.cohere(),
        properties=[
            wvcc.Property(
                name="title",
                data_type=wvcc.DataType.TEXT
            )
        ]
    )

finally:
    client.close()
```

```python
# NearText Query
import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import Move
import os

client = weaviate.connect_to_local()

try:
    publications = client.collections.get("Publication")

    response = publications.query.near_text(
        query="fashion",
        distance=0.6,
        move_to=Move(force=0.85, concepts="haute couture"),
        move_away=Move(force=0.45, concepts="finance"),
        return_metadata=wvc.query.MetadataQuery(distance=True),
        limit=2
    )

    for o in response.objects:
        print(o.properties)
        print(o.metadata)

finally:
    client.close()
```

The wvc namespace exposes commonly used classes in the v4 API. The namespace is divided further into submodules based on their primary purpose.

import weaviate.classes as wvc

Interact with collections
When you connect to a Weaviate database, the v4 API returns a WeaviateClient object, while the v3 API returns a Client object.

The v3 API's interactions were built around the client object (an instance of Client). This includes server interactions for CRUD and search operations.

In the v4 API, the main starting points for your interaction with Weaviate follow a different paradigm.

Server-level interactions such as checking readiness (client.is_ready()) or getting node statuses (client.cluster.nodes()) still remain with client (now an instance of WeaviateClient).

CRUD and search operations are now performed against a Collection object to reflect that these operations target a particular collection.

This example below shows a function with a Collection typing hint).

from weaviate.collections import Collection

my_collection = client.collections.get(collection_name)

def work_with_collection(collection: Collection):
    # Do something with the collection, e.g.:
    r = collection.query.near_text(query="financial report summary")
    return r

response = work_with_collection(my_collection)

The collection object includes its name as an attribute. Accordingly, operations such as a near_text query can be performed without specifying the collection name. The v4 collection object has a more focussed namespace in comparison to the breadth of operations available with the v3 client object. This simplifies your code and reduces the potential for errors.

Python Client v4

```python
jeopardy = client.collections.get("JeopardyQuestion")

data_object = jeopardy.query.fetch_object_by_id("00ff6900-e64f-5d94-90db-c8cfa3fc851b")

print(data_object.properties)
```

Python Client v3 (DEPRECATED: DO NOT USE)
```python
data_object = client.data_object.get_by_id(
    "00ff6900-e64f-5d94-90db-c8cfa3fc851b",
    class_name="JeopardyQuestion",
)

print(json.dumps(data_object, indent=2))
```

Terminology changes (e.g. class -> collection)
Some of the terms within the Weaviate ecosystem are changing, and the client has changed accordingly:

A Weaviate "Class" is now called a "Collection". A collection stores a set of data objects together with their vector embeddings.
A "Schema" is now called a "Collection Configuration", a set of settings that define collection name, vectorizers, index configurations, property definitions, and so on.
Due to the architectural changes as well as changes to the terminology, most of the API has been changed. Expect to find differences in the way you interact with Weaviate.

For example, client.collections.list_all() is the replacement for client.schema.get().

Manage data has more details and additional sample code for working with data, such as working with collections. See searches for further details on various queries and filters.

Collection creation from JSON
You can still create a collection from a JSON definition. This may be a useful way to migrate your existing data, for example. You could fetch an existing definition and then use it to create a new collection.

import weaviate

client = weaviate.connect_to_local()

try:
    collection_definition = {
        "class": "TestArticle",
        "properties": [
            {
                "name": "title",
                "dataType": ["text"],
            },
            {
                "name": "body",
                "dataType": ["text"],
            },
        ],
    }

    client.collections.create_from_dict(collection_definition)

finally:
    client.close()

Removal of builder patterns
The builder patterns for constructing queries have been removed. Builder patterns could be confusing, and led to runtime errors that could not be picked up with static analysis.

Instead, construct queries in the v4 API using specific methods and its parameters.

Python Client v4
```python
from weaviate.classes.query import MetadataQuery

jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.near_text(
    query="animals in movies",
    limit=2,
    return_metadata=MetadataQuery(distance=True)
)

for o in response.objects:
    print(o.properties)
    print(o.metadata.distance)
```

Python Client v3 (DEPRECATED: DO NOT USE)
```python
response = (
    client.query
    .get("JeopardyQuestion", ["question", "answer"])
    .with_near_text({
        "concepts": ["animals in movies"]
    })
    .with_limit(2)
    .with_additional(["distance"])
    .do()
)

print(json.dumps(response, indent=2))
```

Instantiate a client
There are multiple ways to connect to your Weaviate instance. To instantiate a client, use one of these styles:

- Connection helper functions
- Explicit instantiation
- Async client

Connection helper functions
- weaviate.connect_to_weaviate_cloud()
    previously connect_to_wcs()
- weaviate.connect_to_local()
- weaviate.connect_to_embedded()
- weaviate.connect_to_custom()

```python
import weaviate
client = weaviate.connect_to_local()  # Connect with default parameters
```

The v4 client helper functions provide some optional parameters to customize your client.

Specify external API keys
Specify connection timeout values
Specify authentication details

External API keys
To add API keys for services such as Cohere or OpenAI, use the headers parameter.

```python
import weaviate
import os

client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")
    }
)
```

Timeout values
You can set timeout values, in seconds, for the client. Use the Timeout class to configure the timeout values for initialization checks as well as query and insert operations.

```python
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout

client = weaviate.connect_to_local(
    port=8080,
    grpc_port=50051,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
    )
)
```

Timeouts on generate queries
If you see errors while using the generate submodule, try increasing the query timeout values (Timeout(query=60)).

The generate submodule uses a large language model to generate text. The submodule is dependent on the speed of the language model and any API that serves the language model.

Increase the timeout values to allow the client to wait longer for the language model to respond.

Explicit instantiation
If you need to pass custom parameters, use the weaviate.WeaviateClient class to instantiate a client. This is the most flexible way to instantiate the client object.

When you instantiate a connection directly, you have to call the .connect() method to connect to the server.

import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout, Auth
import os

client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_params(
        http_host="localhost",
        http_port=8099,
        http_secure=False,
        grpc_host="localhost",
        grpc_port=50052,
        grpc_secure=False,
    ),
    auth_client_secret=Auth.api_key("secr3tk3y"),
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")
    },
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120),  # Values in seconds
    ),
    skip_init_checks=False
)

client.connect()  # When directly instantiating, you need to connect manually

Async client
Added in weaviate-client v4.7.0
The v4 API client supports asynchronous (asyncio) operations through the WeaviateAsyncClient class.

You can instantiate an WeaviateAsyncClient object directly, or use helper functions with a weaviate.use_async_xxx prefix such as weaviate.use_async_with_weaviate_cloud().

For more details, see the async Python client documentation.

Initial connection checks
When establishing a connection to the Weaviate server, the client performs a series of checks. These includes checks for the server version, and to make sure that the REST and gRPC ports are available.

You can set skip_init_checks to True to skip these checks.

import weaviate

client = weaviate.connect_to_local(
    skip_init_checks=True
)

In most cases, you should use the default False setting for skip_init_checks. However, setting skip_init_checks=True may be a useful temporary measure if you have connection issues.

For additional connection configuration, see Timeout values.

Batch imports
The v4 client offers two ways to perform batch imports. From the client object directly, or from the collection object.

We recommend using the collection object to perform batch imports of single collections or tenants. If you are importing objects across many collections, such as in a multi-tenancy configuration, using client.batch may be more convenient.

Batch sizing
There are three methods to configure the batching behavior. They are dynamic, fixed_size and rate_limit.

Method	Description	When to use
dynamic	The batch size and the number of concurrent requests are dynamically adjusted on-the-fly during import, depending on the server load.	Recommended starting point.
fixed_size	The batch size and number of concurrent requests are fixed to sizes specified by the user.	When you want to specify fixed parameters.
rate_limit	The number of objects sent to Weaviate is rate limited (specified as n_objects per minute).	When you want to avoid hitting third-party vectorization API rate limits.
Usage
We recommend using a context manager as shown below.

These methods return a new context manager for each batch. Attributes that are returned from one batch, such as failed_objects or failed_references, are not included in any subsequent calls.

Dynamic
```python
import weaviate

client = weaviate.connect_to_local()

try:
    with client.batch.dynamic() as batch:  # or <collection>.batch.dynamic()
        # Batch import objects/references - e.g.:
        batch.add_object(properties={"title": "Multitenancy"}, collection="WikiArticle", uuid=src_uuid)
        batch.add_object(properties={"title": "Database schema"}, collection="WikiArticle", uuid=tgt_uuid)
        batch.add_reference(from_collection="WikiArticle", from_uuid=src_uuid, from_property="linkedArticle", to=tgt_uuid)

finally:
    client.close()
```

Fixed size
```python
import weaviate

client = weaviate.connect_to_local()

try:
    with client.batch.fixed_size(batch_size=100, concurrent_requests=4) as batch:  # or <collection>.batch.fixed_size()
        # Batch import objects/references - e.g.:
        batch.add_object(properties={"title": "Multitenancy"}, collection="WikiArticle", uuid=src_uuid)
        batch.add_object(properties={"title": "Database schema"}, collection="WikiArticle", uuid=tgt_uuid)
        batch.add_reference(from_collection="WikiArticle", from_uuid=src_uuid, from_property="linkedArticle", to=tgt_uuid)

finally:
    client.close()
```

Rate limit
```python
import weaviate

client = weaviate.connect_to_local()

try:
    with client.batch.rate_limit(requests_per_minute=600) as batch:  # or <collection>.batch.rate_limit()
        # Batch import objects/references - e.g.:
        batch.add_object(properties={"title": "Multitenancy"}, collection="WikiArticle", uuid=src_uuid)
        batch.add_object(properties={"title": "Database schema"}, collection="WikiArticle", uuid=tgt_uuid)
        batch.add_reference(from_collection="WikiArticle", from_uuid=src_uuid, from_property="linkedArticle", to=tgt_uuid)

finally:
    client.close()
```

If the background thread that is responsible for sending the batches raises an exception during batch processing, the error is raised to the main thread.

Error handling
During a batch import, any failed objects or references will be stored for retrieval. Additionally, a running count of failed objects and references is maintained.

The counter can be accessed through batch.number_errors within the context manager.

A list of failed objects can be obtained through batch.failed_objects and a list of failed references can be obtained through batch.failed_references.

Note that these lists are reset when a batching process is initialized. So make sure to retrieve them before starting a new batch import block.

```python
import weaviate

client = weaviate.connect_to_local()

try:
    # ===== First batch import block =====
    with client.batch.rate_limit(requests_per_minute=600) as batch:  # or <collection>.batch.rate_limit()
        # Batch import objects/references
        for i in source_iterable:  # Some insertion loop
            if batch.number_errors > 10:  # Monitor errors during insertion
                # Break or raise an exception
                pass
    # Note these are outside the `with` block - they are populated after the context manager exits
    failed_objs_a = client.batch.failed_objects  # Get failed objects from the first batch import
    failed_refs_a = client.batch.failed_references  # Get failed references from the first batch import

    # ===== Second batch import block =====
    # This will clear the failed objects/references
    with client.batch.rate_limit(requests_per_minute=600) as batch:  # or <collection>.batch.rate_limit()
        # Batch import objects/references
        for i in source_iterable:  # Some insertion loop
            if batch.number_errors > 10:  # Monitor errors during insertion
                # Break or raise an exception
                pass
    # Note these are outside the `with` block - they are populated after the context manager exits
    failed_objs_b = client.batch.failed_objects  # Get failed objects from the second batch import
    failed_refs_b = client.batch.failed_references  # Get failed references from the second batch import

finally:
    client.close()
```

Batch vectorization
Added in v1.25.
Some model providers provide batch vectorization APIs, where each request can include multiple objects.

From Weaviate v1.25.0, a batch import automatically makes use of the model providers' batch vectorization APIs where available. This reduces the number of requests to the model provider, improving throughput.

The client automatically handles vectorization if you set the vectorizer when you create the collection.

Create a client
```python
collection = client.collections.create(
        name="NewCollection",
        properties=[
            Property(name="url", data_type=DataType.TEXT),
            Property(name="title", data_type=DataType.TEXT),
            Property(name="raw", data_type=DataType.TEXT),
            Property(name="sha", data_type=DataType.TEXT),
        ],
        vectorizer_config=[
            Configure.NamedVectors.text2vec_cohere(name="cohereFirst"),
            Configure.NamedVectors.text2vec_cohere(name="cohereSecond"),
        ]
    )
```

To modify the vectorization settings, update the client object. This example adds multiple vectorizers:

Cohere. Set the service API key. Set the request rate.

OpenAI. Set the service API key. Set the base URL.

VoyageAI. Set the service API key.

Modify the client
```python
from weaviate.classes.config import Integrations

integrations = [
    # Each model provider may expose different parameters
    Integrations.cohere(
        api_key=cohere_key,
        requests_per_minute_embeddings=rpm_embeddings,
    ),
    Integrations.openai(
        api_key=openai_key,
        requests_per_minute_embeddings=rpm_embeddings,
        tokens_per_minute_embeddings=tpm_embeddings,   # e.g. OpenAI also exposes tokens per minute for embeddings
    ),
]
client.integrations.configure(integrations)
```

Working with collections
Instantiate a collection
You can instantiate a collection object by creating a collection, or by retrieving an existing collection.

Create a collection

import weaviate
import weaviate.classes.config as wvcc

client = weaviate.connect_to_local()

try:
    # Note that you can use `client.collections.create_from_dict()` to create a collection from a v3-client-style JSON object
    collection = client.collections.create(
        name="TestArticle",
        vectorizer_config=wvcc.Configure.Vectorizer.text2vec_cohere(),
        generative_config=wvcc.Configure.Generative.cohere(),
        properties=[
            wvcc.Property(
                name="title",
                data_type=wvcc.DataType.TEXT
            )
        ]
    )

finally:
    client.close()

With cross-references

import weaviate
import weaviate.classes.config as wvcc

client = weaviate.connect_to_local()

try:
    articles = client.collections.create(
        name="TestArticle",
        vectorizer_config=wvcc.Configure.Vectorizer.text2vec_cohere(),
        generative_config=wvcc.Configure.Generative.cohere(),
        properties=[
            wvcc.Property(
                name="title",
                data_type=wvcc.DataType.TEXT
            )
        ]
    )

    authors = client.collections.create(
        name="TestAuthor",
        vectorizer_config=wvcc.Configure.Vectorizer.text2vec_cohere(),
        generative_config=wvcc.Configure.Generative.cohere(),
        properties=[
            wvcc.Property(
                name="name",
                data_type=wvcc.DataType.TEXT
            )
        ],
        references=[
            wvcc.ReferenceProperty(
                name="wroteArticle",
                target_collection="TestArticle"
            )
        ]
    )
finally:
    client.close()

Get a collection

import weaviate

client = weaviate.connect_to_local()

try:
    collection = client.collections.get("TestArticle")
finally:
    client.close()

Collection submodules
Operations in the v4 client are grouped into submodules. The key submodules for interacting with objects are:

data: CUD operations (read operations are in query)
batch: Batch import operations
query: Search operations
generate: Retrieval augmented generation operations
Build on top of query operations
aggregate: Aggregation operations
data
The data submodule contains all object-level CUD operations, including:

insert for creating objects.
This function takes the object properties as a dictionary.
insert_many for adding multiple objects with one request.
This function takes the object properties as a dictionary or as a DataObject instance.
Note: For larger numbers of objects, consider using batch imports.
update for updating objects (for PATCH operations).
replace for replacing objects (for PUT operations).
delete_by_id for deleting objects by ID.
delete_many for batch deletion.
reference_xxx for reference operations, including reference_add, reference_add_many, reference_update and reference_delete.
See some examples below. Note that each function will return varying types of objects.

Insert
questions = client.collections.get("JeopardyQuestion")

new_uuid = questions.data.insert(
    properties={
        "question": "This is the capital of Australia."
    },
    references={  # For adding cross-references
        "hasCategory": target_uuid
    }
)

Insert many
questions = client.collections.get("JeopardyQuestion")

properties = [{"question": f"Test Question {i+1}"} for i in range(5)]
response = questions.data.insert_many(properties)

insert_many sends one request
insert_many sends one request for the entire function call. For requests with a large number of objects, consider using batch imports.

Delete by id
questions = client.collections.get("JeopardyQuestion")

deleted = questions.data.delete_by_id(uuid=new_uuid)

Delete many
from weaviate.classes.query import Filter

questions = client.collections.get("JeopardyQuestion")

response = questions.data.delete_many(
    where=Filter.by_property(name="question").equal("Test Question")
)

insert_many sends one request
insert_many sends one request for the entire function call. For requests with a large number of objects, consider using batch imports.

insert_many with DataObjects
The insert_many function takes a list of DataObject instances or a list of dictionaries. This is useful if you want to specify additional information to the properties, such as cross-references, object uuid, or a custom vector.

from weaviate.util import generate_uuid5

questions = client.collections.get("JeopardyQuestion")

data_objects = list()
for i in range(5):
    properties = {"question": f"Test Question {i+1}"}
    data_object = wvc.data.DataObject(
        properties=properties,
        uuid=generate_uuid5(properties)
    )
    data_objects.append(data_object)

response = questions.data.insert_many(data_objects)

Cross-reference creation
Cross-references should be added under a references parameter in the relevant function/method, with a structure like:

{
    "<REFERENCE_PROPERTY_NAME>": "<TARGET_UUID>"
}

For example:

from weaviate.util import generate_uuid5

questions = client.collections.get("JeopardyQuestion")

data_objects = list()
for i in range(5):
    properties = {"question": f"Test Question {i+1}"}
    data_object = wvc.data.DataObject(
        properties=properties,
        references={
            "hasCategory": target_uuid
        },
        uuid=generate_uuid5(properties)
    )
    data_objects.append(data_object)

response = questions.data.insert_many(data_objects)

Using the properties parameter to add references is deprecated and will be removed in the future.

query
The query submodule contains all object-level query operations, including fetch_objects for retrieving objects without additional search parameters, bm25 for keyword search, near_<xxx> for vector search operators, hybrid for hybrid search and so on.

These queries return a _QueryReturn object, which contains a list of _Object objects.

BM25
questions = client.collections.get("JeopardyQuestion")
response = questions.query.bm25(
    query="animal",
    limit=2
)

for o in response.objects:
    print(o.properties)  # Object properties

Near text
questions = client.collections.get("JeopardyQuestion")
response = questions.query.near_text(
    query="animal",
    limit=2
)

for o in response.objects:
    print(o.properties)  # Object properties

    Queries with custom returns
You can further specify:

Whether to include the object vector (via include_vector)
Default is False
Which properties to include (via return_properties)
All properties are returned by default
Which references to include (via return_references)
Which metadata to include
No metadata is returned by default
Each object includes its UUID as well as all properties by default.

For example:

Default

questions = client.collections.get("JeopardyQuestion")
response = questions.query.bm25(
    query="animal",
    limit=2
)

for o in response.objects:
    print(o.properties)  # All properties by default
    print(o.references)  # References not returned by default
    print(o.uuid)  # UUID included by default
    print(o.vector)  # No vector
    print(o.metadata)  # No metadata

Customized returns

questions = client.collections.get("JeopardyQuestion")
response = questions.query.bm25(
    query="animal",
    include_vector=True,
    return_properties=["question"],
    return_metadata=wvc.query.MetadataQuery(distance=True),
    return_references=wvc.query.QueryReference(
        link_on="hasCategory",
        return_properties=["title"],
        return_metadata=wvc.query.MetadataQuery(creation_time=True)
    ),
    limit=2
)

for o in response.objects:
    print(o.properties)  # Selected properties only
    print(o.references)  # Selected references
    print(o.uuid)  # UUID included by default
    print(o.vector)  # With vector
    print(o.metadata)  # With selected metadata

    query + group by
Results of a query can be grouped by a property as shown here.

The results are organized by both their individual objects as well as the group.

The objects attribute is a list of objects, each containing a belongs_to_group property to indicate which group it belongs to.
The group attribute is a dictionary with each key indicating the value of the group, and the value being a list of objects belonging to that group.
questions = client.collections.get("JeopardyQuestion")
response = questions.query.near_text(
    query="animal",
    distance=0.2,
    group_by=wvc.query.GroupBy(
        prop="points",
        number_of_groups=3,
        objects_per_group=5
    )
)

for k, v in response.groups.items():  # View by group
    print(k, v)

for o in response.objects:  # View by object
    print(o)

generate
The generate methods perform retrieval augmented generation (RAG). This is a two-step process involving a search followed by prompting a large language model. Therefore, function names are shared across the query and generate submodules, with additional parameters available in the generate submodule.

Generate

questions = client.collections.get("JeopardyQuestion")
response = questions.generate.bm25(
    query="animal",
    limit=2,
    grouped_task="What do these animals have in common?",
    single_prompt="Translate the following into French: {answer}"
)

print(response.generated)  # Generated text from grouped task
for o in response.objects:
    print(o.generated)  # Generated text from single prompt
    print(o.properties)  # Object properties

Query

questions = client.collections.get("JeopardyQuestion")
response = questions.query.bm25(
    query="animal",
    limit=2
)

for o in response.objects:
    print(o.properties)  # Object properties


----

Cross-references
Use cross-references to establish directional relationships between collections.

Additional information
Notes:

Cross-references does not affect object vectors of the source or the target objects.
For multi-tenancy collection, you can establish a cross-reference from a multi-tenancy collection object to:
A non-multi-tenancy collection object, or
A multi-tenancy collection object belonging to the same tenant.
Define a cross-reference property
Include the reference property in the collection definition before adding cross-references to it.

Python Client v4
Python Client v3
JS/TS Client v3
from weaviate.classes.config import Property, DataType, ReferenceProperty

client.collections.create(
    name="JeopardyQuestion",
    description="A Jeopardy! question",
    properties=[
        Property(name="question", data_type=DataType.TEXT),
        Property(name="answer", data_type=DataType.TEXT),
    ],
    references=[
        ReferenceProperty(
            name="hasCategory",
            target_collection="JeopardyCategory"
        )
    ]

)

Add a cross-reference property
It is also possible to add a cross-reference property to an existing collection definition.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import ReferenceProperty

# Add the reference to JeopardyQuestion, after it was created
category = client.collections.get("JeopardyCategory")
# category.config.add_reference(
category.config.add_reference(
    ReferenceProperty(
        name="hasQuestion",
        target_collection="JeopardyQuestion"
    )
)

Create an object with a cross-reference
Specify a cross-reference when creating an object.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
questions = client.collections.get("JeopardyQuestion")

questions.data.insert(
    properties=properties,  # A dictionary with the properties of the object
    uuid=obj_uuid,  # The UUID of the object
    references={"hasCategory": category_uuid},  # e.g. {"hasCategory": "583876f3-e293-5b5b-9839-03f455f14575"}
)

Add a one-way cross-reference
Specify the required id and properties for the source and the target.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
questions = client.collections.get("JeopardyQuestion")

questions.data.reference_add(
    from_uuid=question_obj_id,
    from_property="hasCategory",
    to=category_obj_id
)

Add two-way cross-references
This requires adding reference properties in both directions, and adding two cross-references per object pair (from A -> to B and from B -> to A).

Create the JeopardyCategory collection:

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Property, DataType, ReferenceProperty

category = client.collections.create(
    name="JeopardyCategory",
    description="A Jeopardy! category",
    properties=[
        Property(name="title", data_type=DataType.TEXT)
    ]
)

Create the JeopardyQuestion collection including the reference property to JeopardyCategory:

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
client.collections.create(
    name="JeopardyQuestion",
    description="A Jeopardy! question",
    properties=[
        Property(name="question", data_type=DataType.TEXT),
        Property(name="answer", data_type=DataType.TEXT),
    ],
    references=[
        ReferenceProperty(
            name="hasCategory",
            target_collection="JeopardyCategory"
        )
    ]
)

Modify JeopardyCategory to add the reference to JeopardyQuestion:

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import ReferenceProperty

# Add the reference to JeopardyQuestion, after it was created
category = client.collections.get("JeopardyCategory")
# category.config.add_reference(
category.config.add_reference(
    ReferenceProperty(
        name="hasQuestion",
        target_collection="JeopardyQuestion"
    )
)

And add the cross-references:

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
# For the "San Francisco" JeopardyQuestion object, add a cross-reference to the "U.S. CITIES" JeopardyCategory object
questions = client.collections.get("JeopardyQuestion")
questions.data.reference_add(
    from_uuid=question_obj_id,
    from_property="hasCategory",
    to=category_obj_id
)

# For the "U.S. CITIES" JeopardyCategory object, add a cross-reference to "San Francisco"
categories = client.collections.get("JeopardyCategory")
categories.data.reference_add(
    from_uuid=category_obj_id,
    from_property="hasQuestion",
    to=question_obj_id
)

Add multiple (one-to-many) cross-references
Weaviate allows creation of multiple cross-references from one source object.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
from weaviate.classes.data import DataReference

questions = client.collections.get("JeopardyQuestion")

refs_list = []
for temp_uuid in [category_obj_id, category_obj_id_alt]:
    ref_obj = DataReference(
        from_uuid=question_obj_id,
        from_property="hasCategory",
        to_uuid=temp_uuid
    )
    refs_list.append(ref_obj)

questions.data.reference_add_many(refs_list)

Read cross-references
Cross-references can be read as part of the object.

Python Client v4
Python Client v3
JS/TS Client v3
from weaviate.classes.query import QueryReference

questions = client.collections.get("JeopardyQuestion")

# Include the cross-references in a query response
response = questions.query.fetch_objects(  # Or `hybrid`, `near_text`, etc.
    limit=2,
    return_references=QueryReference(
        link_on="hasCategory",
        return_properties=["title"]
    )
)

# Or include cross-references in a single-object retrieval
obj = questions.query.fetch_object_by_id(
    uuid=question_obj_id,
    return_references=QueryReference(
        link_on="hasCategory",
        return_properties=["title"]
    )
)

Delete a cross-reference
Deleting a cross-reference with the same parameters used to define the cross-reference.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
# From the "San Francisco" JeopardyQuestion object, delete the "MUSEUMS" category cross-reference
questions = client.collections.get("JeopardyQuestion")
questions.data.reference_delete(
    from_uuid=question_obj_id,
    from_property="hasCategory",
    to=category_obj_id
)

What happens if the target object is deleted?
Update a cross-reference
The targets of a cross-reference can be updated.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
# In the "San Francisco" JeopardyQuestion object, set the "hasCategory" cross-reference only to "MUSEUMS"
questions = client.collections.get("JeopardyQuestion")
questions.data.reference_replace(
    from_uuid=question_obj_id,
    from_property="hasCategory",
    to=category_obj_id
)

Search patterns and basics
With Weaviate you can query your data using vector similarity search, keyword search, or a mix of both with hybrid search. You can control what object properties and metadata to return.

This page provides fundamental search syntax to get you started.

List objects
You can get objects without specifying any parameters. This returns objects in ascending UUID order.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
GraphQL
jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects()

for o in response.objects:
    print(o.properties)

Example response
The output is like this:

{
  "data": {
    "Get": {
      "JeopardyQuestion": [
        {
          "question": "This prophet passed the time he spent inside a fish offering up prayers"
        },
        // shortened for brevity
      ]
    }
  }
}

Additional information
Specify the information that you want your query to return. You can return object properties, object IDs, and object metadata.

limit returned objects
Use limit to set a fixed maximum number of objects to return.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
GraphQL
jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects(
    limit=1
)

for o in response.objects:
    print(o.properties)

Example response
Paginate with limit and offset
To start in the middle of your result set, define an offset. Set a limit to return objects starting at the offset.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
GraphQL
jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects(
    limit=1,
    offset=1
)

for o in response.objects:
    print(o.properties)

Example response
To paginate through the entire database, use a cursor instead of offset and limit.

Specify object properties
You can specify which object properties to return.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
GraphQL
jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects(
    limit=1,
    return_properties=["question", "answer", "points"]
)

for o in response.objects:
    print(o.properties)

Example response
Retrieve the object vector
You can retrieve the object vector. (Also applicable where named vectors are used.)

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
GraphQL
jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects(
    include_vector=True,
    limit=1
)

print(response.objects[0].vector["default"])

Example response
Retrieve the object id
You can retrieve the object id (uuid).

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
GraphQL
jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects(
    # Object IDs are included by default with the `v4` client! :)
    limit=1
)

for o in response.objects:
    print(o.uuid)

Example response
Retrieve cross-referenced properties
To retrieve properties from cross-referenced objects, specify:

The cross-reference property
The target cross-referenced collection
The properties to retrieve
Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
GraphQL
from weaviate.classes.query import QueryReference

jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects(
    return_references=[
        QueryReference(
            link_on="hasCategory",
            return_properties=["title"]
        ),
    ],
    limit=2
)

for o in response.objects:
    print(o.properties["question"])
    # print referenced objects
    for ref_obj in o.references["hasCategory"].objects:
        print(ref_obj.properties)

Example response
Retrieve metadata values
You can specify metadata fields to be returned.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
GraphQL
from weaviate.classes.query import MetadataQuery

jeopardy = client.collections.get("JeopardyQuestion")
response = jeopardy.query.fetch_objects(
    limit=1,
    return_metadata=MetadataQuery(creation_time=True)
)

for o in response.objects:
    print(o.properties)  # View the returned properties
    print(o.metadata.creation_time)  # View the returned creation time

For a comprehensive list of metadata fields, see GraphQL: Additional properties.

Multi-tenancy
If multi-tenancy is enabled, specify the tenant parameter in each query.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
# Connect to the collection
mt_collection = client.collections.get("WineReviewMT")

# Get the specific tenant's version of the collection
collection_tenant_a = mt_collection.with_tenant("tenantA")

# Query tenantA's version
response = collection_tenant_a.query.fetch_objects(
    return_properties=["review_body", "title"],
    limit=1,
)

print(response.objects[0].properties)

Replication
For collections with replication enabled, you can specify the consistency level in your queries. This applies to CRUD queries as well as searches.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
Curl
from weaviate.classes.config import ConsistencyLevel

questions = client.collections.get(collection_name).with_consistency_level(
    consistency_level=ConsistencyLevel.QUORUM
)
response = collection.query.fetch_object_by_id("36ddd591-2dee-4e7e-a3cc-eb86d30a4303")

# The parameter passed to `withConsistencyLevel` can be one of:
# * 'ALL',
# * 'QUORUM' (default), or
# * 'ONE'.
#
# It determines how many replicas must acknowledge a request
# before it is considered successful.

for o in response.objects:
    print(o.properties)  # Inspect returned objects

    Manage collections
Every object in Weaviate belongs to exactly one collection. Use the examples on this page to manage your collections.

Terminology
Newer Weaviate documentation discuses "collections." Older Weaviate documentation refers to "classes" instead. Expect to see both terms throughout the documentation.

Create a collection
To create a collection, specify at least the collection name. If you don't specify any properties, auto-schema creates them.

Capitalization
Weaviate follows GraphQL naming conventions.

Start collection names with an upper case letter.
Start property names with a lower case letter.
If you use an initial upper case letter to define a property name, Weaviate changes it to a lower case letter internally.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
client.collections.create("Article")

Create a collection and define properties
Properties are the data fields in your collection. Each property has a name and a data type.

Additional information
Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Property, DataType

# Note that you can use `client.collections.create_from_dict()` to create a collection from a v3-client-style JSON object
client.collections.create(
    "Article",
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="body", data_type=DataType.TEXT),
    ]
)

Disable auto-schema
By default, Weaviate creates missing collections and missing properties. When you configure collections manually, you have more precise control of the collection settings.

To disable auto-schema set AUTOSCHEMA_ENABLED: 'false' in your system configuration file.

Specify a vectorizer
Specify a vectorizer for a collection.

Additional information
Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    properties=[  # properties configuration is optional
        Property(name="title", data_type=DataType.TEXT),
        Property(name="body", data_type=DataType.TEXT),
    ]
)

Define multiple named vectors
Added in v1.24
You can define multiple named vectors per collection. This allows each object to be represented by multiple vectors, such as a text vector and an image vector, or a title vector and a body vector.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "ArticleNV",
    vectorizer_config=[
        # Set a named vector
        Configure.NamedVectors.text2vec_cohere(  # Use the "text2vec-cohere" vectorizer
            name="title", source_properties=["title"]       # Set the source property(ies)
        ),
        # Set another named vector
        Configure.NamedVectors.text2vec_openai(  # Use the "text2vec-openai" vectorizer
            name="body", source_properties=["body"]         # Set the source property(ies)
        ),
        # Set another named vector
        Configure.NamedVectors.text2vec_openai(  # Use the "text2vec-openai" vectorizer
            name="title_country", source_properties=["title", "country"] # Set the source property(ies)
        )
    ],
    properties=[  # Define properties
        Property(name="title", data_type=DataType.TEXT),
        Property(name="body", data_type=DataType.TEXT),
        Property(name="country", data_type=DataType.TEXT),
    ],
)

Specify vectorizer settings
To configure how a vectorizer works (i.e. what model to use) with a specific collection, set the vectorizer parameters.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Configure

client.collections.create(
    "Article",
    vectorizer_config=Configure.Vectorizer.text2vec_cohere(
        model="embed-multilingual-v2.0",
        vectorize_collection_name=True
    ),
)

Set vector index type
The vector index type can be set for each collection at creation time, between hnsw, flat and dynamic index types.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    vector_index_config=Configure.VectorIndex.hnsw(),  # Use the HNSW index
    # vector_index_config=Configure.VectorIndex.flat(),  # Use the FLAT index
    # vector_index_config=Configure.VectorIndex.dynamic(),  # Use the DYNAMIC index
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="body", data_type=DataType.TEXT),
    ]
)

Additional information
Set vector index parameters
Various vector index parameters are configurable at collection creation time, including compression and filter strategy.

Filter strategy parameter
Was added in v1.27

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Configure, Property, DataType, VectorDistances, VectorFilterStrategy

client.collections.create(
    "Article",
    # Additional configuration not shown
    vector_index_config=Configure.VectorIndex.hnsw(
        quantizer=Configure.VectorIndex.Quantizer.bq(),
        ef_construction=300,
        distance_metric=VectorDistances.COSINE,
        filter_strategy=VectorFilterStrategy.SWEEPING  # or ACORN (Available from Weaviate v1.27.0)
    ),
)

Additional information
Property-level settings
Configure individual properties in a collection. Each property can have it's own configuration. Here are some common settings:

Vectorize the property
Vectorize the property name
Set a tokenization type
Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Configure, Property, DataType, Tokenization

client.collections.create(
    "Article",
    vectorizer_config=Configure.Vectorizer.text2vec_huggingface(),

    properties=[
        Property(
            name="title",
            data_type=DataType.TEXT,
            vectorize_property_name=True,  # Use "title" as part of the value to vectorize
            tokenization=Tokenization.LOWERCASE  # Use "lowecase" tokenization
        ),
        Property(
            name="body",
            data_type=DataType.TEXT,
            skip_vectorization=True,  # Don't vectorize this property
            tokenization=Tokenization.WHITESPACE  # Use "whitespace" tokenization
        ),
    ]
)

Specify a distance metric
If you choose to bring your own vectors, you should specify the distance metric.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
from weaviate.classes.config import Configure, VectorDistances

client.collections.create(
    "Article",
    vector_index_config=Configure.VectorIndex.hnsw(
        distance_metric=VectorDistances.COSINE
    ),
)

Additional information
Set inverted index parameters
Various inverted index parameters are configurable for each collection. Some parameters are set at the collection level, while others are set at the property level.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    # Additional settings not shown
    properties=[ # properties configuration is optional
        Property(
            name="title",
            data_type=DataType.TEXT,
            index_filterable=True,
            index_searchable=True,
        ),
        Property(
            name="Chunk",
            data_type=DataType.INT,
            index_range_filters=True,
        ),
    ],
    inverted_index_config=Configure.inverted_index(  # Optional
        bm25_b=0.7,
        bm25_k1=1.25,
        index_null_state=True,
        index_property_length=True,
        index_timestamps=True
    )
)

Specify a reranker model integration
Configure a reranker model integration for reranking retrieved results.

Related pages
Available reranker model integrations
Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    reranker_config=Configure.Reranker.cohere()
)

Update the reranker model integration
Available from v1.25.23, v1.26.8 and v1.27.1
The reranker and generative configurations are mutable from v1.25.23, v1.26.8 and v1.27.1.

Update the reranker model integration for reranking retrieved results.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Reconfigure

collection = client.collections.get("Article")

collection.config.update(
    reranker_config=Reconfigure.Reranker.cohere()  # Update the reranker module
)

Specify a generative model integration
Specify a generative model integration for a collection (for RAG).

Related pages
Available generative model integrations
Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    generative_config=Configure.Generative.openai(),
)

Specify a generative model name
Specify a generative model name.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Configure, Property, DataType

client.collections.create(
    "Article",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    generative_config=Configure.Generative.openai(
        model="gpt-4"
    ),
)

Update the generative model integration
Available from v1.25.23, v1.26.8 and v1.27.1
The reranker and generative configurations are mutable from v1.25.23, v1.26.8 and v1.27.1.

Update a reranker model integration for reranking retrieved results.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Reconfigure

collection = client.collections.get("Article")

collection.config.update(
    generative_config=Reconfigure.Generative.cohere()  # Update the generative module
)

Replication settings
Replication factor change in v1.25
In Weaviate v1.25, a replication factor cannot be changed once it is set.

This is due to the schema consensus algorithm change in v1.25. This will be improved in future versions.

Configure replication per collection.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
cURL
from weaviate.classes.config import Configure

client.collections.create(
    "Article",
    replication_config=Configure.replication(
        factor=3,
        async_enabled=True,
    )
)

Additional information
Sharding settings
Configure sharding per collection.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Configure

client.collections.create(
    "Article",
    sharding_config=Configure.sharding(
        virtual_per_physical=128,
        desired_count=1,
        desired_virtual_count=128,
    )
)

Additional information
Multi-tenancy
Added in v1.20
Create a collection with multi-tenancy enabled.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Configure

client.collections.create(
    "Article",
    multi_tenancy_config=Configure.multi_tenancy(True)
)

Read a single collection definition
Retrieve a collection definition from the schema.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
articles = client.collections.get("Article")
articles_config = articles.config.get()

print(articles_config)

Read all collection definitions
Fetch the database schema to retrieve all of the collection definitions.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
response = client.collections.list_all(simple=False)

print(response)

Update a collection definition
Replication factor change in v1.25
In Weaviate v1.25, a replication factor cannot be changed once it is set.

This is due to the schema consensus algorithm change in v1.25. This will be improved in future versions.

You can update a collection definition to change the mutable collection settings.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Java
Go
from weaviate.classes.config import Reconfigure, VectorFilterStrategy

articles = client.collections.get("Article")

# Update the collection definition
articles.config.update(
    inverted_index_config=Reconfigure.inverted_index(
        bm25_k1=1.5
    ),
    vector_index_config=Reconfigure.VectorIndex.hnsw(
        filter_strategy=VectorFilterStrategy.ACORN  # Available from Weaviate v1.27.0
    )
)
articles = client.collections.get("Article")

article_shards = articles.config.update_shards(
    status="READY",
    shard_names=shard_names  # The names (List[str]) of the shard to update (or a shard name)
)

print(article_shards)

Update a parameter
Some parameters cannot be modified after you create your collection.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
from weaviate.classes.config import Reconfigure

# Get the Article collection object
articles = client.collections.get("Article")

# Update the collection configuration
articles.config.update(
    # Note, use Reconfigure here (not Configure)
    inverted_index_config=Reconfigure.inverted_index(
        stopwords_removals=["a", "the"]
    )
)

Delete a collection
You can delete any unwanted collection(s), along with the data that they contain.

Deleting a collection also deletes its objects
When you delete a collection, you delete all associated objects!

Be very careful with deletes on a production database and anywhere else that you have important data.

This code deletes a collection and its objects.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
Curl
# collection_name can be a string ("Article") or a list of strings (["Article", "Category"])
client.collections.delete(collection_name)  # THIS WILL DELETE THE SPECIFIED COLLECTION(S) AND THEIR OBJECTS

# Note: you can also delete all collections in the Weaviate instance with:
# client.collections.delete_all()

Add a property
Indexing limitations after data import
Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
from weaviate.classes.config import Property, DataType

articles = client.collections.get("Article")

articles.config.add_property(
    Property(
        name="onHomepage",
        data_type=DataType.BOOL
    )
)

Inspect shards (for a collection)
An index itself can be comprised of multiple shards.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
articles = client.collections.get("Article")

article_shards = articles.config.get_shards()
print(article_shards)

Update shard status
You can manually update a shard to change it's status. For example, update the shard status from READONLY to READY after you make other changes.

Python Client v4
Python Client v3
JS/TS Client v3
JS/TS Client v2
Go
Java
articles = client.collections.get("Article")

article_shards = articles.config.update_shards(
    status="READY",
    shard_names=shard_names  # The names (List[str]) of the shard to update (or a shard name)
)

print(article_shards)
