"""Count the words of law text in each section of Title 26 (USLM XML).

Usage: python -I tools/parse_usc26.py <usc26.xml> <out.csv>

Counts only the operative text of each section: the heading and the body.
Editorial notes (<notes>, <note>) and source credits (<sourceCredit>) are not
law text and are left out.
"""

import csv
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://xml.house.gov/schemas/uslm/1.0}"
LEVELS = ["subtitle", "chapter", "subchapter", "part", "subpart"]
SKIP = {NS + "notes", NS + "note", NS + "sourceCredit"}
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-.,%$()§]*")


def text_of(el):
    """All text inside el, without skipped elements."""
    parts = []

    def walk(e):
        if e.tag in SKIP:
            if e.tail:
                parts.append(e.tail)
            return
        if e.text:
            parts.append(e.text)
        for c in e:
            walk(c)
        if e.tail and e is not el:
            parts.append(e.tail)

    walk(el)
    return " ".join(parts)


def main(src, out):
    tree = ET.parse(src)
    root = tree.getroot()
    rows = []

    def visit(el, path):
        tag = el.tag.replace(NS, "")
        if tag in LEVELS:
            num = el.find(NS + "num")
            head = el.find(NS + "heading")
            path = dict(path)
            path[tag] = (num.get("value") if num is not None else "") or ""
            path[tag + "_heading"] = (head.text or "").strip() if head is not None else ""
            # Clear lower levels.
            for lower in LEVELS[LEVELS.index(tag) + 1:]:
                path.pop(lower, None)
                path.pop(lower + "_heading", None)
        if tag == "section" and el.get("identifier", "").startswith("/us/usc/t26/s"):
            num = el.find(NS + "num")
            head = el.find(NS + "heading")
            heading = " ".join(text_of(head).split()) if head is not None else ""
            body = text_of(el)
            words = len(WORD.findall(body))
            rows.append(
                {
                    "section": el.get("identifier").rsplit("/s", 1)[1],
                    "heading": heading,
                    "status": el.get("status", ""),
                    "words": words,
                    **{k: path.get(k, "") for k in LEVELS},
                    **{k + "_heading": path.get(k + "_heading", "") for k in LEVELS},
                }
            )
            return  # do not look for sections inside sections
        for c in el:
            visit(c, path)

    visit(root, {})
    fields = ["section", "heading", "status", "words"] + LEVELS + [k + "_heading" for k in LEVELS]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} sections, {sum(r['words'] for r in rows):,} words of law text")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
