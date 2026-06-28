# ClassMind — Stage 2 Proposal
**Version:** 1.0 |  **Date:** [28 june, 2026]

**Participant:** Narendra Andhale |  **Repository:** https://github.com/Nightrider1946/classmind-rdkx5

---

## Challenge 1 — Concept & Application Design

### Scenario
ClassMind is designed to operate indoors in a college classroom/lab 
environment (target deployment: IIIT Nagpur). Operating conditions: 
standard classroom lighting (LED/tube light), a single fixed camera 
position at the front of the room (3-5m coverage range), and local 
WiFi for camera feed and ESP32 actuator communication. Target latency: 
attendance capture completes within 15-20 seconds per class session; 
occupancy state updates every 5-10 seconds for responsive energy control.

### User
**Primary user:** Teachers — eliminates manual attendance taking, 
saving 3-5 minutes per class session.
**Secondary user:** Institution — reduces electricity wastage from 
lights/fans left on in unoccupied classrooms.
**Interaction mode:** Passive for students (briefly face the camera 
during the attendance window); teacher interacts via a web dashboard 
to select subject/class, view the live feed, trigger attendance 
capture, and review results.

### Core AI Capabilities
- **Perception:** YOLO11n object detection on the RDK X5 BPU detects 
  person bounding boxes from the live camera feed.
- **Decision:** A dual-path decision system — (1) a lightweight, 
  continuous occupancy counter for energy decisions, and (2) a 
  triggered burst-capture pipeline that crops detected faces and runs 
  identity recognition against a pre-computed student embedding 
  database.
- **Actuation:** An ESP32 microcontroller (HTTP over WiFi) drives a 
  relay to control classroom lights/fan based on occupancy state 
  changes.

### Innovation / Differentiation
Unlike single-purpose object-detection demos, ClassMind's design 
unifies **two AI-driven outcomes from one camera pipeline**: 
energy-saving automation and attendance recognition, sharing hardware 
resources through a single coordinated capture layer rather than 
running independent, conflicting camera connections. The design is 
informed by real on-device testing rather than assumptions — we 
benchmarked two face-recognition approaches on the actual target 
hardware (RDK X5, 4GB RAM, ARM CPU) and selected the architecture 
based on measured results, not vendor claims (see Risk Analysis, 
Challenge 3).

### Measurable Goals
| Metric | Target | Current Validation |
|--------|--------|----------------------|
| Person detection inference time (BPU) | <20ms | 13-15ms, measured on-device ✅ |
| Face recognition time per person | <2s | 1.5s, measured on-device ✅ |
| Detection confidence (person class) | >85% | 91%, measured on test subjects ✅ |
| Attendance session duration (10 people) | <60s | ~20-30s in informal multi-person test ✅ |
| Occupancy responsiveness | <10s | Configurable, tested at 5s interval ✅ |
| Scale target (Stage 3) | 50 students, <90s total | Not yet tested at scale — planned Stage 3 |

---

## Challenge 2 — AI System Architecture

*This section describes the target architecture for ClassMind. Components 
marked **[Validated]** have been implemented and tested on the actual RDK X5 
board. Components marked **[Planned]** are the Stage 3 implementation target.*

### System Flow Diagram

```text
┌──────────────┐     ┌────────────────┐
│ Camera Input │────▶│ Camera Manager │  [Validated]
│ (DroidCam /  │     │ (shared,       │  Single thread-safe capture,
│  MIPI Stage3)│     │  thread-safe)  │  solves multi-consumer conflict
└──────────────┘     └────────┬───────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
      ┌────────────────┐           ┌─────────────────────┐
      │ Occupancy Path │           │ Attendance Path     │
      │ (continuous)   │           │ (triggered, 10–20s) │
      │ [Validated]    │           │ [Validated]         │
      └───────┬────────┘           └──────────┬──────────┘
              ▼                              ▼
      ┌────────────────┐           ┌─────────────────────┐
      │ YOLO11n (BPU)  │           │ YOLO11n (BPU)       │
      │ Person Count   │           │ Person BBox + Crop  │
      │ [Validated:    │           │ [Validated:         │
      │ 13–15 ms]      │           │ 91% Confidence]     │
      └───────┬────────┘           └──────────┬──────────┘
              ▼                              ▼
      ┌────────────────┐           ┌─────────────────────┐
      │ State Change   │           │ InsightFace (CPU)   │
      │ Detector       │           │ buffalo_s           │
      │ [Validated]    │           │ Recognition         │
      │                │           │ [Validated: ~1.5 s] │
      └───────┬────────┘           └──────────┬──────────┘
              │                              ▼
              │                     ┌─────────────────────┐
              │                     │ Attendance CSV      │
              │                     │ Logger              │
              │                     │ [Validated]         │
              │                     └─────────────────────┘
              ▼
┌────────────────────────────────────────────┐
│ ESP32 HTTP Controller (Wi-Fi)              │  [Validated]
└───────────────────────┬────────────────────┘
                        ▼
               ┌────────────────┐
               │ Relay → Light  │
               │ / Fan Control  │
               │ [Validated,    │
               │ LED Proxy;     │
               │ Real Relay =   │
               │ Stage 3]       │
               └────────────────┘

     ═══════════════════════════════════════
     ROS 2 MIDDLEWARE LAYER  [Planned, Stage 3]
     ═══════════════════════════════════════
     All modules above will publish/subscribe through
     dedicated ROS 2 nodes (see Node Graph below) to
     decouple perception, decision, and actuation —
     enabling independent testing, logging, and future
     multi-sensor expansion (e.g. additional cameras,
     IMU-based fall detection).
```

