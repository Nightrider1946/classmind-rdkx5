import cv2
import threading
import time
from ai_engine.config import DROIDCAM_URL

class CameraManager:
    """Single shared camera connection - thread safe frame access."""
    
    def __init__(self, url=DROIDCAM_URL):
        self.url = url
        self.cap = None
        self.latest_frame = None
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        self.cap = cv2.VideoCapture(self.url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.running = True
        thread = threading.Thread(target=self._update_loop, daemon=True)
        thread.start()
        print("[CameraManager] Started")

    def _update_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                with self.lock:
                    self.latest_frame = frame
            else:
                print("[CameraManager] Frame read failed, retrying...")
                time.sleep(1)

    def get_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
            return None

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

# Single global instance shared across the whole app
camera_manager = CameraManager()