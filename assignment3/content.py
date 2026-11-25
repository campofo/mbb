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

from tables import PART_A_1 as ATTACK_TABLE, PART_A_2 as TIMELINE_TABLE  # noqa: E402
from tables import PART_B_1 as DIAMOND_CORE, PART_B_2 as DIAMOND_META, PART_B_3 as KILL_CHAIN  # noqa: E402

PART_A = [
    H(2, "Part A. Intelligence profile"),
    P("**Word count (Parts A to D): {WC}** (excluding the executive brief, sources and the Diamond/kill-chain tables)", count=False),
    H(3, "A1. Identity, motivations and objectives"),
    P("\"ShinyHunters\" is best understood as a brand. Since 2020 the name has served as a handle and leak identity for a "
      "changing set of mostly young English- and French-speaking people, and six years of prosecutions show how often "
      "those people change. Charges from the 2020 to 2021 period named three French nationals, among them Sebastien "
      "Raoult, who built phishing pages for the group and was sentenced in Seattle in January 2024 to three years and "
      "more than US$5 million in restitution [4]. The 2024 Snowflake campaign was charged against a Canadian, Connor "
      "Moucka, and a US citizen living in Turkey, John Binns [5]. French police arrested four people in June 2025, one of "
      "them using the handle \"ShinyHunters\" itself [10], and Dutch, Jordanian and US arrests followed in September and "
      "October 2026 [12][13]. Vendors attribute more cautiously. Google's Threat Intelligence Group (GTIG) tracks the 2025 "
      "Salesforce intrusions as UNC6040 and the extortion as UNC6240, and says only that UNC6240 \"consistently claimed\" "
      "to be ShinyHunters, probably to put more pressure on victims [2]. Mandiant's report on the Snowflake actor, "
      "UNC5537, never uses the name, although one of the hackers told Wired he was a member [1][8]. The brand claim is "
      "therefore well supported for 2020 to 2021 and for 2025 to 2026, contested for the 2024 Snowflake campaign, and in "
      "every period consistent with changing membership."),
    P("The group steals data in bulk for money, then extorts the owner or sells the data on. The evidence for this is "
      "specific to the actor: forum sale listings for Ticketmaster and Santander data [17], AT&T's reported US$370,000 "
      "payment for deletion [8], 72-hour bitcoin demands in the Salesforce campaign [2], and the FBI's 2026 estimate of at "
      "least US$70 million in extortion payments from more than 140 organisations [12]. Unlike the espionage actors covered "
      "in this course, ShinyHunters wants the victim to know about the theft, because the victim's fear of disclosure is "
      "what it sells. I read the group's 2026 claim that its FBI intrusion was \"not financially motivated\" [12] as "
      "reputation-building, not a change of objective (Part D, judgement 2)."),
    P("The business model runs through three channels, often on the same data. Private extortion comes first, by email or "
      "phone demands to staff with 72-hour bitcoin deadlines [2], sometimes through a hired go-between, as with AT&T [8]. "
      "Resale follows on BreachForums, where Moucka alone made at least US$495,000 [6] and where Santander and Ticketmaster "
      "data were advertised in 2024 [17]. Public shaming completes it: from late 2025 a leak portal listed 39 "
      "Salesforce-customer victims, including Qantas, Toyota and FedEx [11], and in 2026 targets appeared on the leak site "
      "1 to 28 days after their phishing domains were registered [14]. Private extortion leads because a breach that is "
      "paid for and never published is worth most to both sides, and resale is the fallback once a victim refuses. Stolen "
      "data also loses value with age and with every disclosure, so the group moves quickly, which is the opposite of an "
      "espionage actor's habit of keeping access quietly for as long as it can."),
    H(3, "A2. Capabilities, tools and TTPs"),
    P("ShinyHunters does not deploy ransomware and rarely uses custom malware. Its capability lies in reaching data "
      "platforms through stolen identities and then exporting in bulk, and its tradecraft has gone through three "
      "documented phases:"),
    B("In 2020 and 2021 the group relied on phishing and repository mining. Spoofed login pages collected employee "
      "credentials, and private code repositories were searched for cloud keys [4]."),
    B("In 2024 the Snowflake actors (UNC5537) used credentials that infostealers such as VIDAR, RedLine and Lumma had "
      "collected, some of them as early as 2020, to log into customer Snowflake accounts that had neither MFA nor network "
      "allow-lists [1]. A reconnaissance utility the actors called \"rapeflake\" (Mandiant's FROSTBITE) and DBeaver "
      "Ultimate listed the tables; data was staged with CREATE TEMPORARY STAGE and COPY INTO (gzip) and pulled down with "
      "GET [1]."),
    B("From 2025 the group turned to vishing and SaaS token abuse. Callers posing as IT support talked staff into "
      "authorising a modified Salesforce Data Loader connected app, sometimes named \"My Ticket Portal\", and collected "
      "Okta credentials and MFA codes [2]. The UNC6395 cluster stole OAuth tokens from the Salesloft Drift integration, ran "
      "SOQL exports across Salesforce tenants and searched the results for AWS keys and Snowflake tokens it could reuse "
      "[3]. In 2026 Okta tracked a ShinyHunters-linked vishing cluster using legal-themed lure domains [14]."),
    ATTACK_TABLE,
    H(3, "A3. Infrastructure and targeting/victimology"),
    P("Most of ShinyHunters' infrastructure is rented or borrowed. Access ran through commercial VPNs (Mullvad and Private "
      "Internet Access) and Tor, bulk exfiltration went to VPSs at ALEXHOST (AS200019, Moldova), and stolen data was kept "
      "on MEGA [1][2]. The Drift campaign added DigitalOcean and AWS hosts and distinctive user-agents such as "
      "\"Salesforce-Multi-Org-Fetcher/1.0\" [3]. Extortion used Tuta mail addresses (shinycorp@tuta[.]com and "
      "shinygroup@tuta[.]com) [2], Telegram channels, and a succession of BreachForums domains and leak sites. The forums "
      "were the group's sales channel and, from 2025, its leak site, until they were seized in October 2025 [11]."),
    P("The victims of each wave share a platform more than a sector. In 2020 they were consumer platforms such as "
      "Tokopedia [16]. In 2024 they were Snowflake customers in telecoms, ticketing, banking and retail, and Mandiant "
      "notified about 165 organisations [1]. In 2025 they were Salesforce tenants in aviation (Qantas), insurance (Allianz "
      "Life) and luxury retail (LVMH brands), as well as Google's own corporate instance [2][15]. In none of these waves "
      "was the platform itself breached: Snowflake and Salesforce both say so, and Mandiant found no compromise of "
      "Snowflake's enterprise environment [1][11]. The data belonged to the platforms' customers, and the harm landed on "
      "those customers' own clients, such as AT&T's subscribers. I treat the customer organisation as the victim in the "
      "Diamond Model sense, and the platform as a shared attack surface whose defaults (optional MFA, broad API access, "
      "long-lived tokens) let a single technique reach hundreds of victims."),
    H(3, "A4. Historical activity and relationships"),
    TIMELINE_TABLE,
    P("The most important relationship is with \"the Com\", the loose English-speaking online community that also "
      "produced Scattered Spider and LAPSUS$. GTIG judges that the overlap between UNC6040 and Com actors more likely "
      "reflects shared communities than a direct operational relationship [2]. In August 2025 the brands merged their "
      "messaging as \"Scattered LAPSUS$ Hunters\" [11], but a merger announced on Telegram proves shared branding at most. "
      "Links to established e-crime are visible but loose. The Snowflake actors are tied to the Com rather than to "
      "Russian-speaking ransomware [5], and in 2026 ShinyHunters reportedly hijacked the Cl0p leak site [19], an act of "
      "rivalry rather than partnership. The evidence supports a network of individuals who share a brand, forums and "
      "techniques and regroup from one campaign to the next."),
]

