#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLASSMIND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

ROS_WS="${CLASSMIND_ROS_WS:-${CLASSMIND_DIR}/ros2_ws}"

echo "========================================"
echo " ClassMind ROS 2 Setup"
echo "========================================"

source /opt/ros/humble/setup.bash

mkdir -p "${ROS_WS}/src"

rm -rf "${ROS_WS}/src/classmind_ros"

cp -r \
    "${CLASSMIND_DIR}/classmind_ws_ros" \
    "${ROS_WS}/src/classmind_ros"

cd "${ROS_WS}"

echo
echo "Building ClassMind ROS 2 package..."

colcon build --symlink-install

echo
echo "========================================"
echo " ClassMind ROS 2 Setup Complete"
echo "========================================"

echo
echo "ROS workspace:"
echo "${ROS_WS}"

echo
echo "Configure ClassMind with:"
echo
echo "export CLASSMIND_ROS_WS=\"${ROS_WS}\""
