# ClassMind — Stage 3 Technical Documentation

**Version:** 1.0  
**Date:** July 2026  
**Author:** Narendra Andhale

---

# System Architecture

ClassMind launches the complete system using a single command:

```bash
./launch_classmind.sh
```

```
                    ClassMind Launcher
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
   Flask AI System                       ROS 2 Pipeline
        │                                     │
        │                             sensor_bridge Node
        │                                     │
        │                            ESP32 /gas Endpoint
        │                                     │
        │                             /classmind/gas
        │                                     │
        │                              decision Node
        │                                     │
        ▼                                     ▼
 Camera Manager                     Baseline Calibration
        │                            Threshold Detection
        │                            ESP32 Alert Control
        │
 ┌──────┴───────────┐
 │                  │
 ▼                  ▼
YOLO11n (BPU)   InsightFace (CPU)
Occupancy       Attendance
 │                  │
 ▼                  ▼
ESP32         Attendance CSV
RGB LED
Buzzer
```

---

# ROS 2 Nodes

| Node | Purpose |
|------|---------|
| sensor_bridge | Reads MQ sensor data from ESP32 every 2 seconds |
| decision | Performs baseline calibration, threshold detection and controls ESP32 alerts |

---

# AI Workloads

| Component | Hardware | Mode |
|-----------|----------|------|
| YOLO11n Person Detection | RDK X5 BPU | Continuous |
| InsightFace Recognition | CPU | Teacher-triggered |
| MQ Sensor Bridge | ROS 2 | Every 2 seconds |
| ESP32 Control | WiFi HTTP | Event-driven |

---

# MQ Sensor Logic

- 10-sample automatic baseline calibration
- Relative threshold detection (ADC Δ ≥ 250)
- Automatic alert hold for 10 seconds
- Automatic reset after timeout

**Note:** The MQ-series sensor is used as an environmental monitoring prototype and is **not** presented as a calibrated gas detector.

---

# Model Deployment

| Component | Version |
|-----------|---------|
| Board | D-Robotics RDK X5 (4GB) |
| RDKOS | 3.5.0 |
| Model Zoo Branch | rdk_x5 |
| Model Zoo Commit | b60777a65e4ea315406b49cb5348d24ad85096f0 |
| Detection Model | yolo11n_detect_bayese_640x640_nv12.bin |

---

# Performance Summary

| Component | Measured Result |
|-----------|-----------------|
| YOLO11n Pre-processing | ~10 ms |
| YOLO11n BPU Inference | ~13 ms |
| YOLO11n Post-processing | ~6 ms |
| InsightFace Recognition | ~1.5 s/person |
| MQ Sensor Poll Interval | 2 s |
| ESP32 Alert Response | <200 ms |

---

# Failure Recovery

| Failure | Behaviour |
|---------|-----------|
| Camera disconnected | Automatic reconnect |
| ESP32 unavailable | HTTP timeout, system continues |
| ROS node failure | Flask continues running |
| Flask failure | ROS 2 continues running |
| Power restart | ESP32 returns to safe state |

---

# Interfaces

| Interface | Protocol |
|-----------|----------|
| DroidCam → RDK X5 | HTTP MJPEG |
| RDK X5 → ESP32 | HTTP GET |
| MQ Sensor → ESP32 | Analog ADC |
| ESP32 → RGB LED | GPIO |
| ESP32 → Buzzer | GPIO |

---

# Prototype Scope

### Implemented

- ✅ BPU-accelerated YOLO11n person detection
- ✅ InsightFace attendance system
- ✅ Automatic CSV attendance logging
- ✅ Shared camera manager
- ✅ ROS 2 sensor bridge
- ✅ MQ environmental monitoring
- ✅ ESP32 RGB LED & buzzer control
- ✅ One-command launcher
- ✅ Automated Model Zoo setup
- ✅ Automated ROS 2 setup

### Future Work

- Relay-controlled classroom appliances
- Native MIPI camera
- Multi-classroom deployment
- Cloud synchronization
- Teacher authentication
- Analytics dashboard

---

ClassMind demonstrates a complete edge AI classroom prototype integrating BPU-accelerated computer vision, CPU-based face recognition, ROS 2 communication, environmental monitoring, and ESP32 hardware control on the D-Robotics RDK X5.
