"""
file-organizer.py
-----------------
Organizes a folder by sorting files into type-based subfolders:
Images, Documents, Videos, Music, Archives, Programs, and Others.

Dependencies: Only uses built-in Python modules (os, shutil).
"""

import os
import shutil

# -------------------------------
# File type extension groups
# -------------------------------
file_types = {
    "Images": ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico'),
    "Documents": ('.pdf', '.docx', '.doc', '.txt', '.pptx', '.ppt', '.xlsx', '.xls', '.odt', '.csv', '.rtf', '.md'),
    "Videos": ('.mp4', '.mkv', '.mov', '.avi', '.wmv', '.flv', '.webm', '.vob', '.mpeg', '.3gp'),
    "Music": ('.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma', '.alac'),
    "Archives": ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.cab'),
    "Programs": ('.exe', '.msi', '.bat', '.cmd', '.sh', '.jar', '.py'),
}

print("🗂️ File Organizer - Sort files by type into folders!\n")

default_path = os.path.join(os.path.expanduser("~"), "Downloads")
target_folder = input(f"📁 Enter folder path to organize (default: {default_path}): ").strip()

if not target_folder:
    target_folder = default_path

if not os.path.exists(target_folder):
    print("❌ The provided folder does not exist.")
    exit(1)

print(f"\n✅ Organizing files in: {target_folder}\n")

moved_files = 0
other_files = 0

for file in os.listdir(target_folder):
    file_path = os.path.join(target_folder, file)

    if os.path.isfile(file_path):
        ext = os.path.splitext(file)[1].lower()
        moved = False
        for folder, extensions in file_types.items():
            if ext in extensions:
                dest_folder = os.path.join(target_folder, folder)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                shutil.move(file_path, os.path.join(dest_folder, file))
                print(f"📁 Moved {file} to {folder}/")
                moved_files += 1
                moved = True
                break
        if not moved:
            dest_folder = os.path.join(target_folder, "Others")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            shutil.move(file_path, os.path.join(dest_folder, file))
            print(f"📁 Moved {file} to Others/")
            other_files += 1

print(f"\n✅ Done! Moved {moved_files} files into categorized folders.")
if other_files:
    print(f"ℹ️ {other_files} files did not match any category and were moved to 'Others/'.")

print("\n🎉 Your folder is now organized!")
