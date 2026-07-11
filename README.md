# ClassMind — Smart Classroom Intelligence System

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Challenge](https://img.shields.io/badge/Challenge-Robotics%20Dream%20Keeper-blue)
![Stage](https://img.shields.io/badge/Stage-2%20Build-green)

## Demo

🎥 Stage 3 Demo:
https://youtu.be/Bc0XRAdNyIA
## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Nightrider1946/classmind-rdkx5.git
cd classmind-rdkx5
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install the D-Robotics Model Zoo

```bash
chmod +x scripts/setup_model_zoo.sh
./scripts/setup_model_zoo.sh
```

### 4. Build the ROS 2 package

```bash
chmod +x scripts/setup_ros.sh
./scripts/setup_ros.sh
```

### 5. Configure the project

Edit `ai_engine/config.py` and set:

- DroidCam URL
- ESP32 IP address

Or export the environment variable:

```bash
export CLASSMIND_ESP32_IP="YOUR_ESP32_IP"
```

### 6. Launch the complete system

```bash
./launch_classmind.sh
```

Open the web interface at:

```
http://<RDK_X5_IP>:5000
```

## Requirements

- D-Robotics RDK X5 (RDKOS 3.5.0)
- ROS 2 Humble
- Python 3.10+
- ESP32-S3
- MQ-series analog sensor
- DroidCam (Android/iOS) or USB camera

### Safe Shutdown
Press Ctrl+C — launch_classmind.sh handles SIGINT, 
sends /off to ESP32, terminates ROS nodes and Flask cleanly.

### No motors involved — no hardware e-stop required.
Environmental alert auto-clears after 10 seconds.

## Overview

ClassMind is an intelligent classroom management system built on RDK X5 
that solves two real problems faced by every college — manual attendance 
and energy waste in empty classrooms.

**Attendance System:** A camera (currently DroidCam, MIPI camera planned ) feeds live video to RDK X5. YOLO11n runs person detection 
on the BPU (13-15ms inference, 91% confidence validated), crops detected 
faces, and InsightFace (buffalo_s) performs recognition against a 
pre-computed student embedding database (1.5s per match, validated with 
multiple people). Attendance is logged automatically to CSV — zero 
manual effort required.

**Energy Management:**The occupancy monitor continuously analyzes the shared camera stream and communicates with an ESP32 over Wi-Fi. During the prototype, the ESP32 controls an RGB LED and buzzer, while the firmware also provides an interface for relay-based classroom automation.
A Flask web dashboard lets a teacher select subject/class, view the 
live camera feed, trigger an attendance session, and view results — 
all running locally on the RDK X5.

## Project Details

- **Event:** Robotics Dream Keeper Challenge by D-Robotics
- **Track:** Smart Life Robotics
- **Timeline:** June 1 – July 15, 2026
- **Developer:** Narendra Andhale

## Hardware Stack

| Component | Purpose | Status |
|-----------|---------|--------|
| RDK X5 (4GB) | Main AI compute brain | Available |
| Wide angle MIPI camera | Face detection + occupancy | Pending |
| ESP32 | Relay control for lights/fans | Available |
| DHT22 sensor | Room temperature monitoring | Available |
| MQ2 gas sensor | Safety monitoring | Available |
| Relay module | Switch control | pending |

## Software Stack

| Technology | Purpose |
|------------|---------|
| ROS 2 | System communication backbone |
| YOLO (Ultralytics) | Real time face detection on BPU |
| InsightFace | Face recognition and attendance |
| OpenCV | Camera capture and image processing |
| Python | Primary programming language |
| Ubuntu | Operating system on RDK X5 |

Flask
ONNX Runtime
D-Robotics Model Zoo
BPU Runtime

## System Architecture

See full architecture, module design, compute allocation, and ROS 2 
node graph in **[docs/PROPOSAL.md](docs/PROPOSAL.md)**.

```text
                    DroidCam / Camera
                           │
                           ▼
      ┌────────────────────────────────────┐
      │ Camera Manager (Shared, Thread-Safe)│
      └───────────────┬────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
 ┌──────────────────┐     ┌────────────────────┐
 │ Occupancy Path   │     │ Attendance Path    │
 │ (Continuous)     │     │ (Teacher Triggered)│
 └────────┬─────────┘     └─────────┬──────────┘
          │                         │
          ▼                         ▼
 ┌──────────────────┐     ┌────────────────────┐
 │ YOLO11n (BPU)    │     │ YOLO11n (BPU)      │
 │ Person Counting  │     │ Person Detection   │
 └────────┬─────────┘     │ + Person Crop      │
          │               └─────────┬──────────┘
          ▼                         ▼
 ┌──────────────────┐     ┌────────────────────┐
 │ ESP32 Controller │     │ InsightFace (CPU)  │
 │ HTTP API         │     │ buffalo_s          │
 └────────┬─────────┘     │ Recognition        │
          │               └─────────┬──────────┘
          ▼                         ▼
 ┌──────────────────┐     ┌────────────────────┐
 │ Relay Control    │     │ Attendance Logger  │
 │ Light / Fan      │     │ CSV Generation     │
 └──────────────────┘     └────────────────────┘
```
## Repository Structure

```text
classmind-rdkx5/
│
├── README.md                              # Project overview & quick start
├── LICENSE                                # Apache License 2.0
├── requirements.txt                       # Python dependencies
├── launch_classmind.sh                    # One-command launcher
│
├── app.py                                 # Flask application entry point
│
├── ai_engine/
│   ├── __init__.py
│   ├── config.py                          # Global configuration
│   ├── camera_manager.py                  # Shared thread-safe camera manager
│   ├── yolo_detector.py                   # YOLO11n BPU inference
│   ├── face_recognition.py                # InsightFace recognition engine
│   ├── attendance.py                      # Attendance workflow
│   ├── occupancy_monitor.py               # Continuous occupancy detection
│   └── esp32_controller.py                # ESP32 HTTP communication
│
├── templates/
│   ├── index.html                         # Dashboard
│   ├── attendance.html                    # Attendance page
│   └── result.html                        # Attendance results
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── classmind_ws_ros/
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   ├── resource/
│   │   └── classmind_ros
│   │
│   ├── launch/
│   │   └── classmind.launch.py
│   │
│   ├── classmind_ros/
│   │   ├── __init__.py
│   │   ├── sensor_bridge_node.py          # ESP32 → ROS2 bridge
│   │   └── decision.py                    # Decision & alert node
│   │
│   └── test/
│       ├── test_flake8.py
│       ├── test_pep257.py
│       └── test_copyright.py
│
├── esp32_firmware/
│   └── TEST/
│       ├── src/
│       │   └── main.cpp
│       ├── include/
│       │   ├── secrets.example.h
│       │   └── secrets.h                  # gitignored
│       └── platformio.ini
│
├── scripts/
│   ├── setup_model_zoo.sh                 # Clone & configure Model Zoo
│   ├── setup_ros.sh                       # Build ROS2 package
│   └── enroll_faces.py                    # Generate InsightFace embeddings
│
├── docs/
│   ├── STAGE1.md
│   ├── PROPOSAL.md                        # Stage 2 proposal
│   ├── ROADMAP.md
│   ├── STAGE3.md                          # Final implementation
│   ├── BENCHMARK.md                       # Performance results
│   └── PROJECT_STATUS.md                  # Completed vs planned features
│
├── hardware/
│   └── BOM.md
│
├── assets/
│   ├── architecture.png
│   ├── dashboard.png
│   ├── attendance_demo.png
│   ├── occupancy_demo.png
│   ├── mq_sensor_demo.png
│   ├── ros2_terminal.png
│   ├── bpu_benchmark.png
│   ├── stage1_yolo_bpu_terminal.png
│   ├── stage3_system.jpg
│   └── thumbnail.png
│
├── database/                              # gitignored
│   ├── .gitkeep
│   └── README.md
│
├── classmind_faces/                       # gitignored
│   ├── .gitkeep
│   └── README.md
│
├── attendance_logs/                       # gitignored
│   ├── .gitkeep
│   └── README.md

```

## Current Status

- [x] Application form submitted
- [x] Registration confirmed by D-Robotics
- [x] GitHub repository created
- [x] Discord joined — username: naren
- [x] Project concept defined — ClassMind
- [x] System architecture designed
- [x] OpenCV installed and working on laptop
- [x] Face detection running on laptop (Haar Cascade)
- [x] Live webcam detection working
- [x] Group photo multi-face detection working
- [X] RDK Studio registered
- [X] YOLO installed and running — 86% confidence
- [X] RDK X5 board received
- [X] Camera connected to RDK X5
- [X] YOLO running on BPU
- [x] ESP32 relay connected
- [x] Full ROS 2 pipeline working
- [ ] Deployed in IIIT Nagpur lab
- [X] Stage 1 submitted
- [x] Stage 2 submitted
- [x] Stage 3 submitted

## Progress Log

### Day - June 5, 2026
- Registered for Robotics Dream Keeper Challenge
- Joined Discord community
- Created GitHub repository
- Learned complete OpenCV fundamentals
- Built working face detection using Haar Cascade
- Live webcam detection working
- Multi-face detection on group photo working
- YOLO person detection working ,86% confidence
- RDK X5 shipping confirmed from D-robotics, arrives ~June 18

### Day – June 17, 2026
- Successfully flashed RDK OS 3.5.0 Desktop on RDK X5
- Connected the board to Wi-Fi and verified internet connectivity
- Enabled SSH and remotely accessed the board from laptop
- Explored the RDK Model Zoo and runtime examples
- Learned how the BPU inference pipeline works on RDK X5
- Used DroidCam as a temporary vision sensor during development
- Successfully ran YOLO11 object detection on the RDK X5 BPU
- Performed custom image inference and verified detection results
- Submitted Stage 1 Pull Request to the Robotics Dream Keeper Challenge

### Day - June 28, 2026
- Benchmarked DeepFace vs InsightFace on actual hardware — switched to 
  InsightFace after measuring 19s vs 1.5s recognition time
- Fixed camera resource contention with shared camera_manager
- Built ESP32 HTTP-based occupancy/light control — validated working
- Built Flask web dashboard with live feed and attendance workflow
- Validated multi-person face recognition end-to-end (narendra + jyoti, 
  confidence 0.665–0.762)
- Designed full system architecture, ROS 2 node graph, risk analysis
- Completed Stage 2 documentation (docs/PROPOSAL.md, ROADMAP.md, BOM.md)

### Day – July 11, 2026
  - Implemented ROS 2 MQ sensor bridge
  
  - Implemented Decision Node with automatic baseline calibration
  
  - Added ESP32 alert control
  
  - Added 10-second automatic alert reset
  
  - Added one-command launcher (launch_classmind.sh)
  
  - Added automatic Model Zoo setup script
  
  - Added ROS setup automation
  
  - Added enrollment script for InsightFace database generation
  
  - Completed benchmark measurements
  
  - Finalized Stage 3 documentation
  
  - Recorded demonstration video

## Links

- **Challenge:** Robotics Dream Keeper Challenge by D-Robotics
- **Official Repo:** https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge
- **Discord:** D-Robotics Community (username: naren)
- **Full Proposal:** [docs/PROPOSAL.md](docs/PROPOSAL.md)
- **DEMO VIDEO :** https://youtu.be/Bc0XRAdNyIA
- **Developer:** Narendra Andhale — IIIT Nagpur

## About the Developer

B.Tech ECE IoT student at IIIT Nagpur (2024-2028).
Co-Head of IoTics Club Robotics Wing.
Experience with ROS 2, Raspberry Pi, ESP32, Arduino, Python,
and embedded systems. Previously built a quadcopter
drone, weather station, and ROS 2 target tracking
system. Interned at India Space Lab.

---

*ClassMind — Making classrooms intelligent,
one frame at a time.*
