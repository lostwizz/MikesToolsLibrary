###############################################################################
'''
   MyUtil.py


   27Feb25 M.Merrett-

'''

__author__ = 'Mike Merrett'
__updated__ = '2025-08-02 03:46:05'
__version__ = "0.1.2.00322-dev"
###############################################################################

import socket
import re
import os
from datetime import datetime

from MyLogging import *

try:
    import arcpy
    arcpy_available = True
except ImportError:
    arcpy_available = False



#-----------------------------------------------------------------

def featureList(FC:str):
    fields = arcpy.ListFields(FC )
    for fld in fields:
        print( fld.name)
        #logger.traceh( fld.name)
    #logger.mark()
    print('---------------------------------------')

#-----------------------------------------------------------------
def TestSQLport():

    server_name = 'vm-db-prd4.city.local'
    port = 1433  # Default SQL Server port

    try:
        socket.create_connection(('vm-db-prd4', 1433), timeout=10)
        print("Server is reachable")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return  False


#-----------------------------------------------------------------
def dump_list( aList, loggerlevel_even=87, loggerlevel_odd=88 ):
    c =0
    # print( f"{type( aList) }")
    # if type(aList) ==list:
    for i  in aList:
        c +=1
        if c % 2 ==1:
            logger.log( loggerlevel_odd, f"aList={i}")
        else:
            logger.log( loggerlevel_even, f"aList={i}")
    # elif type(aList) == dict:
        # for index, (key, value) in enumerate(aList.items()):
            # c+= 1
            # if c % 2 ==1:
                # logger.log( loggerlevel_odd, f"Index {index}: Key = {key}, Value = {value}")
            # else:
                # logger.log( loggerlevel_even, f"Index {index}: Key = {key}, Value = {value}")




#-----------------------------------------------------------------
def compareDump( aDict, bDict, msg="", ignoreFields=[]):
    """
    Compare two dictionary-like objects and print the differences.

    Args:
        other: Another dictionary-like object to compare with.
        msg: An optional message to include in the output.
    """
    print(f"Compare {aDict.__class__.__name__}")
    for key in aDict.flds:
        a = str(aDict.get(key, ""))
        b = str(bDict.get(key, ""))

        c = ( "\x1b[0;34;40m", "<- {key.center(20)} -ignr ->")

        if key in ignoreFields:
            print(f"\x1b[0;34;40m {a.rjust(40)} <- {key.center(20)} -ignr -> {b}\x1b[0m")
        else:
            if a != b:
                print(f"\x1b[1;32;40m {a.rjust(40)} <- {key.center(20)} -Diff -> {b}\x1b[0m")

            else:
                print(f"\x1b[1;36;40m {a.rjust(40)} <- {key.center(20)} -Same -> {b}\x1b[0m")



#-----------------------------------------------------------------