PART_B = [
    H(2, "Part B. Representative incident: the AT&T Snowflake theft (April 2024)"),
    P("Between 14 and 25 April 2024, attackers took call and text metadata for nearly all AT&T wireless customers (more "
      "than 100 million people, covering May to October 2022) from AT&T's Snowflake workspace [9]. I chose this incident "
      "because it is the best-documented ShinyHunters-associated case, with an SEC filing, a federal indictment, a guilty "
      "plea and a ransom payment traced on the blockchain [5][6][8][9]."),
    DIAMOND_CORE,
    DIAMOND_META,
    KILL_CHAIN,
    P("AT&T learned of the theft on 19 April 2024, when the actor claimed it, while exfiltration was still going on [9]. "
      "A security researcher whom the hacker had enlisted ran the negotiation, and AT&T paid him a fee as well. The "
      "opening demand of US$1 million came down to about US$370,000, paid in May as 5.7 BTC, which TRM Labs traced "
      "on-chain, and a video of the data being deleted was supplied in return [8]. Two later facts limit what that payment "
      "bought. The intermediary warned that fragments of the data might still exist, and the DOJ says Moucka re-extorted "
      "at least one victim [7][8]. Wagenius, a serving US soldier, later pleaded guilty to extorting AT&T over the same "
      "data [7]."),
    P("The kill chain fits this incident poorly. Weaponisation, installation and command and control barely apply to a "
      "SaaS intrusion with no malware, and all of the attacker's effort sits at the two ends: obtaining a credential, then "
      "extorting. The middle of the chain, where endpoint security looks, is empty, so defence has to sit at the identity "
      "layer and in the platform's own query logs."),
]

