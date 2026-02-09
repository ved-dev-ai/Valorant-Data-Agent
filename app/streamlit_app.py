import streamlit as st

from main import answer_question


st.set_page_config(page_title="Valorant Data Agent", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Work+Sans:wght@400;600&display=swap');

    :root {
        --bg-1: #0f1226;
        --bg-2: #101826;
        --accent: #ff5f5f;
        --accent-2: #ffd166;
        --text: #e9edf5;
        --muted: #9aa6b2;
        --card: rgba(19, 23, 39, 0.9);
        --border: rgba(255, 255, 255, 0.08);
    }

    .stApp {
        background: radial-gradient(1200px 600px at 10% 0%, rgba(255, 95, 95, 0.15), transparent 60%),
                    radial-gradient(900px 500px at 90% 10%, rgba(255, 209, 102, 0.12), transparent 60%),
                    linear-gradient(160deg, var(--bg-1), var(--bg-2));
        color: var(--text);
        font-family: 'Work Sans', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.02em;
    }

    .hero {
        padding: 1.8rem 1.6rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(255, 95, 95, 0.18), rgba(19, 23, 39, 0.92));
        border: 1px solid var(--border);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 1rem;
        margin-bottom: 0.9rem;
    }

    .chip {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: rgba(255, 255, 255, 0.04);
        color: var(--text);
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }

    .info-card {
        padding: 1rem 1.1rem;
        border-radius: 14px;
        border: 1px solid var(--border);
        background: var(--card);
        min-height: 96px;
    }

    .info-title {
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .info-text {
        color: var(--muted);
        font-size: 0.9rem;
    }

    .stChatInput textarea {
        border-radius: 14px;
        border: 1px solid var(--border);
        background: rgba(255, 255, 255, 0.04);
    }

    .stChatMessage {
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Valorant Data Agent</div>
        <div class="hero-subtitle">Ask about teams, players, results, and stats. The agent blends database facts with contextual summaries.</div>
        <span class="chip">SQL facts</span>
        <span class="chip">RAG context</span>
        <span class="chip">Fast answers</span>
    </div>
    """,
    unsafe_allow_html=True,
)

top_left, top_mid, top_right = st.columns(3)
with top_left:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">What you can ask</div>
            <div class="info-text">Team info, roster changes, match results, map stats, and tournament highlights.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_mid:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">How it answers</div>
            <div class="info-text">Prioritizes SQL facts, adds short explanations from the RAG knowledge base.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_right:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">Try prompts</div>
            <div class="info-text">"Who is the coach of Leviatan?" or "Top 5 players by kda."</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask a question about Valorant data")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = answer_question(user_prompt)
            except Exception as exc:  # pragma: no cover - UI error handling
                response = f"Sorry, I ran into an error: {exc}"
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
