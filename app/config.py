"""App configuration, read from environment variables. Never hardcode secrets here."""
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://vault:vault@localhost:5432/leadqualifier"
)
