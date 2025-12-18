#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
MikesVersionModifier.py





"""
__version__ = "0.0.1.140-release"
__author__ = "Mike Merrett"
__updated__ = "2025-12-17 22:54:09"
###############################################################################


import os
import re
import pathspec

# -----------------------------------------------------------------
def load_gitignore(directory, logger=None):
    """Load .gitignore patterns if present."""
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            patterns = f.read().splitlines()
        if logger:
            logger.tracew(f"Loaded .gitignore from {gitignore_path}")
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return None

# -----------------------------------------------------------------
def version_replacer(match, new_suffix, logger=None):
    """
    Replace the 4th number (build) and suffix.
    new_suffix should look like "136-dev" or "200-qa".
    """
    major, minor, patch, build = match.group(2), match.group(3), match.group(4), match.group(5)
    extra_build = match.group(6)  # optional numeric part like 127
    old_suffix = match.group(7)

    # Parse new_suffix into build + label
    try:
        build_part, label = new_suffix.split("-", 1)
    except ValueError:
        if logger:
            logger.error(f"Invalid suffix format: {new_suffix}. Expected like '136-dev'")
        return match.group(0)

    # Use the new build number directly
    new_build = build_part

    return f'{match.group(1)}{major}.{minor}.{patch}.{new_build}-{label}{match.group(8)}'




# -----------------------------------------------------------------
def processFile(new_suffix, version_pattern, root, file, logger=None):
    """Process a single .py file and update its __version__ string."""
    file_path = os.path.join(root, file)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, count = version_pattern.subn(
        lambda m: version_replacer(m, new_suffix, logger), content
    )

    if count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        if logger:
            logger.info(f"Updated: {file_path}")

# -----------------------------------------------------------------
def update_version_suffix(directory, new_suffix, logger=None):
    """
    Traverse all .py files in a directory, normalize __version__ to 4 numbers + suffix.
    """
    version_pattern = re.compile(
        r'(__version__\s*=\s*[\'"])(\d+)\.(\d+)\.(\d+)\.(\d+)(?:-(\d+))?-(dev|qa|test|release)([\'"])'
    )

    spec = load_gitignore(directory, logger)

    if logger:
        logger.traceb(f"Starting version suffix update... {new_suffix=}")

    for root, dirs, files in os.walk(directory):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not (spec and spec.match_file(os.path.relpath(os.path.join(root, d), directory)))]

        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), directory)
            if file.endswith(".py") and not (spec and spec.match_file(rel_path)):
                # if logger:
                #     logger.tracew(f"Processing {rel_path}")
                processFile(new_suffix, version_pattern, root, file, logger)

# -----------------------------------------------------------------
if __name__ == "__main__":
    # Example usage: replace with your logger setup
    directory = "D:/_Python_Projects/MikesToolsLibrary"
    new_suffix = "dev"  # or "qa", "test", "release"
    update_version_suffix(directory, new_suffix)