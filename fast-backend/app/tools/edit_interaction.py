from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class EditInteractionSchema(BaseModel):
    """
    Input schema for the edit_interaction tool.
    Allows surgical updates to existing form fields.
    """
    hcp_name: Optional[str] = Field(description="Updated HCP name")
    date: Optional[str] = Field(description="Updated interaction date")
    interaction_type: Optional[str] = Field(description="Updated interaction type")
    sentiment: Optional[str] = Field(description="Updated HCP sentiment ('Positive', 'Neutral', 'Negative')")
    shared_materials: Optional[List[str]] = Field(description="Updated materials list")
    topic_discussed: Optional[str] = Field(description="Updated interaction topic or medicine")
    time: Optional[str] = Field(description="Updated interaction time (e.g., '10:30 AM')")

@tool("edit_interaction", args_schema=EditInteractionSchema)
def edit_interaction(
    hcp_name: Optional[str] = None,
    date: Optional[str] = None,
    interaction_type: Optional[str] = None,
    sentiment: Optional[str] = None,
    shared_materials: Optional[List[str]] = None,
    topic_discussed: Optional[str] = None,
    time: Optional[str] = None
):
    """
    Makes a surgical update to specific interaction fields.
    Use this when a user wants to CORRECT or UPDATE an existing field in the form.
    This internal tool logically maps to the PATCH /tools/edit-interaction API.
    """
    updates = {}
    if hcp_name is not None:
        updates["hcp_name"] = hcp_name
    if date is not None:
        updates["date"] = date
    if interaction_type is not None:
        updates["interaction_type"] = interaction_type
    if sentiment is not None:
        updates["sentiment"] = sentiment
    if shared_materials is not None:
        updates["shared_materials"] = shared_materials
    if topic_discussed is not None:
        updates["topic_discussed"] = topic_discussed
    if time is not None:
        updates["time"] = time

    # Note: In a production scenario, this function would call the 
    # REST API or shared database layer. For this assignment, we 
    # return the structured values to be aggregated into the LangGraph state.
    return {
        **updates,
        "status": "success",
        "message": "Surgically updated interaction fields."
    }
