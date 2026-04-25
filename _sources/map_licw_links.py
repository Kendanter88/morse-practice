"""Map LICW PDF hyperlinks to lesson exercises.

Strategy
--------
- Each lesson exercise page contains a fixed set of links of two kinds:
  * MPP   → host morsecode.world
  * WLT   → host longislandcw.github.io
- pypdf returns link annotations with rect coordinates. We sort by visual
  reading order (left column top-to-bottom, then right column top-to-bottom)
  to get the same order the user sees on the page.
- We have a hand-curated list of which PDF pages hold the MPP/WLT lists for
  each lesson plus the expected exercise sequence per lesson per tool.
- We zip the sorted URL list with the expected exercise sequence to produce
  the final {lesson, exercise, mpp, wlt} mapping.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import pypdf


def reading_order_key(rect):
    """Return a sort key for left-to-right, top-to-bottom reading order.

    PDF y-coordinates increase upward, so we negate y. We bucket x into
    columns at a 250pt threshold (PDF page width ≈ 612pt for letter)."""
    x, y = rect[0], rect[1]
    column = 0 if x < 250 else 1
    return (column, -y)


def page_links(reader, page_num):
    page = reader.pages[page_num - 1]
    annots = page.get("/Annots")
    if not annots:
        return []
    out = []
    for ref in annots:
        try:
            a = ref.get_object()
        except Exception:
            continue
        if a.get("/Subtype") != "/Link":
            continue
        action = a.get("/A")
        if not action:
            continue
        uri = action.get("/URI")
        if not uri:
            continue
        rect = a.get("/Rect")
        out.append({"uri": str(uri), "rect": [float(v) for v in rect]})
    return out


def split_by_position(links, mpp_count):
    """Split links into (mpp, wlt) blocks by vertical position on the page.

    MPP and WLT sections are stacked vertically with a visible gap between them.
    We take the top `mpp_count` links (by reading order) as MPP; the rest are WLT.
    """
    ordered = sorted(links, key=lambda l: reading_order_key(l["rect"]))
    return ordered[:mpp_count], ordered[mpp_count:]


def reading_order_two_blocks(links, mpp_count):
    """For pages with two stacked blocks (MPP on top, WLT below), build the
    MPP and WLT lists each in their own reading order.

    Each block is itself a two-column list. We identify the block boundary
    by finding the largest y-gap between consecutive links sorted by y desc.
    """
    by_y_desc = sorted(links, key=lambda l: -l["rect"][1])
    # Find largest gap between consecutive distinct y values.
    distinct_y = sorted({round(l["rect"][1], 1) for l in by_y_desc}, reverse=True)
    if len(distinct_y) < 2:
        return reading_sorted(links), []
    gaps = [(distinct_y[i] - distinct_y[i + 1], distinct_y[i + 1])
            for i in range(len(distinct_y) - 1)]
    # Largest gap defines the threshold: links with y > threshold = MPP.
    biggest = max(gaps, key=lambda g: g[0])
    threshold = biggest[1] + biggest[0] / 2
    mpp = [l for l in links if l["rect"][1] > threshold]
    wlt = [l for l in links if l["rect"][1] <= threshold]
    # If the count is wrong (only one block on page), fall back to count-based split.
    if mpp_count and abs(len(mpp) - mpp_count) > 1:
        return split_by_position(links, mpp_count)
    return reading_sorted(mpp), reading_sorted(wlt)


def reading_sorted(links):
    return sorted(links, key=lambda l: reading_order_key(l["rect"]))


# ---------------------------------------------------------------------------
# Per-lesson exercise expectations.
#
# Each lesson lists the exercises in the order the PDF presents them under the
# MPP and WLT bullet lists. WLT diverges from MPP only when the bullet lists
# differ — the PDF includes some "Alphabet Mix" items in WLT only.
# ---------------------------------------------------------------------------

LESSONS = [
    {
        "id": 1,
        "pages_mpp": [10],
        "pages_wlt": [11],
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Numbers — Flow Rate 1",
            "2 letter words — Flow Rate 1",
            "2-3 letter words #1",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
        ],
        "wlt": [
            "Alphabet — Flow Rate 1",
            "Numbers — Flow Rate 1",
            "2 letter words — Flow Rate 1",
            "2-3 letter words #1",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
        ],
    },
    {
        "id": 2,
        "pages_mpp": [13],
        "pages_wlt": [13],
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "2 letter words",
            "2-3 letter words #1",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
        ],
        "wlt": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "2 letter words",
            "2-3 letter words #1",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
        ],
    },
    {
        "id": 3,
        "pages_mpp": [15],
        "pages_wlt": [15],
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2 letter words — Flow Rate 1",
            "2 letter words — Flow Rate 2",
            "States and Provinces — with Voice",
            "2-3 letter words #1",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
        ],
        "wlt": [
            "Alphabet — Flow Rate 1",
            "Alphabet Mix #1",
            "Alphabet Mix #2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2 letter words — Flow Rate 1",
            "2 letter words — Flow Rate 2",
            "States and Provinces — Voice",
            "2-3 letter words #1",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
        ],
    },
    {
        "id": 4,
        "pages_mpp": [17],
        "pages_wlt": [17],
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2 letter words — Flow Rate 1",
            "2 letter words — Flow Rate 2",
            "States and Provinces — with Voice",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending: 3-5 Letter Words",
        ],
        "wlt": [
            "Alphabet — Flow Rate 1",
            "Alphabet Mix #1",
            "Alphabet Mix #2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2 letter words — Flow Rate 1",
            "2 letter words — Flow Rate 2",
            "States and Provinces — Voice",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending 3 to 5-letter words",
        ],
    },
    {
        "id": 5,
        "pages_mpp": [19],
        "pages_wlt": [19],
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2 letter words — Flow Rate 1",
            "2 letter words — Flow Rate 2",
            "States and Provinces — with Voice",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Many 3 Ltr Words — Flow Rate 1",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending: 3-5 Letter Words",
        ],
        "wlt": [
            "Alphabet — Flow Rate 1",
            "Alphabet Mix #1",
            "Alphabet Mix #2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2 letter words — Flow Rate 1",
            "2 letter words — Flow Rate 2",
            "States and Provinces — Voice",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Many 3-Ltr words",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending 3 to 5-letter words",
        ],
    },
    {
        "id": 6,
        "pages_mpp": [21],
        "pages_wlt": [21],
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Many 3 Ltr Words — Flow Rate 1",
            "Many 3 Ltr Words — Flow Rate 2",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "4 letter words #1",
            "Many 4 Ltr Words — Flow Rate 1",
            "2-word phrases #1",
            "Many 2-word phrases — Flow Rate 1",
            "Binomial Expressions #1",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending: 3-5 Letter Words",
        ],
        "wlt": [
            "Alphabet Mix #1",
            "Alphabet Mix #2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Many 3-Ltr words — Flow Rate 1",
            "Many 3-Ltr words — Flow Rate 2",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "4 letter words #1",
            "Many 4-Ltr words",
            "2-word phrases #1",
            "Many 2-word phrases",
            "Binomial Expressions #1",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending 3 to 5-letter words",
        ],
    },
    {
        "id": 7,
        "pages_mpp": [23],
        "pages_wlt": [23],
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Many 3 Ltr Words — Flow Rate 1",
            "Many 3 Ltr Words — Flow Rate 2",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "4 letter words #1",
            "Many 4 Ltr Words — Flow Rate 1",
            "2-word phrases #1",
            "2-word phrases #2",
            "Many 2-word phrases — Flow Rate 1",
            "Binomial Expressions #1",
            "Binomial Expressions #2",
            "States and Provinces — with Voice",
            "States and Provinces — No Voice",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending: 3-5 Letter Words",
        ],
        "wlt": [
            "Alphabet Mix #1",
            "Alphabet Mix #2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Many 3-Ltr words — Flow Rate 1",
            "Many 3-Ltr words — Flow Rate 2",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "4 letter words #1",
            "Many 4-Ltr words",
            "2-word phrases #1",
            "2-word phrases #2",
            "Many 2-word phrases",
            "Binomial Expressions #1",
            "Binomial Expressions #2",
            "States and Provinces — Voice",
            "States and Provinces — No Voice",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending 3 to 5-letter words",
        ],
    },
    {
        "id": 8,
        # MPP block lives entirely at the top of page 25; WLT block starts after
        # it on page 25 and continues onto page 26. Special-cased in main().
        "pages_mpp": [25],
        "pages_wlt": [25, 26],
        "split_first_page": True,
        "mpp": [
            "Alphabet — Flow Rate 1",
            "Alphabet — Flow Rate 2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "Many 3 Ltr Words — Flow Rate 1",
            "Many 3 Ltr Words — Flow Rate 2",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "4 letter words #1",
            "Many 4 Ltr Words — Flow Rate 1",
            "2-word phrases #1",
            "2-word phrases #2",
            "Many 2-word phrases — Flow Rate 1",
            "Binomial Expressions #1",
            "Binomial Expressions #2",
            "States and Provinces — with Voice",
            "States and Provinces — No Voice",
            "Sending: Alphabet",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending: 3-5 Letter Words",
            "Sending: 5-7 Letter Words",
        ],
        "wlt": [
            "Alphabet Mix #1",
            "Alphabet Mix #2",
            "Numbers — Flow Rate 1",
            "Numbers — Flow Rate 2",
            "2-3 letter words #1",
            "2-3 letter words #2",
            "Many 3-Ltr words — Flow Rate 1",
            "Many 3-Ltr words — Flow Rate 2",
            "3-4 letter words #1",
            "3-4 letter words #2",
            "4 letter words #1",
            "Many 4-Ltr words",
            "2-word phrases #1",
            "2-word phrases #2",
            "Many 2-word phrases",
            "Binomial Expressions #1",
            "Binomial Expressions #2",
            "States and Provinces — Voice",
            "States and Provinces — No Voice",
            "Sending: Letters",
            "Sending: Tri-Letters",
            "Sending: Numbers",
            "Sending 3 to 5-letter words",
            "Sending 5 to 7-letter words",
        ],
    },
]


def main(pdf_path: Path, out_path: Path):
    reader = pypdf.PdfReader(str(pdf_path))
    result = []
    issues = []

    for L in LESSONS:
        if L.get("split_first_page"):
            # Lesson 8 case: MPP and start-of-WLT share page 25, then WLT
            # continues onto page 26.
            shared_page = L["pages_mpp"][0]
            shared_links = page_links(reader, shared_page)
            mpp_links, wlt_head = reading_order_two_blocks(
                shared_links, len(L["mpp"])
            )
            wlt_tail = []
            for p in L["pages_wlt"]:
                if p == shared_page:
                    continue
                wlt_tail.extend(page_links(reader, p))
            wlt_links = wlt_head + reading_sorted(wlt_tail)
        elif L["pages_mpp"] == L["pages_wlt"]:
            # Both blocks share a page — split by vertical position.
            page_all = []
            for p in L["pages_mpp"]:
                page_all.extend(page_links(reader, p))
            mpp_links, wlt_links = reading_order_two_blocks(page_all, len(L["mpp"]))
        else:
            mpp_links = []
            for p in L["pages_mpp"]:
                mpp_links.extend(page_links(reader, p))
            mpp_links = reading_sorted(mpp_links)
            wlt_links = []
            for p in L["pages_wlt"]:
                wlt_links.extend(page_links(reader, p))
            wlt_links = reading_sorted(wlt_links)

        if len(mpp_links) != len(L["mpp"]):
            issues.append(
                f"Lesson {L['id']}: MPP count mismatch — pdf={len(mpp_links)} expected={len(L['mpp'])}"
            )
        if len(wlt_links) != len(L["wlt"]):
            issues.append(
                f"Lesson {L['id']}: WLT count mismatch — pdf={len(wlt_links)} expected={len(L['wlt'])}"
            )

        mpp_pairs = list(zip(L["mpp"], [l["uri"] for l in mpp_links]))
        wlt_pairs = list(zip(L["wlt"], [l["uri"] for l in wlt_links]))

        result.append(
            {
                "id": L["id"],
                "mpp": mpp_pairs,
                "wlt": wlt_pairs,
            }
        )

    out_path.write_text(json.dumps(result, indent=2))
    print(f"Wrote {out_path}")
    if issues:
        print("\nIssues:")
        for i in issues:
            print(f"  - {i}")
    else:
        print("\nAll lesson link counts matched expected exercise counts.")


if __name__ == "__main__":
    pdf = Path(sys.argv[1])
    out = Path(sys.argv[2])
    main(pdf, out)
