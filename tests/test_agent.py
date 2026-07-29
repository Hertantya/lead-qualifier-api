from fastapi.testclient import TestClient

from app.main import app
from app.models import ResearchLeadResponse

client = TestClient(app)


def test_research_lead_endpoint(monkeypatch):
    def fake_research_lead(company_name):
        return ResearchLeadResponse(
            company_name=company_name,
            summary="Acme Corp is a 250-person logistics company expanding in Texas.",
            draft_email="Hi Acme team, congrats on the new distribution hub...",
            tool_calls=["search_company_info"],
        )

    monkeypatch.setattr("app.routers.agent.research_lead", fake_research_lead)

    response = client.post("/research-lead", json={"company_name": "Acme Corp"})

    assert response.status_code == 200
    body = response.json()
    assert body["company_name"] == "Acme Corp"
    assert "search_company_info" in body["tool_calls"]


def test_research_lead_rejects_empty_company_name():
    response = client.post("/research-lead", json={"company_name": ""})
    assert response.status_code == 422
