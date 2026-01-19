###############################################################################
# Title: Header Hashtag Fixer
# Class: CS 30
# Assignment: final project
# Coder: Amir
# Last date modified: 1/18/2026
###############################################################################
""" Since there are a lot of inconsistencies with the number of hashtags
in the header of our files, this script was written to automatically correct
all the files and change the number of hashtags to 79.
"""
###############################################################################
import os

HEADER_HASH_TAG = 79 * "#" + "\n"
# min number of hashtags to be considered as a header hashtag
MIN_HASHTAG = 20
# change depending on your system
# copy the absolute path and paste it here
SOURCE_DIRECTORY = "C:/Users/KAVOSH/PycharmProjects/CS-30-Final-Project"


def correctHeader(fileName):
    """ corrects a given file if it finds any problems with its
    header.
    fileName: the name of the file to correct. (str)
    """
    lines = None
    changed = 0
    with open(fileName, mode='r', encoding="utf-8") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]
        hash_tag_counter = 0
        for c in line:
            if c == "#":
                hash_tag_counter += 1
        if hash_tag_counter >= MIN_HASHTAG and hash_tag_counter != 79:
            lines[i] = HEADER_HASH_TAG
            changed += 1
        if changed >= 3:
            break
    with open(fileName, mode='w', encoding='utf-8') as f:
        f.writelines(lines)
    return changed


def fix_directory(directory: str):
    """ recursively corrects all the directories.
    directory: the name of the folder to correct its files.(str)
    """
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isfile(path) and path.endswith(".py"):
            changed = correctHeader(path)
            if changed != 0:
                print(f"Fixed: {path}")
                print(f"{changed} items changed.")
        elif os.path.isdir(path):
            fix_directory(path)  # recursive call for subdirectories


if __name__ == "__main__":
    fix_directory(SOURCE_DIRECTORY)
