import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    TEMP_DIR = os.getenv("TEMP_DIR", "temp")


settings = Settings()
