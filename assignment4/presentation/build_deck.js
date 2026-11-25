// Builds the A4 presentation under academic-presentation standards:
// action titles, one exhibit per slide, >=20pt body, <=~40 body words, in-slide citations,
// conclusions slide last in the main deck, then references and appendix.
// Usage: node build_deck.js   (needs pptxgenjs; set PPTX_SKILL_DIR to apply the theme)
const path = require("path");
const pptxgen = require("pptxgenjs");
const script = require("./script.json");

const COL = { bg: "FFFFFF", primary: "1F4E79", accent: "2E75B6", alert: "C00000", body: "2D2D2D",
  muted: "6B6B6B", soft: "EBF3FA", rule: "D0D7DE" };
const FONT = "Arial";
const THEME = { name: "Academic", headFontFace: FONT, bodyFontFace: FONT,
  colors: { dk1: COL.body, lt1: "FFFFFF", dk2: COL.primary, lt2: "F2F2F2", accent1: COL.primary, accent2: COL.accent,
    accent3: COL.alert, accent4: "7F7F7F", accent5: "A5A5A5", accent6: "5B9BD5", hlink: COL.accent, folHlink: COL.primary } };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.title = "RansomHub: Ransomware Campaign Intelligence";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
const M = 0.6, W = 13.33 - 2 * M;

function base(slideIdx, title, opts = {}) {
  const s = pres.addSlide();
  s.background = { color: COL.bg };
  s.addText(title, { x: M, y: 0.3, w: W - 2.4, h: 1.1, fontFace: FONT, fontSize: 26, bold: true,
    color: COL.primary, valign: "top", isTextBox: true, margin: 0 });
  const sp = script.slides[slideIdx];
  if (sp && !opts.noSpeaker) s.addText("Speaker: " + sp.speaker, { x: 13.33 - M - 2.2, y: 0.32, w: 2.2, h: 0.4,
    fontFace: FONT, fontSize: 13, color: sp.handover ? COL.alert : COL.muted, bold: !!sp.handover, align: "right",
    isTextBox: true, margin: 0 });
  if (sp) s.addNotes(sp.speaker + ": " + sp.text);
  s.addText(String(pres.slides.length), { x: 13.33 - M - 0.6, y: 7.0, w: 0.6, h: 0.3, fontFace: FONT, fontSize: 12,
    color: COL.muted, align: "right", isTextBox: true, margin: 0 });
  return s;
}
function cite(s, text) {
  s.addText(text, { x: M, y: 6.95, w: W - 1.0, h: 0.35, fontFace: FONT, fontSize: 12, color: COL.muted,
    isTextBox: true, margin: 0 });
}
function bullets(s, items, x, y, w, h, size = 20) {
  // One plain run per bullet: pptxgenjs drops or splits bullets on multi-run paragraphs.
  s.addText(items.map((t, i) => ({ text: Array.isArray(t) ? t.map(p => p.text).join("") : t,
    options: { bullet: true, breakLine: i < items.length - 1 } })), { x, y, w, h, fontFace: FONT, fontSize: size, color: COL.body, valign: "top", paraSpaceAfter: 14,
    isTextBox: true, margin: 0 });
}
function header(s, text, x, y, w) {
  s.addText(text, { x, y, w, h: 0.45, fontFace: FONT, fontSize: 20, bold: true, color: COL.accent, isTextBox: true, margin: 0 });
}
function table(s, rows, x, y, w, colW, size = 16, focusRow = -1) {
  const head = rows[0].map(t => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: COL.primary } } }));
  const body = rows.slice(1).map((r, i) => r.map((t, j) => ({ text: t, options: {
    bold: j === 0 || i === focusRow, color: i === focusRow ? COL.alert : COL.body,
    fill: { color: i === focusRow ? "FBE9E9" : (i % 2 ? "F6F8FA" : "FFFFFF") } } })));
  s.addTable([head, ...body], { x, y, w, colW, fontFace: FONT, fontSize: size, valign: "middle",
    border: { type: "solid", pt: 0.75, color: COL.rule }, margin: [4, 6, 4, 6] });
}

