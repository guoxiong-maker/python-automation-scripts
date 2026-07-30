#!/usr/bin/env python3
"""Scan a directory tree and list the top N largest files.

Examples:
    python 05_file_size_analyzer.py --dir ./ --top 10 --format MB
"""
import argparse
import os
import sys

UNITS = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}

def scan_sizes(directory):
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                yield path, os.path.getsize(path)
            except OSError:
                continue

def analyze(directory, top=20, unit="MB"):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        return 1
    divisor = UNITS[unit]
    files = sorted(scan_sizes(directory), key=lambda x: x[1], reverse=True)[:top]
    if not files:
        print("No files found.")
        return 0
    print(f"Top {len(files)} largest files (sizes in {unit}):\n")
    for path, size in files:
        print(f"{size / divisor:>12.2f}  {path}")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find largest files.")
    parser.add_argument("--dir", required=True, help="Directory to scan")
    parser.add_argument("--top", type=int, default=20, help="Number of files")
    parser.add_argument("--format", choices=["B", "KB", "MB", "GB"], default="MB")
    args = parser.parse_args()
    sys.exit(analyze(args.dir, args.top, args.format))
