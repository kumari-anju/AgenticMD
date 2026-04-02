# Stream API Endpoint (SSE)

The `/chat/stream` endpoint provides real-time updates from the backend to the frontend as the AI processes tools, maintaining the "no manual entry" workflow.

## GET /chat/stream

Streams Server-Sent Events (SSE) as the LangGraph executes nodes for a given prompt.

### Query Parameters

- `prompt` (string, required): The natural language input from the user.
- `thread_id` (string, optional): A unique ID to maintain conversation state. If omitted, a new one is generated.

### Event Format

Each event is a JSON object sent as an SSE `data:` line:

```
data: {"node": "agent", "state": {"hcp_name": null, "interaction_type": null, "topic_discussed": null, ...}}

data: {"node": "tools", "state": {"hcp_name": "Dr. Smith", "interaction_type": "Meeting", "topic_discussed": "Medicine Beta", ...}}

data: {"node": "aggregator", "state": {"hcp_name": "Dr. Smith", "date": "2026-04-02", "interaction_type": "Meeting", "topic_discussed": "Medicine Beta", ...}}

data: {"node": "__end__", "response": "I've logged...", "state": {"hcp_name": "Dr. Smith", "date": "2026-04-02", "interaction_type": "Meeting", "topic_discussed": "Medicine Beta", ...}, "thread_id": "..."}
```

### Testing with CURL

```bash
curl -N "http://localhost:8000/api/v1/chat/stream?prompt=Log+a+meeting+with+Dr.+Lee+today&thread_id=stream-test-1"
```

> [!NOTE]
> The `-N` flag disables curl's output buffering so you can see events as they arrive.
