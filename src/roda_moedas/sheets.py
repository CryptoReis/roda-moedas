from __future__ import annotations

import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

from .calculations import SHEET_COLUMNS

WORKSHEET = "Folha1"


def is_dry_run() -> bool:
    """Return True when writes should stay in the Streamlit session only."""
    try:
        return bool(st.secrets.get("app", {}).get("dry_run", False))
    except Exception:
        return False


def ensure_columns(data: pd.DataFrame) -> pd.DataFrame:
    if data is None or data.empty:
        return pd.DataFrame(columns=SHEET_COLUMNS)

    data = data.copy()
    for column in SHEET_COLUMNS:
        if column not in data.columns:
            data[column] = None
    return data[SHEET_COLUMNS]


class SessionStore:
    """Small no-network store used for safe local/dry-run testing."""

    def read(self) -> pd.DataFrame:
        rows = st.session_state.setdefault("dry_run_rows", [])
        return ensure_columns(pd.DataFrame(rows))

    def append(self, row: dict[str, object]) -> None:
        rows = st.session_state.setdefault("dry_run_rows", [])
        rows.append(row)


class GoogleSheetsStore:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def read(self) -> pd.DataFrame:
        try:
            data = self.conn.read(worksheet=WORKSHEET, usecols=list(range(len(SHEET_COLUMNS))), ttl=1)
        except Exception:
            data = pd.DataFrame(columns=SHEET_COLUMNS)
        return ensure_columns(data)

    def append(self, row: dict[str, object]) -> None:
        existing_data = self.read()
        updated_data = pd.concat([existing_data, pd.DataFrame([row])], ignore_index=True)
        self.conn.update(worksheet=WORKSHEET, data=updated_data)


def get_store():
    if is_dry_run():
        return SessionStore(), "dry-run"
    try:
        return GoogleSheetsStore(), "google-sheets"
    except Exception as exc:
        st.warning(
            "Google Sheets is not configured in this environment, so this run is using "
            "session-only dry-run storage. No live data will be written."
        )
        st.caption(f"Connection detail: {exc}")
        return SessionStore(), "dry-run"
