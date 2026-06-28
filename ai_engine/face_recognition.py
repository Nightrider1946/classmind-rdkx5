import pickle
import numpy as np
import insightface

from .config import DATABASE


class FaceRecognizer:

    def __init__(self):

        self.face_app = insightface.app.FaceAnalysis(
            name="buffalo_s"
        )

        self.face_app.prepare(
            ctx_id=-1,
            det_size=(640,640)
        )

        with open(DATABASE, "rb") as f:
            self.database = pickle.load(f)

    def recognize(self, image):

        faces = self.face_app.get(image)

        if len(faces) == 0:
            return "No Face", 0

        embedding = faces[0].embedding

        best_name = "Unknown"
        best_score = -1

        for student, embeddings in self.database.items():

            for db_embedding in embeddings:

                score = np.dot(
                    embedding,
                    db_embedding
                ) / (
                    np.linalg.norm(embedding)
                    *
                    np.linalg.norm(db_embedding)
                )

                if score > best_score:

                    best_score = score
                    best_name = student

        if best_score < 0.45:
            return "Unknown", best_score

        return best_name, best_score