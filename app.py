from flask import Flask, render_template, request, Response, redirect, url_for
import cv2

from ai_engine.config import DROIDCAM_URL
from ai_engine.attendance import AttendanceEngine
from ai_engine.occupancy_monitor import start_occupancy_thread
from ai_engine.camera_manager import camera_manager

# Instead of cap.read(), do:

app = Flask(__name__)

engine = AttendanceEngine()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():

    subject = request.form["subject"]
    classroom = request.form["classroom"]
    duration = int(request.form["duration"])

    engine.start_session(
        subject,
        classroom,
        duration
    )

    return render_template(
        "attendance.html",
        subject=subject,
        classroom=classroom,
        duration=duration
    )


def generate_frames():

    cap = cv2.VideoCapture(DROIDCAM_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE,1)

    while True:

        frame = camera_manager.get_frame()

        if frame is None:
            continue

        # AI runs here
        frame = engine.process_frame(frame)

        _, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )

        if engine.is_finished():
            break

    engine.save_csv()


@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/result")
def result():

    attendance = engine.get_attendance()

    return render_template(
        "result.html",
        attendance=attendance
    )

from flask import jsonify

@app.route("/status")
def status():
    return jsonify({
        "finished": engine.is_finished()
    })

if __name__ == "__main__":
    camera_manager.start()
    start_occupancy_thread()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )