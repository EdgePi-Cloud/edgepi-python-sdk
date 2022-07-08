"""increment patch number for publishing to TestPyPi"""

import sys
import fileinput


SEARCH_TEXT = "version"
TEST_PYPI_VER_NUM = "TEST_PYPI_VER_NUM"


def bump_version_patch(vers_line: str) -> str:
    """
    Increments patch number of a version line taking the format
    major.minor.patch
    """
    version = vers_line.split('"')[1]
    semantic_list = version.split(".")
    patch_num = int(semantic_list[2]) + 1
    new_ver = semantic_list[0] + "." + semantic_list[1] + "." + str(patch_num)
    return line.replace(version, new_ver)


if __name__ == "__main__":
    # get current version number
    with fileinput.input("./setup.py", inplace=True) as file:
        for line in file:
            if SEARCH_TEXT in line:
                # replace line containing version number
                new_line = bump_version_patch(line)
                sys.stdout.write(new_line)
            else:
                # do not modify line
                sys.stdout.write(line)

        file.close()
