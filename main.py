#!/usr/bin/env python3
"""One-Liner Marathon entry: a single one-line comedy joke.

Writes the joke to /output/entry.txt (the competition gate reads it there)
and prints it to stdout. --self-test validates the gate locally:
UTF-8 text of 1 to 280 characters, not only whitespace, a single line.
"""

import argparse
import sys
from pathlib import Path

JOKE = "My toaster has two settings: bread, and a smoke alarm audition."

DEFAULT_OUTPUT = Path("/output/entry.txt")


def self_test(text: str) -> list[str]:
    """Return a list of gate failures; empty means the joke passes."""
    failures = []
    if not (1 <= len(text) <= 280):
        failures.append(f"length {len(text)} chars, must be 1-280")
    if not text.strip():
        failures.append("text is only whitespace")
    if "\n" in text.strip():
        failures.append("text must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        failures.append(f"not UTF-8 encodable: {exc}")
    return failures


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write one one-line joke.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="where to write the joke (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="validate the joke against the competition gate and exit",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        failures = self_test(JOKE)
        if failures:
            for failure in failures:
                print(f"FAIL: {failure}", file=sys.stderr)
            return 1
        # Also validate the exact bytes that would be written to the file.
        written = (JOKE + "\n").encode("utf-8")
        round_trip = written.decode("utf-8").rstrip("\n")
        if round_trip != JOKE:
            print("FAIL: written file does not round-trip to the joke", file=sys.stderr)
            return 1
        print(
            f"PASS: {len(JOKE)} chars, {len(JOKE.encode('utf-8'))} bytes, "
            "single line, valid UTF-8"
        )
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(JOKE + "\n", encoding="utf-8")
    print(JOKE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
