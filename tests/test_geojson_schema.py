import json
import jsonschema
import pytest
from jsonschema import validate

from microjson.utils import gather_example_files

# Load the generated GeoJSON schema
with open("geojson_schema.json") as f:
    schema = json.load(f)

# Define the directories containing the example JSON files
VALID_EXAMPLES_DIR = "tests/json/geojson/valid"
INVALID_EXAMPLES_DIR = "tests/json/geojson/invalid"

# Gather the example files
valid_examples = gather_example_files(VALID_EXAMPLES_DIR)
invalid_examples = gather_example_files(INVALID_EXAMPLES_DIR)


@pytest.mark.parametrize("filename", valid_examples)
def test_valid_geojsons(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a GeoJSON object
    try:
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        pytest.fail(f"JSON Schema validation failed. Error: {err}")
    except Exception as e:
        pytest.fail(
            f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}"""
        )


@pytest.mark.parametrize("filename", invalid_examples)
def test_invalid_geojsons(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a GeoJSON object
    try:
        validate(instance=data, schema=schema)
        pytest.fail(
            f"""Parsing succeeded on {filename},
                    but it should not have."""
        )
    except jsonschema.exceptions.ValidationError:
        # The validation error is expected, so we just pass
        pass
    except Exception as e:
        # An unexpected error occurred, so we fail the test
        pytest.fail(
            f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}"""
        )
