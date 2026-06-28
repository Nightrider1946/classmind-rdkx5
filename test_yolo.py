import cv2

from ai_engine.config import DROIDCAM_URL
from ai_engine.yolo_detector import YOLODetector

yolo = YOLODetector()

cap = cv2.VideoCapture(DROIDCAM_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

ret, frame = cap.read()
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

if not ret:
    print("Camera not working")
    exit()


persons = yolo.detect_people(frame)

print(persons)

cap.release()