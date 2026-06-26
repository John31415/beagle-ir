from html import escape
import streamlit as st

THEME_CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap");

:root {
    --bg: #f3f3f5;
    --surface: rgba(255, 255, 255, 0.86);
    --surface-strong: rgba(255, 255, 255, 0.96);
    --ink: #111217;
    --muted: #626774;
    --line: rgba(17, 18, 23, 0.08);
    --accent: #6d28d9;
    --accent-deep: #4c1d95;
    --accent-soft: rgba(109, 40, 217, 0.12);
    --shadow: 0 24px 60px rgba(17, 18, 23, 0.08);
}

html, body, [class*="css"] {
    font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
    background:
        radial-gradient(circle at top left, rgba(109, 40, 217, 0.08), transparent 28%),
        radial-gradient(circle at top right, rgba(17, 18, 23, 0.05), transparent 24%),
        linear-gradient(180deg, #f8f8fa 0%, #f1f1f4 100%) !important;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(109, 40, 217, 0.08), transparent 28%),
        radial-gradient(circle at top right, rgba(17, 18, 23, 0.05), transparent 24%),
        linear-gradient(180deg, #f8f8fa 0%, #f1f1f4 100%) !important;
    color: #111217 !important;
}

div.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    background: transparent !important;
}

.main {
    background: transparent !important;
}

.main .block-container {
    animation: fade-in-up 0.55s ease;
    background: transparent !important;
}

@keyframes fade-in-up {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse-glow {
    0%, 100% {
        transform: scale(1);
        opacity: 0.65;
    }
    50% {
        transform: scale(1.08);
        opacity: 1;
    }
}

@keyframes soft-rise {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.nav-shell {
    margin-bottom: 1rem;
}

.nav-caption {
    color: var(--muted);
    font-size: 0.8rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
    font-weight: 600;
}

.nav-title {
    font-family: "Instrument Serif", Georgia, serif;
    font-size: 2rem;
    color: var(--ink);
    line-height: 1;
}

.hero-panel {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(245, 245, 248, 0.88));
    box-shadow: var(--shadow);
}

.hero-panel::before {
    content: "";
    position: absolute;
    right: -60px;
    bottom: -90px;
    width: 220px;
    height: 220px;
    border-radius: 999px;
    background: radial-gradient(circle, rgba(109, 40, 217, 0.22), rgba(109, 40, 217, 0));
    filter: blur(6px);
    pointer-events: none;
    animation: pulse-glow 7s ease-in-out infinite;
}

.hero-badge,
.section-eyebrow {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    background: rgba(17, 18, 23, 0.04);
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.hero-title {
    margin: 1rem 0 0.75rem;
    font-family: "Instrument Serif", Georgia, serif;
    font-size: clamp(2.5rem, 4.6vw, 4rem);
    line-height: 0.95;
    letter-spacing: -0.03em;
    color: var(--ink);
}

.hero-copy {
    max-width: 760px;
    color: var(--muted);
    font-size: 1.03rem;
    line-height: 1.7;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    margin-top: 1.4rem;
}

.metric-card {
    border: 1px solid var(--line);
    border-radius: 20px;
    background: rgba(250, 250, 252, 0.92);
    padding: 1rem 1.1rem;
}

.metric-label {
    color: var(--muted);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.metric-value {
    margin-top: 0.5rem;
    color: var(--ink);
    font-size: 1.06rem;
    font-weight: 600;
}

.section-head {
    margin: 0.65rem 0 0.9rem;
}

.section-title {
    margin: 0.5rem 0 0.45rem;
    color: var(--ink);
    font-size: 1.65rem;
    line-height: 1.1;
}

.section-copy {
    max-width: 760px;
    color: var(--muted);
    line-height: 1.65;
}

.query-summary {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    align-items: center;
    margin: 0.3rem 0 1rem;
    padding: 0.9rem 1rem;
    border-radius: 18px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.78);
}

.query-summary span {
    color: var(--muted);
    font-size: 0.9rem;
}

.query-summary strong {
    color: var(--ink);
    font-weight: 600;
}

.helper-note {
    margin: 0 0 0.8rem;
    padding: 0.95rem 1rem;
    border-radius: 18px;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.72);
    color: var(--muted);
    line-height: 1.6;
}

.doc-card {
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 1.15rem 1.2rem;
    margin-bottom: 0.75rem;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 12px 30px rgba(17, 18, 23, 0.06);
    animation: soft-rise 0.35s ease both;
}

.doc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.doc-header-left {
    display: flex;
    align-items: center;
    gap: 0.95rem;
    min-width: 0;
}

.doc-index {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.92rem;
    font-weight: 700;
    flex-shrink: 0;
}

.doc-name {
    color: var(--ink);
    font-size: 1.05rem;
    font-weight: 600;
    word-break: break-word;
}

.doc-path {
    margin-top: 0.2rem;
    color: var(--muted);
    font-size: 0.9rem;
    word-break: break-word;
}

.doc-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.38rem 0.7rem;
    border-radius: 999px;
    background: rgba(17, 18, 23, 0.05);
    color: var(--muted);
    font-size: 0.78rem;
    white-space: nowrap;
}

.message-row {
    display: flex;
    margin-bottom: 0.85rem;
}

.message-row.user {
    justify-content: flex-end;
}

.message-row.assistant {
    justify-content: flex-start;
}

.message-bubble {
    max-width: min(80%, 760px);
    border-radius: 22px;
    padding: 0.9rem 1rem;
    line-height: 1.65;
    box-shadow: 0 10px 26px rgba(17, 18, 23, 0.06);
    border: 1px solid var(--line);
}

.message-row.user .message-bubble {
    background: linear-gradient(135deg, var(--accent), var(--accent-deep));
    color: #ffffff;
    border-color: transparent;
    border-bottom-right-radius: 8px;
}

.message-row.assistant .message-bubble {
    background: rgba(255, 255, 255, 0.92);
    color: var(--ink);
    border-bottom-left-radius: 8px;
}

.message-meta {
    margin-bottom: 0.35rem;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    opacity: 0.82;
}

.empty-state {
    border: 1px dashed rgba(17, 18, 23, 0.16);
    border-radius: 24px;
    padding: 1.5rem;
    margin-top: 0.4rem;
    background: rgba(255, 255, 255, 0.66);
}

.empty-title {
    color: var(--ink);
    font-size: 1.12rem;
    font-weight: 600;
}

.empty-copy {
    margin-top: 0.35rem;
    color: var(--muted);
    line-height: 1.65;
}

/* 1. Estilo base para todos los botones */
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"],
div[data-testid="stDownloadButton"] button,
div[data-testid="stFormSubmitButton"] button {
    min-height: 2.75rem !important;
    border-radius: 999px !important;
    border: 1px solid var(--line) !important;
    background: rgba(255, 255, 255, 0.94) !important;
    color: var(--ink) !important;
    box-shadow: 0 10px 24px rgba(17, 18, 23, 0.05) !important;
    transition: all 0.2s ease !important;
}

/* 2. Hover general (Botones secundarios) */
div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:hover,
div[data-testid="stDownloadButton"] button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: white !important;
    transform: translateY(-1px) !important;
}

