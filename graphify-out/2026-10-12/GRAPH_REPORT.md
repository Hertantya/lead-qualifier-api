# Graph Report - lead-qualifier-api  (2026-10-12)

## Corpus Check
- Corpus is ~10,958 words - fits in a single context window. You may not need a graph.

## Summary
- 133 nodes · 285 edges · 10 communities (7 shown, 3 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.89)
- Token cost: 87,884 input · 0 output

## Community Hubs (Navigation)
- Infra, CI and Knowledge Docs
- Lead Qualification (LLM)
- RAG Ask Endpoint
- Agent Research Loop
- Chunking and Embedding
- Config and Vector Store
- Mocked Enrichment Tools

## God Nodes (most connected - your core abstractions)
1. `get_client()` - 12 edges
2. `QualifyResponse` - 11 edges
3. `main()` - 10 edges
4. `Project Study Guide` - 10 edges
5. `qualify_lead_with_tools()` - 9 edges
6. `ToolQualifyResponse` - 9 edges
7. `AskResponse` - 9 edges
8. `ResearchLeadResponse` - 9 edges
9. `chunk_text()` - 9 edges
10. `ask()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Raw Agent Loop (no framework)` --references--> `research_lead()`  [EXTRACTED]
  PROJECT_STUDY_GUIDE.md → app/agent/loop.py
- `Lazy OpenAI Client Construction` --rationale_for--> `get_client()`  [EXTRACTED]
  CODE_DOCUMENTATION.md → app/llm.py
- `Structured Outputs` --references--> `qualify_lead()`  [EXTRACTED]
  PROJECT_STUDY_GUIDE.md → app/llm.py
- `Tool Use / Function Calling Loop` --references--> `qualify_lead_with_tools()`  [EXTRACTED]
  PROJECT_STUDY_GUIDE.md → app/llm.py
- `Paragraph-aware Chunking with Overlap` --rationale_for--> `chunk_text()`  [EXTRACTED]
  CODE_DOCUMENTATION.md → app/rag/chunking.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **RAG pipeline: sample docs ingested into pgvector and queried by /ask** — docs_product_overview, docs_refund_policy, scripts_ingest_docs_main, docker_compose_db, app_rag_qa_ask, project_study_guide_rag_from_scratch [INFERRED 0.85]
- **Hand-rolled tool-calling loops with mocked CRM tools** — project_study_guide_tool_calling_loop, app_llm_qualify_lead_with_tools, app_agent_loop_research_lead, app_llm_lookup_company_firmographics, app_agent_loop_search_company_info [EXTRACTED 1.00]
- **Running tests without a real API key** — _github_workflows_ci_test_job, project_study_guide_router_boundary_mocking, code_documentation_lazy_client [INFERRED 0.85]

## Communities (10 total, 3 thin omitted)

### Community 0 - "Infra, CI and Knowledge Docs"
Cohesion: 0.13
Nodes (20): CI Workflow (ci.yml), CI test job (pytest -q, Python 3.12, dummy OPENAI_API_KEY), init_schema(), Code Documentation (EN/ID), EMBEDDING_DIM 1536 coupling to text-embedding-3-small, Ingestion has no duplicate check, app service (FastAPI container), db service (pgvector/pgvector:pg16) (+12 more)

### Community 1 - "Lead Qualification (LLM)"
Cohesion: 0.18
Nodes (12): get_client(), qualify_lead(), qualify_lead_with_tools(), QualifyRequest, QualifyResponse, ToolQualifyResponse, qualify_lead_endpoint(), qualify_lead_with_tools_endpoint() (+4 more)

### Community 2 - "RAG Ask Endpoint"
Cohesion: 0.18
Nodes (8): health(), AskRequest, AskResponse, Citation, ask(), ask_endpoint(), test_ask_endpoint(), fake_ask()

### Community 3 - "Agent Research Loop"
Cohesion: 0.19
Nodes (7): _AgentFinalAnswer, research_lead(), ResearchLeadRequest, ResearchLeadResponse, research_lead_endpoint(), test_research_lead_endpoint(), fake_research_lead()

### Community 4 - "Chunking and Embedding"
Cohesion: 0.16
Nodes (5): Chunk, chunk_text(), embed_texts(), test_chunk_text_keeps_short_input_as_one_chunk(), test_chunk_text_splits_long_input_into_multiple_chunks()

### Community 5 - "Config and Vector Store"
Cohesion: 0.16
Nodes (3): get_connection(), insert_chunks(), search()

### Community 6 - "Mocked Enrichment Tools"
Cohesion: 0.50
Nodes (3): _search_company_info(), _lookup_company_firmographics(), Mocked CRM/Enrichment Tools (Acme Corp, Globex)

## Ambiguous Edges - Review These
- `Product API Rate Limits (100/20 rpm)` → `Known Gaps (no auth/rate-limit, no reranking)`  [AMBIGUOUS]
  docs/product_overview.md · relation: conceptually_related_to

## Knowledge Gaps
- **2 isolated node(s):** `Support Hours and Enterprise SLA`, `30-day full refund, then pro-rated`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 37 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_client()` connect `Lead Qualification (LLM)` to `Infra, CI and Knowledge Docs`, `RAG Ask Endpoint`, `Agent Research Loop`, `Chunking and Embedding`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `QualifyResponse` (e.g. with `qualify_lead()` and `qualify_lead_with_tools()`) actually correct?**
  _`QualifyResponse` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Support Hours and Enterprise SLA`, `30-day full refund, then pro-rated` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Infra, CI and Knowledge Docs` be split into smaller, more focused modules?**
  _Cohesion score 0.12643678160919541 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `Infra, CI and Knowledge Docs` to `Chunking and Embedding`, `Config and Vector Store`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `main()` (e.g. with `Product Overview (sample KB doc)` and `Refund Policy (sample KB doc)`) actually correct?**
  _`main()` has 2 INFERRED edges - model-reasoned connections that need verification._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Product API Rate Limits (100/20 rpm)` and `Known Gaps (no auth/rate-limit, no reranking)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._