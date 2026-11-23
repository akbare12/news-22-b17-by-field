#!/usr/bin/env python3
"""news-image-20261122 b17 by-field: copy the drawn entry to MAKEFUN_OUTPUT_DIR.

The entry image is drawn by draw.py and stored beside this file as entry.png.
This program only copies it into the output directory the grader provides.
Nothing is ever written next to this file: the destination is always inside
MAKEFUN_OUTPUT_DIR.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        data = fh.read()
    with open(src, "rb") as fh:
        orig = fh.read()
    if data != orig:
        print("error: output differs from source", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("error: output over 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: output is not a PNG", file=sys.stderr)
        return 1
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        print(f"error: bad dimensions {w}x{h}", file=sys.stderr)
        return 1
    print("OK", dst, len(data), "bytes",
          hashlib.sha256(data).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
