#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
MikesVersionModifier.py

MikesSettings package
---------





"""
__version__ = "0.0.1.140-release"
__author__ = "Mike Merrett"
__updated__ = "2025-12-17 21:29:10"
###############################################################################

import sys

import os
import re

TEMPLATES = {
    "top_text": "\"###############################################################################\"",
    "filename_comment": lambda name: f"# {name}",
    "version": "__version__ = \"0.0.0.{build}\"",
    "author": "__author__ = \"Mike Merrett\"",
    "updated": "__updated__ = \"2025-07-28\""
}


def check_and_update_py_files(directory:str, build_number:str):
    version_pattern = re.compile(r"(__version__\s*=\s*['\"])(\d+\.\d+\.\d+)(?:\.\d+)?(['\"])")
    author_pattern = re.compile(r"__author__\s*=\s*['\"](.+?)['\"]")
    updated_pattern = re.compile(r"__updated__\s*=\s*['\"](.+?)['\"]")

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            print( f"{filepath=}")
            with open(filepath, "r") as f:
                lines = f.readlines()

            issues = []
            new_lines = lines[:]
            inserts = []

            # Top text string check
            if not lines or not re.match(r'^\s*[\'"].+[\'"]', lines[0]):
                inserts.append(TEMPLATES["top_text"] + "\n")
                issues.append("Inserted top text string")

            # Filename comment
            if not any(f"# {filename}" in line for line in lines):
                inserts.append(TEMPLATES["filename_comment"](filename) + "\n")
                issues.append("Inserted filename comment")

            # Version check + update
            version_found = False
            for idx, line in enumerate(new_lines):
                match = version_pattern.search(line)
                if match:
                    full, base_version, quote = match.group(1), match.group(2), match.group(3)
                    new_version = f"{base_version}.{build_number}"
                    new_lines[idx] = f"{full}{new_version}{quote}\n"
                    version_found = True
                    break
            if not version_found:
                inserts.append(TEMPLATES["version"].replace("{build}", str(build_number)) + "\n")
                issues.append("Inserted default __version__")

            # Author
            if not any(author_pattern.search(line) for line in new_lines):
                inserts.append(TEMPLATES["author"] + "\n")
                issues.append("Inserted __author__")

            # Updated
            if not any(updated_pattern.search(line) for line in new_lines):
                inserts.append(TEMPLATES["updated"] + "\n")
                issues.append("Inserted __updated__")

            # Inject missing metadata after any existing imports
            insert_index = next((i for i, line in enumerate(new_lines) if not line.strip().startswith("import")), 0)
            new_lines = new_lines[:insert_index] + inserts + new_lines[insert_index:]

            # Save updated file
            with open(filepath, "w") as f:
                f.writelines(new_lines)

            # Reporting
            if issues:
                print(f"🔧 {filename} - Fixed issues:")
                for issue in issues:
                    print(f"   ✅ {issue}")
            else:
                print(f"✅ {filename} - No issues found, version updated")

# Example usage
# check_and_update_py_files(r"D:\_Python_Projects\MasterCopyCommonCode", build_number=456)
# Example usage
build_number= read_and_increment_build()
logger.tracea( f"{build_number=}")
check_and_update_py_files(r"D:\_Python_Projects\MasterCopyCommonCode\stuff_dir", build_number=build_number)
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


# -----------------------------------------------------------------
if __name__ == "__main__":
    print("this must be called from another module")

    # mySettings.dump()

    sys.exit(-99)
