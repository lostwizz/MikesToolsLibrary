#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
MikesVersionModifier.py


Version format:
• 2 = major
• 3 = minor
• 4 = patch
• 5 = build
• 6 = suffix label (dev, qa, test, release)
"""
__version__ = "0.3.1.00193-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-18 00:40:22"
###############################################################################

import os
import re
import pathspec
import argparse

# -----------------------------------------------------------------
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
# Regex: __version__ = "X.Y.Z.N-suffix"
version_pattern = re.compile(
    r'(__version__\s*=\s*[\'"])(\d+)\.(\d+)\.(\d+)\.(\d+)-([\w\-]+)([\'"])'
)


# -----------------------------------------------------------------
def version_replacer(match, new_suffix, bump=None, set_values=None, logger=None):
    # Extract version components from regex groups
    major = int(match.group(2))
    minor = int(match.group(3))
    patch = int(match.group(4))
    build = int(match.group(5))
    suffix = match.group(6)

    # Parse new_suffix like "145-dev" or just "qa"
    if "-" in new_suffix:
        build_part, label = new_suffix.split("-", 1)
        if build_part.isdigit():
            build = int(build_part)
            suffix = label
        else:
            suffix = new_suffix
    else:
        suffix = new_suffix

    # Apply explicit set values if provided
    if set_values:
        major = int(set_values.get("major", major))
        minor = int(set_values.get("minor", minor))
        patch = int(set_values.get("patch", patch))
        build = int(set_values.get("build", build))

    # Apply bump logic (support list of bumps)
    if bump:
        if isinstance(bump, str):
            bump = [bump]
        for b in bump:
            if b == "major":
                major += 1
                minor = 0
                patch = 0
                # build stays unchanged
            elif b == "minor":
                minor += 1
                patch = 0
                # build stays unchanged
            elif b == "patch":
                patch += 1
                # build stays unchanged
            elif b == "build":
                build += 1

    # Return the new version string with build padded to 5 digits
    return f'{match.group(1)}{major}.{minor}.{patch}.{build:05d}-{suffix}{match.group(7)}'


# -----------------------------------------------------------------
def processFile(new_suffix, version_pattern, root, file, bump=None, set_values=None, logger=None):
    """Process a single .py file and update its __version__ string."""

    # if file != "versionExample.py" and file != "MikesVersionModifier.py":
    #     return # skip other files for now

    # if logger:
    #     logger.tracej(f"Processing file: {os.path.join(root, file)}")

    file_path = os.path.join(root, file)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, count = version_pattern.subn(
        lambda m: version_replacer(m, new_suffix, bump=bump, set_values=set_values, logger=logger),
        content
    )

    if count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        if logger:
            logger.info(f"Updated: {file_path}")

# -----------------------------------------------------------------
def update_version_suffix(directory, new_suffix, bump=None, set_values=None, logger=None):
    """
    Traverse all .py files in a directory, normalize __version__ to 4 numbers + suffix.
    bump: which segment to increment ("major","minor","patch","build").
    set_values: dict to explicitly set version numbers.
    """
    spec = load_gitignore(directory, logger)

    if logger:
        logger.traceb(f"Starting version suffix update... {new_suffix=} {bump=} {set_values=}")

    for root, dirs, files in os.walk(directory):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not (spec and spec.match_file(os.path.relpath(os.path.join(root, d), directory)))]

        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), directory)
            if file.endswith(".py") and not (spec and spec.match_file(rel_path)):
                processFile(new_suffix, version_pattern, root, file, bump=bump, set_values=set_values, logger=logger)


# -----------------------------------------------------------------
def validate_version_lines(content, file_path, logger=None):
    matches = version_pattern.findall(content)
    if len(matches) == 0:
        if logger: logger.error(f"No __version__ line found in {file_path}")
        return False
    elif len(matches) > 1:
        if logger: logger.error(f"Multiple __version__ lines found in {file_path}")
        return False
    return True

# -----------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update __version__ strings in Python files.")

    # suffix argument
    parser.add_argument("--suffix", required=True,
                        help="New suffix (e.g. dev, qa, release)")

    # bump argument: allow multiple values
    parser.add_argument("--bump", nargs="+",
                        choices=["major", "minor", "patch", "build"],
                        help="Which version segments to bump (can specify multiple)")

    # set argument: allow explicit values like major=1 minor=0
    parser.add_argument("--set", nargs="*",
                        help="Explicitly set version numbers, e.g. major=1 minor=0 patch=0 build=5")

    # directory argument: default to your project root
    parser.add_argument("--directory", default="D:/_Python_Projects/MikesToolsLibrary",
                        help="Root directory to traverse")

    args = parser.parse_args()

    # Parse set values into dict
    set_values = None
    if args.set:
        set_values = {}
        for kv in args.set:
            key, val = kv.split("=")
            set_values[key] = int(val)

    # Call your updater
    update_version_suffix(
        args.directory,
        new_suffix=args.suffix,
        bump=args.bump,
        set_values=set_values
    )