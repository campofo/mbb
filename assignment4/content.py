"""Assignment 4 report content: RansomHub ransomware campaign intelligence.

Blocks with count=True are the report prose that the brief's word limit applies to
(tables, IOC/ATT&CK appendices, references, contribution statement and AI note are excluded).
"""

C = True  # counted


def P(text, count=C):
    return {"t": "p", "text": text, "count": count}


def B(text, count=C):
    return {"t": "bullet", "text": text, "count": count}


def H(level, text):
    return {"t": f"h{level}", "text": text}


def T(header, rows, widths=None, caption=None, size=19, first_bold=True):
    return {"t": "table", "header": header, "rows": rows, "widths": widths, "caption": caption,
            "size": size, "firstColBold": first_bold, "firstColShade": first_bold}


TITLE = "RansomHub: Ransomware Campaign Intelligence Investigation"

FRONT = [
    {"t": "p", "text": "CIS*6530 Cyber Threat Intelligence and Adversarial Risk Analysis · Assignment 4", "size": 20},
    H(1, TITLE),
    P("**Group members (name, student number):** [Member 1] · [Member 2] · [Member 3]", count=False),
    P("**Word count: {WC}** (report body; excludes tables, the IOC and ATT&CK appendix tables, references, "
      "the contribution statement and the AI-use note)", count=False),
    {"t": "note", "text": "**Bottom line.** RansomHub was the most prolific ransomware-as-a-service (RaaS) brand of 2024. "
     "It was built on purchased Knight code and on affiliates displaced by the LockBit and ALPHV takedowns, and it disappeared "
     "on 1 April 2025 without any law-enforcement action against its core. Its intrusions were affiliate-run and hands-on-keyboard. "
     "The representative case in this report went from an exposed RDP server to domain-wide encryption in about 118 hours, and the "
     "defensive opportunities sit in that window, not at the encryption stage.", "count": C},
]

S1 = [
    H(2, "1. Adversary profile: Diamond Model of one incident"),
    P("We model one intrusion rather than RansomHub's whole history. The DFIR Report documented it in detail [2]. "
      "It began in November 2024 with a password-spray attack on an internet-facing Remote Desktop Protocol (RDP) "
      "server and ended six days later with RansomHub encryption across the domain. We chose it as the most completely evidenced public "
      "RansomHub intrusion: telemetry for every stage, hashed tooling and a measured exfiltration volume. The victim is "
      "anonymised, which limits only that vertex."),
    T(["Feature", "Evidence for this incident", "Confidence / gaps"], [
        ["Adversary", "A RansomHub affiliate. The binary, the note and the operator tooling tie the attack to the brand [2]. "
         "The hands-on operator used a Splashtop display name \"johnattan\" from a client host \"WINVM\", and the clipboard "
         "showed 10.0.2.15, the VirtualBox NAT default. The operator was working from a virtual machine [2].",
         "Affiliate identity unknown. Brand attribution is high confidence, individual attribution none."],
        ["Capability", "Password spraying; Mimikatz (DCSync per child domain, LSASS); NirSoft CredentialsFileView; Advanced IP "
         "Scanner and SoftPerfect NetScan; Atera and Splashtop remote-management (RMM) tools; Rclone over SFTP; the RansomHub "
         "encryptor amd64.exe run with -pass and -only-local, spread over SMB via random six-letter services; vssadmin, "
         "wevtutil and Hyper-V Stop-VM before encryption [2].",
         "High. Tools were recovered and hashed."],
        ["Infrastructure", "Spray sources 185.190.24.54 and 185.190.24.33; interactive logon from 164.138.90.2; exfiltration to "
         "38.180.245.207 on TCP 443 (SFTP, not HTTPS) [2]. Legitimate Atera and Splashtop SaaS relays were used for "
         "C2-like access. Victim communication runs through RansomHub's Tor negotiation and leak infrastructure [1].",
         "High for the IPs (from logs); the hosting providers' role is unknown."],
        ["Victim", "A multi-domain Active Directory organisation with internet-exposed RDP, Hyper-V hosts, file servers and "
         "Veeam backup servers (the exfiltration script was staged in C:\\ProgramData\\Veeam\\) [2].",
         "Name, sector, size and country withheld by the source."],
    ], widths=[0.16, 0.56, 0.28], caption="Table 1. Core features (sources in brackets)."),
    T(["Meta-feature", "This incident"], [
        ["Timestamp", "November 2024; time to ransomware about 118 hours over six calendar days [2]."],
        ["Phase", "Every phase from initial access to impact is evidenced (see Section 2)."],
        ["Result", "About 2.03 GB exfiltrated in about 40 minutes on day 3; domain-wide encryption, shadow copies deleted, "
         "logs cleared on day 6 [2]. Ransom amount and payment outcome are not reported."],
        ["Direction", "Adversary → infrastructure → victim for access; victim → infrastructure (38.180.245.207) for "
         "exfiltration."],
        ["Methodology", "Human-operated double extortion: living off the land plus commercial RMM, credential theft, "
         "exfiltration before encryption."],
        ["Resources", "RaaS access (builds, panel, leak site supplied by the operator [3]); free or commercial tools; "
         "rented VPS addresses; an operator VM."],
    ], widths=[0.2, 0.8], caption="Table 2. Meta-features (all six recorded)."),
    P("Two unknowns limit this diamond: the affiliate's identity (and the affiliate, not the brand, chose the victim), "
      "and the negotiation, so Result stops at encryption. Both follow from how RaaS works."),
]

