"""
ROBOGUARD AI — BharatCode Model API Client
Integrates with the official BharatCode model API (https://bharatcode.ai/api/model/v1)
supporting deepseek-v4.1-flash and qwen-3.8-27b models with OpenAI-compatible payload.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional
from config.settings import BHARATCODE_API_BASE, BHARATCODE_DEFAULT_MODEL

class BharatCodeClient:
    """Official client for BharatCode AI Model API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 model: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key or os.getenv("BHARATCODE_API_KEY", "").strip()
        self.base_url = (base_url or BHARATCODE_API_BASE).rstrip("/")
        self.model = model or BHARATCODE_DEFAULT_MODEL
        self.timeout = timeout

    def is_configured(self) -> bool:
        """Returns True if an API key is provided and non-empty."""
        return bool(self.api_key and len(self.api_key) > 5)

    def test_connection(self) -> Dict[str, Any]:
        """Performs a lightweight probe to verify API key validity and endpoint availability."""
        if not self.is_configured():
            return {
                "success": False,
                "message": "API key is not configured. Set BHARATCODE_API_KEY in environment or Settings page.",
                "status_code": 401
            }

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": "Ping: Respond with 'PONG'"}
            ],
            "max_tokens": 10
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {
                    "success": True,
                    "message": f"Connection established successfully with model '{self.model}'.",
                    "status_code": 200,
                    "raw_response": content
                }
            elif resp.status_code == 402:
                err_msg = ""
                try:
                    err_json = resp.json()
                    err_msg = err_json.get("error", {}).get("message", "")
                except Exception:
                    pass
                if not err_msg:
                    err_msg = resp.text[:250]
                return {
                    "success": False,
                    "status_code": 402,
                    "is_payment_required": True,
                    "message": f"BharatCode Plan Required (HTTP 402): {err_msg}",
                    "raw_error": err_msg
                }
            else:
                return {
                    "success": False,
                    "message": f"API returned HTTP {resp.status_code}: {resp.text[:200]}",
                    "status_code": resp.status_code
                }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": f"Connection timed out ({self.timeout}s) contacting {self.base_url}.",
                "status_code": 408
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Network exception: {str(e)}",
                "status_code": 500
            }

    def generate_chat_completion(self, messages: List[Dict[str, str]],
                                 temperature: float = 0.2, max_tokens: int = 1500) -> Dict[str, Any]:
        """
        Sends chat completion request to BharatCode Model API.
        Enforces defensive retry and timeout handling.
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "API key not configured. Enable Offline Mode or set BHARATCODE_API_KEY."
            }

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Up to 2 attempts for transient errors
        last_error = ""
        for attempt in range(2):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    return {
                        "success": True,
                        "content": content,
                        "model": data.get("model", self.model),
                        "usage": data.get("usage", {})
                    }
                elif resp.status_code == 402:
                    err_msg = ""
                    try:
                        err_json = resp.json()
                        err_msg = err_json.get("error", {}).get("message", "")
                    except Exception:
                        pass
                    if not err_msg:
                        err_msg = resp.text[:250]
                    return {
                        "success": False,
                        "status_code": 402,
                        "is_payment_required": True,
                        "error": f"BharatCode Subscription Required (HTTP 402): {err_msg}"
                    }
                elif resp.status_code in [429, 500, 502, 503, 504]:
                    last_error = f"HTTP {resp.status_code}: {resp.text[:150]}"
                    continue
                else:
                    return {
                        "success": False,
                        "error": f"BharatCode API HTTP {resp.status_code}: {resp.text[:200]}"
                    }
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                continue

        return {
            "success": False,
            "error": f"Failed after 2 attempts: {last_error}"
        }
