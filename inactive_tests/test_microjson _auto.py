import json
import pytest
from pydantic import ValidationError
from microjson import MicroJSONAuto, GeoJSONAuto
import os

# Define the directories containing the example JSON files
VALID_EXAMPLES_DIR = 'tests/geojson/json/valid'
INVALID_EXAMPLES_DIR = 'tests/geojson/json/invalid'


def gather_example_files(directory):
    files = []
    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(directory):
        # Filter to just the .json files
        example_files = [os.path.join(dirpath, f)
                         for f in filenames if f.endswith('.json')]
        files.extend(example_files)
    return files


valid_examples = gather_example_files(VALID_EXAMPLES_DIR)
invalid_examples = gather_example_files(INVALID_EXAMPLES_DIR)


@pytest.mark.parametrize("filename", valid_examples)
def test_valid_geojsons(filename):
    with open(filename, 'r') as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a GeoJSON object
    try:
        _ = GeoJSONAuto.parse_obj(data)
    except ValidationError as e:
        pytest.fail(f"""ValidationError occurred
                    during validation of {filename}: {str(e)}""")
    except Exception as e:
        pytest.fail(f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}""")


@pytest.mark.parametrize("filename", invalid_examples)
def test_invalid_geojsons(filename):
    with open(filename, 'r') as f:
        data = json.load(f, strict=True)

    # This will raise a ValidationError if the data does not match the GeoJSON
    try:
        _ = GeoJSONAuto.parse_obj(data)
        pytest.fail(f"""Parsing succeeded on {filename},
                    but it should not have.""")
    except ValidationError:
        # The validation error is expected, so we just pass
        pass
    except Exception as e:
        # An unexpected error occurred, so we fail the test
        pytest.fail(f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}""")


@pytest.mark.parametrize("filename", valid_examples)
def test_valid_microjsons(filename):
    with open(filename, 'r') as f:
        data = json.load(f, strict=True)

    # Try to parse the data as a GeoJSON object
    try:
        _ = MicroJSONAuto.parse_obj(data)
    except ValidationError as e:
        pytest.fail(f"""ValidationError occurred
                    during validation of {filename}: {str(e)}""")
    except Exception as e:
        pytest.fail(f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}""")


@pytest.mark.parametrize("filename", invalid_examples)
def test_invalid_microjsons(filename):
    with open(filename, 'r') as f:
        data = json.load(f, strict=True)

    # This will raise a ValidationError if the data does not
    # match the GeoJSON schema
    try:
        _ = MicroJSONAuto.parse_obj(data)
        pytest.fail(f"""Parsing succeeded on {filename},
                    but it should not have.""")
    except ValidationError:
        # The validation error is expected, so we just pass
        pass
    except Exception as e:
        # An unexpected error occurred, so we fail the test
        pytest.fail(f"""Unexpected error occurred
                    during validation of {filename}: {str(e)}""")
