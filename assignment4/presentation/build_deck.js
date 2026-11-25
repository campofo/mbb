// Builds the A4 presentation deck: node build_deck.js  (needs pptxgenjs)
const path = require("path");
const pptxgen = require("pptxgenjs");
const script = require("./script.json");

const SKILL = process.env.PPTX_SKILL_DIR;
const THEME = {
  name: "RansomHub Brief", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "1B1F2A", lt1: "FFFFFF", dk2: "2B3140", lt2: "F3F4F7", accent1: "C8102E", accent2: "E8A33D",
    accent3: "4A5568", accent4: "8C1C2B", accent5: "6B7A90", accent6: "2E7D5B", hlink: "C8102E", folHlink: "8C1C2B" },
};
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "RansomHub: Ransomware Campaign Intelligence";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const W = 13.33;

pres.defineSlideMaster({
  title: "DARK", background: { color: THEME.colors.dk1 },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.7, y: 2.2, w: 11.9, h: 1.6,
    fontSize: 44, bold: true, color: C.background1, fontFace: "Cambria", valign: "bottom" }, text: "" } }],
});
pres.defineSlideMaster({
  title: "CONTENT", background: { color: THEME.colors.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 9.6, h: 0.9,
      fontSize: 28, bold: true, color: C.text1, fontFace: "Cambria", valign: "middle", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.4, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: "6B7A90" },
});

function speakerTag(slide, who, dark) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.45, y: 0.5, w: 2.3, h: 0.5, rectRadius: 0.25,
    fill: { color: dark ? C.accent1 : C.background2 }, line: { color: dark ? C.accent1 : C.background2 }, objectName: "speaker" });
  slide.addText("Speaker: " + who, { x: 10.45, y: 0.5, w: 2.3, h: 0.5, align: "center", fontSize: 13, bold: true,
    color: dark ? C.background1 : C.accent1, isTextBox: true, margin: 0 });
}
function source(slide, text) {
  slide.addText(text, { x: 0.6, y: 6.95, w: 11.5, h: 0.35, fontSize: 10, color: "6B7A90", isTextBox: true, margin: 0 });
}
function card(slide, x, y, w, h, head, body, opts = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12,
    fill: { color: opts.fill || C.background2 }, line: { color: opts.fill || C.background2 }, objectName: "card" });
  slide.addText([
    { text: head, options: { bold: true, fontSize: opts.headSize || 20, color: opts.headColor || C.accent1, breakLine: true } },
    { text: body, options: { fontSize: opts.bodySize || 16, color: opts.bodyColor || C.text1 } },
  ], { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: h - 0.3, valign: "top", isTextBox: true, margin: 0, paraSpaceAfter: 6 });
}
function stat(slide, x, y, big, label, dark) {
  slide.addText(big, { x, y, w: 3.8, h: 1.2, fontSize: 54, bold: true, fontFace: "Cambria",
    color: dark ? C.accent2 : C.accent1, isTextBox: true, margin: 0 });
  slide.addText(label, { x, y: y + 1.2, w: 3.6, h: 0.9, fontSize: 15, color: dark ? C.background1 : C.text1,
    isTextBox: true, margin: 0, valign: "top" });
}
const notes = (slide, i) => slide.addNotes(script.slides[i].speaker + ": " + script.slides[i].text);

// 1. Title + members
pres.addSection({ title: "Introduction" });
let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Introduction" });
s.addText("RansomHub: the RaaS that rose on others' takedowns", { placeholder: "title" });
s.addText("CIS*6530 Assignment 4 · Ransomware Campaign Intelligence Investigation", { x: 0.7, y: 3.9, w: 11.9, h: 0.5,
  fontSize: 18, color: C.accent2, isTextBox: true, margin: 0 });
s.addText(script.members.map((m, i) => ({ text: m, options: { breakLine: i < script.members.length - 1 } })),
  { x: 0.7, y: 4.7, w: 11.9, h: 1.5, fontSize: 16, color: C.background1, isTextBox: true, margin: 0, paraSpaceAfter: 6 });
notes(s, 0);

