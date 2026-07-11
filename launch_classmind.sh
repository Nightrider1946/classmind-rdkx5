#!/bin/bash

set -e

echo "========================================"
echo "       ClassMind System Launcher"
echo "========================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLASSMIND_DIR="$SCRIPT_DIR"
ROS_WS="${CLASSMIND_ROS_WS:-/root/classmind_ws}"

cleanup() {

    echo ""
    echo "[ClassMind] Shutdown requested..."

    if [ -n "$FLASK_PID" ]; then
        kill "$FLASK_PID" 2>/dev/null || true
    fi

    if [ -n "$ROS_PID" ]; then
        kill "$ROS_PID" 2>/dev/null || true
    fi

    wait 2>/dev/null || true

    echo "[ClassMind] System stopped."

    exit 0
}

trap cleanup SIGINT SIGTERM


echo "[1/3] Loading ROS 2 Humble..."

source /opt/ros/humble/setup.bash


echo "[2/3] Loading ClassMind ROS workspace..."

source "$ROS_WS/install/setup.bash"


echo "[3/3] Starting ClassMind services..."


# ========================================
# START ROS 2 PIPELINE
# ========================================

echo "[ClassMind] Starting ROS 2 pipeline..."

ros2 launch classmind_ros classmind.launch.py &

ROS_PID=$!

echo "[ClassMind] ROS PID: $ROS_PID"

export CLASSMIND_MODEL_ZOO="${CLASSMIND_MODEL_ZOO:-/root/classmind_model_zoo_test}"
# ========================================
# START FLASK / AI PIPELINE
# ========================================

echo "[ClassMind] Starting Flask AI system..."

cd "$CLASSMIND_DIR"

python3 app.py &

FLASK_PID=$!

echo "[ClassMind] Flask PID: $FLASK_PID"


# ========================================
# SYSTEM READY
# ========================================

echo ""
echo "========================================"
echo " ClassMind is running"
echo ""
echo " Flask AI Pipeline : ACTIVE"
echo " ROS 2 Pipeline    : ACTIVE"
echo ""
echo " Press CTRL+C for safe shutdown"
echo "========================================"


wait