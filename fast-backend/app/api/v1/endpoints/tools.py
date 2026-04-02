from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

class LogInteractionRequest(BaseModel):
    hcp_name: str = Field(..., description="Name of the Healthcare Provider")
    date: str = Field(..., description="The date of the interaction (YYYY-MM-DD)")
    interaction_type: str = Field(..., description="The type of interaction")
    sentiment: str = Field(..., description="The sentiment ('Positive', 'Neutral', 'Negative')")
    shared_materials: List[str] = Field(default_factory=list, description="Materials shared")
    topic_discussed: Optional[str] = Field(None, description="The primary topic or medicine discussed")

class EditInteractionRequest(BaseModel):
    hcp_name: Optional[str] = Field(None, description="Updated HCP name")
    date: Optional[str] = Field(None, description="Updated interaction date (YYYY-MM-DD)")
    interaction_type: Optional[str] = Field(None, description="Updated interaction type")
    sentiment: Optional[str] = Field(None, description="Updated sentiment")
    shared_materials: Optional[List[str]] = Field(None, description="Updated materials list")
    topic_discussed: Optional[str] = Field(None, description="Updated topic discussed")

class LookupHCPRequest(BaseModel):
    hcp_name: str

class SummarizeNotesRequest(BaseModel):
    notes: str

class ValidateFormRequest(BaseModel):
    hcp_name: Optional[str] = None
    date: Optional[str] = None
    interaction_type: Optional[str] = None
    sentiment: Optional[str] = None
    shared_materials: Optional[List[str]] = None

class ToolResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any]

@router.post("/log-interaction", response_model=ToolResponse)
async def log_interaction_api(
    request: LogInteractionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Internal tool API to log a new interaction.
    """
    return ToolResponse(
        status="success",
        message=f"Successfully logged interaction with {request.hcp_name} on {request.date}.",
        data=request.model_dump()
    )

@router.patch("/edit-interaction", response_model=ToolResponse)
async def edit_interaction_api(
    request: EditInteractionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Internal tool API to surgically update an existing interaction.
    """
    # Filter out None values to perform partial update
    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    return ToolResponse(
        status="success",
        message="Surgically updated interaction fields.",
        data=updates
    )

@router.post("/custom-lookup", response_model=ToolResponse)
async def custom_lookup_api(
    request: LookupHCPRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Internal tool API to search for an HCP.
    """
    if "smith" in request.hcp_name.lower():
        data = {"hcp_name": "Dr. Smith", "specialty": "Cardiology"}
        return ToolResponse(status="Found", message="HCP Found.", data=data)
    return ToolResponse(status="Not Found", message="HCP not in database.", data={})

@router.post("/custom-summarize")
async def custom_summarize_api(
    request: SummarizeNotesRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Internal tool API to summarize interaction notes.
    """
    summary = f"SUMMARY: {request.notes[:50]}..."
    return {"summary": summary}

@router.post("/custom-validate")
async def custom_validate_api(
    request: ValidateFormRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Internal tool API to validate the interaction form.
    """
    missing = []
    if not request.hcp_name: missing.append("HCP Name")
    if not request.date: missing.append("Date")
    if not request.sentiment: missing.append("Sentiment")
    if not request.shared_materials: missing.append("Shared Materials")
    
    if len(missing) == 0:
        return {"status": "Complete", "message": "All required fields are present."}
    return {"status": "Incomplete", "missing_fields": missing, "message": f"Please provide: {', '.join(missing)}"}
