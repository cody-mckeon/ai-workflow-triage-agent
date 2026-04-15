import json
import os
import sys
from textwrap import dedent

from openai import OpenAI
from pydantic import BaseModel, Field


class TriageResult(BaseModel):
    category: str = Field(description="Best-fit request category")
    priority: str = Field(description="One of: low, medium, high, urgent")
    recommended_owner: str = Field(description="Team or role that should own the next step")
    next_action: str = Field(description="Single best next step")
    suggested_response: str = Field(description="Short professional response back to requester")
    reasoning: str = Field(description="Very short explanation of why this classification was chosen")


SYSTEM_PROMPT = dedent("""
You are an AI workflow triage assistant for incoming business requests.

Your job is to read a messy request and convert it into a clean triage decision.
Return structured output only.

Rules:
- Choose a practical category that fits the request.
- Priority must be exactly one of: low, medium, high, urgent.
- Recommended owner should be a realistic team or role.
- Next action should be one concrete action, not a long plan.
- Suggested response should be concise and professional.
- Reasoning should be brief, plain English, and under 30 words.

Suggested categories you may use when relevant:
- marketing_web_update
- analytics_tracking
- design_request
- bug_fix
- api_integration
- content_update
- stakeholder_question
- ai_automation_request
- general_operations
""").strip()


EXAMPLE_REQUEST = (
    "We need to update the homepage banner for Mother's Day and also track clicks on the CTA. "
    "Marketing wants it live by Friday."
)


def triage_request(user_request: str, model: str = "gpt-4o-2024-08-06") -> TriageResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)

    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request},
        ],
        text_format=TriageResult,
    )

    return response.output_parsed


def main() -> None:
    if len(sys.argv) > 1:
        request_text = " ".join(sys.argv[1:]).strip()
    else:
        request_text = EXAMPLE_REQUEST

    try:
        result = triage_request(request_text)
        print(json.dumps(result.model_dump(), indent=2))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
