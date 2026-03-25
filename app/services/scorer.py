import json
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_fixed

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from app.config import settings


PROMPT_PATH = Path("app/prompts/scoring_prompt.txt")


def load_prompt():
    return PROMPT_PATH.read_text()


class ScoringAgent:

    def __init__(self):

        if not settings.OPENAI_KEY:
            raise ValueError("OPENAI_API_KEY not set")

        self.llm = ChatOpenAI(
            model=settings.MODEL,
            api_key=settings.OPENAI_KEY,
            temperature=0,
            timeout=30
        )

        system_prompt = load_prompt()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{profile}")
        ])

        # LCEL chain (new standard)
        self.chain = self.prompt | self.llm

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def score(self, profile: str) -> dict:

        response = self.chain.invoke({
            "profile": profile
        })

        return json.loads(response.content)
