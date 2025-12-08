# version_utils.py
import pathlib
import sys

try:
    # Python 3.11+ has tomllib in the stdlib
    import tomllib
except ImportError:
    import tomli as tomllib  # fallback for older versions

def get_version() -> str:
    """
    Reads the version string from pyproject.toml.
    Returns it as a string, e.g. "1.2.3".
    """
    pyproject_path = pathlib.Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)

    # Works with PEP 621 standard metadata
    return data["project"]["version"]