from fastapi.testclient import TestClient

from app.main import app
from app.models import AskResponse, Citation

client = TestClient(app)


def test_ask_endpoint(monkeypatch):
    def fake_ask(question, top_k=4):
        return AskResponse(
            answer="Refunds are allowed within 30 days.",
            citations=[Citation(source="refund_policy.md", chunk_index=0, text="30 day refund window.")],
        )

    monkeypatch.setattr("app.routers.ask.rag_ask", fake_ask)

    response = client.post("/ask", json={"question": "Can I get a refund?"})

    assert response.status_code == 200
    body = response.json()
    assert "30 days" in body["answer"]
    assert body["citations"][0]["source"] == "refund_policy.md"


def test_ask_rejects_empty_question():
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422
