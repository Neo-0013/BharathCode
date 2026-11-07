# Explainable ROS 2 Diagnostics & Robotics Cybersecurity: A Research & Engineering Report
**ROBOGUARD AI — Autonomous Engineering Copilot**
*BharatCode Build League 2026*

---

## 1. Executive Summary & Problem Formulation

Modern autonomous mobile robots (AMRs), self-driving vehicles, and industrial manipulators rely heavily on the **Robot Operating System 2 (ROS 2)**, with **ROS 2 Jazzy Jalisco** serving as the premier Long-Term Support (LTS) distribution. ROS 2 builds upon the **Data Distribution Service (DDS)** standard for decentralized, real-time publish-subscribe communication.

While DDS delivers remarkable modularity and deterministic transport, it introduces profound engineering complexities:
1. **Silent Communication Failures via QoS Incompatibilities:** DDS enforces mathematical compatibility laws across endpoints (e.g., Reliability, Durability, Liveliness). When a subscriber requests `RELIABLE` delivery from a publisher offering `BEST_EFFORT`, the middleware negotiates an incompatible match and silently discards messages without throwing fatal runtime exceptions in the subscriber application.
2. **Coordinate Tree (TF2) Divergence & Latency Skew:** Coordinate transformations governed by **REP-105** must form a continuous, acyclic tree connecting sensor frames (`laser_frame`, `camera_optical_frame`) to robot reference frames (`base_link`, `odom`, `map`). Clock skew across distributed compute nodes or missing transform publishers cause `LookupException` and `ExtrapolationException`, halting navigation and trajectory planning.
3. **Cybersecurity Blindspots in Default DDS Deployments:** By default, standard ROS 2 communicates over unencrypted, unauthenticated UDP multicast (`ROS_DOMAIN_ID=0`, `ROS_SECURITY_ENABLE=false`). Any unauthenticated device on the local network or shared Wi-Fi can passively sniff telemetry, inject false actuation velocity (`/cmd_vel`), or trigger denial-of-service through discovery amplification.
4. **Fragmented and High-Cognitive-Load Tooling:** Robotics developers are forced to juggle disparate CLI tools (`ros2 doctor`, `ros2 topic info -v`, `rqt_graph`, `tf2_tools`, `wireshark`). Manual log inspection across dozens of asynchronous nodes is error-prone, slow, and inaccessible to junior engineers.

**ROBOGUARD AI** was engineered to resolve these challenges by introducing a **Dual-Engine Reasoning Architecture**: deterministic, rule-based verification combined with an explainable AI Copilot powered by the **BharatCode Model API** (`deepseek-v4.1-flash` and `qwen-3.8-27b`).

---

## 2. Evaluation of Existing Diagnostic Approaches

| Tool / Approach | Primary Focus | Deterministic Verification | SROS2 Security Audit | Explainable Root-Cause Guidance | Unified Observability UI |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `ros2 doctor` | Basic environment & network sanity | Partial | ❌ No | ❌ No | ❌ Terminal only |
| `rqt_graph` | Visualizing node/topic connections | ❌ Graph only | ❌ No | ❌ No | Desktop Qt |
| `rqt_console` | Filtering log severity | ❌ Raw logs | ❌ No | ❌ No | Desktop Qt |
| Standard LLM Chatbots | Generic text assistance | ❌ Prone to Hallucination | ❌ No | ⚠️ Unverified | Generic Chat |
| **ROBOGUARD AI** | **Comprehensive Diagnostics & SROS2 Security** | **✅ Formal Verification** | **✅ Comprehensive Audit** | **✅ Grounded BharatCode Copilot** | **✅ Modern Observability UI** |

---

## 3. The Dual-Engine Reasoning Paradigm

A core philosophical tenet of ROBOGUARD AI is that **AI models must never replace empirical engineering evidence**:

```
[Raw ROS 2 Logs / Topics / QoS / SROS2 Enclaves]
                     │
                     ▼
       ┌───────────────────────────┐
       │   Deterministic Engine    │
       │   - Exact Regex Matching  │
       │   - Formal QoS Matrices   │
       │   - TF2 Tree Topology     │
       │   - SROS2 XML Auditing    │
       └─────────────┬─────────────┘
                     │ (Extracted Evidence & Finding IDs)
                     ▼
       ┌───────────────────────────┐
       │     AI Copilot Layer      │
       │   (BharatCode Model API)  │
       │   - Grounded Explanations │
       │   - Root Cause Hierarchy  │
       │   - Safety Guardrails     │
       └─────────────┬─────────────┘
                     │
                     ▼
        [Actionable Verified Runbook]
```

