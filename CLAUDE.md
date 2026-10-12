# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -r requirements.txt          # use .venv (Windows: .venv\Scripts\activate)
uvicorn app.main:app --reload            # dev server, Swagger at http://127.0.0.1:8000/docs
pytest -q                                # full suite (what CI runs, Python 3.12)
pytest tests/test_qualify.py::test_name  # single test
docker compose up --build                # Postgres+pgvector and the API
python -m scripts.ingest_docs            # chunk/embed docs/*.md into pgvector (needed before /ask works)
```

No linter or formatter is configured.

## Architecture

A FastAPI service that uses the OpenAI SDK directly. LangChain and other agent frameworks are left out on purpose, so don't add them. Every LLM call goes through `app.llm.get_client()`. It builds the client lazily, so importing a module never needs an API key. `OPENAI_BASE_URL` lets the same code target any OpenAI-compatible endpoint.

Request flow: `app/main.py` → `app/routers/*` (thin, one call each) → logic in `app/llm.py`, `app/rag/qa.py` or `app/agent/loop.py`. Request and response schemas live in `app/models.py`.

There are three LLM patterns, and they share one shape:
- **Structured output**: `client.beta.chat.completions.parse(response_format=<PydanticModel>)`. A `None` parsed result is treated as a refusal and raises `ValueError`.
- **Tool loop** (`qualify_lead_with_tools` in `app/llm.py`, `research_lead` in `app/agent/loop.py`): call with `tools=`, run any `tool_calls` locally through a `_AVAILABLE_TOOLS` name→function dict, add `role: "tool"` messages, and repeat up to `max_turns`. Then make a final `parse` call for the structured answer. The two loops are separate copies. If you change one, check whether the other needs the same change.
- **RAG** (`app/rag/`): `chunking` → `embeddings` → `store` (raw psycopg + pgvector, table `doc_chunks`, cosine `<=>`) → `qa` (stuffs the top-k chunks tagged `[source:index]` into the prompt). `EMBEDDING_DIM = 1536` in `store.py` is tied to `text-embedding-3-small`, so changing the embedding model means changing the schema too. `ingest_docs` only appends rows, so running it again duplicates chunks.

The tools (`_lookup_company_firmographics`, `_search_company_info`) are mocked with hardcoded dicts that stand in for real enrichment APIs.

Config comes only from environment variables, through `app/config.py` (python-dotenv loads `.env`). See `.env.example`.

## Tests

The tests use `TestClient` and monkeypatch the function **as imported into the router module** (e.g. `app.routers.ask.rag_ask`, `app.routers.agent.research_lead`), not where it is defined. This way no network, API key or database is needed. Write new endpoint tests the same way.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
