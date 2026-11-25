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

from tables import S1_1, S1_2, S2_1  # noqa: E402

FRONT = [
    {"t": "p", "text": "CIS*6530 Cyber Threat Intelligence and Adversarial Risk Analysis · Assignment 4", "size": 20},
    H(1, TITLE),
    P("**Group members (name, student number):** [Member 1] · [Member 2] · [Member 3]", count=False),
    P("**Word count: {WC}** (report body; excludes tables, the IOC and ATT&CK appendix tables, references, "
      "the contribution statement and the AI-use note)", count=False),
    {"t": "note", "text": "**Bottom line.** RansomHub was the busiest ransomware-as-a-service (RaaS) brand of 2024. It ran on "
     "code bought from the Knight gang and on affiliates left stranded when police disrupted LockBit and ALPHV, and on "
     "1 April 2025 it vanished without any law-enforcement action against its operators. The intrusion we model took "
     "about 118 hours to get from an exposed RDP server to encryption across the domain, and those hours are where "
     "defenders have their chances.", "count": C},
]

S1 = [
    H(2, "1. Adversary profile: Diamond Model of one incident"),
    P("Our Diamond Model covers a single intrusion, documented by The DFIR Report from the victim's own telemetry [2]. "
      "In November 2024 an affiliate sprayed passwords at an internet-facing Remote Desktop Protocol (RDP) server and, "
      "six days later, ran the RansomHub encryptor across the domain. We picked this case because no other public "
      "RansomHub intrusion is as complete: every stage appears in the logs, the tools were recovered and hashed, and the "
      "volume of stolen data was measured."),
    S1_1,
    S1_2,
    P("Two things are missing from the diamond. We do not know who the affiliate was, and under RaaS it was the "
      "affiliate, not the brand, that picked this victim. Nor can we see the ransom negotiation, so the Result feature "
      "ends at encryption."),
]

S2 = [
    H(2, "2. Attack lifecycle (Lockheed Martin Cyber Kill Chain)"),
    S2_1,
    P("Five of the seven stages can be read straight from the victim's logs. The intruder came back on several days, "
      "reran scanners and installed two different remote-management tools, and each of those visits gave defenders a "
      "chance to act before impact. The two stages we cannot evidence happen away from the victim's network: choosing "
      "the target and making the demand."),
]

S3 = [
    H(2, "3. Malware behaviour, TTPs and indicators"),
    P("RansomHub's encryptor reuses code from Knight, a rival whose source code went up for sale in February 2024 [4], "
      "and CISA lists Cyclops and Knight as its earlier names [1]. Group-IB describes a locker written in Go, with builds "
      "for Windows, Linux and ESXi [3], while Arete also reports C++ components [5]. The vendors agree on the platforms "
      "but not on the language."),
    P("Each victim gets its own Curve25519 key pair [1], and Group-IB reports that files are encrypted with AES-256, "
      "ChaCha20 or XChaCha20, depending on what the hardware supports [3]. Files under 0x100000 bytes are encrypted whole. "
      "Larger ones are processed in 0x100000-byte chunks with 0x200000 bytes skipped in between, which is "
      "much faster. Every file gets a 58-byte footer ending in 0x00ABCDEF [1]. "
      "The extension is random; Arete ties it to the first six characters of the public key [5]. The ransom note, usually "
      "\"How To Restore Your Files.txt\", names no price. It gives a client ID, a link to a private .onion chat and a "
      "deadline of 3 to 90 days chosen by the affiliate [1]."),
    P("The binary refuses to run without a -pass value. In our case the affiliate launched it as amd64.exe -pass "
      "[redacted], and it copied itself to other hosts over SMB, with the -only-local flag stopping those copies from "
      "spreading again [2]. Before encrypting it shut down Hyper-V virtual machines, deleted shadow copies through vssadmin "
      "and Win32_ShadowCopy, loosened symlink evaluation and wiped the Security, System and Application logs [2]. CISA "
      "lists about 30 processes, among them SQL, Oracle and Outlook, that it kills first [1]."),
    P("Data theft is left to the affiliate, because the encryptor has no exfiltration code [1]. Here the affiliate used "
      "Rclone, started by a hidden VBScript (nocmd.vbs) through a batch file (rcl.bat). An include-list of document, mail "
      "and image extensions (*.pst, *.msg, *.edb, *.pdf, *.xlsx and others) kept the haul to 2.03 GB of the files most "
      "useful for extortion [2]."),
    P("The operators also wrote their own EDR killer, EDRKillShifter, and from May 2024 offered it to affiliates through "
      "the panel [4]. It loads a vulnerable driver and uses it to terminate security products, behaviour CISA maps to "
      "T1562.001 [1]. See Appendix A (Tables A1 and A2) for the full mapping and indicators."),
]