// 2. Bottom line stats
pres.addSection({ title: "Adversary and lifecycle" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Adversary and lifecycle" });
s.addText("Bottom line: a brand, a workforce, and a six-day window", { placeholder: "title" });
speakerTag(s, script.slides[1].speaker);
stat(s, 0.6, 1.7, "210+", "victims in RansomHub's first six months (Feb–Aug 2024)");
stat(s, 4.75, 1.7, "118 h", "from RDP password spray to domain-wide encryption in our case");
stat(s, 8.9, 1.7, "Apr 2025", "1 April: infrastructure went dark; no law-enforcement action claimed");
card(s, 0.6, 4.6, 12.1, 1.9, "What this means",
  "RansomHub was a wrapper around a mobile affiliate workforce. The defender's leverage is in the long, noisy "
  + "intrusion before encryption, not in tracking the brand name.", { headSize: 20, bodySize: 18 });
source(s, "Sources: CISA AA24-242A; The DFIR Report (30 Jun 2025); The Hacker News (30 Apr 2025)");
notes(s, 1);

// 3. Diamond model
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Adversary and lifecycle" });
s.addText("One incident, four vertices: the November 2024 RDP intrusion", { placeholder: "title" });
speakerTag(s, script.slides[2].speaker);
s.addShape(pres.shapes.DIAMOND, { x: 5.17, y: 2.45, w: 3.0, h: 3.0, fill: { color: C.text1 }, line: { color: C.text1 }, objectName: "diamond" });
s.addText("RansomHub\naffiliate case", { x: 5.17, y: 3.45, w: 3.0, h: 1.0, align: "center", fontSize: 15, bold: true,
  color: C.background1, isTextBox: true, margin: 0 });
card(s, 0.6, 1.5, 4.3, 2.3, "Adversary", "Unnamed affiliate working from a VirtualBox VM (\"WINVM\", Splashtop name \"johnattan\")");
card(s, 8.43, 1.5, 4.3, 2.3, "Capability", "Password spray, Mimikatz DCSync, Atera + Splashtop, Rclone, amd64.exe -pass");
card(s, 0.6, 4.2, 4.3, 2.3, "Infrastructure", "Spray 185.190.24.54/.33 · logon 164.138.90.2 · exfil 38.180.245.207:443 (SFTP)");
card(s, 8.43, 4.2, 4.3, 2.3, "Victim", "Multi-domain AD, exposed RDP, Hyper-V, Veeam backups. Sector withheld");
source(s, "Source: The DFIR Report, \"Hide Your RDP: Password Spray Leads to RansomHub Deployment\" (30 Jun 2025)");
notes(s, 2);

// 4. Lifecycle timeline
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Adversary and lifecycle" });
s.addText("Six days inside before a single file was encrypted", { placeholder: "title" });
speakerTag(s, script.slides[3].speaker);
const days = [
  ["Day 1", "RDP spray → valid logon; RDP to DCs; Mimikatz DCSync"],
  ["Day 2", "IP Scanner + NetScan; Atera on backup servers"],
  ["Day 3", "Rclone over SFTP: 2.03 GB in ~40 min"],
  ["Day 4", "Quiet: Rclone traces cleaned up"],
  ["Day 5", "Back via Splashtop; passwords reset"],
  ["Day 6", "amd64.exe over SMB; VMs stopped; shadows + logs wiped; encryption"],
];
s.addShape(pres.shapes.LINE, { x: 0.9, y: 2.55, w: 11.6, h: 0, line: { color: C.accent3, width: 2 } });
days.forEach(([d, t], i) => {
  const x = 0.6 + i * 2.05;
  s.addShape(pres.shapes.OVAL, { x: x + 0.65, y: 2.3, w: 0.5, h: 0.5, fill: { color: i === 5 ? C.accent1 : C.text1 },
    line: { color: C.background1, width: 2 }, objectName: "dot" + i });
  s.addText(d, { x, y: 1.65, w: 1.8, h: 0.5, align: "center", fontSize: 16, bold: true, color: C.text1, isTextBox: true, margin: 0 });
  s.addText(t, { x, y: 3.0, w: 1.85, h: 2.1, fontSize: 14, color: C.text1, valign: "top", isTextBox: true, margin: 0 });
});
card(s, 0.6, 5.3, 12.1, 1.35, "Detection windows",
  "Failed-logon burst (day 1) · DCSync from a non-DC (day 1) · new RMM installs (day 2) · Rclone / SFTP on 443 (day 3)",
  { headSize: 16, bodySize: 15 });
source(s, "Source: The DFIR Report (30 Jun 2025). Recon and the demand are not evidenced in the source.");
notes(s, 3);

// 5. Payload behaviour
pres.addSection({ title: "Malware, victims, negotiation" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Malware, victims, negotiation" });
s.addText("The payload: fast, password-locked and anti-recovery", { placeholder: "title" });
speakerTag(s, script.slides[4].speaker, true);
card(s, 0.6, 1.5, 3.9, 4.0, "Encrypts",
  "Curve25519 key pair per victim; AES-256 / ChaCha20 for files. Intermittent mode: 1 MB on, 2 MB skipped. "
  + "Random extension; \"How To Restore Your Files.txt\" with no amount", { bodySize: 18 });
card(s, 4.72, 1.5, 3.9, 4.0, "Prevents recovery",
  "Stops Hyper-V VMs and ~30 processes; vssadmin Delete Shadows /all /quiet; wevtutil clears Security, System, Application logs", { bodySize: 18 });
card(s, 8.84, 1.5, 3.9, 4.0, "Evades and spreads",
  "Will not run without -pass. Self-propagates over SMB as random six-letter services. Operators' own EDRKillShifter "
  + "kills security tools via a vulnerable driver", { bodySize: 18 });
source(s, "Sources: CISA AA24-242A; Group-IB (28 Aug 2024); ESET (26 Mar 2025); The DFIR Report (30 Jun 2025)");
notes(s, 4);

// 6. RaaS structure
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Malware, victims, negotiation" });
s.addText("Why affiliates came: a 90/10 split and their own wallets", { placeholder: "title" });
speakerTag(s, script.slides[5].speaker);
s.addChart(pres.charts.DOUGHNUT, [{ name: "Split", labels: ["Affiliate", "Operator"], values: [90, 10] }], {
  x: 0.6, y: 1.5, w: 4.6, h: 4.8, holeSize: 60, chartColors: [THEME.colors.accent1, THEME.colors.accent3],
  showPercent: true, showLegend: true, legendPos: "b", legendFontFace: "+mn-lt", legendFontSize: 14,
  dataLabelColor: "FFFFFF", dataLabelFontSize: 16, dataLabelFontFace: "+mn-lt",
  showTitle: true, title: "Share of each ransom", titleFontFace: "+mn-lt", titleFontSize: 16, titleColor: THEME.colors.dk1,
});
card(s, 5.6, 1.5, 7.1, 1.5, "Operators supply", "Go lockers for Windows, Linux and ESXi; EDRKillShifter; a panel with chats; a Tor leak site");
card(s, 5.6, 3.15, 7.1, 1.5, "Affiliates bring", "Access, tools, exfiltration infrastructure and the negotiation, and they move between brands");
card(s, 5.6, 4.8, 7.1, 1.6, "House rules", "No CIS, Cuba, North Korea or China; no re-attacking payers; non-profit hospitals: data extortion only; $5,000 deposit from June 2024");
source(s, "Sources: Group-IB (28 Aug 2024); ESET (26 Mar 2025)");
notes(s, 5);

// 7. Victims
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Malware, victims, negotiation" });
s.addText("Victims are chosen by exposure and leverage, not by sector", { placeholder: "title" });
speakerTag(s, script.slides[6].speaker);
const victims = [["Christie's", "Auction · May 2024"], ["Frontier", "Telecom · Apr 2024"], ["Change Healthcare", "Health · Apr 2024 (re-extortion)"],
  ["Kawasaki Europe", "Manufacturing · Sep 2024"]];
victims.forEach(([n, d], i) => card(s, 0.6 + (i % 2) * 3.15, 1.5 + Math.floor(i / 2) * 1.6, 3.0, 1.45, n, d, { headSize: 16, bodySize: 13 }));
card(s, 7.0, 1.5, 5.7, 4.9, "Why these victims",
  "11 critical-infrastructure sectors in 210 victims (FBI). Manufacturing and healthcare lead. Entry follows exposed RDP and "
  + "edge CVEs (Citrix, FortiOS, Confluence). Rules allowing data-only extortion of hospitals point to regulatory leverage. "
  + "Geography is the only firm exclusion: the CIS.", { fill: THEME.colors.dk1, headColor: C.accent2, bodyColor: C.background1, bodySize: 15 });
card(s, 0.6, 4.75, 6.15, 1.65, "Most-hit countries", "United States, United Kingdom, Spain, France, Italy", { headSize: 16, bodySize: 14 });
source(s, "Sources: CISA AA24-242A; Bitsight; Group-IB; The Register; BleepingComputer; The Record; TechCrunch");
notes(s, 6);

// 8. Negotiation
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Malware, victims, negotiation" });
s.addText("Negotiation: high anchors, inflated claims, short clocks", { placeholder: "title" });
speakerTag(s, script.slides[7].speaker);
s.addChart(pres.charts.BAR, [{ name: "US$ thousands", labels: ["Median initial demand", "Median payment"], values: [900, 350] }], {
  x: 0.6, y: 1.5, w: 5.6, h: 4.9, barDir: "col", chartColors: [THEME.colors.accent1, THEME.colors.accent3],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontFace: "+mn-lt", dataLabelFontSize: 14, dataLabelColor: THEME.colors.dk1,
  dataLabelFormatCode: "$#,##0\"k\"", catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 13, catAxisLabelColor: THEME.colors.dk1,
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false,
  showTitle: true, title: "Arete 2024 RansomHub cases", titleFontFace: "+mn-lt", titleFontSize: 15, titleColor: THEME.colors.dk1,
});
card(s, 6.6, 1.5, 6.1, 1.55, "Claimed vs notified", "Christie's: \"500,000+\" vs 45,798 · Frontier: \"2 million+\" vs 751,895", { bodySize: 15 });
card(s, 6.6, 3.2, 6.1, 1.55, "Clocks and outcomes", "Kawasaki: countdown to 14 Sep 2024, then 487 GB published · Frontier: 9 days", { bodySize: 15 });
card(s, 6.6, 4.9, 6.1, 1.5, "Why so little chat data", "Per-victim onion chats run by affiliates: only 1 RansomHub chat among 295 public ones", { bodySize: 15 });
source(s, "Sources: Arete (Jan 2025); The Register; BleepingComputer; SC Media; ransomware.live negotiation archive");
notes(s, 7);

// 9. Law enforcement
pres.addSection({ title: "Law enforcement and recommendations" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Law enforcement and recommendations" });
s.addText("Law enforcement fed RansomHub; the market ended it", { placeholder: "title" });
speakerTag(s, script.slides[8].speaker, true);
const events = [
  ["Dec 2023", "FBI disrupts ALPHV"], ["Feb 2024", "Operation Cronos hits LockBit; RansomHub launches"],
  ["Aug 2024", "Joint advisory AA24-242A"], ["Apr 2025", "RansomHub goes dark; DragonForce claims it"],
  ["Sep 2025", "DOJ charges Scattered Spider member (RansomHub affiliate)"],
];
events.forEach(([d, t], i) => {
  const y = 1.5 + i * 0.98;
  s.addText(d, { x: 0.6, y, w: 1.6, h: 0.8, fontSize: 16, bold: true, color: C.accent1, isTextBox: true, margin: 0, valign: "middle" });
  s.addText(t, { x: 2.3, y, w: 4.6, h: 0.8, fontSize: 15, color: C.text1, isTextBox: true, margin: 0, valign: "middle" });
});
card(s, 7.3, 1.5, 5.4, 4.9, "Our judgement (moderate confidence)",
  "No action ever hit RansomHub's core. Takedowns of rivals supplied its affiliates; the advisory raised defenders' costs; "
  + "affiliate charges came after it had folded. Its affiliates moved to DragonForce and Qilin: displacement, not degradation.",
  { fill: THEME.colors.dk1, headColor: C.accent2, bodyColor: C.background1, bodySize: 16 });
source(s, "Sources: The Register (28 Dec 2024); CISA AA24-242A; The Hacker News (Apr 2025, Jul 2024); US DOJ (Sep 2025)");
notes(s, 8);

// 10. Recommendations
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Law enforcement and recommendations" });
s.addText("What to do on Monday morning", { placeholder: "title" });
speakerTag(s, script.slides[9].speaker);
const recs = [
  ["Detect", "Spray-then-success RDP logons · DCSync from non-DCs · Rclone / SFTP on 443 · unapproved RMM installs"],
  ["Respond", "Assume theft before encryption · hunt random six-letter services · verify the attacker's data claims"],
  ["Mitigate", "No internet-facing RDP · patch CISA's edge CVEs · driver blocklist on · tiered admin"],
  ["Be resilient", "Immutable offline backups with separate credentials · payment policy decided in advance · track affiliates, not brands"],
];
recs.forEach(([h, b], i) => card(s, 0.6 + (i % 2) * 6.15, 1.5 + Math.floor(i / 2) * 2.5, 5.95, 2.3, h, b, { bodySize: 15 }));
source(s, "Each recommendation traces to a finding in the report (Sections 2, 3, 6 and 8).");
notes(s, 9);

(async () => {
  const out = path.join(__dirname, "A4_RansomHub_Presentation.pptx");
  await pres.writeFile({ fileName: out });
  if (SKILL) {
    const { applyTheme } = require(path.join(SKILL, "scripts", "apply_theme.js"));
    await applyTheme(out, THEME);
  }
  console.log("wrote", out);
})();
