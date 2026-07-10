# ClassMind — Stage 3 Technical Documentation
**Version:** 1.0 | **Date:** July 2026
**Author:** Narendra Andhale

---

## System Architecture

ClassMind runs four concurrent subsystems from one command:
```text
./launch_classmind.sh
│
├── Flask Web App (app.py)
│   │
│   ├── Camera Manager
│   │   └── Shared thread-safe camera capture
│   │
│   ├── YOLO11n (RDK X5 BPU)
│   │   └── Occupancy Monitor
│   │       └── ESP32 HTTP Control
│   │           └── Relay / Light / Fan Control
│   │
│   └── InsightFace (CPU)
│       └── Attendance Recognition
│           └── Attendance CSV
│
└── ROS 2 (classmind.launch.py)
    │
    ├── sensor_bridge Node
    │   └── ESP32 /gas Endpoint
    │       └── /classmind/gas ROS 2 Topic
    │
    └── decision Node
        ├── 10-Sample Baseline Calibration
        ├── Raw ADC Delta Calculation
        ├── Relative Threshold (Delta >= 250)
        └── ESP32 Environmental Alert
            ├── /red
            ├── 10-Second Alert Hold
            └── /off
```
## ROS 2 Node Graph

| Node | Executable | Publishes | Subscribes |
|------|------------|-----------|------------|
| sensor_bridge | sensor_bridge | /classmind/gas (std_msgs/String) | — |
| decision | decision | — | /classmind/gas |

Check interval: sensor_bridge polls ESP32 /gas every 2 seconds.

## Multi-Task Workload

| Task | Hardware | Trigger | Latency |
|------|----------|---------|---------|
| Person detection (YOLO11n) | BPU | Continuous, every frame | 13-15ms |
| Face recognition (InsightFace) | CPU | Triggered by teacher | ~1.5s/person |
| MQ sensor bridge | CPU (network I/O) | Every 2 seconds | ~50ms HTTP |
| Occupancy → light control | CPU + ESP32 | Every 5-10 seconds | <200ms |

All four run simultaneously from ./launch_classmind.sh.

## Sensor Calibration

MQ-series analog prototype:
- Sensor connected via voltage divider to ESP32 ADC
- Decision Node performs 10-sample auto-calibration at startup
- Baseline established from average of 10 readings
- Alert threshold: delta >= 250 ADC units above baseline
- Alert hold: 10 seconds, then auto-clear
- NOT a calibrated CO/gas detector — prototype signal monitor only

Typical baseline observed: 1877-1997 ADC units
Typical normal delta: 0-5 units
Alert test (simulated): delta = 323-403 units

## Known Issues

| Issue | Status | Impact |
|-------|--------|--------|
| DroidCam single-connection limit | Fixed via Camera Manager | None |
| OOM with heavy models (VGG-Face) | Fixed — switched to InsightFace buffalo_s | None |
| Flask debug=True duplicate processes | Fixed — debug=False | None |
| Stale ESP32 actuator state after ROS restart | Fixed — startup reset in Decision Node | None |
| ai_engine.config not accessible from ROS nodes | Fixed — CLASSMIND_ESP32_IP env var | None |
| Face recognition not tested at 50-student scale | Known limitation | Planned Stage 4 |

## Configuration

```bash
# Required environment variable
export CLASSMIND_ESP32_IP="YOUR_ESP32_IP"

# ai_engine/config.py settings
DROIDCAM_URL = "http://PHONE_IP:4747/video"
ESP32_IP = "YOUR_ESP32_IP"
FACE_DB_PATH = "/root/classmind_faces/"
```

## Failure Recovery

| Failure | Behavior |
|---------|---------|
| DroidCam disconnect | Camera Manager retries with backoff |
| ESP32 unreachable | HTTP timeout (2s), logged, system continues |
| ROS node crash | Other subsystems continue independently |
| Flask crash | ROS nodes continue independently |
| Power loss | ESP32 relay defaults to OFF (safe state) |

## Interfaces

| Interface | Protocol | Direction |
|-----------|---------|-----------|
| DroidCam → RDK X5 | HTTP MJPEG over WiFi | Inbound |
| RDK X5 → ESP32 | HTTP GET over WiFi | Outbound |
| ESP32 → Relay | GPIO | Outbound |
| ESP32 → Buzzer | GPIO | Outbound |
| ESP32 → RGB LED | GPIO | Outbound |
| ESP32 ADC ← MQ sensor | Analog voltage divider | Inbound |
