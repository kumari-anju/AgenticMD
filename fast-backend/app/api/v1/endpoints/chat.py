from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from uuid import uuid4
from sqlalchemy.orm import Session
import json

from app.graph.builder import create_graph
from langchain_core.messages import HumanMessage, BaseMessage
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.crud import conversation as crud_conversation

router = APIRouter()

# Compile the graph once
graph = create_graph()

class ChatRequest(BaseModel):
    prompt: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    state: Dict[str, Any]
    thread_id: str

@router.post("/process", response_model=ChatResponse)
async def process_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Orchestration endpoint for natural language interactions.
    Requires authentication. Links thread to the logged-in user.
    """
    thread_id = request.thread_id or str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Track conversation: create mapping if new thread
    existing = crud_conversation.get_conversation(db, user_id=current_user.id, thread_id=thread_id)
    if not existing:
        crud_conversation.create_conversation(db, user_id=current_user.id, thread_id=thread_id)

    try:
        inputs = {"messages": [HumanMessage(content=request.prompt)]}
        result = graph.invoke(inputs, config=config)

        last_message = result["messages"][-1]
        ai_response = last_message.content if hasattr(last_message, "content") else "I've processed your request."

        form_state = {
            "hcp_name": result.get("hcp_name"),
            "date": result.get("date"),
            "interaction_type": result.get("interaction_type"),
            "sentiment": result.get("sentiment"),
            "shared_materials": result.get("shared_materials", []),
            "topic_discussed": result.get("topic_discussed"),
            "time": result.get("time")
        }

        return ChatResponse(
            response=ai_response,
            state=form_state,
            thread_id=thread_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/state")
async def get_interaction_state(
    thread_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetches the current state of the interaction form for a given thread_id.
    Verifies the user owns the thread.
    """
    # Verify ownership
    conv = crud_conversation.get_conversation(db, user_id=current_user.id, thread_id=thread_id)
    if not conv:
        raise HTTPException(status_code=403, detail="You do not own this conversation.")

    config = {"configurable": {"thread_id": thread_id}}

    try:
        snapshot = graph.get_state(config)
        values = snapshot.values if snapshot.values else {}

        form_state = {
            "hcp_name": values.get("hcp_name"),
            "date": values.get("date"),
            "interaction_type": values.get("interaction_type"),
            "sentiment": values.get("sentiment"),
            "shared_materials": values.get("shared_materials", []),
            "topic_discussed": values.get("topic_discussed"),
            "time": values.get("time")
        }

        return {
            "thread_id": thread_id,
            "state": form_state
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
async def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns all conversation thread_ids for the logged-in user.
    """
    conversations = crud_conversation.get_conversations_by_user(db, user_id=current_user.id)
    return {
        "user_id": current_user.id,
        "conversations": [
            {
                "thread_id": c.thread_id,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in conversations
        ]
    }

@router.get("/history")
async def get_chat_history(
    thread_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the full message history (Human + AI) for a given conversation.
    Verifies the user owns the thread.
    """
    conv = crud_conversation.get_conversation(db, user_id=current_user.id, thread_id=thread_id)
    if not conv:
        raise HTTPException(status_code=403, detail="You do not own this conversation.")

    config = {"configurable": {"thread_id": thread_id}}

    try:
        snapshot = graph.get_state(config)
        values = snapshot.values if snapshot.values else {}
        raw_messages = values.get("messages", [])

        messages = []
        for msg in raw_messages:
            # Normalize role
            if msg.type == "human":
                role = "human"
            elif msg.type in ("ai", "assistant"):
                role = "ai"
            else:
                # Skip tool, system, or other message types
                continue

            # Ensure content is a string
            content = msg.content
            if isinstance(content, list):
                # Handle complex content (e.g., text blocks)
                content = "".join([c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"])
            
            if content:
                messages.append({"role": role, "content": content})

        return {
            "thread_id": thread_id,
            "messages": messages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversations/{thread_id}")
async def delete_conversation(
    thread_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a conversation record for the logged-in user.
    """
    deleted = crud_conversation.delete_conversation(db, user_id=current_user.id, thread_id=thread_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found or not owned by you.")
    return {"status": "deleted", "thread_id": thread_id}

@router.get("/stream")
async def stream_interaction(
    prompt: str,
    thread_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    SSE endpoint that streams real-time state updates as the LangGraph
    processes each node (agent → tools → aggregator → agent).
    Requires authentication.
    """
    thread_id = thread_id or str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [HumanMessage(content=prompt)]}

    # Track conversation
    existing = crud_conversation.get_conversation(db, user_id=current_user.id, thread_id=thread_id)
    if not existing:
        crud_conversation.create_conversation(db, user_id=current_user.id, thread_id=thread_id)

    def event_generator():
        try:
            for event in graph.stream(inputs, config=config, stream_mode="updates"):
                for node_name, node_output in event.items():
                    form_state = {
                        "hcp_name": node_output.get("hcp_name"),
                        "date": node_output.get("date"),
                        "interaction_type": node_output.get("interaction_type"),
                        "sentiment": node_output.get("sentiment"),
                        "shared_materials": node_output.get("shared_materials", []),
                        "topic_discussed": node_output.get("topic_discussed"),
                        "time": node_output.get("time"),
                    }

                    ai_response = None
                    if "messages" in node_output:
                        msgs = node_output["messages"]
                        if msgs and hasattr(msgs[-1], "content"):
                            ai_response = msgs[-1].content

                    payload = {
                        "node": node_name,
                        "state": form_state,
                    }
                    if ai_response:
                        payload["response"] = ai_response

                    yield f"data: {json.dumps(payload)}\n\n"

            # Final event with thread_id
            snapshot = graph.get_state(config)
            values = snapshot.values if snapshot.values else {}
            final_state = {
                "hcp_name": values.get("hcp_name"),
                "date": values.get("date"),
                "interaction_type": values.get("interaction_type"),
                "sentiment": values.get("sentiment"),
                "shared_materials": values.get("shared_materials", []),
                "topic_discussed": values.get("topic_discussed"),
                "time": values.get("time"),
            }
            yield f"data: {json.dumps({'node': '__end__', 'state': final_state, 'thread_id': thread_id})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