S4 = [
    H(2, "4. Infrastructure and RaaS structure"),
    P("RansomHub kept development and deployment apart. The operators supplied the locker builds, EDRKillShifter, a "
      "panel for managing targets and chat rooms, and a Tor leak site, with a separate onion domain for each panel [3]. "
      "Affiliates paid for access and carried out the intrusions. What drew them in was the money: they kept 90% of each "
      "payment, received it into their own wallets and passed the operators' 10% on afterwards [3][4]. ALPHV had just "
      "kept a $22 million payment that belonged to one of its own affiliates, so holding the wallet removed the biggest "
      "risk of signing up with a RaaS brand [9][14]. From 21 June 2024 new affiliates also had to put down a US$5,000 "
      "deposit [4]."),
    P("The house rules banned attacks on the Commonwealth of Independent States (CIS), Cuba, North Korea and China, and on "
      "any victim who had already paid. Non-profit hospitals could not be encrypted, although their data could still be "
      "held to ransom [3]. An affiliate who broke a promise made after payment was banned [3]. The rules protect "
      "the brand's reputation, on which its income depends."),
    P("Network infrastructure is rarely reused, while tools are reused constantly. CISA's list of IP addresses is mostly "
      "historical and largely linked to QakBot [1], and the addresses in our case appear in no other public RansomHub "
      "report we found. What recurs from one intrusion to the next is commodity tooling: Mimikatz, Rclone, AnyDesk and "
      "other RMM products, and network scanners [1][2]. ESET followed one affiliate, which it calls \"QuadSwitcher\", "
      "working for RansomHub, Play, Medusa and BianLian, and assessed with high confidence that the same actor carried "
      "out all of those attacks [4]. The infrastructure that matters belongs to affiliates like this one, and it moves "
      "with them from brand to brand."),
]

S5 = [
    H(2, "5. Victim and industry-targeting analysis"),
    P("By August 2024 the FBI had counted at least 210 RansomHub victims in 11 critical-infrastructure sectors, including "
      "healthcare, water and critical manufacturing [1]. Bitsight puts manufacturing first, ahead of healthcare and professional services [16], and "
      "Group-IB lists the United States, United Kingdom, Spain, France and Italy as the countries hit hardest [3]. The "
      "public cases fit that spread: Christie's (auctions, May 2024) [11], Frontier Communications (telecoms, April 2024) "
      "[12], Kawasaki Motors Europe (manufacturing, September 2024) [13], the second extortion of Change Healthcare "
      "(healthcare, April 2024) [14] and Halliburton (energy services, August 2024), although Halliburton has never "
      "confirmed that RansomHub was responsible [15]."),
    P("Three features of how RansomHub worked explain this breadth better than any preference for a sector. Access was "
      "opportunistic: exposed RDP in our case, and in CISA's reporting a list of edge-device CVEs in Citrix, FortiOS, "
      "Confluence, BIG-IP and ActiveMQ [1]. Any organisation with an exposed perimeter could become a victim. Targets were "
      "also chosen by many independent affiliates, which spreads the victim list further. Where the rules do show a "
      "preference, it is for leverage, since permitting data-only extortion of hospitals and re-extorting Change "
      "Healthcare both point to sectors in which a leak brings regulators and patient-safety concerns [3][14]. "
      "Manufacturing probably leads because downtime there is so costly. We assess with moderate confidence that exposure "
      "and leverage drove RansomHub's victimology and that sector choice played little part. Geography is the one firm "
      "exclusion, and the CIS ban fits a Russian-speaking operator base."),
]

