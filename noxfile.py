from nox_poetry import session


@session(python="3.9")
def export_ts(session):
    #session.install("-r", "requirements-dev.txt")
    #session.install("-e", ".")
    session.install("microjson")
    session.run("datamodel-codegen",
                "--reuse-model",
                "--snake-case-field",
                "--input", "external",
                "--output", "geojson",
                "--target", "3.9")
    session.run("pydantic2ts", "--module", "microjson/model.py",
                "--output", "microjsonschema.ts")

    # generate GeoJSON schema
    from microjson.modelv1 import GeoJSON
    # Get the schema for the model as a dictionary
    schema_dict = GeoJSON.schema()
    # Add 'null' to the list of allowed types for the 'geometry' field of 
    # Feature object
    schema_dict = schema_dict['definitions']['Feature']
    schema_dict['properties']['geometry']['anyOf'].append({'type': 'null'})
    with open('geojson_schema.json', 'w') as f:
        f.write(GeoJSON.schema_json(indent=2))

    from microjson.modelv1 import MicroJSON
    with open('microjson_schema.json', 'w') as f:
        f.write(MicroJSON.schema_json(indent=2))
    
    # generate pydantic model from the GeoJSON schema
    session.run("datamodel-codegen",
                "--reuse-model",
                "--snake-case-field",
                "--input", "geojson_schema.json",
                "--output", "geojson/roundtrip.py",
                "--target", "3.9")

    # generate pydantic model from the MicroJSON schema
    session.run("datamodel-codegen",
                "--reuse-model",
                "--snake-case-field",
                "--input", "microjson_schema.json",
                "--output", "microjson/roundtrip.py",
                "--target", "3.9")

