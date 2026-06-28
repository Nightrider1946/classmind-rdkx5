import time
import threading
from ai_engine.camera_manager import camera_manager
from ai_engine.yolo_detector import YOLODetector
from ai_engine.esp32_controller import set_light

yolo = YOLODetector()

def occupancy_loop(check_interval=5):
    last_state = None

    while True:
        frame = camera_manager.get_frame()
        if frame is None:
            time.sleep(2)
            continue

        persons = yolo.detect_people(frame)
        person_count = len(persons)
        current_state = person_count > 0

        if current_state != last_state:
            set_light(current_state)
            last_state = current_state

        print(f"[Occupancy] {person_count} person(s) — Light: {'ON' if current_state else 'OFF'}")
        time.sleep(check_interval)

def start_occupancy_thread():
    thread = threading.Thread(target=occupancy_loop, daemon=True)
    thread.start()
    print("Occupancy monitor thread started")