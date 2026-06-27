from datetime import date
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from mcp.server.fastmcp import FastMCP

SPREADSHEET_ID = "1-cxw7XD6sfZfvRJpRyIX9R2kWNCyvr6FfbKKjc0mVOU"
SHEET_NAME = "Schedule"
CREDENTIALS_FILE = Path(__file__).parent.parent / "configs" / "google_sheet_cred.json"

mcp = FastMCP("schedule-assistant")


def get_worksheet():
    creds = Credentials.from_service_account_file(
        str(CREDENTIALS_FILE),
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


@mcp.tool()
def log_task(task: str, due_date: str, status: str = "To-do") -> str:
    """Append a task to columns U, V, X of the Schedule sheet (skips W, which is a formula).

    Args:
        task: Description of the task.
        due_date: Date in DD-MM-YYYY format. Resolve relative dates like 'tomorrow' or
                  'next tuesday' before calling. Always ask the user if not provided.
        status: Task status. Defaults to 'To-do'. Options: To-do, Doing, Done, Drop.
    """
    ws = get_worksheet()

    # Find first empty row in column U (col 21)
    col_u = ws.col_values(21)
    next_row = len(col_u) + 1

    # Write U+V together, then X separately to skip W (formula column)
    ws.update(f"U{next_row}:V{next_row}", [[due_date, task]])
    ws.update(f"X{next_row}", [[status]])

    return f"Scheduled: {due_date} | {task} | {status} (row {next_row})"


if __name__ == "__main__":
    mcp.run()
