# ClassMind — Smart Classroom Intelligence System

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Challenge](https://img.shields.io/badge/Challenge-Robotics%20Dream%20Keeper-blue)
![Stage](https://img.shields.io/badge/Stage-1%20Ignite-green)

## Overview

ClassMind is an intelligent classroom management system 
built on RDK X5 that solves two real problems faced by 
every college, manual attendance and energy waste in 
empty classrooms.

**Attendance System:** A wide angle camera captures 
burst frames for 10-15 seconds. RDK X5 BPU runs YOLO 
face detection on each frame, tracks unique faces, 
splits classroom into zones, and selects the clearest 
image per student for recognition. Complete attendance 
for 50 students generated in under 20 seconds, zero 
teacher effort required.

**Energy Management:** Same camera monitors occupancy 
every 5 minutes. When zero people detected, RDK X5 
signals ESP32 via ROS 2 to control relay switches for 
lights and fans automatically.

## Project Details

- **Event:** Robotics Dream Keeper Challenge by D-Robotics
- **Track:** Smart Life Robotics
- **Timeline:** June 1 – July 15, 2026
- **Developer:** Narendra Andhale

## Hardware Stack

| Component | Purpose | Status |
|-----------|---------|--------|
| RDK X5 (4GB) | Main AI compute brain | Incoming |
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
| DeepFace | Face recognition and attendance |
| OpenCV | Camera capture and image processing |
| Python | Primary programming language |
| Ubuntu | Operating system on RDK X5 |

## ROS 2 Architecture

```
/camera_node
    ↓ raw frames
/burst_capture_node (10-15 sec, 20 frames)
    ↓ frame buffer
/zone_splitter_node (6 zones)
    ↓ zone images
/detection_node (YOLO on BPU)
    ↓ detected faces per zone
/recognition_node (DeepFace)
    ↓ student IDs
/attendance_node
    ↓ attendance report
/energy_node (occupancy monitoring)
    ↓ occupancy status
/esp32_bridge_node
    ↓ relay commands
Lights + Fan Control
```

## Repository Structure

```
classmind-rdkx5/
├── README.md
├── src/                    ← Python source code
├── docs/                   ← Documentation
│   ├── PROPOSAL.md
│   ├── ROADMAP.md
│   ├── STAGE1.md
│   └── DISCORD_POST.md
├── hardware/               ← BOM and wiring
│   └── BOM.md
├── assets/                 ← Screenshots and evidence
└── launch/                 ← ROS 2 launch files
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
- [ ] DeepFace face recognition working
- [ ] RDK X5 board received
- [ ] Camera connected to RDK X5
- [ ] YOLO running on BPU
- [ ] ESP32 relay connected
- [ ] Full ROS 2 pipeline working
- [ ] Deployed in IIIT Nagpur lab
- [ ] Stage 1 submitted
- [ ] Stage 2 submitted
- [ ] Stage 3 submitted

## Progress Log

### Day — June 5, 2026
- Registered for Robotics Dream Keeper Challenge
- Joined Discord community
- Created GitHub repository
- Learned complete OpenCV fundamentals
- Built working face detection using Haar Cascade
- Live webcam detection working
- Multi-face detection on group photo working
- YOLO person detection working ,86% confidence
- RDK X5 shipping confirmed from D-robotics, arrives ~June 18

## Links

- **Challenge:** Robotics Dream Keeper Challenge by D-Robotics
- **Official Repo:** https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge
- **Discord:** D-Robotics Community (username: naren)
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
