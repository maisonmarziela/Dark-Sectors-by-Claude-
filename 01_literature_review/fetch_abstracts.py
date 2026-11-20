"""Print the arXiv abstracts of the papers whose *specific quantitative claims* are
used in Project CRH, so the claims can be checked against the authors' own words.

Usage:  python fetch_abstracts.py [id1 id2 ...]      (default: the KEY list below)
Writes key_abstracts.md next to this file when run with the default list.
"""
from __future__ import annotations

import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

KEY = [
    "0902.0144", "0808.0899", "1306.5534", "hep-ph/0005125", "0807.4363",
    "astro-ph/0301229", "2102.00022", "1303.1521", "2410.23350", "2105.13354",
    "hep-ph/9911386", "hep-th/0007220", "1408.1678", "1905.09128", "2301.10731",
    "1001.4525", "1708.08464", "cond-mat/9911101", "2106.10576", "1807.04512",
]
NS = {"a": "http://www.w3.org/2005/Atom"}


def main() -> int:
    ids = sys.argv[1:] or KEY
    url = "http://export.arxiv.org/api/query?id_list=" + ",".join(ids) + f"&max_results={len(ids)}"
    req = urllib.request.Request(url, headers={"User-Agent": "project-crh-citation-check/1.0"})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=60).read())
    blocks = []
    for e in root.findall("a:entry", NS):
        aid = e.findtext("a:id", namespaces=NS).split("/abs/")[-1]
        title = " ".join(e.findtext("a:title", namespaces=NS).split())
        summary = " ".join(e.findtext("a:summary", namespaces=NS).split())
        blocks.append(f"## arXiv:{aid} — {title}\n\n> {summary}\n")
    text = "# Abstracts of key references (verbatim from arXiv)\n\n" + "\n".join(blocks)
    if not sys.argv[1:]:
        (Path(__file__).resolve().parent / "key_abstracts.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
