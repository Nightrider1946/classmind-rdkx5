import cv2

from ai_engine.config import DROIDCAM_URL
from ai_engine.yolo_detector import YOLODetector
from ai_engine.face_recognition import FaceRecognizer

cap = cv2.VideoCapture(DROIDCAM_URL)

ret, frame = cap.read()

cap.release()

if not ret:
    print("Camera Error")
    exit()

yolo = YOLODetector()
recognizer = FaceRecognizer()

persons = yolo.detect_people(frame)

print(f"Detected {len(persons)} person(s)")

for person in persons:

    name, score = recognizer.recognize(person["crop"])

    print("---------------------")
    print("Name :", name)
    print("Score:", round(score,3))