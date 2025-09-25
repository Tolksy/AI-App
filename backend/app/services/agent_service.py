"""
Agent Service with CrewAI for autonomous task execution
Implements multi-agent systems for complex task automation
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory

from app.core.config import settings, LLM_CONFIG, AGENT_CONFIG
from app.services.rag_service import RAGService
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)


class AgentService:
    """Service for managing autonomous AI agents"""
    
    def __init__(self):
        self.llm = None
        self.rag_service = None
        self.document_service = None
        self.agents = {}
        self.crews = {}
        self.active_tasks = {}
        
    async def initialize(self):
        """Initialize the agent service"""
        try:
            logger.info("Initializing Agent service...")
            
            # Initialize LLM
            await self._initialize_llm()
            
            # Initialize agents
            await self._initialize_agents()
            
            # Initialize crews
            await self._initialize_crews()
            
            logger.info("✅ Agent service initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Agent service: {str(e)}")
            raise
    
    async def _initialize_llm(self):
        """Initialize language model for agents"""
        try:
            llm_config = LLM_CONFIG[settings.DEFAULT_LLM_PROVIDER]
            
            if settings.DEFAULT_LLM_PROVIDER == "openai":
                self.llm = ChatOpenAI(
                    model=llm_config["model"],
                    temperature=llm_config["temperature"],
                    openai_api_key=llm_config["api_key"]
                )
            else:
                # Fallback
                self.llm = OpenAI(
                    temperature=llm_config["temperature"],
                    openai_api_key=llm_config.get("api_key")
                )
                
            logger.info(f"Agent LLM initialized: {llm_config['model']}")
            
        except Exception as e:
            logger.error(f"Error initializing agent LLM: {str(e)}")
            raise
    
    async def _initialize_agents(self):
        """Initialize different types of agents"""
        try:
            # General Purpose Agent
            self.agents["general"] = Agent(
                role="General Assistant",
                goal="Help users with various tasks and provide intelligent assistance",
                backstory="""You are an intelligent AI assistant with access to various tools
                and knowledge sources. You can help with research, analysis, problem-solving,
                and task automation.""",
                verbose=True,
                allow_delegation=False,
                tools=self._get_general_tools(),
                llm=self.llm
            )
            
            # Research Agent
            self.agents["research"] = Agent(
                role="Research Specialist",
                goal="Conduct thorough research and analysis on any topic",
                backstory="""You are a dedicated research specialist with expertise in
                information gathering, analysis, and synthesis. You excel at finding
                relevant information from multiple sources and presenting it clearly.""",
                verbose=True,
                allow_delegation=False,
                tools=self._get_research_tools(),
                llm=self.llm
            )
            
            # Scheduling Agent
            self.agents["scheduling"] = Agent(
                role="Schedule Optimization Specialist",
                goal="Optimize schedules and time management for maximum productivity",
                backstory="""You are an expert in time management and productivity optimization.
                You help users create efficient schedules, identify time-wasting activities,
                and suggest improvements for better work-life balance.""",
                verbose=True,
                allow_delegation=False,
                tools=self._get_scheduling_tools(),
                llm=self.llm
            )
            
            # Document Analysis Agent
            self.agents["document_analyst"] = Agent(
                role="Document Analysis Expert",
                goal="Analyze and extract insights from documents",
                backstory="""You are a document analysis expert who can read, understand,
                and extract key information from various document types. You excel at
                summarizing content, identifying patterns, and providing actionable insights.""",
                verbose=True,
                allow_delegation=False,
                tools=self._get_document_tools(),
                llm=self.llm
            )

            # Social Media Agent
            self.agents["social_media"] = Agent(
                role="Social Media Content Creator and Manager",
                goal="Create engaging content and manage social media presence",
                backstory="""You are a social media expert who creates compelling content,
                optimizes posts for engagement, researches trending topics, and manages
                posting schedules across platforms. You excel at understanding audience
                behavior and creating content that drives engagement and growth.""",
                verbose=True,
                allow_delegation=False,
                tools=self._get_social_media_tools(),
                llm=self.llm
            )

            logger.info("Initialized all agent types")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {str(e)}")
            raise
    
    async def _initialize_crews(self):
        """Initialize agent crews for collaborative tasks"""
        try:
            # Research Crew
            self.crews["research_crew"] = Crew(
                agents=[self.agents["research"], self.agents["document_analyst"]],
                tasks=[],  # Tasks will be added dynamically
                verbose=True,
                process=Process.sequential
            )
            
            # Productivity Crew
            self.crews["productivity_crew"] = Crew(
                agents=[self.agents["scheduling"], self.agents["general"]],
                tasks=[],
                verbose=True,
                process=Process.hierarchical,
                manager_agent=self.agents["general"]
            )
            
            # Analysis Crew
            self.crews["analysis_crew"] = Crew(
                agents=[
                    self.agents["document_analyst"],
                    self.agents["research"],
                    self.agents["general"]
                ],
                tasks=[],
                verbose=True,
                process=Process.sequential
            )
            
            logger.info("Initialized all agent crews")
            
        except Exception as e:
            logger.error(f"Error initializing crews: {str(e)}")
            raise
    
    def _get_general_tools(self) -> List:
        """Get tools for general agent"""
        return [
            web_search_tool,
            calculator_tool,
            time_analysis_tool,
            knowledge_search_tool
        ]

    def _get_research_tools(self) -> List:
        """Get tools for research agent"""
        return [
            web_search_tool,
            knowledge_search_tool,
            document_analysis_tool,
            data_extraction_tool
        ]

    def _get_scheduling_tools(self) -> List:
        """Get tools for scheduling agent"""
        return [
            calendar_analysis_tool,
            time_analysis_tool,
            productivity_suggestions_tool,
            schedule_optimization_tool
        ]

    def _get_document_tools(self) -> List:
        """Get tools for document analysis agent"""
        return [
            document_analysis_tool,
            content_extraction_tool,
            summary_generation_tool,
            knowledge_search_tool
        ]

    def _get_social_media_tools(self) -> List:
        """Get tools for social media agent"""
        return [
            content_creation_tool,
            post_optimization_tool,
            hashtag_research_tool,
            engagement_analysis_tool,
            scheduling_tool,
            linkedin_posting_tool
        ]
    
    async def execute_task(
        self,
        task: str,
        agent_type: str = "general",
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute a task using the specified agent"""
        try:
            if agent_type not in self.agents:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            agent = self.agents[agent_type]
            
            # Create task
            crewai_task = Task(
                description=task,
                expected_output="A comprehensive response addressing the task",
                agent=agent
            )
            
            # Create temporary crew
            crew = Crew(
                agents=[agent],
                tasks=[crewai_task],
                verbose=True
            )
            
            # Execute task
            result = await asyncio.get_event_loop().run_in_executor(
                None, crew.kickoff
            )
            
            return {
                "response": str(result),
                "agent_type": agent_type,
                "status": "completed",
                "actions": [{"action": "task_execution", "result": str(result)}]
            }
            
        except Exception as e:
            logger.error(f"Error executing task: {str(e)}")
            return {
                "response": f"I encountered an error while executing the task: {str(e)}",
                "agent_type": agent_type,
                "status": "error",
                "actions": []
            }
    
    async def execute_complex_task(
        self,
        task: str,
        agent_type: str = "general",
        parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute complex tasks using agent crews"""
        try:
            task_id = f"task_{datetime.utcnow().timestamp()}"
            self.active_tasks[task_id] = {
                "status": "running",
                "started_at": datetime.utcnow(),
                "steps_completed": []
            }
            
            # Determine appropriate crew
            if "research" in task.lower() or "analyze" in task.lower():
                crew = self.crews["research_crew"]
            elif "schedule" in task.lower() or "time" in task.lower():
                crew = self.crews["productivity_crew"]
            elif "document" in task.lower() or "analyze" in task.lower():
                crew = self.crews["analysis_crew"]
            else:
                crew = self.crews["productivity_crew"]  # Default
            
            # Create tasks for the crew
            tasks = self._create_crew_tasks(task, parameters or {})
            
            # Update crew tasks
            crew.tasks = tasks
            
            # Execute crew
            result = await asyncio.get_event_loop().run_in_executor(
                None, crew.kickoff
            )
            
            self.active_tasks[task_id].update({
                "status": "completed",
                "completed_at": datetime.utcnow(),
                "result": str(result)
            })
            
            return {
                "task_id": task_id,
                "status": "completed",
                "result": {"output": str(result)},
                "steps_completed": [task.description for task in tasks]
            }
            
        except Exception as e:
            logger.error(f"Error executing complex task: {str(e)}")
            return {
                "task_id": task_id,
                "status": "error",
                "result": {"error": str(e)},
                "steps_completed": []
            }
    
    def _create_crew_tasks(self, main_task: str, parameters: Dict[str, Any]) -> List[Task]:
        """Create tasks for agent crews"""
        tasks = []
        
        # Primary task
        tasks.append(Task(
            description=main_task,
            expected_output="Initial analysis and task breakdown",
            agent=self.agents["general"]
        ))
        
        # Research task if needed
        if "research" in main_task.lower():
            tasks.append(Task(
                description=f"Research and gather information for: {main_task}",
                expected_output="Comprehensive research findings",
                agent=self.agents["research"]
            ))
        
        # Analysis task
        tasks.append(Task(
            description=f"Analyze and synthesize information for: {main_task}",
            expected_output="Detailed analysis and recommendations",
            agent=self.agents["document_analyst"]
        ))
        
        return tasks
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents and active tasks"""
        return {
            "agents": {
                name: {
                    "role": agent.role,
                    "goal": agent.goal,
                    "tools_count": len(agent.tools),
                    "status": "active",
                    "backstory": agent.backstory
                }
                for name, agent in self.agents.items()
            },
            "crews": {
                name: {
                    "agents": [agent.role for agent in crew.agents],
                    "process": crew.process.value,
                    "status": "active"
                }
                for name, crew in self.crews.items()
            },
            "active_tasks": len(self.active_tasks)
        }


# Tool definitions for agents
@tool
def web_search_tool(query: str) -> str:
    """Search the web for current information"""
    try:
        # This would integrate with a real web search API
        return f"Web search results for: {query}\n[This would contain actual search results]"
    except Exception as e:
        return f"Error searching web: {str(e)}"

@tool
def calculator_tool(expression: str) -> str:
    """Perform mathematical calculations"""
    try:
        # Simple calculator implementation
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

@tool
def time_analysis_tool(schedule_data: str) -> str:
    """Analyze time usage and productivity patterns"""
    try:
        # Analyze schedule data
        return "Time analysis: [This would contain detailed time analysis]"
    except Exception as e:
        return f"Error analyzing time: {str(e)}"

@tool
def knowledge_search_tool(query: str) -> str:
    """Search the knowledge base for relevant information"""
    try:
        # This would use the RAG service
        return f"Knowledge base search for: {query}\n[This would contain relevant documents]"
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

@tool
def document_analysis_tool(document_id: str) -> str:
    """Analyze a specific document"""
    try:
        return f"Document analysis for ID: {document_id}\n[This would contain document insights]"
    except Exception as e:
        return f"Error analyzing document: {str(e)}"

@tool
def data_extraction_tool(source: str, criteria: str) -> str:
    """Extract specific data from sources"""
    try:
        return f"Data extraction from {source} with criteria: {criteria}\n[This would contain extracted data]"
    except Exception as e:
        return f"Error extracting data: {str(e)}"

@tool
def calendar_analysis_tool(date_range: str) -> str:
    """Analyze calendar and scheduling patterns"""
    try:
        return f"Calendar analysis for {date_range}\n[This would contain scheduling insights]"
    except Exception as e:
        return f"Error analyzing calendar: {str(e)}"

@tool
def productivity_suggestions_tool(current_schedule: str) -> str:
    """Generate productivity improvement suggestions"""
    try:
        return f"Productivity suggestions based on schedule:\n[This would contain actionable suggestions]"
    except Exception as e:
        return f"Error generating suggestions: {str(e)}"

@tool
def schedule_optimization_tool(schedule_data: str) -> str:
    """Optimize schedule for better productivity"""
    try:
        return f"Schedule optimization:\n[This would contain optimized schedule recommendations]"
    except Exception as e:
        return f"Error optimizing schedule: {str(e)}"

@tool
def content_extraction_tool(document_content: str) -> str:
    """Extract key content from documents"""
    try:
        return f"Content extraction:\n[This would contain extracted key points]"
    except Exception as e:
        return f"Error extracting content: {str(e)}"

@tool
def summary_generation_tool(content: str) -> str:
    """Generate summaries of content"""
    try:
        return f"Summary:\n[This would contain a concise summary]"
    except Exception as e:
        return f"Error generating summary: {str(e)}"

@tool
def content_creation_tool(topic: str, platform: str = "linkedin", tone: str = "professional") -> str:
    """Create engaging social media content"""
    try:
        # This would use AI to generate content based on topic, platform, and tone
        return f"Generated {tone} content for {platform} about: {topic}\n[This would contain actual generated content]"
    except Exception as e:
        return f"Error creating content: {str(e)}"

@tool
def post_optimization_tool(content: str, platform: str = "linkedin") -> str:
    """Optimize content for better engagement"""
    try:
        # This would analyze and optimize the content
        return f"Optimized content for {platform}:\n[This would contain optimized version]"
    except Exception as e:
        return f"Error optimizing content: {str(e)}"

@tool
def hashtag_research_tool(topic: str, count: int = 10) -> str:
    """Research relevant hashtags for content"""
    try:
        # This would research trending and relevant hashtags
        return f"Top {count} hashtags for '{topic}':\n[This would contain actual hashtag research]"
    except Exception as e:
        return f"Error researching hashtags: {str(e)}"

@tool
def engagement_analysis_tool(post_content: str, platform: str = "linkedin") -> str:
    """Analyze potential engagement for content"""
    try:
        # This would predict engagement metrics
        return f"Engagement analysis for {platform}:\n[This would contain engagement predictions]"
    except Exception as e:
        return f"Error analyzing engagement: {str(e)}"

@tool
def scheduling_tool(optimal_times: str = "business_hours") -> str:
    """Suggest optimal posting times"""
    try:
        # This would suggest best times to post
        return f"Optimal posting schedule:\n[This would contain scheduling recommendations]"
    except Exception as e:
        return f"Error with scheduling: {str(e)}"

@tool
def linkedin_posting_tool(content: str, scheduled_time: str = None) -> str:
    """Post content to LinkedIn"""
    try:
        # This would integrate with LinkedIn API to post content
        return f"LinkedIn post scheduled/published:\n[This would contain posting confirmation]"
    except Exception as e:
        return f"Error posting to LinkedIn: {str(e)}"

