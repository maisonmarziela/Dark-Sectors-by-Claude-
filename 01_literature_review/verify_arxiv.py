"""Verify arXiv identifiers cited in Project CRH against the arXiv metadata API.

For each (arXiv id, expected title fragment, expected author surname) triple this
script fetches the official metadata and records whether the title and author
match what the literature review claims.  Nothing is sent to arXiv except the
identifiers themselves.

Usage:
    python verify_arxiv.py            # writes arxiv_verification.json / .md

A reference is marked VERIFIED only if BOTH the title fragment and the author
surname are found in the arXiv record.  This checks that the citation exists
and is what we say it is; it does NOT check that we have characterised the
paper's content correctly.
"""
from __future__ import annotations

import json
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "http://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

# (arXiv id, title fragment (case-insensitive), author surname fragment)
REFS: list[tuple[str, str, str]] = [
    # --- mirror matter / hidden sectors ---
    ("hep-ph/0606202", "mirror particles and mirror matter", "okun"),
    ("hep-ph/0605188", "higgs-field portal", "wilczek"),
    ("hep-ph/0507031", "mirror neutron oscillations", "berezhiani"),
    ("0804.2088", "more about neutron", "berezhiani"),
    ("2009.11046", "mirror-neutron oscillations", "abel"),
    ("2111.05543", "neutron to mirror neutron", "broussard"),
    ("hep-ph/0204256", "mirror atom bound states", "foot"),
    ("1401.3965", "mirror dark matter", "foot"),
    ("hep-ph/0008105", "early mirror universe", "berezhiani"),
    ("hep-ph/0312335", "mirror world", "berezhiani"),
    ("astro-ph/0203152", "tunguska", "foot"),
    ("1608.08632", "dark sectors 2016", "alexander"),
    ("2005.01515", "dark photon", "fabbrichesi"),
    ("1903.03616", "higgs portal", "arcadi"),
    ("hep-ph/0506256", "twin higgs", "chacko"),
    ("hep-ph/0604261", "hidden valley", "strassler"),
    ("0905.1709", "dark sectors", "dvali"),
    ("1607.06821", "nnaturalness", "arkani-hamed"),
    ("0706.2050", "species", "dvali"),
    ("1705.06726", "anomalous currents", "dror"),
    ("1303.1521", "double-disk dark matter", "fan"),
    # --- braneworlds ---
    ("hep-ph/9803315", "hierarchy problem and new dimensions", "arkani-hamed"),
    ("hep-ph/9905221", "large mass hierarchy", "randall"),
    ("hep-th/9906064", "alternative to compactification", "randall"),
    ("hep-ph/9911386", "manyfold universe", "arkani-hamed"),
    ("hep-th/0103239", "ekpyrotic universe", "khoury"),
    # --- gravity: multi-graviton / bimetric ---
    ("hep-th/0007220", "multi-graviton", "boulanger"),
    ("hep-th/0206042", "nonlinear bigravity", "damour"),
    ("hep-th/0210184", "gravity in theory space", "arkani-hamed"),
    ("1011.1232", "resummation of massive gravity", "de rham"),
    ("1109.3515", "bimetric gravity from ghost-free massive gravity", "hassan"),
    ("1203.5783", "interacting spin-2 fields", "hinterbichler"),
    ("1105.3735", "theoretical aspects of massive gravity", "hinterbichler"),
    ("1401.4173", "massive gravity", "de rham"),
    ("1512.00021", "bimetric theory", "schmidt-may"),
    ("1408.0487", "doubly coupled matter", "yamashita"),
    ("1408.1678", "couplings to matter in massive", "de rham"),
    ("0807.2838", "exchange symmetry", "hossenfelder"),
    # --- screening / environment-dependent couplings / defects ---
    ("1001.4525", "symmetron", "hinterbichler"),
    ("astro-ph/0309300", "chameleon fields", "khoury"),
    ("1709.09071", "chameleon gravity", "burrage"),
    ("gr-qc/9602056", "tensor-scalar gravity and binary-pulsar", "damour"),
    ("hep-th/9401069", "string dilaton and a least coupling principle", "damour"),
    ("1311.1244", "topological dark matter", "derevianko"),
    ("2102.13379", "topological defect dark matter", "afach"),
    # --- fifth forces / hidden mass ---
    ("0807.4363", "weak equivalence principle", "carroll"),
    ("0902.4461", "scalar dark force", "carroll"),
    ("0807.3060", "fifth force", "bovy"),
    ("hep-ph/0307284", "inverse-square law", "adelberger"),
    ("1207.2442", "torsion-balance tests", "wagner"),
    ("1408.3588", "short-range gravity", "murata"),
    ("2209.15487", "microscope", "touboul"),
    ("0808.0899", "earth-bound dark matter", "adler"),
    ("1306.5534", "dark matter in the solar system", "pitjev"),
    ("0705.4298", "earth's heat flow", "mack"),
    # --- quantum foundations / emergent spacetime ---
    ("2106.10576", "causal framework for non-linear quantum mechanics", "kaplan"),
    ("quant-ph/0105127", "decoherence, einselection", "zurek"),
    ("astro-ph/0302131", "parallel universes", "tegmark"),
    ("1005.3035", "building up spacetime", "raamsdonk"),
    ("gr-qc/9406019", "von neumann algebra automorphisms", "connes"),
    # --- collider ---
    ("2301.10731", "invisible", "atlas"),
    # --- added after the first literature pass (ids found by web search, then checked here) ---
    ("2206.12976", "ramsey interferometry", "broz"),
    ("0902.0144", "mirror gravity", "berezhiani"),
    ("1001.4444", "twin matter", "milgrom"),
    ("2003.03382", "bimetric theory", "ben"),
    ("0908.3384", "bimetric", "hohmann"),
    ("2102.00022", "short-range fifth force", "berg"),
    ("1807.04512", "light scalar dark matter", "hees"),
    ("1708.08464", "neutron star inspirals", "hook"),
    ("2105.13354", "density induced vacuum instability", "balkin"),
    ("2410.23350", "quadratically coupled dark matter", ""),
    ("1402.6144", "many classical worlds", "hall"),
    ("hep-ph/0306120", "mirror matter", "ignatiev"),
    ("astro-ph/0407623", "mirror matter-type dark matter", "foot"),
]

