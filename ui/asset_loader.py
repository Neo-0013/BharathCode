"""
ROBOGUARD AI — Offline-first HTML asset loader.

The WebGL pages (story hero, SOC dashboard) are authored against CDN URLs for
Three.js / GSAP. For a competition demo that may run on flaky venue Wi-Fi, we
inline vendored copies (assets/vendor/) so the 3D engines work with zero
network access, and inject live Python-computed graph data into the SOC page.
"""

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
VENDOR_DIR = ASSETS_DIR / "vendor"

# CDN <script src> pattern -> vendored file name
_VENDOR_MAP = {
    "three.min.js": "three.min.js",
    "OrbitControls.js": "OrbitControls.js",
    "gsap.min.js": "gsap.min.js",
    "ScrollTrigger.min.js": "ScrollTrigger.min.js",
    "ScrollToPlugin.min.js": "ScrollToPlugin.min.js",
    "tailwindcss.js": "tailwindcss.js",
}
_SCRIPT_RE = re.compile(r'<script\s+src=[\"\']https?://([^\"\']+)[\"\']\s*></script>')
_GRAPH_MARKER = "/*__ROBOGUARD_GRAPH_DATA__*/null"


@lru_cache(maxsize=None)
def _vendor_text(name: str) -> Optional[str]:
    path = VENDOR_DIR / name
    if not path.exists():
        return None
    # Defuse accidental </script> sequences inside inlined libraries
    return path.read_text(encoding="utf-8").replace("</script>", "<\\/script>")


def inline_vendor_scripts(html: str) -> str:
    """Replace CDN script tags with inlined vendored copies when available."""
    def _sub(match: "re.Match[str]") -> str:
        url = match.group(1)
        if "tailwindcss" in url:
            vendored = "tailwindcss.js"
        else:
            vendored = _VENDOR_MAP.get(url.split("/")[-1].split("?")[0])
        text = _vendor_text(vendored) if vendored else None
        if text is None:
            return match.group(0)  # leave CDN tag as a fallback
        return f"<script>/* vendored: {vendored} */\n{text}\n</script>"
    return _SCRIPT_RE.sub(_sub, html)


def load_html_asset(name: str, graph_data: Optional[Dict[str, Any]] = None) -> str:
    """Read assets/<name>, inline vendored JS, and inject graph JSON if given."""
    path = ASSETS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Asset not found: {path}")
    html = inline_vendor_scripts(path.read_text(encoding="utf-8"))
    if graph_data is not None and _GRAPH_MARKER in html:
        payload = json.dumps(graph_data).replace("</", "<\\/")
        html = html.replace(_GRAPH_MARKER, payload)
    return html
