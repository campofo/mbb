"""Assignment 3 content: Threat Actor Intelligence Profile, Option B (ShinyHunters).

count=True marks Parts A-D prose, the scope of the 2,000-2,800 word limit
(the executive brief, sources, and Diamond/kill-chain tables are excluded).
"""

C = True


def P(text, count=C):
    return {"t": "p", "text": text, "count": count}


def B(text, count=C, size=None):
    d = {"t": "bullet", "text": text, "count": count}
    if size:
        d["size"] = size
    return d


def H(level, text):
    return {"t": f"h{level}", "text": text}


def T(header, rows, widths=None, caption=None, size=19, first_bold=True):
    return {"t": "table", "header": header, "rows": rows, "widths": widths, "caption": caption,
            "size": size, "firstColBold": first_bold, "firstColShade": first_bold}


TITLE = "ShinyHunters: Threat Actor Intelligence Profile"

FRONT = [
    {"t": "p", "text": "CIS*6530 Cyber Threat Intelligence and Adversarial Risk Analysis · Assignment 3 · Option B", "size": 20},
    H(1, TITLE),
    P("**Name:** [your name]    **Student number:** [your student number]", count=False),
    P("Intelligence cut-off: 25 November 2026. Sources are cited as [n] and listed in Part F.", count=False),
]

