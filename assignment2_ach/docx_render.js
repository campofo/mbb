// Render the JSON spec from make_docx.py (on stdin) into a .docx at argv[2].
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  ShadingType, AlignmentType, PageOrientation, HeadingLevel, LevelFormat,
  BorderStyle, VerticalAlign,
} = require("docx");

const spec = JSON.parse(fs.readFileSync(0, "utf8"));
const out = process.argv[2];
const FONT = "Georgia", SANS = "Arial";

const tr = (rs, extra = {}) => rs.map(r => new TextRun({ text: r.text, bold: r.bold, italics: r.italic, ...extra }));
const para = (rs, opts = {}, runOpts = {}) => new Paragraph({ children: tr(rs, runOpts), ...opts });

// ---- matrix (landscape Letter: 15840 x 12240, 0.5in margins -> 14400 usable)
const W = 14400;
const widths = [2300, 1000, 1000, 1000, 1000, 1100];
widths.push(W - widths.reduce((a, b) => a + b, 0));
const fill = { C: "E3F1E3", I: "F6D3D0", NA: "EEEEEE" };
const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: "888888" };
const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };

function cell(text, i, { head = false, rowCls = "" } = {}) {
  const isRating = i >= 1 && i <= 5;
  const tally = rowCls.includes("tally");
  let shade;
  if (head) shade = "36597A";
  else if (tally) shade = "DFE6EE";
  else if (isRating) shade = fill[text] || undefined;
  else if (i === 0 && rowCls.includes("added")) shade = "FFF6DC";
  return new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    borders,
    verticalAlign: isRating ? VerticalAlign.CENTER : VerticalAlign.TOP,
    shading: shade ? { type: ShadingType.CLEAR, color: "auto", fill: shade } : undefined,
    margins: { top: 50, bottom: 50, left: 70, right: 70 },
    children: [new Paragraph({
      alignment: isRating ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: [new TextRun({
        text, font: SANS,
        size: head ? 14 : isRating ? 18 : 14,
        bold: head || isRating || i === 0 || tally,
        color: head ? "FFFFFF" : (text === "I" && isRating && !tally ? "8A1810" : undefined),
      })],
    })],
  });
}

const table = new Table({
  width: { size: W, type: WidthType.DXA },
  columnWidths: widths,
  rows: [
    new TableRow({ tableHeader: true, children: spec.header.map((h, i) => cell(h, i, { head: true })) }),
    ...spec.rows.map(r => new TableRow({ cantSplit: true, children: r.cells.map((c, i) => cell(c, i, { rowCls: r.cls })) })),
  ],
});

const small = { font: SANS, size: 16 };
const matrixChildren = [
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(spec.matrix_title)] }),
  para(spec.matrix_meta, { spacing: { after: 80 } }, { font: SANS, size: 18, color: "444444" }),
  para(spec.key, { spacing: { after: 120 } }, small),
  table,
  new Paragraph({ spacing: { before: 160, after: 60 }, children: [new TextRun({ text: spec.assumptions_title, bold: true, ...small })] }),
  ...spec.assumptions.map(a => para(a, { numbering: { reference: "bullets", level: 0 }, spacing: { after: 40 } }, small)),
];

// ---- report (portrait Letter)
const reportChildren = [
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(spec.report_title)] }),
  para(spec.report_meta, { spacing: { after: 80 } }, { size: 20, color: "444444" }),
  para(spec.wc, {
    spacing: { after: 120 },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "EEF2F7" },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: "36597A", space: 6 } },
  }, { font: SANS, size: 20 }),
  ...spec.body.map(b => {
    if (b.type === "h2") return new Paragraph({ heading: HeadingLevel.HEADING_2, children: tr(b.runs) });
    if (b.type === "li") return para(b.runs, { numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 } });
    return para(b.runs, { alignment: AlignmentType.JUSTIFIED, spacing: { after: 140 } });
  }),
];

const doc = new Document({
  creator: "", lastModifiedBy: "", title: "CIS*6530 Assignment 2", description: "",
  styles: {
    default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { line: 276 } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 32, bold: true }, paragraph: { spacing: { before: 0, after: 60 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 26, bold: true },
        paragraph: { spacing: { before: 280, after: 100 }, keepNext: true, outlineLevel: 1,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "999999", space: 2 } } } },
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [
    { properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
        margin: { top: 720, bottom: 720, left: 720, right: 720 } } }, children: matrixChildren },
    { properties: { page: { size: { width: 12240, height: 15840 },
        margin: { top: 1150, bottom: 1150, left: 1220, right: 1220 } } }, children: reportChildren },
  ],
});

Packer.toBuffer(doc).then(buf => fs.writeFileSync(out, buf));