### Deterministic Rule Engine
The deterministic engine evaluates inputs against official ROS 2 Jazzy and DDS Security specifications:
- **QoS Compatibility Law:** Implements the partial order:
  $$\text{Offered}(\text{Policy}) \ge \text{Requested}(\text{Policy})$$
  Ensuring that violations in Reliability (`BEST_EFFORT` pub vs `RELIABLE` sub) and Durability (`VOLATILE` pub vs `TRANSIENT_LOCAL` sub) are detected with mathematical certainty.
- **TF2 Acyclic Graph Verification:** Parses parent-child frame relationships, detecting disjoint subgraphs, disconnected roots, and absence of REP-105 canonical frames (`base_link`).
- **Defensive SROS2 Audit:** Checks for unauthenticated DDS access (`<allow_unauthenticated_participants>true</allow_unauthenticated_participants>`), wildcard permissions (`<topic>*</topic>`), and unencrypted discovery ranges.

### BharatCode AI Copilot Engine
Once empirical facts are established, the AI copilot interprets the findings for human engineers:
- **Multi-Level Explanations:** Adapts explanations for junior robotics students (plain-English conceptual breakdown) and principal systems architects (DDS RTPS protocol dynamics).
- **Safety Guardrails (`ResponseValidator`):** Intercepts dangerous generated commands (e.g. `rm -rf`, raw socket floods) and ensures all suggested remediation steps use validated ROS 2 CLI commands (`ros2 topic info`, `ros2 lifecycle set`, `ros2 run tf2_tools view_frames`).
- **Resilient Offline Fallback:** When network connectivity is severed or API credentials are unavailable, ROBOGUARD AI executes an internal rule-based synthesis engine, maintaining 100% operational utility in air-gapped robotics test environments.

---

## 4. Robotics Cybersecurity Architecture (SROS2 & DDS Security)

Robotics systems operate at the physical-digital boundary: a software defect or security compromise directly risks physical collisions, property destruction, or human injury.

### SROS2 Defensive Architecture
ROBOGUARD AI implements checks aligned with the **OMG DDS Security Specification v1.1**:
1. **Authentication:** Enforces X.509 Public Key Infrastructure (PKI) where each node enclave possesses a signed certificate and private key.
2. **Access Control (Governance & Permissions):** Validates that `governance.xml` requires authenticated participants and encrypts discovery metadata, while `permissions.xml` explicitly restricts topic publication and subscription without wildcard authorizations.
3. **Cryptographic Integrity & Confidentiality:** Validates AES-GCM (128/256-bit) encryption of real-time telemetry payloads.
4. **Network Exposure Isolation:** Audits `ROS_DOMAIN_ID` and `ROS_AUTOMATIC_DISCOVERY_RANGE`, penalizing deployments that broadcast unsegmented Simple Participant Discovery Protocol (SPDP) packets over shared corporate subnets.

---

## 5. References & Authoritative Sources

1. **Open Source Robotics Foundation (OSRF):** *ROS 2 Documentation (Jazzy Jalisco Release)*, 2024. https://docs.ros.org/en/jazzy/
2. **Object Management Group (OMG):** *DDS Security Specification, Version 1.1*, formal/2018-04-01.
3. **ROS Enhancement Proposal (REP) 105:** *Coordinate Frames for Mobile Platforms*, Foote, T., 2010.
4. **ROS Enhancement Proposal (REP) 2004:** *Package Quality Categories*, Woodall, W. et al., 2020.
5. **SROS2 Documentation:** *Secure Robot Operating System 2 Integration Guide*, Canonical & Open Robotics, 2024.
6. **BharatCode AI Documentation:** *BharatCode Model API Specification v1 (`deepseek-v4.1-flash`, `qwen-3.8-27b`)*, 2026. https://bharatcode.ai/
7. **Maruyama, Y., Kato, S., & Azumi, T.:** *Exploring the performance of ROS2*, IEEE International Conference on Embedded Software and Systems (ICESS), 2016.
8. **Dieber, B. et al.:** *Penetration testing ROS*, International Conference on Simulation, Modeling, and Programming for Autonomous Robots (SIMPAR), 2016.
