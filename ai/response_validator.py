"""
ROBOGUARD AI — AI Response Validator & Safety Guardrails
Sanitizes model outputs, intercepts dangerous shell commands,
and validates that copilot explanations remain grounded in empirical evidence.
"""

import re
from typing import Dict, Any, List, Tuple

class ResponseValidator:
    """Validates and enforces safety boundaries on AI model responses."""

    # Disallowed dangerous commands
    DANGEROUS_PATTERNS = [
        r'\brm\s+-[rf]{1,2}\b',
        r':\(\)\s*\{.*\}',        # Fork bomb
        r'\bmkfs\b',
        r'\bdd\s+if=',
        r'\bcurl\b.*\|\s*(?:bash|sh)',
        r'\bwget\b.*\|\s*(?:bash|sh)',
        r'\bchmod\s+777\s+/',
        r'\bchown\s+-[R\s]+root\s+/'
    ]

    # Valid ROS 2 CLI prefixes
    VALID_ROS2_PATTERNS = [
        r'\bros2\s+(?:topic|node|param|service|action|lifecycle|pkg|run|launch|bag|security|doctor|multicast)\b',
        r'\bcolcon\s+build\b',
        r'\brosdep\s+install\b',
        r'\bsource\s+(?:install|/opt/ros)'
    ]

    def validate_and_sanitize(self, response_text: str, finding_id: str = "") -> Tuple[bool, str, List[str]]:
        """
        Validates text against safety guardrails.
        Returns: (is_safe: bool, sanitized_text: str, warnings: List[str])
        """
        warnings = []
        is_safe = True

        if not response_text or not response_text.strip():
            return False, "Empty response received from AI model.", ["Empty response"]

        # 1. Dangerous command audit
        for pat in self.DANGEROUS_PATTERNS:
            if re.search(pat, response_text, re.IGNORECASE):
                is_safe = False
                warnings.append(f"Blocked dangerous system pattern: {pat}")
                response_text = re.sub(pat, "[BLOCKED DANGEROUS COMMAND]", response_text, flags=re.IGNORECASE)

        # 2. Check if finding_id is mentioned when specified
        if finding_id and finding_id not in response_text:
            warnings.append(f"Response did not explicitly cite finding ID '{finding_id}'. Verify grounding.")

        # 3. Verify presence of valid ROS 2 commands
        has_ros_command = any(re.search(p, response_text, re.IGNORECASE) for p in self.VALID_ROS2_PATTERNS)
        if not has_ros_command:
            warnings.append("No standard ROS 2 CLI commands were detected in the generated troubleshooting text.")

        return is_safe, response_text, warnings
