import json
import pytest
from pydantic import ValidationError
from microjson.model import MicroJSON, GeoJSON
from microjson.fileutils import gather_example_files


# Define the directories containing the example JSON files
VALID_EXAMPLES_DIR = "tests/json/geojson/valid"
INVALID_EXAMPLES_DIR = "tests/json/geojson/invalid"
VALID_MICROJSON_DIR = "tests/json/microjson/valid"
INVALID_MICROJSON_DIR = "tests/json/microjson/invalid"


valid_examples = gather_example_files(VALID_EXAMPLES_DIR)
invalid_examples = gather_example_files(INVALID_EXAMPLES_DIR)
valid_microjson = gather_example_files(VALID_MICROJSON_DIR) + valid_examples
invalid_microjson = gather_example_files(
    INVALID_MICROJSON_DIR) + invalid_examples


@pytest.mark.parametrize("filename", valid_examples)
def test_valid_geojson(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a GeoJSON object
    try:
        _ = GeoJSON.model_validate(data)
    except ValidationError as e:
        pytest.fail(
            f"""ValidationError occurred
                    during validation of {filename}: {str(e)}"""
        )
    except Exception as e:
        pytest.fail(
            f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}"""
        )


@pytest.mark.parametrize("filename", invalid_examples)
def test_invalid_geojson(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # This will raise a ValidationError if the data does not match the GeoJSON
    try:
        _ = GeoJSON.model_validate(data)
        pytest.fail(
            f"""Parsing succeeded on {filename},
                    but it should not have."""
        )
    except ValidationError:
        # The validation error is expected, so we just pass
        pass
    except Exception as e:
        # An unexpected error occurred, so we fail the test
        pytest.fail(
            f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}"""
        )


@pytest.mark.parametrize("filename", valid_microjson)
def test_valid_microjson(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a MicroJSON object
    try:
        _ = MicroJSON.model_validate(data)
    except ValidationError as e:
        pytest.fail(
            f"""ValidationError occurred
                    during validation of {filename}: {str(e)}"""
        )
    except Exception as e:
        pytest.fail(
            f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}"""
        )


@pytest.mark.parametrize("filename", invalid_microjson)
def test_invalid_microjson(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # This will raise a ValidationError if the data does not
    # match the MicroJSON schema
    try:
        _ = MicroJSON.model_validate(data)
        pytest.fail(
            f"""Parsing succeeded on {filename},
                    but it should not have."""
        )
    except ValidationError:
        # The validation error is expected, so we just pass
        pass
    except Exception as e:
        # An unexpected error occurred, so we fail the test
        pytest.fail(
            f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}"""
        )
