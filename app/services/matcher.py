from app.services.embedder import Embedder
from app.services.vector_store import VectorStore


embedder = Embedder()
vector_store = VectorStore()


class Matcher:

    def add_candidate(self, profile_text, meta):

        vec = embedder.embed(profile_text)

        vector_store.add(vec, meta)

    def match_jd(self, jd_text):

        jd_vec = embedder.embed(jd_text)

        return vector_store.search(jd_vec)
