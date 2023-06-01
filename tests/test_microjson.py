import json
import pytest
from pydantic import ValidationError
from microjson import MicroJSON  # Import your MicroJSON Pydantic model


def test_valid_microjson():
    # This is an example of a valid MicroJSON document
    valid_microjson = {
        "type": "FeatureCollection",
        "coordinatesystem": {
            "axes": ["x", "y", "z"],
            "units": ["pixel", "pixel", "pixel"],
            "pixelsPerUnit": [1.0, 1.0, 1.0]
        },
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "id": "1",
                    "type": "type1"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [1.0, 2.0, 3.0]
                }
            }
        ],
        "geometries": []
    }

    try:
        valid_microjson_str = json.dumps(valid_microjson)
        MicroJSON.parse_raw(valid_microjson_str)
    except ValidationError:
        pytest.fail("Valid MicroJSON raised ValidationError")


def test_invalid_microjson():
    # This is an example of an invalid MicroJSON document
    invalid_microjson = {
        "type": "FeatureCollection",
        "coordinates": {"axes": ["invalid_axis", "y", "z"]},
        "features": [],
        # Add all the required fields
    }
    with pytest.raises(ValidationError):
        invalid_microjson_str = json.dumps(invalid_microjson)
        MicroJSON.parse_raw(invalid_microjson_str)

