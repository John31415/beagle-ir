from datetime import datetime
from html import escape
from pathlib import Path
import streamlit as st
from backend_controller.backend_controller import get_recommendations, rag_controller, retrieval_controller
from frontend.utils.pdf_utils import display_cropped_pdf, get_document_name, get_download_payload, resolve_document_path
from theme import render_empty_state, render_hero_panel, render_query_summary, render_section_intro

def initialize_state() -> None:
    defaults = {
        "page": "home",
        "retrieval_results": [],
        "retrieval_last_query": "",
        "retrieval_has_run": False,
        "retrieval_error": "",
        "recommendation_results": [],
        "recommendations_loaded": False,
        "recommendations_dirty": True,
        "recommendations_error": "",
        "chat_messages": [
            _build_message(
                "assistant",
                "Ask about the corpus and I will answer with the RAG module.",
            )
        ],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_top_navigation() -> None:
    title_col, home_col, search_col, chat_col = st.columns([4.2, 1.1, 1.1, 1.1])
    with title_col:
        st.markdown(
            """
            <div class="nav-shell">
                <div class="nav-caption">Calm information retrieval workspace</div>
                <div class="nav-title">Beagle IR</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with home_col:
        if st.button(
            "Home",
            key="nav_home",
            type="primary" if st.session_state.page == "home" else "secondary",
            use_container_width=True,
        ):
            _navigate("home")
    with search_col:
        if st.button(
            "Search",
            key="nav_search",
            type="primary" if st.session_state.page == "search" else "secondary",
            use_container_width=True,
        ):
            _navigate("search")
    with chat_col:
        if st.button(
            "RAG Chat",
            key="nav_chat",
            type="primary" if st.session_state.page == "chat" else "secondary",
            use_container_width=True,
        ):
            _navigate("chat")

def render_home_page(project_root: Path) -> None:
    render_hero_panel(
        badge="Recommendation Module",
        title="Explore the corpus from one focused workspace",
        subtitle=(
            "Start on the home page, surface recommendations, then jump into "
            "search or RAG chat whenever you want to investigate further."
        ),
        metrics=[
            ("Home focus", "Recommendations"),
            ("Retrieval view", "Google-style search"),
            ("RAG view", "Conversation flow"),
        ],
    )
    action_col_left, action_col_right = st.columns(2)
    with action_col_left:
        if st.button(
            "Open Search Interface",
            key="home_open_search",
            type="primary",
            use_container_width=True,
        ):
            _navigate("search")
    with action_col_right:
        if st.button(
            "Open RAG Chat",
            key="home_open_chat",
            use_container_width=True,
        ):
            _navigate("chat")
    header_col, refresh_col = st.columns([4.5, 1.2])
    with header_col:
        render_section_intro(
            eyebrow="Recommended PDFs",
            title="Documents that may interest you",
            description=(
                "This module updates from the interaction history. Each document "
                "can be previewed on demand or downloaded directly."
            ),
        )
    with refresh_col:
        refresh_requested = st.button(
            "Refresh",
            key="refresh_recommendations",
            use_container_width=True,
        )
    _load_recommendations(force=refresh_requested)
    if st.session_state.recommendations_error:
        st.error(st.session_state.recommendations_error)
    if st.session_state.recommendation_results:
        render_document_list(
            st.session_state.recommendation_results,
            section_key="recommendations",
            project_root=project_root,
        )
    elif not st.session_state.recommendations_error:
        render_empty_state(
            "Recommendations will appear here",
            "Search or ask questions first so the system can build history and propose relevant PDFs.",
        )

def render_search_page(project_root: Path) -> None:
    render_hero_panel(
        badge="Retrieval Module",
        title="Search the corpus with a focused retrieval flow",
        subtitle=(
            "Submit a query, wait for ranked PDF matches, and inspect only the "
            "documents you want with manual previews and direct downloads."
        ),
        metrics=[
            ("Interaction", "Search and browse"),
            ("Result type", "Ranked PDF list"),
            ("Preview mode", "On demand"),
        ],
    )
    render_section_intro(
        eyebrow="Search Interface",
        title="Find relevant documents",
        description=(
            "Type a query in the search bar below. The ranked results appear as "
            "a clean list with preview and download actions beside each PDF."
        ),
    )
    with st.form("retrieval_form", clear_on_submit=False):
        input_col, submit_col = st.columns([5.4, 1.2])
        with input_col:
            query = st.text_input(
                "Search the corpus",
                placeholder="Search papers, methods, tasks, benchmarks, or keywords...",
                label_visibility="collapsed",
                key="retrieval_query_input",
            )
        with submit_col:
            search_requested = st.form_submit_button(
                "Search",
                type="primary",
                use_container_width=True,
            )
    if search_requested:
        cleaned_query = query.strip()
        if not cleaned_query:
            st.session_state.retrieval_error = "Please type a query before searching."
        else:
            _reset_preview_state("search")
            with st.spinner("Searching the corpus..."):
                try:
                    documents = _unique_documents(retrieval_controller(cleaned_query))
                    st.session_state.retrieval_results = documents
                    st.session_state.retrieval_last_query = cleaned_query
                    st.session_state.retrieval_has_run = True
                    st.session_state.retrieval_error = ""
                    st.session_state.recommendations_dirty = True
                except Exception as exc:
                    st.session_state.retrieval_results = []
                    st.session_state.retrieval_last_query = cleaned_query
                    st.session_state.retrieval_has_run = True
                    st.session_state.retrieval_error = f"Search failed: {exc}"
    if st.session_state.retrieval_error:
        st.error(st.session_state.retrieval_error)
    if st.session_state.retrieval_has_run and st.session_state.retrieval_last_query:
        render_query_summary(
            st.session_state.retrieval_last_query,
            len(st.session_state.retrieval_results),
            "documents returned",
        )
    if st.session_state.retrieval_results:
        render_document_list(
            st.session_state.retrieval_results,
            section_key="search",
            project_root=project_root,
        )
    elif st.session_state.retrieval_has_run and not st.session_state.retrieval_error:
        render_empty_state(
            "No documents matched this query",
            "Try broader keywords, a different phrasing, or a shorter query.",
        )
    elif not st.session_state.retrieval_has_run:
        render_empty_state(
            "Your search results will appear here",
            "Run a query to get ranked PDF matches from the retrieval controller.",
        )

def render_chat_page() -> None:
    render_hero_panel(
        badge="RAG Module",
        title="Chat with the corpus in a messenger-style layout",
        subtitle=(
            "Your questions appear on the right, the grounded answer appears on "
            "the left, and the conversation stays available throughout the session."
        ),
        metrics=[
            ("Interaction", "Ongoing conversation"),
            ("Answering mode", "Grounded generation"),
            ("Session memory", "Streamlit state"),
        ],
    )
    info_col, action_col = st.columns([4.5, 1.2])
    with info_col:
        st.markdown(
            """
            <div class="helper-note">
                Ask about the corpus, a topic, or a document. The RAG module will answer in chat form.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col:
        if st.button("Clear chat", key="clear_chat_history", use_container_width=True):
            st.session_state.chat_messages = [
                _build_message(
                    "assistant",
                    "The chat has been cleared. Ask about the corpus whenever you are ready.",
                )
            ]
            st.rerun()
    for message in st.session_state.chat_messages:
        _render_chat_message(message)
    prompt = st.chat_input("Ask about the corpus, a topic, or a document...")
    if not prompt:
        return
    cleaned_prompt = prompt.strip()
    if not cleaned_prompt:
        return
    st.session_state.chat_messages.append(_build_message("user", cleaned_prompt))
    with st.spinner("Generating a grounded answer..."):
        try:
            answer = rag_controller(cleaned_prompt).strip()
            if not answer:
                answer = "The RAG module did not return an answer for that question."
        except Exception as exc:
            answer = f"The RAG module failed to answer this query: {exc}"
    st.session_state.chat_messages.append(_build_message("assistant", answer))
    st.session_state.recommendations_dirty = True
    st.rerun()

def render_document_list(
    documents: list[str],
    section_key: str,
    project_root: Path,
) -> None:
    for index, document_path in enumerate(_unique_documents(documents), start=1):
        resolved_path = resolve_document_path(project_root, document_path)
        preview_key = _preview_key(section_key, document_path)
        is_preview_open = st.session_state.get(preview_key, False)
        if resolved_path.exists():
            doc_name = get_document_name(resolved_path)
            doc_pill = f"PDF | {_format_file_size(resolved_path)}"
        else:
            doc_name = get_document_name(document_path)
            doc_pill = "Missing file"
        st.markdown(
            f"""
            <div class="doc-card">
                <div class="doc-header">
                    <div class="doc-header-left">
                        <div class="doc-index">{index}</div>
                        <div>
                            <div class="doc-name">{escape(doc_name)}</div>
                            <div class="doc-path">{escape(document_path)}</div>
                        </div>
                    </div>
                    <div class="doc-pill">{escape(doc_pill)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        size_in_mb = resolved_path.stat().st_size / (1024 * 1024)
        preview_col, download_col, spacer_col = st.columns([1.15, 1.15, 3.7])
        with preview_col:
            if size_in_mb < 1.5:
                if st.button(
                    "Hide preview" if is_preview_open else "Preview",
                    key=f"preview_toggle::{section_key}::{index}",
                    use_container_width=True,
                ):
                    st.session_state[preview_key] = not is_preview_open
                    st.rerun()
            else:
                st.button("No Preview", disabled=True, key=f"preview_disabled::{section_key}::{index}", use_container_width=True)
        with download_col:
            download_payload = get_download_payload(resolved_path)
            if download_payload is None:
                st.button(
                    "Download",
                    key=f"download_disabled::{section_key}::{index}",
                    disabled=True,
                    use_container_width=True,
                )
            else:
                st.download_button(
                    "Download",
                    data=download_payload,
                    file_name=doc_name,
                    mime="application/pdf",
                    key=f"download::{section_key}::{index}",
                    use_container_width=True,
                )
        with spacer_col:
            if resolved_path.exists():
                st.caption(f"Stored at: {resolved_path.relative_to(project_root)}")
            else:
                st.caption("This file path is not currently available on disk.")
        if st.session_state.get(preview_key, False):
            display_cropped_pdf(resolved_path)

def _build_message(role: str, content: str) -> dict[str, str]:
    return {
        "role": role,
        "content": content.strip(),
        "timestamp": datetime.now().strftime("%H:%M"),
    }

def _render_chat_message(message: dict[str, str]) -> None:
    role = "user" if message.get("role") == "user" else "assistant"
    speaker = "You" if role == "user" else "Beagle"
    timestamp = message.get("timestamp", "")
    content = escape(message.get("content", "")).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="message-row {role}">
            <div class="message-bubble">
                <div class="message-meta">{escape(speaker)} | {escape(timestamp)}</div>
                <div>{content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _navigate(page: str) -> None:
    if st.session_state.page != page:
        st.session_state.page = page
        st.rerun()

def _load_recommendations(force: bool = False) -> None:
    if (
        not force
        and st.session_state.recommendations_loaded
        and not st.session_state.recommendations_dirty
    ):
        return
    _reset_preview_state("recommendations")
    with st.spinner("Loading recommendations..."):
        try:
            documents = _unique_documents(get_recommendations())
            st.session_state.recommendation_results = documents
            st.session_state.recommendations_error = ""
        except Exception as exc:
            st.session_state.recommendation_results = []
            st.session_state.recommendations_error = (
                f"Recommendations failed to load: {exc}"
            )
    st.session_state.recommendations_loaded = True
    st.session_state.recommendations_dirty = False

def _preview_key(section_key: str, document_path: str) -> str:
    return f"preview::{section_key}::{document_path}"

def _reset_preview_state(section_key: str) -> None:
    prefix = f"preview::{section_key}::"
    for key in list(st.session_state.keys()):
        if key.startswith(prefix):
            del st.session_state[key]

def _unique_documents(documents: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_documents = []
    for document in documents:
        if document not in seen:
            seen.add(document)
            unique_documents.append(document)
    return unique_documents

def _format_file_size(file_path: Path) -> str:
    size_in_mb = file_path.stat().st_size / (1024 * 1024)
    return f"{size_in_mb:.2f} MB"