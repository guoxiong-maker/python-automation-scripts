#!/usr/bin/env python3
"""Find duplicate files in a directory by computing SHA256 hashes.

Examples:
    python 02_find_duplicates.py --dir ./my_files
    python 02_find_duplicates.py --dir ./my_files --delete
"""
import argparse
import hashlib
import os
import sys


def hash_file(path, chunk=65536):
    """Return the SHA256 hex digest of a file read in chunks."""
    sha = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            sha.update(block)
    return sha.hexdigest()


def find_duplicates(directory, delete=False):
    """Find duplicate files; optionally delete them, keeping the first seen."""
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        return 1

    seen, duplicates = {}, []
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                digest = hash_file(path)
            except OSError as exc:
                print(f"Warning: cannot read '{path}': {exc}", file=sys.stderr)
                continue
            if digest in seen:
                duplicates.append((path, seen[digest]))
                if delete:
                    os.remove(path)
                    print(f"[DELETED] {path}")
                else:
                    print(f"[DUP] {path}  ==  {seen[digest]}")
            else:
                seen[digest] = path

    print(f"\nFound {len(duplicates)} duplicate file(s).")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find duplicate files by SHA256 hash.")
    parser.add_argument("--dir", required=True, help="Directory to scan")
    parser.add_argument("--delete", action="store_true",
                        help="Delete duplicates (keeps first occurrence)")
    args = parser.parse_args()
    sys.exit(find_duplicates(args.dir, args.delete))
