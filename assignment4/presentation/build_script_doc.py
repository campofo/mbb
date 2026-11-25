"""Write the narration script (script.json) as a Word document for recording."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from build_common import build  # noqa: E402

s = json.loads((HERE / "script.json").read_text())
words = sum(len(x["text"].split()) for x in s["slides"])
blocks = [{"t": "h1", "text": "RansomHub presentation: recording script"},
          {"t": "p", "text": f"About {words} words of narration, roughly {words // 135}–{words // 125} minutes at a normal "
           "speaking pace (limit 10). Each member says their name at the start of their segment and hands over by name, "
           "and the slides carry a matching speaker tag. Replace [Member n] with real names before recording."},
          {"t": "p", "text": "**Speakers:** " + " · ".join(s["members"])}]
prev = None
for i, sl in enumerate(s["slides"], 1):
    if sl["speaker"] != prev:
        blocks.append({"t": "h2", "text": f"Segment: {sl['speaker']}"})
        prev = sl["speaker"]
    blocks.append({"t": "h3", "text": f"Slide {i}"})
    blocks.append({"t": "p", "text": sl["text"]})
build({"title": "RansomHub presentation script", "footer": "CIS*6530 Assignment 4 · presentation script",
       "sections": [{"blocks": blocks}]}, HERE / "A4_Presentation_Script.docx", HERE.parent / "tools" / "render_docx.js", pdf=False)
print("wrote A4_Presentation_Script.docx")
