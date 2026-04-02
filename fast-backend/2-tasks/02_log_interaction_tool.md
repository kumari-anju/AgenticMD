# Task: Implement POST /tools/log-interaction

Internal tool-specific API invoked by the LLM when it identifies a request to create a new record. Extracts entities like HCP name, date, sentiment, and shared materials to populate the form.

## Requirements
- Endpoint: `POST /tools/log-interaction`
- Input: JSON containing at least `hcp_name`, `date`, `sentiment`, and `shared_materials`.
- Logic: Create a new interaction record in the database.
- LangGraph Integration: Configure the graph to trigger this tool on "create" intents.

## Checklist
- [x] Define the `LogInteractionRequest` Pydantic model.
- [x] Add the tool logic to `app/tools/`.
- [x] Create/Update the database service for interaction creation.
- [x] Integrate with the LangGraph `builder.py` as a tool node.

> [!IMPORTANT]
> Upon completion, update the status in [task_status_update.md](file:///Users/anju/Documents/learning/AgenticMD/fast-backend/task_status_update.md).