PART_A = [
    H(2, "Part A. Intelligence profile"),
    P("**Word count (Parts A–D): {WC}** (excluding the executive brief, sources and the Diamond/kill-chain tables)", count=False),
    H(3, "A1. Identity, motivations and objectives"),
    P("\"ShinyHunters\" is best treated as a brand: a handle and leak identity used since 2020 by a changing set of "
      "mostly young, English- and French-speaking individuals, not a stable organisation. The prosecutions show the "
      "turnover. The group's 2020–21 era produced charges against three French nationals, including Sebastien Raoult. "
      "Raoult built phishing pages for the group and was sentenced in Seattle in January 2024 to three years and more "
      "than US$5 million in restitution [4]. The 2024 Snowflake campaign was charged against a Canadian (Connor "
      "Moucka) and a US citizen living in Turkey (John Binns) [5]. In June 2025 French police arrested four people, "
      "one using the handle \"ShinyHunters\" itself [10]. In September–October 2026, Dutch, Jordanian and US arrests followed "
      "[12][13]. Vendors are careful on this point. Google's Threat Intelligence Group (GTIG) tracks the 2025 Salesforce "
      "intrusions as UNC6040 and the extortion as UNC6240. It says only that UNC6240 \"consistently claimed\" to be "
      "ShinyHunters, likely to raise pressure on victims [2]. Mandiant's report on the Snowflake actor UNC5537 never uses the "
      "name, though one of the hackers described himself to Wired as a member [1][8]. The brand claim is therefore "
      "well-supported for 2020–21 and 2025–26, contested for the 2024 Snowflake campaign, and in every period "
      "consistent with shifting membership."),
    P("The motivation is money, obtained by stealing data in bulk and then extorting the owner or selling the data. "
      "The evidence is specific to this actor: forum sale listings for Ticketmaster and Santander data [17]; AT&T's "
      "reported US$370,000 payment for deletion [8]; 72-hour bitcoin demands in the Salesforce campaign [2]; and the "
      "FBI's 2026 estimate of at least US$70 million in extortion payments from more than 140 organisations [12]. Unlike "
      "the espionage actors covered in this course, ShinyHunters wants the victim to know about the theft, because "
      "the victim's fear of disclosure is the product being sold. The group's 2026 claim that its FBI intrusion was "
      "\"not financially motivated\" [12] is better read as reputation-building than as a change of objective (Part D, "
      "judgement 2)."),
    P("The business model uses three channels, often on the same dataset. The first is **private extortion**: email or "
      "phone demands to staff with 72-hour bitcoin deadlines [2], sometimes through a hired intermediary, as with AT&T "
      "[8]. The second is **resale**: listings on BreachForums, where Moucka alone made at least US$495,000 [6], and where "
      "Santander and Ticketmaster data were advertised in 2024 [17]. The third is **public shaming**: from late 2025 a "
      "leak portal listed 39 Salesforce-customer victims, including Qantas, Toyota and FedEx [11], and in 2026 targets "
      "appeared on the leak site 1 to 28 days after their phishing domains were registered [14]. The order matters. Private "
      "extortion comes first because a paid, unpublished breach is worth most to both sides, and resale is the fallback once "
      "the victim refuses. The data also loses value with age and with each disclosure, so the group works fast. That is "
      "the opposite of an espionage actor, which keeps access quietly for as long as possible and never wants the victim to "
      "know."),
    H(3, "A2. Capabilities, tools and TTPs"),
    P("ShinyHunters does not deploy ransomware and rarely uses custom malware. Its capability is access to data platforms "
      "through stolen identities, followed by bulk export. Three generations of tradecraft are documented:"),
    B("**2020–21: phishing and repository mining.** Spoofed login pages harvested employee credentials, and private code "
      "repositories were searched for cloud keys [4]."),
    B("**2024: infostealer credentials against Snowflake (UNC5537).** The actors used credentials that infostealers (VIDAR, "
      "RedLine, Lumma and others) had harvested, some as far back as 2020. They logged into customer Snowflake accounts that "
      "had no MFA and no network allow-lists [1]. A recon utility the actors named \"rapeflake\" (FROSTBITE) and DBeaver "
      "Ultimate enumerated tables. Data was staged with CREATE TEMPORARY STAGE and COPY INTO (gzip) and pulled with GET [1]."),
    B("**2025–26: vishing and SaaS token abuse.** Callers posing as IT support talked staff into authorising a modified "
      "Salesforce Data Loader connected app (sometimes named \"My Ticket Portal\") and harvested Okta credentials and MFA codes [2]. "
      "The cluster UNC6395 stole OAuth tokens from the Salesloft Drift integration and ran SOQL exports across Salesforce "
      "tenants, then searched them for AWS keys and Snowflake tokens to reuse [3]. Okta has tracked a ShinyHunters-linked "
      "vishing cluster using legal-themed lure domains in 2026 [14]."),
    T(["ATT&CK ID", "Technique", "Actor-specific evidence"], [
        ["T1078.004", "Valid Accounts: Cloud Accounts", "Infostealer credentials used on Snowflake tenants [1]"],
        ["T1566.004", "Phishing: Spearphishing Voice", "IT-support calls leading to connected-app approval [2]"],
        ["T1528", "Steal Application Access Token", "Salesloft Drift OAuth tokens abused (UNC6395) [3]"],
        ["T1550.001", "Use Alternate Authentication Material: App Access Token", "Stolen Drift tokens used to query Salesforce [3]"],
        ["T1213", "Data from Information Repositories", "SQL/SOQL bulk queries against Snowflake and Salesforce [1][3]"],
        ["T1074.002", "Data Staged: Remote Data Staging", "CREATE TEMPORARY STAGE + COPY INTO in the victim tenant [1]"],
        ["T1560.001", "Archive Collected Data: Archive via Utility", "COPY INTO ... COMPRESSION=GZIP [1]"],
        ["T1552.001", "Unsecured Credentials: Credentials in Files", "Exported records searched for AKIA keys and Snowflake tokens [3]"],
        ["T1090.003", "Proxy: Multi-hop Proxy", "Mullvad/PIA VPN and Tor exit nodes for access and exfiltration [1][2][3]"],
        ["T1657", "Financial Theft (extortion)", "Bitcoin demands, 72-hour deadlines; AT&T payment [2][8]"],
    ], widths=[0.15, 0.38, 0.47], caption="Table 1. Ten techniques, each tied to reporting on this actor.", size=18),
    H(3, "A3. Infrastructure and targeting/victimology"),
    P("ShinyHunters' infrastructure is mostly rented or borrowed. Access ran through commercial VPNs (Mullvad, Private "
      "Internet Access) and Tor. Bulk exfiltration went to VPSs at ALEXHOST (AS200019, Moldova). Stolen data was "
      "stored on MEGA [1][2]. The Drift campaign added DigitalOcean and AWS hosts and distinctive user-agents such as "
      "\"Salesforce-Multi-Org-Fetcher/1.0\" [3]. Extortion used Tuta mail addresses (shinycorp@tuta[.]com, "
      "shinygroup@tuta[.]com) [2], Telegram channels, and successive BreachForums domains and leak sites. Those forums "
      "were the group's sales channel and, from 2025, its leak site, until their seizure in October 2025 [11]."),
    P("The victimology follows the platform, not the sector. In 2020 the victims were consumer platforms such as Tokopedia "
      "[16]. In 2024 they were Snowflake customers in telecoms, ticketing, banking and retail; Mandiant notified about 165 "
      "organisations [1]. In 2025 they were Salesforce tenants in aviation (Qantas), insurance (Allianz Life) and luxury "
      "retail (LVMH brands), plus Google's own corporate instance [2][15]. This raises the guide's question about who "
      "the victim is. In every wave the platform itself was not breached. Snowflake and Salesforce both say so, and Mandiant "
      "found no compromise of Snowflake's enterprise environment [1][11]. The data belonged to the customers, and the "
      "harm fell on their own customers, such as AT&T subscribers. We treat the customer organisation as the victim in "
      "the Diamond sense, and the platform as the shared attack surface whose default settings (MFA optional, broad API "
      "access, long-lived tokens) made a single technique scale to hundreds of victims."),
    H(3, "A4. Historical activity and relationships"),
    T(["Date", "Event"], [
        ["May 2020", "Tokopedia and other databases sold; claimed Microsoft GitHub theft [16]"],
        ["2021–22", "Raoult and two other French nationals indicted (W.D. Wash.); Raoult arrested in Morocco [4]"],
        ["Apr–Jun 2024", "Snowflake campaign (UNC5537): AT&T, Ticketmaster, Santander; data sold on BreachForums [1][9][17]"],
        ["Oct–Nov 2024", "Moucka arrested in Canada; Moucka and Binns indicted [5]"],
        ["Mid-2025", "Salesforce vishing (UNC6040/UNC6240); June arrests in France [2][10]"],
        ["Aug 2025", "Drift OAuth theft (UNC6395); \"Scattered LAPSUS$ Hunters\" alliance announced [3][11]"],
        ["Oct 2025", "BreachForums extortion portal seized by the FBI and French authorities [11]"],
        ["Sep–Oct 2026", "FBIjobs.gov breach claim; arrests in the Netherlands, Jordan and the US [12][13][19]"],
        ["Nov 2026", "Leak-site posts claim a return; Okta links a vishing cluster to the new \"INCEPTION\" site [14]"],
    ], widths=[0.18, 0.82], caption="Table 2. Timeline of significant activity.", size=18),
    P("The most important relationship is with \"The Com\", the loose English-speaking online ecosystem that also produced "
      "Scattered Spider and LAPSUS$. GTIG judges that the overlap between UNC6040 and Com actors more plausibly reflects "
      "shared communities than a direct operational relationship [2]. In August 2025 the brands openly merged their "
      "messaging as \"Scattered LAPSUS$ Hunters\" [11]. A merger announced "
      "on Telegram is a claim, not evidence of shared command. Ties to established e-crime are visible but loose. The "
      "Snowflake actors are linked to the Com rather than to Russian-speaking ransomware [5]. In 2026 ShinyHunters reportedly "
      "hijacked the Cl0p leak site [19], which is rivalry rather than an affiliate relationship. The structure the evidence supports "
      "is a network of individuals who share a brand, forums and techniques, recombining from campaign to campaign."),
]

