import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_ZOO = os.getenv(
    "CLASSMIND_MODEL_ZOO",
    os.path.join(
        BASE_DIR,
        "third_party",
        "rdk_model_zoo"
    )
)

YOLO_MODEL = os.path.join(
    MODEL_ZOO,
    "samples",
    "vision",
    "ultralytics_yolo",
    "model",
    "yolo11n_detect_bayese_640x640_nv12.bin"
)

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "insightface_db.pkl"
)

DROIDCAM_URL = "http://10.139.104.86:4747/video"

ATTENDANCE_LOG = os.path.join(
    BASE_DIR,
    "attendance_logs"
)

ESP32_IP = "10.139.104.208"