/* 3. Botón de SEARCH (Primary) - Estilo Normal */
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"],
div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primary"],
div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg, var(--accent), var(--accent-deep)) !important;
    color: #ffffff !important;
    border: none !important;
}

/* 4. Botón de SEARCH (Primary) - Estilo HOVER (Esto evita el Rojo) */
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover,
div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primary"]:hover,
div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: var(--accent-deep) !important; /* Un tono más oscuro */
    color: #ffffff !important;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.3) !important;
}

/* --- SUSTITUYE DESDE AQUÍ --- */

/* 1. Contenedor raíz: lo hacemos invisible para que no ensucie las esquinas */
div[data-testid="stTextInputRootElement"] {
    background-color: transparent !important;
    border: none !important;
}

/* 2. El "cuerpo" de la barra: aquí aplicamos tu diseño redondeado */
div[data-testid="stTextInputRootElement"] > div {
    border-radius: 999px !important;
    background: var(--surface-strong) !important;
    border: 1px solid var(--line) !important;
    box-shadow: 0 14px 32px rgba(17, 18, 23, 0.06) !important;
    padding: 2px 12px !important;
    transition: all 0.2s ease;
}

/* 3. El Input real: arreglamos el color del texto invisible */
div[data-testid="stTextInputRootElement"] input {
    color: var(--ink) !important; 
    font-size: 1rem !important;
    background-color: transparent !important;
    caret-color: var(--accent) !important; /* Color de la rayita que parpadea */
}

