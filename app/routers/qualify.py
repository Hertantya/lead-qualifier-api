from fastapi import APIRouter

from app.llm import qualify_lead, qualify_lead_with_tools
from app.models import QualifyRequest, QualifyResponse, ToolQualifyResponse

router = APIRouter(tags=["qualify"])


@router.post("/qualify-lead", response_model=QualifyResponse)
def qualify_lead_endpoint(req: QualifyRequest) -> QualifyResponse:
    return qualify_lead(req)


@router.post("/qualify-lead/with-tools", response_model=ToolQualifyResponse)
def qualify_lead_with_tools_endpoint(req: QualifyRequest) -> ToolQualifyResponse:
    return qualify_lead_with_tools(req)
