import os


def gather_example_files(directory) -> list:
    """
    Gather all the .json files in a directory and its subdirectories.
    """
    files = []
    # Walk through the directory
    for dirpath, _, filenames in os.walk(directory):
        # Filter to just the .json files
        example_files = [
            os.path.join(dirpath, f) for f in filenames if f.endswith(".json")
        ]
        files.extend(example_files)
    return files
