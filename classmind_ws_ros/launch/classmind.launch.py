from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    sensor_bridge = Node(
        package="classmind_ros",
        executable="sensor_bridge",
        name="classmind_sensor_bridge",
        output="screen"
    )

    decision_node = Node(
        package="classmind_ros",
        executable="decision",
        name="classmind_decision_node",
        output="screen"
    )

    return LaunchDescription([
        sensor_bridge,
        decision_node
    ])