import nox
from microjson.model import GeoJSON, MicroJSON
import json


@nox.session(python="3.9")
def generate_geojson_pydantic(session):
    session.install("-r", "requirements-dev.txt")
    session.install("-e", ".")
    session.run("datamodel-codegen",
                "--reuse-model",
                "--snake-case-field",
                "--input", "external",
                "--output", "geojson",
                "--target", "3.9")


@nox.session(python="3.9")
def generate_roundtrip_json_schema(session):
    session.install("-r", "requirements-dev.txt")
    session.install("-e", ".")
    # generate GeoJSON schema
    # Get the schema for the model as a dictionary
    schema_dict = GeoJSON.model_json_schema()
    # Add 'null' to the list of allowed types for the 'geometry' field of
    # Feature object
    schema_dict = schema_dict['$defs']['Feature']
    schema_dict['properties']['geometry']['anyOf'].append({'type': 'null'})
    with open('geojson_schema.json', 'w') as f:
        f.write(json.dumps(GeoJSON.model_json_schema(), indent=4))

    with open('microjson_schema.json', 'w') as f:
        f.write(json.dumps(MicroJSON.model_json_schema(), indent=4))


@nox.session(python="3.9")
def generate_roundtrip_pydantic(session):
    # generate pydantic model from the GeoJSON schema
    session.install("-r", "requirements-dev.txt")
    session.run("datamodel-codegen",
                "--reuse-model",
                "--snake-case-field",
                "--input", "geojson_schema.json",
                "--output", "geojson/roundtrip.py",
                "--target", "3.9")


@nox.session
def typescript(session):
    # Install json-schema-to-typescript
    session.run("npm", "install", "json-schema-to-typescript", external=True)

    # Use json-schema-to-typescript
    session.run("npx",
                "json-schema-to-typescript",
                "microjson_schema.json",
                "-o",
                "microjson.d.ts",
                external=True)
