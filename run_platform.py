#!/usr/bin/env python3
"""
ROBOGUARD AI — Unified Platform Launcher
Starts the unified high-performance platform server (FastAPI on port 8000)
which serves both the Storytelling Hero Landing Page and the full 3D Robotics SOC Dashboard.

Usage:
    python3 run_platform.py
    python3 run_platform.py --no-browser
    python3 run_platform.py --port 8080
    python3 run_platform.py --with-streamlit  # optionally launch secondary Streamlit instance on 8501
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
    p = argparse.ArgumentParser(description="Launch ROBOGUARD AI Unified Platform")
    p.add_argument("--port", type=int, default=8000,
                   help="Port for the unified server (default: 8000)")
    p.add_argument("--hero-port", type=int, default=None,
                   help="Alias for --port")
    p.add_argument("--soc-port", type=int, default=8501,
                   help="Port for optional secondary Streamlit server (default: 8501)")
    p.add_argument("--with-streamlit", action="store_true",
                   help="Also start the secondary Streamlit app on port 8501")
    p.add_argument("--no-browser", action="store_true",
                   help="Don't open a browser automatically")
    p.add_argument("--host", default="0.0.0.0",
                   help="Bind host (default: 0.0.0.0)")
    return p.parse_args()


def banner(port: int, with_streamlit: bool = False, soc_port: int = 8501):
    stream_line = f"║  📊  Streamlit Dev →  http://localhost:{soc_port:<5}       ║\n" if with_streamlit else ""
    print(f"""
╔══════════════════════════════════════════════════════╗
║     🛡️  ROBOGUARD AI — Unified Platform Server      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🌐  Hero Landing  →  http://localhost:{port:<5}       ║
║  🛡️  SOC Dashboard →  http://localhost:{port:<5}/soc   ║
║  ⚡  Single Unified FastAPI Server (Sub-10ms latency)║
{stream_line}║                                                      ║
║  Press Ctrl+C to stop the platform                   ║
╚══════════════════════════════════════════════════════╝
""")


def start_server(host: str, port: int) -> subprocess.Popen:
    """Start the unified FastAPI server via uvicorn."""
    cmd = [
        sys.executable, "-m", "uvicorn",
        "server:app",
        "--host", host,
        "--port", str(port),
        "--log-level", "warning",
    ]
    return subprocess.Popen(cmd, cwd=str(ROOT))


def start_streamlit(host: str, port: int) -> subprocess.Popen:
    """Start the secondary Streamlit dashboard if requested."""
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", str(port),
        "--server.address", host,
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
    ]
    env = os.environ.copy()
    env["ROBOGUARD_HERO_URL"] = f"http://localhost:8000"
    return subprocess.Popen(cmd, cwd=str(ROOT), env=env)


def wait_for_server(port: int, timeout: float = 12.0, label: str = "server") -> bool:
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
    port = args.hero_port if args.hero_port is not None else args.port
    banner(port, with_streamlit=args.with_streamlit, soc_port=args.soc_port)

    procs = []

    print("  ⏳ Starting Unified High-Performance Server (FastAPI)…")
    srv_proc = start_server(args.host, port)
    procs.append(srv_proc)

    if args.with_streamlit:
        print("  ⏳ Starting secondary Streamlit server…")
        st_proc = start_streamlit(args.host, args.soc_port)
        procs.append(st_proc)

    # Wait for server to be ready
    if wait_for_server(port, timeout=10, label="Unified Platform"):
        print(f"  ✅ Unified Platform ready at http://localhost:{port}")
        print(f"     • Hero Landing Page : http://localhost:{port}/")
        print(f"     • SOC Operations    : http://localhost:{port}/soc")

    if args.with_streamlit and wait_for_server(args.soc_port, timeout=15, label="Streamlit"):
        print(f"  ✅ Secondary Streamlit ready at http://localhost:{args.soc_port}")

    if not args.no_browser:
        webbrowser.open(f"http://localhost:{port}")
        print(f"\n  🌐 Browser opened → http://localhost:{port}")

    print("\n  🟢 ROBOGUARD AI is live. Press Ctrl+C to stop.\n")

    def _shutdown(sig, frame):
        print("\n  🛑 Shutting down ROBOGUARD AI...")
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        time.sleep(1.0)
        for p in procs:
            try:
                p.kill()
            except Exception:
                pass
        print("  ✅ Platform stopped cleanly.")
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
