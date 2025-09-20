"""
Lead Generation Strategy API routes
Conversational AI for strategy planning and execution
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.lead_strategy_ai import LeadStrategyAI

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    message: str
    type: str
    suggestions: List[str] = []
    strategy: Optional[Dict[str, Any]] = None
    execution_plan: Optional[str] = None


class StrategyRequest(BaseModel):
    business_type: str
    industry: str
    target_audience: str
    goals: List[str]
    budget: Optional[str] = None
    timeline: Optional[str] = None


class ExecutionPlanRequest(BaseModel):
    strategy_id: str
    execution_type: str = "full"
    start_date: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_strategy_ai(
    request: ChatMessage,
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Chat with the Lead Generation Strategy AI Expert
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        response = await strategy_ai.chat_with_strategy_ai(
            message=request.message,
            context=request.context or {}
        )
        
        return ChatResponse(**response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/history")
async def get_conversation_history(
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Get conversation history with the Strategy AI
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        history = await strategy_ai.get_conversation_history()
        
        return {
            "conversation_history": history,
            "total_messages": len(history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversation/clear")
async def clear_conversation(
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Clear conversation history
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        await strategy_ai.clear_conversation()
        
        return {
            "message": "Conversation history cleared successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategy/create")
async def create_lead_strategy(
    request: StrategyRequest,
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Create a comprehensive lead generation strategy
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        # Create strategy message
        strategy_message = f"""
        Create a lead generation strategy for:
        - Business Type: {request.business_type}
        - Industry: {request.industry}
        - Target Audience: {request.target_audience}
        - Goals: {', '.join(request.goals)}
        - Budget: {request.budget or 'Not specified'}
        - Timeline: {request.timeline or 'Not specified'}
        """
        
        response = await strategy_ai.chat_with_strategy_ai(
            message=strategy_message,
            context={
                "business_type": request.business_type,
                "industry": request.industry,
                "target_audience": request.target_audience,
                "goals": request.goals,
                "budget": request.budget,
                "timeline": request.timeline
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plan/execute")
async def execute_plan(
    request: ExecutionPlanRequest,
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Execute a lead generation plan
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        execution_message = f"""
        Execute the lead generation plan:
        - Strategy ID: {request.strategy_id}
        - Execution Type: {request.execution_type}
        - Start Date: {request.start_date or 'Immediately'}
        """
        
        response = await strategy_ai.chat_with_strategy_ai(
            message=execution_message,
            context={
                "strategy_id": request.strategy_id,
                "execution_type": request.execution_type,
                "start_date": request.start_date
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies/active")
async def get_active_strategies(
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Get active lead generation strategies
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        strategies = await strategy_ai.get_active_strategies()
        
        return {
            "active_strategies": strategies,
            "total_strategies": len(strategies)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plans/execution")
async def get_execution_plans(
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Get execution plans
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        plans = await strategy_ai.get_execution_plans()
        
        return {
            "execution_plans": plans,
            "total_plans": len(plans)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/self-referential/start")
async def start_self_referential_lead_generation(
    strategy_ai: LeadStrategyAI = Depends(lambda: None)
):
    """
    Start finding leads for the software itself
    """
    try:
        if not strategy_ai:
            raise HTTPException(status_code=503, detail="Strategy AI not available")
        
        result = await strategy_ai.start_self_referential_lead_generation()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/expertise/niches")
async def get_supported_niches():
    """
    Get supported business niches and expertise areas
    """
    return {
        "supported_niches": [
            {
                "name": "Automotive",
                "id": "automotive",
                "description": "Car dealerships, auto services, vehicle sales",
                "expertise_level": "expert"
            },
            {
                "name": "Real Estate",
                "id": "real_estate",
                "description": "Real estate agents, property management, home sales",
                "expertise_level": "expert"
            },
            {
                "name": "Technology",
                "id": "technology",
                "description": "Tech companies, startups, IT departments",
                "expertise_level": "expert"
            },
            {
                "name": "Healthcare",
                "id": "healthcare",
                "description": "Medical practices, hospitals, healthcare providers",
                "expertise_level": "expert"
            },
            {
                "name": "SaaS",
                "id": "saas",
                "description": "Software as a Service companies",
                "expertise_level": "expert"
            },
            {
                "name": "E-commerce",
                "id": "ecommerce",
                "description": "Online stores, retail businesses",
                "expertise_level": "expert"
            },
            {
                "name": "Finance",
                "id": "finance",
                "description": "Financial services, banks, insurance",
                "expertise_level": "expert"
            },
            {
                "name": "Consulting",
                "id": "consulting",
                "description": "Business consultants, professional services",
                "expertise_level": "expert"
            },
            {
                "name": "Fitness",
                "id": "fitness",
                "description": "Gyms, personal trainers, fitness studios",
                "expertise_level": "expert"
            },
            {
                "name": "Education",
                "id": "education",
                "description": "Schools, training companies, educational services",
                "expertise_level": "expert"
            }
        ],
        "total_niches": 10
    }


@router.get("/expertise/self-referential")
async def get_self_referential_strategy():
    """
    Get strategy for finding leads for the software itself
    """
    return {
        "target_audience": "Business owners, marketers, sales teams, entrepreneurs",
        "pain_points": [
            "Manual lead generation is time-consuming",
            "Low conversion rates from cold outreach",
            "Difficulty finding qualified prospects",
            "Lack of automated follow-up systems",
            "Poor lead quality and qualification"
        ],
        "buying_signals": [
            "Searching for lead generation software",
            "Complaining about manual processes",
            "Asking about automation tools",
            "Mentioning low conversion rates",
            "Looking for sales solutions"
        ],
        "lead_sources": [
            "LinkedIn (sales and marketing professionals)",
            "Reddit (entrepreneur and business subreddits)",
            "Twitter (business and startup communities)",
            "Facebook groups (entrepreneurs, marketers)",
            "Industry forums and communities",
            "Competitor analysis and customer research"
        ],
        "outreach_channels": [
            "LinkedIn messaging",
            "Email sequences",
            "Social media engagement",
            "Content marketing",
            "Webinar invitations",
            "Case study sharing"
        ],
        "messaging_angles": [
            "Save 10+ hours per week on lead generation",
            "Increase conversion rates by 300%",
            "Automate your entire sales pipeline",
            "Find qualified leads 24/7 without manual work",
            "Never miss a follow-up again"
        ],
        "conversion_tactics": [
            "Free trial offers",
            "ROI calculators",
            "Case study demonstrations",
            "Competitive comparisons",
            "Success story sharing"
        ]
    }


@router.get("/capabilities")
async def get_ai_capabilities():
    """
    Get AI capabilities and features
    """
    return {
        "conversational_ai": {
            "description": "Natural language conversation about lead generation strategy",
            "capabilities": [
                "Niche expertise across all industries",
                "Strategy creation and planning",
                "Plan execution and monitoring",
                "Self-referential lead generation",
                "Real-time advice and recommendations"
            ]
        },
        "niche_expertise": {
            "description": "Deep expertise in specific business niches",
            "capabilities": [
                "Target audience analysis",
                "Pain point identification",
                "Buying signal recognition",
                "Lead source optimization",
                "Outreach channel selection",
                "Message angle development",
                "Conversion tactic recommendations"
            ]
        },
        "strategy_creation": {
            "description": "Comprehensive lead generation strategy development",
            "capabilities": [
                "Business analysis and planning",
                "Target audience definition",
                "Lead source identification",
                "Outreach sequence design",
                "Qualification criteria setup",
                "Success metrics definition",
                "Implementation timeline creation"
            ]
        },
        "plan_execution": {
            "description": "Autonomous execution of lead generation plans",
            "capabilities": [
                "Automated lead sourcing",
                "Intelligent lead qualification",
                "Personalized outreach sequences",
                "Follow-up automation",
                "Performance monitoring",
                "Continuous optimization"
            ]
        },
        "self_referential": {
            "description": "Finding leads for the software itself",
            "capabilities": [
                "Target market identification",
                "Competitor analysis",
                "Lead source discovery",
                "Outreach campaign creation",
                "Conversion optimization",
                "ROI tracking and reporting"
            ]
        }
    }

