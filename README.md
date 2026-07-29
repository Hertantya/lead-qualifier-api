# lead-qualifier-api

An LLM-powered lead qualification service, built as a FastAPI app: structured
outputs, tool use (function calling), a from-scratch RAG pipeline over pgvector,
and a hand-rolled agent loop. No LangChain/LangGraph/CrewAI — every abstraction
here is one you can read top to bottom.

## Endpoints

| Method | Path                     | What it does                                                              |
|--------|--------------------------|----------------------------------------------------------------------------|
| GET    | `/health`                | Liveness check                                                             |
| POST   | `/qualify-lead`          | Scores a lead 1-10 from a free-text description (structured output only)  |
| POST   | `/qualify-lead/with-tools` | Same, but the model calls a `lookup_company_firmographics` tool first    |
| POST   | `/ask`                   | RAG: answers a question from `docs/*.md` with citations                   |
| POST   | `/research-lead`         | Sales-research agent: researches a company, drafts an outreach email      |

## Architecture

```
app/
├── config.py       # env vars only — never hardcode secrets
├── models.py        # Pydantic request/response schemas
├── llm.py            # OpenAI wrapper: structured outputs + tool use
├── main.py            # FastAPI app, wires up routers
├── rag/
│   ├── chunking.py    # paragraph-aware text chunking
│   ├── embeddings.py  # OpenAI embeddings call
│   ├── store.py       # pgvector schema + similarity search
│   └── qa.py          # retrieve -> prompt -> answer with citations
├── agent/
│   └── loop.py        # raw while-loop agent: LLM + tools, no framework
└── routers/           # one file per endpoint group
```

## Running locally (without Docker)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env            # then edit .env and set your real OPENAI_API_KEY
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive Swagger UI.

The `/ask` endpoint needs a running Postgres with pgvector (see Docker section
below) and an ingested knowledge base:

```bash
python -m scripts.ingest_docs
```

## Running everything with Docker Compose

```bash
docker compose up --build
```

This starts Postgres (with the pgvector extension) and the API together. Set
`OPENAI_API_KEY` in your shell (or a `.env` file next to `docker-compose.yml`)
before running it — Compose reads it from the environment.

Then ingest the sample docs into the running Postgres container:

```bash
docker compose exec app python -m scripts.ingest_docs
```

## Tests

```bash
pytest -q
```

All LLM calls are mocked in tests (via `monkeypatch` on the router-level
functions), so the suite runs with no API key and no network access. CI
(`.github/workflows/ci.yml`) runs the same suite on every push.

## Deploying

Both routes below need a Postgres+pgvector instance too — Railway and Fly.io
both offer managed Postgres, or use any pgvector-compatible Postgres add-on.

**Railway** (no config file needed — it detects the `Dockerfile`):
1. `railway login`, then `railway init` in this folder.
2. Add a Postgres plugin from the Railway dashboard (or bring your own pgvector-enabled Postgres).
3. `railway variables set OPENAI_API_KEY=... DATABASE_URL=...`
4. `railway up`

**Fly.io** (a starter `fly.toml` is included):
1. `fly launch --no-deploy` to confirm/adjust the app name and region.
2. `fly secrets set OPENAI_API_KEY=... DATABASE_URL=...`
3. `fly deploy`

Both of these require your own Railway/Fly.io account and are left for you to
run — I can prep the config but shouldn't create paid cloud resources or
deployments on your behalf without you driving it.

## Design notes (why it's built this way)

- **Structured outputs** (`/qualify-lead`) use `client.beta.chat.completions.parse`
  with a Pydantic `response_model` — the SDK validates the model's JSON against
  the schema before your code ever sees it.
- **Tool use** (`/qualify-lead/with-tools`, `/research-lead`) follows the same
  loop every agent framework builds on: call the model with `tools=[...]`, and
  if it responds with `tool_calls`, execute them locally, append the results as
  `role: "tool"` messages, and call the model again. Repeat until it stops
  asking for tools, then ask for the final structured answer.
- **RAG is hand-built**, not a framework: chunk -> embed -> store in pgvector ->
  cosine-similarity search -> stuff the top chunks into the prompt -> ask the
  model to answer only from that context and cite sources.
- **Secrets** only ever come from environment variables (`app/config.py`), never
  from code — `.env` is git-ignored, `.env.example` documents what's needed.
