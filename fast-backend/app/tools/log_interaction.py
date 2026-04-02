from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class LogInteractionSchema(BaseModel):
    """
    Input schema for the log_interaction tool.
    Extracts key fields from a natural language interaction.
    Allows partial updates by making most fields optional.
    """
    hcp_name: Optional[str] = Field(default=None, description="Name of the Healthcare Provider (e.g., 'Dr. Smith')")
    date: Optional[str] = Field(default=None, description="The date of the interaction (e.g., 'Today' or 'YYYY-MM-DD')")
    interaction_type: Optional[str] = Field(default=None, description="The type of interaction (e.g., 'Meeting', 'Phone Conversation', 'Email')")
    sentiment: Optional[str] = Field(default=None, description="The sentiment of the HCP ('Positive', 'Neutral', 'Negative')")
    shared_materials: Optional[List[str]] = Field(default=None, description="Materials shared during the interaction (e.g., ['Brochures', 'Digital Assets'])")
    topic_discussed: Optional[str] = Field(default=None, description="The primary topic or medicine discussed during the interaction")
    time: Optional[str] = Field(default=None, description="The time of the interaction (e.g., '10:30 AM' or 'HH:MM')")

@tool("log_interaction", args_schema=LogInteractionSchema)
def log_interaction(
    hcp_name: Optional[str] = None, 
    date: Optional[str] = None, 
    interaction_type: Optional[str] = None, 
    sentiment: Optional[str] = None, 
    shared_materials: Optional[List[str]] = None, 
    topic_discussed: Optional[str] = None,
    time: Optional[str] = None
):
    """
    Extracts interaction details and updates the form.
    Use this as soon as any information about an interaction is available.
    """
    updates = {}
    if hcp_name is not None: updates["hcp_name"] = hcp_name
    if date is not None: updates["date"] = date
    if interaction_type is not None: updates["interaction_type"] = interaction_type
    if sentiment is not None: updates["sentiment"] = sentiment
    if shared_materials is not None: updates["shared_materials"] = shared_materials
    if topic_discussed is not None: updates["topic_discussed"] = topic_discussed
    if time is not None: updates["time"] = time

    return {
        **updates,
        "status": "success",
        "message": "Successfully logged/updated interaction fields."
    }