S6 = [
    H(2, "6. Ransom negotiation analysis"),
    P("Little public negotiation data exists for RansomHub, and the reason lies in how it negotiated. The largest public "
      "archive of ransomware chats holds 295 conversations from 31 groups, only one of them RansomHub's [10]. That one is "
      "a single templated message with no amount, no deadline and no reply from the victim [10]. Every note pointed to a "
      "private onion chat [1], each affiliate panel had its own onion domain [3], and the affiliate rather than the "
      "operators ran the conversation and took the payment [3]. RansomHub therefore never had the shared negotiation "
      "portals that researchers have scraped for other groups, and its internal chats have not leaked the way LockBit's "
      "and Black Basta's did."),
    P("Incident-response data fills part of the gap. In Arete's 2024 RansomHub cases the median opening demand was "
      "US$900,000 and the median payment US$350,000 [5]. Victims who paid usually settled at about 39% of the first "
      "figure, which suggests the demands were anchored deliberately high."),
    P("The public cases show how pressure was applied, though they lean towards victims who refused to pay, since those "
      "are the ones that become public:"),
    B("Countdown deadlines. Kawasaki Motors Europe was given a timer that ran out on 14 September 2024, after which "
      "RansomHub published 487 GB that it said was the stolen data [13]. Frontier was given nine days [12]."),
    B("Inflated claims. RansomHub said it held data on at least 500,000 Christie's clients, and Christie's notified "
      "45,798 [11]. It claimed more than 2 million Frontier customers, and Frontier notified 751,895 [12]. Overstating the "
      "haul makes refusal look more expensive."),
    B("A claimed sale. When Christie's stopped responding, RansomHub announced that the data had been sold, which analysts "
      "quoted by The Register suspected was face-saving rather than a real sale [11]."),
    B("Re-extortion. RansomHub listed Change Healthcare, which had reportedly already paid ALPHV about US$22 million, and "
      "threatened to sell 4 TB unless it paid again [14]. Its rule against re-attacking paying victims evidently covered "
      "only its own."),
    B("Reassurance. The note offers to decrypt files under 1 MB free as proof [4], and affiliates who did not honour a "
      "paid deal were banned [3]."),
    P("We found no public source that confirms a RansomHub payment by a named victim. Halliburton disclosed US$35 million "
      "in costs without saying whether any of it went on a ransom [15]. Paid outcomes are therefore visible only in "
      "aggregate, through the Arete medians, while refusals can be followed case by case."),
]

S7 = [
    H(2, "7. Law-enforcement and disruption actions"),
    P("We found no arrest, indictment, sanction or seizure aimed at RansomHub's core operators in DOJ or vendor reporting "
      "up to November 2026. Every action that affected it was indirect."),
    P("**Action 1: the ALPHV disruption (December 2023) and Operation Cronos against LockBit (February 2024).** Both "
      "operations targeted other groups, yet they shaped RansomHub more than anything that came later. It launched on "
      "the RAMP forum on 2 February 2024 [4], between the two, and recruited the displaced ALPHV and LockBit affiliates by "
      "letting them hold their own wallets [9][18]. *Before:* RansomHub did not exist. *After:* within six months it had "
      "at least 210 victims [1], a rise The Register attributes to the two takedowns [9]."),
    P("**Action 2: the #StopRansomware joint advisory AA24-242A (29 August 2024).** The FBI, CISA, MS-ISAC and HHS "
      "published RansomHub's techniques, the CVEs it exploited, file paths, IP addresses and an email address [1]. "
      "*Before:* defenders depended on vendor reporting. *After:* the indicators could be deployed widely, yet the "
      "tradecraft stayed the same, and our November 2024 case followed the advisory's description closely [2][4]. An "
      "advisory makes defence cheaper but does nothing to the operators."),
    P("**Action 3: charges against Scattered Spider (Octo Tempest), a documented RansomHub affiliate.** Microsoft reported "
      "that Octo Tempest added RansomHub to its payloads in the second quarter of 2024 [7]. In September 2025 the US "
      "Department of Justice unsealed a complaint against Thalha Jubair, a UK national, covering at least 120 intrusions "
      "linked to the group and more than US$115 million in ransom payments, alongside charges in the UK [8]. *Before:* "
      "the affiliate was deploying RansomHub in 2024. *After:* RansomHub had already gone dark, so the charges took "
      "affiliate capacity out of the wider ecosystem, not out of RansomHub."),
    P("**The 1 April 2025 collapse.** In March RansomHub's leak site was defaced with \"R.I.P. 3/3/25\", and on 1 April "
      "2025 its infrastructure went offline [6][17]. No agency claimed responsibility. DragonForce announced that "
      "RansomHub had \"moved\" to its new cartel infrastructure, and researchers reported affiliates moving to Qilin and "
      "former RansomHub affiliates setting up new brands such as VanHelsing [6]. The pattern is a business failure "
      "followed by fragmentation."),
    P("**Judgement.** RansomHub gained more from law enforcement than it lost. Takedowns of its competitors produced its "
      "rise, internal and competitive pressure produced its fall, and its affiliates carried on under other names. The "
      "evidence supports treating RaaS brands as disposable wrappers around a persistent workforce of affiliates, a view "
      "we hold with moderate confidence. The alternative is that a sealed investigation brought about the April 2025 "
      "collapse. We cannot rule that out, but no source supports it, and DragonForce's public claim points to a market "
      "explanation."),
]

