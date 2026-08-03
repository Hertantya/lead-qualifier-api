"""A hand-rolled agent loop: LLM + tools + while loop, no LangGraph/CrewAI.

This is the pattern every agent framework wraps: the model decides which tool
to call and with what arguments, our code executes it and feeds the result
back, and we repeat until the model is ready to give a final answer.
"""
import json

from openai.types.chat import (
    ChatCompletionFunctionToolParam,
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionMessageParam,
)
from pydantic import BaseModel

from app import config
from app.llm import get_client
from app.models import ResearchLeadResponse

AGENT_SYSTEM_PROMPT = (
    "You are a sales-research agent. Given a company name, use the "
    "search_company_info tool to gather facts, then write a two-sentence "
    "summary and a short, personalized outreach email draft. "
    "Call the tool at most once per company."
)


def _search_company_info(company_name: str) -> dict:
    """Mocked stand-in for a real web search / Apollo / Clay lookup."""
    fake_db = {
        "acme corp": {
            "industry": "Logistics",
            "employee_count": 250,
            "recent_news": "Opened a new distribution hub in Texas.",
        },
        "globex": {
            "industry": "Retail",
            "employee_count": 12,
            "recent_news": "Launched a direct-to-consumer online store.",
        },
    }
    return fake_db.get(
        company_name.strip().lower(),
        {"industry": "Unknown", "employee_count": None, "recent_news": "No public information found."},
    )


AGENT_TOOLS: list[ChatCompletionFunctionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "search_company_info",
            "description": "Search the web/CRM for a company's industry, size, and recent news.",
            "parameters": {
                "type": "object",
                "properties": {"company_name": {"type": "string"}},
                "required": ["company_name"],
            },
        },
    }
]

_AVAILABLE_TOOLS = {"search_company_info": _search_company_info}


class _AgentFinalAnswer(BaseModel):
    summary: str
    draft_email: str


def research_lead(company_name: str, max_turns: int = 4) -> ResearchLeadResponse:
    client = get_client()
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": f"Research this company and draft outreach: {company_name}"},
    ]
    tool_calls_made: list[str] = []

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            tools=AGENT_TOOLS,
        )
        choice = response.choices[0]
        if not choice.message.tool_calls:
            break  # model is done gathering facts, ready for a final answer

        messages.append(choice.message.model_dump(exclude_unset=True))  # type: ignore[arg-type]
        for call in choice.message.tool_calls:
            if not isinstance(call, ChatCompletionMessageFunctionToolCall):
                continue
            fn = _AVAILABLE_TOOLS[call.function.name]
            args = json.loads(call.function.arguments)
            result = fn(**args)
            tool_calls_made.append(call.function.name)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)}
            )

    completion = client.beta.chat.completions.parse(
        model=config.OPENAI_MODEL,
        messages=messages + [{"role": "user", "content": "Give your final summary and email draft now."}],
        response_format=_AgentFinalAnswer,
    )
    parsed = completion.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Model refused to produce structured output")

    return ResearchLeadResponse(
        company_name=company_name,
        summary=parsed.summary,
        draft_email=parsed.draft_email,
        tool_calls=tool_calls_made,
    )
