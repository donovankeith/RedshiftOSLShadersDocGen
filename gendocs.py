#!/usr/bin/env python3
"""Redshift OSL Shaders - Docs Generator
Generates README.md documentation for https://github.com/redshift3d/RedshiftOSLShaders

## Assumptions

- Directory is empty except for:
    - **Shader**: [ShaderName].osl
    - **Screenshot/Demo**: [ShaderName].[jpg, png, gif]
    - **Example Image**: [ShaderName]_Example*.[jpg, png, gif]
    - **Example Project**: [ShaderName]_Example*.zip
- ShaderNamesAreWrittenInCamelCase
"""

__author__ = "Donovan Keith"
__copyright__ = "Copyright 2022, Maxon Computer GmbH"
__credits__ = ["Donovan Keith"]
__version__ = "0.1.0"
__license__ = "MIT0"

import os
import glob
import re

# Need to `cd` to RedshiftOSLShaders directory and then call this script via path.
PATH_SRC = os.getcwd()

ID_SHADER = "shader"
ID_IMAGE_SCREENSHOT = "screenshot"
ID_IMAGE_EXAMPLE = "example"
ID_PROJECT = "project"
ID_TITLE = "title"

def camel_case_split(name):
    """
    Reference: https://stackoverflow.com/a/37697078
    By: Jossef Harush Kadouri
    License: CC BY-SA 4.0
    """

    return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()

def camel_to_title(name):
    return " ".join(camel_case_split(name))

def print_script_info():
    doc_lines = __doc__.splitlines()
    title = doc_lines[0]
    description = doc_lines[1]

    print("\n")
    print(title.upper(), " - ", __version__)
    print(description)
    print("Generating docs...")

def main():
    """ Main entry point of the app """

    print_script_info()

    root = PATH_SRC
    pattern = os.path.join(root, "*.*")

    shaders = {}

    for file in glob.glob(pattern):
        basename = os.path.basename(file)
        file_parts = os.path.splitext(basename)
        filename = file_parts[0]
        extension = file_parts[1]

        acceptable_extensions = [".osl", ".png", ".jpg", ".gif", ".zip"]
        if extension not in acceptable_extensions:
            continue

        if filename.upper() == "README":
            continue

        shader_id = re.split(r"[._]", filename)[0]

        if shader_id not in shaders.keys():
            shaders[shader_id] = {}
            shaders[shader_id][ID_TITLE] = camel_to_title(shader_id)


        if extension == ".osl":
            shaders[shader_id][ID_SHADER] = basename
        elif extension in [".jpg", ".png"]:
            if "example" in basename.lower():
                shaders[shader_id][ID_IMAGE_EXAMPLE] = basename
            else:
                shaders[shader_id][ID_IMAGE_SCREENSHOT] = basename
        elif extension in [".zip"]:
            shaders[shader_id][ID_PROJECT] = basename

    header_file = open(os.path.join(os.path.dirname(__file__), "HEADER.md"), 'r')
    header = header_file.read()
    header_file.close()

    output = ""

    for key in sorted(shaders.keys()):
        entry = shaders[key]
        output += f"\n### {entry[ID_TITLE]}"
        if ID_IMAGE_SCREENSHOT in entry.keys():
            output += f"\n\n![]({entry[ID_IMAGE_SCREENSHOT]})"

        started_list = False
        if ID_SHADER in entry.keys():
            if not started_list:
                output += "\n"
            output += f"\n- [{entry[ID_SHADER]} 📝]({entry[ID_SHADER]})"
            started_list = True
        if ID_PROJECT in entry.keys():
            if not started_list:
                output += "\n"
            output += f"\n- [{entry[ID_PROJECT]} 📦]({entry[ID_PROJECT]})"
        if ID_IMAGE_EXAMPLE in entry.keys():
            output += f"\n- [{entry[ID_IMAGE_EXAMPLE]} 🖼️]({entry[ID_IMAGE_EXAMPLE]})"
        output += "\n"

    output = header + output

    readme_path = os.path.join(root, "README.md")
    with open(readme_path, 'w') as f:
        f.write(output)

    print("SUCCESS: ")
    print(readme_path)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()