#-----------------------------------------------------------------
HEADER_TEMPLATE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# {filename}
__version__ = "0.1.2.00322-dev"
__author__ = '{author}'
__updated__ = '2025-07-28 16:29:08'
###############################################################################
'''
DEFAULT_AUTHOR = "Mike Merrett"

#-----------------------------------------------------------------
def read_and_increment_build():
    build_num = mySettings.getRunCounter()
    new_build = f"{int(build_num):04}" if build_num else "0001"

    print(f"{new_build=}")
    return new_build


# # # # # # # # # # #-----------------------------------------------------------------
# # # # # # # # # # # def ensure_metadata(content: str, build: str, filename: str):
# # # # # # # # # # #     lines = content.splitlines()
# # # # # # # # # # #     updated = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

# # # # # # # # # # #     # Extract existing version base if present
# # # # # # # # # # #     version_pattern = re.compile(r"__version__\s*=\s*['\"](\d+\.\d+\.\d+)(?:\.(\d+))?['\"]")
# # # # # # # # # # #     version_match = version_pattern.search(content)

# # # # # # # # # # #     if version_match:
# # # # # # # # # # #         base_version = version_match.group(1)
# # # # # # # # # # #         version = f"{base_version}.{build}"
# # # # # # # # # # #     else:
# # # # # # # # # # #         version = f"0.0.0.{build}"  # fallback if not found

# # # # # # # # # # #     # 🛠 Apply updates to content
# # # # # # # # # # #     has_custom_header = any('__version__' in line for line in lines) and any('# -*- coding' in line for line in lines)

# # # # # # # # # # #     if not has_custom_header:
# # # # # # # # # # #         header = HEADER_TEMPLATE.format(
# # # # # # # # # # #             filename=filename,
# # # # # # # # # # #             build=build,
# # # # # # # # # # #             author=DEFAULT_AUTHOR,
# # # # # # # # # # #             updated=updated
# # # # # # # # # # #         )
# # # # # # # # # # #         new_lines = [header.strip()] + lines
# # # # # # # # # # #         return "\n".join(new_lines), version

# # # # # # # # # # #     updated_content = version_pattern.sub(lambda m: f"{m.group(0).split('.')[0]}.{build}'", content)

# # # # # # # # # # #     updated_pattern = re.compile(r"(__updated__\s*=\s*['\"])(.+?)(['\"])")
# # # # # # # # # # #     updated_content = updated_pattern.sub(lambda m: f"{m.group(1)}{updated}{m.group(3)}", updated_content)

# # # # # # # # # # #     return updated_content, version
# # # # # # # # # # def ensure_metadata(content: str, build: str, filename: str):
# # # # # # # # # #     updated = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

# # # # # # # # # #     # Regex to extract version (ideally in __version__)
# # # # # # # # # #     version_pattern = re.compile(r"__version__\s*=\s*['\"](\d+\.\d+\.\d+)(?:\.(\d+))?['\"]")
# # # # # # # # # #     version_match = version_pattern.search(content)

# # # # # # # # # #     if version_match:
# # # # # # # # # #         base_version = version_match.group(1)
# # # # # # # # # #         full_version = f"{base_version}.{build}"
# # # # # # # # # #         content = version_pattern.sub(f"__version__ = '{full_version}'", content)
# # # # # # # # # #     else:
# # # # # # # # # #         # Search loosely anywhere for a version-like string
# # # # # # # # # #         loose_match = re.search(r"(\d+\.\d+\.\d+)", content)
# # # # # # # # # #         base_version = loose_match.group(1) if loose_match else "0.0.0"
# # # # # # # # # #         full_version = f"{base_version}.{build}"

# # # # # # # # # #         # Inject version line just after shebang or encoding if available
# # # # # # # # # #         lines = content.splitlines()
# # # # # # # # # #         insert_at = 0
# # # # # # # # # #         for i, line in enumerate(lines[:5]):
# # # # # # # # # #             if line.startswith("#!") or "coding" in line:
# # # # # # # # # #                 insert_at = i + 1
# # # # # # # # # #         lines.insert(insert_at, f"__version__ = '{full_version}'")
# # # # # # # # # #         content = "\n".join(lines)

# # # # # # # # # #     # Add __author__ if missing
# # # # # # # # # #     if "__author__" not in content:
# # # # # # # # # #         content = f"__author__ = '{DEFAULT_AUTHOR}'\n{content}"

# # # # # # # # # #     # Replace or insert updated timestamp
# # # # # # # # # #     updated_pattern = re.compile(r"__updated__\s*=\s*['\"](.+?)['\"]")
# # # # # # # # # #     if updated_pattern.search(content):
# # # # # # # # # #         content = updated_pattern.sub(f"__updated__ = '2025-07-28 16:29:08'", content)
# # # # # # # # # #     else:
# # # # # # # # # #         content = f"__updated__ = '2025-07-28 16:29:08'\n{content}"

# # # # # # # # # #     # Make sure encoding line exists
# # # # # # # # # #     if "# -*- coding" not in content:
# # # # # # # # # #         content = f"# -*- coding: utf-8 -*-\n{content}"

# # # # # # # # # #     return content, full_version
# # # # # # # # # # #-----------------------------------------------------------------
# # # # # # # # # # def process_file(file_path:str, build:str):
# # # # # # # # # #     with open(file_path, "r+", encoding="utf-8") as file:
# # # # # # # # # #         content = file.read()

# # # # # # # # # #         # Inject metadata if needed
# # # # # # # # # #         new_content, ver = ensure_metadata(content, build, os.path.basename(file_path))

# # # # # # # # # #         # Update existing __version__ string
# # # # # # # # # #         version_pattern = re.compile(r"(__version__\s*=\s*['\"])(\d+\.\d+\.\d+)(?:\.(\d+))?(['\"])")
# # # # # # # # # #         updated_content = version_pattern.sub(lambda m: f"{m.group(1)}{m.group(2)}.{build}{m.group(4)}", new_content)



# # # # # # # # # #         file.seek(0)
# # # # # # # # # #         file.write(updated_content)
# # # # # # # # # #         file.truncate()
# # # # # # # # # #         print(f"🔧 {file_path} updated.  {ver}")

# # # # # # # # # # #-----------------------------------------------------------------
# # # # # # # # # # def update_directory(root_dir:str):
# # # # # # # # # #     build = read_and_increment_build()
# # # # # # # # # #     for dirpath, _, filenames in os.walk(root_dir):
# # # # # # # # # #         for filename in filenames:
# # # # # # # # # #             if filename.endswith(".py"):
# # # # # # # # # #                 full_path = os.path.join(dirpath, filename)
# # # # # # # # # #                 process_file(full_path, build)

# # # # # # # # # # # ▶️ Run like this:
# # # # # # # # # # # update_directory("your_project_directory")


#-----------------------------------------------------------------

# import os
# import re

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


