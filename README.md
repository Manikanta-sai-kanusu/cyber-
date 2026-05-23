# Honeypot Network with Deception Technology

## Problem
Our network has no deception layer — attackers scan freely and can map out real services without detection.

## Solution
We deployed a Honeypot Network with 4 fake services (SSH, HTTP, SMB, FTP) that do nothing except log every attacker who touches them. Attackers think they found real servers, but every connection they make is silently recorded, fingerprinted, and reported. This provides us with instant alerts and threat intelligence about the scanning tools being used.

## How to Run

Install requirements:
```bash
pip install flask
```

Start the services (run each in a separate terminal):
```bash
python3 ssh_honeypot.py
python3 dashboard.py
python3 fingerprint.py
```

Open the live dashboard at `http://localhost:5000`

## Services

| Service | Port | Pretends To Be | Actually Does |
|---------|------|----------------|---------------|
| SSH | 2222 | Linux remote login server | Logs IP, banner grab, credentials tried |
| HTTP | 8080 | Admin web panel | Logs all requests, paths, headers |
| SMB | 4445 | Windows file server | Logs connection attempts and payloads |
| FTP | 2121 | File transfer server | Logs IP and login commands attempted |

## Test It

```bash
# Port scan — triggers T1046 detection
nmap -sV -p 2222,8080,4445,2121 localhost

# Hit the fake admin panel
curl http://localhost:8080/admin

# Simulate FTP login attempt
nc localhost 2121   # then type: USER root

# SSH banner grab
telnet localhost 2222
```

## Project Structure

```
honeypot-hackathon/
├── ssh_honeypot.py      # All 4 fake services — SSH, HTTP, SMB, FTP
├── dashboard.py         # Flask live dashboard at localhost:5000
├── fingerprint.py       # Attacker fingerprinting + threat intel report
├── honeypot_logs.json   # Auto-created log file (append-only)
└── README.md
```

## MITRE ATT&CK Mapping

- **T1046 (Network Service Discovery):** The honeypot logs when attackers scan our ports, recording timestamps, IP addresses, and which ports are hit.
- **T1595 (Active Scanning):** The fingerprinter tool identifies the tools used based on behavior (e.g., Nmap pattern = many services in a short time).

Detection maps to MITRE ATT&CK T1046 + T1595 with <1s response