// 1. Title (dark)
let s = pres.addSlide();
s.background = { color: COL.primary };
s.addText("RansomHub rose on its rivals' takedowns and collapsed without a police action", { x: M + 0.1, y: 1.2,
  w: 11.5, h: 2.0, fontFace: FONT, fontSize: 36, bold: true, color: "FFFFFF", valign: "top", isTextBox: true, margin: 0 });
s.addText("A ransomware campaign intelligence investigation · CIS*6530 Assignment 4 · November 2026", { x: M + 0.1, y: 3.4,
  w: 11.5, h: 0.5, fontFace: FONT, fontSize: 18, color: "CFE0F1", isTextBox: true, margin: 0 });
s.addText(script.members.map((m, i) => ({ text: m, options: { breakLine: i < script.members.length - 1 } })),
  { x: M + 0.1, y: 4.4, w: 11.5, h: 1.6, fontFace: FONT, fontSize: 18, color: "FFFFFF", paraSpaceAfter: 8,
    isTextBox: true, margin: 0 });
s.addNotes(script.slides[0].speaker + ": " + script.slides[0].text);

// 2. Research question
s = base(1, "Our question: how did RansomHub operate, and did law enforcement change it?");
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.4, y: 1.8, w: 10.5, h: 2.1, rectRadius: 0.1,
  fill: { color: COL.soft }, line: { color: COL.accent, width: 1.5 } });
s.addText("How did RansomHub's affiliates break in, extort and negotiate, and did any law-enforcement action degrade "
  + "the operation, or did its affiliates simply move to other brands?", { x: 1.7, y: 1.95, w: 9.9, h: 1.8,
  fontFace: FONT, fontSize: 22, color: COL.primary, valign: "middle", isTextBox: true, margin: 0 });
bullets(s, [[{ text: "Evidence: ", bold: true }, { text: "one fully logged intrusion (Nov 2024) plus 18 public sources" }],
  [{ text: "Methods: ", bold: true }, { text: "Diamond Model, kill chain, before/after comparison of each action" }]],
  M, 4.4, W, 2.0);
cite(s, "Sources listed on the References slide");

// 3. Context timeline
s = base(2, "Takedowns of ALPHV and LockBit handed RansomHub its first affiliates");
const tl = [["Dec 2023", "FBI disrupts ALPHV"], ["Feb 2024", "Cronos hits LockBit;\nRansomHub launches"],
  ["Aug 2024", "210+ victims;\nFBI/CISA advisory"], ["Apr 2025", "Infrastructure\ngoes dark"]];
s.addShape(pres.shapes.LINE, { x: 1.0, y: 3.0, w: 11.3, h: 0, line: { color: COL.rule, width: 3 } });
tl.forEach(([d, t], i) => {
  const x = 0.8 + i * 3.25, hot = i === 2;
  s.addShape(pres.shapes.OVAL, { x: x + 1.1, y: 2.78, w: 0.45, h: 0.45, fill: { color: hot ? COL.alert : COL.primary },
    line: { color: "FFFFFF", width: 2 } });
  s.addText(d, { x, y: 2.05, w: 2.7, h: 0.5, align: "center", fontFace: FONT, fontSize: 20, bold: true,
    color: hot ? COL.alert : COL.primary, isTextBox: true, margin: 0 });
  s.addText(t, { x, y: 3.45, w: 2.7, h: 1.0, align: "center", fontFace: FONT, fontSize: 17, color: COL.body,
    isTextBox: true, margin: 0 });
});
s.addText("Six months from launch to the largest victim count of any RaaS brand in 2024", { x: 0.6, y: 4.85, w: 12.1,
  h: 0.6, align: "center", fontFace: FONT, fontSize: 20, italic: true, color: COL.alert, isTextBox: true, margin: 0 });
cite(s, "CISA AA24-242A (2024); The Register (28 Dec 2024); ESET (2025); The Hacker News (30 Apr 2025)");

