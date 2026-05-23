# Honeypot Network with Deception Technology

## Problem
Our network has no deception layer — attackers scan freely and can map out real services without detection.

## Solution
We deployed a Honeypot Network with 4 fake services (SSH, HTTP, SMB, RDP) that do nothing except log every attacker who touches them. Attackers think they found real servers, but every connection they make is silently recorded, fingerprinted, and reported. This provides us with instant alerts and threat intelligence about the scanning tools being used.

## How to Run

Install requirements:
```bash
pip install -r requirements.txt
```

### Terminal 1 — Honeypot Server

Move to the backend folder:
```bash
cd "C:\Users\Manikanta\Downloads\hackathon-defense-main\hackathon-defense-main\honeypot-project\backend"
```

Start the honeypot:
```bash
python ssh_honeypot.py
```

Expected output:
```
[*] SSH honeypot listening on port 2222
[*] HTTP honeypot listening on port 8080
[*] SMB honeypot listening on port 4445
[*] RDP honeypot listening on port 3389
[*] All honeypot services running
```

When an attacker connects, you will see live alerts:
```
[ALERT] HTTP hit from 127.0.0.1
[ALERT] SSH hit from 127.0.0.1
[ALERT] SMB hit from 127.0.0.1
```

### Terminal 2 — Dashboard

```bash
python dashboard.py
```

Open the live dashboard at `http://localhost:5000`

### Terminal 3 — Threat Intelligence Report

```bash
python fingerprint.py
```

Expected output:
```
THREAT INTELLIGENCE REPORT
Tool   : Nmap / Port Scanner
MITRE  : T1046, T1595
```

---

## Testing (Attacker Simulation)

Open a separate terminal and move to the backend folder:
```bash
cd "C:\Users\Manikanta\Downloads\hackathon-defense-main\hackathon-defense-main\honeypot-project\backend"
```

**1. Scan honeypot ports:**
```bash
nmap -Pn -sT -p 2222,8080,3389,4445 127.0.0.1
```
Expected output:
```
2222/tcp open
3389/tcp open
4445/tcp open
8080/tcp open
```

**2. Simulate HTTP attack:**
```bash
curl http://localhost:8080/admin
```
Expected output:
```
<h1>Admin Panel</h1>
```

**3. View captured logs:**
```bash
type honeypot_logs.json
```
Expected output:
```json
{"service":"HTTP","attacker_ip":"127.0.0.1"}
```

---

## Services

| Service | Port | Pretends To Be | Actually Does |
|---------|------|----------------|---------------|
| SSH | 2222 | Linux remote login server | Logs IP, banner grab, credentials tried |
| HTTP | 8080 | Admin web panel | Logs all requests, paths, headers |
| SMB | 4445 | Windows file server | Logs connection attempts and payloads |
| RDP | 3389 | Windows remote desktop | Logs connection attempts and payloads |

## Project Structure

```
hackathon-defense-main/
├── honeypot-project/
│   ├── attacker-simulator/
│   │   └── .gitkeep
│   ├── backend/
│   │   ├── logs/
│   │   ├── app.py
│   │   ├── dashboard.py
│   │   ├── Dockerfile
│   │   ├── fingerprint.py
│   │   ├── honeypot_logs.json
│   │   ├── honeypot_server.py
│   │   ├── http_service.py
│   │   ├── logger.py
│   │   ├── rdp_service.py
│   │   ├── requirements.txt
│   │   ├── smb_service.py
│   │   ├── ssh_honeypot.py
│   │   └── ssh_service.py
│   └── docs/
│       └── .gitkeep
├── README.md
└── .gitignore
```

## MITRE ATT&CK Mapping

- **T1046 (Network Service Discovery):** The honeypot logs when attackers scan our ports, recording timestamps, IP addresses, and which ports are hit.
- **T1595 (Active Scanning):** The fingerprinter tool identifies the tools used based on behavior (e.g., Nmap pattern = many services in a short time).

Detection maps to MITRE ATT&CK T1046 + T1595 with <1s response