PART_B = [
    H(2, "Part B. Representative incident: the AT&T Snowflake theft (April 2024)"),
    P("We model one victim. Between 14 and 25 April 2024, attackers exfiltrated call and text metadata for nearly all "
      "AT&T wireless customers (more than 100 million people, covering May–October 2022) from AT&T's Snowflake workspace "
      "[9]. It is the best-documented ShinyHunters-associated incident. It has an SEC filing, a federal indictment, a "
      "guilty plea and a traced ransom payment [5][6][8][9]."),
    T(["Feature", "AT&T incident", "Confidence / gaps"], [
        ["Adversary", "Connor Moucka (\"Judische\", \"Waifu\") and John Binns (\"IRDev\") [5][7]; US soldier Cameron "
         "Wagenius (\"Kiberphant0m\") later pleaded guilty to extorting AT&T [7]. Mandiant cluster UNC5537 [1]. "
         "Self-described to Wired as ShinyHunters [8].",
         "High for the individuals (plea). Low for the ShinyHunters label."],
        ["Capability", "Infostealer-harvested Snowflake credentials; no MFA on the account; Snowflake UI/SnowSQL, FROSTBITE and "
         "DBeaver for recon; staged COPY INTO + GET bulk export [1][6].",
         "Tooling is campaign-level [1]; AT&T-specific tool use is not public."],
        ["Infrastructure", "Mullvad/PIA VPN for access; ALEXHOST VPS for exfiltration; MEGA storage [1]; bitcoin wallet "
         "for the 5.7 BTC payment and an intermediary (\"Reddington\") for negotiation [8].",
         "Campaign-level infrastructure; AT&T-specific IPs not public."],
        ["Victim", "AT&T: Snowflake-hosted workspace of call/text records (numbers, counts, durations, some cell-site IDs) "
         "[9]. Indirect victims: more than 100 million subscribers.", "High (SEC 8-K)."],
    ], widths=[0.15, 0.6, 0.25], caption="Table 3. Diamond Model core features.", size=18),
    T(["Meta-feature", "AT&T incident"], [
        ["Timestamp", "Exfiltration 14–25 Apr 2024; AT&T aware 19 Apr; payment May 2024; disclosed 12 Jul 2024 [8][9]"],
        ["Phase", "Initial access, collection, exfiltration, extortion (Table 4)"],
        ["Result", "Data stolen; about US$370,000 (5.7 BTC) paid for deletion, a reduction from a US$1 million demand; "
         "deletion video supplied [8]"],
        ["Direction", "Adversary → AT&T SaaS tenant (no on-premises access); data → attacker VPS → MEGA"],
        ["Methodology", "Credential reuse against an under-configured SaaS tenant; extortion through a third party"],
        ["Resources", "Infostealer log markets, commercial VPNs, cheap VPSs, cryptocurrency"],
    ], widths=[0.2, 0.8], caption="Table 3b. Meta-features (six of six).", size=18),
    T(["Kill-chain stage", "Evidence for the AT&T case", "Status"], [
        ["Reconnaissance", "Credentials obtained from infostealer logs; campaign-wide, 79.7% of accounts used had prior exposure [1]",
         "Campaign-level; the source of AT&T's credential is not public"],
        ["Weaponisation", "No malware built; FROSTBITE/DBeaver prepared for Snowflake queries [1]", "Not evidenced for AT&T"],
        ["Delivery", "Logon to AT&T's Snowflake workspace with stolen credentials [9][6]", "Evidenced"],
        ["Exploitation", "No vulnerability; access possible because MFA was not enforced [6]", "Evidenced (configuration)"],
        ["Installation", "None: a SaaS session needs no persistence", "Not applicable"],
        ["Command and control", "Interactive sessions over VPN [1]", "Campaign-level"],
        ["Actions on objectives", "Bulk export 14–25 Apr; extortion via intermediary; 5.7 BTC paid; claimed deletion [8][9]",
         "Evidenced"],
    ], widths=[0.2, 0.55, 0.25], caption="Table 4. Kill-chain mapping, with gaps stated.", size=18),
    P("The extortion phase is unusually well documented. AT&T first learned of the theft on 19 April 2024, when the actor "
      "claimed it, while exfiltration was still under way [9]. Negotiation ran through a security researcher whom the hacker "
      "had enlisted, and AT&T paid him a fee as well. The opening demand of US$1 million fell to about US$370,000, paid in "
      "May as 5.7 BTC, which TRM Labs traced on-chain. A video of the data being deleted was supplied in return [8]. Two later "
      "facts limit what that payment bought. The intermediary warned that fragments of the data might remain, and the DOJ "
      "says Moucka re-extorted at least one victim [7][8]. Wagenius, a serving US soldier, later pleaded guilty to extorting "
      "AT&T over the same data [7]. For AT&T, the incident was not over when the money was paid."),
    P("The kill chain shows that the model fits poorly. Three stages (weaponisation, installation and C2) barely apply "
      "to a SaaS intrusion with no malware. All the attacker's effort sits at either end: buying or harvesting a credential, "
      "then extorting. The middle of the chain, where endpoint security looks, is empty. Defence therefore has to sit at "
      "the identity layer and in the platform's own query logs."),
]

