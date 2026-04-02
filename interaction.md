# AgenticMD Interaction Documentation

The "Interaction" is the core feature of AgenticMD. It represents a recorded engagement between a professional (user) and a Healthcare Provider (HCP). 

## 🤖 AI-Driven Interaction Logging

AgenticMD uses **LangGraph** to orchestrate an AI agent that listens to natural language and extracts relevant details into a structured form. This allows for rapid, hands-free data entry.

### The Lifecycle of an Interaction
1.  **Input**: The user describes an interaction in plain English (or via voice-to-text).
2.  **Extraction**: The AI agent identifies key entities (HCP name, date, sentiment, etc.).
3.  **Refinement**: The user can correct the AI or add missing details through further conversation.
4.  **Logging**: Once the form is complete, the interaction is finalized and stored in the database.

---

## 📋 Interaction Form Structure

The interaction form consists of several structured fields, all of which can be populated by the AI assistant:

| Field | Description | AI Extraction Logic |
| :--- | :--- | :--- |
| **HCP Name** | Name of the Healthcare Provider. | Identifies names like "Dr. Smith" or "John Doe". |
| **Interaction Type** | Meeting, Phone, Email, etc. | Derived from context like "called him" or "met in person". |
| **Date & Time** | When the interaction occurred. | Recognizes relative dates like "today", "yesterday", or "last Monday". |
| **Sentiment** | The overall tone of the interaction. | Classified as Positive, Neutral, or Negative based on tone. |
| **Topic Discussed** | The primary medical topic or medicine. | Extracted from the core discussion points. |
| **Shared Materials** | Brochures, samples, or documents. | Identifies items mentioned as "shared" or "given". |

---

## 🛠 AI Agent Tools

The AI assistant uses 5 specialized tools to manage the interaction state:

### 1. `log_interaction`
- **Purpose**: Finalizes the current interaction and saves it to the permanent record.
- **Trigger**: When the user says "log this", "submit", or when the form is fully validated and ready.

### 2. `edit_interaction`
- **Purpose**: Performs "surgical" updates on specific fields without affecting others.
- **Trigger**: "Actually, the date was yesterday" or "Change the sentiment to positive".

### 3. `custom_lookup`
- **Purpose**: Verifies if an HCP exists in the system and retrieves their details (e.g., specialty).
- **Trigger**: Automatically called when an HCP name is mentioned.

### 4. `custom_summarize`
- **Purpose**: Condenses detailed notes into a short, readable summary for the database.
- **Trigger**: Used when the user provides lengthy meeting notes.

### 5. `custom_validate`
- **Purpose**: Checks the current state for missing mandatory fields.
- **Trigger**: Called before logging to ensure data integrity.

---

## 🔄 State Synchronization

The interaction state is persistent and synchronized in real-time:
- **Backend Persistence**: LangGraph uses a `MemorySaver` checkpointer to maintain the state across multiple turns for a given `thread_id`.
- **Frontend Sync**: The React frontend uses **Server-Sent Events (SSE)** and the `/state` endpoint to update the UI instantly as the AI processes information.

---

## 💡 Example Conversation

> **User**: "I had a great meeting with Dr. Smith today. He was very impressed with the new product data. I gave him the latest brochure."

**AI Assistant Internal Actions:**
1. Calls `custom_lookup` for "Dr. Smith".
2. Updates state: `hcp_name: "Dr. Smith"`, `date: "2026-04-02"`, `sentiment: "Positive"`, `shared_materials: ["Brochure"]`.
3. Calls `custom_validate` and finds that the interaction is complete.
4. **AI Response**: "Successfully extracted details for Dr. Smith. Everything looks complete. Should I log this interaction for you?"