/* 4. Placeholder: para que se vea el texto de ejemplo */
div[data-testid="stTextInputRootElement"] input::placeholder {
    color: var(--muted) !important;
    opacity: 0.6;
}

/* 5. Comportamiento al hacer clic (Focus) */
div[data-testid="stTextInputRootElement"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent), 0 14px 32px rgba(109, 40, 217, 0.1) !important;
}

/* --- HASTA AQUÍ --- */

/* --- CHAT INPUT MATCHED TO RETRIEVAL SEARCH BAR --- */

/* Limpiar TODOS los fondos oscuros en la zona inferior */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stChatFloatingInputContainer"],
.stChatFloatingInputContainer,
.stChatInputContainer,
[data-testid="stChatInput"],
section[data-testid="stChatInput"],
div[data-testid="stChatInput"] {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* Limpiar todos los divs y elementos anidados */
[data-testid="stBottom"] *,
[data-testid="stBottomBlockContainer"] *,
.stChatInputContainer *,
[data-testid="stChatInput"] * {
    background: transparent !important;
}

/* Establecer el fondo CLARO en el contenedor del chat bottom */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stBottomBlockContainer"] > div {
    background: 
        radial-gradient(circle at top left, rgba(109, 40, 217, 0.08), transparent 28%),
        radial-gradient(circle at top right, rgba(17, 18, 23, 0.05), transparent 24%),
        linear-gradient(180deg, #f8f8fa 0%, #f1f1f4 100%) !important;
}

/* Una sola capa visual para evitar el efecto de barras superpuestas */
.stChatInputContainer > div,
[data-testid="stChatInput"] > div,
section[data-testid="stChatInput"] > div {
    background: rgba(255, 255, 255, 0.96) !important;
    border-radius: 999px !important;
    border: 1px solid rgba(17, 18, 23, 0.08) !important;
    box-shadow: 0 14px 32px rgba(17, 18, 23, 0.06) !important;
    padding: 0px 12px !important;
    transition: all 0.2s ease !important;
}

/* Las capas internas no deben dibujar otra barra */
.stChatInputContainer > div > div,
[data-testid="stChatInput"] > div > div,
section[data-testid="stChatInput"] > div > div,
.stChatInputContainer [data-baseweb="textarea"],
.stChatInputContainer [data-baseweb="base-input"],
.stChatInputContainer [data-baseweb="input"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
}

/* Focus state en el input */
.stChatInputContainer > div:focus-within,
[data-testid="stChatInput"] > div:focus-within,
section[data-testid="stChatInput"] > div:focus-within {
    border-color: #6d28d9 !important;
    box-shadow: 0 0 0 1px #6d28d9, 0 14px 32px rgba(109, 40, 217, 0.1) !important;
}

/* Textarea e input - asegurar que sean visibles sobre el fondo blanco */
.stChatInputContainer textarea,
.stChatInputContainer input,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input,
textarea[data-testid="stChatInputTextArea"],
input[data-testid="stChatInputTextArea"],
[data-baseweb="textarea"],
[data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
    color: #111217 !important;
    -webkit-text-fill-color: #111217 !important;
    caret-color: #6d28d9 !important;
    font-size: 1rem !important;
    font-family: "IBM Plex Sans", "Segoe UI", sans-serif !important;
    line-height: 1.35 !important;
    padding: 0.38rem 2.65rem 0.38rem 0.45rem !important;
    min-height: 1.35rem !important;
    outline: none !important;
}

.stChatInputContainer textarea::placeholder,
.stChatInputContainer input::placeholder,
[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInput"] input::placeholder,
textarea[data-testid="stChatInputTextArea"]::placeholder,
input[data-testid="stChatInputTextArea"]::placeholder {
    color: #626774 !important;
    opacity: 0.6 !important;
}

/* Botones en el chat input */
.stChatInputContainer button,
[data-testid="stChatInput"] button,
section[data-testid="stChatInput"] button {
    background: rgba(109, 40, 217, 0.08) !important;
    border: 1px solid rgba(109, 40, 217, 0.12) !important;
    border-radius: 999px !important;
    color: #6d28d9 !important;
    width: 1.9rem !important;
    height: 1.9rem !important;
    transition: all 0.2s ease !important;
}

.stChatInputContainer button:hover,
[data-testid="stChatInput"] button:hover,
section[data-testid="stChatInput"] button:hover {
    background: #6d28d9 !important;
    border-color: #6d28d9 !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

/* Limpiar pseudoelementos */
.stChatFloatingInputContainer::before,
.stChatFloatingInputContainer > div::before,
[data-testid="stChatInput"]::before,
section[data-testid="stChatInput"]::before {
    display: none !important;
}

/* --- FEEDBACK BUTTONS (Like / Dislike) --- */
/* Confirmado por inspección del DOM real: Streamlit traduce la key del
   propio st.button (ej. "like::search::1") en una clase
   "st-key-like--search--1" sobre su stElementContainer padre (los "::" se
   convierten en "--"). Le damos a cada botón una key que incluye el
   estado (idle/active) y apuntamos el CSS a esa clase real. */

/* Par like/dislike: reduce el gap entre ellos y los pega a la derecha,
   sin afectar el gap global de st.columns en el resto de la app. */
div[class*="st-key-fb-pair"] div[data-testid="stHorizontalBlock"] {
    gap: 0.3rem !important;
    justify-content: flex-end !important;
}

div[class*="st-key-fb-pair"] div[data-testid="stColumn"] {
    width: fit-content !important;
    min-width: fit-content !important;
    flex: 0 0 auto !important;
}

/* Forma circular + símbolo más grande, aplica a idle y active por igual */
div[class*="st-key-fb-"] button[data-testid="stBaseButton-secondary"] {
    width: 2.75rem !important;
    height: 2.75rem !important;
    min-height: 2.75rem !important;
    min-width: 2.75rem !important;
    padding: 0 !important;
    border-radius: 50% !important;
}

div[class*="st-key-fb-"] button[data-testid="stBaseButton-secondary"] p {
    font-size: 1.3rem !important;
    line-height: 1 !important;
}

div[class*="st-key-fb-active-"] button[data-testid="stBaseButton-secondary"] {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--accent-soft) !important;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.18) !important;
}

div[class*="st-key-fb-active-"] button[data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent-deep) !important;
    background: var(--accent-soft) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stSpinner"] > div {
    border-top-color: var(--accent);
}

