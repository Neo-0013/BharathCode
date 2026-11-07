"""
ROBOGUARD AI — Automated Code Patch & Fix Diff Generator
Generates unified Git diffs (--- a/ +++ b/) and downloadable .patch files
for automated remediation of QoS mismatches, missing transforms, SROS2 hardening,
and launch dependency failures.
"""

from typing import Dict, Any, Optional

class PatchGenerator:
    """Generates deterministic source code and configuration patches."""

    @staticmethod
    def generate_patch(finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a diagnostic or security finding and returns a structured patch
        containing target filename, unified diff string, explanation, and corrected code.
        """
        fid = finding.get("id", "")
        category = finding.get("category", "")
        title = finding.get("title", "")
        entities = finding.get("entities", [])

        # 1. QoS Reliability Mismatch Patch
        if "QOS" in fid or "Reliability" in title:
            topic = entities[0] if entities else "/cmd_vel"
            target_file = f"src/robot_navigation/src/{topic.strip('/').replace('/', '_')}_subscriber.py"
            diff = (
                f"--- a/{target_file}\n"
                f"+++ b/{target_file}\n"
                f"@@ -12,6 +12,12 @@\n"
                f" from rclpy.node import Node\n"
                f"+from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy\n"
                f" \n"
                f" class TelemetrySubscriber(Node):\n"
                f"     def __init__(self):\n"
                f"         super().__init__('telemetry_subscriber')\n"
                f"-        # INCOMPATIBLE: Default subscriber requested RELIABLE from BEST_EFFORT publisher\n"
                f"-        self.sub = self.create_subscription(Twist, '{topic}', self.cb, 10)\n"
                f"+        # HARDENED: Explicitly match offered QoS policy\n"
                f"+        qos = QoSProfile(depth=10)\n"
                f"+        qos.reliability = ReliabilityPolicy.BEST_EFFORT\n"
                f"+        qos.durability = DurabilityPolicy.VOLATILE\n"
                f"+        self.sub = self.create_subscription(Twist, '{topic}', self.cb, qos)\n"
            )
            corrected_code = (
                f"from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy\n\n"
                f"# Configure compatible QoS Profile for {topic}\n"
                f"qos_profile = QoSProfile(depth=10)\n"
                f"qos_profile.reliability = ReliabilityPolicy.BEST_EFFORT\n"
                f"qos_profile.durability = DurabilityPolicy.VOLATILE\n\n"
                f"self.sub = self.create_subscription(\n"
                f"    Twist,\n"
                f"    '{topic}',\n"
                f"    self.callback_handler,\n"
                f"    qos_profile\n"
                f")"
            )
            return {
                "target_file": target_file,
                "patch_filename": f"fix_{topic.strip('/').replace('/', '_')}_qos.patch",
                "diff": diff,
                "corrected_code": corrected_code,
                "remediation_summary": f"Configured subscriber QoS to BEST_EFFORT on '{topic}' to match publisher capability."
            }

        # 2. QoS Durability Mismatch Patch
        if "Durability" in title:
            topic = entities[0] if entities else "/map"
            target_file = f"src/robot_bringup/launch/costmap.launch.py"
            diff = (
                f"--- a/{target_file}\n"
                f"+++ b/{target_file}\n"
                f"@@ -20,4 +20,8 @@\n"
                f"         Node(\n"
                f"             package='nav2_costmap_2d',\n"
                f"             executable='nav2_costmap_2d',\n"
                f"+            parameters=[{{\n"
                f"+                'global_costmap.global_costmap.map_topic': '{topic}',\n"
                f"+                'global_costmap.global_costmap.subscribe_to_updates': True,\n"
                f"+                'global_costmap.global_costmap.qos_durability': 'transient_local'\n"
                f"+            }}]\n"
                f"         )\n"
            )
            corrected_code = (
                f"# Launch configuration with TRANSIENT_LOCAL durability\n"
                f"Node(\n"
                f"    package='nav2_costmap_2d',\n"
                f"    executable='nav2_costmap_2d',\n"
                f"    parameters=[{{\n"
                f"        'qos_durability': 'transient_local',\n"
                f"        'topic': '{topic}'\n"
                f"    }}]\n"
                f")"
            )
            return {
                "target_file": target_file,
                "patch_filename": f"fix_{topic.strip('/').replace('/', '_')}_durability.patch",
                "diff": diff,
                "corrected_code": corrected_code,
                "remediation_summary": f"Configured TRANSIENT_LOCAL durability parameter in launch node."
            }

        # 3. TF2 Frame Disconnection Patch
        if "TF" in fid or "TF2" in category:
            target_file = "src/robot_bringup/launch/static_transforms.launch.py"
            diff = (
                f"--- a/{target_file}\n"
                f"+++ b/{target_file}\n"
                f"@@ -10,3 +10,12 @@\n"
                f"     return LaunchDescription([\n"
                f"+        # Fix disconnected TF2 tree: publish missing map -> odom transform\n"
                f"+        Node(\n"
                f"+            package='tf2_ros',\n"
                f"+            executable='static_transform_publisher',\n"
                f"+            name='static_map_to_odom',\n"
                f"+            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']\n"
                f"+        ),\n"
                f"     ])\n"
            )
            corrected_code = (
                f"# Static Transform Publisher (map -> odom)\n"
                f"from launch_ros.actions import Node\n\n"
                f"static_tf_node = Node(\n"
                f"    package='tf2_ros',\n"
                f"    executable='static_transform_publisher',\n"
                f"    name='static_map_to_odom',\n"
                f"    arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']\n"
                f")"
            )
            return {
                "target_file": target_file,
                "patch_filename": "fix_tf2_map_odom_connection.patch",
                "diff": diff,
                "corrected_code": corrected_code,
                "remediation_summary": "Added static_transform_publisher to bridge map -> odom coordinate frames."
            }

        # 4. Cybersecurity SROS2 Governance Hardening Patch
        if "SEC" in fid or "Cybersecurity" in category:
            target_file = "sros2/governance.xml"
            diff = (
                f"--- a/{target_file}\n"
                f"+++ b/{target_file}\n"
                f"@@ -5,8 +5,8 @@\n"
                f"     <domain_rule>\n"
                f"       <domain_id>42</domain_id>\n"
                f"-      <allow_unauthenticated_participants>true</allow_unauthenticated_participants>\n"
                f"-      <discovery_protection>NONE</discovery_protection>\n"
                f"+      <allow_unauthenticated_participants>false</allow_unauthenticated_participants>\n"
                f"+      <discovery_protection>ENCRYPT</discovery_protection>\n"
                f"     </domain_rule>\n"
            )
            corrected_code = (
                f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<dds xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
                f'  <governance>\n'
                f'    <domain_rule>\n'
                f'      <domain_id>42</domain_id>\n'
                f'      <!-- Enforce strict mutual X.509 authentication -->\n'
                f'      <allow_unauthenticated_participants>false</allow_unauthenticated_participants>\n'
                f'      <enable_join_access_control>true</enable_join_access_control>\n'
                f'      <discovery_protection>ENCRYPT</discovery_protection>\n'
                f'      <liveliness_protection>ENCRYPT</liveliness_protection>\n'
                f'    </domain_rule>\n'
                f'  </governance>\n'
                f'</dds>'
            )
            return {
                "target_file": target_file,
                "patch_filename": "harden_sros2_governance.patch",
                "diff": diff,
                "corrected_code": corrected_code,
                "remediation_summary": "Enforced authentication and encrypted discovery metadata in SROS2 governance."
            }

        # 5. Default Build / Dependency Patch
        target_file = "package.xml"
        diff = (
            f"--- a/{target_file}\n"
            f"+++ b/{target_file}\n"
            f"@@ -25,4 +25,6 @@\n"
            f"   <buildtool_depend>ament_cmake</buildtool_depend>\n"
            f"+  <exec_depend>rclpy</exec_depend>\n"
            f"+  <exec_depend>geometry_msgs</exec_depend>\n"
            f" </package>\n"
        )
        corrected_code = (
            f"<exec_depend>rclpy</exec_depend>\n"
            f"<exec_depend>geometry_msgs</exec_depend>\n"
            f"<exec_depend>tf2_ros</exec_depend>"
        )
        return {
            "target_file": target_file,
            "patch_filename": "fix_dependencies.patch",
            "diff": diff,
            "corrected_code": corrected_code,
            "remediation_summary": "Added missing ROS 2 execution dependencies in package manifest."
        }
