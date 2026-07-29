"""Wraps OpenAI's embeddings endpoint."""
from app import config
from app.llm import get_client


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = get_client()
    response = client.embeddings.create(model=config.OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]
