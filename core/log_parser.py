"""
ROBOGUARD AI — Log Parser Module
Deterministic parser for ROS 2 console logs, Colcon build logs,
and Linux terminal exceptions. Extracts structured error signatures,
log levels, node names, timestamps, and stack traces.
"""

import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.settings import CONFIG_DIR, Severity, DiagnosticCategory, Confidence

class LogEntry:
    def __init__(self, raw: str, level: str = "INFO", timestamp: Optional[str] = None,
                 logger: Optional[str] = None, message: str = ""):
        self.raw = raw
        self.level = level.upper()
        self.timestamp = timestamp
        self.logger = logger
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "timestamp": self.timestamp,
            "logger": self.logger,
            "message": self.message,
            "raw": self.raw
        }

class LogParser:
    def __init__(self, rules_path: Optional[Path] = None):
        if rules_path is None:
            rules_path = CONFIG_DIR / "rules.yaml"
        self.rules_path = rules_path
        self.rules = self._load_rules()

        # Standard ROS 2 console log pattern:
        # [SEVERITY] [timestamp] [logger_name]: message
        # e.g.: [ERROR] [1715420102.123456789] [nav2_costmap]: Lifecycle node failed
        self.ros2_log_regex = re.compile(
            r'^\[(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|FATAL)\]\s+'
            r'(?:\[(?P<timestamp>[\d\.\s:-]+)\]\s+)?'
            r'(?:\[(?P<logger>[a-zA-Z0-9_\.\/-]+)\]:\s+)?'
            r'(?P<message>.*)$',
            re.MULTILINE
        )

    def _load_rules(self) -> List[Dict[str, Any]]:
        if not self.rules_path.exists():
            return []
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("log_patterns", []) if data else []
        except Exception:
            return []

    def parse_lines(self, text: str) -> List[LogEntry]:
        """Parse raw log text into structured LogEntry records."""
        entries: List[LogEntry] = []
        if not text or not text.strip():
            return entries

        lines = text.splitlines()
        current_entry: Optional[LogEntry] = None

        for line in lines:
            match = self.ros2_log_regex.match(line)
            if match:
                if current_entry:
                    entries.append(current_entry)
                current_entry = LogEntry(
                    raw=line,
                    level=match.group("level"),
                    timestamp=match.group("timestamp"),
                    logger=match.group("logger"),
                    message=match.group("message") or ""
                )
            else:
                # Continuation of multiline trace or unstructured log
                if current_entry:
                    current_entry.message += "\n" + line
                    current_entry.raw += "\n" + line
                else:
                    # Unstructured log line
                    level = "ERROR" if any(w in line.upper() for w in ["ERROR", "FATAL", "EXCEPTION", "FAIL"]) else "INFO"
                    current_entry = LogEntry(raw=line, level=level, message=line)

        if current_entry:
            entries.append(current_entry)

        return entries

    def match_rules(self, text: str) -> List[Dict[str, Any]]:
        """Match deterministic rules against the full log text."""
        findings = []
        if not text:
            return findings

        for rule in self.rules:
            pattern = rule.get("regex")
            if not pattern:
                continue

            matches = list(re.finditer(pattern, text, re.MULTILINE))
            if matches:
                # Capture the full matched evidence and any captured groups
                matched_snippets = []
                entities = []
                for m in matches:
                    matched_snippets.append(m.group(0).strip())
                    # Collect named or positional capture groups
                    for g in m.groups():
                        if g and g not in entities:
                            entities.append(g)

                evidence = "\n---\n".join(matched_snippets[:3])
                if len(matches) > 3:
                    evidence += f"\n... and {len(matches) - 3} additional occurrences"

                finding = {
                    "id": rule.get("id"),
                    "title": rule.get("title"),
                    "category": rule.get("category"),
                    "severity": rule.get("severity", Severity.HIGH),
                    "status": rule.get("status", Confidence.CONFIRMED),
                    "evidence": evidence,
                    "entities": entities,
                    "root_cause": rule.get("root_cause", ""),
                    "troubleshooting": rule.get("troubleshooting", []),
                    "validation_commands": rule.get("validation_commands", []),
                    "match_count": len(matches)
                }
                findings.append(finding)

        return findings
