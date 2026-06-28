from ai_engine.attendance import AttendanceEngine

engine = AttendanceEngine()

attendance = engine.start(
    subject="Operating Systems",
    classroom="C-201",
    duration=20
)

print(attendance)