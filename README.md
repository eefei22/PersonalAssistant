# Personal Assistant

An AI-powered personal assistant that manages expenses and tasks via natural language, backed by Google Sheets.

## Use Cases

- **Track expenses** — log purchases with natural language (e.g. "I spent RM 12 on lunch today"), then ask for summaries ("show me my expenses this month").
- **Manage tasks** — schedule to-dos with due dates ("add a task to renew passport by next Friday"), update statuses, and list upcoming deadlines.
- **Chat interface** — multi-turn conversation with memory per session, so the assistant remembers context.

## Architecture

```
api.py              FastAPI server (REST API)
agent/
├── agent.py        OpenAI tool-calling loop (gpt-5-nano)
├── tools.py        Tool definitions + execution (log_expense, log_task, read_expenses, read_tasks)
└── system_prompt.py
shared/
└── sheets.py       Google Sheets client (gspread)
mcp_servers/        Alternative MCP-based tool servers
configs/
├── config.env      API keys
└── google_sheet_cred.json
```

## Tech Stack

| | |
|---|---|
| Language | Python 3 |
| Web framework | FastAPI |
| AI | OpenAI (gpt-5-nano) with function calling |
| Data store | Google Sheets (via gspread) |
| Config | python-dotenv |

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv_pa
   .venv_pa\Scripts\activate
   pip install fastapi uvicorn openai gspread python-dotenv pydantic
   ```

2. Place your credentials in `configs/`:
   - `config.env` — `OPENAI_API_KEY` and `PA_API_KEY`
   - `google_sheet_cred.json` — Google service account key

3. Run the API server:
   ```bash
   uvicorn api:app --reload
   ```

4. Or run interactively in the terminal:
   ```bash
   python -m agent.agent
   ```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat` | Send a message, get an AI reply |
| `DELETE` | `/session/{id}` | Clear conversation history |
| `GET` | `/health` | Health check |

Auth: `X-API-Key` header.