S2 = [
    H(2, "2. Attack lifecycle (Lockheed Martin Cyber Kill Chain)"),
    T(["Stage", "Evidence in this incident", "Status"], [
        ["Reconnaissance", "The affiliate found an internet-facing RDP server. How it was found (scanning or a purchased "
         "list) is not reported.", "Inferred, not evidenced"],
        ["Weaponisation", "No exploit was built. The operator supplied the encryptor, and per-victim builds need a "
         "64-character password [4].", "Not applicable / not evidenced"],
        ["Delivery", "Password spray against the RDP server from two IPs over about four hours; six accounts "
         "authenticated (Event ID 4624) [2].", "Evidenced"],
        ["Exploitation", "No vulnerability was exploited. The intruder logged on with a valid account from 164.138.90.2 "
         "with an elevated token [2].", "Evidenced (valid accounts)"],
        ["Installation", "Day 2: Atera installed on two backup servers; Splashtop used from day 5; new services "
         "(Event ID 7045); passwords reset for several users before impact [2].", "Evidenced"],
        ["Command and control", "Direct RDP throughout, plus Atera and Splashtop to blend in with administration "
         "traffic [2].", "Evidenced"],
        ["Actions on objectives", "Day 1: net/nltest discovery, RDP to two domain controllers, Mimikatz DCSync. "
         "Days 1–2: IP Scanner and NetScan sweeps. Day 3: Rclone exfiltration of 2.03 GB. Day 6: amd64.exe, SMB "
         "propagation, VM shutdown, shadow-copy deletion, log clearing, encryption [2].", "Evidenced; ransom note image "
         "only, negotiation not reported"],
    ], widths=[0.18, 0.6, 0.22], caption="Table 3. Kill-chain mapping of the same incident."),
    P("Five of seven stages are evidenced from the victim's own logs, across five days of returning sessions, repeated "
      "scans and two RMM installs, each a detection opportunity before impact. The unevidenced stages happen outside "
      "the victim: target selection and the demand."),
]

