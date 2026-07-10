import cv2
import csv
import time
import os
from datetime import datetime

from .yolo_detector import YOLODetector
from .face_recognition import FaceRecognizer
from ai_engine.camera_manager import camera_manager
from ai_engine.config import ATTENDANCE_LOG

from ai_engine.esp32_controller import (
    attendance_start_beep,
    attendance_end_beep,
)

class AttendanceEngine:

    def __init__(self):

        self.yolo = YOLODetector()
        self.recognizer = FaceRecognizer()

        self.attendance = {}
        self.subject = ""
        self.classroom = ""
        self.duration = 20
        self.start_time = None

        self.end_beep_sent = False


    # ----------------------------
    # Called once when teacher clicks START
    # ----------------------------
    def start_session(self, subject, classroom, duration):

        self.subject = subject
        self.classroom = classroom
        self.duration = duration

        self.attendance = {}
        self.end_beep_sent = False
        self.start_time = time.time()


        print("Attendance Session Started")
        attendance_start_beep()

    # ----------------------------
    # Called for EVERY video frame
    # ----------------------------
    def process_frame(self, frame):

        persons = self.yolo.detect_people(frame)

        for person in persons:

            x1, y1, x2, y2 = person["bbox"]

            crop = frame[y1:y2, x1:x2]

            if crop.size == 0:
                continue

            name, score = self.recognizer.recognize(crop)

            # Ignore unknown people
            if name in ["Unknown", "No Face"]:
                continue

            # Keep highest confidence
            if (
                name not in self.attendance
                or score > self.attendance[name]
            ):
                self.attendance[name] = score

            # Draw Bounding Box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                f"{name} {score:.2f}",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

        return frame

    # ----------------------------
    # Remaining time
    # ----------------------------
    def remaining_time(self):

        elapsed = time.time() - self.start_time

        return max(
            0,
            self.duration - int(elapsed)
        )

    # ----------------------------
    # Is attendance completed?
    # ----------------------------
    def is_finished(self):

        if self.start_time is None:
            return False

        finished = (
            time.time() - self.start_time
        ) >= self.duration

        # Send end beep only once
        if finished and not self.end_beep_sent:

            attendance_end_beep()

            self.end_beep_sent = True

            print("Attendance Session Completed")

        return finished

    # ----------------------------
    # Return attendance dictionary
    # ----------------------------
    def get_attendance(self):

        return self.attendance

    # ----------------------------
    # Save CSV
    # ----------------------------
    def save_csv(self):

        os.makedirs(
            ATTENDANCE_LOG,
            exist_ok=True
        )

        filename = os.path.join(
            ATTENDANCE_LOG,
            datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
        )

        with open(filename,"w",newline="") as f:

            writer = csv.writer(f)

            writer.writerow(
                ["Subject",self.subject]
            )

            writer.writerow(
                ["Classroom",self.classroom]
            )

            writer.writerow([])

            writer.writerow(
                ["Student","Confidence"]
            )

            for name,score in self.attendance.items():

                writer.writerow(
                    [name,round(score,3)]
                )

        print("Saved:",filename)