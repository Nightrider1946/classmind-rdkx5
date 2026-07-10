# ClassMind Face Enrollment Images

This directory stores local student face images used to generate the ClassMind recognition database.

Create one directory for each student:

```text
classmind_faces/
├── Narendra/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
├── Student_2/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── 3.jpg
```

Each enrollment image should contain exactly one clearly visible face.

Multiple images with variations in face angle and lighting are recommended.

Generate the local InsightFace embedding database using:

```bash
python3 scripts/enroll_faces.py
```

The generated database is stored at:

```text
database/insightface_db.pkl
```

Student face images and generated biometric embeddings are deployment-specific and are excluded from the public repository.
