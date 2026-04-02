# AgenticMD Backend Documentation

The AgenticMD backend is a high-performance, industry-standard FastAPI application designed to orchestrate AI-driven interaction logging using LangGraph and Google Gemini.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/) & [LangChain](https://python.langchain.com/)
- **AI Model**: Google Gemini (via `langchain-google-genai`)
- **Database**: SQLite with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)

## 🚀 Setup Guide

### Prerequisites
- Python 3.9+ 
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installation
1. Navigate to the backend directory:
   ```bash
   cd fast-backend
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Configure environment variables in `.env`:
   ```env
   PROJECT_NAME="AgenticMD Backend"
   DATABASE_URL="sqlite:///./sql_app.db"
   GOOGLE_API_KEY="your-gemini-api-key"
   SECRET_KEY="your-secret-key"
   ```

### Running the Server
```bash
uv run uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Swagger Documentation: `http://localhost:8000/docs`

Detailed technical specifications for the AI-driven interactions can be found in the [Interaction & AI Logic Guide](interaction.md).

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/signup`: Register a new user.
- `POST /api/v1/auth/login`: Authenticate and receive a JWT token.

### Chat & Orchestration
- `POST /api/v1/chat/process`: The primary entry point for the AI assistant. Processes natural language prompts and updates form state.
- `GET /api/v1/chat/state`: Retrieves the current form state for a given thread ID.
- `GET /api/v1/chat/stream`: (SSE) Real-time streaming of LangGraph node execution.

### Interaction Tools
These endpoints are used by the LangGraph agent to perform structured operations:
- `POST /api/v1/tools/log-interaction`: Logs a complete interaction to the database.
- `PATCH /api/v1/tools/edit-interaction`: Performs surgical updates on specific fields.
- `POST /api/v1/tools/custom-lookup`: Verifies HCP names and details.
- `POST /api/v1/tools/custom-summarize`: Generates summaries from interaction notes.
- `POST /api/v1/tools/custom-validate`: Validates form completeness before submission.

## 🏗 Architecture & State
The backend follows a layered architecture:
- `app/graph`: **LangGraph** workflow logic and `InteractionState` management.
- `app/tools`: Custom AI tools (Log, Edit, Lookup, Summarize, Validate).
- `app/api`: FastAPI Route handlers and JWT authentication.
- `app/models`: SQLAlchemy database models.
- `app/schemas`: Pydantic models for data validation.
- `app/crud`: Database abstraction layer.

### LangGraph State Schema
The core `InteractionState` includes:
- `hcp_name`, `date`, `time`, `interaction_type`, `sentiment`, `shared_materials`, `topic_discussed`, and `messages` history.