PART_C = [
    H(2, "Part C. Law-enforcement and disruption actions"),
    P("**Action 1: prosecution of Sebastien Raoult (arrested 2022, sentenced January 2024).** This removed one operator of "
      "the 2020 to 2021 phishing infrastructure and imposed restitution [4]. *Afterwards* the brand carried on without a "
      "pause: within months of the sentence, data from the Snowflake campaign was on sale under the ShinyHunters name "
      "[17]. The action disrupted one person and one generation of tooling, and left the name, its forum presence and its "
      "reputation intact."),
    P("**Action 2: the Snowflake arrests and charges (October 2024 to August 2026).** Moucka was arrested in Canada on 30 "
      "October 2024 and Binns was detained in Turkey. Both were indicted for extorting about US$2.5 million from at least "
      "ten organisations [5], and Moucka pleaded guilty in August 2026 [6]. *Afterwards* the Snowflake extortion wave "
      "ended, as victims switched on the MFA and allow-lists whose absence it had relied on [1]. Within months, though, "
      "the brand's activity had moved to Salesforce vishing (UNC6040) [2]. Binns has reportedly been released and has "
      "obtained Turkish citizenship, which bars extradition, although this rests on unnamed sources [7]. The people and "
      "the technique were disrupted, and the business continued with a new technique."),
    P("**Action 3: the French arrests (June 2025) and the BreachForums seizure (October 2025).** French police arrested "
      "four suspected BreachForums and ShinyHunters figures [10], and a new BreachForums was announced within a week [18]. "
      "In October 2025 the FBI and French authorities seized the BreachForums domain then serving as the Salesforce "
      "extortion portal [11]. *Afterwards* activity sped up. The Salesforce campaign hit Qantas, Allianz Life and LVMH "
      "brands in July 2025, the Drift token theft followed in August [3][15], and the group said the seizure had \"no "
      "impact\" and kept leaking through other channels [11]. Arrests at the forum layer did not reach the people running "
      "the intrusions."),
    P("**Action 4: the 2026 arrests.** On 15 September a 24-year-old was arrested in Amsterdam, and the FBI called him "
      "\"one of the alleged leaders\". A suspect was detained in Jordan, and on 9 October a Canadian \"primary "
      "co-conspirator\" was arrested in Pennsylvania [12][13]. *Afterwards* the leak site went offline [14], the group's "
      "Telegram spokesperson fell silent [13], and Okta saw no leak-site publishing from September to early November "
      "[13][14]. In November new posts claimed a return, and Okta linked the vishing cluster to a new \"INCEPTION\" leak "
      "site, though INCEPTION denies being ShinyHunters [14]. This is the first wave of arrests to coincide with a visible "
      "halt."),
    P("**Judgement.** Until 2025 law enforcement was a cost of doing business for the brand. Each wave removed individuals "
      "and forced a change of technique, and each was followed within months by a new campaign under the same name. I "
      "judge the 2026 wave differently. It reached people the FBI describes as leaders, coincided with the first sustained "
      "halt, and has been followed by what looks more like a rebrand than a confident return. Fragmentation is the most "
      "likely outcome: vishing and token theft are cheap and easy to learn, so they will persist under new names, but the "
      "ShinyHunters brand has probably been degraded as a trusted extortion label."),
]

