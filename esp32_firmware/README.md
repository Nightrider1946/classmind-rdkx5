# ClassMind — ESP32 Firmware

ESP32 firmware (PlatformIO + Arduino framework, C++) that exposes 
HTTP endpoints for relay/LED control, used by ClassMind's occupancy 
monitoring system running on RDK X5.

## Endpoints
- `GET /led/on` — turns relay/LED ON (occupied state)
- `GET /led/off` — turns relay/LED OFF (unoccupied state)

## Build & Flash
```bash
pio run --target upload
```

## Hardware
- ESP32 Dev Board
- Built-in RGB LED (for development/testing)
- Relay module (Stage 3 — real light/fan control)

Communicates with RDK X5 over local WiFi via HTTP (same network).