S3 = [
    H(2, "3. Malware behaviour, TTPs and indicators"),
    P("**Lineage and build.** RansomHub's encryptor reuses code from Knight, whose source code was offered for sale in "
      "February 2024 [4]. CISA describes RansomHub as formerly known as Cyclops and Knight [1]. Group-IB describes the locker as "
      "written in Go with builds for Windows, Linux and ESXi [3]. Arete reports C++ and Go components [5]. The sources agree on platforms but not language."),
    P("**Encryption.** Each victim gets its own Curve25519 key pair [1]. Group-IB says file encryption uses AES-256, "
      "ChaCha20 or XChaCha20, depending on hardware support [3]. Files under 0x100000 bytes are fully encrypted. Larger "
      "files are encrypted in 0x100000-byte chunks with 0x200000 bytes skipped between chunks. This intermittent mode trades "
      "completeness for speed. A 58-byte footer ending in 0x00ABCDEF is appended to every file [1]. The extension is "
      "random, and Arete links it to the first six characters of the public key [5]. The note is usually named "
      "\"How To Restore Your Files.txt\". It contains no amount, only a client ID, a per-victim .onion chat link and a "
      "deadline of 3 to 90 days set by the affiliate [1]."),
    P("**Execution controls and anti-recovery.** The binary will not run without a -pass value. In our incident it was "
      "launched as amd64.exe -pass [redacted] and spread itself over SMB, with -only-local preventing re-propagation loops "
      "[2]. Before encrypting, it stopped Hyper-V virtual machines, deleted shadow copies (vssadmin and "
      "Win32_ShadowCopy), set permissive symlink evaluation and cleared the Security, System and Application logs [2]. "
      "CISA lists about 30 processes (SQL, Oracle, Outlook and others) it kills first [1]."),
    P("**Exfiltration.** The encryptor has no exfiltration function [1]. Theft is therefore an affiliate choice. In this "
      "case it was Rclone driven by a hidden VBScript (nocmd.vbs → rcl.bat). An include-list of document, mail and "
      "image extensions (*.pst, *.msg, *.edb, *.pdf, *.xlsx and others) limited the haul to 2.03 GB of high-leverage "
      "files [2]."),
    P("**Defence evasion.** RansomHub's operators built and maintained their own EDR killer, EDRKillShifter, and offered "
      "it to affiliates through the panel from May 2024 [4]. It loads a vulnerable driver to terminate security "
      "products. CISA maps this behaviour to T1562.001 [1]. The full technique mapping and the cited indicators are in "
      "Appendix A (Tables A1 and A2)."),
]

S4 = [
    H(2, "4. Infrastructure and RaaS structure"),
    P("RansomHub separated development from deployment. The operators supplied the locker builds, EDRKillShifter, an "
      "affiliate panel for managing targets and chat rooms, and a Tor leak site. Each panel had its own onion domain [3]. "
      "Affiliates bought access and did the intrusions. The offer that drove recruitment was economic: affiliates kept "
      "90% of each payment and received ransoms into their own wallets, paying the operators their 10% afterwards [3][4]. "
      "For affiliates who had just watched ALPHV keep a $22 million payment from its own partner, control of the wallet "
      "addressed the main risk of working with a RaaS brand [9][14]. From 21 June 2024 the operators required a US$5,000 "
      "deposit from new affiliates [4]."),
    P("The rules show what the operators wanted to protect. Attacks on the Commonwealth of Independent States (CIS), Cuba, "
      "North Korea and China were banned. Paid victims could not be re-attacked. Non-profit hospitals could not be "
      "encrypted, although their data could still be ransomed [3]. Affiliates who broke a post-payment promise were banned "
      "[3]. These are reputational controls. A brand that lives on payments needs victims to believe that paying works."),
    P("Infrastructure reuse is low at the network layer and high at the tool layer. CISA's IP list is mostly historical "
      "and largely QakBot-linked [1]. The addresses in our incident appear in no other public RansomHub case we found. "
      "Reuse instead shows in commodity tools that recur across intrusions: Mimikatz, Rclone, AnyDesk and other RMM tools, "
      "and network scanners [1][2]. ESET also tracked one affiliate, \"QuadSwitcher\", working for RansomHub, Play, Medusa "
      "and BianLian, and assessed with high confidence that the same actor carried out those attacks [4]. In RaaS, the infrastructure that matters belongs to the affiliate and moves between brands."),
]

