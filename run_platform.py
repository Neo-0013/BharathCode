#!/usr/bin/env python3
"""
ROBOGUARD AI — Unified Launcher
Starts the Hero server (FastAPI/port 8000) and the SOC Dashboard (Streamlit/port 8501)
in parallel, then opens the hero page in the default browser.

Usage:
    python3 launch.py
    python3 launch.py --no-browser
    python3 launch.py --hero-port 3000 --soc-port 8080
"""

import argparse
import os
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def parse_args():
    p = argparse.ArgumentParser(description="Launch ROBOGUARD AI platform")
    p.add_argument("--hero-port", type=int, default=8000,
                   help="Port for the Hero landing page server (default: 8000)")
    p.add_argument("--soc-port",  type=int, default=8501,
                   help="Port for the SOC Streamlit dashboard (default: 8501)")
    p.add_argument("--no-browser", action="store_true",
                   help="Don't open a browser automatically")
    p.add_argument("--host", default="0.0.0.0",
                   help="Bind host for both servers (default: 0.0.0.0)")
    return p.parse_args()


def banner(hero_port: int, soc_port: int):
    print("""
╔══════════════════════════════════════════════════════╗
║          🛡️  ROBOGUARD AI — Launching...            ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🌐  Hero Landing  →  http://localhost:{hero:<5}       ║
║  🛡️  SOC Dashboard →  http://localhost:{soc:<5}       ║
║                                                      ║
║  Press Ctrl+C to stop both servers                   ║
╚══════════════════════════════════════════════════════╝
""".format(hero=hero_port, soc=soc_port))


def start_hero(host: str, port: int) -> subprocess.Popen:
    """Start the FastAPI hero server via uvicorn."""
    cmd = [
        sys.executable, "-m", "uvicorn",
        "hero_server:app",
        "--host", host,
        "--port", str(port),
        "--log-level", "warning",
    ]
    return subprocess.Popen(cmd, cwd=str(ROOT))


def start_soc(host: str, port: int) -> subprocess.Popen:
    """Start the Streamlit SOC dashboard."""
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", str(port),
        "--server.address", host,
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
    ]
    env = os.environ.copy()
    env["ROBOGUARD_HERO_URL"] = f"http://localhost:{port - 1}"  # hero port
    return subprocess.Popen(cmd, cwd=str(ROOT), env=env)


def wait_for_server(port: int, timeout: float = 15.0, label: str = "server") -> bool:
    """Poll until the server responds or timeout."""
    import socket
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.3)
    print(f"  ⚠️  {label} on port {port} did not start within {timeout}s")
    return False


def main():
    args = parse_args()
    banner(args.hero_port, args.soc_port)

    procs = []

    print("  ⏳ Starting Hero server (FastAPI)…")
    hero_proc = start_hero(args.host, args.hero_port)
    procs.append(hero_proc)

    print("  ⏳ Starting SOC Dashboard (Streamlit)…")
    soc_proc = start_soc(args.host, args.soc_port)
    procs.append(soc_proc)

    # Wait for hero to be ready before opening browser
    if wait_for_server(args.hero_port, timeout=12, label="Hero"):
        print(f"  ✅ Hero page ready at http://localhost:{args.hero_port}")
    if wait_for_server(args.soc_port, timeout=20, label="SOC Dashboard"):
        print(f"  ✅ SOC Dashboard ready at http://localhost:{args.soc_port}")

    if not args.no_browser:
        webbrowser.open(f"http://localhost:{args.hero_port}")
        print(f"\n  🌐 Browser opened → http://localhost:{args.hero_port}")

    print("\n  🟢 Both servers running. Press Ctrl+C to stop.\n")

    def _shutdown(sig, frame):
        print("\n  🛑 Shutting down ROBOGUARD AI...")
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        # Give them a moment to die gracefully
        time.sleep(1.5)
        for p in procs:
            try:
                p.kill()
            except Exception:
                pass
        print("  ✅ All servers stopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT,  _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    # Keep alive — monitor processes
    while True:
        for p in procs:
            if p.poll() is not None:
                print(f"  ⚠️  Process {p.pid} exited unexpectedly (code {p.returncode})")
        time.sleep(2)


if __name__ == "__main__":
    main()