// 4. Methods: Diamond
s = base(3, "One fully logged intrusion anchors our Diamond Model");
s.addShape(pres.shapes.DIAMOND, { x: 2.35, y: 2.55, w: 2.5, h: 2.5, fill: { color: COL.soft }, line: { color: COL.accent, width: 2 } });
s.addText("Nov 2024\nintrusion", { x: 2.35, y: 3.35, w: 2.5, h: 0.9, align: "center", valign: "middle", fontFace: FONT,
  fontSize: 16, bold: true, color: COL.primary, isTextBox: true, margin: 0 });
const dv = [["Adversary", "unnamed affiliate on a VM", 2.1, 1.55, 3.0], ["Infrastructure", "spray, logon and exfil IPs", 0.45, 3.35, 1.85],
  ["Capability", "spray, Mimikatz, RMM, Rclone", 4.9, 3.35, 2.1], ["Victim", "multi-domain AD, exposed RDP", 2.1, 5.15, 3.0]];
dv.forEach(([h, t, x, y, w]) => s.addText([{ text: h, options: { bold: true, color: COL.primary, breakLine: true } },
  { text: t, options: { color: COL.body } }], { x, y, w, h: 0.95, align: "center", valign: "middle", fontFace: FONT, fontSize: 16,
  isTextBox: true, margin: 0 }));
header(s, "Why this case", 7.4, 1.7, 5.3);
bullets(s, ["Every kill-chain stage in the victim's own logs", "Hashed tools, measured 2.03 GB exfiltration",
  [{ text: "Gap: ", bold: true }, { text: "affiliate identity and the ransom demand" }]], 7.4, 2.3, 5.3, 3.6);
cite(s, "The DFIR Report, \"Hide Your RDP: Password Spray Leads to RansomHub Deployment\" (30 Jun 2025)");

// 5. Results: six days
s = base(4, "The intruder spent six days inside before encrypting anything");
const days = [["Day 1", "Spray succeeds;\nDCSync"], ["Day 2", "Scans;\nAtera installed"], ["Day 3", "2.03 GB\nexfiltrated"],
  ["Day 4", "Clean-up"], ["Day 5", "Back via\nSplashtop"], ["Day 6", "Encryption"]];
s.addShape(pres.shapes.LINE, { x: 0.9, y: 2.55, w: 7.2, h: 0, line: { color: COL.rule, width: 3 } });
days.forEach(([d, t], i) => {
  const x = 0.6 + i * 1.3, hot = i === 5;
  s.addShape(pres.shapes.OVAL, { x: x + 0.4, y: 2.35, w: 0.4, h: 0.4, fill: { color: hot ? COL.alert : COL.primary },
    line: { color: "FFFFFF", width: 2 } });
  s.addText(d, { x, y: 1.75, w: 1.2, h: 0.45, align: "center", fontFace: FONT, fontSize: 17, bold: true,
    color: hot ? COL.alert : COL.primary, isTextBox: true, margin: 0 });
  s.addText(t, { x: x - 0.05, y: 2.95, w: 1.3, h: 1.1, align: "center", fontFace: FONT, fontSize: 16, color: COL.body,
    isTextBox: true, margin: 0 });
});
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 4.5, w: 7.5, h: 1.0, rectRadius: 0.08, fill: { color: "FBE9E9" },
  line: { color: COL.alert, width: 1 } });
s.addText("118 hours from first logon to ransomware", { x: 0.6, y: 4.5, w: 7.5, h: 1.0, align: "center", valign: "middle",
  fontFace: FONT, fontSize: 22, bold: true, color: COL.alert, isTextBox: true, margin: 0 });
header(s, "Detection chances", 8.7, 1.7, 4.0);
bullets(s, ["Failed-logon burst", "DCSync from a non-DC", "New RMM installs", "Rclone/SFTP on port 443"], 8.7, 2.3, 4.0, 3.6);
cite(s, "The DFIR Report (30 Jun 2025)");

