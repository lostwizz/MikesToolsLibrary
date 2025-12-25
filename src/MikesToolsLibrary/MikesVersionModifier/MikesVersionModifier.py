#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
MikesVersionManager.py

Unified version management with:
- Single authoritative version file (TOML)
- Plugin-style file updaters (Python, BAT, INI, TOML, easily extendable)
- Bump / set / suffix logic
- Dry-run mode
- Optional Git commit of version bump

Version format:
• 2 = major
• 3 = minor
• 4 = patch
• 5 = build
• 6 = suffix label (dev, qa, test, release)
"""
__version__ = "0.1.2.00322-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-24 19:27:48"
###############################################################################

import os
import re
import argparse
import subprocess
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pathspec

# from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MikesLogging import get_logger
logger = get_logger(__name__)

#-----------------------------------------------------------------
# Python 3.11+: tomllib is stdlib; for 3.10- you'd use tomli / tomli-w instead.
try:
    import tomllib  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("Python 3.11+ is required (tomllib).")

try:
    import tomli_w  # pip install tomli-w
except ImportError:  # pragma: no cover
    raise SystemExit("Please install tomli-w: pip install tomli-w")




###############################################################################
# Logging setup
###############################################################################


#-----------------------------------------------------------------
# def setup_logger(verbose: bool = False) -> logging.Logger:
    # logger = logging.getLogger("version_manager")
    # logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # handler = logging.StreamHandler()
    # fmt = logging.Formatter("%(levelname)s: %(message)s")
    # handler.setFormatter(fmt)
    # logger.handlers.clear()
    # logger.addHandler(handler)

    # return logger
    from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
    


###############################################################################
# Git ignore handling
###############################################################################


#-----------------------------------------------------------------
def load_gitignore(directory: str, logger: Optional[logging.Logger] = None):
    """Load .gitignore patterns if present."""
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            patterns = f.read().splitlines()
        if logger:
            logger.debug(f"Loaded .gitignore from {gitignore_path}")
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return None


###############################################################################
# Version data model and operations
###############################################################################

#-----------------------------------------------------------------
@dataclass
class Version:
    major: int
    minor: int
    patch: int
    build: int
    suffix: str

    #-----------------------------------------------------------------
    @classmethod
    def from_dict(cls, d: Dict) -> "Version":
        return cls(
            major=int(d["major"]),
            minor=int(d["minor"]),
            patch=int(d["patch"]),
            build=int(d["build"]),
            suffix=str(d["suffix"]),
        )

    #-----------------------------------------------------------------
    def to_dict(self) -> Dict:
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "build": self.build,
            "suffix": self.suffix,
        }

    #-----------------------------------------------------------------
    def as_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}.{self.build:05d}-{self.suffix}"


#-----------------------------------------------------------------
# def load_version_file(path: str, logger: Optional[logging.Logger] = None) -> Version:
def load_version_file(path: str, logger=None) -> Version:
    if logger:
        logger.debug(f"Loading version from {path}")
    with open(path, "rb") as f:
        data = tomllib.load(f)
    v = Version.from_dict(data["version"])
    if logger:
        logger.info(f"Loaded version: {v.as_string()}")
    return v


#-----------------------------------------------------------------
def save_version_file(
    version: Version, path: str, logger: Optional[logging.Logger] = None
) -> None:
    if logger:
        logger.debug(f"Saving version to {path}: {version.as_string()}")
    with open(path, "wb") as f:
        tomli_w.dump({"version": version.to_dict()}, f)


#-----------------------------------------------------------------
def apply_set_values(version: Version, set_values: Dict[str, int]) -> None:
    for key in ("major", "minor", "patch", "build"):
        if key in set_values:
            setattr(version, key, int(set_values[key]))


#-----------------------------------------------------------------
def apply_bumps(version: Version, bumps: List[str]) -> None:
    for b in bumps:
        if b == "major":
            version.major += 1
            version.minor = 0
            version.patch = 0
            # build unchanged
        elif b == "minor":
            version.minor += 1
            version.patch = 0
            # build unchanged
        elif b == "patch":
            version.patch += 1
            # build unchanged
        elif b == "build":
            version.build += 1


###############################################################################
# Plugin-style updaters
###############################################################################


#-----------------------------------------------------------------
class FileUpdater:
    """Base class for file updaters."""

    extensions: Tuple[str, ...] = ()

    def update(
        self, content: str, version: Version, logger: Optional[logging.Logger] = None
    ) -> Tuple[str, int]:
        """Return (new_content, replacements_count)."""
        raise NotImplementedError


#-----------------------------------------------------------------
class PythonFileUpdater(FileUpdater):
    extensions = (".py",)

    # __version__ = "X.Y.Z.N-suffix"
    pattern = re.compile(
        r'(__version__\s*=\s*[\'"])(\d+\.\d+\.\d+\.\d+-[\w\-]+)([\'"])'
    )

    def update(
        self, content: str, version: Version, logger: Optional[logging.Logger] = None
    ) -> Tuple[str, int]:
        new_version = version.as_string()

        def repl(m: re.Match) -> str:
            old = m.group(2)
            if logger:
                logger.debug(f"Python: {old} -> {new_version}")
            return f"{m.group(1)}{new_version}{m.group(3)}"

        return self.pattern.subn(repl, content)


#-----------------------------------------------------------------
class BatFileUpdater(FileUpdater):
    extensions = (".bat", ".cmd")

    # set VERSION=1.2.3.00001-dev
    pattern = re.compile(
        r'(set\s+version\s*=\s*)(\d+\.\d+\.\d+\.\d+-[\w\-]+)', re.IGNORECASE
    )

    def update(
        self, content: str, version: Version, logger: Optional[logging.Logger] = None
    ) -> Tuple[str, int]:
        new_version = version.as_string()

        def repl(m: re.Match) -> str:
            old = m.group(2)
            if logger:
                logger.debug(f"BAT: {old} -> {new_version}")
            return f"{m.group(1)}{new_version}"

        return self.pattern.subn(repl, content)


#-----------------------------------------------------------------
class IniFileUpdater(FileUpdater):
    extensions = (".ini", ".cfg")

    # version = 1.2.3.00001-dev
    pattern = re.compile(
        r'(version\s*=\s*)(\d+\.\d+\.\d+\.\d+-[\w\-]+)', re.IGNORECASE
    )

    def update(
        self, content: str, version: Version, logger: Optional[logging.Logger] = None
    ) -> Tuple[str, int]:
        new_version = version.as_string()

        def repl(m: re.Match) -> str:
            old = m.group(2)
            if logger:
                logger.debug(f"INI: {old} -> {new_version}")
            return f"{m.group(1)}{new_version}"

        return self.pattern.subn(repl, content)


#-----------------------------------------------------------------
class TomlFileUpdater(FileUpdater):
    extensions = (".toml",)

    # version = "1.2.3.00001-dev"
    pattern = re.compile(
        r'(version\s*=\s*")(.*?)(")', re.IGNORECASE
    )

    def update(
        self, content: str, version: Version, logger: Optional[logging.Logger] = None
    ) -> Tuple[str, int]:
        new_version = version.as_string()

        def repl(m: re.Match) -> str:
            old = m.group(2)
            if logger:
                logger.debug(f"TOML: {old} -> {new_version}")
            return f'{m.group(1)}{new_version}{m.group(3)}'

        return self.pattern.subn(repl, content)


#-----------------------------------------------------------------
UPDATERS: List[FileUpdater] = [
    PythonFileUpdater(),
    BatFileUpdater(),
    IniFileUpdater(),
    TomlFileUpdater(),
]


#-----------------------------------------------------------------
def get_updater_for_file(filename: str) -> Optional[FileUpdater]:
    ext = os.path.splitext(filename)[1].lower()
    for updater in UPDATERS:
        if ext in updater.extensions:
            return updater
    return None


###############################################################################
# Core processing
###############################################################################


#-----------------------------------------------------------------
def process_file(
    root: str,
    file: str,
    version: Version,
    dry_run: bool,
    logger: Optional[logging.Logger],
) -> Optional[str]:
    """Process a single file. Returns path if changed, else None."""
    updater = get_updater_for_file(file)
    if updater is None:
        return None

    file_path = os.path.join(root, file)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        if logger:
            logger.warning(f"Skipping non-text file: {file_path}")
        return None

    new_content, count = updater.update(content, version, logger=logger)

    if count == 0:
        return None

    if dry_run:
        if logger:
            logger.info(f"[DRY-RUN] Would update: {file_path} ({count} occurrences)")
        return None

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    if logger:
        logger.info(f"Updated: {file_path} ({count} occurrences)")
    return file_path


#-----------------------------------------------------------------
def update_tree(
    directory: str,
    version: Version,
    dry_run: bool,
    logger: Optional[logging.Logger] = None,
) -> List[str]:
    """Walk directory tree, update files, return list of changed file paths."""
    spec = load_gitignore(directory, logger)
    changed_files: List[str] = []

    if logger:
        logger.debug(f"Starting traversal in {directory}")

    for root, dirs, files in os.walk(directory):
        # Filter ignored directories
        dirs[:] = [
            d
            for d in dirs
            if not (
                spec
                and spec.match_file(os.path.relpath(os.path.join(root, d), directory))
            )
        ]

        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), directory)
            if spec and spec.match_file(rel_path):
                if logger:
                    logger.debug(f"Skipping ignored file: {rel_path}")
                continue

            changed = process_file(root, file, version, dry_run, logger)
            if changed:
                changed_files.append(os.path.abspath(changed))

    return changed_files


###############################################################################
# Git integration
###############################################################################


#-----------------------------------------------------------------
def git_commit(
    repo_dir: str,
    files: List[str],
    message: str,
    logger: Optional[logging.Logger] = None,
) -> None:
    if not files:
        if logger:
            logger.info("No files changed; skipping Git commit.")
        return

    # Ensure paths are relative to repo_dir for git
    rel_files = [os.path.relpath(f, repo_dir) for f in files]

    if logger:
        logger.info(f"Adding files to Git: {rel_files}")

    subprocess.run(["git", "-C", repo_dir, "add"] + rel_files, check=True)

    if logger:
        logger.info(f"Committing with message: {message}")

    subprocess.run(["git", "-C", repo_dir, "commit", "-m", message], check=True)

    if logger:
        logger.info("Git commit completed.")


###############################################################################
# CLI
###############################################################################


#-----------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Unified version manager: bump version and sync across files."
    )

    parser.add_argument(
        "--directory",
        default=".",
        help="Root directory to traverse (project root).",
    )

    parser.add_argument(
        "--version-file",
        default="version.toml",
        help="Path to TOML version file (relative to directory or absolute).",
    )

    parser.add_argument(
        "--suffix",
        help="New suffix (e.g. dev, qa, test, release). If omitted, keep existing.",
    )

    parser.add_argument(
        "--bump",
        nargs="+",
        choices=["major", "minor", "patch", "build"],
        help="Which version segments to bump (can specify multiple).",
    )

    parser.add_argument(
        "--set",
        nargs="*",
        help=(
            "Explicitly set version numbers, e.g.: "
            "major=1 minor=0 patch=0 build=5"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write any files; just show what would change.",
    )

    parser.add_argument(
        "--git-commit",
        action="store_true",
        help="Commit version bump to Git (requires clean repo state).",
    )

    parser.add_argument(
        "--git-message",
        default="chore: bump version",
        help="Git commit message to use with --git-commit.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging.",
    )

    return parser.parse_args()




#-----------------------------------------------------------------
def update_version_suffix(directory, new_suffix=None, bump=None, set_values=None, logger=None):
    version = load_version_file("version.toml", logger=logger)

    if set_values:
        for key, value in set_values.items():
            setattr(version, key, value)

    if bump:
        version.apply_bump(bump)

    if new_suffix:
        version.suffix = new_suffix

    save_version_file(version, "version.toml", logger=logger)

    return update_tree(directory, version, dry_run=False, logger=logger)



#-----------------------------------------------------------------
def main() -> None:
    args = parse_args()
    # logger = setup_logger(verbose=args.verbose)
    logger = LoggerSetup().get_logger("version_modifier")


    project_root = os.path.abspath(args.directory)
    version_file = args.version_file
    if not os.path.isabs(version_file):
        version_file = os.path.join(project_root, version_file)

    if not os.path.exists(version_file):
        logger.error(f"Version file not found: {version_file}")
        raise SystemExit(1)

    version = load_version_file(version_file, logger=logger)
    # version = load_version_file(version_file)

    # Parse set values
    set_values: Dict[str, int] = {}
    if args.set:
        for kv in args.set:
            if "=" not in kv:
                logger.error(f"Invalid --set argument: {kv}")
                raise SystemExit(1)
            key, val = kv.split("=", 1)
            if key not in ("major", "minor", "patch", "build"):
                logger.error(f"Unknown version key in --set: {key}")
                raise SystemExit(1)
            set_values[key] = int(val)

    # Apply explicit sets
    if set_values:
        apply_set_values(version, set_values)

    # Apply bumps
    if args.bump:
        apply_bumps(version, args.bump)

    # Apply suffix change
    if args.suffix:
        logger.debug(f"Changing suffix: {version.suffix} -> {args.suffix}")
        version.suffix = args.suffix

    logger.info(f"New version: {version.as_string()}")

    # Save version file (unless dry-run)
    changed_files: List[str] = []
    if args.dry_run:
        logger.info("[DRY-RUN] Would update version file and project files.")
    else:
        save_version_file(version, version_file, logger=logger)
        changed_files.append(os.path.abspath(version_file))

    # Update other files
    changed_in_tree = update_tree(
        project_root, version, dry_run=args.dry_run, logger=logger
    )
    changed_files.extend(changed_in_tree)

    if args.dry_run:
        logger.info("[DRY-RUN] No files were modified.")
        return

    logger.info(f"Total files changed: {len(changed_files)}")

    # Optional Git commit
    if args.git_commit:
        try:
            git_commit(
                repo_dir=project_root,
                files=changed_files,
                message=args.git_message,
                logger=logger,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            raise SystemExit(1)



#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
if __name__ == "__main__":
    main()


    