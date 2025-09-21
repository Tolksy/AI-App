"""
Advanced Lead Scoring System - AI-powered lead qualification and scoring
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from agent_tasks import TaskTracker, TaskType, task_tracker

logger = logging.getLogger(__name__)

@dataclass
class LeadScore:
    total_score: int
    email_score: int
    company_score: int
    engagement_score: int
    fit_score: int
    factors: List[str]
    recommendations: List[str]

class LeadScoringAgent:
    def __init__(self):
        self.scoring_rules = {
            "email_quality": {
                "company_email": 25,
                "gmail": 10,
                "yahoo": 8,
                "hotmail": 5,
                "other": 15
            },
            "company_size": {
                "1-10": 20,
                "11-50": 35,
                "51-200": 50,
                "201-500": 65,
                "500+": 40
            },
            "industry": {
                "technology": 40,
                "saas": 45,
                "healthcare": 35,
                "finance": 30,
                "marketing": 35,
                "consulting": 25,
                "other": 20
            },
            "job_title": {
                "ceo": 40,
                "cto": 35,
                "vp": 30,
                "director": 25,
                "manager": 20,
                "other": 15
            },
            "engagement": {
                "high": 30,
                "medium": 20,
                "low": 10
            },
            "contact_info": {
                "email_only": 20,
                "email_phone": 35,
                "email_phone_address": 50,
                "full_profile": 60
            }
        }
    
    async def score_lead(self, lead_data: Dict[str, Any], 
                        ideal_customer_profile: Dict[str, Any] = None) -> LeadScore:
        """Score a lead based on multiple factors"""
        task = task_tracker.create_task(
            TaskType.LEAD_QUALIFICATION,
            f"Scoring lead: {lead_data.get('name', 'Unknown')}",
            {"lead_data": lead_data, "icp": ideal_customer_profile}
        )
        
        try:
            task_tracker.start_task(task.id)
            
            # Calculate individual scores
            email_score = self._calculate_email_score(lead_data)
            company_score = self._calculate_company_score(lead_data)
            engagement_score = self._calculate_engagement_score(lead_data)
            fit_score = self._calculate_fit_score(lead_data, ideal_customer_profile)
            
            # Calculate total score
            total_score = min(100, email_score + company_score + engagement_score + fit_score)
            
            # Generate factors and recommendations
            factors = self._generate_scoring_factors(lead_data, email_score, company_score, engagement_score, fit_score)
            recommendations = self._generate_recommendations(lead_data, total_score, factors)
            
            lead_score = LeadScore(
                total_score=total_score,
                email_score=email_score,
                company_score=company_score,
                engagement_score=engagement_score,
                fit_score=fit_score,
                factors=factors,
                recommendations=recommendations
            )
            
            result = {
                "lead_score": lead_score.__dict__,
                "scoring_breakdown": {
                    "email_score": email_score,
                    "company_score": company_score,
                    "engagement_score": engagement_score,
                    "fit_score": fit_score,
                    "total_score": total_score
                },
                "qualification_status": self._get_qualification_status(total_score),
                "next_actions": self._get_next_actions(total_score, lead_data)
            }
            
            task_tracker.complete_task(task.id, result)
            return lead_score
        
        except Exception as e:
            error_msg = f"Lead scoring error: {str(e)}"
            task_tracker.fail_task(task.id, error_msg)
            logger.error(error_msg)
            raise
    
    def _calculate_email_score(self, lead_data: Dict[str, Any]) -> int:
        """Calculate email quality score"""
        email = lead_data.get('email', '').lower()
        if not email:
            return 0
        
        # Check email domain
        domain = email.split('@')[1] if '@' in email else ''
        
        if any(company in domain for company in ['gmail', 'yahoo', 'hotmail', 'outlook']):
            return self.scoring_rules['email_quality'].get('gmail', 10)
        elif domain and '.' in domain:
            return self.scoring_rules['email_quality'].get('company_email', 25)
        else:
            return self.scoring_rules['email_quality'].get('other', 15)
    
    def _calculate_company_score(self, lead_data: Dict[str, Any]) -> int:
        """Calculate company-related score"""
        company_size = lead_data.get('company_size', '').lower()
        industry = lead_data.get('industry', '').lower()
        job_title = lead_data.get('title', '').lower()
        
        size_score = 0
        for size_range, score in self.scoring_rules['company_size'].items():
            if size_range in company_size:
                size_score = score
                break
        
        industry_score = 0
        for industry_type, score in self.scoring_rules['industry'].items():
            if industry_type in industry:
                industry_score = score
                break
        
        title_score = 0
        for title_type, score in self.scoring_rules['job_title'].items():
            if title_type in job_title:
                title_score = score
                break
        
        # Average the scores
        return int((size_score + industry_score + title_score) / 3)
    
    def _calculate_engagement_score(self, lead_data: Dict[str, Any]) -> int:
        """Calculate engagement and activity score"""
        engagement_level = lead_data.get('activity_level', 'low').lower()
        mutual_connections = lead_data.get('mutual_connections', 0)
        profile_views = lead_data.get('profile_views', 0)
        
        # Base engagement score
        base_score = self.scoring_rules['engagement'].get(engagement_level, 10)
        
        # Bonus for mutual connections
        if mutual_connections > 10:
            base_score += 10
        elif mutual_connections > 5:
            base_score += 5
        
        # Bonus for profile activity
        if profile_views > 100:
            base_score += 10
        elif profile_views > 50:
            base_score += 5
        
        return min(50, base_score)
    
    def _calculate_fit_score(self, lead_data: Dict[str, Any], 
                           ideal_customer_profile: Dict[str, Any] = None) -> int:
        """Calculate how well the lead fits the ideal customer profile"""
        if not ideal_customer_profile:
            return 20  # Default score if no ICP
        
        fit_score = 0
        total_criteria = 0
        
        # Check industry fit
        if 'target_industries' in ideal_customer_profile:
            lead_industry = lead_data.get('industry', '').lower()
            target_industries = [ind.lower() for ind in ideal_customer_profile['target_industries']]
            if any(target in lead_industry for target in target_industries):
                fit_score += 20
            total_criteria += 1
        
        # Check company size fit
        if 'target_company_sizes' in ideal_customer_profile:
            lead_size = lead_data.get('company_size', '').lower()
            target_sizes = [size.lower() for size in ideal_customer_profile['target_company_sizes']]
            if any(target in lead_size for target in target_sizes):
                fit_score += 20
            total_criteria += 1
        
        # Check job title fit
        if 'target_job_titles' in ideal_customer_profile:
            lead_title = lead_data.get('title', '').lower()
            target_titles = [title.lower() for title in ideal_customer_profile['target_job_titles']]
            if any(target in lead_title for target in target_titles):
                fit_score += 20
            total_criteria += 1
        
        # Check location fit
        if 'target_locations' in ideal_customer_profile:
            lead_location = lead_data.get('location', '').lower()
            target_locations = [loc.lower() for loc in ideal_customer_profile['target_locations']]
            if any(target in lead_location for target in target_locations):
                fit_score += 20
            total_criteria += 1
        
        # Calculate average fit score
        if total_criteria > 0:
            return int(fit_score / total_criteria)
        else:
            return 20
    
    def _generate_scoring_factors(self, lead_data: Dict[str, Any], 
                                 email_score: int, company_score: int, 
                                 engagement_score: int, fit_score: int) -> List[str]:
        """Generate human-readable scoring factors"""
        factors = []
        
        # Email factors
        email = lead_data.get('email', '')
        if email_score >= 20:
            factors.append("✅ Professional company email address")
        elif email_score >= 10:
            factors.append("⚠️ Personal email address (Gmail/Yahoo)")
        else:
            factors.append("❌ Low-quality email address")
        
        # Company factors
        company_size = lead_data.get('company_size', '')
        if company_score >= 40:
            factors.append("✅ Ideal company size for your business")
        elif company_score >= 25:
            factors.append("⚠️ Acceptable company size")
        else:
            factors.append("❌ Company size may not be ideal")
        
        # Engagement factors
        if engagement_score >= 25:
            factors.append("✅ High engagement and activity level")
        elif engagement_score >= 15:
            factors.append("⚠️ Moderate engagement level")
        else:
            factors.append("❌ Low engagement level")
        
        # Fit factors
        if fit_score >= 30:
            factors.append("✅ Excellent fit with ideal customer profile")
        elif fit_score >= 20:
            factors.append("⚠️ Good fit with ideal customer profile")
        else:
            factors.append("❌ Poor fit with ideal customer profile")
        
        # Contact information completeness
        contact_score = 0
        if lead_data.get('email'):
            contact_score += 1
        if lead_data.get('phone'):
            contact_score += 1
        if lead_data.get('address'):
            contact_score += 1
        
        if contact_score >= 3:
            factors.append("✅ Complete contact information available")
        elif contact_score >= 2:
            factors.append("⚠️ Partial contact information")
        else:
            factors.append("❌ Limited contact information")
        
        return factors
    
    def _generate_recommendations(self, lead_data: Dict[str, Any], 
                                total_score: int, factors: List[str]) -> List[str]:
        """Generate actionable recommendations based on lead score"""
        recommendations = []
        
        if total_score >= 80:
            recommendations.extend([
                "🎯 HIGH PRIORITY: Contact immediately",
                "📧 Send personalized email within 24 hours",
                "📞 Schedule a call this week",
                "🔗 Connect on LinkedIn with personalized message"
            ])
        elif total_score >= 60:
            recommendations.extend([
                "📋 MEDIUM PRIORITY: Add to nurture sequence",
                "📧 Send value-driven email",
                "📅 Follow up in 3-5 days",
                "🎯 Focus on pain points and solutions"
            ])
        elif total_score >= 40:
            recommendations.extend([
                "📝 LOW PRIORITY: Add to general outreach",
                "📧 Send educational content",
                "📅 Follow up in 1-2 weeks",
                "🔍 Research more about their company"
            ])
        else:
            recommendations.extend([
                "❌ QUALIFY OUT: Not a good fit",
                "📝 Remove from active outreach",
                "🔍 Focus on higher-scoring leads",
                "📊 Update ideal customer profile"
            ])
        
        # Specific recommendations based on factors
        if "❌ Personal email address" in factors:
            recommendations.append("💡 Try to find their company email address")
        
        if "❌ Low engagement level" in factors:
            recommendations.append("💡 Use different communication channels (phone, LinkedIn)")
        
        if "❌ Limited contact information" in factors:
            recommendations.append("💡 Research more contact details before outreach")
        
        return recommendations
    
    def _get_qualification_status(self, total_score: int) -> str:
        """Get qualification status based on total score"""
        if total_score >= 80:
            return "Hot Lead - Contact Immediately"
        elif total_score >= 60:
            return "Warm Lead - Add to Nurture Sequence"
        elif total_score >= 40:
            return "Cold Lead - General Outreach"
        else:
            return "Unqualified - Remove from Pipeline"
    
    def _get_next_actions(self, total_score: int, lead_data: Dict[str, Any]) -> List[str]:
        """Get next actions based on lead score"""
        actions = []
        
        if total_score >= 80:
            actions = [
                "Send personalized email within 24 hours",
                "Schedule discovery call",
                "Connect on LinkedIn",
                "Add to high-priority follow-up sequence"
            ]
        elif total_score >= 60:
            actions = [
                "Send value-driven email",
                "Add to nurture sequence",
                "Research company pain points",
                "Schedule follow-up in 3-5 days"
            ]
        elif total_score >= 40:
            actions = [
                "Send educational content",
                "Add to general outreach",
                "Research company background",
                "Follow up in 1-2 weeks"
            ]
        else:
            actions = [
                "Qualify out of pipeline",
                "Update ideal customer profile",
                "Focus on higher-scoring leads"
            ]
        
        return actions

# Global lead scoring agent instance
lead_scorer = LeadScoringAgent()