// 6. Results: payload flow
s = base(5, "The encryptor removes every recovery route before it encrypts");
const steps = ["Stop VMs and ~30 processes", "Delete shadow copies", "Clear event logs", "Encrypt (Curve25519 + AES/ChaCha20)"];
steps.forEach((t, i) => {
  const x = 0.6 + i * 3.1, hot = i === 3;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.9, w: 2.7, h: 1.5, rectRadius: 0.08,
    fill: { color: hot ? "FBE9E9" : COL.soft }, line: { color: hot ? COL.alert : COL.accent, width: 1.5 } });
  s.addText(t, { x: x + 0.1, y: 1.9, w: 2.5, h: 1.5, align: "center", valign: "middle", fontFace: FONT, fontSize: 18,
    bold: hot, color: hot ? COL.alert : COL.primary, isTextBox: true, margin: 0 });
  if (i < 3) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 2.73, y: 2.45, w: 0.34, h: 0.4, fill: { color: COL.muted }, line: { color: COL.muted } });
});
bullets(s, [[{ text: "Locked: ", bold: true }, { text: "will not run without -pass" }],
  [{ text: "Fast: ", bold: true }, { text: "large files encrypted 1 MB on, 2 MB skipped" }],
  [{ text: "Blinding: ", bold: true }, { text: "operators' EDRKillShifter disables security tools" }]], M, 4.0, W, 2.6);
cite(s, "CISA AA24-242A (2024); Group-IB (2024); ESET (2025); The DFIR Report (2025)");

// 7. Results: 90/10
s = base(6, "Affiliates kept 90% of each ransom and held the wallet");
s.addChart(pres.charts.DOUGHNUT, [{ name: "Split", labels: ["Affiliate", "Operator"], values: [90, 10] }], {
  x: M, y: 1.5, w: 5.6, h: 5.1, holeSize: 58, chartColors: [COL.primary, "A5A5A5"], showPercent: true,
  showLegend: true, legendPos: "b", legendFontFace: FONT, legendFontSize: 16, dataLabelColor: "FFFFFF",
  dataLabelFontSize: 18, dataLabelFontFace: FONT, showTitle: false });
s.addText("Ransom paid straight\nto the affiliate", { x: 2.05, y: 3.35, w: 2.7, h: 0.9, align: "center", fontFace: FONT,
  fontSize: 14, bold: true, color: COL.alert, isTextBox: true, margin: 0 });
header(s, "Why affiliates came", 7.0, 1.7, 5.7);
bullets(s, ["ALPHV had kept a $22M ransom from its own affiliate", "Rules: no CIS targets, no re-attacking payers",
  "$5,000 deposit from June 2024"], 7.0, 2.3, 5.7, 3.8);
cite(s, "Group-IB (28 Aug 2024); ESET (26 Mar 2025); TechCrunch (15 Apr 2024)");

// 8. Results: victims
s = base(7, "Exposure, more than sector, decided who became a victim");
table(s, [["Victim", "Sector", "Date", "Outcome"],
  ["Change Healthcare", "Healthcare", "Apr 2024", "Re-extorted after paying ALPHV"],
  ["Frontier", "Telecoms", "Apr 2024", "751,895 notified"],
  ["Christie's", "Auction", "May 2024", "Refused; data \"sold\""],
  ["Kawasaki Europe", "Manufacturing", "Sep 2024", "Refused; 487 GB published"]], M, 1.65, 7.4, [2.2, 1.7, 1.2, 2.3], 16);
header(s, "Pattern", 8.5, 1.7, 4.2);
bullets(s, ["Entry via exposed RDP and edge-device CVEs", "11 critical-infrastructure sectors among 210 victims",
  "Only firm exclusion: CIS countries"], 8.5, 2.3, 4.2, 4.0);
cite(s, "CISA AA24-242A; The Register; BleepingComputer; SC Media; TechCrunch (2024)");

