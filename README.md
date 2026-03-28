<img width="338" height="457" alt="Screenshot 2026-03-29 at 01 32 28" src="https://github.com/user-attachments/assets/75914717-b921-487e-b2a8-159e56551159" />

**Detecting the logs that aren't there.**

EVI is a cybersecurity-focused log analysis tool that identifies **missing or tampered log entries** by detecting **unexpected gaps in timestamps**. Instead of only analyzing what exists, EVI highlights **what should exist but doesn't**—a critical blind spot in traditional systems.

---

## 🚀 Overview

In modern systems, logs are treated as a source of truth. However, attackers often **delete or manipulate logs** to hide their activity.

EVI addresses this by:

* Parsing logs from multiple formats
* Reconstructing event timelines
* Detecting suspicious gaps in activity
* Classifying severity of anomalies
* Presenting results via an interactive terminal dashboard

---

## 🎯 Key Features

### 🔍 Log Analysis

* Supports multiple formats:
  * ISO timestamps
  * Apache logs
  * Syslog
* Normalizes timestamps into a unified timeline

### ⏱️ Gap Detection Engine

* Calculates time differences between consecutive log entries
* Flags gaps exceeding defined thresholds

### 🚨 Severity Classification

| Severity | Condition    | Meaning                         |
| -------- | ------------ | ------------------------------- |
| LOW      | < 60 seconds | Normal system delay             |
| MEDIUM   | 1–5 minutes  | Suspicious activity             |
| CRITICAL | > 5 minutes  | Possible log tampering/deletion |

---

### 🤖 EVI Assistant (AI Persona)

EVI is not just a tool—it behaves like a **digital forensic analyst**:

* Explains findings in human-readable language
* Guides investigation steps
* Highlights critical anomalies

---

### 🖥️ Interactive TUI Dashboard

* Clean terminal-based interface
* Real-time status updates
* Action-driven workflow:
  * Forensic Scan
  * Live Monitoring
  * Hybrid Mode

---

## 🧠 How It Works

```text
Logs → Parsing → Normalization → Timeline Reconstruction
     → Gap Detection → Severity Scoring → User Output
```

### Step-by-step:

1. Extract timestamps from logs
2. Convert to a standard format
3. Sort chronologically
4. Compute time differences between entries
5. Flag anomalies based on thresholds
6. Display results with explanations

---

## 🧪 Modes of Operation

### 1. Forensic Scan

* Full analysis of existing log files
* Identifies historical anomalies

### 2. Live Monitor

* Continuously monitors logs (streaming/tail mode)
* Detects gaps in real time

### 3. Hybrid Mode

* Combines historical scan + live monitoring

---

## 📸 Sample Output

```text
🤖 EVI
"Starting forensic scan..."

• Parsing timestamps...
• Checking sequence...
⚠ Gap detected: 7 minutes

Result: CRITICAL

"This gap may indicate deleted or tampered logs."
```

---

## 🛠️ Tech Stack

* **Python** — Core logic
* **Rich (TUI library)** — Terminal UI dashboard
* **Datetime / Parsing utilities** — Timestamp handling

---

## 📦 Installation

```bash
git clone https://github.com/21amY26/EVI.git
cd evi-evidence-inspector
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python3 main.py
```

### Menu Options:

```
1. Forensic Scan
2. Live Monitor
3. Hybrid MoDE
4. Help
0. Exit
```

---

## 📊 Use Cases

* 🔐 Cybersecurity investigations
* 🕵️ Digital forensics
* 🏢 Insider threat detection
* 📋 Compliance auditing
* 🚨 Incident response

---

## ⚠️ Limitations

* Assumes timestamp integrity within remaining logs
* Does not yet correlate across distributed systems
* Requires structured or semi-structured logs

---

## 🔮 Future Improvements

* Multi-system correlation
* Machine learning anomaly detection
* Visualization dashboard (web-based)
* Integration with SIEM tools
* Voice-enabled EVI assistant

---

## 👥 Team

* **Kasmya Bhatia**
* **Amisha Singh**
* **Ashwarya Pradhan**

---

## 📜 License

MIT License

---

## 💬 Final Note

> Logs tell stories.
> EVI finds the missing chapters.
