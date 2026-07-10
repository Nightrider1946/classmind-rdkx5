import os
import pickle

import cv2
import insightface


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLASSMIND_DIR = os.path.dirname(SCRIPT_DIR)

FACE_DB = os.path.join(
    CLASSMIND_DIR,
    "classmind_faces"
)

DATABASE_DIR = os.path.join(
    CLASSMIND_DIR,
    "database"
)

DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "insightface_db.pkl"
)


print("========================================")
print(" ClassMind Face Enrollment")
print("========================================")

print(f"\nFace image directory: {FACE_DB}")
print(f"Database output: {DATABASE_FILE}")


if not os.path.isdir(FACE_DB):
    print("\nERROR: classmind_faces directory not found.")
    print("\nExpected structure:")
    print("""
classmind_faces/
├── Student_Name_1/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
└── Student_Name_2/
    ├── 1.jpg
    ├── 2.jpg
    └── 3.jpg
""")
    raise SystemExit(1)


print("\nLoading InsightFace buffalo_s...")

app = insightface.app.FaceAnalysis(
    name="buffalo_s"
)

app.prepare(
    ctx_id=-1,
    det_size=(640, 640)
)


database = {}


for student_name in sorted(os.listdir(FACE_DB)):

    student_path = os.path.join(
        FACE_DB,
        student_name
    )

    if not os.path.isdir(student_path):
        continue

    print(f"\nProcessing student: {student_name}")

    embeddings = []


    for image_name in sorted(os.listdir(student_path)):

        image_path = os.path.join(
            student_path,
            image_name
        )

        image = cv2.imread(image_path)

        if image is None:
            print(f"  SKIPPED: Unable to read {image_name}")
            continue

        faces = app.get(image)

        if len(faces) == 0:
            print(f"  SKIPPED: No face found in {image_name}")
            continue

        if len(faces) > 1:
            print(f"  SKIPPED: Multiple faces found in {image_name}")
            continue

        embeddings.append(
            faces[0].embedding
        )

        print(f"  Added: {image_name}")


    if embeddings:

        database[student_name] = embeddings

        print(
            f"Student enrolled: {student_name}"
        )

        print(
            f"Valid embeddings: {len(embeddings)}"
        )

    else:

        print(
            f"WARNING: No valid embeddings for {student_name}"
        )


if not database:

    print("\nERROR: No students were enrolled.")
    print("Database was not created.")

    raise SystemExit(1)


os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)


with open(
    DATABASE_FILE,
    "wb"
) as database_file:

    pickle.dump(
        database,
        database_file
    )


print("\n========================================")
print(" Face Enrollment Complete")
print("========================================")

print(f"\nStudents enrolled: {len(database)}")


for student_name, embeddings in database.items():

    print(
        f"  {student_name}: {len(embeddings)} embedding(s)"
    )


print("\nDatabase saved to:")
print(DATABASE_FILE)