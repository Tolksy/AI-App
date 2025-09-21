"""
Real Agent Task System - Tracks actual AI agent activities and results
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import sqlite3
from dataclasses import dataclass, asdict
import uuid

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(Enum):
    WEB_SCRAPING = "web_scraping"
    EMAIL_OUTREACH = "email_outreach"
    LINKEDIN_RESEARCH = "linkedin_research"
    LEAD_QUALIFICATION = "lead_qualification"
    MARKET_ANALYSIS = "market_analysis"
    COMPETITOR_RESEARCH = "competitor_research"

@dataclass
class AgentTask:
    id: str
    task_type: TaskType
    description: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress_percentage: int = 0
    metadata: Optional[Dict[str, Any]] = None

class TaskTracker:
    def __init__(self, db_path: str = "agent_tasks.db"):
        self.db_path = db_path
        self.active_tasks: Dict[str, AgentTask] = {}
        self.task_history: List[AgentTask] = []
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for task tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_tasks (
                id TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT,
                error TEXT,
                progress_percentage INTEGER DEFAULT 0,
                metadata TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Task tracking database initialized")
    
    def create_task(self, task_type: TaskType, description: str, metadata: Optional[Dict] = None) -> AgentTask:
        """Create a new agent task"""
        task_id = str(uuid.uuid4())
        task = AgentTask(
            id=task_id,
            task_type=task_type,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        # Store in database
        self._save_task_to_db(task)
        self.active_tasks[task_id] = task
        
        logger.info(f"📋 Created task: {task_type.value} - {description}")
        return task
    
    def start_task(self, task_id: str):
        """Mark a task as started"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            task.progress_percentage = 10
            self._update_task_in_db(task)
            logger.info(f"🚀 Started task: {task.description}")
    
    def update_task_progress(self, task_id: str, progress: int, status_update: Optional[str] = None):
        """Update task progress"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.progress_percentage = min(100, max(0, progress))
            if status_update:
                task.metadata = task.metadata or {}
                task.metadata["status_update"] = status_update
            self._update_task_in_db(task)
    
    def complete_task(self, task_id: str, result: Optional[Dict[str, Any]] = None):
        """Mark a task as completed with results"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.progress_percentage = 100
            task.result = result or {}
            self._update_task_in_db(task)
            
            # Move to history
            self.task_history.append(task)
            del self.active_tasks[task_id]
            
            logger.info(f"✅ Completed task: {task.description}")
            if result:
                logger.info(f"📊 Task result: {json.dumps(result, indent=2)}")
    
    def fail_task(self, task_id: str, error: str):
        """Mark a task as failed"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            task.error = error
            self._update_task_in_db(task)
            
            # Move to history
            self.task_history.append(task)
            del self.active_tasks[task_id]
            
            logger.error(f"❌ Failed task: {task.description} - {error}")
    
    def get_active_tasks(self) -> List[AgentTask]:
        """Get all currently active tasks"""
        return list(self.active_tasks.values())
    
    def get_task_history(self, limit: int = 50) -> List[AgentTask]:
        """Get recent task history"""
        return sorted(self.task_history, key=lambda x: x.created_at, reverse=True)[:limit]
    
    def get_task_stats(self) -> Dict[str, Any]:
        """Get task statistics"""
        total_tasks = len(self.task_history) + len(self.active_tasks)
        completed_tasks = len([t for t in self.task_history if t.status == TaskStatus.COMPLETED])
        failed_tasks = len([t for t in self.task_history if t.status == TaskStatus.FAILED])
        
        success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": round(success_rate, 1)
        }
    
    def _save_task_to_db(self, task: AgentTask):
        """Save task to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO agent_tasks 
            (id, task_type, description, status, created_at, started_at, completed_at, result, error, progress_percentage, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id,
            task.task_type.value,
            task.description,
            task.status.value,
            task.created_at.isoformat(),
            task.started_at.isoformat() if task.started_at else None,
            task.completed_at.isoformat() if task.completed_at else None,
            json.dumps(task.result) if task.result else None,
            task.error,
            task.progress_percentage,
            json.dumps(task.metadata) if task.metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def _update_task_in_db(self, task: AgentTask):
        """Update task in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE agent_tasks SET
            status = ?, started_at = ?, completed_at = ?, result = ?, error = ?, progress_percentage = ?, metadata = ?
            WHERE id = ?
        ''', (
            task.status.value,
            task.started_at.isoformat() if task.started_at else None,
            task.completed_at.isoformat() if task.completed_at else None,
            json.dumps(task.result) if task.result else None,
            task.error,
            task.progress_percentage,
            json.dumps(task.metadata) if task.metadata else None,
            task.id
        ))
        
        conn.commit()
        conn.close()

# Global task tracker instance
task_tracker = TaskTracker()
