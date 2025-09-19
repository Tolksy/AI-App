"""
Agent API routes for autonomous task execution
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.services.agent_service import AgentService

router = APIRouter()


class AgentTaskRequest(BaseModel):
    task: str
    agent_type: str = "general"
    parameters: Optional[Dict[str, Any]] = None


class AgentTaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    steps_completed: List[str]


class AgentStatusResponse(BaseModel):
    agents: Dict[str, Dict[str, Any]]
    crews: Dict[str, Dict[str, Any]]
    active_tasks: int


@router.post("/execute", response_model=AgentTaskResponse)
async def execute_agent_task(
    task_request: AgentTaskRequest,
    background_tasks: BackgroundTasks = None,
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Execute a task using autonomous agents
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        result = await agent_service.execute_complex_task(
            task=task_request.task,
            agent_type=task_request.agent_type,
            parameters=task_request.parameters or {}
        )
        
        return AgentTaskResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute/simple")
async def execute_simple_task(
    task: str,
    agent_type: str = "general",
    context: Optional[Dict[str, Any]] = None,
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Execute a simple task using a single agent
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        result = await agent_service.execute_task(
            task=task,
            agent_type=agent_type,
            context=context or {}
        )
        
        return {
            "response": result.get("response", ""),
            "agent_type": result.get("agent_type", agent_type),
            "status": result.get("status", "completed"),
            "actions": result.get("actions", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=AgentStatusResponse)
async def get_agent_status(
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Get status of all agents and active tasks
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        status = await agent_service.get_agent_status()
        
        return AgentStatusResponse(**status)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents")
async def list_agents(
    agent_service: AgentService = Depends(lambda: None)
):
    """
    List all available agents
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        agents = {}
        for name, agent in agent_service.agents.items():
            agents[name] = {
                "role": agent.role,
                "goal": agent.goal,
                "backstory": agent.backstory,
                "tools_count": len(agent.tools),
                "status": "active"
            }
        
        return {
            "agents": agents,
            "total": len(agents)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crews")
async def list_crews(
    agent_service: AgentService = Depends(lambda: None)
):
    """
    List all available agent crews
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        crews = {}
        for name, crew in agent_service.crews.items():
            crews[name] = {
                "agents": [agent.role for agent in crew.agents],
                "process": crew.process.value,
                "status": "active"
            }
        
        return {
            "crews": crews,
            "total": len(crews)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/active")
async def get_active_tasks(
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Get list of currently active tasks
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        return {
            "active_tasks": list(agent_service.active_tasks.keys()),
            "total": len(agent_service.active_tasks)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Get status of a specific task
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        if task_id not in agent_service.active_tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task_info = agent_service.active_tasks[task_id]
        
        return {
            "task_id": task_id,
            "status": task_info.get("status", "unknown"),
            "started_at": task_info.get("started_at"),
            "completed_at": task_info.get("completed_at"),
            "result": task_info.get("result"),
            "steps_completed": task_info.get("steps_completed", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/research")
async def conduct_research(
    topic: str,
    depth: str = "medium",  # shallow, medium, deep
    sources: Optional[List[str]] = None,
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Conduct research on a specific topic using research agents
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        # Create research task based on depth
        if depth == "shallow":
            task = f"Provide a brief overview and key points about: {topic}"
        elif depth == "deep":
            task = f"Conduct comprehensive research on: {topic}. Include detailed analysis, multiple perspectives, and actionable insights."
        else:  # medium
            task = f"Research and provide detailed information about: {topic}. Include key findings, analysis, and recommendations."
        
        result = await agent_service.execute_complex_task(
            task=task,
            agent_type="research",
            parameters={"sources": sources or [], "depth": depth}
        )
        
        return {
            "topic": topic,
            "depth": depth,
            "research_result": result,
            "sources_used": sources or []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-document")
async def analyze_document_with_agent(
    document_id: str,
    analysis_type: str = "comprehensive",  # summary, key_points, comprehensive, insights
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Analyze a document using document analysis agents
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        task = f"Analyze document {document_id} with {analysis_type} analysis"
        
        result = await agent_service.execute_complex_task(
            task=task,
            agent_type="document_analyst",
            parameters={"document_id": document_id, "analysis_type": analysis_type}
        )
        
        return {
            "document_id": document_id,
            "analysis_type": analysis_type,
            "analysis_result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize-schedule")
async def optimize_schedule_with_agent(
    schedule_data: Dict[str, Any],
    optimization_goals: Optional[List[str]] = None,
    agent_service: AgentService = Depends(lambda: None)
):
    """
    Optimize a schedule using scheduling agents
    """
    try:
        if not agent_service:
            raise HTTPException(status_code=503, detail="Agent service not available")
        
        goals = optimization_goals or ["productivity", "work_life_balance", "efficiency"]
        
        task = f"Optimize the provided schedule for: {', '.join(goals)}. Analyze current schedule and provide specific recommendations."
        
        result = await agent_service.execute_complex_task(
            task=task,
            agent_type="scheduling",
            parameters={"schedule_data": schedule_data, "goals": goals}
        )
        
        return {
            "original_schedule": schedule_data,
            "optimization_goals": goals,
            "optimization_result": result,
            "recommendations": result.get("result", {}).get("output", "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

