"""
ROBOGUARD AI — ROS Graph Explorer Page
Interactive ROS 2 computational graph visualization with node inspection,
topic connectivity filters, and QoS mismatch edge highlights.
"""

import streamlit as st
from config.settings import UI_THEME
from core.ros_graph import ROSGraphBuilder
from ui.components import render_header

def render_graph_explorer_page(diagnostic_engine):
    render_header("ROS Graph Explorer", "Interactive node & topic communication topology, isolated clusters, and QoS mismatch paths.")

    current_analysis = st.session_state.get("current_analysis", None)
    scenario_meta = st.session_state.get("current_scenario_meta", {})
    scenario_data = scenario_meta.get("data", {})

    nodes = scenario_data.get("nodes", [])
    topics = scenario_data.get("topics", [])
    qos_pairs = scenario_data.get("qos_pairs", [])

    # If no structured nodes in active scenario, show demo topology or empty state
    if not nodes and not topics:
        st.markdown(f"""
        <div class="rg-card" style="text-align: center; padding: 2.5rem 1rem;">
            <div style="font-size: 1.05rem; font-weight: 600; color: #E2E8F0; margin-bottom: 0.5rem;">No Communication Graph Data Loaded</div>
            <div style="font-size: 0.85rem; color: {UI_THEME['text_secondary']}; max-width: 520px; margin: 0 auto 1.5rem auto;">
                To explore an interactive ROS 2 node and topic graph, load <b>Scenario 1</b> or <b>Scenario 2</b> from the Command Center, or upload a structured JSON topology dump.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    tab_comp, tab_tf = st.tabs([
        "🌐 Computational Node & Topic Graph",
        "📐 TF2 Coordinate Frame Hierarchy (REP-105)"
    ])

    with tab_comp:
        # Build NetworkX graph
        builder = ROSGraphBuilder()
        
        # Filter for QoS errors
        qos_errors = []
        if current_analysis:
            for f in current_analysis.get("findings", []):
                if f.get("category") == "QoS Profile Compatibility" and f.get("severity") == "CRITICAL":
                    entities = f.get("entities", [])
                    if len(entities) >= 3:
                        qos_errors.append({"topic": entities[0], "publisher": entities[1], "subscriber": entities[2]})

        builder.build_from_data(nodes, topics, qos_errors)
        stats = builder.get_topology_statistics()

        # Metric Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Nodes", stats.get("total_nodes", 0))
        with col2:
            st.metric("Total Topics", stats.get("total_topics", 0))
        with col3:
            st.metric("Communication Edges", stats.get("total_edges", 0))
        with col4:
            st.metric("Connected Subgraphs", stats.get("connected_components_count", 0))

        # Render Plotly interactive graph
        fig = builder.render_plotly()
        st.plotly_chart(fig, use_container_width=True)

        # Graph Legend & Inspector
        col_leg, col_insp = st.columns([1.2, 1.8])

        with col_leg:
            st.markdown("### Topology Legend")
            st.markdown("""
            - 🟢 **Green Circle:** Active ROS 2 Node
            - 🟡 **Amber Circle:** Inactive / Unconfigured Lifecycle Node
            - 🔴 **Red Circle:** Crashed / Failed Node
            - 🔷 **Cyan Diamond:** ROS 2 Topic
            - ⚪ **Gray Line:** Healthy Pub/Sub Edge
            - 🔴 **Red Dotted Line:** QoS Incompatible Communication Path
            """)

            orphans = stats.get("orphaned_entities", [])
            if orphans:
                st.warning(f"⚠️ Detected {len(orphans)} orphaned entities: {', '.join(orphans)}")

        with col_insp:
            st.markdown("### Endpoint Inspector")
            node_names = [n.get("name") for n in nodes if n.get("name")]
            selected_node = st.selectbox("Inspect Node Details", ["-- Select Node --"] + node_names)

            if selected_node != "-- Select Node --":
                node_info = next((n for n in nodes if n.get("name") == selected_node), None)
                if node_info:
                    st.json(node_info)

    with tab_tf:
        tf_edges = scenario_data.get("tf_edges", [])
        if not tf_edges:
            # Fallback to standard mobile robot tree if not explicitly defined
            tf_edges = [
                {"parent": "map", "child": "odom"},
                {"parent": "odom", "child": "base_link"},
                {"parent": "base_link", "child": "base_footprint"},
                {"parent": "base_link", "child": "laser_frame"},
                {"parent": "base_link", "child": "camera_optical_frame"}
            ]

        from core.tf_analyzer import TFAnalyzer
        tf_analyzer = TFAnalyzer()
        tf_tree_fig = tf_analyzer.render_plotly_tree(tf_edges)
        st.plotly_chart(tf_tree_fig, use_container_width=True)

        col_tf_info, col_tf_cmd = st.columns([1.4, 1.0])
        with col_tf_info:
            tree_eval = tf_analyzer.analyze_tf_tree(tf_edges)
            st.markdown(f"""
            <div class="rg-card">
                <div style="font-weight: 600; color: #F8FAFC; font-size: 0.9rem;">REP-105 Coordinate Framework Conformance</div>
                <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 0.35rem;">
                    Canonical Root Frames: <code>{', '.join(tree_eval['roots'])}</code><br>
                    Leaf Frames: <code>{', '.join(tree_eval['leaves'])}</code><br>
                    Total Frames: <b>{tree_eval['total_frames']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if len(tree_eval['roots']) > 1:
                st.error(f"🚨 Disconnected TF2 Tree! Multiple roots detected: {', '.join(tree_eval['roots'])}. Localization requires a connected path from map to odom.")

        with col_tf_cmd:
            st.markdown("**TF2 Verification Commands:**")
            st.code("ros2 run tf2_tools view_frames\nros2 run tf2_ros tf2_echo map odom\nros2 run tf2_ros tf2_monitor", language="bash")
