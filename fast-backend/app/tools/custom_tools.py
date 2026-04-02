from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class LookupHCPSchema(BaseModel):
    """
    Input schema for the lookup_hcp tool.
    Searches for HCP details by name.
    """
    hcp_name: str = Field(description="Name of the HCP to search")

class SummarizeNotesSchema(BaseModel):
    """
    Input schema for the summarize_notes tool.
    Summarizes the interaction notes.
    """
    notes: str = Field(description="The notes to summarize")

class ValidateFormSchema(BaseModel):
    """
    Input schema for the validate_form tool.
    Checks the interaction state for missing fields.
    """
    hcp_name: Optional[str] = Field(description="Current HCP name")
    date: Optional[str] = Field(description="Current interaction date")
    interaction_type: Optional[str] = Field(description="Current interaction type")
    sentiment: Optional[str] = Field(description="Current HCP sentiment")
    shared_materials: Optional[List[str]] = Field(description="Current shared materials")

@tool("lookup_hcp", args_schema=LookupHCPSchema)
def lookup_hcp(hcp_name: str):
    """
    Searches for an HCP by name to verify their existence and retrieve basic details.
    This internal tool logically maps to the POST /tools/custom-lookup API.
    """
    if "smith" in hcp_name.lower():
        return {"status": "Found", "data": {"hcp_name": "Dr. Smith", "specialty": "Cardiology"}}
    return {"status": "Not Found", "message": "HCP not in database."}

@tool("summarize_notes", args_schema=SummarizeNotesSchema)
def summarize_notes(notes: str):
    """
    Generates a concise summary of the interaction based on provide notes.
    This internal tool logically maps to the POST /tools/custom-summarize API.
    """
    return {"summary": f"SUMMARY: {notes[:50]}..."}

@tool("validate_form", args_schema=ValidateFormSchema)
def validate_form(hcp_name=None, date=None, interaction_type=None, sentiment=None, shared_materials=None):
    """
    Checks if all required interaction fields are populated.
    This internal tool logically maps to the POST /tools/custom-validate API.
    """
    missing = []
    if not hcp_name: missing.append("HCP Name")
    if not date: missing.append("Date")
    if not interaction_type: missing.append("Interaction Type")
    if not sentiment: missing.append("Sentiment")
    if not shared_materials or len(shared_materials) == 0: missing.append("Shared Materials")
    
    if len(missing) == 0:
        return {"status": "Complete", "message": "All required fields are present."}
    return {"status": "Incomplete", "missing_fields": missing, "message": f"Form is incomplete. Please provide: {', '.join(missing)}"}