PART_C = [
    H(2, "Part C. Law-enforcement and disruption actions"),
    P("**Action 1: prosecution of Sebastien Raoult (arrested 2022, sentenced January 2024).** The action removed one "
      "operator of the 2020–21 phishing infrastructure and imposed restitution [4]. *Afterwards*, the brand did not pause. "
      "Within months of the sentence, data from the Snowflake campaign was being sold under the ShinyHunters name [17]. "
      "What was disrupted was one person and one generation's tooling. The name, its forum presence and its reputation "
      "were untouched."),
    P("**Action 2: the Snowflake arrests and charges (October 2024 – August 2026).** Moucka was arrested in Canada on "
      "30 October 2024, and Binns was detained in Turkey. Both were indicted for extorting at least ten organisations of "
      "about US$2.5 million [5]. Moucka pleaded guilty in August 2026 [6]. *Afterwards*, the Snowflake extortion wave ended, "
      "as victims enforced the MFA and allow-lists whose absence it depended on [1]. Within months, however, "
      "the brand's activity moved to Salesforce vishing (UNC6040) [2]. Binns has reportedly been released and obtained "
      "Turkish citizenship, which bars extradition; this rests on unnamed sources [7]. The result was that the people "
      "and the technique were disrupted, but the business continued with a new technique."),
    P("**Action 3: the French arrests (June 2025) and the BreachForums seizure (October 2025).** French police arrested "
      "four suspected BreachForums/ShinyHunters figures [10]; a new BreachForums was announced within a week [18]. "
      "In October 2025 the FBI and French authorities seized the "
      "BreachForums domain then serving as the Salesforce extortion portal [11]. *Afterwards*, activity accelerated "
      "rather than slowed. The Salesforce campaign hit Qantas, Allianz Life and LVMH brands in July 2025, and the Drift "
      "token theft followed in August [3][15]. The group said the seizure had \"no impact\" and continued leaking from "
      "other channels [11]. Arrests that hit the forum layer did not reach the people running the intrusions."),
    P("**Action 4: the 2026 arrests.** A 24-year-old was arrested in Amsterdam on 15 September; the FBI called him \"one "
      "of the alleged leaders\". A suspect was detained in Jordan, and on 9 October a Canadian \"primary co-conspirator\" "
      "was arrested in Pennsylvania [12][13]. *Afterwards*, the leak site went offline [14], the group's Telegram "
      "spokesperson went silent [13], and Okta observed a gap in leak-site publishing from September to early November [13][14]. In "
      "November new posts claimed a return, and Okta linked the vishing cluster to a new \"INCEPTION\" leak site. "
      "INCEPTION denies being ShinyHunters [14]. This is the first wave to coincide with a visible halt."),
    P("**Judgement.** Up to 2025, law enforcement was a cost of doing business for the brand. It removed individuals and "
      "forced changes of technique, but each wave was followed within months by a new campaign under the same name. Our "
      "judgement for the 2026 wave is different. It reached people the FBI describes as leaders, coincided with the first "
      "sustained halt, and has been followed by a likely rebrand rather than a confident return. The most likely outcome "
      "is fragmentation. The techniques (vishing, token theft) will persist under new names, because they are cheap and "
      "learnable, but the ShinyHunters brand has probably been degraded as a trusted extortion label."),
]

