# ClassMind — Smart Classroom Intelligence System

- **Participant:** Narendra Andhale
- **Stage completed:** 2
- **Repository:** https://github.com/Nightrider1946/classmind-rdkx5
- **Demo video:** N/A (Stage 2 is documentation-focused; demo video planned for Stage 3)
- **Community post:** https://discord.com/channels/1300358874280230994/1511596144327659682/1511596144327659682

## Summary

ClassMind is an intelligent classroom management system built on RDK X5 
that solves two real problems faced by every college  manual attendance 
and energy waste in empty classrooms. A camera feed is processed through 
YOLO11n running on the RDK X5 BPU (13-15ms inference, 91% confidence 
validated) to detect people. Detected faces are cropped and matched 
against a student database using InsightFace (buffalo_s) for attendance 
(1.5s per recognition, multi-person validated). A background occupancy 
monitor uses the same detection pipeline to control classroom lights/fan 
via an ESP32 relay over WiFi/HTTP. A Flask web dashboard lets teachers 
select subject/class, view the live feed, trigger attendance capture, 
and review results.

In Stage 2, I moved from "running demos" to a fully designed system 
architecture, backed by real on-device benchmarking: I tested two face 
recognition approaches (DeepFace and InsightFace) directly on RDK X5 
hardware, measured a 19s vs 1.5s recognition time difference, and 
selected InsightFace based on that evidence not assumptions. I also 
identified and fixed a real engineering problem (camera resource 
contention between concurrent consumers) with a custom shared 
camera-manager thread. Stage 2 deliverables include complete system 
architecture, module design with failure modes, BPU/CPU compute 
allocation, ROS 2 node graph (with honest current-status vs target-state 
documentation), BOM, week-by-week roadmap, and risk analysis.

## Technical Highlights

- **Board:** RDK X5 (4GB), RDKOS 3.5.0, BPU-accelerated inference
- **AI:** YOLO11n (BPU, 13-15ms, 91% confidence) for person/face 
  detection; InsightFace buffalo_s (CPU, 1.5s/match) for recognition 
  selected after benchmarking against DeepFace (19s/match, rejected)
- **Sensors/Actuators:** DroidCam (current dev camera), ESP32 (WiFi/HTTP 
  relay control for lights/fan, occupancy-triggered)
- **System:** Flask web dashboard, shared thread-safe camera manager 
  (solves multi-consumer camera conflict), attendance CSV logging
- **ROS 2:** Proof-of-concept bridge validating `/classmind/attendance` 
  and `/classmind/occupancy` topic/message design; full node graph 
  (camera/detection/recognition/actuation nodes) designed and planned 
  for Stage 3

## Links & Evidence

- Stage 2 Proposal (Architecture, BOM, Risk Analysis): [docs/PROPOSAL.md](docs/PROPOSAL.md)
- Roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)
- Bill of Materials: [hardware/BOM.md](hardware/BOM.md)
- Working source code: [app.py](app.py), [ai_engine/](ai_engine/)
- ESP32 firmware: [esp32_firmware/](esp32_firmware/)
- Stage 1 evidence: [docs/STAGE1.md](docs/STAGE1.md)

---

I agree that this showcase document may be used by the Robotics Dream 
Keeper Challenge organizers as described in the official README 
(promotion, judging, and archives).
