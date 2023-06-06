import nox


@nox.session(python="3.9")
def export_ts(session):
    session.install("-r", "requirements-dev.txt")
    session.install("-e", ".")
    session.run("datamodel-codegen",
                "--reuse-model",
                "--snake-case-field",
                "--input", "external",
                "--output", "geojson",
                "--target", "3.9")
    session.run("pydantic2ts", "--module", "microjson/model.py",
                "--output", "microjsonschema.ts")

    # generate GeoJSON schema
    from microjson.model import GeoJSON
    with open('geojson_schema.json', 'w') as f:
        f.write(GeoJSON.schema_json(indent=2))

    from microjson.model import MicroJSON
    with open('microjson_schema.json', 'w') as f:
        f.write(MicroJSON.schema_json(indent=2))
