#!/usr/bin/env python3
"""The Funniest Sick-Day Excuse — make.fun entry.

Writes one line (under 200 characters) to /output/entry.txt:
a sick-day excuse a boss might half believe and a coworker would
laugh at, with the twist landing at the very end.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import os
import sys

# The entry: one line, 146 characters. Laryngitis is a real, believable
# reason to stay home; the joke turns on office life ("per my last
# email") and the punchline — whispering it "with authority" — lands
# on the last word, in the voice of a real person typing a message.
ENTRY = (
    "Woke up with laryngitis, which would be fine, except my job is 90% "
    "saying 'per my last email' and I physically cannot whisper that "
    "with authority."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-200 characters,
    # not only whitespace, a single line.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"entry is {len(text)} characters, over the 200 limit",
              file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
