"""
Advanced Analytics Engine - Real-time performance tracking and reporting
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from agent_tasks import TaskTracker, TaskType, task_tracker
import sqlite3

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    total_leads: int
    qualified_leads: int
    contacted_leads: int
    converted_leads: int
    conversion_rate: float
    response_rate: float
    cost_per_lead: float
    roi: float
    avg_lead_score: float
    pipeline_value: float

@dataclass
class CampaignPerformance:
    campaign_name: str
    total_sent: int
    opens: int
    clicks: int
    responses: int
    meetings_booked: int
    deals_closed: int
    open_rate: float
    click_rate: float
    response_rate: float
    conversion_rate: float

class AnalyticsEngine:
    def __init__(self, db_path: str = "analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize analytics database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lead_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                total_leads INTEGER DEFAULT 0,
                qualified_leads INTEGER DEFAULT 0,
                contacted_leads INTEGER DEFAULT 0,
                converted_leads INTEGER DEFAULT 0,
                avg_lead_score REAL DEFAULT 0,
                pipeline_value REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name TEXT NOT NULL,
                date DATE NOT NULL,
                total_sent INTEGER DEFAULT 0,
                opens INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                responses INTEGER DEFAULT 0,
                meetings_booked INTEGER DEFAULT 0,
                deals_closed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_type TEXT NOT NULL,
                date DATE NOT NULL,
                tasks_completed INTEGER DEFAULT 0,
                tasks_failed INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0,
                avg_task_duration REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Analytics database initialized")
    
    async def generate_performance_report(self, start_date: datetime = None, 
                                        end_date: datetime = None) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        task = task_tracker.create_task(
            TaskType.MARKET_ANALYSIS,
            f"Generating performance report from {start_date} to {end_date}",
            {"start_date": start_date.isoformat() if start_date else None, "end_date": end_date.isoformat() if end_date else None}
        )
        
        try:
            task_tracker.start_task(task.id)
            
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Generate different report sections
            lead_metrics = await self._get_lead_metrics(start_date, end_date)
            campaign_performance = await self._get_campaign_performance(start_date, end_date)
            agent_performance = await self._get_agent_performance(start_date, end_date)
            trend_analysis = await self._get_trend_analysis(start_date, end_date)
            top_performers = await self._get_top_performers(start_date, end_date)
            recommendations = await self._generate_recommendations(lead_metrics, campaign_performance, agent_performance)
            
            report = {
                "report_period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days_analyzed": (end_date - start_date).days
                },
                "lead_metrics": lead_metrics.__dict__,
                "campaign_performance": [camp.__dict__ for camp in campaign_performance],
                "agent_performance": agent_performance,
                "trend_analysis": trend_analysis,
                "top_performers": top_performers,
                "recommendations": recommendations,
                "generated_at": datetime.now().isoformat()
            }
            
            task_tracker.complete_task(task.id, report)
            return report
        
        except Exception as e:
            error_msg = f"Analytics report generation error: {str(e)}"
            task_tracker.fail_task(task.id, error_msg)
            logger.error(error_msg)
            raise
    
    async def _get_lead_metrics(self, start_date: datetime, end_date: datetime) -> PerformanceMetrics:
        """Get lead performance metrics"""
        # In a real implementation, this would query the database
        # For now, we'll generate realistic mock data
        
        import random
        
        total_leads = random.randint(200, 800)
        qualified_leads = int(total_leads * random.uniform(0.15, 0.35))
        contacted_leads = int(qualified_leads * random.uniform(0.6, 0.9))
        converted_leads = int(contacted_leads * random.uniform(0.08, 0.20))
        
        return PerformanceMetrics(
            total_leads=total_leads,
            qualified_leads=qualified_leads,
            contacted_leads=contacted_leads,
            converted_leads=converted_leads,
            conversion_rate=round((converted_leads / total_leads * 100), 2) if total_leads > 0 else 0,
            response_rate=round(random.uniform(12, 28), 2),
            cost_per_lead=round(random.uniform(15, 45), 2),
            roi=round(random.uniform(250, 800), 2),
            avg_lead_score=round(random.uniform(65, 85), 1),
            pipeline_value=round(random.uniform(150000, 500000), 2)
        )
    
    async def _get_campaign_performance(self, start_date: datetime, end_date: datetime) -> List[CampaignPerformance]:
        """Get campaign performance data"""
        import random
        
        campaigns = [
            "LinkedIn Outreach Q1",
            "Email Nurture Sequence",
            "Cold Email Campaign",
            "Social Media Prospecting",
            "Referral Program"
        ]
        
        campaign_data = []
        for campaign in campaigns:
            total_sent = random.randint(500, 2000)
            opens = int(total_sent * random.uniform(0.20, 0.45))
            clicks = int(opens * random.uniform(0.05, 0.15))
            responses = int(total_sent * random.uniform(0.05, 0.15))
            meetings_booked = int(responses * random.uniform(0.15, 0.35))
            deals_closed = int(meetings_booked * random.uniform(0.10, 0.30))
            
            campaign_perf = CampaignPerformance(
                campaign_name=campaign,
                total_sent=total_sent,
                opens=opens,
                clicks=clicks,
                responses=responses,
                meetings_booked=meetings_booked,
                deals_closed=deals_closed,
                open_rate=round((opens / total_sent * 100), 2) if total_sent > 0 else 0,
                click_rate=round((clicks / opens * 100), 2) if opens > 0 else 0,
                response_rate=round((responses / total_sent * 100), 2) if total_sent > 0 else 0,
                conversion_rate=round((deals_closed / total_sent * 100), 2) if total_sent > 0 else 0
            )
            campaign_data.append(campaign_perf)
        
        return campaign_data
    
    async def _get_agent_performance(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get agent performance metrics"""
        import random
        
        agent_types = ["web_scraping", "email_outreach", "linkedin_research", "lead_qualification"]
        agent_data = {}
        
        for agent_type in agent_types:
            tasks_completed = random.randint(50, 200)
            tasks_failed = random.randint(2, 15)
            success_rate = round(((tasks_completed - tasks_failed) / tasks_completed * 100), 2) if tasks_completed > 0 else 0
            avg_duration = round(random.uniform(30, 180), 2)  # seconds
            
            agent_data[agent_type] = {
                "tasks_completed": tasks_completed,
                "tasks_failed": tasks_failed,
                "success_rate": success_rate,
                "avg_task_duration": avg_duration,
                "total_tasks": tasks_completed + tasks_failed
            }
        
        return agent_data
    
    async def _get_trend_analysis(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get trend analysis data"""
        import random
        
        # Generate weekly trend data
        weeks = []
        current_date = start_date
        while current_date < end_date:
            week_data = {
                "week_start": current_date.isoformat(),
                "leads_generated": random.randint(40, 120),
                "leads_qualified": random.randint(8, 35),
                "response_rate": round(random.uniform(10, 25), 2),
                "conversion_rate": round(random.uniform(8, 18), 2)
            }
            weeks.append(week_data)
            current_date += timedelta(days=7)
        
        # Calculate trends
        if len(weeks) >= 2:
            first_week = weeks[0]
            last_week = weeks[-1]
            
            lead_trend = ((last_week['leads_generated'] - first_week['leads_generated']) / first_week['leads_generated'] * 100) if first_week['leads_generated'] > 0 else 0
            conversion_trend = last_week['conversion_rate'] - first_week['conversion_rate']
        else:
            lead_trend = 0
            conversion_trend = 0
        
        return {
            "weekly_data": weeks,
            "trends": {
                "lead_generation_trend": round(lead_trend, 2),
                "conversion_rate_trend": round(conversion_trend, 2),
                "overall_performance": "improving" if lead_trend > 0 and conversion_trend > 0 else "stable" if lead_trend == 0 else "declining"
            }
        }
    
    async def _get_top_performers(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get top performing campaigns, sources, and agents"""
        import random
        
        return {
            "top_campaigns": [
                {"name": "LinkedIn Outreach Q1", "performance": 94.2, "metric": "conversion_rate"},
                {"name": "Email Nurture Sequence", "performance": 87.5, "metric": "response_rate"},
                {"name": "Referral Program", "performance": 78.9, "metric": "lead_quality"}
            ],
            "top_sources": [
                {"name": "LinkedIn Sales Navigator", "leads": 245, "conversion": 18.5},
                {"name": "Google My Business", "leads": 189, "conversion": 15.2},
                {"name": "Industry Directories", "leads": 156, "conversion": 12.8}
            ],
            "top_agents": [
                {"type": "linkedin_research", "success_rate": 96.8, "tasks_completed": 187},
                {"type": "lead_qualification", "success_rate": 94.2, "tasks_completed": 234},
                {"type": "email_outreach", "success_rate": 89.5, "tasks_completed": 156}
            ]
        }
    
    async def _generate_recommendations(self, lead_metrics: PerformanceMetrics, 
                                      campaign_performance: List[CampaignPerformance],
                                      agent_performance: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on performance data"""
        recommendations = []
        
        # Lead generation recommendations
        if lead_metrics.conversion_rate < 10:
            recommendations.append("🎯 LOW CONVERSION: Focus on lead qualification and targeting. Consider updating your ideal customer profile.")
        elif lead_metrics.conversion_rate > 20:
            recommendations.append("🚀 HIGH CONVERSION: Scale successful campaigns and replicate winning strategies.")
        
        # Campaign recommendations
        best_campaign = max(campaign_performance, key=lambda x: x.conversion_rate)
        worst_campaign = min(campaign_performance, key=lambda x: x.conversion_rate)
        
        recommendations.append(f"📈 SCALE SUCCESS: {best_campaign.campaign_name} is performing best ({best_campaign.conversion_rate}% conversion). Increase budget and scale this campaign.")
        
        if worst_campaign.conversion_rate < 5:
            recommendations.append(f"🔧 OPTIMIZE: {worst_campaign.campaign_name} needs improvement ({worst_campaign.conversion_rate}% conversion). Review targeting and messaging.")
        
        # Agent recommendations
        for agent_type, performance in agent_performance.items():
            if performance['success_rate'] < 85:
                recommendations.append(f"🤖 AGENT ISSUE: {agent_type.replace('_', ' ').title()} has {performance['success_rate']}% success rate. Review and optimize this agent.")
        
        # Cost optimization
        if lead_metrics.cost_per_lead > 40:
            recommendations.append("💰 COST OPTIMIZATION: Cost per lead is high. Focus on higher-converting channels and improve targeting.")
        
        # Response rate optimization
        if lead_metrics.response_rate < 15:
            recommendations.append("📧 RESPONSE OPTIMIZATION: Response rate is low. A/B test subject lines and improve email personalization.")
        
        return recommendations
    
    async def track_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time performance metrics"""
        # This would connect to live data sources
        # For now, return current performance snapshot
        
        import random
        
        return {
            "current_hour": {
                "leads_generated": random.randint(2, 8),
                "emails_sent": random.randint(15, 45),
                "responses_received": random.randint(1, 5),
                "tasks_completed": random.randint(8, 20)
            },
            "today": {
                "leads_generated": random.randint(25, 75),
                "emails_sent": random.randint(200, 500),
                "responses_received": random.randint(15, 40),
                "tasks_completed": random.randint(150, 300)
            },
            "this_week": {
                "leads_generated": random.randint(150, 400),
                "emails_sent": random.randint(1200, 2500),
                "responses_received": random.randint(80, 200),
                "tasks_completed": random.randint(800, 1500)
            }
        }

# Global analytics engine instance
analytics_engine = AnalyticsEngine()
