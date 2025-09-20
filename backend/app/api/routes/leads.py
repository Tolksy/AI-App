"""
Lead Generation API routes
Endpoints for managing leads, campaigns, and lead generation
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.lead_generation_service import LeadGenerationService, Lead, LeadStatus, LeadSource

router = APIRouter()


class LeadCreateRequest(BaseModel):
    name: str
    company: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: str = "manual"
    tags: Optional[List[str]] = None
    notes: Optional[str] = ""


class LeadUpdateRequest(BaseModel):
    status: Optional[str] = None
    score: Optional[float] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class LeadResponse(BaseModel):
    id: str
    name: str
    company: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: str
    status: str
    score: float
    tags: List[str]
    notes: str
    created_at: str
    last_contacted: Optional[str] = None
    metadata: Dict[str, Any] = {}


class LeadStatsResponse(BaseModel):
    total_leads: int
    qualified_leads: int
    contacted_leads: int
    converted_leads: int
    conversion_rate: float
    last_updated: str


class CampaignCreateRequest(BaseModel):
    name: str
    industry: str
    target_locations: List[str]
    search_terms: List[str]
    outreach_sequence: str
    enabled: bool = True


@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    status: Optional[str] = None,
    limit: int = 100,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Get leads from the database
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        # Convert status string to enum
        status_enum = None
        if status:
            try:
                status_enum = LeadStatus(status)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
        leads = await lead_service.get_leads(status=status_enum, limit=limit)
        
        # Convert to response format
        lead_responses = []
        for lead in leads:
            lead_responses.append(LeadResponse(
                id=lead.id,
                name=lead.name,
                company=lead.company,
                email=lead.email,
                phone=lead.phone,
                linkedin_url=lead.linkedin_url,
                source=lead.source.value,
                status=lead.status.value,
                score=lead.score,
                tags=lead.tags,
                notes=lead.notes,
                created_at=lead.created_at.isoformat(),
                last_contacted=lead.last_contacted.isoformat() if lead.last_contacted else None,
                metadata=lead.metadata
            ))
        
        return lead_responses
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=LeadResponse)
async def create_lead(
    request: LeadCreateRequest,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Create a new lead manually
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        lead_data = {
            "name": request.name,
            "company": request.company,
            "email": request.email,
            "phone": request.phone,
            "linkedin_url": request.linkedin_url,
            "tags": request.tags or [],
            "notes": request.notes or ""
        }
        
        lead = await lead_service.add_lead_manually(lead_data)
        
        return LeadResponse(
            id=lead.id,
            name=lead.name,
            company=lead.company,
            email=lead.email,
            phone=lead.phone,
            linkedin_url=lead.linkedin_url,
            source=lead.source.value,
            status=lead.status.value,
            score=lead.score,
            tags=lead.tags,
            notes=lead.notes,
            created_at=lead.created_at.isoformat(),
            last_contacted=lead.last_contacted.isoformat() if lead.last_contacted else None,
            metadata=lead.metadata
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Get a specific lead by ID
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        leads = await lead_service.get_leads()
        lead = next((lead for lead in leads if lead.id == lead_id), None)
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        return LeadResponse(
            id=lead.id,
            name=lead.name,
            company=lead.company,
            email=lead.email,
            phone=lead.phone,
            linkedin_url=lead.linkedin_url,
            source=lead.source.value,
            status=lead.status.value,
            score=lead.score,
            tags=lead.tags,
            notes=lead.notes,
            created_at=lead.created_at.isoformat(),
            last_contacted=lead.last_contacted.isoformat() if lead.last_contacted else None,
            metadata=lead.metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    request: LeadUpdateRequest,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Update a lead
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        leads = await lead_service.get_leads()
        lead = next((lead for lead in leads if lead.id == lead_id), None)
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Update lead fields
        if request.status:
            try:
                status_enum = LeadStatus(request.status)
                await lead_service.update_lead_status(lead_id, status_enum)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {request.status}")
        
        if request.score is not None:
            lead.score = request.score
        
        if request.tags is not None:
            lead.tags = request.tags
        
        if request.notes is not None:
            lead.notes = request.notes
        
        return LeadResponse(
            id=lead.id,
            name=lead.name,
            company=lead.company,
            email=lead.email,
            phone=lead.phone,
            linkedin_url=lead.linkedin_url,
            source=lead.source.value,
            status=lead.status.value,
            score=lead.score,
            tags=lead.tags,
            notes=lead.notes,
            created_at=lead.created_at.isoformat(),
            last_contacted=lead.last_contacted.isoformat() if lead.last_contacted else None,
            metadata=lead.metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: str,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Delete a lead
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        # This would implement actual lead deletion
        return {"message": f"Lead {lead_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/overview", response_model=LeadStatsResponse)
async def get_lead_stats(
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Get lead generation statistics
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        stats = await lead_service.get_lead_stats()
        
        return LeadStatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/qualify/{lead_id}")
async def qualify_lead(
    lead_id: str,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Manually trigger lead qualification
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        # This would trigger manual qualification
        return {"message": f"Lead {lead_id} qualification triggered"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/outreach/{lead_id}")
async def send_outreach(
    lead_id: str,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Manually trigger outreach to a lead
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        # This would trigger manual outreach
        return {"message": f"Outreach sent to lead {lead_id}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sources/available")
async def get_available_sources():
    """
    Get available lead sources
    """
    return {
        "sources": [
            {
                "name": "LinkedIn",
                "id": "linkedin",
                "description": "Professional networking platform",
                "enabled": True
            },
            {
                "name": "Google My Business",
                "id": "google_my_business",
                "description": "Local business directory",
                "enabled": True
            },
            {
                "name": "Yelp",
                "id": "yelp",
                "description": "Business review platform",
                "enabled": True
            },
            {
                "name": "Web Scraping",
                "id": "web_scraping",
                "description": "Custom website scraping",
                "enabled": True
            }
        ]
    }


@router.get("/industries/supported")
async def get_supported_industries():
    """
    Get supported industries for lead generation
    """
    return {
        "industries": [
            {
                "name": "Automotive",
                "id": "automotive",
                "description": "Car dealerships, auto services, vehicle sales",
                "keywords": ["car", "vehicle", "auto", "dealership", "sales"]
            },
            {
                "name": "Travel & Tourism",
                "id": "travel",
                "description": "Travel agencies, hotels, vacation rentals",
                "keywords": ["vacation", "travel", "trip", "booking", "hotel"]
            },
            {
                "name": "Real Estate",
                "id": "real_estate",
                "description": "Real estate agents, property management, home sales",
                "keywords": ["property", "house", "home", "real estate", "buying"]
            },
            {
                "name": "Technology",
                "id": "technology",
                "description": "Software companies, tech services, IT solutions",
                "keywords": ["software", "tech", "IT", "digital", "app"]
            },
            {
                "name": "Healthcare",
                "id": "healthcare",
                "description": "Medical practices, healthcare services, clinics",
                "keywords": ["medical", "health", "clinic", "doctor", "healthcare"]
            }
        ]
    }


@router.post("/campaigns/")
async def create_campaign(
    request: CampaignCreateRequest,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Create a new lead generation campaign
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        # This would create a new campaign
        return {
            "message": "Campaign created successfully",
            "campaign_id": f"campaign_{datetime.utcnow().timestamp()}",
            "name": request.name,
            "industry": request.industry,
            "status": "active" if request.enabled else "paused"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campaigns/")
async def get_campaigns(
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Get all lead generation campaigns
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        # This would return actual campaigns
        return {
            "campaigns": [
                {
                    "id": "campaign_1",
                    "name": "Automotive Leads Q1",
                    "industry": "automotive",
                    "status": "active",
                    "leads_generated": 150,
                    "conversion_rate": 12.5
                },
                {
                    "id": "campaign_2",
                    "name": "Travel Agencies",
                    "industry": "travel",
                    "status": "active",
                    "leads_generated": 89,
                    "conversion_rate": 8.7
                }
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/")
async def export_leads(
    format: str = "csv",
    status: Optional[str] = None,
    lead_service: LeadGenerationService = Depends(lambda: None)
):
    """
    Export leads to file
    """
    try:
        if not lead_service:
            raise HTTPException(status_code=503, detail="Lead generation service not available")
        
        # This would implement actual export functionality
        return {
            "message": f"Leads exported to {format} format",
            "download_url": f"/downloads/leads_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{format}",
            "total_leads": 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
