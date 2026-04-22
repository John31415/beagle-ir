from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(FRONTEND_ROOT) not in sys.path:
    sys.path.insert(0, str(FRONTEND_ROOT))

import streamlit as st

from theme import apply_theme
from views import (
    initialize_state,
    render_chat_page,
    render_home_page,
    render_search_page,
    render_top_navigation,
)


def main() -> None:
    st.set_page_config(
        page_title="Beagle IR",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    apply_theme()
    initialize_state()
    render_top_navigation()

    current_page = st.session_state.page
    if current_page == "search":
        render_search_page(PROJECT_ROOT)
    elif current_page == "chat":
        render_chat_page()
    else:
        render_home_page(PROJECT_ROOT)


if __name__ == "__main__":
    main()
