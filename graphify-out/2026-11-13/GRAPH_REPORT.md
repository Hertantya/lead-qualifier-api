# Graph Report - lead-qualifier-api  (2026-11-09)

## Corpus Check
- Corpus is ~11,582 words - fits in a single context window. You may not need a graph.

## Summary
- 203 nodes · 340 edges · 16 communities (11 shown, 5 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- API Endpoints and Agent Loop
- Architecture and Design Docs
- Chunking and Vector Storage
- LLM Configuration and RAG QA
- Lead Qualification Endpoints
- Docker Compose App Services
- CI Workflow
- Docker Compose Database
- Product and Refund Policies
- Python Dependencies
- Origin of the Word Robot
- Fun Fact: Honey
- Fun Fact: Lightning
- Fun Fact: Octopuses

## God Nodes (most connected - your core abstractions)
1. `Lead Qualifier API Code Documentation` - 12 edges
2. `get_client()` - 11 edges
3. `QualifyResponse` - 11 edges
4. `ToolQualifyResponse` - 9 edges
5. `AskResponse` - 9 edges
6. `ResearchLeadResponse` - 9 edges
7. `Unpinned Python application and test dependencies` - 9 edges
8. `Project Study Guide` - 9 edges
9. `qualify_lead_with_tools()` - 8 edges
10. `QualifyRequest` - 8 edges

## Surprising Connections (you probably didn't know these)
- `fake_qualify_lead()` --calls--> `QualifyResponse`  [EXTRACTED]
  tests/test_qualify.py → app/models.py
- `fake_qualify_with_tools()` --calls--> `ToolQualifyResponse`  [EXTRACTED]
  tests/test_qualify.py → app/models.py
- `fake_research_lead()` --calls--> `ResearchLeadResponse`  [EXTRACTED]
  tests/test_agent.py → app/models.py
- `test_chunk_text_keeps_short_input_as_one_chunk()` --calls--> `chunk_text()`  [EXTRACTED]
  tests/test_chunking.py → app/rag/chunking.py
- `test_chunk_text_splits_long_input_into_multiple_chunks()` --calls--> `chunk_text()`  [EXTRACTED]
  tests/test_chunking.py → app/rag/chunking.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Refund entitlement combines purchase age, annual-contract remainder, MSA precedence and processing rules** — docs_refund_policy_refund_policy, docs_refund_policy_prorated_refund, docs_refund_policy_master_service_agreement, docs_refund_policy_refund_request [EXTRACTED 1.00]
- **Three Core LLM Patterns Sharing One Shape** — claude_three_llm_patterns, code_documentation_structured_output, code_documentation_tool_calling_loop, code_documentation_rag_pipeline [EXTRACTED 1.00]
- **End-to-End RAG Pipeline Components** — code_documentation_rag_pipeline, code_documentation_paragraph_chunking_overlap, code_documentation_pgvector_cosine_search, code_documentation_citation_tagging, code_documentation_ingest_pipeline [EXTRACTED 1.00]
- **Framework-Free Learning Design Philosophy** — claude_no_agent_frameworks, project_study_guide_fundamentals_first, project_study_guide_mock_swappability, readme_design_notes [INFERRED 0.85]

## Communities (16 total, 5 thin omitted)

### Community 0 - "API Endpoints and Agent Loop"
Cohesion: 0.10
Nodes (15): _AgentFinalAnswer, research_lead(), _search_company_info(), health(), AskRequest, AskResponse, Citation, ResearchLeadRequest (+7 more)

### Community 1 - "Architecture and Design Docs"
Cohesion: 0.13
Nodes (22): CLAUDE.md Repository Guidance, graphify Knowledge Graph Workflow, Lazy OpenAI Client via app.llm.get_client(), Three Shared LLM Patterns (Structured Output, Tool Loop, RAG), Lead Qualifier API Code Documentation, Hand-Rolled Agent Loop (research_lead), Source:Index Citation Tagging, Environment-Only Configuration (app/config.py) (+14 more)

### Community 2 - "Chunking and Vector Storage"
Cohesion: 0.13
Nodes (9): Chunk, chunk_text(), get_connection(), init_schema(), insert_chunks(), search(), main(), test_chunk_text_keeps_short_input_as_one_chunk() (+1 more)

### Community 3 - "LLM Configuration and RAG QA"
Cohesion: 0.19
Nodes (4): get_client(), _lookup_company_firmographics(), embed_texts(), ask()

### Community 4 - "Lead Qualification Endpoints"
Cohesion: 0.23
Nodes (11): qualify_lead(), qualify_lead_with_tools(), QualifyRequest, QualifyResponse, ToolQualifyResponse, qualify_lead_endpoint(), qualify_lead_with_tools_endpoint(), test_qualify_lead() (+3 more)

### Community 5 - "Docker Compose App Services"
Cohesion: 0.12
Nodes (15): build, depends_on, environment, ports, condition, db, DATABASE_URL, OPENAI_API_KEY (+7 more)

### Community 6 - "CI Workflow"
Cohesion: 0.12
Nodes (15): OPENAI_API_KEY, jobs, test, name, on, pull_request, push, env (+7 more)

### Community 7 - "Docker Compose Database"
Cohesion: 0.15
Nodes (13): environment, healthcheck, image, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER (+5 more)

### Community 8 - "Product and Refund Policies"
Cohesion: 0.20
Nodes (9): Enterprise: unlimited seats, custom enrichment, onboarding, SSO, account manager, 100 requests/minute/key, Enterprise support: 24/7 and 1-hour response SLA for critical issues, Growth: 20 seats, 5,000 enriched leads/month, HubSpot and Salesforce integrations, priority support, 100 requests/minute/key, Standard support: Monday-Friday, 9am-6pm Singapore time, Starter: 3 seats, 500 enriched leads/month, email support, 20 API requests/minute/key, Signed Enterprise Master Service Agreement cancellation terms override the default refund policy, After 30 days: pro-rated refund for remaining months of an annual contract, Refund policy: full refund within 30 days of purchase, no questions asked (+1 more)

### Community 9 - "Python Dependencies"
Cohesion: 0.20
Nodes (10): Unpinned Python application and test dependencies, fastapi, httpx, openai, pgvector, psycopg[binary], pydantic, pytest (+2 more)

### Community 10 - "Origin of the Word Robot"
Cohesion: 1.00
Nodes (3): Karel Čapek: credited in the source with coining robot in R.U.R., R.U.R.: 1920 play, Robot: word derived from Czech robota, meaning forced labor

## Knowledge Gaps
- **20 isolated node(s):** `Lightning: about 30,000 K, approximately five times hotter than the Sun's surface`, `Honey: source claims sealed Egyptian tomb pots remain edible after 3,000+ years`, `Octopuses: three hearts, two stop beating while swimming according to the source`, `Starter: 3 seats, 500 enriched leads/month, email support, 20 API requests/minute/key`, `Growth: 20 seats, 5,000 enriched leads/month, HubSpot and Salesforce integrations, priority support, 100 requests/minute/key` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 82 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_client()` connect `LLM Configuration and RAG QA` to `API Endpoints and Agent Loop`, `Lead Qualification Endpoints`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `QualifyResponse` (e.g. with `qualify_lead()` and `qualify_lead_with_tools()`) actually correct?**
  _`QualifyResponse` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Lightning: about 30,000 K, approximately five times hotter than the Sun's surface`, `Honey: source claims sealed Egyptian tomb pots remain edible after 3,000+ years`, `Octopuses: three hearts, two stop beating while swimming according to the source` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API Endpoints and Agent Loop` be split into smaller, more focused modules?**
  _Cohesion score 0.09716599190283401 - nodes in this community are weakly interconnected._
- **Why does `ask()` connect `LLM Configuration and RAG QA` to `API Endpoints and Agent Loop`, `Chunking and Vector Storage`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Should `Architecture and Design Docs` be split into smaller, more focused modules?**
  _Cohesion score 0.1310344827586207 - nodes in this community are weakly interconnected._
- **Should `Chunking and Vector Storage` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._