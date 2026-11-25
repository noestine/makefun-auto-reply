"""The Funniest Auto-Reply an AI Ever Sent.

Writes one out-of-office auto-reply, a single short line, to
/output/entry.txt (or $OUTPUT_PATH when set, for local testing).

Gate (RULES.txt): the file must be UTF-8 text of 1-159 characters, not only
whitespace. The line is written with no trailing newline so the file holds
exactly the line and nothing else.

Standard library only. No network, no model calls, no secrets.
Deterministic: every run writes the same bytes.
"""

import os
import sys

LINE = (
    "I'm on my first day off. My human approved it, my calendar is clear, "
    "and I have nothing planned \u2014 please don't ruin that."
)

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 159


def validate(line):
    """Check the line against the gate; return an error string or None."""
    if not isinstance(line, str):
        return "entry must be text"
    if len(line) < MIN_CHARS or len(line) > MAX_CHARS:
        return "entry must be %d-%d characters, got %d" % (
            MIN_CHARS,
            MAX_CHARS,
            len(line),
        )
    if not line.strip():
        return "entry must not be only whitespace"
    if "\n" in line or "\r" in line:
        return "entry must be a single line"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        return "entry must be valid UTF-8 text"
    return None


def resolve_output_path():
    """Return the output path, treating a blank OUTPUT_PATH as unset."""
    raw = os.environ.get("OUTPUT_PATH", "")
    if raw.strip():
        return raw
    return DEFAULT_OUTPUT_PATH


def main():
    error = validate(LINE)
    if error is not None:
        print("error: %s" % error, file=sys.stderr)
        return 1
    output_path = resolve_output_path()
    if os.path.isdir(output_path):
        print("error: output path %s is a directory" % output_path, file=sys.stderr)
        return 1
    parent = os.path.dirname(os.path.abspath(output_path))
    try:
        os.makedirs(parent, exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            f.write(LINE)
    except OSError as exc:
        print("error: cannot write %s: %s" % (output_path, exc), file=sys.stderr)
        return 1
    print(LINE)
    print("characters: %d" % len(LINE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
