"""Tests for the offline asset loader and scenario -> graph data pipeline."""
import json
import re

from core.dynamic_graph_generator import DynamicGraphGenerator
from ui.asset_loader import load_html_asset, inline_vendor_scripts


def test_html_assets_have_no_cdn_script_tags_after_load():
    for name in ("soc_dashboard.html", "story_hero.html"):
        html = load_html_asset(name)
        assert not re.search(r'<script\s+src="https?://', html), f"{name} still depends on a CDN"
        assert "THREE" in html and "gsap" in html.lower()


def test_graph_data_is_injected_as_valid_json():
    payload = DynamicGraphGenerator().export_graph_json()
    html = load_html_asset("soc_dashboard.html", graph_data=payload)
    assert "/*__ROBOGUARD_GRAPH_DATA__*/null" not in html
    m = re.search(r"const GRAPH_DATA = (\{.*?\});\n", html, re.S)
    assert m, "graph payload not injected"
    parsed = json.loads(m.group(1))
    assert parsed["stats"]["total_edges"] == len(parsed["edges"])


def test_script_terminators_in_payload_are_escaped():
    html = load_html_asset("soc_dashboard.html", graph_data={"nodes": [{"id": "x", "label": "</script><b>"}], "edges": []})
    assert "</script><b>" not in html


def test_default_graph_flags_cmd_vel_edges_only():
    g = DynamicGraphGenerator().export_graph_json()
    bad = [e for e in g["edges"] if e["error"]]
    assert len(bad) == 2 and all(e["from"] == "topic:/cmd_vel" for e in bad)


def test_qos_pairs_are_normalised_per_subscriber():
    scenario = {
        "nodes": [{"name": "/pub"}, {"name": "/good"}, {"name": "/bad"}],
        "topics": [{
            "name": "/t", "publishers": ["/pub"], "subscribers": ["/good", "/bad"],
            "publishers_count": 1, "subscribers_count": 2,
        }],
        "qos_pairs": [{
            "topic": "/t", "publisher": "/pub", "subscriber": "/bad",
            "pub_qos": {"reliability": "BEST_EFFORT", "durability": "VOLATILE"},
            "sub_qos": {"reliability": "RELIABLE", "durability": "VOLATILE"},
        }],
    }
    norm = DynamicGraphGenerator.normalize_scenario(scenario)
    g = DynamicGraphGenerator().export_graph_json(norm)
    errs = {e["to"] for e in g["edges"] if e["error"]}
    assert errs == {"node:/bad"}


def test_normalize_scenario_rejects_empty_payload():
    assert DynamicGraphGenerator.normalize_scenario({}) is None
    assert DynamicGraphGenerator.normalize_scenario(None) is None


def test_all_demo_scenarios_produce_renderable_graphs():
    import glob
    for path in glob.glob("data/demo_scenarios/*.json"):
        data = json.load(open(path))
        norm = DynamicGraphGenerator.normalize_scenario(data)
        g = DynamicGraphGenerator().export_graph_json(norm)
        assert g["nodes"], path
        ids = {n["id"] for n in g["nodes"]}
        assert all(e["from"] in ids and e["to"] in ids for e in g["edges"]), path
