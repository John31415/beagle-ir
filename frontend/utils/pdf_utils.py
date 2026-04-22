import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

@st.cache_data(show_spinner = False)
def read_pdf_bytes(file_path: str) -> bytes:
    """Read a PDF file and return its contents as a bytes object.
    """

    return Path(file_path).read_bytes()

@st.cache_data(show_spinner = False)
def encode_pdf_as_base64(file_path: str) -> str:
    """Encode a PDF file as a Base64 string.
    """

    return base64.b64encode(read_pdf_bytes(file_path)).decode("utf-8")

def resolve_document_path(project_root: Path, document_path: str) -> Path:
    """Resolve a document path relative to a project root.
    """

    candidate = Path(document_path)
    if candidate.is_absolute():
        return candidate
    return project_root / candidate

def get_document_name(document_path: str | Path) -> str:
    """Extract the filename from a document path.
    """

    return Path(document_path).name

def get_download_payload(file_path: str | Path) -> bytes | None:
    """Retrieve the raw bytes payload of a file for download.
    """

    resolved_path = Path(file_path)
    if not resolved_path.exists():
        return None
    return read_pdf_bytes(str(resolved_path))

def display_cropped_pdf(file_path: str | Path, height = 430) -> None:
    """Display a cropped PDF preview in Streamlit. Renders a PDF inside a fixed-height container.
    """

    resolved_path = Path(file_path)
    if not resolved_path.exists():
        st.warning("Preview unavailable because the file could not be found.")
        return
    base64_pdf = encode_pdf_as_base64(str(resolved_path))
    pdf_url = (
        f"data:application/pdf;base64,{base64_pdf}"
        "#page=1&toolbar=0&navpanes=0&scrollbar=0"
    )
    pdf_display = f"""
    <div style="
        width: 100%;
        height: {height}px;
        overflow: hidden;
        border: 1px solid rgba(17, 18, 23, 0.10);
        border-radius: 20px;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(246, 246, 249, 0.88));
        box-shadow: 0 18px 36px rgba(17, 18, 23, 0.08);
        margin: 0.2rem 0 1rem;
    ">
        <iframe
            src="{pdf_url}"
            style="
                width: 100%;
                height: 960px;
                margin-top: 0;
                border: none;
            ">
        </iframe>
    </div>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)