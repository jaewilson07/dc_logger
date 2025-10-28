#!/usr/bin/env python3
"""Sync version from pyproject.toml to __init__.py"""

import re
from pathlib import Path

import tomllib


def sync_version():
    # Read version from pyproject.toml
    pyproject_path = Path("pyproject.toml")
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)

    version = pyproject_data["project"]["version"]

    # Update __init__.py
    init_path = Path("src/dc_logger/__init__.py")
    init_content = init_path.read_text()

    # Replace version
    new_content = re.sub(
        r'__version__ = "[^"]+"', f'__version__ = "{version}"', init_content
    )

    if new_content != init_content:
        init_path.write_text(new_content)
        print(f"✓ Version synced to {version}")
        return 1  # Exit with 1 to indicate file was modified
    else:
        print(f"✓ Version already {version}")
        return 0


if __name__ == "__main__":
    exit(sync_version())
