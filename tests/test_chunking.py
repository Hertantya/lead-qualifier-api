from app.rag.chunking import chunk_text


def test_chunk_text_splits_long_input_into_multiple_chunks():
    paragraphs = [f"Paragraph {i} " + ("word " * 30) for i in range(10)]
    text = "\n\n".join(paragraphs)

    chunks = chunk_text(text, source="doc.md", chunk_size=200, overlap=20)

    assert len(chunks) > 1
    assert all(c.source == "doc.md" for c in chunks)
    assert [c.index for c in chunks] == list(range(len(chunks)))


def test_chunk_text_keeps_short_input_as_one_chunk():
    text = "Just one short paragraph."

    chunks = chunk_text(text, source="short.md")

    assert len(chunks) == 1
    assert chunks[0].text == text