PART_D = [
    H(2, "Part D. Key analytic judgements and confidence"),
    P("**Judgement 1: ShinyHunters is a shared brand with shifting membership, not a stable organisation (high "
      "confidence).** The evidence is that four separate groups of defendants, in four countries, have been charged across "
      "six years. GTIG also describes the name as a claim used for pressure [2], and the 2026 successor denies the name "
      "while using the same tradecraft [14]. The alternative is a persistent core leadership with rotating contractors. "
      "The FBI's \"alleged leaders\" language supports that [12]. We judge it less likely because the brand survived the "
      "removal of each prior set of operators unchanged. A persistent core is compatible with the evidence but not "
      "required by it."),
    P("**Judgement 2: the objective is monetisation, not notoriety or ideology (moderate confidence).** Every documented "
      "campaign ends in a sale listing, a ransom demand or a payment [2][8][17], and the FBI's US$70 million estimate "
      "implies a functioning business [12]. The alternative is status-seeking. The FBI breach claim was described as not "
      "financial, and Com culture rewards notoriety. We hold that notoriety serves extortion: a famous name raises "
      "payment rates. The FBI incident remains the one case that fits the alternative better."),
    P("**Judgement 3: the 2026 arrests have degraded the brand, and its activity is fragmenting rather than ending "
      "(low-to-moderate confidence).** The evidence is the halt in leak-site publishing, the silent spokesperson, a return "
      "claim that relies on old PGP keys, and Okta's INCEPTION link [13][14]. A plausible alternative is a deliberate "
      "pause before a full return under the original name, which happened after earlier forum seizures. Confidence is "
      "low-to-moderate because the observation window is only two months."),
    P("**Judgement 4: the Snowflake actors were part of ShinyHunters (low confidence).** One participant self-identified "
      "to Wired [8]. Neither Mandiant nor the indictment uses the name [1][5]. Because claiming the brand is itself a "
      "pressure tactic, a self-description is weak evidence. The alternative, that the UNC5537 actors borrowed the name "
      "or used ShinyHunters' forum to sell, fits the sources equally well."),
]

