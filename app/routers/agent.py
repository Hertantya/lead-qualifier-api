from fastapi import APIRouter

from app.agent.loop import research_lead
from app.models import ResearchLeadRequest, ResearchLeadResponse

router = APIRouter(tags=["agent"])


@router.post("/research-lead", response_model=ResearchLeadResponse)
def research_lead_endpoint(req: ResearchLeadRequest) -> ResearchLeadResponse:
    return research_lead(req.company_name)
