"""Shared helpers: word counting and building a docx (+PDF) from a block spec."""
import json
import re
import shutil
import subprocess
from pathlib import Path

WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-/.&%$,]*")


def strip(text: str) -> str:
    return text.replace("**", "").replace("*", "")


def count_words(blocks) -> int:
    n = 0
    for b in blocks:
        if b.get("count") and b["t"] in ("p", "bullet", "note"):
            n += len(WORD.findall(strip(b["text"])))
    return n


def build(spec: dict, out_docx: Path, renderer: Path, pdf: bool = True):
    out_docx = Path(out_docx).resolve()
    subprocess.run(["node", str(renderer), str(out_docx)], input=json.dumps(spec).encode(), check=True)
    if pdf:
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out_docx.parent), str(out_docx)],
                       check=True, capture_output=True)
