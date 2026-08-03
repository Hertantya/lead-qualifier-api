"""Thin wrapper around the OpenAI SDK: structured outputs + tool use (function calling)."""
import json

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionFunctionToolParam,
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionMessageParam,
)

from app import config
from app.models import QualifyRequest, QualifyResponse, ToolQualifyResponse

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """Lazily construct the OpenAI client so importing this module never requires a key."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=config.OPENAI_API_KEY, base_url=config.OPENAI_BASE_URL)
    return _client


QUALIFY_SYSTEM_PROMPT = (
    "You are a lead qualification assistant for a B2B SaaS company selling "
    "sales-automation software. Score how well the described company fits as "
    "a customer, from 1 (poor fit) to 10 (ideal fit), explain your reasoning "
    "in one or two sentences, and recommend a next action "
    "(e.g. 'schedule demo', 'nurture', 'disqualify')."
)


def qualify_lead(req: QualifyRequest) -> QualifyResponse:
    """Structured-output call: no tools, just a validated JSON answer."""
    client = get_client()
    completion = client.beta.chat.completions.parse(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": QUALIFY_SYSTEM_PROMPT},
            {"role": "user", "content": req.company_description},
        ],
        response_format=QualifyResponse,
    )
    result = completion.choices[0].message.parsed
    if result is None:
        raise ValueError("Model refused to produce structured output")
    return result


# --- Tool use / function calling ---

def _lookup_company_firmographics(company_name: str) -> dict:
    """Mocked stand-in for a real Apollo/Clay/HubSpot enrichment lookup."""
    fake_db = {
        "acme corp": {"employee_count": 250, "industry": "Logistics", "funding_stage": "Series B"},
        "globex": {"employee_count": 12, "industry": "Retail", "funding_stage": "Bootstrapped"},
    }
    return fake_db.get(
        company_name.strip().lower(),
        {"employee_count": None, "industry": "Unknown", "funding_stage": "Unknown"},
    )


TOOLS: list[ChatCompletionFunctionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "lookup_company_firmographics",
            "description": (
                "Look up a company's employee count, industry, and funding stage "
                "from CRM/enrichment data."
            ),
            "parameters": {
                "type": "object",
                "properties": {"company_name": {"type": "string"}},
                "required": ["company_name"],
            },
        },
    }
]

_AVAILABLE_TOOLS = {"lookup_company_firmographics": _lookup_company_firmographics}


def qualify_lead_with_tools(req: QualifyRequest, max_turns: int = 3) -> ToolQualifyResponse:
    """Same qualification task, but the model can call a tool to fetch facts first."""
    client = get_client()
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": QUALIFY_SYSTEM_PROMPT
            + " Use the lookup_company_firmographics tool to get facts before scoring.",
        },
        {"role": "user", "content": req.company_description},
    ]
    tools_used: list[str] = []

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
        )
        choice = response.choices[0]
        if not choice.message.tool_calls:
            break

        messages.append(choice.message.model_dump(exclude_unset=True))  # type: ignore[arg-type]
        for call in choice.message.tool_calls:
            if not isinstance(call, ChatCompletionMessageFunctionToolCall):
                continue
            fn = _AVAILABLE_TOOLS[call.function.name]
            args = json.loads(call.function.arguments)
            result = fn(**args)
            tools_used.append(call.function.name)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)}
            )

    completion = client.beta.chat.completions.parse(
        model=config.OPENAI_MODEL,
        messages=messages + [{"role": "user", "content": "Now give your final structured qualification."}],
        response_format=QualifyResponse,
    )
    result = completion.choices[0].message.parsed
    if result is None:
        raise ValueError("Model refused to produce structured output")
    return ToolQualifyResponse(**result.model_dump(), tools_used=tools_used)