PART_D = [
    H(2, "Part D. Key analytic judgements and confidence"),
    P("**Judgement 1: ShinyHunters is a shared brand with changing membership, not a stable organisation (high "
      "confidence).** Four separate sets of defendants in four countries have been charged over six years, GTIG treats "
      "the name as a claim used for pressure [2], and the 2026 successor rejects the name while using the same tradecraft "
      "[14]. The alternative is a lasting core leadership that hires rotating contractors, which the FBI's \"alleged "
      "leaders\" language supports [12]. I think it less likely because the brand carried on unchanged each time a set of "
      "operators was removed. A lasting core fits the evidence, but the evidence does not require one."),
    P("**Judgement 2: the objective is money, not notoriety or ideology (moderate confidence).** Every documented campaign "
      "ends in a sale listing, a ransom demand or a payment [2][8][17], and the FBI's US$70 million estimate implies a "
      "working business [12]. The alternative is status-seeking, since the FBI breach was described as not financial and "
      "Com culture rewards notoriety. My view is that notoriety serves extortion, because a famous name raises payment "
      "rates, but the FBI incident is the one case that fits the alternative better."),
    P("**Judgement 3: the 2026 arrests have degraded the brand, and its activity is fragmenting rather than ending "
      "(low-to-moderate confidence).** The evidence is the halt in leak-site publishing, the silent spokesperson, a return "
      "claim that relies on old PGP keys, and Okta's link to INCEPTION [13][14]. A plausible alternative is a deliberate "
      "pause before a full return under the original name, as happened after earlier forum seizures. My confidence is "
      "limited because the observation window is only two months."),
    P("**Judgement 4: the Snowflake actors were part of ShinyHunters (low confidence).** One participant described himself "
      "as a member to Wired [8], but neither Mandiant nor the indictment uses the name [1][5]. Claiming the brand is "
      "itself a pressure tactic, so a self-description is weak evidence, and the alternative (that the UNC5537 actors "
      "borrowed the name, or simply used ShinyHunters' forum to sell) fits the sources equally well."),
]

EXEC_BRIEF = [
    {"t": "pagebreak"},
    H(2, "Part E. Executive brief"),
    H(3, "For the SOC / IR team"),
    B("Enforce phishing-resistant MFA and network allow-lists on Snowflake, Salesforce and every other data SaaS, "
      "including service and contractor accounts. The 2024 wave succeeded only where both were missing (A2, B).",
      count=False, size=19),
    B("Hunt in Snowflake query history for the client APPLICATION values \"rapeflake\" and \"DBeaver_DBeaverUltimate\", "
      "for CREATE TEMPORARY STAGE followed by COPY INTO and GET, and for logons from Mullvad, PIA or ALEXHOST "
      "(AS200019) [1].", count=False, size=19),
    B("Audit Salesforce connected apps (for example a Data Loader named \"My Ticket Portal\"), remove \"API Enabled\" "
      "where it is not needed, alert on Tor exit nodes and on the user-agent \"Salesforce-Multi-Org-Fetcher/1.0\", and "
      "revoke third-party OAuth tokens after any vendor incident [2][3].", count=False, size=19),
    B("Treat CRM exports as credential leaks: scan records for AWS keys (AKIA...) and Snowflake tokens and rotate them, "
      "because UNC6395 harvested secrets for its next intrusion [3].", count=False, size=19),
    B("Require call-back verification before the help desk authorises an app or resets MFA, and watch for legal-themed "
      "lure domains and for extortion from shinycorp@ or shinygroup@tuta[.]com [2][14].", count=False, size=19),
    H(3, "For organisational leadership"),
    P("Our most sensitive data now sits in cloud platforms that vendors run. This group does not break into those "
      "platforms. It logs in as our staff or contractors, or talks them into letting it in, copies everything and then "
      "demands payment to keep the data unpublished. One weak login at a supplier can expose millions of customer records; "
      "at AT&T it was more than 100 million. Arrests have not reliably stopped these crews, who tend to reappear under new "
      "names.", count=False),
    P("**Decision 1: fund identity controls for every SaaS data platform**, including those used by contractors and "
      "integrations, and make strong MFA a contract condition for any vendor that holds our data.", count=False),
    P("**Decision 2: set the extortion-payment policy now, before a demand arrives.** Paying does not guarantee deletion; "
      "the Snowflake defendant re-extorted at least one victim [7]. The policy should be agreed with legal counsel, with "
      "the regulators' notification deadlines in mind.", count=False),
]

