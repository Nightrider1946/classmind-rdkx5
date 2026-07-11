# ClassMind — Smart Classroom Intelligence System

- **Participant:** Narendra Andhale
- **Stage completed:** 3
- **Repository:** https://github.com/Nightrider1946/classmind-rdkx5
- **Demo video:** https://youtu.be/Bc0XRAdNyIA
- **Community post:** https://discord.com/channels/1300358874280230994/1511596144327659682/1525469212104069152

## Summary

ClassMind is an end-to-end intelligent classroom system on RDK X5
combining BPU-accelerated person detection, CPU face recognition,
ROS 2 sensor fusion, IoT energy automation, and a Flask teacher portal.

One command starts the entire system: ./launch_classmind.sh

Stage 3 adds: MQ environmental sensor via ESP32 ADC, ROS 2 sensor
bridge publishing /classmind/gas, ROS 2 Decision Node with 10-sample
baseline calibration and alert threshold, startup actuator reset,
unified launcher with graceful shutdown.

## Technical Highlights

- **Board:** RDK X5 4GB, RDKOS 3.5.0
- **AI:** YOLO11n BPU (13-15ms, hbm_runtime); InsightFace 
  buffalo_s CPU (1.5s/person, ArcFace)
- **ROS 2:** sensor_bridge node + decision node; 
  /classmind/gas topic (std_msgs/String, 2s interval)
- **Multi-task:** BPU YOLO continuous + CPU InsightFace 
  triggered + ROS 2 MQ bridge async — all concurrent
- **Sensors:** DroidCam/phone (vision) + MQ-series analog 
  (environmental, via ESP32 ADC + voltage divider)
- **Actuators:** ESP32 relay (light/fan), buzzer 
  (attendance signal), RGB LED (environmental alert)
- **Safety:** Startup actuator reset, 10s alert hold, 
  graceful SIGINT shutdown

## Links & Evidence

- **Demo video:** https://youtu.be/Bc0XRAdNyIA
- **Release:** v1.0-demo
- **Quick Start:** README.md
- **Architecture:** docs/STAGE3.md
- **Benchmark:** docs/benchmark.md
- **ROS 2 package:** classmind_ws_ros/
- **Stage 2 Proposal:** docs/PROPOSAL.md
- **BOM:** hardware/BOM.md

---

I agree that this showcase document may be used by the Robotics 
Dream Keeper Challenge organizers as described in the official 
README (promotion, judging, and archives).