div[data-testid="stHorizontalBlock"] {
    gap: 0.75rem;
}

@media (max-width: 900px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }

    .doc-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .message-bubble {
        max-width: 100%;
    }
}
</style>
"""


def apply_theme() -> None:
    st.markdown(THEME_CSS, unsafe_allow_html=True)

def render_hero_panel(
    badge: str,
    title: str,
    subtitle: str,
    metrics: list[tuple[str, str]] | None = None,
) -> None:
    metrics_markup = ""
    if metrics:
        cards = "".join(
            f"""
            <div class="metric-card">
                <div class="metric-label">{escape(label)}</div>
                <div class="metric-value">{escape(value)}</div>
            </div>
            """ for label, value in metrics
        )
        metrics_markup = f'<div class="metric-grid">{cards}</div>'
    with st.container():
        st.markdown(
            f"""
            <section class="hero-panel">
                <div class="hero-badge">{escape(badge)}</div>
                <h1 class="hero-title">{escape(title)}</h1>
                <p class="hero-copy">{escape(subtitle)}</p>
                {metrics_markup}
            </section>
            """,
            unsafe_allow_html=True,
        )

def render_section_intro(eyebrow: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <section class="section-head">
            <div class="section-eyebrow">{escape(eyebrow)}</div>
            <h2 class="section-title">{escape(title)}</h2>
            <p class="section-copy">{escape(description)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

def render_query_summary(query: str, result_count: int, label: str) -> None:
    st.markdown(
        f"""
        <div class="query-summary">
            <span>Latest query</span>
            <strong>{escape(query)}</strong>
            <span>{result_count} {escape(label)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_empty_state(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-title">{escape(title)}</div>
            <div class="empty-copy">{escape(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )