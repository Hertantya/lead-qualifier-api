"""pgvector-backed storage for document chunks and their embeddings.

pgvector is just a Postgres extension: chunks live in an ordinary table with
one extra VECTOR column, and similarity search is a normal SQL ORDER BY.
"""
from typing import LiteralString, cast

import psycopg
from pgvector.psycopg import register_vector

from app import config
from app.rag.chunking import Chunk

EMBEDDING_DIM = 1536  # text-embedding-3-small


def get_connection() -> psycopg.Connection:
    conn = psycopg.connect(config.DATABASE_URL, autocommit=True)
    # The vector type must exist in the database before we can register it on
    # this connection, so ensure the extension first (idempotent + cheap).
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    return conn


def init_schema(conn: psycopg.Connection) -> None:
    # EMBEDDING_DIM is a hardcoded internal constant, not user input, so
    # interpolating it into the DDL is safe despite the f-string losing its
    # LiteralString type.
    query = cast(
        LiteralString,
        f"""
        CREATE TABLE IF NOT EXISTS doc_chunks (
            id SERIAL PRIMARY KEY,
            source TEXT NOT NULL,
            chunk_index INT NOT NULL,
            text TEXT NOT NULL,
            embedding VECTOR({EMBEDDING_DIM}) NOT NULL
        )
        """,
    )
    conn.execute(query)


def insert_chunks(conn: psycopg.Connection, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    with conn.cursor() as cur:
        for chunk, embedding in zip(chunks, embeddings):
            cur.execute(
                "INSERT INTO doc_chunks (source, chunk_index, text, embedding) VALUES (%s, %s, %s, %s)",
                (chunk.source, chunk.index, chunk.text, embedding),
            )


def search(conn: psycopg.Connection, query_embedding: list[float], top_k: int = 4) -> list[dict]:
    """Nearest-neighbor search using pgvector's cosine-distance operator (<=>)."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT source, chunk_index, text
            FROM doc_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (query_embedding, top_k),
        )
        rows = cur.fetchall()
    return [{"source": r[0], "chunk_index": r[1], "text": r[2]} for r in rows]
