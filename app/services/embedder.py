from langchain_openai import OpenAIEmbeddings
from app.config import settings


class Embedder:

    def __init__(self):

        self.model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_KEY
        )

    def embed(self, text: str):

        return self.model.embed_query(text)
