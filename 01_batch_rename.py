#!/usr/bin/env python3
"""Batch rename files in a directory using prefix, suffix, or sequential numbering.

Examples:
    python 01_batch_rename.py --dir ./photos --prefix vacation_ --sequential
    python 01_batch_rename.py --dir ./docs --suffix _backup --dry-run
"""
import argparse
import os
import sys


def batch_rename(directory, prefix="", suffix="", sequential=False, dry_run=False):
    """Rename files in *directory* applying prefix/suffix and optional numbering."""
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        return 1

    files = sorted(f for f in os.listdir(directory)
                   if os.path.isfile(os.path.join(directory, f)))
    if not files:
        print("No files found to rename.")
        return 0

    width = len(str(len(files)))
    renamed = 0
    for idx, filename in enumerate(files, start=1):
        name, ext = os.path.splitext(filename)
        if sequential:
            new_name = f"{prefix}{str(idx).zfill(width)}{suffix}{ext}"
        else:
            new_name = f"{prefix}{name}{suffix}{ext}"
        if new_name == filename:
            continue
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)
        tag = "[DRY-RUN]" if dry_run else "[RENAMED]"
        print(f"{tag} {filename}  ->  {new_name}")
        if not dry_run:
            os.rename(src, dst)
        renamed += 1

    action = "Would rename" if dry_run else "Renamed"
    print(f"
{action} {renamed} file(s).")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files with patterns.")
    parser.add_argument("--dir", required=True, help="Target directory")
    parser.add_argument("--prefix", default="", help="Prefix added to filenames")
    parser.add_argument("--suffix", default="", help="Suffix added to filenames")
    parser.add_argument("--sequential", action="store_true", help="Use sequential numbering")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changing files")
    args = parser.parse_args()
    sys.exit(batch_rename(args.dir, args.prefix, args.suffix,
                          args.sequential, args.dry_run))