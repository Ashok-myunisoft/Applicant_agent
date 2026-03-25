import faiss
import numpy as np


class VectorStore:

    def __init__(self, dim=1536):

        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, embedding, meta):

        vec = np.array([embedding]).astype("float32")
        self.index.add(vec)

        self.metadata.append(meta)

    def search(self, embedding, k=5):

        q = np.array([embedding]).astype("float32")

        scores, indices = self.index.search(q, k)

        results = []

        for i, score in zip(indices[0], scores[0]):

            if i == -1:
                continue

            results.append({
                "candidate": self.metadata[i],
                "similarity_score": float(score)
            })

        return results
