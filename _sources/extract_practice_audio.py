"""Build a {code: url} map of every CWops Intermediate practice audio file.

Reads:  _sources/cwops-practice-files.htm
Writes: _sources/cwops-practice-audio.json
"""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
SRC = ROOT / "_sources" / "cwops-practice-files.htm"
OUT = ROOT / "_sources" / "cwops-practice-audio.json"


def normalize(code: str) -> str:
    """Match the hyphen/underscore variants the curriculum uses.

    The curriculum references files like WD101-10 / SS101-10. The URL
    paths use WD101_10 / SS101_10. We standardize on hyphen form for the key.
    """
    return code.replace("_", "-").upper()


def main():
    html = SRC.read_text(encoding="utf-8", errors="replace")
    found = {}
    for m in re.finditer(r'href="([^"]+\.mp3)"', html, flags=re.I):
        url = m.group(1)
        name = Path(urlparse(url).path).stem  # SS101_10
        key = normalize(name)
        # First win — the page sometimes has duplicate links per file.
        if key not in found:
            found[key] = url
    OUT.write_text(json.dumps(found, indent=2, sort_keys=True))
    print(f"Wrote {OUT}")
    print(f"  Files: {len(found)}")
    # Sanity print a few
    for k in ["WD101-10", "PR101-10", "SS101-15", "POTA101-20", "CWT-201-20", "DIS4-10"]:
        print(f"  {k}: {found.get(k, 'MISSING')}")


if __name__ == "__main__":
    main()
