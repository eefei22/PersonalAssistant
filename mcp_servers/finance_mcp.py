import json
from datetime import date
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from mcp.server.fastmcp import FastMCP

SPREADSHEET_ID = "1-cxw7XD6sfZfvRJpRyIX9R2kWNCyvr6FfbKKjc0mVOU"
SHEET_NAME = "Finances"
CREDENTIALS_FILE = Path(__file__).parent.parent / "configs" / "google_sheet_cred.json"

mcp = FastMCP("personal-assistant")


def get_worksheet():
    creds = Credentials.from_service_account_file(
        str(CREDENTIALS_FILE),
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


@mcp.tool()
def log_expense(item: str, amount: float, expense_date: str = "") -> str:
    """Append an expense row to columns J, K, L of the Trackers spreadsheet.

    Args:
        item: What was purchased.
        amount: How much was spent. Always ask the user if not provided.
        expense_date: Date in DD-MM-YYYY format. Always ask user if not provided.
                      Resolve relative dates like 'yesterday' or '4 days ago' before calling.
    """
    if expense_date:
        row_date = expense_date
    else:
        row_date = date.today().strftime("%d-%m-%Y")

    ws = get_worksheet()
    col_j = ws.col_values(10)
    next_row = len(col_j) + 1

    ws.update(f"J{next_row}:L{next_row}", [[row_date, item, amount]])
    return f"Logged: {row_date} | {item} | {amount} (row {next_row})"


if __name__ == "__main__":
    mcp.run()
