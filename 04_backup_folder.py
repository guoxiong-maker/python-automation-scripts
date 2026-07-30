#!/usr/bin/env python3
"""Compress a folder into a timestamped zip backup with optional rotation.

Examples:
    python 04_backup_folder.py --src ./project --dest ./backups
    python 04_backup_folder.py --src ./project --dest ./backups --max-backups 5
"""
import argparse
import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path


def create_backup(src, dest, max_backups=0):
    if not os.path.isdir(src):
        print(f"Error: source '{src}' is not a valid directory.", file=sys.stderr)
        return 1
    os.makedirs(dest, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    src_name = os.path.basename(os.path.normpath(src)) or "backup"
    zip_path = os.path.join(dest, f"{src_name}_backup_{timestamp}.zip")
    print(f"Creating backup: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src):
            for name in files:
                file_path = os.path.join(root, name)
                zf.write(file_path, os.path.relpath(file_path, src))
    print(f"Backup complete: {os.path.getsize(zip_path) / 1024:.1f} KB")
    if max_backups > 0:
        pattern = f"{src_name}_backup_*.zip"
        backups = sorted(Path(dest).glob(pattern), key=os.path.getmtime)
        while len(backups) > max_backups:
            old = backups.pop(0)
            old.unlink()
            print(f"Rotated old backup: {old.name}")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a timestamped zip backup.")
    parser.add_argument("--src", required=True, help="Source folder")
    parser.add_argument("--dest", required=True, help="Destination folder")
    parser.add_argument("--max-backups", type=int, default=0, help="Keep N backups")
    args = parser.parse_args()
    sys.exit(create_backup(args.src, args.dest, args.max_backups))
