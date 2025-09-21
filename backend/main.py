"""
RAG-based Agentic AI System - Main FastAPI Application
Combines advanced language models with external data retrieval for intelligent responses
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.services.rag_service import RAGService
from app.services.agent_service import AgentService
from app.services.document_service import DocumentService
from app.services.lead_generation_service import LeadGenerationService
from app.services.lead_strategy_ai import LeadStrategyAI
from app.api.routes import chat, documents, agents, scheduling, leads, strategy
from app.middleware.auth import AuthMiddleware
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting RAG-based Agentic AI System - Updated")
    
    # Initialize database
    await init_db()
    
    # Initialize services
    app.state.rag_service = RAGService()
    app.state.agent_service = AgentService()
    app.state.document_service = DocumentService()
    app.state.lead_generation_service = LeadGenerationService()
    app.state.lead_strategy_ai = LeadStrategyAI()
    
    # Initialize vector stores and embeddings
    await app.state.rag_service.initialize()
    await app.state.agent_service.initialize()
    await app.state.lead_generation_service.initialize(
        app.state.rag_service, 
        app.state.agent_service
    )
    await app.state.lead_strategy_ai.initialize(
        app.state.rag_service,
        app.state.agent_service,
        app.state.lead_generation_service
    )
    
    logger.info("✅ All services initialized successfully")
    
    yield
    
    logger.info("🛑 Shutting down RAG-based Agentic AI System")


# Create FastAPI app
app = FastAPI(
    title="RAG-based Agentic AI System",
    description="Advanced AI system combining RAG with autonomous agents for intelligent task execution",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include API routes
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(scheduling.router, prefix="/api/v1/scheduling", tags=["Scheduling"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Lead Generation"])
app.include_router(strategy.router, prefix="/api/v1/strategy", tags=["Strategy AI"])


# Pydantic models for API requests/responses
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    use_rag: bool = True
    use_agents: bool = False


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[Dict[str, Any]]] = None
    agent_actions: Optional[List[Dict[str, Any]]] = None
    confidence: float


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    chunks_processed: int


class AgentTaskRequest(BaseModel):
    task: str
    agent_type: str = "general"
    parameters: Optional[Dict[str, Any]] = None


class AgentTaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    steps_completed: List[str]


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "RAG-based Agentic AI System",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Chat endpoint with RAG and Agent capabilities
@app.post("/api/v1/chat/message", response_model=ChatResponse)
async def chat_message(
    message: ChatMessage,
    background_tasks: BackgroundTasks
):
    """
    Main chat endpoint with RAG and agent capabilities
    """
    try:
        # Get RAG service from app state
        rag_service: RAGService = app.state.rag_service
        agent_service: AgentService = app.state.agent_service
        
        response_data = {
            "response": "",
            "conversation_id": message.conversation_id or "new_conversation",
            "sources": [],
            "agent_actions": [],
            "confidence": 0.0
        }
        
        # RAG-based response
        if message.use_rag:
            rag_result = await rag_service.generate_response(
                query=message.message,
                conversation_id=response_data["conversation_id"],
                context=message.context
            )
            response_data["response"] = rag_result["response"]
            response_data["sources"] = rag_result.get("sources", [])
            response_data["confidence"] = rag_result.get("confidence", 0.0)
        
        # Agent-based task execution
        if message.use_agents and message.message:
            agent_result = await agent_service.execute_task(
                task=message.message,
                context=message.context or {}
            )
            response_data["agent_actions"] = agent_result.get("actions", [])
            
            # If no RAG response, use agent response
            if not message.use_rag:
                response_data["response"] = agent_result.get("response", "")
        
        # Log conversation for learning
        background_tasks.add_task(
            rag_service.log_conversation,
            response_data["conversation_id"],
            message.message,
            response_data["response"]
        )
        
        return ChatResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Document upload endpoint
@app.post("/api/v1/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload and process documents for the knowledge base
    """
    try:
        document_service: DocumentService = app.state.document_service
        
        # Process document in background
        result = await document_service.process_document(
            file=file,
            background_tasks=background_tasks
        )
        
        return DocumentUploadResponse(**result)
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Agent task execution endpoint
@app.post("/api/v1/agents/execute", response_model=AgentTaskResponse)
async def execute_agent_task(
    task_request: AgentTaskRequest,
    background_tasks: BackgroundTasks
):
    """
    Execute autonomous agent tasks
    """
    try:
        agent_service: AgentService = app.state.agent_service
        
        result = await agent_service.execute_complex_task(
            task=task_request.task,
            agent_type=task_request.agent_type,
            parameters=task_request.parameters or {}
        )
        
        return AgentTaskResponse(**result)
        
    except Exception as e:
        logger.error(f"Error executing agent task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Knowledge base search endpoint
@app.get("/api/v1/search")
async def search_knowledge_base(
    query: str,
    limit: int = 10,
    similarity_threshold: float = 0.7
):
    """
    Search the knowledge base using semantic similarity
    """
    try:
        rag_service: RAGService = app.state.rag_service
        
        results = await rag_service.search_documents(
            query=query,
            limit=limit,
            threshold=similarity_threshold
        )
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