### Module Design

| Module | Responsibility | Input | Output | Failure Mode | Status |
|--------|----------------|-------|--------|---------------|--------|
| `camera_manager.py` | Single shared camera connection, thread-safe frame distribution | DroidCam HTTP stream | Latest frame (BGR array) | Stream drop → retry with backoff | ✅ Validated |
| `yolo_detector.py` | Person detection on BPU | Frame | List of {bbox, confidence, crop} | Low confidence (<0.6) filtered, no crash | ✅ Validated |
| `occupancy_monitor.py` | Continuous occupancy tracking | Frame | ESP32 light command on state change | No frame → skip cycle, retry | ✅ Validated |
| `face_recognition.py` | Identity matching (InsightFace) | Cropped face | (name, confidence) | No match → "Unknown", logged | ✅ Validated |
| `attendance.py` | Session orchestration, CSV logging | Subject/class/duration | attendance.csv | Camera loss → graceful partial save | ✅ Validated |
| `esp32_controller.py` | HTTP relay dispatch | Boolean state | HTTP request | Timeout (2s) → fail-safe, no crash | ✅ Validated |
| `classmind_bridge_node` | ROS 2 publisher for attendance/occupancy events | Internal Python calls | `/classmind/*` topics | Node crash → web app continues independently | ⚠️ Proof-of-concept only — see note below |