S5 = [
    H(2, "5. Victim and industry-targeting analysis"),
    P("By August 2024 the FBI counted at least 210 RansomHub victims across 11 critical-infrastructure sectors, including "
      "water, healthcare, government services, financial services, critical manufacturing, transportation and "
      "communications [1]. Bitsight ranks manufacturing first, followed by healthcare and professional services [16]. "
      "Group-IB names the United States, United Kingdom, Spain, France and Italy as the most-hit countries [3]. Public "
      "cases follow the same pattern. They include Christie's (auction, UK/US, May 2024) [11], Frontier Communications "
      "(telecoms, US, April 2024) [12], Kawasaki Motors Europe (manufacturing, September 2024) [13], the second extortion "
      "of Change Healthcare (healthcare, April 2024) [14], and Halliburton (energy services, August 2024). Halliburton's "
      "attribution to RansomHub is reported but has not been confirmed by the company [15]."),
    P("The breadth is the pattern. Three features of RansomHub explain it better than any sector preference. First, the "
      "initial-access methods are opportunistic: exposed RDP in our case, and CISA's list of edge-device CVEs (Citrix, "
      "FortiOS, Confluence, BIG-IP, ActiveMQ) [1]. Victims are those whose perimeter is exposed, whatever their industry. "
      "Second, affiliates choose targets, so the victim mix reflects many independent operators. Third, the rules point "
      "towards leverage. Allowing data-only extortion of hospitals, and re-extorting Change Healthcare, show the brand "
      "leaning into sectors where a leak brings regulatory and patient-safety consequences [3][14]. Manufacturing leads plausibly because downtime there is expensive. Our "
      "assessment, with moderate confidence, is that RansomHub's victimology is driven by exposure and leverage, not "
      "by choice of sector. Geography is the clear exception: the CIS ban is consistent with a Russian-speaking operator "
      "base."),
]

S6 = [
    H(2, "6. Ransom negotiation analysis"),
    P("Public negotiation data for RansomHub is unusually thin, and the reason is itself a finding. The largest public "
      "archive of ransomware chats holds 295 conversations across 31 groups but only one RansomHub chat [10]. That chat is a "
      "single templated message (encrypted servers and backups, stolen accounting, HR and client data, threats to "
      "notify clients and publish), with no amount, deadline or victim reply [10]. RansomHub's design explains the gap. "
      "Every note points to a per-victim onion chat [1]. Each affiliate panel had its own onion domain [3]. Affiliates, not "
      "the operators, ran the conversation and received the payment [3]. The shared, guessable negotiation portals that "
      "researchers scraped for other groups did not exist. Nor have its internal chats leaked, unlike LockBit's or Black Basta's."),
    P("Aggregate incident-response data fills part of the gap. Across Arete's 2024 RansomHub engagements, the median "
      "initial demand was US$900,000 and the median payment US$350,000 [5]. Victims who paid typically settled at "
      "about 39% of the opening figure. That is consistent with negotiation from a deliberately high anchor."),
    P("The public cases show the pressure tactics, and they are biased towards victims who refused to pay, because those "
      "are the cases that become visible:"),
    B("**Deadlines and countdowns.** Kawasaki Motors Europe was given a timer expiring on 14 September 2024. RansomHub then "
      "published 487 GB, which it claimed was the stolen data [13]. Frontier was given nine days [12]."),
    B("**Inflated claims as leverage.** RansomHub claimed data on at least 500,000 Christie's clients; Christie's notified "
      "45,798 [11]. It claimed more than 2 million Frontier customers; Frontier notified 751,895 [12]. Overstatement raises the perceived cost of refusal."),
    B("**Sale instead of leak.** After Christie's stopped talking, RansomHub announced the data had been sold. Analysts "
      "quoted by The Register suspected this was face-saving rather than a real sale [11]."),
    B("**Re-extortion.** RansomHub listed Change Healthcare, which had reportedly already paid ALPHV about US$22 million. "
      "It threatened to sell 4 TB unless paid again [14]. The brand's no-re-attack rule evidently covered only its own victims."),
    B("**Credibility offers.** The note offers free decryption of files under 1 MB as proof [4]. Affiliates who failed to "
      "honour a paid deal were banned [3]."),
    P("We found no public source confirming a RansomHub payment in a named case. Halliburton disclosed US$35 million in "
      "costs but did not say whether any of it was a ransom [15]. The honest conclusion is that RansomHub paid outcomes "
      "are visible only in aggregate (the Arete medians), and non-payment outcomes are visible case by case."),
]

