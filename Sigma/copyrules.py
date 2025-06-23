#!/usr/bin/env python3
"""
Copy Sigma rule files whose names (or paths) are listed in a text file
to a destination directory.

Usage:
    python copy_rules.py rules.txt /path/to/dest [-s /path/to/src]
"""

import argparse
import shutil
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy Sigma rules listed in a text file to a destination folder"
    )
    parser.add_argument("list_file", help="Text file with rule names or paths")
    parser.add_argument("dest_dir", help="Destination directory")
    parser.add_argument(
        "-s",
        "--src-dir",
        help="Source directory containing rules (required if names are relative)",
    )
    args = parser.parse_args()

    dest_path = Path(args.dest_dir).expanduser().resolve()
    dest_path.mkdir(parents=True, exist_ok=True)

    src_base = Path(args.src_dir).expanduser().resolve() if args.src_dir else None

    with Path(args.list_file).expanduser().open(encoding="utf-8") as fh:
        for line in fh:
            name = line.strip()
            if not name or name.startswith("#"):
                continue  # skip blanks & comments

            rule_path = Path(name)
            if not rule_path.is_absolute():
                if not src_base:
                    print(
                        f"Skipping '{name}': relative path without --src-dir.",
                        file=sys.stderr,
                    )
                    continue
                rule_path = src_base / rule_path

            if rule_path.is_file():
                shutil.copy2(rule_path, dest_path / rule_path.name)
            else:
                print(f"Warning: rule not found → {rule_path}", file=sys.stderr)


if __name__ == "__main__":
    main()