**Honest note on ROS 2 bridge status:** A minimal bridge node was built that 
can publish to `/classmind/attendance` and `/classmind/occupancy` topics via 
CLI invocation from the Flask app. This validates topic/message design but is 
**not yet a production-quality integration** (no persistent publisher object, 
no subscriber consuming the data for decision-making). Stage 3 will refactor 
this into proper long-running ROS 2 nodes with the Flask layer as a thin 
client, or alternatively restructure perception/decision logic to run natively 
as ROS 2 nodes rather than a bridged Flask app. This is flagged transparently 
as our primary architectural risk (see Risk #2, Challenge 3).

### Compute Allocation

| Module | Runs On | Expected Utilisation |
|--------|---------|------------------------|
| YOLO11n person detection | **BPU** | ~15-20% per inference (13-15ms), low duty cycle |
| Occupancy state logic | CPU (lightweight) | <5% — simple counting/comparison |
| InsightFace recognition | **CPU** | 1.5s burst per face, only during attendance trigger (not continuous) |
| Camera frame decode (HTTP/MJPEG) | CPU | ~10-15% continuous (single shared thread) |
| Flask web server + video streaming | CPU | ~5-10%, I/O bound |
| ESP32 communication | CPU (network I/O) | Negligible, async HTTP calls |
| ROS 2 middleware (Stage 3 target) | CPU | Est. <5% — lightweight message passing |

**No cloud/host offload is used** — fully edge-deployed on RDK X5 as required.

### ROS 2 Node Graph (Target Design)
/camera_node                    [Planned — wraps camera_manager.py]

└──▶ publishes: /classmind/frames        [sensor_msgs/Image]   ~10-15 Hz

/detection_node                 [Planned — wraps yolo_detector.py]

├──▶ subscribes: /classmind/frames

└──▶ publishes: /classmind/detections     [custom msg: bbox[], confidence[], class_id[]]   ~matches frame rate

/occupancy_node                 [Planned — wraps occupancy_monitor.py]

├──▶ subscribes: /classmind/detections

└──▶ publishes: /classmind/occupancy      [std_msgs/String, JSON: person_count]   event-driven, ~0.1-0.2 Hz

/recognition_node               [Planned — wraps face_recognition.py]

├──▶ subscribes: /classmind/detections (triggered mode)

└──▶ publishes: /classmind/attendance     [std_msgs/String, JSON: name, confidence]   ~0.5-1 Hz during active session

/esp32_bridge_node               [Planned — wraps esp32_controller.py]

└──▶ subscribes: /classmind/occupancy → triggers HTTP relay call

/classmind_bridge (current PoC)  [Validated as proof-of-concept only]

└──▶ CLI-based publish to /classmind/attendance, /classmind/occupancy

(Demonstrates message schema; not yet the production node graph above)

| Topic | Message Type | Publisher | Subscriber | Approx. Rate |
|-------|---------------|------------|-------------|----------------|
| `/classmind/frames` | `sensor_msgs/Image` | camera_node | detection_node | 10-15 Hz |
| `/classmind/detections` | Custom (bbox array) | detection_node | occupancy_node, recognition_node | Matches frame rate |
| `/classmind/occupancy` | `std_msgs/String` (JSON) | occupancy_node | esp32_bridge_node | Event-driven |
| `/classmind/attendance` | `std_msgs/String` (JSON) | recognition_node | (logging node, future dashboard) | ~0.5-1 Hz during session |

---

## Challenge 3 — Engineering Plan

### Bill of Materials (BOM)

| Part | Qty | Supplier/SKU | Notes | Est. Cost |
|------|-----|----------------|-------|-----------|
| D-Robotics RDK X5 (4GB) | 1 | D-Robotics (sponsored) | 10 TOPS BPU, USB-C 5V/5A power | ₹0 (sponsored) |
| Camera — DroidCam (current) | 1 | Existing phone | WiFi stream, 1280x720, validation phase | ₹0 |
| D-Robotics RDK X5 IMX219 120° Camera Module | 1 | D-Robotics distributor | Wide-angle classroom coverage, BPU-native | ₹1,500–₹2,000 |
| ESP32-S3 Dev Board | 1 | Existing | WiFi relay controller | ₹1000 |
| 5V/5A USB-C Power Adapter | 1 | Robu.in / RPi Official | Stable BPU-load power delivery | ₹1,235 |
| MicroSD Card 32GB Class 10 | 1 | Local electronics market | OS storage | ₹1300 |
| 1-Channel Relay Module (5V) | 1 | Robu.in | Light/fan switching from ESP32 | ₹100-150 |
| Jumper wires + breadboard | Set | Local market | GPIO/relay wiring | ₹100-150 |
| **Total (excluding sponsored board)** | | | | **~₹5835** |

### Timeline / Roadmap

| Week | Milestone | Status |
|------|-----------|--------|
| Week 1 | RDK X5 setup, SSH, network, YOLO on BPU, sensor proof (Stage 1) | ✅ Complete |
| Week 2, Day 1 | System architecture design, model evaluation (DeepFace vs InsightFace benchmarking) | ✅ Complete |
| Week 2, Day 2 | Camera resource-sharing fix, occupancy monitor, ESP32 HTTP integration | ✅ Complete |
| Week 2, Day 3 | Flask web app integration, multi-person recognition end-to-end test | ✅ Complete |
| Week 2, Day 4 | ROS 2 proof-of-concept bridge, Stage 2 documentation | ✅ Complete |
| Week 3 | Refactor to proper ROS 2 node graph (camera/detection/recognition/esp32 nodes) | ⏳ Planned |
| Week 3-4 | MIPI camera integration, zone-splitting for 50-student scale testing | ⏳ Planned |
| Week 4 | Real relay + light/fan hardware integration (beyond LED proxy) | ⏳ Planned |
| Week 5 | Demo video, final documentation, Stage 3 submission | ⏳ Planned |

### Risk Analysis

| # | Risk | Mitigation | Trigger to Pivot |
|---|------|-----------|--------------------|
| 1 | Face recognition model too slow on ARM CPU for scale (measured: DeepFace/Facenet at 19s/lookup even with caching) | Benchmarked alternatives on actual hardware; switched to InsightFace (buffalo_s), achieving 1.5s/lookup with in-memory embedding comparison | If InsightFace exceeds 5s/lookup at full 50-student scale, fall back to SFace (faster, lower accuracy) or add zone-based parallel processing |
| 2 | Current ROS 2 integration is a CLI-bridge proof-of-concept, not production-grade middleware | Documented transparently; Stage 3 plan includes refactoring to native ROS 2 nodes (camera/detection/recognition/actuation) as outlined in Node Graph above | If refactor proves too time-intensive, document final architecture honestly as "Flask-orchestrated with ROS 2 telemetry," with clear rationale |
| 3 | Camera resource contention — DroidCam single-connection limit initially broke occupancy monitoring when attendance ran concurrently | Built `camera_manager.py`: single shared capture thread, thread-safe frame buffer for multiple consumers — validated as stable fix | If MIPI camera (Stage 3) has different concurrency behavior, re-test and adapt manager accordingly |
| 4 | False positive detections (e.g. patterned backgrounds misclassified as person/face) | Confidence thresholding (YOLO >0.6, InsightFace similarity threshold ~0.4) | If false-positive rate >15% in real classroom testing, add temporal consistency check (require detection across 3+ consecutive frames) |
| 5 | Limited RAM (4GB, ~800MB free under load) risks OOM kills with heavier models | Selected lightweight models (YOLO11n, InsightFace buffalo_s); confirmed heavier models (VGG-Face) cause OOM in testing | If OOM recurs with scale testing, add swap space or further reduce model footprint |

### GitHub Project Structure
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

*I agree that this showcase document may be used by the Robotics Dream Keeper 
Challenge organizers as described in the official README (promotion, judging, 
and archives).*
