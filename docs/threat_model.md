# ROBOGUARD AI — Robotics Threat Model Specification
**Defensive Security Analysis of Autonomous Mobile Robots Running ROS 2 Jazzy**

---

## 1. System Overview & Trust Boundaries

Robotics systems operate in physical environments where cyber compromises directly translate into physical kinetic hazards. The following diagram delineates the primary trust boundaries in a modern ROS 2 autonomous robot:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Cloud / Remote Fleet Management (HTTPS / TLS 1.3)                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [Trust Boundary 1: Fleet WAN]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ External Local Network / Facility Wi-Fi (UDP Multicast 239.255.0.1)    │
│ [Attack Surface: Eavesdropping, SPDP Flooding, Rogue Node Injection]   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [Trust Boundary 2: Robot Onboard LAN]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Onboard Compute (SROS2 Enclaves & Linux Host Permissions)              │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │  High-Privilege Actuation & Navigation Enclaves                    │ │
│ │  - /controller_server, /diff_drive_controller (/cmd_vel)          │ │
│ └─────────────────────────────────┬──────────────────────────────────┘ │
│                                   │ [Trust Boundary 3: Enclave Boundary]
│ ┌─────────────────────────────────┴──────────────────────────────────┐ │
│ │  Low-Privilege Sensors & Diagnostic Enclaves                       │ │
│ │  - /camera_driver, /diagnostics_aggregator                         │ │
│ └────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. STRIDE Threat Analysis Matrix

| STRIDE Category | Specific Robotics Vulnerability in ROS 2 | Real-World Impact | ROBOGUARD AI Detection Rule | SROS2 Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| **Spoofing** | Attacker connects unauthenticated node to Domain 0 and publishes false velocity commands to `/cmd_vel`. | Autonomous robot crashes into facility walls or personnel. | `ROBO-SEC-001`<br>`ROBO-SEC-005` | Enable `ROS_SECURITY_ENABLE=true` and enforce X.509 certificate validation. |
| **Tampering** | Man-in-the-Middle (MitM) alters unauthenticated LaserScan distance fields in transit over Wi-Fi. | Obstacle avoidance algorithm fails; robot runs over dropped cargo. | `ROBO-SEC-001` | Enforce AES-GCM-256 cryptographic payload integrity in DDS governance. |
| **Repudiation** | Malicious command injected without cryptographic signatures; standard `rosout` lacks audit trails. | Inability to establish post-incident forensic liability after an industrial accident. | `ROBO-SEC-002` | Enforce SROS2 signed digital certificates per node enclave. |
| **Information Disclosure** | Plaintext DDS discovery packets expose camera feeds, SLAM maps, and facility layouts. | Corporate espionage; unauthorized mapping of secure warehouse layout. | `ROBO-SEC-004`<br>`ROBO-SEC-007` | Enable `<discovery_protection>ENCRYPT</discovery_protection>` and restrict discovery range. |
| **Denial of Service** | Flooding UDP multicast discovery port (7400) with malformed SPDP participant packets. | Real-time control loops miss deadlines; watchdog activates emergency stop. | `ROBO-SEC-003`<br>`ROBO-SEC-004` | Set `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` or configure unicast initial peers. |
| **Elevation of Privilege** | Low-privilege diagnostic node granted wildcard `<topic>*</topic>` permission policy. | Exploited diagnostics logger issues emergency stop overrides or disables safety gates. | `ROBO-SEC-006` | Enforce strict topic namespaces in `permissions.xml` without wildcards. |

---

## 3. Defense-in-Depth Verification Checklist

1. [x] **DDS Cryptographic Enclaves:** Each executable runs under an individual SROS2 enclave signed by the system Certificate Authority (CA).
2. [x] **Fail-Closed Security Strategy:** `ROS_SECURITY_STRATEGY=Enforce` is configured, preventing fallback to unauthenticated plaintext communication.
3. [x] **Subnet Segmentation:** `ROS_DOMAIN_ID` is uniquely allocated away from the default Domain 0.
4. [x] **Discovery Boundary Hardening:** `ROS_AUTOMATIC_DISCOVERY_RANGE` is restricted to `LOCALHOST` or unicast peering.
5. [x] **Least-Privilege Topic Scoping:** Wildcards (`*`) are purged from `permissions.xml` policies.
