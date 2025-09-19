"""
Chat API routes for RAG-based conversations
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.services.rag_service import RAGService
from app.services.agent_service import AgentService

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    use_rag: bool = True
    use_agents: bool = False
    agent_type: Optional[str] = "general"


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[Dict[str, Any]]] = None
    agent_actions: Optional[List[Dict[str, Any]]] = None
    confidence: float


class ConversationHistoryRequest(BaseModel):
    conversation_id: str
    limit: int = 10


@router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    rag_service: RAGService = Depends(lambda: None),
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Send a message and get AI response with RAG and agent capabilities
    """
    try:
        # This would be injected by the main app
        # For now, we'll handle the dependency injection in the main app
        
        response_data = {
            "response": "",
            "conversation_id": request.conversation_id or "new_conversation",
            "sources": [],
            "agent_actions": [],
            "confidence": 0.0
        }
        
        # RAG-based response
        if request.use_rag and rag_service:
            rag_result = await rag_service.generate_response(
                query=request.message,
                conversation_id=response_data["conversation_id"],
                context=request.context
            )
            response_data["response"] = rag_result["response"]
            response_data["sources"] = rag_result.get("sources", [])
            response_data["confidence"] = rag_result.get("confidence", 0.0)
        
        # Agent-based task execution
        if request.use_agents and agent_service:
            agent_result = await agent_service.execute_task(
                task=request.message,
                agent_type=request.agent_type,
                context=request.context or {}
            )
            response_data["agent_actions"] = agent_result.get("actions", [])
            
            # If no RAG response, use agent response
            if not request.use_rag:
                response_data["response"] = agent_result.get("response", "")
        
        # Log conversation for learning
        if rag_service:
            background_tasks.add_task(
                rag_service.log_conversation,
                response_data["conversation_id"],
                request.message,
                response_data["response"]
            )
        
        return ChatResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/history")
async def get_conversation_history(
    conversation_id: str,
    limit: int = 10,
    rag_service: RAGService = Depends(lambda: None)
):
    """
    Get conversation history
    """
    try:
        if not rag_service:
            raise HTTPException(status_code=503, detail="RAG service not available")
        
        history = await rag_service.get_conversation_history(conversation_id, limit)
        
        return {
            "conversation_id": conversation_id,
            "history": history,
            "total_messages": len(history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def clear_conversation(
    conversation_id: str,
    rag_service: RAGService = Depends(lambda: None)
):
    """
    Clear conversation history
    """
    try:
        if not rag_service:
            raise HTTPException(status_code=503, detail="RAG service not available")
        
        await rag_service.clear_conversation(conversation_id)
        
        return {
            "message": "Conversation cleared successfully",
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def list_conversations():
    """
    List all active conversations
    """
    try:
        # This would typically query a database for active conversations
        return {
            "conversations": [],
            "total": 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