EXEC_BRIEF = [
    {"t": "pagebreak"},
    H(2, "Part E. Executive brief"),
    H(3, "For the SOC / IR team"),
    B("**Identity is the perimeter.** Enforce phishing-resistant MFA and network allow-lists on Snowflake, Salesforce "
      "and every data SaaS, including service and contractor accounts. The 2024 wave worked only where both were missing (A2, B).", count=False, size=19),
    B("**Hunt in platform logs.** In Snowflake query history, look for client APPLICATION values \"rapeflake\" or "
      "\"DBeaver_DBeaverUltimate\", CREATE TEMPORARY STAGE followed by COPY INTO and GET, and logons from Mullvad, PIA "
      "or ALEXHOST (AS200019) [1].", count=False, size=19),
    B("**Lock down connected apps.** Audit Salesforce connected apps (for example Data Loader named \"My Ticket Portal\"), remove "
      "\"API Enabled\" where not needed, alert on Tor exit nodes and the user-agent \"Salesforce-Multi-Org-Fetcher/1.0\", and "
      "revoke third-party OAuth tokens after a vendor incident [2][3].", count=False, size=19),
    B("**Treat exports as credential leaks.** Scan CRM records for AWS keys (AKIA...) and Snowflake tokens, and rotate them. "
      "UNC6395 harvested secrets for its next intrusion [3].", count=False, size=19),
    B("**Harden the help desk.** Use call-back verification for any IT-support request to authorise apps or reset MFA. "
      "Watch for legal-themed lure domains and extortion from shinycorp@ or shinygroup@tuta[.]com [2][14].", count=False, size=19),
    H(3, "For organisational leadership"),
    P("**The risk in plain terms.** The company's most sensitive data now lives in cloud platforms run by vendors. This "
      "group does not break those platforms. It logs in as our staff or contractors, or talks them into letting it in, "
      "then copies everything and demands payment not to publish it. One weak login at a supplier can expose millions of "
      "our customers' records (AT&T: more than 100 million). Arrests have not reliably stopped these crews; they reappear "
      "under new names.", count=False),
    P("**Decision 1: fund identity controls for every SaaS data platform**, including those used by contractors and "
      "integrations, and make strong MFA a contract condition for vendors who hold our data.", count=False),
    P("**Decision 2: set the extortion-payment policy now, before a demand arrives.** Paying does not guarantee deletion; "
      "the Snowflake defendant re-extorted at least one victim [7]. The policy should be approved with legal counsel and "
      "the regulators' notification timelines in mind.", count=False),
]

