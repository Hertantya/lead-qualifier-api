"""Retrieval-augmented answering with citations: the /ask endpoint's logic."""
from app import config
from app.llm import get_client
from app.models import AskResponse, Citation
from app.rag import store
from app.rag.embeddings import embed_texts

ASK_SYSTEM_PROMPT = (
    "Answer the user's question using ONLY the provided context chunks. "
    "If the answer isn't in the context, say you don't know. "
    "Cite chunks inline using their [source:index] tag."
)


def ask(question: str, top_k: int = 4) -> AskResponse:
    conn = store.get_connection()
    try:
        query_embedding = embed_texts([question])[0]
        matches = store.search(conn, query_embedding, top_k=top_k)
    finally:
        conn.close()

    context = "\n\n".join(f"[{m['source']}:{m['chunk_index']}] {m['text']}" for m in matches)

    client = get_client()
    completion = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": ASK_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    answer = completion.choices[0].message.content or ""

    citations = [
        Citation(source=m["source"], chunk_index=m["chunk_index"], text=m["text"]) for m in matches
    ]
    return AskResponse(answer=answer, citations=citations)
