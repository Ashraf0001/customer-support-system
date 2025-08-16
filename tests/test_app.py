import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.prompt_loader import PromptManager
from app.workflows.customer_support_workflow import CustomerSupportWorkflow
from app.schemas.customer_support_schema import SupportTicketSchema


client = TestClient(app)


def test_health_endpoints():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.text == "ok"

    r = client.get("/readyz")
    assert r.status_code == 200
    assert r.text == "ready"


def test_prompt_loading():
    s = PromptManager.get_prompt(
        "ticket_analysis",
        ticket=SupportTicketSchema(
            id="t1",
            customer_email="u@example.com",
            subject="Login",
            content="Cannot login",
            priority="high",
        ),
    )
    assert "Ticket Information" in s


@patch("requests.post")
def test_workflow_end_to_end_with_mocked_ollama(mock_post):
    # Prepare two different mocked responses: one for analysis, one for response generation
    analysis_payload = {
        "response": json.dumps(
            {
                "category": "technical",
                "sentiment": "negative",
                "urgency": "high",
                "confidence": 0.9,
                "reasoning": "Password issue",
            }
        )
    }
    response_payload = {
        "response": json.dumps(
            {
                "response_text": "We can help.",
                "response_type": "automated",
                "suggested_actions": ["Try again"],
                "confidence": 0.95,
            }
        )
    }

    mock_post.return_value.status_code = 200
    payloads = [analysis_payload, response_payload]

    def json_side_effect():
        return payloads.pop(0)

    mock_post.return_value.json.side_effect = json_side_effect

    wf = CustomerSupportWorkflow()
    ticket = SupportTicketSchema(
        id="t2",
        customer_email="u2@example.com",
        subject="Reset",
        content="Reset link not working",
        priority="medium",
    )
    result = wf.run(ticket)

    # Analyze node completed
    a = result.nodes.get("AnalyzeTicketNode", {})
    assert a.get("status") == "completed"
    assert a.get("classification", {}).get("category") == "technical"

    # Classify node completed
    c = result.nodes.get("ClassifyTicketNode", {})
    assert c.get("status") == "completed"

    # Generate response node completed
    r = result.nodes.get("GenerateResponseNode", {})
    assert r.get("status") == "completed"
    assert r.get("response").response_type in {"automated", "escalation", "follow_up"}





