# API Documentation: Process Interaction

This endpoint facilitates the AI-driven data entry process by parsing natural language messages through a LangGraph-based orchestrator.

## 1. Process Interaction

**Endpoint**: `POST /api/v1/interaction/`

### Description
Parses a natural language message and updates the state of the "Interaction Details" form. The AI uses Gemini to extract fields like HCP name, date, sentiment, and materials.

### Request Body
- `message` (string, required): The natural language input from the user (e.g., "Log a positive interaction...").
- `state` (object, optional): The current form state to maintain context across messages.

### Sample CURL Request
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/interaction/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "Log a positive interaction with Dr. Miller from today about brochures.",
  "state": {
    "hcp_name": null,
    "date": null,
    "sentiment": null,
    "shared_materials": [],
    "topic_discussed": null
  }
}'
```

### Success Response (200 OK)
```json
{
  "state": {
    "hcp_name": "Dr. Miller",
    "date": "Today",
    "sentiment": "Positive",
    "shared_materials": ["Brochures"],
    "topic_discussed": "Brochure review",
    "messages": []
  },
  "response": "Successfully logged interaction with Dr. Miller on Today with Positive sentiment.",
  "form_data": {
    "hcp_name": "Dr. Miller",
    "date": "Today",
    "sentiment": "Positive",
    "shared_materials": ["Brochures"],
    "topic_discussed": "Brochure review"
  }
}
```

## 2. Get Interaction State

**Endpoint**: `GET /api/v1/chat/state`

### Description
Fetches the current state of the interaction form to ensure the left-side panel remains synchronized with the AI's actions. Requires a `thread_id` query parameter to identify the conversation.

### Query Parameters
- `thread_id` (string, required): The unique thread identifier used during the chat session.

### Sample CURL Request
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/chat/state?thread_id=test-thread-1' \
  -H 'accept: application/json'
```

### Success Response (200 OK)
```json
{
  "thread_id": "test-thread-1",
  "state": {
    "hcp_name": "Sarah Smith",
    "date": "2026-04-02",
    "interaction_type": "Meeting",
    "sentiment": "Positive",
    "shared_materials": [],
    "topic_discussed": "Meeting topics"
  }
}
```
