import json
import jsonschema
from jsonschema import validate, RefResolver
from referencing import Registry, Resource

# Load the schema
schema_url = (
    "https://jorcleme.github.io/cisco-business-json-schemas/schemas/videos/videos.json"
)
schema = {"$ref": schema_url}

# Define a registry and register the schema
registry = Registry().with_resource(Resource.from_contents(schema), schema_url)

# Create a resolver with the registry
resolver = RefResolver.from_schema(schema, registry=registry)

try:
    # Validate the data with the custom resolver
    validate(instance=data, schema=schema, resolver=resolver)
    print("Validation successful!")
except jsonschema.exceptions.ValidationError as e:
    print(f"Validation error: {e.message}")
