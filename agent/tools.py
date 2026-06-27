import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.sheets import get_worksheet

# ---------------------------------------------------------------------------
# Tool schemas — OpenAI function-calling format
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "log_expense",
            "description": "Append an expense row to the Finances sheet (columns J=Date, K=Item, L=Amount).",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {"type": "string", "description": "What was purchased."},
                    "amount": {"type": "number", "description": "Amount spent in RM."},
                    "expense_date": {
                        "type": "string",
                        "description": "Date in DD-MM-YYYY format. Resolve relative dates before calling.",
                    },
                },
                "required": ["item", "amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "log_task",
            "description": "Append a task to the Schedule sheet (columns U=Due Date, V=Task, X=Status).",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "Description of the task."},
                    "due_date": {
                        "type": "string",
                        "description": "Due date in DD-MM-YYYY format. Resolve relative dates before calling.",
                    },
                    "status": {
                        "type": "string",
                        "description": "Task status. Defaults to 'To-do'.",
                        "enum": ["To-do", "Doing", "Done", "Drop"],
                    },
                },
                "required": ["task", "due_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_expenses",
            "description": "Read all expense rows from the Finances sheet. Use this to answer questions like 'show me my expenses' or 'how much did I spend this month'.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_tasks",
            "description": "Read all task rows from the Schedule sheet. Use this to answer questions about upcoming tasks, deadlines, or to-dos.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]


# ---------------------------------------------------------------------------
# Tool execution functions
# ---------------------------------------------------------------------------

def log_expense(item: str, amount: float, expense_date: str = "") -> str:
    row_date = expense_date or date.today().strftime("%d-%m-%Y")
    ws = get_worksheet("Finances")
    col_j = ws.col_values(10)
    next_row = len(col_j) + 1
    ws.update(f"J{next_row}:L{next_row}", [[row_date, item, amount]])
    return f"Logged: {row_date} | {item} | RM {amount}"


def log_task(task: str, due_date: str, status: str = "To-do") -> str:
    ws = get_worksheet("Schedule")
    col_u = ws.col_values(21)
    next_row = len(col_u) + 1
    ws.update(f"U{next_row}:V{next_row}", [[due_date, task]])
    ws.update(f"X{next_row}", [[status]])
    return f"Scheduled: {due_date} | {task} | {status}"


def read_expenses() -> str:
    ws = get_worksheet("Finances")
    dates = ws.col_values(10)   # J
    items = ws.col_values(11)   # K
    amounts = ws.col_values(12) # L

    rows = []
    max_len = max(len(dates), len(items), len(amounts))
    for i in range(max_len):
        d = dates[i] if i < len(dates) else ""
        it = items[i] if i < len(items) else ""
        am = amounts[i] if i < len(amounts) else ""
        if it or am:
            rows.append({"date": d, "item": it, "amount": am})

    if not rows:
        return "No expenses found."
    return str(rows)


def read_tasks() -> str:
    ws = get_worksheet("Schedule")
    due_dates = ws.col_values(21)  # U
    tasks = ws.col_values(22)      # V
    statuses = ws.col_values(24)   # X

    rows = []
    max_len = max(len(due_dates), len(tasks), len(statuses))
    for i in range(max_len):
        d = due_dates[i] if i < len(due_dates) else ""
        t = tasks[i] if i < len(tasks) else ""
        s = statuses[i] if i < len(statuses) else ""
        if t:
            rows.append({"due_date": d, "task": t, "status": s})

    if not rows:
        return "No tasks found."
    return str(rows)


# ---------------------------------------------------------------------------
# Dispatcher — called by the agent loop
# ---------------------------------------------------------------------------

def execute_tool(name: str, inputs: dict) -> str:
    if name == "log_expense":
        return log_expense(**inputs)
    elif name == "log_task":
        return log_task(**inputs)
    elif name == "read_expenses":
        return read_expenses()
    elif name == "read_tasks":
        return read_tasks()
    else:
        return f"Unknown tool: {name}"
