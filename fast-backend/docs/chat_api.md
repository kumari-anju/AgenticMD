# Chat API Endpoint

The `/chat/process` endpoint is the primary gateway for natural language interaction between the UI chat assistant and the LangGraph engine.

## POST /chat/process

Processes a user prompt and triggers the orchestration logic.

### Request Body

- `prompt` (string, required): The natural language input from the user.
- `thread_id` (string, optional): A unique ID to maintain conversation state across multiple calls. If provided, the AI will remember context from previous turns.

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
    "sentiment": null,
    "shared_materials": [],
    "topic_discussed": null
  },
  "thread_id": "session-12345"
}
```

### Testing with CURL

```bash
curl -X POST "http://localhost:8000/api/v1/chat/process" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Hi, I met with HCP Sarah Smith yesterday. She seemed very positive about the new study.",
       "thread_id": "demo-thread-1"
     }'
```
