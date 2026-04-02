# API Documentation

Complete reference for all backend APIs in the LangGraph-driven AI assistant.

---

## 1. POST /api/v1/auth/signup

Creates a new user account. Validates email uniqueness and password confirmation.

### Request Body
- `email` (string, required): Registered email.
- `full_name` (string, required): Full name.
- `password` (string, required): Password.
- `confirm_pass` (string, required): Password confirmation.
- `role` (string, optional): User role.
- `organization` (string, optional): Organization name.

```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "password123",
  "confirm_pass": "password123",
  "role": "Physician",
  "organization": "General Hospital"
}
```

### Response Body
- `email`: user@example.com
- `full_name`: John Doe
- `id`: 1

---

## 2. POST /api/v1/auth/login

Authenticates user and returns a 24-hour session token.

### Request Body
- `email` (string, required): Registered email.
- `password` (string, required): Password.

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Response Body
- `access_token`: "random_token_string"
- `token_type`: "bearer"

---

## 3. POST /api/v1/chat/process

The primary orchestration endpoint. Receives natural language prompts and sends them to the LangGraph engine.

### Request Body

- `prompt` (string, required): The natural language input from the user.
- `thread_id` (string, optional): A unique ID to maintain conversation state across multiple calls.

```json
{
  "prompt": "Log a new interaction with HCP John Doe for today.",
  "thread_id": "session-12345"
}
```

### Response Body

- `response` (string): The AI's textual confirmation or clarification message.
- `state` (object): The current extracted interaction form data.
- `thread_id` (string): The thread ID used for this conversation.

```json
{
  "response": "Understood. I've logged a new interaction record with HCP John Doe for today (2026-04-01). Is there anything else you'd like to add?",
  "state": {
    "hcp_name": "John Doe",
    "date": "2026-04-01",
    "interaction_type": "Meeting",
    "sentiment": null,
    "shared_materials": [],
    "topic_discussed": null
  },
  "thread_id": "session-12345"
}
```

### CURL

```bash
curl -X POST "http://localhost:8000/api/v1/chat/process" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Hi, I met with HCP Sarah Smith yesterday. She seemed very positive about the new study.",
       "thread_id": "demo-thread-1"
     }'
```

---

## 2. POST /api/v1/interaction/

Parses a natural language message and updates the state of the "Interaction Details" form. The AI uses Gemini to extract fields like HCP name, date, sentiment, and materials.

### Request Body

- `message` (string, required): The natural language input from the user.
- `state` (object, optional): The current form state to maintain context across messages.

```json
{
  "message": "Log a positive interaction with Dr. Miller from today about brochures.",
  "state": {
    "hcp_name": null,
    "date": null,
    "sentiment": null,
    "shared_materials": [],
    "topic_discussed": null
  }
```

### Response Body

```json
{
  "state": {
    "hcp_name": "Dr. Miller",
    "date": "2026-04-02",
    "interaction_type": "Meeting",
    "sentiment": "Positive",
    "shared_materials": ["Brochures"],
    "topic_discussed": "Product benefits",
    "messages": []
  },
  "response": "Successfully logged interaction with Dr. Miller.",
  "form_data": {
    "hcp_name": "Dr. Miller",
    "date": "2026-04-02",
    "interaction_type": "Meeting",
    "sentiment": "Positive",
    "shared_materials": ["Brochures"],
    "topic_discussed": "Product benefits"
  }
}
```

### CURL

```bash
curl -X POST "http://localhost:8000/api/v1/interaction/" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Log a positive interaction with Dr. Miller from today about brochures."
     }'
```

---

## 3. POST /api/v1/tools/log-interaction

Internal tool API invoked by the LLM when it identifies a request to create a new record.

### Request Body

- `hcp_name` (string, required): Name of the HCP.
- `date` (string, required): Date of the interaction (YYYY-MM-DD).
- `interaction_type` (string, required): Type of interaction (e.g., 'Meeting', 'Phone Conversation').
- `sentiment` (string, required): HCP sentiment ('Positive', 'Neutral', 'Negative').
- `shared_materials` (array of strings): List of materials shared.

```json
{
  "hcp_name": "Dr. John Smith",
  "date": "2026-04-01",
  "interaction_type": "Meeting",
  "sentiment": "Positive",
  "shared_materials": ["Product Brochure"]
}
```

### Response Body

```json
{
  "status": "success",
  "message": "Successfully logged interaction with Dr. John Smith on 2026-04-01.",
  "data": {
    "hcp_name": "Dr. John Smith",
    "date": "2026-04-01",
    "interaction_type": "Meeting",
    "sentiment": "Positive",
    "shared_materials": ["Product Brochure"],
    "topic_discussed": "Medicine Alpha"
  }
}
```

### CURL

```bash
curl -X POST "http://localhost:8000/api/v1/tools/log-interaction" \
     -H "Content-Type: application/json" \
     -d '{
       "hcp_name": "Dr. Jane Doe",
       "date": "2026-04-01",
       "sentiment": "Neutral",
       "shared_materials": ["e-Detailing App"]
     }'
```

---

## 4. PATCH /api/v1/tools/edit-interaction

Internal tool API invoked by the LLM when a user provides corrections. Updates only the specific fields mentioned while preserving all other existing form data.

### Request Body

All fields are optional.

- `hcp_name` (string): Updated HCP name.
- `date` (string): Updated interaction date (YYYY-MM-DD).
- `interaction_type` (string): Updated interaction type.
- `sentiment` (string): Updated sentiment ('Positive', 'Neutral', 'Negative').
- `shared_materials` (array of strings): Updated materials list.
- `topic_discussed` (string): Updated primary topic of discussion.

