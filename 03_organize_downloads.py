#!/usr/bin/env python3
"""Auto-organize a folder by file extension into categorized subfolders.

Categories: Images, Documents, Videos, Audio, Archives, Code, Others.

Examples:
    python 03_organize_downloads.py
    python 03_organize_downloads.py --dir ~/Downloads --dry-run
"""
import argparse
import os
import shutil
import sys

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                  ".txt", ".csv", ".md", ".rtf"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Code": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".html", ".css",
             ".json", ".xml", ".sh", ".go", ".rb"},
}


def categorize(ext):
    """Return the category folder name for a given file extension."""
    ext = ext.lower()
    for category, exts in CATEGORIES.items():
        if ext in exts:
            return category
    return "Others"


def organize(directory, dry_run=False):
    """Move each file in *directory* into its category subfolder."""
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        return 1

    moved = 0
    for name in os.listdir(directory):
        src = os.path.join(directory, name)
        if not os.path.isfile(src):
            continue
        category = categorize(os.path.splitext(name)[1])
        tag = "[DRY-RUN]" if dry_run else "[MOVED]"
        print(f"{tag} {name}  ->  {category}/")
        if not dry_run:
            dest_dir = os.path.join(directory, category)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(src, os.path.join(dest_dir, name))
        moved += 1

    action = "Would move" if dry_run else "Moved"
    print(f"\n{action} {moved} file(s).")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize a folder by file extension.")
    parser.add_argument("--dir", default=os.path.expanduser("~/Downloads"),
                        help="Folder to organize (default: ~/Downloads)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    args = parser.parse_args()
    sys.exit(organize(args.dir, args.dry_run))