# Citations whose arXiv id we do not trust from memory: looked up by exact title.
TITLE_LOOKUPS: list[tuple[str, str]] = [
    ("Geophysical constraints on mirror matter within the Earth", "ignatiev"),
    ("Environmental dependence of masses and coupling constants", "olive"),
    ("Opposite thermodynamic arrows of time", "schulman"),
    ("New bounds from positronium decays on massless mirror dark photons", "vigo"),
    ("Galilean equivalence for galactic dark matter", "kesden"),
    ("state-dependent terms in quantum theory", "polkovnikov"),
    ("Have mirror micrometeorites been detected", "foot"),
    ("Detecting dark matter using centrifuging techniques", "mitra"),
]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().replace("\n", " ").split())


def fetch(params: dict[str, str]) -> ET.Element:
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "project-crh-citation-check/1.0"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return ET.fromstring(r.read())
        except Exception as exc:  # noqa: BLE001 - network errors are retried
            if attempt == 3:
                raise
            print(f"  retry after error: {exc}", file=sys.stderr)
            time.sleep(4 * (attempt + 1))
    raise RuntimeError("unreachable")


def parse_entry(e: ET.Element) -> dict:
    raw_id = e.findtext("a:id", default="", namespaces=NS)
    aid = raw_id.split("/abs/")[-1]
    base = aid.rsplit("v", 1)[0] if "v" in aid.split("/")[-1] else aid
    authors = [a.findtext("a:name", default="", namespaces=NS) for a in e.findall("a:author", NS)]
    return {
        "id": base,
        "title": " ".join(e.findtext("a:title", default="", namespaces=NS).split()),
        "authors": authors[:6] + (["et al."] if len(authors) > 6 else []),
        "n_authors": len(authors),
        "all_authors_norm": norm(" ; ".join(authors)),
        "published": e.findtext("a:published", default="", namespaces=NS)[:10],
        "journal_ref": e.findtext("arxiv:journal_ref", default="", namespaces=NS) or "",
        "doi": e.findtext("arxiv:doi", default="", namespaces=NS) or "",
    }


