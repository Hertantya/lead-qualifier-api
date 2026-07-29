"""Pydantic schemas: the request/response contract for every endpoint."""
from pydantic import BaseModel, Field


class QualifyRequest(BaseModel):
    company_description: str = Field(min_length=1, description="Free-text description of the lead/company")


class QualifyResponse(BaseModel):
    score: int = Field(ge=1, le=10, description="Lead quality score, 1 (poor fit) to 10 (ideal fit)")
    reasoning: str
    recommended_action: str


class ToolQualifyResponse(QualifyResponse):
    tools_used: list[str] = Field(default_factory=list, description="Names of tools the model invoked before answering")


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=10)


class Citation(BaseModel):
    source: str
    chunk_index: int
    text: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]


class ResearchLeadRequest(BaseModel):
    company_name: str = Field(min_length=1)


class ResearchLeadResponse(BaseModel):
    company_name: str
    summary: str
    draft_email: str
    tool_calls: list[str] = Field(default_factory=list)
