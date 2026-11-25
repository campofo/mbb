// Generic report renderer: reads a JSON spec on stdin, writes a .docx to argv[2].
// Block types: h1 h2 h3 p bullet table pagebreak note
// Inline markup in text: **bold**, *italic*.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  ShadingType, AlignmentType, PageOrientation, HeadingLevel, LevelFormat,
  BorderStyle, PageBreak, Footer, PageNumber,
} = require("docx");

const spec = JSON.parse(fs.readFileSync(0, "utf8"));
const FONT = "Calibri";
const BODY = 23; // 11.5pt

function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const border = { style: BorderStyle.SINGLE, size: 4, color: "8C8C8C" };
const borders = { top: border, bottom: border, left: border, right: border };

function table(b, usable) {
  const n = b.header.length;
  const w = b.widths ? b.widths.map(x => Math.round(x * usable)) : Array(n).fill(Math.floor(usable / n));
  w[w.length - 1] = usable - w.slice(0, -1).reduce((a, c) => a + c, 0);
  const size = b.size || 19;
  const cell = (text, i, head) => new TableCell({
    width: { size: w[i], type: WidthType.DXA }, borders,
    shading: head ? { type: ShadingType.CLEAR, color: "auto", fill: "1F3A5F" }
                  : (b.firstColShade && i === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: "EEF2F7" } : undefined),
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: String(text).split("\n").map(line => new Paragraph({
      children: runs(line, { font: FONT, size, bold: head || (b.firstColBold && i === 0), color: head ? "FFFFFF" : undefined }),
    })),
  });
  return new Table({
    width: { size: usable, type: WidthType.DXA }, columnWidths: w,
    rows: [
      new TableRow({ tableHeader: true, children: b.header.map((h, i) => cell(h, i, true)) }),
      ...b.rows.map(r => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, i, false)) })),
    ],
  });
}

function blocks(list, usable) {
  const out = [];
  for (const b of list) {
    switch (b.t) {
      case "h1": out.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(b.text) })); break;
      case "h2": out.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(b.text) })); break;
      case "h3": out.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(b.text) })); break;
      case "p": out.push(new Paragraph({ spacing: { after: 120 }, alignment: b.center ? AlignmentType.CENTER : undefined,
        children: runs(b.text, b.size ? { size: b.size } : {}) })); break;
      case "note": out.push(new Paragraph({ spacing: { after: 120 },
        shading: { type: ShadingType.CLEAR, color: "auto", fill: "EEF2F7" },
        border: { left: { style: BorderStyle.SINGLE, size: 18, color: "1F3A5F", space: 6 } },
        children: runs(b.text) })); break;
      case "bullet": out.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 },
        children: runs(b.text, b.size ? { size: b.size } : {}) })); break;
      case "table": out.push(table(b, usable)); out.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
        if (b.caption) out.push(new Paragraph({ spacing: { after: 160 }, children: runs(b.caption, { size: 18, italics: true }) }));
        break;
      case "pagebreak": out.push(new Paragraph({ children: [new PageBreak()] })); break;
      default: throw new Error("unknown block " + b.t);
    }
  }
  return out;
}

const LETTER = { width: 12240, height: 15840 };
const sections = spec.sections.map(s => {
  const land = s.landscape;
  const margin = 1440;
  const usable = (land ? LETTER.height : LETTER.width) - 2 * margin;
  return {
    properties: { page: { size: { ...LETTER, orientation: land ? PageOrientation.LANDSCAPE : PageOrientation.PORTRAIT },
      margin: { top: margin, bottom: margin, left: margin, right: margin } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: spec.footer + " · page ", size: 16, color: "666666" }),
                 new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "666666" })] })] }) },
    children: blocks(s.blocks, usable),
  };
});

const hstyle = (id, name, size, before, after, color) => ({
  id, name, basedOn: "Normal", next: "Normal", quickFormat: true,
  run: { font: FONT, size, bold: true, color },
  paragraph: { spacing: { before, after }, keepNext: true, outlineLevel: Number(id.slice(-1)) - 1 },
});

const doc = new Document({
  creator: "", lastModifiedBy: "", title: spec.title, description: "",
  styles: {
    default: { document: { run: { font: FONT, size: BODY }, paragraph: { spacing: { line: 264 } } } },
    paragraphStyles: [
      hstyle("Heading1", "Heading 1", 32, 240, 120, "1F3A5F"),
      hstyle("Heading2", "Heading 2", 27, 220, 100, "1F3A5F"),
      hstyle("Heading3", "Heading 3", 24, 160, 80, "333333"),
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections,
});
Packer.toBuffer(doc).then(buf => fs.writeFileSync(process.argv[2], buf));