SOURCES = [
    {"t": "pagebreak"},
    H(2, "Part F. Sources"),
    P("Each entry gives the source type and, where it matters, my confidence in it.", count=False),
    *[{"t": "p", "text": t, "count": False, "size": 19} for t in [
        "[1] Mandiant (Google Cloud), \"UNC5537 Targets Snowflake Customer Instances for Data Theft and Extortion,\" 10 Jun. 2024. "
        "https://cloud.google.com/blog/topics/threat-intelligence/unc5537-snowflake-data-theft-extortion · *Vendor threat "
        "intelligence with technical detail; high confidence on TTPs; it deliberately does not name ShinyHunters.*",
        "[2] Google Threat Intelligence Group, \"The Cost of a Call: From Voice Phishing to Data Extortion,\" 4 Jun. 2025 "
        "(updated Aug. 2025). https://cloud.google.com/blog/topics/threat-intelligence/voice-phishing-data-extortion · "
        "*Vendor reporting; high confidence on technique, carefully hedged on attribution.*",
        "[3] Google Threat Intelligence Group, \"Widespread Data Theft Targets Salesforce Instances via Salesloft Drift,\" 26 Aug. 2025. "
        "https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift · "
        "*Vendor reporting with IOCs; does not link UNC6395 to ShinyHunters.*",
        "[4] U.S. Attorney's Office, W.D. Washington, \"Member of notorious international hacking crew sentenced to prison,\" "
        "Jan. 2024. https://www.justice.gov/usao-wdwa/pr/member-notorious-international-hacking-crew-sentenced-prison · "
        "*Primary government document; high confidence.*",
        "[5] CyberScoop, \"Here's the indictment against two men allegedly responsible for Snowflake customer breach,\" "
        "12 Nov. 2024. https://cyberscoop.com/connor-moucka-snowflake-data-breach-indictment-john-binns/ · *Journalism "
        "reproducing a primary legal filing; high confidence on the charges.*",
        "[6] BleepingComputer, \"Canadian pleads guilty to Snowflake cloud data theft attacks,\" 5 Aug. 2026. "
        "https://www.bleepingcomputer.com/news/security/canadian-pleads-guilty-to-snowflake-cloud-data-theft-attacks/ · "
        "*Journalism citing DOJ; high confidence.*",
        "[7] KrebsOnSecurity, \"Canadian Man Pleads Guilty in Snowflake Extortions,\" 6 Aug. 2026. "
        "https://krebsonsecurity.com/2026/08/canadian-man-pleads-guilty-in-snowflake-extortions/ · *Investigative "
        "journalism; DOJ-sourced facts are high confidence; Binns' release rests on unnamed sources (moderate).*",
        "[8] CSO Online (reporting Wired), \"Hacker allegedly paid $370,000 ransom to delete stolen AT&T data,\" Jul. 2024. "
        "https://www.csoonline.com/article/2517422/hacker-allegedly-paid-370000-ransom-to-delete-stolen-att-data.html · "
        "*Journalism; payment confirmed on-chain by TRM Labs; AT&T did not confirm; moderate-high confidence.*",
        "[9] SecurityWeek, \"AT&T Data Breach: Nearly All Wireless Customers Exposed in Massive Hack\" (on AT&T's SEC 8-K), "
        "12 Jul. 2024. https://www.securityweek.com/att-data-breach-nearly-all-wireless-customers-exposed-in-massive-hack/ · "
        "*Journalism on a primary corporate filing; high confidence.*",
        "[10] The Record, report on the French BreachForums/ShinyHunters arrests, Jun. 2025. https://therecord.media/france-breachforums-suspects-arrests · "
        "*Journalism citing the Paris prosecutor's statement; arrest dates vary by one or two days across outlets.*",
        "[11] The Register, \"Cops nuke BreachForums (again) amid cybercrime supergroup extortion blitz,\" 10 Oct. 2025. "
        "https://www.theregister.com/2025/10/10/cops_seize_breachforums/ · *Journalism; group's \"no impact\" claim is self-serving.*",
        "[12] BleepingComputer, \"FBI tells ShinyHunters members to turn themselves in after recent arrest,\" 29 Sep. 2026. "
        "https://www.bleepingcomputer.com/news/security/fbi-tells-shinyhunters-members-to-turn-themselves-in-after-recent-arrest/ · "
        "*Journalism; the US$70M / 140-organisation figures are FBI allegations, not proven.*",
        "[13] BleepingComputer, \"FBI arrests another suspected ShinyHunters hacker after agency breach,\" 9 Oct. 2026. "
        "https://www.bleepingcomputer.com/news/security/fbi-arrests-another-suspected-shinyhunters-hacker-after-agency-breach/ · "
        "*Journalism; suspect unnamed, charges not yet public.*",
        "[14] The Hacker News, \"Okta Links ShinyHunters-Associated Vishing Group to New INCEPTION Data Leak Site,\" 24 Nov. 2026. "
        "https://thehackernews.com/2026/11/okta-links-shinyhunters-associated.html · *Journalism on Okta vendor research; "
        "two-month window, so moderate confidence.*",
        "[15] BleepingComputer, \"ShinyHunters behind Salesforce data theft attacks at Qantas, Allianz Life and LVMH,\" 30 Jul. 2025. "
        "https://www.bleepingcomputer.com/news/security/shinyhunters-behind-salesforce-data-theft-attacks-at-qantas-allianz-life-and-lvmh/ · "
        "*Journalism with victim confirmations.*",
        "[16] BleepingComputer, \"Hacker group floods dark web with data stolen from 11 companies,\" May 2020. "
        "https://www.bleepingcomputer.com/news/security/hacker-group-floods-dark-web-with-data-stolen-from-11-companies/ · "
        "*Journalism on forum listings; claims (e.g. Microsoft GitHub) partly unverified.*",
        "[17] BleepingComputer, \"ShinyHunters claims Santander breach, selling data for 30M customers,\" May 2024. "
        "https://www.bleepingcomputer.com/news/security/shinyhunters-claims-santander-breach-selling-data-for-30m-customers/ · "
        "*Journalism on a sale listing; actor's claim, confirmed by Santander's breach notice.*",
        "[18] Sophos, \"Taking the shine off BreachForums,\" 2025. https://www.sophos.com/en-us/blog/taking-the-shine-off-breachforums · "
        "*Vendor research timeline of BreachForums seizures, relaunches and the June 2025 arrests; moderate confidence.*",
        "[19] The Hacker News, \"ShinyHunters claims FBI breach,\" 23 Sep. 2026. https://thehackernews.com/2026/09/shinyhunters-claims-fbi-breach-says-it.html · "
        "*Journalism on the group's own claims; low confidence on the zero-day claim; FBI confirmed a third-party platform incident.*",
    ]],
    H(2, "Generative AI use"),
    P("[Required by the brief: state specifically what any generative AI tool was used for. For example: \"A generative AI "
      "assistant (Claude) was used to locate and summarise candidate sources, check ATT&CK technique IDs, and draft text, which I "
      "reviewed, verified against the cited sources and edited.\" Replace this with an accurate description of your actual use.]",
      count=False),
]

BODY = FRONT + PART_A + PART_B + PART_C + PART_D
