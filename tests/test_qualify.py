from fastapi.testclient import TestClient

from app.main import app
from app.models import QualifyResponse, ToolQualifyResponse

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_qualify_lead(monkeypatch):
    def fake_qualify_lead(req):
        return QualifyResponse(score=8, reasoning="Good fit.", recommended_action="schedule demo")

    monkeypatch.setattr("app.routers.qualify.qualify_lead", fake_qualify_lead)

    response = client.post("/qualify-lead", json={"company_description": "A 250-person logistics company."})

    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 8
    assert body["recommended_action"] == "schedule demo"


def test_qualify_lead_with_tools(monkeypatch):
    def fake_qualify_with_tools(req):
        return ToolQualifyResponse(
            score=6,
            reasoning="Mid-size fit.",
            recommended_action="nurture",
            tools_used=["lookup_company_firmographics"],
        )

    monkeypatch.setattr("app.routers.qualify.qualify_lead_with_tools", fake_qualify_with_tools)

    response = client.post("/qualify-lead/with-tools", json={"company_description": "Acme Corp, logistics."})

    assert response.status_code == 200
    assert response.json()["tools_used"] == ["lookup_company_firmographics"]


def test_qualify_lead_rejects_empty_description():
    response = client.post("/qualify-lead", json={"company_description": ""})
    assert response.status_code == 422
