"""
Smart AI Lead Generation Agent - FastAPI Backend
Provides intelligent, articulate conversations and autonomous lead generation
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import logging
import json
from datetime import datetime, timedelta
import random
import os

# Import services
from app.services.rag_service import RAGService
from app.services.agent_service import AgentService
from app.services.document_service import DocumentService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="Smart AI Lead Generation Agent",
    description="Autonomous lead generation AI with intelligent conversations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
conversations = {}
leads_database = []


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        logger.info("🚀 Initializing AI Lead Generation Agent services...")

        # Initialize RAG service
        rag_service = RAGService()
        await rag_service.initialize()

        # Initialize Agent service
        agent_service = AgentService()
        await agent_service.initialize()

        # Initialize Document service
        document_service = DocumentService()
        await document_service.initialize(rag_service)

        # Attach to app state
        app.state.rag_service = rag_service
        app.state.agent_service = agent_service
        app.state.document_service = document_service

        logger.info("✅ All services initialized successfully")

    except Exception as e:
        logger.error(f"❌ Error initializing services: {str(e)}")
        raise

# In-memory storage for demo
conversations = {}
leads_database = []


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


class SocialMediaRequest(BaseModel):
    content_type: str = "post"  # post, article, update
    topic: str
    platform: str = "linkedin"
    tone: str = "professional"
    length: str = "medium"
    include_hashtags: bool = True
    scheduled_time: Optional[str] = None


class SocialMediaResponse(BaseModel):
    content: str
    hashtags: List[str]
    optimal_time: str
    engagement_prediction: Dict[str, Any]
    post_id: Optional[str] = None


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


# Social media content creation endpoint
@app.post("/api/v1/social-media/create", response_model=SocialMediaResponse)
async def create_social_media_content(
    request: SocialMediaRequest,
    background_tasks: BackgroundTasks
):
    """
    Create and optionally post social media content using AI agents
    """
    try:
        agent_service: AgentService = app.state.agent_service

        # Create the task for the social media agent
        task = f"""Create a {request.tone} {request.content_type} about {request.topic} for {request.platform}.
        Make it {request.length} length and {'include relevant hashtags' if request.include_hashtags else 'do not include hashtags'}.
        {'Schedule for posting at ' + request.scheduled_time if request.scheduled_time else 'Post immediately'}."""

        # Execute the task using the social media agent
        result = await agent_service.execute_task(
            task=task,
            agent_type="social_media",
            context={
                "platform": request.platform,
                "tone": request.tone,
                "length": request.length,
                "include_hashtags": request.include_hashtags,
                "scheduled_time": request.scheduled_time
            }
        )

        # Parse the result to extract content and metadata
        response_content = result.get("response", "")
        hashtags = ["#business", "#entrepreneurship", "#growth"]  # Default hashtags
        optimal_time = "9:00 AM - 11:00 AM EST"  # Default optimal time
        engagement_prediction = {
            "likes": "50-100",
            "comments": "10-25",
            "shares": "5-15",
            "reach": "500-1000"
        }

        return SocialMediaResponse(
            content=response_content,
            hashtags=hashtags,
            optimal_time=optimal_time,
            engagement_prediction=engagement_prediction
        )

    except Exception as e:
        logger.error(f"Error creating social media content: {str(e)}")
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

