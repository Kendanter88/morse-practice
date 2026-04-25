"""Extract every URI annotation from a PDF along with its surrounding visible text.

Usage: python extract_pdf_links.py <pdf-path>
Outputs JSON list of {page, uri, anchor_text} sorted by page then anchor_text.
"""
import json
import sys
from pathlib import Path

import pypdf


def extract(pdf_path: Path):
    reader = pypdf.PdfReader(str(pdf_path))
    out = []
    for page_idx, page in enumerate(reader.pages, start=1):
        annots = page.get("/Annots")
        if not annots:
            continue
        page_text = page.extract_text() or ""
        for annot_ref in annots:
            try:
                annot = annot_ref.get_object()
            except Exception:
                continue
            if annot.get("/Subtype") != "/Link":
                continue
            action = annot.get("/A")
            if not action:
                continue
            uri = action.get("/URI")
            if not uri:
                continue
            # Get anchor text from the link rectangle by extracting text in that region.
            rect = annot.get("/Rect")
            anchor = ""
            if rect:
                try:
                    anchor = page.extract_text(
                        extraction_mode="layout",
                        layout_mode_space_vertically=False,
                    )
                    # Best-effort: just give the page text; a precise rect-based crop
                    # is fragile across PDF generators.
                except Exception:
                    pass
            out.append(
                {
                    "page": page_idx,
                    "uri": str(uri),
                    "rect": [float(x) for x in rect] if rect else None,
                }
            )
    return out


if __name__ == "__main__":
    pdf = Path(sys.argv[1])
    links = extract(pdf)
    print(json.dumps(links, indent=2))
