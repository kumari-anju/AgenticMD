from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from app.graph.builder import create_graph
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

class InteractionRequest(BaseModel):
    message: str
    state: Optional[dict] = None

class InteractionResponse(BaseModel):
    state: dict
    response: str
    form_data: dict

@router.post("/", response_model=InteractionResponse)
async def process_interaction(
    request: InteractionRequest,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Processes a natural language message through the LangGraph and returns the updated state.
    """
    graph = create_graph()
    
    # Initialize state from request or defaults
    current_state = request.state or {
        "hcp_name": None,
        "date": None,
        "sentiment": None,
        "shared_materials": [],
        "messages": []
    }
    
    # Convert message history if provided
    # (Simplified for now: just appending the new message)
    messages = current_state.get("messages", [])
    # In a real app, we'd deserialize back to BaseMessage objects
    # For now, we'll just use the new message
    input_messages = [HumanMessage(content=request.message)]
    
    # Run the graph
    config = {"configurable": {"thread_id": "1"}} # Dummy thread_id
    result = graph.invoke({"messages": input_messages}, config=config)
    
    # Extract the last AI response
    last_message = result["messages"][-1]
    response_text = last_message.content if isinstance(last_message, AIMessage) else "Processed."
    
    # Prepare response
    return {
        "state": {
            "hcp_name": result.get("hcp_name"),
            "date": result.get("date"),
            "sentiment": result.get("sentiment"),
            "shared_materials": result.get("shared_materials"),
            "messages": [] # Not returning full history in this simplified mode
        },
        "response": response_text,
        "form_data": {
            "hcp_name": result.get("hcp_name"),
            "date": result.get("date"),
            "sentiment": result.get("sentiment"),
            "shared_materials": result.get("shared_materials"),
        }
    }