```json
{
  "sentiment": "Neutral"
}
```

### Response Body

```json
{
  "status": "success",
  "message": "Surgically updated interaction fields.",
  "data": {
    "sentiment": "Neutral"
  }
}
```

### CURL

```bash
curl -X PATCH "http://localhost:8000/api/v1/tools/edit-interaction" \
     -H "Content-Type: application/json" \
     -d '{"sentiment": "Negative"}'
```

---

## 5. POST /api/v1/tools/custom-lookup

Searches for HCP details by name to verify their existence and retrieve basic details.

### Request Body

- `hcp_name` (string, required): The name to search.

```json
{
  "hcp_name": "Smith"
}
```

### Response Body

```json
{
  "status": "Found",
  "message": "HCP Found.",
  "data": {
    "hcp_name": "Dr. Smith",
    "specialty": "Cardiology"
  }
}
```

### CURL

```bash
curl -X POST "http://localhost:8000/api/v1/tools/custom-lookup" \
     -H "Content-Type: application/json" \
     -d '{"hcp_name": "Smith"}'
```

---

## 6. POST /api/v1/tools/custom-summarize

Generates a concise summary of the interaction based on provided notes.

### Request Body

- `notes` (string, required): The notes to summarize.

```json
{
  "notes": "HCP Sarah Smith shared positive feedback on the new study."
}
```

### Response Body

```json
{
  "summary": "SUMMARY: HCP Sarah Smith shared positive feedback on the n..."
}
```

### CURL

```bash
curl -X POST "http://localhost:8000/api/v1/tools/custom-summarize" \
     -H "Content-Type: application/json" \
     -d '{"notes": "Discussion about X reveals positive interest."}'
```

---

## 7. POST /api/v1/tools/custom-validate

Checks if all required interaction fields are populated.

### Request Body

All fields are optional.

- `hcp_name` (string): Current HCP name.
- `date` (string): Current interaction date.
- `interaction_type` (string): Current interaction type.
- `sentiment` (string): Current HCP sentiment.
- `shared_materials` (array): Current shared materials.

```json
{
  "hcp_name": "Sarah Smith",
  "date": "2026-04-01",
  "interaction_type": "Meeting",
  "sentiment": "Positive",
  "shared_materials": ["Brochure"]
}
```

### Response Body

```json
{
  "status": "Complete",
  "message": "All required fields are present."
}
```

### CURL

```bash
curl -X POST "http://localhost:8000/api/v1/tools/custom-validate" \
     -H "Content-Type: application/json" \
     -d '{"hcp_name": "Sarah Smith"}'
```

---

## 8. GET /api/v1/chat/state

Fetches the current state of the interaction form to ensure the frontend panel remains synchronized with the AI's actions.

### Query Parameters

- `thread_id` (string, required): The unique thread identifier used during the chat session.

### Response Body

```json
{
  "thread_id": "test-thread-1",
  "state": {
    "hcp_name": "Sarah Smith",
    "date": "2026-04-02",
    "interaction_type": "Meeting",
    "sentiment": "Positive",
    "shared_materials": [],
    "topic_discussed": "Interaction topic"
  }
}
```

### CURL

```bash
curl -X GET "http://localhost:8000/api/v1/chat/state?thread_id=test-thread-1" \
     -H "accept: application/json"
```

---

## 9. GET /api/v1/chat/stream (SSE)

Server-Sent Events endpoint that streams real-time state updates from the backend as the LangGraph processes each node.

### Query Parameters

- `prompt` (string, required): The natural language input from the user.
- `thread_id` (string, optional): A unique ID to maintain conversation state.

### Event Format

Each event is a JSON object sent as an SSE `data:` line:

```
data: {"node": "agent", "state": {"hcp_name": null, ...}}

data: {"node": "tools", "state": {"hcp_name": "Dr. Smith", ...}}

data: {"node": "aggregator", "state": {"hcp_name": "Dr. Smith", "date": "2026-04-02", ...}}

data: {"node": "__end__", "state": {...}, "thread_id": "..."}
```

### CURL

```bash
curl -N "http://localhost:8000/api/v1/chat/stream?prompt=Log+a+meeting+with+Dr.+Lee+today&thread_id=stream-test-1"
```

> **Note:** The `-N` flag disables curl's output buffering so you can see events as they arrive.

---

## 10. GET /api/v1/auth/me

Returns the profile of the currently logged-in user. Requires Bearer token.

### Response Body

```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "Physician",
  "organization": "St. Marys Hospital",
  "id": 1
}
```

### CURL

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer <access_token>"
```

---

## 11. GET /api/v1/chat/history

Returns the full message history (Human + AI messages) for a given conversation. Verifies the user owns the thread.

### Query Parameters

- `thread_id` (string, required): The conversation thread ID.

### Response Body

```json
{
  "thread_id": "abc-123",
  "messages": [
    {"role": "human", "content": "Log a meeting with Dr. Adams today"},
    {"role": "ai", "content": "I can do that. What was the sentiment?"}
  ]
}
```

### CURL

```bash
curl -X GET "http://localhost:8000/api/v1/chat/history?thread_id=abc-123" \
     -H "Authorization: Bearer <access_token>"
```

---

## 12. DELETE /api/v1/chat/conversations/{thread_id}

Deletes a conversation record for the logged-in user. Verifies ownership before deleting.

### Path Parameters

- `thread_id` (string, required): The conversation thread ID to delete.

### Response Body

```json
{
  "status": "deleted",
  "thread_id": "abc-123"
}
```

### CURL

```bash
curl -X DELETE "http://localhost:8000/api/v1/chat/conversations/abc-123" \
     -H "Authorization: Bearer <access_token>"
```
