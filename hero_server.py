"""
ROBOGUARD AI — FastAPI Hero & Unified Server Entrypoint
Re-exports the unified FastAPI platform from server.py.
"""

from server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, log_level="info")
