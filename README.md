# ROBOGUARD AI 🛡️
### Explainable ROS 2 Diagnostics & Robotics Cybersecurity Copilot
*Official Submission for the BharatCode Build League 2026*

[![ROS 2](https://img.shields.io/badge/ROS%202-Jazzy%20Jalisco-326CE5?style=flat-square&logo=ros)](https://docs.ros.org/en/jazzy/)
[![AI Providers](https://img.shields.io/badge/AI%20Providers-Ollama%20%7C%20Gemini%20%7C%20BharatCode-00E5FF?style=flat-square)](config/settings.py)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Server-FastAPI%20ASGI-009688?style=flat-square&logo=fastapi)](server.py)
[![Tests](https://img.shields.io/badge/Tests-67%2F67%20Passing-10B981?style=flat-square)](tests/)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange?style=flat-square)](LICENSE)

> **"Understand your robot. Diagnose its failures. Strengthen its security."**

---

## 🆕 Final Release Notes (v2.0 — Final Submission Build)

- **Unified Single Server Architecture**: Hero storytelling landing page and the complete Cyber-Physical Robotics SOC Dashboard are served on a single, lightning-fast ASGI server (`python3 run_platform.py` on port 8000) with sub-10ms response times and zero-friction navigation.
- **Executive SOC Dashboard Overhaul**: Completely remade into 5 clean executive tabs:
  1. 📊 **3D Twin & Overview** (Interactive Three.js WebGL AMR Rover with Mecanum wheels, spinning LiDAR, camera views, attack vector simulator, and real-time enforcer console).
  2. 🕸️ **ROS 2 Computational Graph** (Interactive SVG topological network with zoom in/out/recenter, incompatible edge filter, and 1-click eBPF rogue socket isolation).
  3. 📈 **DDS Telemetry & Topic Burst Heatmap** (RTPS wire throughput waveform, network jitter, packet loss, spectral burst matrix, dynamic rate limiter slider, and incident MCAP rosbag dump).
  4. 🚨 **Fleet Incident Horizon** (Predictive contagion timeline from T-25m to T+15m, blast radius impact, and multi-rover isolation controls for AMR-01 through AMR-04).
  5. 🛠️ **Deterministic Findings & Git Patches** (Inline code diffs for `SEC-SROS2-001` and `QOS-REL-001` with 1-click apply and posture upgrade to 95%).
- **Live AI Security Sentinel**: Autonomous defense copilot drawer (`/api/ai/chat`) with multi-provider intelligence (BharatCode, Ollama, Gemini, and deterministic offline runbooks). Automatically detects active cyberattacks and presents proactive alert toasts with 1-click auto-isolation.
- **100% Working Interactive Controls**: Every single button (43/43) is fully wired with real reactive JavaScript state and live backend API sync.
- **Fully Offline Compliant**: All 3D and UI engines (`three.min.js`, `OrbitControls.js`, `gsap.min.js`, `tailwindcss.js`) are 100% vendored with zero external CDN dependencies.
- **Automated Verification**: **67 passing tests** (`67 passed in 8.99s`).

---

## 1. Project Introduction

**ROBOGUARD AI** is an intelligent, commercial-grade engineering diagnostics, auto-remediation, and defensive cybersecurity platform for autonomous mobile robots (AMRs), robotic manipulators, and autonomous systems running **ROS 2 Jazzy**.

ROBOGUARD AI introduces a **Dual-Engine Reasoning Architecture**:
1. **Deterministic Engineering Engine:** Mathematical OMG DDS v1.4 QoS compatibility matrices, acyclic TF2 coordinate transform tree validation against REP-105, log regex error signature parsing, and SROS2/DDS XML security auditing.
2. **Explainable AI Copilot:** Multi-provider architecture powered by **Local Ollama** (zero-cost / private `qwen2.5-coder:3b`), **Google Gemini API**, and the official **BharatCode Model API** (`deepseek-v4.1-flash` and `qwen-3.8-27b`), transforming cryptic DDS errors and stack traces into grounded, evidence-backed root cause explanations and copy-pasteable ROS 2 verification runbooks.

---

## 2. Problem Statement

Autonomous robotics software is notoriously complex and fragile:
- **Silent QoS Mismatches:** ROS 2 DDS middleware silently drops messages when publisher and subscriber Quality of Service (QoS) policies disagree (e.g., Best Effort publisher offering data to a Reliable subscriber), leaving robot navigation blind without clear error messages.
- **Coordinate Frame Disconnections:** In autonomous mobile robots (REP-105), a missing transform in the TF tree (`map` ➔ `odom` ➔ `base_link`) triggers `LookupException` and `ExtrapolationException`, halting motion planners.
- **Critical Cybersecurity Exposure:** Default ROS 2 deployments communicate via unencrypted, unauthenticated UDP multicast (`ROS_SECURITY_ENABLE=false`, Domain 0). Anyone on the local network can eavesdrop on sensor streams or inject malicious velocity commands (`/cmd_vel`).
- **High Cognitive Burden:** Engineers spend hours manually combing through gigabytes of unstructured logs and juggling fragmented CLI tools (`ros2 doctor`, `tf2_tools`, `rqt_graph`).

---

## 3. The ROBOGUARD AI Solution

ROBOGUARD AI bridges the gap between low-level middleware telemetry and high-level engineering decisions:
- **Evidence-Based:** Deterministic checks establish empirical facts first; the AI never hallucinates measurements or unverified outcomes.
- **1-Click Auto-Fix Git Patches:** Generates real unified diffs (`--- a/ +++ b/`) with a 1-click download button (`.patch`) ready for immediate `git apply`.
- **Interactive Attack Surface Simulator:** Simulates real-world cyberattacks (e.g. Rogue `/cmd_vel` injection, LiDAR spoofing) comparing Insecure ROS 2 vs Hardened SROS2 enclaves in real time.
- **eBPF Kernel Socket Clamping:** Enforces kernel-level rule #4092 to isolate unauthenticated remote RTPS GUIDs on Domain 0 before malicious payloads reach the middleware stack.
- **100% Offline-Resilient:** Operates seamlessly in air-gapped robotics facilities; when cloud connectivity is unavailable, Local Ollama or the deterministic offline runbook engine ensures zero downtime.

---

## 4. Key Capabilities & Winning Features

- **Multi-Format Ingestion:** Accepts uploaded ROS 2 console logs (`.log`, `.txt`), pasted terminal logs, JSON diagnostic dumps, YAML launch parameters, and DDS XML security profiles.
- **DDS QoS Compatibility Engine:** Evaluates Reliability, Durability, and Depth compatibility with full violation explanations based on OMG DDS specifications.
- **Plotly TF2 Coordinate Validator:** Identifies disconnected coordinate trees, multiple roots, and REP-105 standard frame absence (`base_link`), rendering interactive trees.
- **1-Click Auto-Fix Patch Generator:** Instant generation and download of Git patches for QoS parameters, TF2 static broadcasters, SROS2 governance XML, and Python dependencies.
- **Interactive Attack Surface Simulator:** Simulates Rogue `/cmd_vel` injection at 42Hz, synthetic point-cloud phantom clusters, and DDS UDP multicast storms with 3D physics feedback.
- **Defensive SROS2 Security Center:** Audits keystores, `ROS_SECURITY_ENABLE`, `ROS_SECURITY_STRATEGY`, and inspects DDS XML governance for unauthenticated participants and wildcard topic permissions.
- **Interactive ROS Graph Explorer:** NetworkX directed graph visualization highlighting nodes, topics, isolated subgraphs, and QoS error edges.
- **Automated Engineering Reports:** One-click generation of Markdown runbooks, publication-grade PDF audit reports via ReportLab, and standalone offline HTML bundles.

---

## 5. Technology Stack

- **Primary Language:** Python 3.12
- **Unified Server:** FastAPI / Uvicorn ASGI (sub-10ms response time)
- **Secondary Workspace:** Streamlit (customized with high-contrast Linear dark-mode CSS tokens)
- **AI Integration:** Multi-provider engine supporting Local Ollama (`qwen2.5-coder:3b`), Google Gemini (`gemini-1.5-flash`), and BharatCode (`deepseek-v4.1-flash`, `qwen-3.8-27b`)
- **3D & Animation:** Three.js r128, OrbitControls, GreenSock GSAP 3.12 (100% vendored offline)
- **Styling:** Tailwind CSS (vendored in `assets/vendor/tailwindcss.js`)
- **Graph & Visualization:** NetworkX 3.7, Plotly 7.1.0
- **Data & Config Processing:** PyYAML 6.0.1, Pandas 3.1.1, JSON, Regex
- **Report Generation:** ReportLab 5.0.1 (PDF compilation) & Markdown
- **Testing & Verification:** Pytest 7.4.4 (**67/67 unit and integration tests passing**)
- **Robotics Target:** ROS 2 Jazzy Jalisco (DDS / SROS2 / REP-105)

---

## 6. Architecture & Workflow

```
[ROS 2 Logs / JSON Dumps / DDS XML]
               │
               ▼
┌──────────────────────────────────────────────┐
│       Deterministic Diagnostic Engine        │
│  - LogParser (Regex signature matcher)       │
│  - QoSAnalyzer (Offered >= Requested matrix) │
│  - TFAnalyzer (REP-105 frame acyclic tree)   │
│  - SecurityEngine (SROS2 & DDS XML audit)    │
│  - PatchGenerator (Unified Git diffs)        │
└──────────────────────┬───────────────────────┘
                       │ (Structured Findings & Evidence)
                       ▼
┌──────────────────────────────────────────────┐
│       AI Sentinel Copilot & Guardrails       │
│  - Multi-Provider (Ollama / Gemini / BC)     │
│  - ResponseValidator (Blocks unsafe cmds)    │
│  - Proactive Intrusion Alert Trigger         │
│  - Deterministic Offline Fallback            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        Unified Presentation Layer            │
│  - Storytelling Hero (/ on port 8000)        │
│  - Executive 3D Robotics SOC (/soc)          │
│  - Three.js WebGL AMR Rover Digital Twin     │
│  - SVG Computational Graph & eBPF Clamping   │
│  - DDS Burst Heatmap & MCAP Bag Dump         │
│  - 1-Click Git Patch Application Studio      │
│  - Standalone Offline HTML & PDF Exports     │
└──────────────────────────────────────────────┘
```

---

## 7. Installation & Quickstart

### Prerequisites
- Linux / macOS / Windows with Python 3.10+ (Python 3.12 recommended)
- `git`

### Step 1: Clone the Repository
```bash
git clone https://github.com/<your-username>/BharathCode.git
cd BharathCode
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure AI Provider (Optional)
```bash
cp .env.example .env
# Option A: Local Ollama (Recommended — 100% Free & Private)
# Pre-installed Ollama on localhost:11434 with qwen2.5-coder:3b works instantly!

# Option B: Google Gemini API (Free Tier)
# export GEMINI_API_KEY="your-gemini-key"

# Option C: BharatCode API
# export BHARATCODE_API_KEY="your-bharatcode-key"
```

### Step 4: Run the Platform (Recommended Single Command)
```bash
python3 run_platform.py
```
This starts the unified server at `http://localhost:8000` and automatically opens your browser:
- **Hero Landing Page:** `http://localhost:8000/`
- **SOC Operations Dashboard:** `http://localhost:8000/soc`

*(Optional: to start the secondary Streamlit workspace concurrently, run `python3 run_platform.py --with-streamlit`)*

---

## 8. Built-in Demonstration Scenarios

ROBOGUARD AI includes **5 pre-configured synthetic demonstration scenarios** for hackathon judges and robotics developers:

1. **Scenario 1:** Baseline Zero-Trust Fleet (Strict SROS2 PKCS#11 keys, matched QoS contracts, 96% security score).
2. **Scenario 2:** SROS2 Keystore Drift (Governance XML out of sync causing authorization rejections).
3. **Scenario 3:** DDS Multicast Storm (Unbounded UDP multicast packet saturation on Domain 0).
4. **Scenario 4:** LiDAR Sensor Tampering (Spoofed point cloud phantom cluster inflating Nav2 costmaps).
5. **Scenario 5:** Insecure AMR Navigation Fleet (Active rogue `/cmd_vel` injection from unauthenticated remote GUID, QoS reliability mismatch).

*To switch scenarios, use the top executive dropdown in the SOC Dashboard or call `POST /api/scenarios/:id`.*

---

## 9. Automated Testing Suite

ROBOGUARD AI includes a comprehensive Pytest test suite covering log parsing, QoS matrices, TF validation, cybersecurity posture scoring, patch generation, asset loading, and server routes:

```bash
python3 -m pytest -v tests/
```

**Results:**
```text
============================== 67 passed in 8.99s ==============================
```

---

## 10. Security & Privacy

- **Safe Local Analysis:** Log parsing and security evaluation occur strictly on your local machine.
- **Zero Hardcoded Secrets:** Credentials are read from environment variables or stored in volatile session memory.
- **Safety Guardrails:** All AI Copilot responses pass through a strict `ResponseValidator` that blocks dangerous shell commands (`rm -rf`, raw socket floods) and ensures suggested troubleshooting commands adhere to standard ROS 2 CLI tools.
- **Air-Gapped Capable:** Fully functional without internet connectivity or external API keys.

---

## 11. Competition Verification

In compliance with the **BharatCode Build League 2026** submission guidelines:
- `BharatCode.txt` is located in the repository root directory.
- Model API client directly integrates with `https://bharatcode.ai/api/model/v1` supporting `deepseek-v4.1-flash` and `qwen-3.8-27b`, with seamless multi-provider fallbacks to Local Ollama and Google Gemini.
- Tested and verified on **ROS 2 Jazzy Jalisco**.

---

## 12. License & Acknowledgements

Developed for the **BharatCode Build League 2026**.  
Licensed under the Apache License 2.0.
