from typing import TypedDict, List, Optional, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class InteractionState(TypedDict):
    """
    Represents the state of the interaction form.
    Standard TypedDict without Annotated labels (except for messages) 
    allows default LangGraph overwrite behavior.
    """
    hcp_name: Optional[str]
    date: Optional[str]
    interaction_type: Optional[str]
    sentiment: Optional[str]
    shared_materials: Optional[List[str]]
    topic_discussed: Optional[str]
    time: Optional[str]
    messages: Annotated[List[BaseMessage], add_messages]