// 9. Results: negotiation
s = base(8, "Victims who paid settled at about 39% of the opening demand");
s.addChart(pres.charts.BAR, [{ name: "US$ thousands", labels: ["Median initial demand", "Median payment"], values: [900, 350] }], {
  x: M, y: 1.5, w: 6.4, h: 5.1, barDir: "col", chartColors: [COL.primary, COL.accent], showValue: true,
  dataLabelPosition: "outEnd", dataLabelFontFace: FONT, dataLabelFontSize: 18, dataLabelColor: COL.body,
  dataLabelFormatCode: "$#,##0\"k\"", catAxisLabelFontFace: FONT, catAxisLabelFontSize: 16, catAxisLabelColor: COL.body,
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, showTitle: false });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.5, y: 1.7, w: 2.3, h: 0.6, rectRadius: 0.06, fill: { color: "FBE9E9" },
  line: { color: COL.alert, width: 1 } });
s.addText("≈ 39% of demand", { x: 4.5, y: 1.7, w: 2.3, h: 0.6, align: "center", valign: "middle", fontFace: FONT,
  fontSize: 16, bold: true, color: COL.alert, isTextBox: true, margin: 0 });
header(s, "Pressure tactics", 7.6, 1.7, 5.1);
bullets(s, ["Inflated claims: Christie's \"500,000\" vs 45,798 notified", "Countdown clocks: Kawasaki, Frontier",
  "Only 1 of 295 public chats is RansomHub's"], 7.6, 2.3, 5.1, 4.0);
cite(s, "Arete (Jan 2025), 2024 incident-response cases; The Register; BleepingComputer; ransomware.live");

// 10. Discussion: law enforcement
s = base(9, "No action reached RansomHub's core; its affiliates moved to other brands");
table(s, [["Action", "Date", "Effect on RansomHub"],
  ["ALPHV and LockBit takedowns", "Dec 2023 to Feb 2024", "Supplied its affiliates"],
  ["Joint advisory AA24-242A", "Aug 2024", "Tradecraft unchanged"],
  ["Charges against Scattered Spider (an affiliate)", "Sep 2025", "Came after the collapse"],
  ["None claimed", "Apr 2025", "Went dark; DragonForce, Qilin absorb affiliates"]], M, 1.65, 8.0, [3.2, 2.0, 2.8], 16, 3);
header(s, "Limitation", 9.0, 1.7, 3.7);
bullets(s, ["Cause of April 2025 collapse unconfirmed", "A sealed investigation cannot be ruled out"], 9.0, 2.3, 3.7, 3.8);
cite(s, "The Register (2024); CISA (2024); Microsoft via The Hacker News (2024); US DOJ (2025); The Hacker News (2025)");

// 11. Recommendations
s = base(10, "Defenders get four chances to stop the attack before encryption");
table(s, [["Area", "First action", "Traces to"],
  ["Detect", "Alert on spray-then-success RDP, DCSync, Rclone/SFTP on 443", "Slide 5"],
  ["Respond", "Assume theft first; verify the attacker's data claims", "Slides 6, 9"],
  ["Mitigate", "No internet-facing RDP; patch edge CVEs; tiered admin", "Slides 5, 8"],
  ["Be resilient", "Offline backups; payment policy decided in advance", "Slides 6, 9"]], M, 1.65, W, [2.0, 8.0, 2.13], 18);
cite(s, "Each action traces to a finding in the report (Sections 2, 3, 6 and 8)");

