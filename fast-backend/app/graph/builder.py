from typing import List, Literal, Annotated
from datetime import datetime
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, SystemMessage

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from app.graph.state import InteractionState
from app.graph.llm import get_llm
from app.tools.log_interaction import log_interaction
from app.tools.edit_interaction import edit_interaction
from app.tools.custom_tools import lookup_hcp, summarize_notes, validate_form

# Define the set of tools
tools = [log_interaction, edit_interaction, lookup_hcp, summarize_notes, validate_form]
tool_node = ToolNode(tools)
memory = MemorySaver()


def call_model(state: InteractionState):
    """
    Calls the LLM to decide the next action based on the current state.
    """
    llm = get_llm().bind_tools(tools)
    messages = state["messages"]
    
    # System prompt to guide the AI
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_prompt = SystemMessage(content=(
        "You are an AI assistant helping a user populate a healthcare interaction form. "
        f"The current date is {current_date}. "
        "The form has fields: hcp_name, date, time, interaction_type, sentiment, topic_discussed, and shared_materials. "
        "Interaction types include: 'Meeting', 'Phone Conversation', 'Email', 'Video Call', etc. "
        "Extraction Rules: "
        "- 'topic_discussed': Map primary topics, medical discussions, or specific medicine mentions here. "
        "- 'shared_materials': Map physical or digital assets shared here. "
        "When extracting dates (e.g., 'today'), return them as YYYY-MM-DD. "
        "When extracting times, return them in a user-friendly format like '10:30 AM'. "
        "IMPORTANT: Call 'log_interaction' AS SOON AS you extract any field (e.g., just the name or time). "
        "Do NOT wait for all fields to be present. The user wants to see the form update in real-time. "
        "If the user corrects a field, use 'edit_interaction'. "
        "After successfully logging/updating fields, ALWAYS ask the user: "
        "'Would you like me to suggest a specific follow-up action, such as scheduling a meeting?' "
        "Always respond politely and confirm the actions taken."
    ))

    
    # Prepend system prompt if not present
    input_messages = [system_prompt] + messages

    # Safety check: ensure there is at least one HumanMessage
    if not any(isinstance(m, HumanMessage) for m in messages):
        # If no HumanMessage, add a dummy one or handle accordingly
        pass

    response = llm.invoke(input_messages)
    return {"messages": [response]}


def form_aggregator(state: InteractionState):
    """
    Extracts form fields from the latest ToolMessage outputs.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, ToolMessage):
        try:
            # Parse tool output
            import json
            output = json.loads(last_message.content)
            
            # Simple field extraction logic
            updates = {}
            for field in ["hcp_name", "date", "time", "interaction_type", "sentiment", "shared_materials", "topic_discussed"]:
                if field in output:
                    updates[field] = output[field]
            return updates
        except:
             pass
    return {}

def should_continue(state: InteractionState) -> Literal["tools", END]:
    """
    Determines if the graph should continue to tools or end.
    """
    messages = state["messages"]
    last_message = messages[-1]
    # Check if the last message has tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

def create_graph():
    """
    Constructs the LangGraph for AI-assisted data entry.
    """
    workflow = StateGraph(InteractionState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    workflow.add_node("aggregator", form_aggregator)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add conditional edges
    workflow.add_conditional_edges("agent", should_continue)

    # Edge from tools to aggregator, then back to agent
    workflow.add_edge("tools", "aggregator")
    workflow.add_edge("aggregator", "agent")

    return workflow.compile(checkpointer=memory)

