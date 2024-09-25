import json
import pytest
from pydantic import ValidationError
from microjson.tilemodel import TileJSON
from microjson.fileutils import gather_example_files


# Define the directories containing the example JSON files
VALID_EXAMPLES_DIR = "tests/json/tilejson/valid"
INVALID_EXAMPLES_DIR = "tests/json/tilejson/invalid"


valid_examples = gather_example_files(VALID_EXAMPLES_DIR)
invalid_examples = gather_example_files(INVALID_EXAMPLES_DIR)


@pytest.mark.parametrize("filename", valid_examples)
def test_valid_tilejson(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a TileJSON object
    try:
        _ = TileJSON.model_validate(data)
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
def test_invalid_tilejson(filename):
    with open(filename, "r") as f:
        data = json.load(f, strict=True)

    # This will raise a ValidationError if the data does not match the TileJSON
    try:
        _ = TileJSON.model_validate(data)
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
