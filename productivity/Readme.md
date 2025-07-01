# 🗂️ File Organizer

Organize your messy folders in one command!  
This script sorts files into subfolders by type (Images, Documents, Videos, Music, Archives, Programs, Others).

---

## 🚀 What It Does

- **Scans a folder** (default: Downloads) and sorts files into type-based subfolders
- **Supports**: Images, Documents, Videos, Music, Archives, Programs, and a catch-all "Others"
- **No extra dependencies** — only Python standard library

---

## 🛠️ How to Use

### 1. **Clone or copy this script into your project**

### 2. **(Recommended) Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# or
source venv/bin/activate   # On macOS/Linux
```

### 3. **Run the script**
```bash
python file-organizer.py
```
- When prompted, enter the folder path to organize (or press Enter to use your Downloads folder).

---

## 📦 Supported File Types

| Folder      | Extensions                                                         |
|-------------|--------------------------------------------------------------------|
| Images      | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .svg, .webp, .ico           |
| Documents   | .pdf, .docx, .doc, .txt, .pptx, .ppt, .xlsx, .xls, .odt, .csv, .rtf, .md |
| Videos      | .mp4, .mkv, .mov, .avi, .wmv, .flv, .webm, .vob, .mpeg, .3gp      |
| Music       | .mp3, .wav, .aac, .flac, .ogg, .m4a, .wma, .alac                  |
| Archives    | .zip, .rar, .7z, .tar, .gz, .bz2, .xz, .iso, .cab                 |
| Programs    | .exe, .msi, .bat, .cmd, .sh, .jar, .py                            |
| Others      | Anything not matched above                                         |

---

## 🧪 Testing Safely

- Create a test folder with dummy files first (see [PowerShell example](#))
- Run the script on your test folder before using on real data!

---

## 🧹 After Running

The folder you organized will have subfolders like:
```
Images/
Documents/
Videos/
Music/
Archives/
Programs/
Others/
```
Each contains the files of that type.

---

## 📝 Notes

- **No files are deleted**, only moved
- Duplicate filenames are **overwritten** (default Python `shutil.move` behavior) — so test first!
- Cross-platform: works on Windows, macOS, Linux