// 12. Conclusions (dark, stays up during Q&A)
s = pres.addSlide();
s.background = { color: COL.primary };
s.addText("Conclusions", { x: M, y: 0.4, w: W, h: 0.5, fontFace: FONT, fontSize: 22, color: "CFE0F1", isTextBox: true, margin: 0 });
s.addText([
  { text: "1. RansomHub was a brand around a mobile affiliate workforce: ", options: { bold: true, breakLine: false } },
  { text: "takedowns of rivals built it; market pressure ended it.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 10 } },
  { text: "2. The defender's window is the six days before encryption, ", options: { bold: true, breakLine: false } },
  { text: "where every stage left a detectable trace.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 10 } },
  { text: "3. Track affiliates and tradecraft, ", options: { bold: true, breakLine: false } },
  { text: "because the same playbook now runs under DragonForce and Qilin.", options: {} },
], { x: M, y: 1.3, w: W, h: 4.3, fontFace: FONT, fontSize: 22, color: "FFFFFF", valign: "top", isTextBox: true, margin: 0 });
s.addText("Questions and feedback welcome · [group contact email]", { x: M, y: 6.3, w: W, h: 0.5, fontFace: FONT,
  fontSize: 16, color: "CFE0F1", isTextBox: true, margin: 0 });
s.addNotes(script.slides[11].speaker + ": " + script.slides[11].text);

// 13. References
s = base(12, "References", { noSpeaker: true });
const refs = [
  "Arete (2025). Malware Spotlight: RansomHub Ransomware.",
  "CISA, FBI, MS-ISAC & HHS (2024). #StopRansomware: RansomHub Ransomware, AA24-242A.",
  "ESET Research (2025). Shifting the sands of RansomHub's EDRKillShifter. WeLiveSecurity.",
  "Group-IB (2024). RansomHub ransomware-as-a-service.",
  "Ransomware.live (2024). Negotiation archive: RansomHub chat.",
  "The DFIR Report (2025). Hide Your RDP: Password Spray Leads to RansomHub Deployment.",
  "The Hacker News (2024). Scattered Spider adopts RansomHub and Qilin (reporting Microsoft Threat Intelligence).",
  "The Hacker News (2025). RansomHub went dark April 1; affiliates fled to Qilin, DragonForce claimed control.",
  "The Register (2024). Christie's data sold (4 Jun); How takedowns of LockBit and ALPHV led to RansomHub's rise (28 Dec).",
  "BleepingComputer (2024). Frontier warns 750,000 of a data breach after extorted by RansomHub.",
  "SC Media (2024). RansomHub releases 487GB of Kawasaki Motors Europe data. TechCrunch (2024). Change Healthcare / RansomHub.",
  "U.S. Department of Justice (2025). United Kingdom national charged in connection with multiple cyber attacks.",
];
s.addText(refs.map((r, i) => ({ text: r, options: { breakLine: i < refs.length - 1 } })), { x: M, y: 1.2, w: W, h: 5.6,
  fontFace: FONT, fontSize: 13, color: COL.body, paraSpaceAfter: 6, valign: "top", isTextBox: true, margin: 0 });

// 14. Appendix A: IOCs
s = base(13, "Appendix A: six indicators from the modelled case support retrospective hunting", { noSpeaker: true });
table(s, [["Indicator", "Context"], ["185.190.24[.]54 / .33", "RDP password-spray sources"], ["164.138.90[.]2", "Interactive RDP logon"],
  ["38.180.245[.]207:443", "Rclone SFTP exfiltration"], ["SHA-256 25117dcb…97328cb", "amd64.exe (encryptor)"],
  ["How To Restore Your Files.txt", "Ransom note name"], ["brahma2023[@]onionmail[.]org", "Email linked to RansomHub"]],
  M, 1.65, W, [5.0, 7.13], 16);
cite(s, "The DFIR Report (2025); CISA AA24-242A (2024). Full list in report Appendix A.");

// 15. Appendix B: anticipated question
s = base(14, "Appendix B: the April 2025 collapse is best explained by the market, on current evidence", { noSpeaker: true });
bullets(s, [[{ text: "For a market explanation: ", bold: true }, { text: "DragonForce's public claim; affiliate moves to Qilin; new brands such as VanHelsing" }],
  [{ text: "Against: ", bold: true }, { text: "no agency comment either way; sealed cases are invisible" }],
  [{ text: "Confidence: ", bold: true }, { text: "moderate" }]], M, 1.7, W, 4.5);
cite(s, "The Hacker News (30 Apr 2025); Rapid7 Q2 2025 ransomware trends");

(async () => {
  const out = path.join(__dirname, "A4_RansomHub_Presentation.pptx");
  await pres.writeFile({ fileName: out });
  if (process.env.PPTX_SKILL_DIR) {
    const { applyTheme } = require(path.join(process.env.PPTX_SKILL_DIR, "scripts", "apply_theme.js"));
    await applyTheme(out, THEME);
  }
  console.log("wrote", out, pres.slides.length, "slides");
})();
