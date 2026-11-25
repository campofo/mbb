"""Build the Assignment 4 report (.docx and .pdf). Usage: python3 build.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
from build_common import build, count_words  # noqa: E402
import content as c  # noqa: E402

LO, HI = 2200, 3000


def main():
    wc = count_words(c.BODY)
    if not LO <= wc <= HI:
        raise SystemExit(f"word count {wc} outside {LO}-{HI}")
    blocks = [dict(b, text=b["text"].replace("{WC}", f"{wc:,}")) if "text" in b else b
              for b in c.BODY + c.APPENDIX + c.REFERENCES + c.CLOSING]
    spec = {"title": c.TITLE, "footer": "CIS*6530 Assignment 4 · RansomHub", "sections": [{"blocks": blocks}]}
    build(spec, HERE / "A4_RansomHub_Report.docx", HERE / "tools" / "render_docx.js")
    print(f"word count {wc}; wrote A4_RansomHub_Report.docx/.pdf")


if __name__ == "__main__":
    main()