S7 = [
    H(2, "7. Law-enforcement and disruption actions"),
    P("No arrest, indictment, sanction or seizure has been announced against RansomHub's core operators; our searches "
      "of DOJ and vendor reporting through November 2026 found none. The actions that affected it were indirect."),
    P("**Action 1: the ALPHV disruption (December 2023) and Operation Cronos against LockBit (February 2024).** These were "
      "not aimed at RansomHub, but they shaped it more than anything aimed at it. RansomHub launched on RAMP on 2 February "
      "2024 [4], between the two operations. It recruited displaced ALPHV and LockBit affiliates by offering wallet "
      "control [9][18]. *Before:* RansomHub did not exist. *After:* it had at least 210 victims within six months [1], "
      "and The Register attributes that rise to the two takedowns [9]. The effect was displacement, not degradation: "
      "the affiliates survived and changed brands."),
    P("**Action 2: the #StopRansomware joint advisory AA24-242A (29 August 2024).** The FBI, CISA, MS-ISAC and HHS "
      "published RansomHub's TTPs, CVEs, file paths, IPs and an email address [1]. *Before:* defenders relied on vendor "
      "reporting. *After:* the indicators became deployable, but tradecraft did not change. Our November 2024 case followed "
      "the advisory's TTPs closely [2][4]. An advisory raises defenders' costs; it does not touch the operators."),
    P("**Action 3: charges against Scattered Spider (Octo Tempest), a documented RansomHub affiliate.** Microsoft reported "
      "that Octo Tempest added RansomHub to its payloads in Q2 2024 [7]. In September 2025 the US Department of Justice "
      "unsealed a complaint against Thalha Jubair, a UK national, for at least 120 intrusions tied to the group, with more "
      "than US$115 million in ransom payments, alongside UK charges [8]. *Before:* the affiliate was deploying RansomHub in "
      "2024. *After:* RansomHub had already gone dark, so the charges removed affiliate capacity from the ecosystem rather "
      "than from RansomHub."),
    P("**The 1 April 2025 collapse.** RansomHub's leak site was defaced with \"R.I.P. 3/3/25\" in March, and its "
      "infrastructure went offline on 1 April 2025 [6][17]. No agency claimed it. DragonForce announced that RansomHub "
      "had \"moved\" to its new cartel infrastructure. Researchers reported affiliates migrating to Qilin and new brands "
      "such as VanHelsing forming from ex-RansomHub affiliates [6]. This was a business failure followed by fragmentation."),
    P("**Judgement.** Law enforcement did not degrade RansomHub; RansomHub was a beneficiary of it. Its rise came from takedowns "
      "of competitors, and its fall came from internal and competitive pressure. Its affiliates simply moved to other "
      "brands. The evidence favours treating RaaS brands as disposable wrappers around a persistent affiliate workforce. "
      "We hold this with moderate confidence. The alternative is that a sealed investigation caused the April 2025 "
      "collapse. We cannot exclude that, but no source supports it, and DragonForce's public claim points to a market "
      "explanation."),
]

