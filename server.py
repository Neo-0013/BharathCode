"""
ROBOGUARD AI — Unified High-Performance Server
Single-server architecture serving both the Fullscreen Storytelling Hero and
the complete 3D Cyber-Physical Robotics SOC Dashboard, plus fast REST APIs.

Endpoints:
    GET  /                 -> Fullscreen Story Hero (story_hero.html)
    GET  /soc              -> Executive SOC Dashboard (soc_dashboard.html)
    GET  /dashboard        -> Redirect to /soc
    GET  /api/status       -> Real-time telemetry, posture & enclave status
    GET  /api/scenarios    -> List available demo scenarios
    POST /api/scenarios/:id-> Switch active scenario & recompute posture
    GET  /api/graph        -> Live ROS 2 computational graph JSON
    POST /api/attack       -> Simulate cyber-physical attack vector
    POST /api/isolate      -> eBPF rule #4092 isolation of rogue node
    POST /api/patch/:id    -> 1-click deterministic patch application
    POST /api/estop        -> Immediate fleet emergency actuation clamp
    GET  /api/export/html  -> Download standalone offline HTML security report
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from ui.asset_loader import load_html_asset
from core.dynamic_graph_generator import DynamicGraphGenerator

ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / "assets"
VENDOR_DIR = ASSETS_DIR / "vendor"

app = FastAPI(
    title="ROBOGUARD AI Unified Platform",
    description="Unified Aerospace & Defense Cyber-Physical Robotics SOC",
    version="2.0.0",
    docs_url="/docs",
    redoc_url=None,
)

# Mount static asset directories
if (ASSETS_DIR / "branding").exists():
    app.mount("/branding", StaticFiles(directory=str(ASSETS_DIR / "branding")), name="branding")
if VENDOR_DIR.exists():
    app.mount("/vendor", StaticFiles(directory=str(VENDOR_DIR)), name="vendor")
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


# --- In-Memory Platform State ---

STATE: Dict[str, Any] = {
    "active_scenario": "scenario_5",
    "scenario_name": "Scenario 5: Insecure AMR Fleet",
    "sros2_active": True,
    "wire_throughput": 284.2,
    "network_latency": 1.84,
    "enclave_integrity": 99.8,
    "critical_vulnerabilities": 2,
    "qos_mismatches": 1,
    "posture_score": 45,
    "drift": -18,
    "hardware_enclave": "6/6 Active",
    "isolated_nodes": [],
    "applied_patches": [],
    "estop_engaged": False,
    "current_attack": None,
}

SCENARIOS_META = {
    "scenario_5": {
        "name": "Scenario 5: Insecure AMR Fleet",
        "description": "Unauthenticated remote telemetry injection via /teleop_keyboard, QoS reliability drift on /cmd_vel.",
        "score": 45,
        "drift": -18,
        "vulns": 2,
        "qos": 1,
    },
    "scenario_4": {
        "name": "Scenario 4: LiDAR Sensor Tampering",
        "description": "Spoofed point cloud phantom obstacles injected on /scan topic, inducing Nav2 costmap hallucination.",
        "score": 58,
        "drift": -12,
        "vulns": 1,
        "qos": 1,
    },
    "scenario_3": {
        "name": "Scenario 3: DDS Multicast Storm",
        "description": "Unbounded UDP multicast packet saturation on RTPS Domain 0, causing high jitter and 12.8% drop rate.",
        "score": 62,
        "drift": -8,
        "vulns": 1,
        "qos": 2,
    },
    "scenario_2": {
        "name": "Scenario 2: SROS2 Keystore Drift",
        "description": "Out-of-sync governance XML certificate causing enclave revocation and authorization rejections.",
        "score": 78,
        "drift": -4,
        "vulns": 1,
        "qos": 0,
    },
    "scenario_1": {
        "name": "Scenario 1: Baseline Zero-Trust Fleet",
        "description": "All nodes secured with SROS2 PKCS#11 hardware keys, strict QoS contracts, zero rogue publishers.",
        "score": 96,
        "drift": 0,
        "vulns": 0,
        "qos": 0,
    },
}


def _render_hero_html() -> str:
    """Render story_hero.html with internal routing to /soc."""
    html = load_html_asset("story_hero.html")
    # Seamless single-server routing: hero directly points to /soc on the same host
    html = html.replace("__SOC_URL__", "/soc")
    return html


def _render_soc_html() -> str:
    """Render soc_dashboard.html with dynamic NetworkX graph injected."""
    try:
        gen = DynamicGraphGenerator(scenario_name=STATE["active_scenario"])
        graph_data = gen.export_graph_json()
    except Exception:
        gen = DynamicGraphGenerator()
        graph_data = gen.export_graph_json()
    return load_html_asset("soc_dashboard.html", graph_data=graph_data)


# --- Frontend Page Routes ---

@app.get("/", response_class=HTMLResponse)
@app.head("/")
async def serve_hero():
    """Serve the fullscreen storytelling hero landing page."""
    return HTMLResponse(content=_render_hero_html(), status_code=200)


@app.get("/soc", response_class=HTMLResponse)
@app.head("/soc")
async def serve_soc():
    """Serve the complete executive 3D Robotics SOC Dashboard."""
    return HTMLResponse(content=_render_soc_html(), status_code=200)


@app.get("/dashboard")
@app.head("/dashboard")
async def redirect_dashboard():
    """Convenience alias redirecting /dashboard to /soc."""
    return RedirectResponse(url="/soc", status_code=307)


# --- REST API Endpoints ---

@app.get("/api/status")
async def get_status():
    """Return real-time telemetry, posture score, and active threat state."""
    return JSONResponse(STATE)


@app.get("/api/scenarios")
async def list_scenarios():
    """Return all available demo scenarios."""
    return JSONResponse({
        "active": STATE["active_scenario"],
        "scenarios": SCENARIOS_META,
    })


@app.post("/api/scenarios/{scenario_id}")
async def switch_scenario(scenario_id: str):
    """Switch active scenario and recalculate security posture metrics."""
    if scenario_id not in SCENARIOS_META:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")
    
    meta = SCENARIOS_META[scenario_id]
    STATE["active_scenario"] = scenario_id
    STATE["scenario_name"] = meta["name"]
    STATE["posture_score"] = meta["score"]
    STATE["drift"] = meta["drift"]
    STATE["critical_vulnerabilities"] = meta["vulns"]
    STATE["qos_mismatches"] = meta["qos"]
    STATE["isolated_nodes"].clear()
    STATE["applied_patches"].clear()
    STATE["estop_engaged"] = False
    STATE["current_attack"] = None

    try:
        gen = DynamicGraphGenerator(scenario_name=scenario_id)
        graph_data = gen.export_graph_json()
    except Exception:
        gen = DynamicGraphGenerator()
        graph_data = gen.export_graph_json()

    return JSONResponse({
        "status": "success",
        "scenario": scenario_id,
        "name": meta["name"],
        "score": meta["score"],
        "vulns": meta["vulns"],
        "qos": meta["qos"],
        "graph": graph_data,
    })


@app.get("/api/graph")
async def get_graph():
    """Return dynamic computational graph JSON for the active scenario."""
    try:
        gen = DynamicGraphGenerator(scenario_name=STATE["active_scenario"])
        return JSONResponse(gen.export_graph_json())
    except Exception as e:
        gen = DynamicGraphGenerator()
        return JSONResponse(gen.export_graph_json())


@app.post("/api/attack")
async def trigger_attack(payload: Dict[str, Any] = Body(...)):
    """Simulate an active attack vector against the cyber-physical testbed."""
    vector = payload.get("vector", "cmd_vel")
    STATE["current_attack"] = vector
    
    if vector == "cmd_vel":
        details = {
            "vector": "cmd_vel",
            "type": "Unauthenticated Remote Actuation",
            "frequency_hz": 42.0,
            "target_topic": "/cmd_vel",
            "source_guid": "01.0f.d4.9a.12.34.56.78",
            "severity": "CRITICAL",
            "alert": "Rogue /cmd_vel vector detected: injection rate 42Hz from unauthenticated remote RTPS GUID.",
        }
    elif vector == "lidar":
        details = {
            "vector": "lidar",
            "type": "Synthetic Phantom Point Cloud Injection",
            "cluster_coord": {"x": 1.42, "y": 0.00, "z": 0.28},
            "target_topic": "/scan",
            "severity": "HIGH",
            "alert": "Injected synthetic point-cloud phantom cluster at x:1.42m y:0.00m. Nav2 costmap inflated.",
        }
    elif vector == "storm":
        details = {
            "vector": "storm",
            "type": "RTPS UDP Multicast Saturation",
            "domain_id": 0,
            "packet_drop_pct": 12.8,
            "severity": "HIGH",
            "alert": "Initiating UDP Multicast saturation attack on Domain ID 0. Drop rate: 12.8%.",
        }
    else:
        details = {
            "vector": vector,
            "type": "Generic RTPS Anomaly",
            "severity": "MEDIUM",
            "alert": f"Simulation event on vector '{vector}'.",
        }
    
    return JSONResponse({"status": "active", "attack": details})


@app.post("/api/isolate")
async def isolate_node(payload: Optional[Dict[str, Any]] = Body(None)):
    """Apply eBPF rule #4092 to isolate rogue publisher socket."""
    target_node = payload.get("node", "/teleop_keyboard") if payload else "/teleop_keyboard"
    if target_node not in STATE["isolated_nodes"]:
        STATE["isolated_nodes"].append(target_node)
    
    # Mitigate critical vulnerability & improve posture score
    if STATE["critical_vulnerabilities"] > 0:
        STATE["critical_vulnerabilities"] -= 1
    STATE["posture_score"] = min(100, STATE["posture_score"] + 23)
    STATE["drift"] = max(0, STATE["drift"] + 15)

    return JSONResponse({
        "status": "isolated",
        "node": target_node,
        "ebpf_rule_id": 4092,
        "socket_fd": 28,
        "action": "SOCK_CLOSE_ENFORCE",
        "updated_posture": STATE["posture_score"],
        "critical_vulnerabilities": STATE["critical_vulnerabilities"],
    })


