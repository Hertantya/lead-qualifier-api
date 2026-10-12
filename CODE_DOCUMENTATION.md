# Lead Qualifier API — Code Documentation / Dokumentasi Kode

> **How to read this document / Cara membaca dokumen ini**
> Every explanation below is written twice: first in **English (EN)**, then immediately in **Bahasa Indonesia (ID)**. Read the EN block if you're comfortable in English, or skip straight to the ID block below it — they say the same thing.
>
> Setiap penjelasan di bawah ini ditulis dua kali: pertama dalam **Bahasa Inggris (EN)**, langsung diikuti oleh **Bahasa Indonesia (ID)**. Baca bagian EN jika kamu nyaman berbahasa Inggris, atau langsung lompat ke bagian ID di bawahnya — keduanya menjelaskan hal yang sama.

---

## Table of Contents / Daftar Isi

1. [High-Level Overview](#1-high-level-overview--gambaran-umum)
2. [Project Structure](#2-project-structure--struktur-proyek)
3. [File-by-File Breakdown](#3-file-by-file-breakdown--rincian-per-file)
   - [3.1 app/config.py](#31-appconfigpy)
   - [3.2 app/models.py](#32-appmodelspy)
   - [3.3 app/llm.py](#33-appllmpy)
   - [3.4 app/main.py](#34-appmainpy)
   - [3.5 app/routers/qualify.py](#35-approutersqualifypy)
   - [3.6 app/routers/ask.py](#36-approutersaskpy)
   - [3.7 app/routers/agent.py](#37-approutersagentpy)
   - [3.8 app/rag/chunking.py](#38-approgchunkingpy)
   - [3.9 app/rag/embeddings.py](#39-approgembeddingspy)
   - [3.10 app/rag/store.py](#310-approgstorepy)
   - [3.11 app/rag/qa.py](#311-approgqapy)
   - [3.12 app/agent/loop.py](#312-appagentlooppy)
   - [3.13 scripts/ingest_docs.py](#313-scriptsingest_docspy)
4. [End-to-End Flow](#4-end-to-end-flow--alur-menyeluruh)

---

## 1. High-Level Overview / Gambaran Umum

**EN:**
This project is a small web API (built with **FastAPI**, a popular Python framework for building APIs) that uses an AI language model (like GPT via OpenAI, or another provider like OpenRouter) to help qualify sales leads. "Qualifying a lead" means looking at a potential customer and deciding: is this company worth pursuing, and why?

The project intentionally avoids AI frameworks like LangChain, LangGraph, or CrewAI. Instead, every AI pattern is hand-written in plain Python so a beginner can read the code top-to-bottom and understand exactly what's happening — no hidden "magic."

There are four main features (API endpoints):

1. **`/qualify-lead`** — You send a text description of a company. The AI reads it and returns a structured score (1–10), reasoning, and a recommended next action. This demonstrates **structured output**: forcing the AI's answer into a strict, predictable JSON shape instead of free-form text.
2. **`/qualify-lead/with-tools`** — Same idea, but before scoring, the AI can call a **"tool"** (a Python function) to look up extra facts about the company (like employee count or funding stage) from a small fake database. This demonstrates **tool use / function calling**: letting the AI decide when it needs more information and fetch it itself.
3. **`/ask`** — You ask a question, and the AI answers it using only the content of markdown files stored in the `docs/` folder, citing which document it used. This demonstrates **RAG (Retrieval-Augmented Generation)**: instead of the AI making things up from its training data, it looks up relevant text first, then answers based on that text.
4. **`/research-lead`** — Given a company name, the AI "researches" it (again using a tool/fake database), writes a two-sentence summary, and drafts a personalized outreach email. This demonstrates a full **agent loop**: the AI can call a tool multiple times in a back-and-forth conversation before giving its final answer.

Under the hood, three technologies work together: **FastAPI** (handles web requests), **OpenAI's Python SDK** (talks to the AI model), and **PostgreSQL with the pgvector extension** (a database that can store and search "embeddings" — numerical representations of text — needed only for the RAG feature).

**ID:**
Proyek ini adalah sebuah web API kecil (dibangun dengan **FastAPI**, sebuah framework Python populer untuk membuat API) yang menggunakan model bahasa AI (seperti GPT via OpenAI, atau provider lain seperti OpenRouter) untuk membantu menilai kelayakan calon pelanggan (lead) penjualan. "Mengkualifikasi lead" artinya melihat calon pelanggan dan memutuskan: apakah perusahaan ini layak untuk dikejar, dan kenapa?

Proyek ini sengaja tidak menggunakan framework AI seperti LangChain, LangGraph, atau CrewAI. Sebagai gantinya, setiap pola AI ditulis manual dalam Python biasa agar pemula bisa membaca kode dari atas ke bawah dan memahami persis apa yang terjadi — tidak ada "sihir" yang tersembunyi.

Ada empat fitur utama (endpoint API):

1. **`/qualify-lead`** — Kamu mengirim deskripsi teks sebuah perusahaan. AI membacanya dan mengembalikan skor terstruktur (1–10), alasan, serta rekomendasi tindakan selanjutnya. Ini mendemonstrasikan **structured output** (keluaran terstruktur): memaksa jawaban AI ke dalam bentuk JSON yang ketat dan dapat diprediksi, bukan teks bebas.
2. **`/qualify-lead/with-tools`** — Konsepnya sama, tapi sebelum memberi skor, AI bisa memanggil sebuah **"tool"** (fungsi Python) untuk mencari fakta tambahan tentang perusahaan tersebut (seperti jumlah karyawan atau tahap pendanaan) dari database palsu kecil. Ini mendemonstrasikan **tool use / function calling**: membiarkan AI memutuskan kapan ia butuh informasi tambahan dan mengambilnya sendiri.
3. **`/ask`** — Kamu mengajukan pertanyaan, dan AI menjawabnya hanya berdasarkan isi file markdown yang tersimpan di folder `docs/`, sambil menyebutkan dokumen mana yang digunakan. Ini mendemonstrasikan **RAG (Retrieval-Augmented Generation)**: alih-alih AI mengarang jawaban dari data latihannya, ia mencari teks yang relevan terlebih dahulu, baru menjawab berdasarkan teks tersebut.
4. **`/research-lead`** — Dengan memberikan nama perusahaan, AI akan "meneliti" perusahaan tersebut (lagi-lagi menggunakan tool/database palsu), menulis ringkasan dua kalimat, dan membuat draf email outreach yang dipersonalisasi. Ini mendemonstrasikan **agent loop** (loop agen) yang utuh: AI bisa memanggil tool berkali-kali dalam percakapan bolak-balik sebelum memberikan jawaban akhirnya.

Di balik layar, tiga teknologi bekerja sama: **FastAPI** (menangani permintaan web), **OpenAI Python SDK** (berkomunikasi dengan model AI), dan **PostgreSQL dengan ekstensi pgvector** (database yang bisa menyimpan dan mencari "embeddings" — representasi numerik dari teks — yang hanya dibutuhkan untuk fitur RAG).

---

## 2. Project Structure / Struktur Proyek

**EN:** Here's how the code is organized on disk:
**ID:** Berikut adalah bagaimana kode diorganisasi di dalam folder:

```
app/
├── config.py         # Reads settings/secrets from environment variables
├── models.py         # Defines the shape of every request & response (Pydantic schemas)
├── llm.py            # Talks to the AI model: structured output + tool use for lead qualification
├── main.py           # The FastAPI application itself; wires all endpoints together
├── rag/
│   ├── chunking.py    # Splits documents into small text pieces ("chunks")
│   ├── embeddings.py  # Converts text into numerical vectors ("embeddings")
│   ├── store.py        # Saves/searches those vectors in PostgreSQL (pgvector)
│   └── qa.py            # Ties retrieval + AI together to answer questions with citations
├── agent/
│   └── loop.py          # The hand-rolled "agent": AI + tool-calling loop for /research-lead
└── routers/            # One file per group of endpoints (thin, just routing)
    ├── qualify.py
    ├── ask.py
    └── agent.py
scripts/
└── ingest_docs.py     # A one-off script: reads docs/*.md, embeds them, stores them in the DB
```

---

## 3. File-by-File Breakdown / Rincian Per File

### 3.1 `app/config.py`

**EN Overview:** This file's only job is to read configuration values (API keys, model names, database connection string) from environment variables, so no secrets are ever hardcoded in the source code. It uses `python-dotenv`'s `load_dotenv()` to also read from a local `.env` file during development.

**ID Ringkasan:** Satu-satunya tugas file ini adalah membaca nilai konfigurasi (API key, nama model, connection string database) dari environment variables, sehingga tidak ada rahasia (secret) yang ditulis langsung di dalam kode sumber. File ini menggunakan `load_dotenv()` dari `python-dotenv` untuk membaca juga dari file `.env` lokal saat development.

| Variable | EN — What it's for | ID — Untuk apa |
|---|---|---|
| `OPENAI_API_KEY` | The secret key used to authenticate with the AI provider (OpenAI or a compatible one like OpenRouter). | Kunci rahasia yang digunakan untuk autentikasi ke provider AI (OpenAI atau yang kompatibel seperti OpenRouter). |
| `OPENAI_BASE_URL` | Optional override so the app can talk to a different OpenAI-compatible API (e.g. OpenRouter) instead of OpenAI directly. If left empty, defaults to OpenAI's own servers. | Override opsional agar aplikasi bisa berbicara ke API lain yang kompatibel dengan OpenAI (misalnya OpenRouter), bukan langsung ke OpenAI. Jika dikosongkan, akan memakai server OpenAI secara default. |
| `OPENAI_MODEL` | Which chat/completion model to use (e.g. `gpt-4o-mini`, or an OpenRouter model slug). | Model chat/completion mana yang dipakai (misalnya `gpt-4o-mini`, atau slug model OpenRouter). |
| `OPENAI_EMBEDDING_MODEL` | Which model to use to turn text into embeddings (vectors), used only by the RAG feature. | Model mana yang dipakai untuk mengubah teks menjadi embeddings (vektor), hanya dipakai oleh fitur RAG. |
| `DATABASE_URL` | The connection string pointing at the Postgres database (used only by the RAG feature). | Connection string yang menunjuk ke database Postgres (hanya dipakai oleh fitur RAG). |

**EN — why it matters to the AI process:** Every other file in this project imports from `config` instead of reading `os.environ` directly. This means if you ever need to switch AI providers or databases, you only change `.env` — no code changes needed.

**ID — kenapa ini penting untuk proses AI:** Semua file lain di proyek ini mengimpor dari `config`, bukan membaca `os.environ` secara langsung. Artinya jika suatu saat kamu perlu mengganti provider AI atau database, kamu hanya perlu mengubah `.env` — tidak perlu mengubah kode.

---

### 3.2 `app/models.py`

**EN Overview:** This file defines the exact "shape" of data flowing in and out of every endpoint, using **Pydantic** (a library that validates data automatically). Think of these as contracts: if a request doesn't match the shape, FastAPI rejects it automatically before your code even runs.

**ID Ringkasan:** File ini mendefinisikan "bentuk" data yang persis untuk setiap data yang masuk dan keluar dari setiap endpoint, menggunakan **Pydantic** (library yang memvalidasi data secara otomatis). Anggap ini sebagai kontrak: jika sebuah request tidak sesuai bentuknya, FastAPI akan menolaknya secara otomatis sebelum kode kamu sempat dijalankan.

| Class | EN — Purpose | ID — Tujuan |
|---|---|---|
| `QualifyRequest` | Input for `/qualify-lead`: just a free-text `company_description` string (must not be empty). | Input untuk `/qualify-lead`: hanya berupa string teks bebas `company_description` (tidak boleh kosong). |
| `QualifyResponse` | Output of `/qualify-lead`: a `score` (must be between 1 and 10), a `reasoning` string, and a `recommended_action` string. | Output dari `/qualify-lead`: sebuah `score` (harus di antara 1 dan 10), string `reasoning`, dan string `recommended_action`. |
| `ToolQualifyResponse` | Same as `QualifyResponse`, but adds a `tools_used` list — the names of any tools the AI called before answering. Used by `/qualify-lead/with-tools`. | Sama seperti `QualifyResponse`, tapi menambahkan daftar `tools_used` — nama-nama tool yang dipanggil AI sebelum menjawab. Dipakai oleh `/qualify-lead/with-tools`. |
| `AskRequest` | Input for `/ask`: a `question` string, plus `top_k` (how many document chunks to retrieve, default 4, between 1 and 10). | Input untuk `/ask`: string `question`, ditambah `top_k` (berapa banyak potongan dokumen yang diambil, default 4, antara 1 dan 10). |
| `Citation` | A single source reference: which document (`source`), which chunk number (`chunk_index`), and the actual `text` of that chunk. | Satu referensi sumber: dokumen mana (`source`), nomor potongan (`chunk_index`), dan `text` asli dari potongan tersebut. |
| `AskResponse` | Output of `/ask`: the AI's `answer` plus a list of `citations` backing it up. | Output dari `/ask`: `answer` dari AI beserta daftar `citations` yang mendukungnya. |
| `ResearchLeadRequest` | Input for `/research-lead`: just a `company_name` string. | Input untuk `/research-lead`: hanya string `company_name`. |
| `ResearchLeadResponse` | Output of `/research-lead`: `company_name`, a `summary`, a `draft_email`, and the list of `tool_calls` made along the way. | Output dari `/research-lead`: `company_name`, sebuah `summary`, `draft_email`, dan daftar `tool_calls` yang dilakukan selama proses. |

**EN — why it matters to the AI process:** `QualifyResponse` and `ResearchLeadResponse`-like schemas are passed directly to the OpenAI SDK as the `response_format` — this is what forces the AI to reply in valid, guaranteed JSON matching these exact fields (the "structured output" feature).

**ID — kenapa ini penting untuk proses AI:** Skema seperti `QualifyResponse` diteruskan langsung ke OpenAI SDK sebagai `response_format` — inilah yang memaksa AI untuk menjawab dalam format JSON yang valid dan sesuai persis dengan field-field ini (fitur "structured output").

---

### 3.3 `app/llm.py`

**EN Overview:** This is the core wrapper around the OpenAI SDK, handling both the plain "structured output" flow and the "tool use" flow for lead qualification.

**ID Ringkasan:** Ini adalah wrapper inti di sekitar OpenAI SDK, menangani baik alur "structured output" biasa maupun alur "tool use" untuk kualifikasi lead.

#### `get_client() -> OpenAI`
**EN:** Lazily creates (only once, then reuses) an `OpenAI` client object configured with the API key and base URL from `config`. "Lazily" means the client isn't built until the first time it's actually needed — so simply importing this file never requires a valid API key to be present (useful for running tests without real credentials).
**ID:** Membuat (hanya sekali, lalu dipakai ulang) objek client `OpenAI` yang dikonfigurasi dengan API key dan base URL dari `config`. "Lazily" (malas/ditunda) artinya client baru dibuat saat benar-benar dibutuhkan pertama kali — sehingga sekadar meng-import file ini tidak pernah membutuhkan API key yang valid (berguna untuk menjalankan test tanpa kredensial asli).

#### `QUALIFY_SYSTEM_PROMPT` (constant)
**EN:** The instruction text sent to the AI as the "system" role, telling it exactly how to behave: score leads 1–10 for a B2B SaaS company, explain reasoning, and recommend a next action.
**ID:** Teks instruksi yang dikirim ke AI sebagai peran "system", memberitahu AI persis bagaimana harus bersikap: memberi skor lead 1–10 untuk perusahaan B2B SaaS, menjelaskan alasan, dan merekomendasikan tindakan selanjutnya.

#### `qualify_lead(req: QualifyRequest) -> QualifyResponse`
**EN:** Powers the `/qualify-lead` endpoint. It calls `client.beta.chat.completions.parse(...)`, passing the system prompt, the user's description, and `response_format=QualifyResponse`. This special `.parse()` method (compared to the regular `.create()`) tells the OpenAI SDK to validate the model's JSON reply against the `QualifyResponse` schema automatically — if the model's answer doesn't fit, `result` comes back as `None` and the function raises an error instead of returning bad data.
**ID:** Menggerakkan endpoint `/qualify-lead`. Fungsi ini memanggil `client.beta.chat.completions.parse(...)`, dengan mengirim system prompt, deskripsi dari user, dan `response_format=QualifyResponse`. Method khusus `.parse()` ini (dibandingkan `.create()` biasa) memberitahu OpenAI SDK untuk secara otomatis memvalidasi balasan JSON dari model terhadap skema `QualifyResponse` — jika jawaban model tidak sesuai, `result` akan bernilai `None` dan fungsi ini akan memunculkan error, bukannya mengembalikan data yang salah.

#### `_lookup_company_firmographics(company_name: str) -> dict`
**EN:** A **mocked** (fake, hardcoded) stand-in for what would normally be a real API call to a data provider like Apollo, Clay, or HubSpot. It has two made-up companies ("Acme Corp" and "Globex") in a small dictionary; any other name returns "Unknown" values. This is the actual Python function that gets executed when the AI decides to use the tool.
**ID:** Sebuah pengganti **mock** (palsu, hardcoded) untuk apa yang biasanya berupa panggilan API sungguhan ke penyedia data seperti Apollo, Clay, atau HubSpot. Fungsi ini memiliki dua perusahaan buatan ("Acme Corp" dan "Globex") di dalam dictionary kecil; nama lain akan mengembalikan nilai "Unknown". Inilah fungsi Python sesungguhnya yang dijalankan ketika AI memutuskan untuk menggunakan tool tersebut.

#### `TOOLS` (constant list)
**EN:** A JSON-like description (following OpenAI's tool-calling schema) of the `lookup_company_firmographics` tool: its name, a description (which the AI reads to decide *when* to use it), and the parameters it accepts. This description is sent to the AI model — the AI itself never runs code; it only ever says "please call this tool with these arguments," and our code (below) does the actual calling.
**ID:** Sebuah deskripsi mirip-JSON (mengikuti skema tool-calling milik OpenAI) untuk tool `lookup_company_firmographics`: namanya, deskripsi (yang dibaca AI untuk memutuskan *kapan* harus memakainya), dan parameter yang diterimanya. Deskripsi ini dikirim ke model AI — AI sendiri tidak pernah menjalankan kode; ia hanya berkata "tolong panggil tool ini dengan argumen berikut," dan kode kita (di bawah) yang benar-benar melakukan pemanggilannya.

#### `_AVAILABLE_TOOLS` (constant dict)
**EN:** A lookup table mapping the tool's string name (`"lookup_company_firmographics"`) to the actual Python function to run. This is how the code translates the AI's request ("call tool X") into "run this specific function."
**ID:** Sebuah tabel pencarian yang memetakan nama tool dalam bentuk string (`"lookup_company_firmographics"`) ke fungsi Python sesungguhnya yang harus dijalankan. Inilah cara kode menerjemahkan permintaan AI ("panggil tool X") menjadi "jalankan fungsi spesifik ini."

#### `qualify_lead_with_tools(req: QualifyRequest, max_turns: int = 3) -> ToolQualifyResponse`
**EN:** Powers `/qualify-lead/with-tools`. This is the classic **tool-calling loop**:
1. Send the conversation so far to the AI, along with the list of `TOOLS` it's allowed to use.
2. If the AI's reply contains `tool_calls`, it means the AI wants to use a tool. The code looks up the requested function in `_AVAILABLE_TOOLS`, runs it with the AI-provided arguments, and appends the result back into the conversation as a special `role: "tool"` message.
3. This repeats (up to `max_turns` times) until the AI stops asking for tools.
4. Finally, a structured-output call (like in `qualify_lead`) asks the AI for its final, validated `QualifyResponse` — and the list of tool names used along the way (`tools_used`) is attached to build the final `ToolQualifyResponse`.

**ID:** Menggerakkan `/qualify-lead/with-tools`. Ini adalah **loop tool-calling** klasik:
1. Kirim percakapan sejauh ini ke AI, beserta daftar `TOOLS` yang boleh dipakai.
2. Jika balasan AI berisi `tool_calls`, artinya AI ingin memakai sebuah tool. Kode akan mencari fungsi yang diminta di dalam `_AVAILABLE_TOOLS`, menjalankannya dengan argumen yang diberikan AI, lalu menambahkan hasilnya kembali ke dalam percakapan sebagai pesan khusus `role: "tool"`.
3. Proses ini berulang (hingga `max_turns` kali) sampai AI berhenti meminta tool.
4. Terakhir, sebuah panggilan structured-output (seperti pada `qualify_lead`) meminta AI memberikan `QualifyResponse` final yang tervalidasi — dan daftar nama tool yang dipakai selama proses (`tools_used`) ditempelkan untuk membentuk `ToolQualifyResponse` akhir.

---

### 3.4 `app/main.py`

**EN Overview:** This is the entry point of the whole application — the file you point `uvicorn` at to actually start the web server.

**ID Ringkasan:** Ini adalah titik masuk (entry point) dari keseluruhan aplikasi — file yang ditunjuk oleh `uvicorn` untuk benar-benar menjalankan web server.

#### `app = FastAPI(...)`
**EN:** Creates the main FastAPI application object, with a title, description, and version shown on the auto-generated `/docs` page.
**ID:** Membuat objek aplikasi FastAPI utama, dengan judul, deskripsi, dan versi yang ditampilkan di halaman `/docs` yang dibuat otomatis.

#### `app.include_router(...)` (three calls)
**EN:** Registers the three router files (`qualify`, `ask`, `agent`) so their endpoints become part of the live application. Without this line, the endpoints defined in those files wouldn't actually be reachable.
**ID:** Mendaftarkan tiga file router (`qualify`, `ask`, `agent`) sehingga endpoint di dalamnya menjadi bagian dari aplikasi yang berjalan. Tanpa baris ini, endpoint yang didefinisikan di file-file tersebut tidak akan bisa diakses.

#### `health() -> dict[str, str]`
**EN:** The `/health` endpoint. Returns a simple `{"status": "ok"}` with no AI or database involved — used to quickly check "is the server even running?"
**ID:** Endpoint `/health`. Mengembalikan `{"status": "ok"}` sederhana tanpa melibatkan AI atau database — dipakai untuk memeriksa dengan cepat "apakah servernya benar-benar berjalan?"

---

### 3.5 `app/routers/qualify.py`

**EN Overview:** A thin "router" file — its only job is to receive the HTTP request, hand it off to the real logic in `llm.py`, and return the result. Routers in this project intentionally contain almost no logic themselves.

**ID Ringkasan:** File "router" yang tipis — satu-satunya tugasnya adalah menerima HTTP request, menyerahkannya ke logika sesungguhnya di `llm.py`, lalu mengembalikan hasilnya. Router dalam proyek ini sengaja dibuat hampir tanpa logika sendiri.

#### `qualify_lead_endpoint(req: QualifyRequest) -> QualifyResponse`
**EN:** Handles `POST /qualify-lead`. Simply calls `qualify_lead(req)` from `llm.py` and returns whatever it returns.
**ID:** Menangani `POST /qualify-lead`. Cukup memanggil `qualify_lead(req)` dari `llm.py` dan mengembalikan hasilnya.

#### `qualify_lead_with_tools_endpoint(req: QualifyRequest) -> ToolQualifyResponse`
**EN:** Handles `POST /qualify-lead/with-tools`. Calls `qualify_lead_with_tools(req)` from `llm.py`.
**ID:** Menangani `POST /qualify-lead/with-tools`. Memanggil `qualify_lead_with_tools(req)` dari `llm.py`.

---

### 3.6 `app/routers/ask.py`

**EN Overview:** The router for the RAG question-answering feature.

**ID Ringkasan:** Router untuk fitur tanya-jawab (RAG).

#### `ask_endpoint(req: AskRequest) -> AskResponse`
**EN:** Handles `POST /ask`. Passes the user's `question` and desired `top_k` (how many chunks to retrieve) straight into the `ask()` function from `app/rag/qa.py`, which does all the real work.
**ID:** Menangani `POST /ask`. Meneruskan `question` dari user dan `top_k` (berapa banyak potongan yang diambil) langsung ke fungsi `ask()` di `app/rag/qa.py`, yang melakukan semua pekerjaan sesungguhnya.

---

### 3.7 `app/routers/agent.py`

**EN Overview:** The router for the sales-research agent feature.

**ID Ringkasan:** Router untuk fitur agen riset penjualan.

#### `research_lead_endpoint(req: ResearchLeadRequest) -> ResearchLeadResponse`
**EN:** Handles `POST /research-lead`. Passes `req.company_name` into `research_lead()` from `app/agent/loop.py`.
**ID:** Menangani `POST /research-lead`. Meneruskan `req.company_name` ke `research_lead()` dari `app/agent/loop.py`.

---

### 3.8 `app/rag/chunking.py`

**EN Overview:** Before text can be searched by AI, it needs to be split into smaller pieces ("chunks") — this file does that splitting.

**ID Ringkasan:** Sebelum teks bisa dicari oleh AI, teks tersebut perlu dipecah menjadi bagian-bagian kecil ("chunk") — file ini yang melakukan pemecahan tersebut.

#### `Chunk` (dataclass)
**EN:** A simple data container representing one chunk of text: which file it came from (`source`), its position/order within that file (`index`), and the actual `text` content.
**ID:** Sebuah wadah data sederhana yang merepresentasikan satu potongan teks: dari file mana asalnya (`source`), posisi/urutannya dalam file tersebut (`index`), dan isi `text` sesungguhnya.

#### `chunk_text(text: str, source: str, chunk_size: int = 800, overlap: int = 100) -> list[Chunk]`
**EN:** Splits a document into a list of `Chunk` objects. It works paragraph by paragraph (splitting on blank lines `\n\n`), packing paragraphs together until adding another one would exceed `chunk_size` characters, then starting a new chunk. To avoid losing context right at a chunk boundary, each new chunk starts with the last `overlap` characters of the previous chunk carried over. This "paragraph-aware chunking with overlap" is a common, simple strategy for RAG — you want chunks small enough to be relevant to a specific question, but with enough overlap that an answer isn't accidentally split across two chunks.
**ID:** Memecah sebuah dokumen menjadi daftar objek `Chunk`. Fungsi ini bekerja paragraf demi paragraf (memecah berdasarkan baris kosong `\n\n`), menggabungkan paragraf-paragraf sampai menambahkan satu paragraf lagi akan melebihi `chunk_size` karakter, lalu memulai chunk baru. Untuk menghindari hilangnya konteks tepat di batas antar-chunk, setiap chunk baru dimulai dengan membawa `overlap` karakter terakhir dari chunk sebelumnya. Strategi "chunking berdasarkan paragraf dengan overlap" ini adalah strategi sederhana dan umum untuk RAG — kamu ingin chunk cukup kecil agar relevan dengan pertanyaan spesifik, tapi dengan overlap yang cukup agar sebuah jawaban tidak terpotong tanpa sengaja di antara dua chunk.

---

### 3.9 `app/rag/embeddings.py`

**EN Overview:** Converts text into "embeddings" — lists of numbers that represent the *meaning* of the text, so similar meanings end up as similar numbers (mathematically "close" to each other).

**ID Ringkasan:** Mengubah teks menjadi "embeddings" — daftar angka yang merepresentasikan *makna* dari teks tersebut, sehingga makna yang mirip akan menghasilkan angka yang mirip pula (secara matematis "dekat" satu sama lain).

#### `embed_texts(texts: list[str]) -> list[list[float]]`
**EN:** Takes a list of text strings and sends them to the AI provider's embeddings endpoint (`client.embeddings.create`, using `config.OPENAI_EMBEDDING_MODEL`). Returns one embedding vector (a list of floating-point numbers) per input string, in the same order. This is used twice in this project: once for every chunk of every document during ingestion, and once for the user's question every time `/ask` is called — so the question and the documents end up represented in the same "number space" and can be compared.
**ID:** Menerima daftar string teks dan mengirimkannya ke endpoint embeddings milik provider AI (`client.embeddings.create`, menggunakan `config.OPENAI_EMBEDDING_MODEL`). Mengembalikan satu vektor embedding (daftar angka desimal) untuk setiap string input, dengan urutan yang sama. Fungsi ini dipakai dua kali dalam proyek ini: sekali untuk setiap potongan dari setiap dokumen saat proses ingestion, dan sekali untuk pertanyaan user setiap kali `/ask` dipanggil — sehingga pertanyaan dan dokumen akhirnya direpresentasikan dalam "ruang angka" yang sama dan bisa dibandingkan.

---

### 3.10 `app/rag/store.py`

**EN Overview:** Handles all direct communication with PostgreSQL/pgvector: creating the table, inserting chunks with their embeddings, and searching for the most similar chunks to a given embedding.

**ID Ringkasan:** Menangani semua komunikasi langsung dengan PostgreSQL/pgvector: membuat tabel, menyimpan chunk beserta embeddings-nya, dan mencari chunk-chunk yang paling mirip dengan sebuah embedding tertentu.

#### `EMBEDDING_DIM = 1536` (constant)
**EN:** The fixed size (number of dimensions) of each embedding vector, matching the `text-embedding-3-small` model. This must stay consistent with whatever embedding model is actually configured, since the database column is created with this exact size.
**ID:** Ukuran tetap (jumlah dimensi) dari setiap vektor embedding, sesuai dengan model `text-embedding-3-small`. Nilai ini harus konsisten dengan model embedding yang sebenarnya dikonfigurasi, karena kolom database dibuat dengan ukuran persis ini.

#### `get_connection() -> psycopg.Connection`
**EN:** Opens a new connection to Postgres using `config.DATABASE_URL`. It also runs `CREATE EXTENSION IF NOT EXISTS vector` (safe to run repeatedly — it only does something the first time) to make sure the pgvector extension is enabled, then calls `register_vector(conn)` so this specific connection knows how to translate Python lists of numbers into Postgres's special `vector` type and back.
**ID:** Membuka koneksi baru ke Postgres menggunakan `config.DATABASE_URL`. Fungsi ini juga menjalankan `CREATE EXTENSION IF NOT EXISTS vector` (aman dijalankan berulang kali — hanya benar-benar melakukan sesuatu di kali pertama) untuk memastikan ekstensi pgvector aktif, lalu memanggil `register_vector(conn)` agar koneksi ini tahu cara menerjemahkan daftar angka Python menjadi tipe khusus `vector` milik Postgres, dan sebaliknya.

#### `init_schema(conn: psycopg.Connection) -> None`
**EN:** Creates the `doc_chunks` table if it doesn't already exist, with columns for an auto-incrementing `id`, the `source` filename, the `chunk_index`, the raw `text`, and the `embedding` (stored as a `VECTOR(1536)` column, using pgvector's special type).
**ID:** Membuat tabel `doc_chunks` jika belum ada, dengan kolom `id` yang bertambah otomatis, nama file `source`, `chunk_index`, teks mentah `text`, dan `embedding` (disimpan sebagai kolom `VECTOR(1536)`, menggunakan tipe khusus pgvector).

#### `insert_chunks(conn, chunks: list[Chunk], embeddings: list[list[float]]) -> None`
**EN:** Loops through each chunk and its matching embedding, inserting one row per chunk into `doc_chunks`. Called once by the ingestion script for every document chunk found in `docs/`.
**ID:** Melakukan loop pada setiap chunk beserta embedding-nya yang cocok, menyisipkan satu baris per chunk ke dalam `doc_chunks`. Dipanggil sekali oleh script ingestion untuk setiap potongan dokumen yang ditemukan di `docs/`.

#### `search(conn, query_embedding: list[float], top_k: int = 4) -> list[dict]`
**EN:** The heart of retrieval. Runs a SQL query that orders all rows in `doc_chunks` by how *close* their `embedding` is to the `query_embedding`, using pgvector's `<=>` cosine-distance operator (smaller distance = more similar meaning), and returns only the top `top_k` closest rows. This is the step that finds "which pieces of my documents are most relevant to this question?"
**ID:** Inti dari proses retrieval (pengambilan data). Menjalankan query SQL yang mengurutkan semua baris di `doc_chunks` berdasarkan seberapa *dekat* `embedding`-nya dengan `query_embedding`, menggunakan operator cosine-distance `<=>` milik pgvector (jarak lebih kecil = makna lebih mirip), dan hanya mengembalikan `top_k` baris terdekat. Inilah langkah yang menemukan "bagian mana dari dokumen saya yang paling relevan dengan pertanyaan ini?"

---

### 3.11 `app/rag/qa.py`

**EN Overview:** This file ties everything in the `rag/` folder together to actually answer a question — it's the "brain" behind `/ask`.

**ID Ringkasan:** File ini menyatukan semua hal di folder `rag/` untuk benar-benar menjawab sebuah pertanyaan — ini adalah "otak" di balik `/ask`.

#### `ASK_SYSTEM_PROMPT` (constant)
**EN:** The instruction given to the AI: answer using *only* the provided context, say "I don't know" if the answer isn't there, and cite sources using a `[source:index]` tag. This instruction is what prevents the AI from making up answers not grounded in your documents (reducing "hallucination").
**ID:** Instruksi yang diberikan ke AI: jawab hanya menggunakan konteks yang diberikan, katakan "tidak tahu" jika jawabannya tidak ada di situ, dan sebutkan sumber menggunakan tag `[source:index]`. Instruksi inilah yang mencegah AI mengarang jawaban yang tidak berdasar pada dokumen kamu (mengurangi "halusinasi").

#### `ask(question: str, top_k: int = 4) -> AskResponse`
**EN:** The full RAG pipeline, step by step:
1. Open a database connection.
2. Turn the user's `question` into an embedding using `embed_texts()`.
3. Call `store.search()` to find the `top_k` most relevant chunks from the database.
4. Close the connection (it's only needed for the search step).
5. Join the retrieved chunks into one `context` string, each tagged with `[source:index]`.
6. Send `ASK_SYSTEM_PROMPT` + the context + the original question to the AI via a normal `client.chat.completions.create(...)` call (no structured output needed here, just plain text).
7. Package the AI's text answer together with `Citation` objects (one per retrieved chunk) into an `AskResponse`.

This is the textbook definition of RAG: **R**etrieve relevant text, **A**ugment the prompt with it, **G**enerate an answer from it.

**ID:** Alur RAG lengkap, langkah demi langkah:
1. Membuka koneksi database.
2. Mengubah `question` dari user menjadi embedding menggunakan `embed_texts()`.
3. Memanggil `store.search()` untuk menemukan `top_k` chunk paling relevan dari database.
4. Menutup koneksi (hanya dibutuhkan untuk langkah pencarian).
5. Menggabungkan chunk-chunk yang ditemukan menjadi satu string `context`, masing-masing diberi tag `[source:index]`.
6. Mengirim `ASK_SYSTEM_PROMPT` + context + pertanyaan asli ke AI melalui panggilan `client.chat.completions.create(...)` biasa (tidak perlu structured output di sini, cukup teks biasa).
7. Mengemas jawaban teks dari AI bersama objek `Citation` (satu per chunk yang ditemukan) menjadi sebuah `AskResponse`.

Inilah definisi tekstual dari RAG: **R**etrieve (ambil) teks yang relevan, **A**ugment (perkaya) prompt dengannya, **G**enerate (hasilkan) jawaban darinya.

---

### 3.12 `app/agent/loop.py`

**EN Overview:** The most advanced file in the project — a hand-written "agent": a loop where the AI can repeatedly decide to use tools before producing a final answer, powering `/research-lead`.

**ID Ringkasan:** File paling kompleks di proyek ini — sebuah "agent" yang ditulis manual: sebuah loop di mana AI bisa berulang kali memutuskan untuk memakai tool sebelum menghasilkan jawaban akhir, menggerakkan `/research-lead`.

#### `AGENT_SYSTEM_PROMPT` (constant)
**EN:** Tells the AI its role: a sales-research agent that should use the `search_company_info` tool to gather facts, then write a two-sentence summary and an outreach email — and only call the tool once per company.
**ID:** Memberitahu AI perannya: agen riset penjualan yang harus memakai tool `search_company_info` untuk mengumpulkan fakta, lalu menulis ringkasan dua kalimat dan email outreach — dan hanya memanggil tool tersebut satu kali per perusahaan.

#### `_search_company_info(company_name: str) -> dict`
**EN:** Another **mocked** stand-in (like `_lookup_company_firmographics` in `llm.py`) for what would be a real web search or CRM lookup. Has fake data for "Acme Corp" and "Globex"; anything else returns "Unknown"/"No public information found."
**ID:** Pengganti **mock** lainnya (seperti `_lookup_company_firmographics` di `llm.py`) untuk apa yang seharusnya berupa pencarian web sungguhan atau lookup CRM. Memiliki data palsu untuk "Acme Corp" dan "Globex"; nama lain akan mengembalikan "Unknown"/"Tidak ada informasi publik yang ditemukan."

#### `AGENT_TOOLS` (constant list) and `_AVAILABLE_TOOLS` (constant dict)
**EN:** Same pattern as `llm.py`'s `TOOLS`/`_AVAILABLE_TOOLS`: a schema describing the `search_company_info` tool for the AI, and a lookup table mapping its name to the real Python function.
**ID:** Pola yang sama dengan `TOOLS`/`_AVAILABLE_TOOLS` di `llm.py`: sebuah skema yang mendeskripsikan tool `search_company_info` untuk AI, dan tabel pencarian yang memetakan namanya ke fungsi Python sesungguhnya.

#### `_AgentFinalAnswer` (Pydantic model)
**EN:** A small private schema (`summary` + `draft_email`) used just for the final structured-output call — separate from the public `ResearchLeadResponse` because the agent itself doesn't need to know about `company_name` or `tool_calls`; those get added afterward.
**ID:** Skema privat kecil (`summary` + `draft_email`) yang dipakai hanya untuk panggilan structured-output terakhir — terpisah dari `ResearchLeadResponse` publik karena agen itu sendiri tidak perlu tahu tentang `company_name` atau `tool_calls`; keduanya ditambahkan belakangan.

#### `research_lead(company_name: str, max_turns: int = 4) -> ResearchLeadResponse`
**EN:** The main agent loop, step by step:
1. Start a conversation with the system prompt and a user message asking to research `company_name`.
2. **Loop** up to `max_turns` times: call the AI with the `AGENT_TOOLS` available.
   - If the AI's reply has no `tool_calls`, it means it's satisfied with the information it has — `break` out of the loop early.
   - Otherwise, execute every requested tool call via `_AVAILABLE_TOOLS`, append the AI's tool request *and* our tool's result back into the `messages` list, and loop again so the AI can see the tool's output.
3. After the loop ends (either by finishing early or hitting `max_turns`), make one final structured-output call asking the AI to produce its `summary` and `draft_email` as an `_AgentFinalAnswer`.
4. Wrap everything (including which tools were actually called, `tool_calls_made`) into the final `ResearchLeadResponse`.

This is exactly the pattern that every "AI agent" framework (LangGraph, CrewAI, AutoGPT, etc.) is built on top of — just written explicitly instead of hidden inside a library.

**ID:** Loop agen utama, langkah demi langkah:
1. Memulai percakapan dengan system prompt dan pesan user yang meminta riset untuk `company_name`.
2. **Loop** hingga `max_turns` kali: memanggil AI dengan `AGENT_TOOLS` yang tersedia.
   - Jika balasan AI tidak memiliki `tool_calls`, artinya AI sudah puas dengan informasi yang dimilikinya — `break` (keluar) dari loop lebih awal.
   - Jika tidak, jalankan setiap permintaan tool call melalui `_AVAILABLE_TOOLS`, tambahkan permintaan tool dari AI *dan* hasil dari tool kita kembali ke dalam daftar `messages`, lalu loop lagi agar AI bisa melihat hasil tool tersebut.
3. Setelah loop berakhir (baik selesai lebih awal atau mencapai `max_turns`), lakukan satu panggilan structured-output terakhir yang meminta AI menghasilkan `summary` dan `draft_email` sebagai `_AgentFinalAnswer`.
4. Bungkus semuanya (termasuk tool apa saja yang benar-benar dipanggil, `tool_calls_made`) menjadi `ResearchLeadResponse` akhir.

Ini persis pola yang menjadi dasar dari setiap framework "AI agent" (LangGraph, CrewAI, AutoGPT, dll.) — hanya saja ditulis secara eksplisit, bukan disembunyikan di dalam sebuah library.

---

### 3.13 `scripts/ingest_docs.py`

**EN Overview:** A standalone script (not part of the running API) that you run manually to load the sample documents into the database. Run it with `python -m scripts.ingest_docs`.

**ID Ringkasan:** Sebuah script mandiri (bukan bagian dari API yang berjalan) yang kamu jalankan secara manual untuk memuat dokumen contoh ke dalam database. Jalankan dengan `python -m scripts.ingest_docs`.

#### `main() -> None`
**EN:** The whole ingestion pipeline, step by step:
1. Open a database connection and make sure the `doc_chunks` table exists (`store.init_schema`).
2. Read every `.md` file in the `docs/` folder.
3. Split each file's text into chunks using `chunk_text()`.
4. Send *all* chunk texts to `embed_texts()` in one batch call, getting back one embedding per chunk.
5. Save every chunk + its embedding into the database with `store.insert_chunks()`.
6. Print how many chunks were ingested, then close the connection.

**ID:** Seluruh pipeline ingestion, langkah demi langkah:
1. Membuka koneksi database dan memastikan tabel `doc_chunks` ada (`store.init_schema`).
2. Membaca setiap file `.md` di folder `docs/`.
3. Memecah teks setiap file menjadi chunk menggunakan `chunk_text()`.
4. Mengirim *semua* teks chunk ke `embed_texts()` dalam satu panggilan batch, mendapatkan kembali satu embedding per chunk.
5. Menyimpan setiap chunk beserta embedding-nya ke database dengan `store.insert_chunks()`.
6. Mencetak berapa banyak chunk yang berhasil di-ingest, lalu menutup koneksi.

**EN — important note:** This script has no duplicate-check — running it twice inserts everything twice. Re-run it only when the files in `docs/` change, and consider clearing the table first if you do.
**ID — catatan penting:** Script ini tidak memiliki pengecekan duplikat — menjalankannya dua kali akan menyisipkan semuanya dua kali. Jalankan ulang hanya ketika file di `docs/` berubah, dan pertimbangkan untuk mengosongkan tabel terlebih dahulu jika kamu melakukannya.

---

## 4. End-to-End Flow / Alur Menyeluruh

**EN:** Here's how a single request travels through the whole system, using `/ask` as the example (the most involved one):

```
1. Client sends POST /ask {"question": "...", "top_k": 4}
2. app/main.py routes it to app/routers/ask.py → ask_endpoint()
3. ask_endpoint() calls app/rag/qa.py → ask()
4. ask() calls app/rag/embeddings.py → embed_texts([question])
   → sends the question text to the AI provider's /embeddings endpoint
   → gets back a vector of 1536 numbers representing the question's meaning
5. ask() calls app/rag/store.py → search(conn, query_embedding, top_k)
   → runs a SQL query in Postgres/pgvector comparing that vector
     against every stored chunk's embedding, returns the closest matches
6. ask() builds a "context" string from those matches
7. ask() calls the AI's chat endpoint (via app/llm.py's get_client())
   with the system prompt + context + question
   → the AI generates a text answer grounded in the context
8. ask() packages the answer + citations into an AskResponse
9. FastAPI serializes it to JSON and sends it back to the client
```

The other three endpoints follow the same overall shape — client → router → logic file → AI/tool calls → structured response — just with different logic files (`llm.py` or `agent/loop.py` instead of `rag/qa.py`) and, in the tool-using ones, an extra back-and-forth loop with the AI before the final answer.

**ID:** Berikut adalah bagaimana satu request melewati keseluruhan sistem, menggunakan `/ask` sebagai contoh (yang paling kompleks):

```
1. Client mengirim POST /ask {"question": "...", "top_k": 4}
2. app/main.py meneruskannya ke app/routers/ask.py → ask_endpoint()
3. ask_endpoint() memanggil app/rag/qa.py → ask()
4. ask() memanggil app/rag/embeddings.py → embed_texts([question])
   → mengirim teks pertanyaan ke endpoint /embeddings milik provider AI
   → mendapatkan kembali vektor berisi 1536 angka yang merepresentasikan makna pertanyaan tersebut
5. ask() memanggil app/rag/store.py → search(conn, query_embedding, top_k)
   → menjalankan query SQL di Postgres/pgvector yang membandingkan vektor tersebut
     dengan embedding dari setiap chunk yang tersimpan, mengembalikan yang paling cocok
6. ask() membangun string "context" dari hasil pencocokan tersebut
7. ask() memanggil endpoint chat milik AI (melalui get_client() dari app/llm.py)
   dengan system prompt + context + pertanyaan
   → AI menghasilkan jawaban teks yang berdasar pada context tersebut
8. ask() mengemas jawaban + citations menjadi sebuah AskResponse
9. FastAPI mengubahnya menjadi JSON dan mengirimkannya kembali ke client
```

Tiga endpoint lainnya mengikuti bentuk keseluruhan yang sama — client → router → file logika → panggilan AI/tool → response terstruktur — hanya dengan file logika yang berbeda (`llm.py` atau `agent/loop.py`, bukan `rag/qa.py`) dan, pada yang memakai tool, ada loop bolak-balik tambahan dengan AI sebelum jawaban akhir.
