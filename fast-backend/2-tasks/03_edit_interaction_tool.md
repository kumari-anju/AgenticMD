# Task: Implement PATCH /tools/edit-interaction

Internal tool-specific API invoked by the LLM when a user provides corrections. It updates only the specific fields mentioned (e.g., changing a name or sentiment) while preserving all other existing form data.

## Requirements
- Endpoint: `PATCH /tools/edit-interaction`
- Input: JSON containing the updated fields.
- Logic: Perform a partial update of the current interaction record.
- Preservation: Ensure all other fields remain unchanged.

## Checklist
- [x] Define the `EditInteractionRequest` Pydantic model.
- [x] Add the tool logic to `app/tools/`.
- [x] Create/Update the database service for interaction modification.
- [x] Integrate with the LangGraph `builder.py` as a tool node.

> [!IMPORTANT]
> Upon completion, update the status in [task_status_update.md](file:///Users/anju/Documents/learning/AgenticMD/fast-backend/task_status_update.md).