S8 = [
    H(2, "8. Risk assessment and recommendations"),
    P("**Risk.** For an organisation with exposed remote access, flat Active Directory and online backups, the risk "
      "from RansomHub-style affiliates is high in likelihood and severe in impact. The brand is gone; its affiliates and playbook now "
      "operate under DragonForce, Qilin and others [6]. Each recommendation is traced to a finding."),
    H(3, "Detection"),
    B("Alert on bursts of failed RDP logons (Event 4625) followed by a successful 4624 type 10 from the same external source. "
      "This would have caught the four-hour spray on day 1 (Section 2) [2]."),
    B("Alert on DCSync (Event 4662 with replication GUIDs) from non-domain-controller hosts, and on LSASS access (Sysmon 10). "
      "The affiliate ran Mimikatz DCSync per child domain on day 1 [2]."),
    B("Alert on Rclone execution, on rclone.conf creation, and on SSH/SFTP sessions on port 443 to non-corporate hosts. "
      "The 2.03 GB theft on day 3 used exactly this [2]."),
    B("Treat new installs of RMM tools (Atera, Splashtop, AnyDesk) as alerts unless they are on an approved list. Two "
      "different RMM tools appeared on backup servers [1][2]."),
    H(3, "Incident response"),
    B("Assume exfiltration before encryption. The encryptor does not steal data, so IR must look for the separate affiliate "
      "tool (Rclone, WinSCP, PuTTY) and quantify what left [1]."),
    B("Hunt for every random six-letter service (Event 7045) and remote copies of the binary over SMB, to scope the spread "
      "[2]. Collect memory early: the rclone configuration in this case was recovered only from memory [2]."),
    B("Build the negotiation plan on the documented tactics. Verify claimed data volumes against your own logs before "
      "responding. Christie's and Frontier showed claims inflated more than tenfold [11][12]. Treat a deadline as a "
      "pressure tactic, not a decryption limit."),
    H(3, "Mitigation"),
    B("Remove internet-facing RDP, or put it behind a VPN with phishing-resistant MFA. This closes the access path in our "
      "case and CISA's password-spray vector [1][2]."),
    B("Patch the edge CVEs CISA lists (Citrix CVE-2023-3519, FortiOS CVE-2023-27997, Confluence CVE-2023-22515, BIG-IP "
      "CVE-2023-46747, ActiveMQ CVE-2023-46604) and keep the Microsoft vulnerable-driver blocklist on to blunt "
      "EDRKillShifter [1][4]."),
    B("Use tiered administration so that a domain-admin credential is not usable on workstations and backup servers. "
      "In our case a single compromised account led to every tier [2]."),
    H(3, "Organisational resilience"),
    B("Keep immutable, offline backups and separate backup credentials from the domain. The affiliate staged its "
      "exfiltration script in the Veeam directory and deleted shadow copies [2]."),
    B("Have leadership decide the payment and legal-notification policy in advance. RansomHub's leverage depends on "
      "regulatory exposure (healthcare re-extortion) and on time pressure (3 to 90 day deadlines) [1][14]."),
    B("Track affiliates, not brands. Assumptions tied to \"RansomHub\" expired on 1 April 2025; "
      "the tradecraft did not [6]."),
]

