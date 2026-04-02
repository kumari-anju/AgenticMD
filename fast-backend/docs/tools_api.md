# Tool-Specific Internal APIs

Internal tool-specific APIs are invoked by the LLM when it identifies specific intents. These APIs perform the actual data persistence or logical operations required to populate the form.

## POST /tools/log-interaction

Invoked when a user wants to log a NEW interaction with an HCP.

### Request Body

- `hcp_name` (string, required): Name of the HCP.
- `date` (string, required): Date of the interaction (YYYY-MM-DD).
- `interaction_type` (string, required): Type of interaction (e.g., 'Meeting', 'Phone Conversation').
- `sentiment` (string, required): HCP sentiment ('Positive', 'Neutral', 'Negative').
- `shared_materials` (array of strings): List of materials shared.
- `topic_discussed` (string): The primary topic or medicine discussed.

```json
{
  "hcp_name": "Dr. John Smith",
  "date": "2026-04-01",
  "interaction_type": "Meeting",
  "sentiment": "Positive",
  "shared_materials": ["Product Brochure"],
  "topic_discussed": "Medicine Gamma"
}
```

### Response Body

- `status` (string): 'success' or 'error'.
- `message` (string): A short summary of the action.
- `data` (object): The logged interaction data.

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
    "topic_discussed": "Medicine Gamma"
  }
}
```

### Testing with CURL

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

## PATCH /tools/edit-interaction

Invoked when a user provides corrections or updates to specific fields (e.g., changing a name or sentiment) while preserving other existing form data.

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

- `status` (string): 'success' or 'error'.
- `message` (string): A short summary of the update.
- `data` (object): The updated interaction fields.

```json
{
  "status": "success",
  "message": "Surgically updated interaction fields.",
  "data": {
    "sentiment": "Neutral"
  }
}
```

### Testing with CURL

```bash
curl -X PATCH "http://localhost:8000/api/v1/tools/edit-interaction" \
     -H "Content-Type: application/json" \
     -d '{
       "sentiment": "Negative"
     }'
```

## POST /tools/custom-lookup

Searches for HCP details by name to verify their existence and retrieve basic details.

### Request Body

- `hcp_name` (string): The name to search.

```json
{
  "hcp_name": "Smith"
}
```

### Response Body

- `status` (string): 'Found' or 'Not Found'.
- `data` (object): HCP details or message.

```json
{
  "status": "Found",
  "data": {
    "hcp_name": "Dr. Smith",
    "specialty": "Cardiology"
  }
}
```

### Testing with CURL

```bash
curl -X POST "http://localhost:8000/api/v1/tools/custom-lookup" \
     -H "Content-Type: application/json" \
     -d '{"hcp_name": "Smith"}'
```

## POST /tools/custom-summarize

Generates a concise summary of the interaction based on provide notes.

### Request Body

- `notes` (string): The notes to summarize.

```json
{
  "notes": "HCP Sarah Smith shared positive feedback on the new study and requested a follow-up visit in two weeks."
}
```

### Response Body

- `summary` (string): The generated summary.

```json
{
  "summary": "SUMMARY: HCP Sarah Smith shared positive feedback on the new study and requested a follow-up visit in two weeks..."
}
```

### Testing with CURL

```bash
curl -X POST "http://localhost:8000/api/v1/tools/custom-summarize" \
     -H "Content-Type: application/json" \
     -d '{"notes": "Discussion about X reveals positive interest."}'
```

## POST /tools/custom-validate

Checks if all required interaction fields are populated.

### Request Body

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

- `status` (string): 'Complete' or 'Incomplete'.
- `message` (string): Validation feedback.

```json
{
  "status": "Complete",
  "message": "All required fields are present."
}
```

### Testing with CURL

```bash
curl -X POST "http://localhost:8000/api/v1/tools/custom-validate" \
     -H "Content-Type: application/json" \
     -d '{"hcp_name": "Sarah Smith"}'
```
