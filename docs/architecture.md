# ROBOGUARD AI — System Architecture Specification
**High-Fidelity Explainable ROS 2 Diagnostics & Cybersecurity Copilot**

---

## 1. Architectural Overview

ROBOGUARD AI is architected as a modular, decoupled software platform separating input parsing, deterministic verification, graph modeling, AI copilot orchestration, and presentation layers.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Ingestion Layer                                 │
│  ROS 2 Logs (.log, .txt) | JSON Dumps | YAML Configs | DDS XML Files  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Deterministic Diagnostic Core                        │
│ ┌───────────────────┐ ┌──────────────────┐ ┌─────────────────────────┐ │
│ │    LogParser      │ │   QoSAnalyzer    │ │       TFAnalyzer        │ │
│ │ (Regex Signatures)│ │(Formal Matrices) │ │   (REP-105 & Trees)     │ │
│ └─────────┬─────────┘ └────────┬─────────┘ └────────────┬────────────┘ │
│           │                    │                        │              │
│ ┌─────────┴─────────┐ ┌────────┴─────────┐ ┌────────────┴────────────┐ │
│ │   NodeAnalyzer    │ │  SecurityEngine  │ │   DiagnosticEngine      │ │
│ │(Topic Parity/Life)│ │ (SROS2 / DDS XML)│ │   (Master Aggregator)   │ │
│ └───────────────────┘ └──────────────────┘ └─────────────────────────┘ │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│   Graph & Topology Engine         │ │   AI Copilot & Guardrails Layer  │
│ - NetworkX Topology Graph         │ │ - BharatCode API (deepseek-v4.1) │
│ - Plotly Interactive Visualizer   │ │ - ResponseValidator & Grounding  │
│ - QoS Warning Edge Highlighter    │ │ - Deterministic Offline Fallback │
└─────────────────┬─────────────────┘ └──────────────────┬───────────────┘
                  │                                      │
                  └─────────────────┬────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Reporting & User Interface Layer                     │
│  - Streamlit Multi-Page Engineering Workspace (Observability Theme)    │
│  - Publication-Grade PDF Generator (ReportLab)                         │
│  - Markdown Runbook Exporter                                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Data Structures

### `DiagnosticFinding`
Standardized dictionary representation emitted by all diagnostic sub-engines:
```python
{
    "id": str,                   # e.g., "ROBO-QOS-001"
    "title": str,                # Concise human-readable finding title
    "category": str,             # DiagnosticCategory enum string
    "severity": str,             # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO"
    "status": str,               # "Confirmed" | "Suspected" | "Informational"
    "evidence": str,             # Raw verbatim snippet extracted from input
    "entities": List[str],       # Associated nodes, topics, frames, or packages
    "root_cause": str,           # Technical explanation of underlying mechanism
    "troubleshooting": List[str],# Numbered remediation steps
    "validation_commands": List[str] # Valid ROS 2 CLI commands for verification
}
```

### `SecurityPosture`
Deterministic cybersecurity posture calculation:
```python
{
    "score": float,              # 0.0 to 100.0%
    "risk_tier": str,            # "HARDENED" | "ACCEPTABLE" | "ELEVATED RISK" | "CRITICAL EXPOSURE"
    "color": str,                # Hex code for UI representation
    "total_findings": int,       # Count of detected security defects
    "assessed_controls_count": 10,
    "deductions_applied": float, # Sum of severity penalties
    "breakdown": List[dict],     # Itemized deduction ledger
    "transparency_note": str     # Explicit scoring formula statement
}
```

---

## 3. Module Responsibilities

| Module | Location | Primary Responsibility |
| :--- | :--- | :--- |
| `config.settings` | `config/settings.py` | App metadata, BharatCode API parameters, color design tokens. |
| `config.rules` | `config/rules.yaml` | Deterministic regex patterns for ROS 2 errors, QoS, and SROS2 rules. |
| `core.log_parser` | `core/log_parser.py` | Multiline log parsing, severity classification, regex signature matching. |
| `core.qos_analyzer`| `core/qos_analyzer.py`| DDS Reliability, Durability, and Depth compatibility matrix evaluation. |
| `core.tf_analyzer` | `core/tf_analyzer.py` | Coordinate frame tree analysis, disconnected roots, REP-105 compliance. |
| `core.node_analyzer`| `core/node_analyzer.py`| Node lifecycle states, unconsumed critical topics, starved subscribers. |
| `core.security_engine`| `core/security_engine.py`| SROS2 environment audit, DDS XML governance and permissions inspection. |
| `core.ros_graph` | `core/ros_graph.py` | NetworkX graph builder and Plotly dark-mode visualizer. |
| `core.report_generator`| `core/report_generator.py`| PDF and Markdown engineering report generation. |
| `ai.client` | `ai/client.py` | Official BharatCode Model API client with retries and timeout protection. |
| `ai.prompts` | `ai/prompts.py` | Evidence-grounded system and task prompt engineering. |
| `ai.response_validator`| `ai/response_validator.py`| Safety guardrail intercepting dangerous commands and validating ROS 2 CLI. |
| `ai.explanation_engine`| `ai/explanation_engine.py`| Dual-mode copilot orchestrating online AI and offline deterministic runbooks. |

---

## 4. Security & Privacy Guarantees

1. **Air-Gapped Resiliency:** When external connectivity is blocked or `force_offline` is toggled, ROBOGUARD AI executes 100% locally.
2. **Volatile Credential Handling:** API tokens are held solely in volatile session memory or read from `BHARATCODE_API_KEY`.
3. **Command Execution Safety:** ROBOGUARD AI never executes terminal commands automatically; all suggested bash snippets are formatted in copyable blocks for mandatory human engineer review.