@app.post("/api/patch/{patch_id}")
async def apply_patch(patch_id: str):
    """Apply deterministic 1-click git patch and reload cryptographic enclaves."""
    if patch_id not in STATE["applied_patches"]:
        STATE["applied_patches"].append(patch_id)
    
    if patch_id == "SEC-SROS2-001":
        if STATE["critical_vulnerabilities"] > 0:
            STATE["critical_vulnerabilities"] -= 1
        STATE["posture_score"] = min(100, STATE["posture_score"] + 30)
        STATE["drift"] = min(0, STATE["drift"] + 12)
        message = "FastDDS governance XML permission enforcement applied. Keystore locked."
    elif patch_id == "QOS-REL-001":
        STATE["qos_mismatches"] = 0
        STATE["posture_score"] = min(100, STATE["posture_score"] + 20)
        STATE["drift"] = min(0, STATE["drift"] + 8)
        message = "Nav2 controller QoS reliability policy harmonized with base_controller."
    else:
        STATE["posture_score"] = min(100, STATE["posture_score"] + 10)
        message = f"Applied custom patch {patch_id}."

    return JSONResponse({
        "status": "applied",
        "patch_id": patch_id,
        "message": message,
        "posture_score": STATE["posture_score"],
        "critical_vulnerabilities": STATE["critical_vulnerabilities"],
        "qos_mismatches": STATE["qos_mismatches"],
    })


@app.post("/api/estop")
async def engage_estop():
    """Engage immediate emergency actuation stop across all fleet rovers."""
    STATE["estop_engaged"] = True
    STATE["wire_throughput"] = 0.0
    return JSONResponse({
        "status": "engaged",
        "action": "FLEET_ACTUATION_HALT",
        "affected_enclaves": 6,
        "message": "Fleet E-STOP engaged. Actuation circuits cut across all 6 AMR enclaves.",
    })


@app.get("/api/export/html")
async def export_offline_html():
    """Generate and download a self-contained offline HTML audit report."""
    html_content = _render_soc_html()
    return Response(
        content=html_content,
        media_type="text/html",
        headers={"Content-Disposition": "attachment; filename=ROBOGUARD_SOC_Report.html"},
    )


# --- Direct Execution ---

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"\n🛡️ ROBOGUARD AI — Unified Platform Server running at http://localhost:{port}\n")
    uvicorn.run("server:app", host=host, port=port, reload=False, access_log=True)