APPENDIX = [
    {"t": "pagebreak"},
    H(2, "Appendix A. MITRE ATT&CK mapping and indicators of compromise"),
    T(["ATT&CK ID", "Technique", "Evidence (this actor)"], [
        ["T1110.003", "Brute Force: Password Spraying", "RDP spray from 185.190.24.54/.33 [2]; CISA [1]"],
        ["T1133 / T1078", "External Remote Services / Valid Accounts", "RDP logon with sprayed account, elevated token [2]"],
        ["T1003.006", "OS Credential Dumping: DCSync", "Mimikatz lsadump::dcsync per child domain [2]"],
        ["T1003.001", "OS Credential Dumping: LSASS Memory", "Mimikatz sekurlsa; Sysmon 10 [2]"],
        ["T1046", "Network Service Discovery", "Advanced IP Scanner, NetScan (16 ports) [2]; Nmap, AngryIPScanner [1]"],
        ["T1219", "Remote Access Software", "Atera, Splashtop [2]; AnyDesk, ConnectWise, N-able [1]"],
        ["T1021.001", "Remote Services: RDP", "Lateral movement to domain controllers (4624 type 10) [2]"],
        ["T1570 / T1543.003", "Lateral Tool Transfer / Windows Service", "Encryptor copied over SMB, run as random service [2]"],
        ["T1048", "Exfiltration Over Alternative Protocol", "Rclone SFTP to 38.180.245.207:443 [2]; PuTTY/HTTP POST [1]"],
        ["T1562.001", "Impair Defenses: Disable or Modify Tools", "EDRKillShifter (vulnerable driver) [4]; CISA [1]"],
        ["T1490", "Inhibit System Recovery", "vssadmin Delete Shadows /all /quiet; Win32_ShadowCopy removal [2][1]"],
        ["T1070.001", "Clear Windows Event Logs", "wevtutil cl security/system/application [2]"],
        ["T1486", "Data Encrypted for Impact", "Curve25519 + AES/ChaCha20, intermittent encryption [1][3]"],
    ], widths=[0.17, 0.33, 0.5], caption="Table A1. Thirteen techniques mapped from actor-specific reporting.", size=18),
    T(["Type", "Indicator (defanged)", "Context", "Src"], [
        ["IPv4", "185.190.24[.]54", "RDP password-spray source", "[2]"],
        ["IPv4", "185.190.24[.]33", "RDP password-spray source", "[2]"],
        ["IPv4", "164.138.90[.]2", "Interactive RDP initial access", "[2]"],
        ["IPv4:port", "38.180.245[.]207:443", "Rclone SFTP exfiltration destination", "[2]"],
        ["SHA-256", "25117dcb2d852df15fe44c5757147e7038f289e6156b0f6ab86d02c0e97328cb", "amd64.exe (RansomHub encryptor)", "[2]"],
        ["SHA-256", "e14ba0fb92e16bb7db3b1efac4b13aee178542c6994543e7535d8efaa589870c", "netscan.exe (SoftPerfect NetScan)", "[2]"],
        ["SHA-256", "4775dfb24f85f5d776f538018a98cc6a9853a1840f5c00b7d0c54695f03a11d9", "nocmd.vbs (hidden Rclone launcher)", "[2]"],
        ["SHA-256", "ffd09a5c27938d1f7424ed66d1474cfeb3df72daabdf10e09f161ed1ffd21271", "rcl.bat (Rclone job)", "[2]"],
        ["SHA-256", "ec45ebd938e363e36cacb42e968a960fbe4e21ced511f0ea2c0790b743ff3c67", "setup.msi (RMM installer)", "[2]"],
        ["Filename", "How To Restore Your Files.txt", "Ransom note name", "[1]"],
        ["File path", "C:\\Users\\%USERNAME%\\Desktop\\IamBatMan.exe", "Ransomware binary location", "[1]"],
        ["Email", "brahma2023[@]onionmail[.]org", "Email linked to RansomHub", "[1]"],
        ["IPv4", "89.23.96[.]203 / 188.34.188[.]7", "Payload-staging servers (URL paths /333/, /555/)", "[1]"],
        ["File marker", "Footer ending 0x00ABCDEF; random extension", "Encrypted-file trailer (58 bytes)", "[1][5]"],
    ], widths=[0.12, 0.47, 0.33, 0.08], caption="Table A2. Fourteen cited indicators. The IPs are historical and may be "
       "reassigned; use them for retrospective hunting, not blocking alone.", size=16, first_bold=False),
]

