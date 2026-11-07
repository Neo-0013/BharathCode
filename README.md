# ROBOGUARD AI 🛡️
### Explainable ROS 2 Diagnostics & Robotics Cybersecurity Copilot
*Official Submission for the BharatCode Build League 2026*

[![ROS 2](https://img.shields.io/badge/ROS%202-Jazzy%20Jalisco-326CE5?style=flat-square&logo=ros)](https://docs.ros.org/en/jazzy/)
[![BharatCode](https://img.shields.io/badge/BharatCode-Model%20API-00E5FF?style=flat-square)](https://bharatcode.ai/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Tests](https://img.shields.io/badge/Tests-28%2F28%20Passing-10B981?style=flat-square)](tests/)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange?style=flat-square)](LICENSE)

> **"Understand your robot. Diagnose its failures. Strengthen its security."**

---

## 1. Project Introduction

**ROBOGUARD AI** is an intelligent, commercial-grade engineering diagnostics and defensive cybersecurity platform for autonomous mobile robots (AMRs), robotic manipulators, and autonomous systems running **ROS 2 Jazzy**.

ROBOGUARD AI introduces a **Dual-Engine Reasoning Architecture**:
1. **Deterministic Engineering Engine:** Mathematical QoS compatibility matrices, acyclic TF2 coordinate transform tree validation, log regex error signature parsing, and SROS2/DDS XML security auditing.
2. **Explainable AI Copilot:** Powered by the official **BharatCode Model API** (`deepseek-v4.1-flash` and `qwen-3.8-27b`), transforming cryptic DDS errors and stack traces into grounded, evidence-backed root cause explanations and copy-pasteable ROS 2 verification runbooks.

---

## 2. Problem Statement

Autonomous robotics software is notoriously complex and fragile:
- **Silent QoS Mismatches:** ROS 2 DDS middleware silently drops messages when publisher and subscriber Quality of Service (QoS) policies disagree (e.g., Best Effort publisher offering data to a Reliable subscriber), leaving robot navigation blind without clear error messages.
- **Coordinate Frame Disconnections:** In autonomous mobile robots (REP-105), a missing transform in the TF tree (`map` ➔ `odom` ➔ `base_link`) triggers `LookupException` and `ExtrapolationException`, halting motion planners.
- **Critical Cybersecurity Exposure:** Default ROS 2 deployments communicate via unencrypted, unauthenticated UDP multicast (`ROS_SECURITY_ENABLE=false`, Domain 0). Anyone on the local Wi-Fi can eavesdrop on sensor streams or inject malicious velocity commands (`/cmd_vel`).
- **High Cognitive Burden:** Engineers spend hours manually combing through gigabytes of unstructured logs and juggling fragmented CLI tools (`ros2 doctor`, `tf2_tools`, `rqt_graph`).

---

## 3. The ROBOGUARD AI Solution

ROBOGUARD AI bridges the gap between low-level middleware telemetry and high-level engineering decisions:
- **Evidence-Based:** Deterministic checks establish empirical facts first; the AI never hallucinates measurements or unverified outcomes.
- **Enterprise Dark-First UI:** Inspired by leading observability dashboards (Datadog/Grafana) and Linear ergonomics, featuring telemetry stat strips, interactive topology graphs, and collapsible detail drawers.
- **100% Offline-Resilient:** Fully operational in air-gapped robotics facilities; when cloud connectivity is unavailable, the deterministic explanation engine provides comprehensive local troubleshooting runbooks.

---

## 4. Key Capabilities

- **Multi-Format Ingestion:** Accepts uploaded ROS 2 console logs (`.log`, `.txt`), pasted terminal logs, JSON diagnostic dumps, YAML launch parameters, and DDS XML security profiles.
- **DDS QoS Compatibility Engine:** Evaluates Reliability, Durability, and Depth compatibility with full violation explanations.
- **TF2 Coordinate Validator:** Identifies disconnected coordinate trees, multiple roots, and REP-105 standard frame absence (`base_link`).
- **Node & Topic Architecture Audit:** Flags unconsumed critical topics (`/cmd_vel` with 0 subscribers), starved subscribers, and inactive lifecycle nodes.
- **Defensive SROS2 Security Center:** Audits keystores, `ROS_SECURITY_ENABLE`, `ROS_SECURITY_STRATEGY`, and inspects DDS XML governance for unauthenticated participants and wildcard topic permissions.
- **Interactive ROS Graph Explorer:** NetworkX & Plotly directed graph visualization highlighting nodes, topics, isolated subgraphs, and QoS error edges.
- **Automated Engineering Reports:** One-click generation of Markdown runbooks and publication-grade PDF audit reports via ReportLab.

---

## 5. Technology Stack

- **Primary Language:** Python 3.12
- **Application Framework:** Streamlit (customized with token-based anti-AI-slop CSS)
- **AI Integration:** BharatCode Model API (`deepseek-v4.1-flash`, `qwen-3.8-27b`)
- **Graph & Visualization:** NetworkX 3.7, Plotly 7.1.0
- **Data & Config Processing:** PyYAML 6.0.1, Pandas 3.1.1, JSON, Regex
- **Report Generation:** ReportLab 5.0.1 (PDF compilation) & Markdown
- **Testing & Verification:** Pytest 7.4.4 (28/28 unit and integration tests passing)
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
└──────────────────────┬───────────────────────┘
                       │ (Structured Findings & Evidence)
                       ▼
┌──────────────────────────────────────────────┐
│           AI Copilot & Guardrails            │
│  - BharatCode Client (deepseek-v4.1-flash)   │
│  - ResponseValidator (Blocks unsafe cmds)    │
│  - Deterministic Offline Fallback            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        Presentation & Reporting Layer         │
│  - Command Center & Telemetry Stat Strips    │
│  - Diagnostics Workspace & Detail Drawers    │
│  - Cybersecurity Center (Transparent Score)  │
│  - Interactive Plotly Topology Explorer      │
│  - Markdown & ReportLab PDF Export           │
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

### Step 3: Configure Environment Variables (Optional)
```bash
cp .env.example .env
# Edit .env to add your BHARATCODE_API_KEY
# If left empty, ROBOGUARD AI automatically runs in 100% Deterministic Offline Mode!
```

### Step 4: Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 8. Built-in Demonstration Scenarios

ROBOGUARD AI includes **5 pre-configured synthetic demonstration scenarios** for hackathon judges and robotics developers:

1. **Scenario 1:** Missing ROS 2 Topic & Unconsumed `/cmd_vel` Actuation (Nav2 AGV failure).
2. **Scenario 2:** Nav2 & Perception QoS Incompatibility (Reliability and Durability mismatches).
3. **Scenario 3:** SLAM Disconnected TF2 Coordinate Tree & Extrapolation Exception.
4. **Scenario 4:** Colcon Workspace Build Failure & Missing Python Dependencies.
5. **Scenario 5:** Insecure Robotic Fleet Configuration (Unencrypted DDS multicast & permissive SROS2 governance).

*To launch any scenario, navigate to the **Command Center** and click **Load & Analyze**.*

---

## 9. Automated Testing Suite

ROBOGUARD AI includes a comprehensive Pytest test suite covering log parsing, QoS matrices, TF validation, cybersecurity posture scoring, and report generation:

```bash
python3 -m pytest -v tests/
```

**Results:**
```text
============================== 28 passed in 0.82s ==============================
```

---

## 10. Security & Privacy

- **Safe Local Analysis:** Log parsing and security evaluation occur strictly on your local machine.
- **Zero Hardcoded Secrets:** Credentials are read from `BHARATCODE_API_KEY` or stored in volatile session memory.
- **Safety Guardrails:** All AI Copilot responses pass through a strict `ResponseValidator` that blocks dangerous shell commands (`rm -rf`, raw socket floods) and ensures suggested troubleshooting commands adhere to standard ROS 2 CLI tools.
- **Air-Gapped Capable:** Fully functional without internet connectivity or API keys.

---

## 11. Competition Verification

In compliance with the **BharatCode Build League 2026** submission guidelines:
- `BharatCode.txt` is located in the repository root directory.
- Model API client directly integrates with `https://bharatcode.ai/api/model/v1` supporting `deepseek-v4.1-flash` and `qwen-3.8-27b`.
- Tested and verified on **ROS 2 Jazzy Jalisco**.

---

## 12. License & Acknowledgements

Developed for the **BharatCode Build League 2026**.  
Licensed under the Apache License 2.0.
