from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1-cxw7XD6sfZfvRJpRyIX9R2kWNCyvr6FfbKKjc0mVOU"
CREDENTIALS_FILE = Path(__file__).parent.parent / "configs" / "google_sheet_cred.json"

_client = None


def get_client() -> gspread.Client:
    global _client
    if _client is None:
        creds = Credentials.from_service_account_file(
            str(CREDENTIALS_FILE),
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        _client = gspread.authorize(creds)
    return _client


def get_worksheet(sheet_name: str) -> gspread.Worksheet:
    return get_client().open_by_key(SPREADSHEET_ID).worksheet(sheet_name)
