#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""


# +++your code here+++
# Write functions and modify main() to call them


def getAbsSpecialPaths(dir):
    matchedAbsSpecialPaths = []

    if not os.path.exists(dir):
        print(f"The directory {dir} does not exist")
    elif not os.path.isdir(dir):
        print(f"The directory {dir} is not a valid or is a file")
    else:
        fnames = os.listdir(dir)
        for fn in fnames:
            fnm = re.match(r".*__(\w+)__.*", fn)
            if fnm:
                matchedAbsSpecialPaths.append(os.path.abspath(os.path.join(dir, fn)))

    return matchedAbsSpecialPaths


def copyToDir(toDir, absFilePaths):
    if os.path.exists(toDir) and not os.path.isdir(toDir):
        print(f"The copy to directory {toDir} is not a valid or is a file")
    else:
        print(f"Performing copy to {toDir}")
        os.makedirs(toDir, exist_ok=True)
        for fn in absFilePaths:
            shutil.copy(fn, toDir)


def zipTo(toZipFile, absFilePaths):
    # Note that I was using this, and it was failing:
    # gzipArgs = ["gzip"] + ["--stdout"] + absFilePaths + [">"] + [f"{toZipFile}"]
    # This is because using output redirection is a shell construct and is treated by
    # python as if I was giving it additional file name in the command.
    # I could have used shell=True in the subprocess.run call, but piping to the file
    # using python is more elegant, and not a security risk.
    gzipArgs = ["gzip"] + ["--stdout"] + absFilePaths
    try:
        print(f"The command is:\n {' '.join(gzipArgs)}")
        with open(toZipFile, "w") as outfile:
            subprocess.run(gzipArgs, check=True, stderr=subprocess.PIPE, stdout=outfile)
        print("gzip completed successfully")
    except FileNotFoundError:
        print(f"Error writing to file: {toZipFile} check that it is a valid file")
    except subprocess.CalledProcessError as cpe:
        print(f"gzip failed with code: {cpe.returncode}")
        print(f"Here is the error {cpe.stderr.decode()}")


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    toDir = ""
    if args[0] == "--todir":
        toDir = args[1]
        del args[0:2]

    tozip = ""
    if args[0] == "--tozip":
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    # +++your code here+++
    # Call your functions
    specialAbsPaths = []
    for destDir in args:
        specialAbsPaths.extend(getAbsSpecialPaths(destDir))

    if specialAbsPaths:
        print(f"Got the following special paths\n{specialAbsPaths}\n")
        if toDir:
            copyToDir(toDir, specialAbsPaths)
        if tozip:
            zipTo(tozip, specialAbsPaths)


if __name__ == "__main__":
    main()
