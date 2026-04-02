# FastAPI Backend (Industry Standard)

This project is a FastAPI-based backend structured using industry-standard layered architecture.

## Features
- **Project Managed by `uv`**: Fast and reliable Python package management.
- **SQLAlchemy ORM**: For database interactions.
- **SQLite Database**: Local file-based database for development.
- **Layered Architecture**: Separation of concerns with `api`, `models`, `schemas`, `crud`, and `db` layers.
- **Environment Driven**: Configuration via `.env` file and `pydantic-settings`.

## Project Structure
```text
fast-backend/
├── app/
│   ├── api/                    # API Routing Layer
│   │   └── v1/
│   │       ├── endpoints/      # Route handlers
│   │       └── api.py          # V1 router aggregation
│   ├── core/                   # Global Configuration & Security
│   ├── db/                     # Database Engine & Session
│   ├── models/                 # SQLAlchemy Models (Database definitions)
│   ├── schemas/                # Pydantic Schemas (Data validation)
│   ├── crud/                   # CRUD logic (Database operations)
│   └── main.py                 # FastAPI Application Entry point
├── .env                        # Environment variables
├── pyproject.toml              # uv dependency management
└── README.md                   # Documentation
```

## Getting Started

### Prerequisites
Ensure you have `uv` installed. If not, install it using:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation
Initialize and install dependencies:
```bash
uv sync
```

### Running the Server
Run the FastAPI application with Uvicorn:
```bash
uv run uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

### API Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Backend API Implementation

All backend APIs required for the LangGraph-driven AI assistant have been implemented.

### Endpoints

| # | Endpoint | Method | Purpose |
|---|----------|--------|---------|
| 1 | `/api/v1/chat/process` | POST | Primary orchestration — sends prompts to LangGraph |
| 2 | `/api/v1/tools/log-interaction` | POST | Internal tool API to log a new interaction |
| 3 | `/api/v1/tools/edit-interaction` | PATCH | Internal tool API for surgical field updates |
| 4 | `/api/v1/tools/custom-lookup` | POST | HCP name search/verification |
| 5 | `/api/v1/tools/custom-summarize` | POST | Interaction notes summarization |
| 6 | `/api/v1/tools/custom-validate` | POST | Form completion validation |
| 7 | `/api/v1/chat/state` | GET | Fetch current form state for synchronization |
| 8 | `/api/v1/chat/stream` | GET | SSE stream for real-time state updates |

### Files Created/Modified

#### New Files
- `app/api/v1/endpoints/chat.py` — Chat orchestration, state retrieval, and SSE streaming
- `app/api/v1/endpoints/tools.py` — All 5 internal tool APIs
- `docs/api.md` — Consolidated API documentation (all 9 endpoints)
- `docs/chat_api.md` — Chat endpoint documentation
- `docs/tools_api.md` — All tool endpoint documentation
- `docs/stream_api.md` — SSE streaming documentation

#### Modified Files
- `app/api/v1/api.py` — Registered `chat` and `tools` routers
- `app/graph/builder.py` — Added `MemorySaver` checkpointer for multi-turn conversations
- `app/tools/log_interaction.py` — Refined tool return structure
- `app/tools/edit_interaction.py` — Refined tool return structure
- `app/tools/custom_tools.py` — API mapping annotations and consistent output
- `docs/interaction_api.md` — Added GET state docs

### Test Results

All endpoints were tested with `curl` and returned expected results:

- **POST /chat/process** — Successfully triggered LangGraph, extracted entities, returned AI response with form state
- **POST /tools/log-interaction** — Accepted HCP data, returned structured confirmation
- **PATCH /tools/edit-interaction** — Performed partial update (only `sentiment`), preserved other fields
- **POST /tools/custom-lookup** — Returned HCP details for "Smith" match
- **POST /tools/custom-summarize** — Generated note summary
- **POST /tools/custom-validate** — Identified missing fields in incomplete form
- **GET /chat/state** — Retrieved checkpointed state for a given thread_id
- **GET /chat/stream** — Streamed node-by-node SSE events (`agent → tools → aggregator → agent → __end__`) with `interaction_type` support.