def main() -> int:
    out: list[dict] = []
    ids = [r[0] for r in REFS]
    got: dict[str, dict] = {}
    for i in range(0, len(ids), 20):
        chunk = ids[i : i + 20]
        root = fetch({"id_list": ",".join(chunk), "max_results": str(len(chunk))})
        for e in root.findall("a:entry", NS):
            rec = parse_entry(e)
            got[rec["id"]] = rec
        time.sleep(3.2)  # arXiv asks for <= 1 request / 3 s

    for aid, tfrag, afrag in REFS:
        rec = got.get(aid)
        if rec is None:
            out.append({"query": aid, "status": "NOT FOUND", "expected_title": tfrag, "expected_author": afrag})
            continue
        t_ok = norm(tfrag) in norm(rec["title"])
        a_ok = norm(afrag) in rec["all_authors_norm"]
        out.append({"query": aid, "status": "VERIFIED" if (t_ok and a_ok) else "MISMATCH",
                    "title_match": t_ok, "author_match": a_ok,
                    "expected_title": tfrag, "expected_author": afrag,
                    **{k: v for k, v in rec.items() if k != "all_authors_norm"}})

    for title, afrag in TITLE_LOOKUPS:
        root = fetch({"search_query": f'ti:"{title}"', "max_results": "5"})
        time.sleep(3.2)
        hit = None
        for e in root.findall("a:entry", NS):
            rec = parse_entry(e)
            if norm(title) in norm(rec["title"]) and norm(afrag) in rec["all_authors_norm"]:
                hit = rec
                break
        if hit is None:
            out.append({"query": f'title:"{title}"', "status": "NOT FOUND",
                        "expected_title": title, "expected_author": afrag})
        else:
            out.append({"query": f'title:"{title}"', "status": "VERIFIED", "title_match": True,
                        "author_match": True, "expected_title": title, "expected_author": afrag,
                        **{k: v for k, v in hit.items() if k != "all_authors_norm"}})

    here = Path(__file__).resolve().parent
    (here / "arxiv_verification.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# arXiv citation verification log", "",
             "Generated by `verify_arxiv.py` from the official arXiv metadata API.",
             "`VERIFIED` = the identifier exists and both the expected title fragment and the",
             "expected author surname match the arXiv record.", "",
             "| status | arXiv id | title (from arXiv) | first authors | journal ref (from arXiv) |",
             "|---|---|---|---|---|"]
    for r in out:
        if r["status"] == "NOT FOUND":
            lines.append(f"| **NOT FOUND** | {r['query']} | (expected: {r['expected_title']}) | (expected: {r['expected_author']}) | |")
        else:
            au = ", ".join(r["authors"][:3]) + (" et al." if r["n_authors"] > 3 else "")
            st = r["status"] if r["status"] == "VERIFIED" else f"**{r['status']}**"
            lines.append(f"| {st} | {r['id']} | {r['title']} | {au} | {r['journal_ref']} |")
    n_ok = sum(r["status"] == "VERIFIED" for r in out)
    lines += ["", f"**{n_ok} of {len(out)} verified.**", ""]
    (here / "arxiv_verification.md").write_text("\n".join(lines), encoding="utf-8")

    for r in out:
        if r["status"] != "VERIFIED":
            print(r["status"], "|", r["query"], "| expected:", r["expected_title"], "/", r["expected_author"],
                  "| got:", r.get("title", "-"), "/", ", ".join(r.get("authors", [])[:3]))
    print(f"{n_ok} of {len(out)} verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
