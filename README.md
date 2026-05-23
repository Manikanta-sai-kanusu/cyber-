Honeypot Network with Deception Technology

FoSC 23CSE313 Hackathon — Problem #29 | Defence Track
A deception-based intrusion detection system that silently logs, fingerprints, and reports attackers.


Problem Statement
Modern networks have no deception layer — attackers can enumerate services freely and go undetected. This project deploys a honeypot network with 4 fake services that lure attackers in, log every interaction, and generate threat intelligence reports mapped to MITRE ATT&CK.

What It Does
Any attacker who connects thinks they found a real server — but every probe is silently recorded, fingerprinted, and reported.
ServicePortPretends To BeActually DoesSSH2222Linux remote login serverLogs IP, banner grab, credentials triedHTTP8080Admin web panelLogs all requests, paths, headersSMB4445Windows file serverLogs connection attempts and payloadsFTP2121File transfer serverLogs IP and login commands attempted

Architecture
Attacker Laptop
      │
      ▼
Honeypot (4 fake services — ssh_honeypot.py)
      │  Python sockets on ports 2222, 8080, 4445, 2121
      ▼
Logger (honeypot_logs.json)
      │
      ├──▶ Flask Dashboard (dashboard.py) — localhost:5000
      │      Live table of all hits, auto-refreshes every 5s
      │
      └──▶ Fingerprinter (fingerprint.py)
             Identifies tool used (Nmap, Hydra, web scanner)
             Maps to MITRE ATT&CK T1046 + T1595

Quickstart
bash# 1. Install dependency
pip install flask

# 2. Start all honeypot services (keep running)
python3 ssh_honeypot.py

# 3. Start the live dashboard (keep running in a new terminal)
python3 dashboard.py

# Then open http://localhost:5000 in your browser

🧪 Test It (Attack Your Own Honeypot)
bash# Port scan — triggers T1046 detection
nmap -sV -p 2222,8080,4445,2121 localhost

# Hit the fake admin panel
curl http://localhost:8080/admin

# Simulate FTP login attempt
nc localhost 2121
# then type: USER root

# SSH banner grab
telnet localhost 2222

Generate Threat Intelligence Report
bashpython3 fingerprint.py
Sample output:
============================================================
   THREAT INTELLIGENCE REPORT
   Generated: 2024-01-01 12:00:00
   Total events: 12 | Unique attacker IPs: 1
============================================================

  ATTACKER IP : 127.0.0.1
  Tool        : Nmap / Port Scanner
  Total hits  : 12
  Services    : {'SSH': 3, 'HTTP': 4, 'SMB': 3, 'FTP': 2}
  First seen  : 11:59:02
  Last seen   : 11:59:04
  MITRE       : T1046 (Network Service Discovery)
                T1595 (Active Scanning)
============================================================

Project Structure
honeypot-hackathon/
├── ssh_honeypot.py      # All 4 fake services — SSH, HTTP, SMB, FTP
├── dashboard.py         # Flask live dashboard at localhost:5000
├── fingerprint.py       # Attacker fingerprinting + threat intel report
├── honeypot_logs.json   # Auto-created log file (append-only)
└── README.md

MITRE ATT&CK Mapping
Technique IDNameWhat the honeypot catchesT1046Network Service DiscoveryLogs attacker scanning your ports — timestamps, IP, which ports hitT1595Active ScanningFingerprints the tool used (Nmap = multi-service probe in short time)

A firewall blocks. A honeypot lets them in and collects intelligence.


Tech Stack

Language: Python 3 (sockets, threading, Flask)
Logging: JSON (append-only NDJSON)
Dashboard: Flask + Jinja2 templating
Containerisation: Docker-compatible (on-premises / hybrid)
Detection mapping: MITRE ATT&CK Framework


View Logs
bash# Dump all logs
cat honeypot_logs.json

# Watch live as attacks come in
tail -f honeypot_logs.json

Team Responsibilities
PersonRolePerson 1Honeypot services (ssh_honeypot.py)Person 2Live dashboard (dashboard.py)Person 3Fingerprinter + MITRE mapping (fingerprint.py)Person 4Architecture diagram, slides, GitHub + docs

Detection maps to MITRE ATT&CK T1046 + T1595 with <1s response time.
