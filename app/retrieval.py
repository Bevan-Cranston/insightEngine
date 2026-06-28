from sentence_transformers import SentenceTransformer
import numpy as np


class SemanticRetriever:
    def __init__(self, embedding_model_name):
        self.embedding_model_name = embedding_model_name
        self.model = SentenceTransformer(self.embedding_model_name)

    def create_embedding(self, text):
        return self.model.encode(text).tolist()

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)

        denominator = (
                np.linalg.norm(a) *
                np.linalg.norm(b)
        )

        if denominator == 0:
            return 0.0

        return np.dot(a, b) / denominator

    def search(self, query, messages, top_k=5):
        query_embedding = query

        scored = []
        for msg in messages:
            if msg.get("embedding") is None:
                continue

            score = self.cosine_similarity(query_embedding, msg["embedding"])
            scored.append({
                **msg,
                "similarity": score,
            })

        return sorted(scored, key=lambda x: x["similarity"], reverse=True)[:top_k]