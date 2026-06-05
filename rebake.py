#!/usr/bin/env python3
"""
Re-bake wrapper.html into generator.html.

generator.html ships the master template (wrapper.html) inside it as a base64
blob in <script type="text/plain" id="masterB64">. The generator decodes that on
boot — it never fetches wrapper.html over the network. So whenever you edit
wrapper.html, you MUST re-bake or the hosted tool will keep serving the OLD
wrapper.

Usage:
    python rebake.py            # re-bake and report
    python rebake.py --check    # exit 1 if generator.html is stale (for CI)

The encoding mirrors the browser's  btoa(unescape(encodeURIComponent(str)))  so
the round-trip is byte-identical to what the generator decodes at runtime.
"""
import base64
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WRAPPER = HERE / "wrapper.html"
GENERATOR = HERE / "generator.html"
# Matches: <script ... id="masterB64" ...> <base64> </script>
TAG_RE = re.compile(r'(<script[^>]*id="masterB64"[^>]*>)([\s\S]*?)(</script>)')


def read_keep_eol(path: Path) -> str:
    # newline='' preserves the file's existing line endings on write-back.
    return path.read_text(encoding="utf-8", newline="")


def bake(wrapper_text: str) -> str:
    return base64.b64encode(wrapper_text.encode("utf-8")).decode("ascii")


def main() -> int:
    check_only = "--check" in sys.argv

    wrapper_text = WRAPPER.read_text(encoding="utf-8")
    new_b64 = bake(wrapper_text)

    gen_text = read_keep_eol(GENERATOR)
    m = TAG_RE.search(gen_text)
    if not m:
        print("ERROR: <script id=\"masterB64\"> not found in generator.html")
        return 2

    current_b64 = m.group(2).strip()
    up_to_date = current_b64 == new_b64

    if check_only:
        if up_to_date:
            print("OK: generator.html is up to date with wrapper.html")
            return 0
        print("STALE: generator.html does not match wrapper.html — run: python rebake.py")
        return 1

    if up_to_date:
        print("Already up to date — nothing to do.")
        return 0

    new_gen = gen_text[: m.start(2)] + new_b64 + gen_text[m.end(2):]
    GENERATOR.write_text(new_gen, encoding="utf-8", newline="")

    # Verify the round-trip decodes back to exactly wrapper.html.
    roundtrip = base64.b64decode(new_b64).decode("utf-8")
    assert roundtrip == wrapper_text, "round-trip mismatch — aborting"
    print(f"Re-baked wrapper.html ({len(wrapper_text):,} chars) into generator.html. Round-trip OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
