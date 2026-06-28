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