S8 = [
    H(2, "8. Risk assessment and recommendations"),
    P("For an organisation with exposed remote access, a flat Active Directory and backups reachable from the domain, an "
      "attack by RansomHub-style affiliates is both likely and severe. The brand is gone, but its affiliates and their "
      "playbook now work under DragonForce, Qilin and others [6]. Each recommendation below traces back to a finding in "
      "this report."),
    H(3, "Detection"),
    B("Alert on a burst of failed RDP logons (Event 4625) followed by a successful type 10 logon (4624) from the same "
      "external source, which would have caught the four-hour spray on day 1 (Section 2) [2]."),
    B("Alert on DCSync (Event 4662 with replication GUIDs) from hosts that are not domain controllers, and on LSASS access "
      "(Sysmon 10); the affiliate ran Mimikatz DCSync against each child domain on day 1 [2]."),
    B("Alert on Rclone execution, on creation of rclone.conf, and on SSH or SFTP sessions on port 443 to non-corporate "
      "hosts, the exact pattern of the 2.03 GB theft on day 3 [2]."),
    B("Treat any new install of an RMM tool (Atera, Splashtop, AnyDesk) as an alert unless it is on an approved list. Two "
      "different RMM tools appeared on the backup servers in our case [1][2]."),
    H(3, "Incident response"),
    B("Assume data left before encryption. The encryptor steals nothing, so responders need to find the affiliate's "
      "separate tool (Rclone, WinSCP or PuTTY) and measure what was taken [1]."),
    B("Hunt for every randomly named six-letter service (Event 7045) and every remote copy of the binary over SMB to scope "
      "the spread [2], and capture memory early, because the Rclone configuration in this case survived only there [2]."),
    B("Base the negotiation plan on the documented tactics. Check claimed data volumes against your own logs before "
      "replying, since the Christie's and Frontier claims were inflated more than tenfold [11][12], and treat a deadline as "
      "a pressure tactic, not a decryption limit."),
    H(3, "Mitigation"),
    B("Take RDP off the internet or put it behind a VPN with phishing-resistant MFA, which closes both the access path in "
      "our case and CISA's password-spray vector [1][2]."),
    B("Patch the edge CVEs CISA lists (Citrix CVE-2023-3519, FortiOS CVE-2023-27997, Confluence CVE-2023-22515, BIG-IP "
      "CVE-2023-46747, ActiveMQ CVE-2023-46604) and keep Microsoft's vulnerable-driver blocklist enabled against "
      "EDRKillShifter [1][4]."),
    B("Use tiered administration so that a domain-admin credential cannot be used on workstations or backup servers; in "
      "our case one compromised account reached every tier [2]."),
    H(3, "Organisational resilience"),
    B("Keep immutable offline backups, with backup credentials kept out of the domain. The affiliate staged its "
      "exfiltration script in the Veeam directory and deleted the shadow copies [2]."),
    B("Have leadership settle the payment and legal-notification policy in advance, because RansomHub's leverage came "
      "from regulatory exposure (the healthcare re-extortion) and from time pressure (3 to 90 day deadlines) [1][14]."),
    B("Track affiliates, not brands. Assumptions tied to \"RansomHub\" expired on 1 April 2025, but the tradecraft did "
      "not [6]."),
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
    P("[Member 1]: [what they researched, wrote and presented; e.g. Sections 1 to 3, Diamond Model and kill chain; presented "
      "the adversary-profile segment].", count=False),
    P("[Member 2]: [e.g. Sections 4 to 6, infrastructure, victimology and negotiation analysis; presented the victims and "
      "negotiation segment].", count=False),
    P("[Member 3]: [e.g. Sections 7 and 8, law enforcement and recommendations, IOC/ATT&CK appendix; presented the law "
      "enforcement and recommendations segment].", count=False),
    H(2, "Generative AI use"),
    P("[Required by the brief: state specifically what any generative AI tool was used for. For example: \"A generative AI "
      "assistant (Claude) was used to locate and summarise candidate sources, check ATT&CK technique IDs, and draft "
      "report text, which the group then reviewed, verified against the cited sources and edited.\" Replace this with an "
      "accurate description of your group's actual use.]", count=False),
]

BODY = FRONT + S1 + S2 + S3 + S4 + S5 + S6 + S7 + S8
