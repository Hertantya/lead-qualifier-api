"""Turn raw documents into overlapping text chunks suitable for embedding."""
from dataclasses import dataclass


@dataclass
class Chunk:
    source: str
    index: int
    text: str


def chunk_text(text: str, source: str, chunk_size: int = 800, overlap: int = 100) -> list[Chunk]:
    """Pack paragraphs into ~chunk_size windows, carrying a small overlap between windows
    so an answer near a chunk boundary doesn't get cut off from its context."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[Chunk] = []
    buffer = ""

    for para in paragraphs:
        if buffer and len(buffer) + len(para) + 1 > chunk_size:
            chunks.append(Chunk(source=source, index=len(chunks), text=buffer.strip()))
            buffer = buffer[-overlap:] + "\n" + para
        else:
            buffer = f"{buffer}\n{para}" if buffer else para

    if buffer.strip():
        chunks.append(Chunk(source=source, index=len(chunks), text=buffer.strip()))

    return chunks
