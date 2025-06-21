#!/usr/bin/env python3
"""
file-backup.py

Usage:
    python file-backup.py <filename>

Description:
    This script creates a backup of the specified file by copying it
    to a new file with ".bak" appended to the original filename.
    Example: "mynotes.txt" will be backed up as "mynotes.txt.bak"
"""

import sys
import shutil
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python file-backup.py <filename>")
        sys.exit(1)

    source_file = sys.argv[1]

    if not os.path.isfile(source_file):
        print(f"Error: File '{source_file}' does not exist.")
        sys.exit(1)

    backup_file = source_file + ".bak"

    try:
        shutil.copy(source_file, backup_file)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"An error occurred while creating backup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
