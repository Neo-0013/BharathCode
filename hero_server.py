"""
ROBOGUARD AI — FastAPI Hero Server
Serves the professional fullscreen hero landing page at port 8000.
No Streamlit chrome, no iframe prison — just a true fullscreen dark hero.
"""

import re
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
VENDOR_DIR = ASSETS_DIR / "vendor"

VENDOR_MAP = {
    "three.min.js":        "three.min.js",
    "OrbitControls.js":    "OrbitControls.js",
    "gsap.min.js":         "gsap.min.js",
    "ScrollTrigger.min.js":"ScrollTrigger.min.js",
    "ScrollToPlugin.min.js":"ScrollToPlugin.min.js",
}

SCRIPT_RE = re.compile(r'<script\s+src="https?://[^"]*/([^"/]+\.js)"\s*></script>')


def _inline_vendors(html: str) -> str:
    """Replace CDN script tags with inlined vendored copies."""
    def _sub(m: re.Match) -> str:
        name = VENDOR_MAP.get(m.group(1))
        path = VENDOR_DIR / name if name else None
        if path and path.exists():
            text = path.read_text(encoding="utf-8").replace("</script>", "<\\/script>")
            return f"<script>/* vendored: {name} */\n{text}\n</script>"
        return m.group(0)
    return SCRIPT_RE.sub(_sub, html)


def _build_hero_html(soc_url: str = "http://localhost:8501") -> str:
    """Read story_hero.html, inline vendors, and patch the SOC launch URL."""
    html = (ASSETS_DIR / "story_hero.html").read_text(encoding="utf-8")
    html = _inline_vendors(html)
    # Inject the SOC_URL so the hero's launchSOC() knows where to go
    html = html.replace("__SOC_URL__", soc_url)
    return html


app = FastAPI(title="ROBOGUARD AI Hero", docs_url=None, redoc_url=None)

# Mount branding/static assets if any exist
branding_dir = ASSETS_DIR / "branding"
if branding_dir.exists():
    app.mount("/branding", StaticFiles(directory=str(branding_dir)), name="branding")


@app.get("/", response_class=HTMLResponse)
@app.head("/")
async def serve_hero():
    """Serve the fullscreen hero landing page."""
    return HTMLResponse(content=_build_hero_html(), status_code=200)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "roboguard-hero"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
