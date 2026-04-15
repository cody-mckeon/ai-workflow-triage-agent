# AI Workflow Triage Agent

A minimal Python script that takes a messy business request and returns structured triage output:
- category
- priority
- recommended owner
- next action
- suggested response
- reasoning

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key_here"
```

## Run

Use the built-in example:

```bash
python ai_workflow_triage_agent.py
```

Pass your own request:

```bash
python ai_workflow_triage_agent.py "We need to add a new landing page section and track clicks on the CTA by Monday."
```

## Why this is a good first build

It is small, fast, and clearly demonstrates:
- structured prompting
- AI as workflow infrastructure
- product/ops thinking instead of chatbot hype

## Next version ideas

- Send output to Slack
- Create an Asana task
- Log triage results in Google Sheets
- Add a tiny Streamlit UI
