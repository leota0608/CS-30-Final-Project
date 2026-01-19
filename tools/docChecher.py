###############################################################################
# Title: Doc Checker
# Class: CS 30
# Assignment: final project
# Coder: Amir
# Last date modified: 1/18/2026
###############################################################################
""" This module checks if all the functions, classes and have header
and doc string.
"""
###############################################################################
import os


def getLines(fileName):
    """ returns all the lines of a given function.
    """
    lines = None
    with open(fileName, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines


def checkExistance(lines):
    """ checks if the functions and classes have docstring.
    lines: list of all the lines.
    """
    i = 0
    missing = []
    while i < len(lines):
        line = lines[i].lstrip()
        if line.startswith("class ") or line.startswith("def "):
            type_ = "class" if line.startswith("class") else "function"
            name = line.split(' ')[1].split("(")[0]
            if type_ == "class":
                name = name.split(':')[0]
            actual_line = i + 1
            # move ahead until we find the :
            while ":" not in lines[i]:
                i += 1
                if i >= len(lines):
                    missing.append((type_, name, actual_line))
                    return "no end", missing
            # move forward until  there is no more space or
            # empty line.
            while lines[i].strip() == "":
                i += 1
                if i >= len(lines):
                    missing.append((type_, name, actual_line))
                    return "no def", missing
            i += 1
            if not (lines[i].lstrip().startswith("'''") or
                    lines[i].lstrip().startswith('"""')):
                missing.append((type_, name, actual_line))
        i += 1
    return "good", missing


def checkFile(fileName):
    """ checks all the functions and classes
    inside a files and reports its situation.
    fileName: name of the file.(str)
    """
    lines = getLines(fileName)
    status, missing = checkExistance(lines)

    print(f"------------checking file {fileName}------------")
    if len(missing) != 0:
        for i in range(len(missing) - 1):
            m = missing[i]
            print(f"{m[0]} {m[1]} at line {m[2]}.")
        last = missing[len(missing) - 1]
        if status == "good":
            print(f"{last[0]} {last[1]} at line {last[2]}.")
        elif status == "no def":
            print(f"{last[0]} {last[1]} seems to not have definition.")
        elif status == "no end":
            print(f"{last[0]} {last[1]} seems to not have :.")
    else:
        print("all good!")


def checkFolders(directory: str):
    """ recursively corrects all the folders.
    directory: the name of the folder to correct its files.(str)
    """
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isfile(path) and path.endswith(".py"):
            checkFile(path)
        elif os.path.isdir(path):
            checkFolders(path)  # recursive call for subdirectories


if __name__ == "__main__":
    # change the folder depending on your system.
    checkFolders("C:/Users/KAVOSH/PycharmProjects/CS-30-Final-Project")
