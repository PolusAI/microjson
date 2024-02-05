import json
import pytest
from pydantic import ValidationError
from microjson.model import MicroJSON, GeoJSON
from microjson.utils import gather_example_files


# Define the directories containing the example JSON files
VALID_PROVENANCE_DIR = "tests/json/provenance/valid"
INVALID_PROVENANCE_DIR = "tests/json/provenance/invalid"



valid_examples = gather_example_files(VALID_PROVENANCE_DIR)
invalid_examples = gather_example_files(INVALID_PROVENANCE_DIR)


@pytest.mark.parametrize("filename", valid_examples)
def test_valid_provenance(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a GeoJSON object
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


@pytest.mark.parametrize("filename", invalid_examples)
def test_invalid_geojson(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # This will raise a ValidationError if the data does not match the GeoJSON
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