SOURCES = [
    {"t": "pagebreak"},
    H(2, "Part F. Sources"),
    P("Each entry gives the source type and, where it matters, our confidence in it.", count=False),
    *[{"t": "p", "text": t, "count": False, "size": 19} for t in [
        "[1] Mandiant (Google Cloud), \"UNC5537 Targets Snowflake Customer Instances for Data Theft and Extortion,\" 10 Jun. 2024. "
        "https://cloud.google.com/blog/topics/threat-intelligence/unc5537-snowflake-data-theft-extortion — *Vendor threat "
        "intelligence with technical detail; high confidence on TTPs; it deliberately does not name ShinyHunters.*",
        "[2] Google Threat Intelligence Group, \"The Cost of a Call: From Voice Phishing to Data Extortion,\" 4 Jun. 2025 "
        "(updated Aug. 2025). https://cloud.google.com/blog/topics/threat-intelligence/voice-phishing-data-extortion — "
        "*Vendor reporting; high confidence on technique, carefully hedged on attribution.*",
        "[3] Google Threat Intelligence Group, \"Widespread Data Theft Targets Salesforce Instances via Salesloft Drift,\" 26 Aug. 2025. "
        "https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift — "
        "*Vendor reporting with IOCs; does not link UNC6395 to ShinyHunters.*",
        "[4] U.S. Attorney's Office, W.D. Washington, \"Member of notorious international hacking crew sentenced to prison,\" "
        "Jan. 2024. https://www.justice.gov/usao-wdwa/pr/member-notorious-international-hacking-crew-sentenced-prison — "
        "*Primary government document; high confidence.*",
        "[5] CyberScoop, \"Here's the indictment against two men allegedly responsible for Snowflake customer breach,\" "
        "12 Nov. 2024. https://cyberscoop.com/connor-moucka-snowflake-data-breach-indictment-john-binns/ — *Journalism "
        "reproducing a primary legal filing; high confidence on the charges.*",
        "[6] BleepingComputer, \"Canadian pleads guilty to Snowflake cloud data theft attacks,\" 5 Aug. 2026. "
        "https://www.bleepingcomputer.com/news/security/canadian-pleads-guilty-to-snowflake-cloud-data-theft-attacks/ — "
        "*Journalism citing DOJ; high confidence.*",
        "[7] KrebsOnSecurity, \"Canadian Man Pleads Guilty in Snowflake Extortions,\" 6 Aug. 2026. "
        "https://krebsonsecurity.com/2026/08/canadian-man-pleads-guilty-in-snowflake-extortions/ — *Investigative "
        "journalism; DOJ-sourced facts are high confidence; Binns' release rests on unnamed sources (moderate).*",
        "[8] CSO Online (reporting Wired), \"Hacker allegedly paid $370,000 ransom to delete stolen AT&T data,\" Jul. 2024. "
        "https://www.csoonline.com/article/2517422/hacker-allegedly-paid-370000-ransom-to-delete-stolen-att-data.html — "
        "*Journalism; payment confirmed on-chain by TRM Labs; AT&T did not confirm; moderate-high confidence.*",
        "[9] SecurityWeek, \"AT&T Data Breach: Nearly All Wireless Customers Exposed in Massive Hack\" (on AT&T's SEC 8-K), "
        "12 Jul. 2024. https://www.securityweek.com/att-data-breach-nearly-all-wireless-customers-exposed-in-massive-hack/ — "
        "*Journalism on a primary corporate filing; high confidence.*",
        "[10] The Record, report on the French BreachForums/ShinyHunters arrests, Jun. 2025. https://therecord.media/france-breachforums-suspects-arrests — "
        "*Journalism citing the Paris prosecutor's statement; arrest dates vary by one or two days across outlets.*",
        "[11] The Register, \"Cops nuke BreachForums (again) amid cybercrime supergroup extortion blitz,\" 10 Oct. 2025. "
        "https://www.theregister.com/2025/10/10/cops_seize_breachforums/ — *Journalism; group's \"no impact\" claim is self-serving.*",
        "[12] BleepingComputer, \"FBI tells ShinyHunters members to turn themselves in after recent arrest,\" 29 Sep. 2026. "
        "https://www.bleepingcomputer.com/news/security/fbi-tells-shinyhunters-members-to-turn-themselves-in-after-recent-arrest/ — "
        "*Journalism; the US$70M / 140-organisation figures are FBI allegations, not proven.*",
        "[13] BleepingComputer, \"FBI arrests another suspected ShinyHunters hacker after agency breach,\" 9 Oct. 2026. "
        "https://www.bleepingcomputer.com/news/security/fbi-arrests-another-suspected-shinyhunters-hacker-after-agency-breach/ — "
        "*Journalism; suspect unnamed, charges not yet public.*",
        "[14] The Hacker News, \"Okta Links ShinyHunters-Associated Vishing Group to New INCEPTION Data Leak Site,\" 24 Nov. 2026. "
        "https://thehackernews.com/2026/11/okta-links-shinyhunters-associated.html — *Journalism on Okta vendor research; "
        "two-month window, so moderate confidence.*",
        "[15] BleepingComputer, \"ShinyHunters behind Salesforce data theft attacks at Qantas, Allianz Life and LVMH,\" 30 Jul. 2025. "
        "https://www.bleepingcomputer.com/news/security/shinyhunters-behind-salesforce-data-theft-attacks-at-qantas-allianz-life-and-lvmh/ — "
        "*Journalism with victim confirmations.*",
        "[16] BleepingComputer, \"Hacker group floods dark web with data stolen from 11 companies,\" May 2020. "
        "https://www.bleepingcomputer.com/news/security/hacker-group-floods-dark-web-with-data-stolen-from-11-companies/ — "
        "*Journalism on forum listings; claims (e.g. Microsoft GitHub) partly unverified.*",
        "[17] BleepingComputer, \"ShinyHunters claims Santander breach, selling data for 30M customers,\" May 2024. "
        "https://www.bleepingcomputer.com/news/security/shinyhunters-claims-santander-breach-selling-data-for-30m-customers/ — "
        "*Journalism on a sale listing; actor's claim, confirmed by Santander's breach notice.*",
        "[18] Sophos, \"Taking the shine off BreachForums,\" 2025. https://www.sophos.com/en-us/blog/taking-the-shine-off-breachforums — "
        "*Vendor research timeline of BreachForums seizures, relaunches and the June 2025 arrests; moderate confidence.*",
        "[19] The Hacker News, \"ShinyHunters claims FBI breach,\" 23 Sep. 2026. https://thehackernews.com/2026/09/shinyhunters-claims-fbi-breach-says-it.html — "
        "*Journalism on the group's own claims; low confidence on the zero-day claim; FBI confirmed a third-party platform incident.*",
    ]],
    H(2, "Generative AI use"),
    P("[Required by the brief: state specifically what any generative AI tool was used for. For example: \"A generative AI "
      "assistant (Claude) was used to locate and summarise candidate sources, check ATT&CK technique IDs, and draft text, which I "
      "reviewed, verified against the cited sources and edited.\" Replace this with an accurate description of your actual use.]",
      count=False),
]

BODY = FRONT + PART_A + PART_B + PART_C + PART_D
