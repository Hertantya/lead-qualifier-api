"""Chunk every markdown file in docs/, embed the chunks, and store them in pgvector.

Run with: python -m scripts.ingest_docs
(requires Postgres with the pgvector extension running — see docker-compose.yml)
"""
from pathlib import Path

from app.rag import store
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_texts

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"


def main() -> None:
    conn = store.get_connection()
    try:
        store.init_schema(conn)

        all_chunks = []
        for path in sorted(DOCS_DIR.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            all_chunks.extend(chunk_text(text, source=path.name))

        if not all_chunks:
            print(f"No markdown files found in {DOCS_DIR}")
            return

        embeddings = embed_texts([c.text for c in all_chunks])
        store.insert_chunks(conn, all_chunks, embeddings)
        print(f"Ingested {len(all_chunks)} chunk(s) from {DOCS_DIR}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
