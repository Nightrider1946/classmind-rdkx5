# 🚀 RDK X5 Ignite Challenge — Stage 1 

**Participant:** Narendra Andhale

**Board:** RDK X5 4GB

**Completion Date:** June 17, 2026

---

# Stage 1 — Ignite Challenge Evidence

## Challenge 1 — Board Bring-Up

### System Setup

* Successfully flashed **RDK OS 3.5.0 Desktop** using **RDK Studio**.
* Verified successful boot and desktop environment.

### Network Connectivity

* Connected the board to WiFi.
* Verified internet connectivity using:

```bash
ping -c 4 google.com
```

### Remote Development

* Enabled SSH on the board.
* Connected remotely from my laptop using VS Code Remote SSH.
* Verified system information using:

```bash
uname -a
htop
```
![SSH LOGIN](https://github.com/Nightrider1946/classmind-rdkx5/blob/main/assets/stage1_ssh_login.png)
This allowed me to develop directly on the RDK X5 from my laptop.

---
## Challenge 2 — Sensor Explorer

### Sensor Selection

For this challenge, I chose to use a **camera as the primary sensor** instead of a GPIO-based sensor.

My long-term project is an **AI-powered attendance system (ClassMind)**, where the camera is the main sensing device. Therefore, I focused on integrating and validating the vision sensor first.

Initially, I planned to demonstrate a GPIO sensor, but I decided to prioritize the camera because it is the core sensor required for my final project. I used my Android phone as a wireless camera through **DroidCam** to begin development while waiting for an official **MIPI CSI camera** to become available.

### Camera Integration

* Connected an Android phone using DroidCam over WiFi.
* Successfully accessed the video stream through OpenCV.
* Verified image acquisition and frame processing on the RDK X5.
* Used the captured images for subsequent AI inference on the BPU.
![CAMERA](https://github.com/Nightrider1946/classmind-rdkx5/blob/main/assets/stage1_camera_setup.png)
### Future Improvement

I plan to replace the DroidCam setup with an **official MIPI CSI camera**, which will provide lower latency, better integration, and a production-ready vision pipeline for future robotics and computer vision projects.

---

## Challenge 3 — First AI Inference on BPU

### Objective

Run an official YOLO model on the **RDK X5 BPU** using the D-Robotics Model Zoo.

### Model Used

* YOLO11n Detect
* BPU Optimized (.bin Model)

### Runtime

Used the official **Ultralytics YOLO Runtime** provided in the D-Robotics Model Zoo.

### Test Performed

Instead of using only the default sample image (`bus.jpg`), I successfully performed inference on my own image.

Command used:

```bash
python3 main.py \
--task detect \
--test-img ~/my_photo.jpg \
--img-save-path ~/my_result.jpg
```

### Result

The model successfully detected a person in the image.

Measured inference timings:

| Stage           | Time   |
| --------------- | ------ |
| Pre-processing  | ~10 ms |
| BPU Inference   | ~13 ms |
| Post-processing | ~6 ms  |

Total inference time was approximately **29 ms**, demonstrating real-time capable performance.

![YOLO](https://github.com/Nightrider1946/classmind-rdkx5/blob/main/assets/stage1_yolo_bpu.png)
---

# What I Learned

During this stage I learned much more than simply running a demo.

I explored how the official D-Robotics Model Zoo is organized and understood the role of:

* Model files (.bin)
* Runtime
* BPU inference
* Pre-processing
* Post-processing
* Output tensors
* Detection pipeline

I also studied how the runtime is structured and how the `main.py` script coordinates the complete inference process.

This helped me understand the workflow:

Image → Pre-processing → BPU Inference → Output Tensors → Post-processing → Detection Result

instead of treating the runtime as a black box.

---

# Tools & Technologies

* RDK X5
* RDK OS 3.5.0
* Python 3
* OpenCV
* D-Robotics Model Zoo
* Ultralytics YOLO Runtime
* BPU Inference
* VS Code Remote SSH
* DroidCam

---



