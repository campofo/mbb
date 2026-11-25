"""Table data for the report body, kept separate from the prose so prose rewrites cannot change it."""

S1_1 = {'t': 'table',
 'header': ['Feature', 'Evidence for this incident', 'Confidence / gaps'],
 'rows': [['Adversary',
           'A RansomHub affiliate. The binary, the note and the operator tooling tie the attack to the brand [2]. '
           'The hands-on operator used a Splashtop display name "johnattan" from a client host "WINVM", and the '
           'clipboard showed 10.0.2.15, the VirtualBox NAT default. The operator was working from a virtual machine '
           '[2].',
           'Affiliate identity unknown. Brand attribution is high confidence, individual attribution none.'],
          ['Capability',
           'Password spraying; Mimikatz (DCSync per child domain, LSASS); NirSoft CredentialsFileView; Advanced IP '
           'Scanner and SoftPerfect NetScan; Atera and Splashtop remote-management (RMM) tools; Rclone over SFTP; '
           'the RansomHub encryptor amd64.exe run with -pass and -only-local, spread over SMB via random six-letter '
           'services; vssadmin, wevtutil and Hyper-V Stop-VM before encryption [2].',
           'High. Tools were recovered and hashed.'],
          ['Infrastructure',
           'Spray sources 185.190.24.54 and 185.190.24.33; interactive logon from 164.138.90.2; exfiltration to '
           '38.180.245.207 on TCP 443 (SFTP, not HTTPS) [2]. Legitimate Atera and Splashtop SaaS relays were used '
           "for C2-like access. Victim communication runs through RansomHub's Tor negotiation and leak "
           'infrastructure [1].',
           "High for the IPs (from logs); the hosting providers' role is unknown."],
          ['Victim',
           'A multi-domain Active Directory organisation with internet-exposed RDP, Hyper-V hosts, file servers and '
           'Veeam backup servers (the exfiltration script was staged in C:\\ProgramData\\Veeam\\) [2].',
           'Name, sector, size and country withheld by the source.']],
 'widths': [0.16, 0.56, 0.28],
 'caption': 'Table 1. Core features (sources in brackets).',
 'size': 19,
 'firstColBold': True,
 'firstColShade': True}


S1_2 = {'t': 'table',
 'header': ['Meta-feature', 'This incident'],
 'rows': [['Timestamp', 'November 2024; time to ransomware about 118 hours over six calendar days [2].'],
          ['Phase', 'Every phase from initial access to impact is evidenced (see Section 2).'],
          ['Result',
           'About 2.03 GB exfiltrated in about 40 minutes on day 3; domain-wide encryption, shadow copies deleted, '
           'logs cleared on day 6 [2]. Ransom amount and payment outcome are not reported.'],
          ['Direction',
           'Adversary → infrastructure → victim for access; victim → infrastructure (38.180.245.207) for '
           'exfiltration.'],
          ['Methodology',
           'Human-operated double extortion: living off the land plus commercial RMM, credential theft, exfiltration '
           'before encryption.'],
          ['Resources',
           'RaaS access (builds, panel, leak site supplied by the operator [3]); free or commercial tools; rented '
           'VPS addresses; an operator VM.']],
 'widths': [0.2, 0.8],
 'caption': 'Table 2. Meta-features (all six recorded).',
 'size': 19,
 'firstColBold': True,
 'firstColShade': True}


S2_1 = {'t': 'table',
 'header': ['Stage', 'Evidence in this incident', 'Status'],
 'rows': [['Reconnaissance',
           'The affiliate found an internet-facing RDP server. How it was found (scanning or a purchased list) is '
           'not reported.',
           'Inferred, not evidenced'],
          ['Weaponisation',
           'No exploit was built. The operator supplied the encryptor, and per-victim builds need a 64-character '
           'password [4].',
           'Not applicable / not evidenced'],
          ['Delivery',
           'Password spray against the RDP server from two IPs over about four hours; six accounts authenticated '
           '(Event ID 4624) [2].',
           'Evidenced'],
          ['Exploitation',
           'No vulnerability was exploited. The intruder logged on with a valid account from 164.138.90.2 with an '
           'elevated token [2].',
           'Evidenced (valid accounts)'],
          ['Installation',
           'Day 2: Atera installed on two backup servers; Splashtop used from day 5; new services (Event ID 7045); '
           'passwords reset for several users before impact [2].',
           'Evidenced'],
          ['Command and control',
           'Direct RDP throughout, plus Atera and Splashtop to blend in with administration traffic [2].',
           'Evidenced'],
          ['Actions on objectives',
           'Day 1: net/nltest discovery, RDP to two domain controllers, Mimikatz DCSync. Days 1 and 2: IP Scanner '
           'and NetScan sweeps. Day 3: Rclone exfiltration of 2.03 GB. Day 6: amd64.exe, SMB propagation, VM '
           'shutdown, shadow-copy deletion, log clearing, encryption [2].',
           'Evidenced; ransom note image only, negotiation not reported']],
 'widths': [0.18, 0.6, 0.22],
 'caption': 'Table 3. Kill-chain mapping of the same incident.',
 'size': 19,
 'firstColBold': True,
 'firstColShade': True}

