"""
Simple AI Lead Generation Agent - FastAPI Backend
Basic working version for MVP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import json
from datetime import datetime
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Lead Generation Agent",
    description="Simple lead generation AI",
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

# Pydantic models for API requests/responses
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    confidence: float

class Lead(BaseModel):
    id: str
    name: str
    email: str
    company: str
    industry: str
    status: str
    created_at: str

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Lead Generation Agent",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Simple chat endpoint
@app.post("/api/v1/chat/message", response_model=ChatResponse)
async def chat_message(message: ChatMessage):
    """Simple chat endpoint"""
    try:
        conversation_id = message.conversation_id or f"conv_{random.randint(1000, 9999)}"
        
        # Simple AI responses based on keywords
        user_message = message.message.lower()
        
        if "lead" in user_message or "prospect" in user_message:
            response = "I can help you find leads! What industry are you targeting? I can search for automotive, real estate, technology, healthcare, or other industries."
        elif "automotive" in user_message:
            response = "Great! For automotive leads, I can help you find car dealerships, auto repair shops, and automotive service providers. Would you like me to start searching?"
        elif "real estate" in user_message:
            response = "Perfect! For real estate, I can find property managers, real estate agents, and real estate companies. Should I begin the search?"
        elif "technology" in user_message:
            response = "Excellent! For tech leads, I can find software companies, IT services, and tech startups. Ready to start?"
        elif "help" in user_message or "hello" in user_message:
            response = "Hello! I'm your AI Lead Generation Agent. I can help you find qualified leads in various industries. What type of business are you looking for leads for?"
        else:
            response = "I'm here to help you find leads! Tell me what industry you're targeting and I'll help you find qualified prospects."
        
        # Store conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        conversations[conversation_id].append({
            "user": message.message,
            "ai": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
            confidence=0.85
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get leads endpoint
@app.get("/api/v1/leads/", response_model=List[Lead])
async def get_leads():
    """Get all leads"""
    return leads_database

# Create lead endpoint
@app.post("/api/v1/leads/", response_model=Lead)
async def create_lead(lead: Lead):
    """Create a new lead"""
    leads_database.append(lead)
    return lead

# Get lead statistics
@app.get("/api/v1/leads/stats/overview")
async def get_lead_stats():
    """Get lead statistics"""
    total_leads = len(leads_database)
    industries = {}
    statuses = {}
    
    for lead in leads_database:
        industries[lead.industry] = industries.get(lead.industry, 0) + 1
        statuses[lead.status] = statuses.get(lead.status, 0) + 1
    
    return {
        "total_leads": total_leads,
        "by_industry": industries,
        "by_status": statuses,
        "conversion_rate": 0.12  # Mock conversion rate
    }

# Add some sample leads for demo
@app.on_event("startup")
async def startup_event():
    """Add sample data on startup"""
    sample_leads = [
        Lead(
            id="1",
            name="John Smith",
            email="john@autodealer.com",
            company="Smith Auto Group",
            industry="automotive",
            status="qualified",
            created_at=datetime.now().isoformat()
        ),
        Lead(
            id="2", 
            name="Sarah Johnson",
            email="sarah@realestate.com",
            company="Johnson Properties",
            industry="real estate",
            status="contacted",
            created_at=datetime.now().isoformat()
        ),
        Lead(
            id="3",
            name="Mike Chen",
            email="mike@techstartup.com", 
            company="TechStart Inc",
            industry="technology",
            status="new",
            created_at=datetime.now().isoformat()
        )
    ]
    
    leads_database.extend(sample_leads)
    logger.info("Added sample leads to database")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )