# ROBOGUARD AI — Honest System Limitations & Engineering Roadmap

---

## 1. Technical Scope & Boundaries

In accordance with strict engineering integrity and the MASTER ENGINEERING DIRECTIVE, ROBOGUARD AI explicitly documents its current architectural scope and limitations:

### 1. Static vs Dynamic Runtime Analysis
- **Current Capability:** ROBOGUARD AI excels at deep static and post-mortem analysis of ROS 2 console logs, Colcon build logs, structured JSON topology exports, YAML launch configurations, and DDS XML governance profiles.
- **Limitation:** In offline mode, the system does not attach live pcap packet sniffers or dynamically inject DDS discovery probes into running hardware without user-supplied exports.

### 2. QoS Policy Evaluation Scope
- **Current Capability:** Evaluates fundamental DDS QoS policies: Reliability (`BEST_EFFORT` vs `RELIABLE`), Durability (`VOLATILE` vs `TRANSIENT_LOCAL`), and History/Depth.
- **Limitation:** Complex time-based QoS policies (such as `LIVELINESS_LEASE_DURATION`, `DEADLINE`, and `LIFESPAN`) are evaluated when explicitly present in diagnostic dumps, but cannot be inferred from raw logs that omit timing metadata.

### 3. Coordinate Frame (TF2) Kinematics
- **Current Capability:** Analyzes transform tree connectivity, topological root frames, leaf node reachability, and REP-105 standard frame hierarchies.
- **Limitation:** Kinematic singularity detection (e.g. Gimbal lock in Euler angles, robot arm joint limits, or numerical quaternion drift) requires continuous live joint state trajectory streaming.

### 4. SROS2 Hardware Cryptography
- **Current Capability:** Audits SROS2 environment variables, keystore paths, DDS XML governance policies, and permissions scopes.
- **Limitation:** Does not assess physical Hardware Security Modules (HSMs), TPM 2.0 chips, or side-channel physical bus tapping (e.g. CAN bus or SPI sniffing).

### 5. AI Copilot Advisory Boundary
- **Current Capability:** The BharatCode AI Copilot generates deeply grounded, evidence-backed explanations and verified ROS 2 CLI commands.
- **Limitation:** AI-generated troubleshooting runbooks are advisory. Robotic physical systems can cause physical harm; human engineer review is strictly required before executing actuation commands on live physical robots.

---

## 2. Engineering Roadmap

- **Phase 2.0 (Post-Hackathon):** Live ROS 2 daemon integration via `rclpy` subscription hooks to ingest active graph topology on live robots.
- **Phase 2.1:** Automated SROS2 enclave generation wizard with interactive certificate generation and XML policy visual editor.
- **Phase 2.2:** Real-time micro-ROS and embedded MCU diagnostic bridge for sensor nodes (STM32, ESP32).
