# AgenticMD - AI Virtual Office Assistant

AgenticMD is a state-of-the-art interaction management system that uses AI to automate and streamline the process of logging and managing professional interactions.

## 🚀 Project Overview

The project consists of two main components:
1.  **Fast-Backend**: A FastAPI application that powers the AI orchestration using LangGraph and Google Gemini.
2.  **Frontend**: A modern Next.js application that provides a sleek interface for users to interact with the AI assistant.

### Key Features
- **AI-Driven Data Extraction**: Automatically extract interaction details (HCP name, duration, sentiment, etc.) from natural language.
- **Dynamic Form Filling**: See form fields populate in real-time as you describe your interaction to the AI assistant.
- **Core AI Tools**: specialized tools for logging, editing, looking up, summarizing, and validating interactions.
- **Secure Authentication**: Robust role-based access for professionals and physicians.
- **Interactive Dashboard**: A premium UI with session history and real-time state synchronization.

---

## 🛠 Tech Stack

| Backend | Frontend |
| :--- | :--- |
| **FastAPI** (Python 3.9+) | **Next.js 15+** |
| **LangGraph** & LangChain | **React 19** |
| **Google Gemini API** | **Vanilla CSS** (Lucide Icons) |
| **SQLAlchemy** (SQLite) | **Node.js 18+** |
| **uv** Package Manager | **npm** |

---

## 🚀 Getting Started

### 1. Backend Setup
1.  Navigate to the `fast-backend` directory.
2.  Install dependencies using `uv sync`.
3.  Configure your `.env` file with a `GOOGLE_API_KEY`.
4.  Run the server: `uv run uvicorn app.main:app --reload`.

For detailed backend documentation, see [backend.md](backend.md).

### 2. Frontend Setup
1.  Navigate to the `frontend` directory.
2.  Install dependencies: `npm install`.
3.  Run the development server: `npm run dev`.

For detailed frontend documentation and usage instructions, see [frontend.md](frontend.md).

---

## 🏗 Project Structure

```text
AgenticMD/
├── fast-backend/           # FastAPI Backend (Python)
│   ├── app/                # Application Source Code
│   ├── tests/              # Backend Tests
│   └── docs/               # Detailed API Documentation
├── frontend/               # Next.js Frontend (React)
│   ├── app/                # Next.js App Router
│   ├── components/         # Reusable UI Components
│   └── public/             # Static Assets
├── documentation/          # Project Screenshots & Assets
├── backend.md              # Backend Setup & API Guide
├── frontend.md             # Frontend Instruction & Screenshots
└── README.md               # Main Project Documentation
```

## 📜 Documentation Links
- [Backend Detailed Guide](backend.md)
- [Frontend Detailed Guide](frontend.md)
- [Interaction & AI Logic Guide](interaction.md)
