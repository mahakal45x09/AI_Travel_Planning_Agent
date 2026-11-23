"""
Chat Router
============
API endpoints for the chat interface.
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.agents.travel_agent import chat_with_agent, clear_session

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the AI travel agent."""
    try:
        reply, session_id = await chat_with_agent(
            message=request.message,
            session_id=request.session_id,
        )
        return ChatResponse(
            reply=reply,
            session_id=session_id,
            destinations_mentioned=[],  # TODO: Extract mentioned destinations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Clear a chat session."""
    clear_session(session_id)
    return {"message": f"Session {session_id} cleared."}
