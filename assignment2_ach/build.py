"""Build the A2 submission PDF from ach_matrix.csv + report_body.html.

Usage: python3 build.py   (needs a Chrome/Chromium binary; set CHROME)
"""
import csv
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDENT = "Clement Ampofo"
PDF_NAME = "Ampofo_Clement_A2.pdf"
CHROME = "/opt/pw-browsers/chromium"  # any Chrome/Chromium binary

HYP = [
    ("H1", "State-linked espionage"),
    ("H2", "Independent insider"),
    ("H3", "Cybercriminal intrusion"),
    ("H4", "Benign / false alarm"),
    ("H5", "Competitor-directed insider (added)"),
]

ASSUMPTIONS = [
    ("A1", "The workstation hosting the RAT (item 2) is <em>not</em> confirmed to be the resigning "
           "scientist's; the scenario says only &quot;the same research division,&quot; so I treat the owner as unknown."),
    ("A2", "The phished scientist (item 3) and the resigning scientist (item 1) are two different people, "
           "as item 10 lists them as two separate anomalous accounts."),
    ("A3", "Reconstructed timeline (day 0 = first evening of bulk download): ACL misconfigured from ~day &minus;42; "
           "phishing ~day &minus;21; phished credentials reused ~day &minus;19; RAT installed ~day &minus;10; "
           "download on days 0 and 1; resignation ~day 3. The ACL fault therefore predates the intrusion."),
    ("A4", "The &quot;previously unseen device&quot; in item 3 has not been verified as a new personal device of the "
           "phished scientist; if it were, the H4 rating on item 3 would soften to C."),
]


def word_count(fragment: str) -> int:
    body = re.sub(r"<h[1-6][^>]*>.*?</h[1-6]>", " ", fragment, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-/.&%]*", text))


def matrix_html() -> str:
    with open(HERE / "ach_matrix.csv", newline="") as f:
        rows = list(csv.reader(f))
    head = "".join(f"<th>{h}<br><span class='hn'>{n}</span></th>" for h, n in HYP)
    out = [f"<table class='mx'><thead><tr><th class='ev'>Evidence item</th>{head}"
           f"<th class='nt'>Justification / notes</th></tr></thead><tbody>"]
    for r in rows[1:]:
        ev, ratings, note = r[0], r[1:6], r[6]
        tally = ev.lower().startswith("inconsistency tally")
        added = ev.startswith("E12")
        cls = "tally" if tally else ("added" if added else "")
        cells = "".join(
            f"<td class='r r{v.strip()}'>{html.escape(v)}</td>" if not tally
            else f"<td class='r rt'>{html.escape(v)}</td>"
            for v in ratings)
        out.append(f"<tr class='{cls}'><td class='ev'>{html.escape(ev)}</td>{cells}"
                   f"<td class='nt'>{html.escape(note)}</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def build():
    body = (HERE / "report_body.html").read_text()
    wc = word_count(body)
    assert 1200 <= wc <= 1800, f"word count {wc} out of range"
    assumptions = "".join(f"<li><strong>{k} [ADDED, student assumption]:</strong> {v}</li>"
                          for k, v in ASSUMPTIONS)
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{STUDENT} A2</title>
<style>
@page {{ size: Letter; margin: 0.8in 0.85in; }}
@page wide {{ size: Letter landscape; margin: 0.5in 0.55in; }}
body {{ font-family: "Georgia", "Times New Roman", serif; font-size: 11pt; line-height: 1.42; color: #111; }}
h1 {{ font-size: 17pt; margin: 0 0 2pt; }}
h2 {{ font-size: 13pt; margin: 16pt 0 5pt; border-bottom: 1px solid #999; padding-bottom: 2pt; }}
.meta {{ color: #444; font-size: 10pt; margin-bottom: 10pt; }}
.wc {{ font-family: Helvetica, Arial, sans-serif; font-size: 10pt; background: #eef2f7; border-left: 3px solid #36597a; padding: 5pt 8pt; margin: 6pt 0 4pt; }}
p {{ margin: 0 0 7pt; text-align: justify; }}
ul {{ margin: 0 0 7pt 0; padding-left: 18pt; }} li {{ margin-bottom: 3pt; }}
.wide {{ page: wide; font-family: Helvetica, Arial, sans-serif; }}
.wide h1 {{ font-family: Georgia, serif; }}
table.mx {{ border-collapse: collapse; width: 100%; font-size: 7.6pt; line-height: 1.25; }}
.mx th, .mx td {{ border: 1px solid #888; padding: 3pt 4pt; vertical-align: top; }}
.mx th {{ background: #36597a; color: #fff; font-size: 8pt; }}
.mx .hn {{ font-weight: normal; font-size: 6.6pt; }}
.mx td.ev {{ width: 17%; font-weight: bold; }}
.mx td.r {{ width: 4.6%; text-align: center; vertical-align: middle; font-weight: bold; font-size: 9pt; }}
.mx .rC {{ background: #e3f1e3; }} .mx .rI {{ background: #f6d3d0; color: #8a1810; }} .mx .rNA {{ background: #eeeeee; color: #555; }}
.mx tr.added td.ev {{ background: #fff6dc; }}
.mx tr.tally td {{ background: #dfe6ee; font-weight: bold; }} .mx .rt {{ font-size: 11pt; }}
.mx tr {{ page-break-inside: avoid; }}
.small {{ font-size: 8.4pt; line-height: 1.3; }} .small li {{ margin-bottom: 2pt; }}
.key {{ font-size: 8.2pt; margin: 3pt 0 6pt; }}
.brk {{ break-before: page; }}
</style></head><body>
<div class="wide">
<h1>Assignment 2: Analysis of Competing Hypotheses: Aurora Biotech Labs</h1>
<div class="meta">{STUDENT} &middot; CIS*6530 Cyber Threat Intelligence and Adversarial Risk Analysis &middot; Deliverable 2.1: ACH matrix</div>
<div class="key"><strong>Key:</strong> C = Consistent &middot; I = Inconsistent &middot; NA = Not applicable / diagnostic-neutral.
Rows 1 to 11 are scenario evidence (all retained). Row E12 (shaded yellow) and assumptions A1 to A4 are the student's own additions, not scenario facts.
The most diagnostic items are 6, 9 and 4 with E12 (report section 3). Items 1, 7, 8, 10 and 11 are consistent with all or nearly all hypotheses and confirm very little.</div>
{matrix_html()}
<div class="small"><p style="margin-top:6pt"><strong>Student-added assumptions (not scenario facts)</strong></p><ul>{assumptions}</ul></div>
</div>
<div class="brk">
<h1>Deliverable 2.2: Analytic report</h1>
<div class="meta">{STUDENT} &middot; CIS*6530 &middot; Assignment 2</div>
<div class="wc"><strong>Word count: {wc:,}</strong> (body text only; excludes the ACH matrix, section headers, and this line)</div>
{body}
</div>
</body></html>"""
    (HERE / "submission.html").write_text(page)

    import subprocess
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", f"--print-to-pdf={HERE / PDF_NAME}",
                    (HERE / "submission.html").as_uri()], check=True, capture_output=True)
    print(f"word count = {wc}; wrote {PDF_NAME}")


if __name__ == "__main__":
    build()
