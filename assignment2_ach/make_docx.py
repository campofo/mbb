"""Convert a built submission.html into a .docx (no author name anywhere).

Usage: python3 make_docx.py SUBMISSION_HTML OUT_DOCX
Needs: bs4, node with the `docx` package (see docx_render.js).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

HERE = Path(__file__).resolve().parent
NAME_RE = re.compile(r"^.*?(?=CIS\*6530)")  # drop anything (e.g. a name) before the course code


def runs(node, bold=False, italic=False):
    out = []
    for ch in node.children:
        if isinstance(ch, NavigableString):
            t = re.sub(r"\s+", " ", str(ch))
            if t:
                out.append({"text": t, "bold": bold, "italic": italic})
        elif ch.name in ("strong", "b"):
            out += runs(ch, True, italic)
        elif ch.name in ("em", "i"):
            out += runs(ch, bold, True)
        elif ch.name == "br":
            out.append({"text": " ", "bold": bold, "italic": italic})
        else:
            out += runs(ch, bold, italic)
    return out


def strip_edges(rs):
    if rs:
        rs[0]["text"] = rs[0]["text"].lstrip()
        rs[-1]["text"] = rs[-1]["text"].rstrip()
    return [r for r in rs if r["text"]]


def meta(div):
    t = NAME_RE.sub("", div.get_text(" ", strip=True))
    return [{"text": t, "bold": False, "italic": False}]


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    wide = soup.select_one("div.wide")
    rep = soup.select_one("div.brk")
    table = wide.select_one("table.mx")
    header = [th.get_text(" ", strip=True) for th in table.select("thead th")]
    rows = []
    for tr in table.select("tbody tr"):
        rows.append({"cls": " ".join(tr.get("class", [])).strip(),
                     "cells": [td.get_text(" ", strip=True) for td in tr.find_all("td")]})
    small = wide.select_one("div.small")
    assumptions = [strip_edges(runs(li)) for li in small.select("li")]
    body = []
    for el in rep.find_all(["h2", "p", "ul"], recursive=False):
        if el.name == "ul":
            body += [{"type": "li", "runs": strip_edges(runs(li))} for li in el.find_all("li")]
        else:
            body.append({"type": el.name, "runs": strip_edges(runs(el))})
    return {
        "matrix_title": wide.h1.get_text(" ", strip=True),
        "matrix_meta": meta(wide.select_one("div.meta")),
        "key": strip_edges(runs(wide.select_one("div.key"))),
        "header": header,
        "rows": rows,
        "assumptions_title": small.p.get_text(" ", strip=True).rstrip(":"),
        "assumptions": assumptions,
        "report_title": rep.h1.get_text(" ", strip=True),
        "report_meta": meta(rep.select_one("div.meta")),
        "wc": strip_edges(runs(rep.select_one("div.wc"))),
        "body": body,
    }


def main(src, out):
    spec = parse(Path(src).read_text(encoding="utf-8"))
    blob = json.dumps(spec)
    subprocess.run(["node", str(HERE / "docx_render.js"), str(Path(out).resolve())],
                   input=blob.encode(), check=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])