REFERENCES = [
    {"t": "pagebreak"},
    H(2, "References"),
    *[{"t": "p", "text": r, "count": False, "size": 19} for r in [
        "[1] CISA, FBI, MS-ISAC and HHS, \"#StopRansomware: RansomHub Ransomware,\" Advisory AA24-242A, 29 Aug. 2024. "
        "https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-242a",
        "[2] The DFIR Report, \"Hide Your RDP: Password Spray Leads to RansomHub Deployment,\" 30 Jun. 2025. "
        "https://thedfirreport.com/2025/06/30/hide-your-rdp-password-spray-leads-to-ransomhub-deployment/",
        "[3] Group-IB, \"RansomHub ransomware-as-a-service,\" 28 Aug. 2024. https://www.group-ib.com/blog/ransomhub-raas/",
        "[4] ESET Research, \"Shifting the sands of RansomHub's EDRKillShifter,\" WeLiveSecurity, 26 Mar. 2025. "
        "https://www.welivesecurity.com/en/eset-research/shifting-sands-ransomhub-edrkillshifter/",
        "[5] Arete, \"Malware Spotlight: RansomHub Ransomware,\" Jan. 2025. "
        "https://areteir.com/resources/malware-spotlight-ransomhub-ransomware",
        "[6] The Hacker News, \"RansomHub Went Dark April 1; Affiliates Fled to Qilin, DragonForce Claimed Control,\" "
        "30 Apr. 2025. https://thehackernews.com/2025/04/ransomhub-went-dark-april-1-affiliates.html",
        "[7] The Hacker News, \"Scattered Spider Adopts RansomHub and Qilin Ransomware\" (reporting Microsoft Threat "
        "Intelligence, 15 Jul. 2024). https://thehackernews.com/2024/07/scattered-spider-adopts-ransomhub-and.html",
        "[8] U.S. Department of Justice, \"United Kingdom National Charged in Connection with Multiple Cyber Attacks, "
        "Including on Critical Infrastructure,\" Sept. 2025. https://www.justice.gov/opa/pr/united-kingdom-national-charged-"
        "connection-multiple-cyber-attacks-including-critical",
        "[9] The Register, \"How cops taking down LockBit, ALPHV led to RansomHub's meteoric rise,\" 28 Dec. 2024. "
        "https://www.theregister.com/2024/12/28/lockbit_alphv_disruptions_ransomhub_rise/",
        "[10] Ransomware.live, negotiation archive (data from V. Marchive's Ransomchats and J. Mousqueton), RansomHub chat. "
        "https://www.ransomware.live/nego/RansomHub/20240810",
        "[11] The Register, \"Christie's avoids leak of stolen data as it's sold instead,\" 4 Jun. 2024, and \"Christie's "
        "clients' data stolen,\" 10 Jun. 2024. https://www.theregister.com/2024/06/04/christies_stolen_data_auctioned_off/",
        "[12] BleepingComputer, \"Frontier warns 750,000 of a data breach after extorted by RansomHub,\" Jun. 2024. "
        "https://www.bleepingcomputer.com/news/security/frontier-warns-750-000-of-a-data-breach-after-extorted-by-ransomhub",
        "[13] The Record, \"Kawasaki Europe says operations restored after cyberattack,\" Sept. 2024. "
        "https://therecord.media/kawasaki-europe-cyberattack-operations-restored ; SC Media, \"RansomHub releases 487GB of "
        "Kawasaki Motors Europe data.\" https://www.scworld.com/news/ransomhub-releases-487gb-of-kawasaki-motors-europe-data",
        "[14] TechCrunch, \"RansomHub ... Change Healthcare stolen patient data,\" 15 Apr. 2024. "
        "https://techcrunch.com/2024/04/15/change-healthcare-stolen-patient-data-ransomhub-leak/",
        "[15] BleepingComputer, \"Halliburton says ransomware attack led to $35 million in losses,\" Oct. 2024. "
        "https://www.bleepingcomputer.com/news/security/halliburton-says-ransomware-attack-led-to-35-million-in-losses/",
        "[16] Bitsight, \"Guide to RansomHub Ransomware (2025).\" https://www.bitsight.com/blog/guide-to-ransomhub-ransomware-2025",
        "[17] Rapid7, \"Q2 2025 Ransomware Trends Analysis: Boom and Bust.\" "
        "https://www.rapid7.com/blog/post/q2-2025-ransomware-trends-analysis-boom-and-bust/",
        "[18] Dark Reading, \"After LockBit, ALPHV Takedowns, RaaS Startups Go on a Recruiting Drive,\" Mar. 2024. "
        "https://www.darkreading.com/threat-intelligence/after-lockbit-alphv-takedowns-raas-recruiting-drive",
    ]],
]

CLOSING = [
    {"t": "pagebreak"},
    H(2, "Contribution statement"),
    P("[Member 1] — [what they researched, wrote and presented; e.g. Sections 1–3, Diamond Model and kill chain; presented "
      "the adversary-profile segment].", count=False),
    P("[Member 2] — [e.g. Sections 4–6, infrastructure, victimology and negotiation analysis; presented the victims and "
      "negotiation segment].", count=False),
    P("[Member 3] — [e.g. Sections 7–8, law enforcement and recommendations, IOC/ATT&CK appendix; presented the law "
      "enforcement and recommendations segment].", count=False),
    H(2, "Generative AI use"),
    P("[Required by the brief: state specifically what any generative AI tool was used for. For example: \"A generative AI "
      "assistant (Claude) was used to locate and summarise candidate sources, check ATT&CK technique IDs, and draft "
      "report text, which the group then reviewed, verified against the cited sources and edited.\" Replace this with an "
      "accurate description of your group's actual use.]", count=False),
]

BODY = FRONT + S1 + S2 + S3 + S4 + S5 + S6 + S7 + S8
