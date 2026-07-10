# ClassMind — Smart Classroom Intelligence System

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Challenge](https://img.shields.io/badge/Challenge-Robotics%20Dream%20Keeper-blue)
![Stage](https://img.shields.io/badge/Stage-2%20Build-green)

## Quick Start

```bash
# Clone
git clone https://github.com/Nightrider1946/classmind-rdkx5.git

# Install Python dependencies
pip install -r requirements.txt

# Configure (set your DroidCam URL and ESP32 IP)
export CLASSMIND_ESP32_IP="YOUR_ESP32_IP"
nano ai_engine/config.py

# Launch complete ClassMind system (ONE COMMAND)
cd /root/classmind
./launch_classmind.sh

# Opens at http://BOARD_IP:5000
```

### Safe Shutdown
Press Ctrl+C — launch_classmind.sh handles SIGINT, 
sends /off to ESP32, terminates ROS nodes and Flask cleanly.

### No motors involved — no hardware e-stop required.
Environmental alert auto-clears after 10 seconds.

## Overview

ClassMind is an intelligent classroom management system built on RDK X5 
that solves two real problems faced by every college — manual attendance 
and energy waste in empty classrooms.

**Attendance System:** A camera (currently DroidCam, MIPI camera planned 
for Stage 3) feeds live video to RDK X5. YOLO11n runs person detection 
on the BPU (13-15ms inference, 91% confidence validated), crops detected 
faces, and InsightFace (buffalo_s) performs recognition against a 
pre-computed student embedding database (1.5s per match, validated with 
multiple people). Attendance is logged automatically to CSV — zero 
manual effort required.

**Energy Management:** A background occupancy monitor continuously 
checks the same camera feed (via a shared, thread-safe camera manager) 
and signals ESP32 over WiFi/HTTP to control a relay for lights/fans 
based on whether the room is occupied.

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
| Relay module | Switch control | Available |

## Software Stack

| Technology | Purpose |
|------------|---------|
| ROS 2 | System communication backbone |
| YOLO (Ultralytics) | Real time face detection on BPU |
| InsightFace | Face recognition and attendance |
| OpenCV | Camera capture and image processing |
| Python | Primary programming language |
| Ubuntu | Operating system on RDK X5 |

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
├── README.md                              # Project overview
├── NarendraAndhale-Project-ClassMind.md   # Challenge documentation
├── app.py                                 # Flask application entry point
│
├── ai_engine/
│   ├── __init__.py
│   ├── config.py                          # Global configuration
│   ├── camera_manager.py                  # Shared thread-safe camera manager
│   ├── yolo_detector.py                   # YOLO11n (BPU) person detection
│   ├── face_recognition.py                # InsightFace (CPU) recognition
│   ├── attendance.py                      # Attendance session manager
│   ├── occupancy_monitor.py               # Classroom occupancy monitoring
│   └── esp32_controller.py                # ESP32 HTTP relay controller
│
├── templates/
│   ├── index.html
│   ├── attendance.html
│   └── result.html
│
├── classmind_faces/                       # Student dataset (gitignored)
├── database/                              # Face embeddings cache (gitignored)
├── attendance_logs/                       # Generated attendance CSVs (gitignored)
│
├── classmind_ws/
│   └── src/
│       └── classmind_ros/                 # ROS 2 integration (PoC)
│
├── esp32_firmware/                        # ESP32 relay firmware
│
├── hardware/
│   └── BOM.md                             # Bill of Materials
│
├── docs/
│   ├── PROPOSAL.md
│   ├── ROADMAP.md
│   ├── STAGE1.md
│   └── DISCORD_POST.md
│
├── assets/                                # Screenshots & demo images
│
├── test_yolo.py                           # YOLO detector testing
├── test_recognition.py                    # InsightFace testing
└── test_attendance.py                     # Attendance pipeline testing
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
- [ ] Full ROS 2 pipeline working
- [ ] Deployed in IIIT Nagpur lab
- [X] Stage 1 submitted
- [ ] Stage 2 submitted
- [ ] Stage 3 submitted

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

## Links

- **Challenge:** Robotics Dream Keeper Challenge by D-Robotics
- **Official Repo:** https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge
- **Discord:** D-Robotics Community (username: naren)
- **Full Proposal:** [docs/PROPOSAL.md](docs/PROPOSAL.md)
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
