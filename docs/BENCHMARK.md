# ClassMind — Benchmark Evidence

## BPU Inference (YOLO11n)

**Model:** yolo11n_detect_bayese_640x640_nv12.bin
**Runtime:** hbm_runtime (D-Robotics BPU SDK)
**Board:** RDK X5 4GB, RDKOS 3.5.0

| Metric | Value |
|--------|-------|
| Pre-process time | 10–17ms |
| Forward time (BPU) | **13–15ms** |
| Post-process time | 6–13ms |
| Input resolution | 640×640 |
| Detection confidence (person) | 91% (validated on test subject) |
| BPU cores | [0] |
| Mode | Continuous real-time stream |

See: assets/stage1_yolo_bpu_terminal.png

## CPU Inference (InsightFace)

**Model:** buffalo_s (ArcFace, 512-dim)
**Runtime:** ONNX Runtime (CPU)

| Metric | Value |
|--------|-------|
| Recognition time (cached embeddings) | ~1.5s/person |
| Cosine similarity range (validated) | 0.665 – 0.762 |
| Simultaneous persons tested | 2 |
| Trigger mode | Session-triggered (not continuous) |

## MQ Sensor Bridge

| Metric | Value |
|--------|-------|
| Poll interval | 2 seconds |
| Baseline calibration samples | 10 |
| Alert threshold | ADC delta >= 250 |
| Alert hold duration | 10 seconds |

## Memory Profile

| State | Used RAM | Free RAM |
|-------|----------|----------|
| System idle | ~1.6GB | ~1.4GB |
| Full ClassMind running | ~2.0–2.4GB | ~600MB–1GB |

## Model Selection Evidence

| Model | Lookup Time | Accuracy | Decision |
|-------|------------|---------|---------|
| DeepFace Facenet | 19–20s (even cached) | High | ❌ Too slow |
| DeepFace SFace | 2–3s | 64% confidence | ❌ Low accuracy |
| InsightFace buffalo_s | **1.5s** | 0.665–0.762 | ✅ Selected |
