"""
Sameer Singh — portfolio site with F.R.I.D.A.Y., an AI assistant with two
modes: Personal (grounded only in this portfolio) and Web Search (a
general OpenAI-powered assistant with live web search).

Run locally:    streamlit run app.py
Config:         .streamlit/config.toml (theme), .streamlit/secrets.toml (API key)
"""

import os

import streamlit as st

from data import (
    PROFILE, SKILLS, EXPERIENCE, PROJECTS, ADDITIONAL_PROJECTS, EDUCATION,
    CERTIFICATIONS, ACHIEVEMENTS, BOOKS, HOBBIES, GALLERY,
    SUGGESTED_QUESTIONS_PERSONAL, 
    SUGGESTED_QUESTIONS_WEB,
    PERSONAL_SYSTEM_PROMPT, WEB_SYSTEM_PROMPT,
)
from chat_engine import get_client, stream_reply, friendly_error, PERSONAL_MODEL, WEB_MODEL

st.set_page_config(
    page_title=f"{PROFILE['name']} | {PROFILE['tagline']}",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLE — "analyst's notebook": paper + graph-paper grid, amber
# accent, monospace data labels. See README for the design plan.
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --fri-ink: #14171C;
    --fri-paper: #F7F7F5;
    --fri-card: #FFFFFF;
    --fri-line: #E3E5E8;
    --fri-grid: rgba(20,23,28,0.05);
    --fri-accent: #E8952E;
    --fri-accent-ink: #7A4B00;
    --fri-accent-soft: rgba(232,149,46,0.12);
    --fri-slate: #45566B;
    --fri-slate-bg: #EEF2F5;
    --fri-mono: 'IBM Plex Mono', ui-monospace, monospace;
    --fri-display: 'Space Grotesk', sans-serif;
    --fri-body: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background-color: var(--fri-paper);
    background-image:
        linear-gradient(var(--fri-grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--fri-grid) 1px, transparent 1px);
    background-size: 28px 28px;
}
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1100px; }
.stApp, .stApp p, .stApp li, .stApp span, .stApp label { font-family: var(--fri-body); }
.stApp h1, .stApp h2, .stApp h3 { font-family: var(--fri-display) !important; color: var(--fri-ink); }

/* Hero "query result" card — the one bold element on the page */
.fri-hero {
    background: var(--fri-card);
    border: 1px solid var(--fri-line);
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin: 0.25rem 0 1.5rem 0;
    box-shadow: 0 1px 2px rgba(20,23,28,0.04);
}
.fri-query { font-family: var(--fri-mono); font-size: 0.92rem; color: var(--fri-slate); }
.fri-query div { line-height: 1.5; }
.fri-hero-divider {
    font-family: var(--fri-mono); font-size: 0.78rem; color: #9AA3AD;
    margin: 0.9rem 0; letter-spacing: 0.02em;
}
.fri-hero-name { font-family: var(--fri-display); font-size: 2.1rem; font-weight: 700; color: var(--fri-ink); line-height: 1.15; }
.fri-hero-role { font-size: 1.02rem; color: var(--fri-slate); margin: 0.2rem 0 1rem 0; }
.fri-hero-stats { display: flex; flex-wrap: wrap; gap: 0.5rem; }

.fri-pill {
    font-family: var(--fri-mono); font-size: 0.78rem; padding: 0.32rem 0.7rem;
    border-radius: 999px; background: var(--fri-slate-bg); color: var(--fri-slate);
    display: inline-block;
}
.fri-pill-accent { background: var(--fri-accent-soft); color: var(--fri-accent-ink); }

.fri-mode-box {
    font-size: 0.92rem; padding: 0.7rem 1rem; border-radius: 12px;
    background: var(--fri-accent-soft); border: 1px solid rgba(232,149,46,0.35);
    color: var(--fri-accent-ink); margin-bottom: 1rem;
}

.fri-card {
    background: var(--fri-card); border: 1px solid var(--fri-line);
    border-radius: 14px; padding: 1.4rem 1.5rem; margin-bottom: 1rem;
    transition: border-color 0.15s ease, transform 0.15s ease;
}
.fri-card:hover { border-color: var(--fri-accent); transform: translateY(-2px); }
.fri-eyebrow {
    font-family: var(--fri-mono); font-size: 0.72rem; letter-spacing: 0.06em;
    color: var(--fri-accent-ink); text-transform: uppercase;
}
.fri-card-title { font-family: var(--fri-display); font-size: 1.2rem; font-weight: 600; color: var(--fri-ink); margin: 0.2rem 0 0.4rem 0; }
.fri-card-sub { color: var(--fri-slate); margin-bottom: 0.6rem; }
.fri-tech-pill {
    display: inline-block; font-family: var(--fri-mono); font-size: 0.74rem;
    padding: 0.2rem 0.6rem; margin: 0.15rem 0.3rem 0.15rem 0;
    border-radius: 999px; background: var(--fri-slate-bg); color: var(--fri-slate);
}

.fri-kv { display: flex; gap: 0.75rem; padding: 0.4rem 0; border-bottom: 1px solid var(--fri-line); }
.fri-kv:last-child { border-bottom: none; }
.fri-kv-key { font-family: var(--fri-mono); font-size: 0.82rem; color: var(--fri-slate); min-width: 130px; }
.fri-kv-val { color: var(--fri-ink); }

@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}
:focus-visible { outline: 2px solid var(--fri-accent); outline-offset: 2px; }
</style>
""", unsafe_allow_html=True)


def safe_image(path, **kwargs):
    """Show an image if it exists locally, else a small actionable hint."""
    if os.path.exists(path):
        st.image(path, **kwargs)
    else:
        st.caption(f"🖼️ add `{path}` to see this image")


def kv_row(key, value):
    st.markdown(f'<div class="fri-kv"><div class="fri-kv-key">{key}</div><div class="fri-kv-val">{value}</div></div>', unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("fri_personal_history", [])
st.session_state.setdefault("fri_web_history", [])

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    safe_image(PROFILE["photo_path"], width='stretch')
    st.markdown(f"### {PROFILE['name']}")
    st.caption(PROFILE["tagline"])
    st.write(PROFILE["summary"])

    st.divider()
    st.markdown("**Resume**")
    if os.path.exists(PROFILE["resume_path"]):
        with open(PROFILE["resume_path"], "rb") as f:
            st.download_button(
                "⬇ Download resume", f,
                file_name=f"{PROFILE['name'].replace(' ', '_')}_Resume.pdf",
                mime="application/pdf", width='stretch',
            )
    else:
        st.caption(f"Add `{PROFILE['resume_path']}` to enable this download.")

    st.divider()
    st.markdown("**Contact**")
    st.caption(f"✉️ {PROFILE['email']}")
    st.caption(f"🔗 {PROFILE['github']}")
    st.caption(f"🔗 {PROFILE['linkedin']}")

    st.divider()
    st.caption("Built with Streamlit + OpenAI")

# ============================================================
# HERO
# ============================================================

st.markdown(f"""
<div class="fri-hero">
    <div class="fri-query">
        <div>&gt; SELECT * FROM analysts</div>
        <div>&nbsp;&nbsp;WHERE focus = 'BI &amp; GenAI';</div>
    </div>
    <div class="fri-hero-divider">— 1 row returned —</div>
    <div class="fri-hero-name">{PROFILE['name']}</div>
    <div class="fri-hero-role">{PROFILE['tagline']} · {PROFILE['based_in']}</div>
    <div class="fri-hero-stats">
        <span class="fri-pill">{PROFILE['years_experience']} experience</span>
        <span class="fri-pill">5 dashboards shipped</span>
        <span class="fri-pill">400K+ row datasets</span>
        <span class="fri-pill fri-pill-accent">{PROFILE['status']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🤖 F.R.I.D.A.Y.", "🚀 Projects", "🙂 About Me", "🏆 Notable Achievements",
])

# ------------------------------------------------------------
# TAB 1 — F.R.I.D.A.Y.
# ------------------------------------------------------------

with tab1:
    mode = st.segmented_control(
        "Mode", options=["Personal","Web Search"], default="Personal",
        required=True, key="fri_mode", label_visibility="collapsed",
    )

    if mode == "Personal":
        st.markdown(
            '<div class="fri-mode-box">🧠 <b>Personal mode</b> — answers only from this portfolio: '
            'Sameer\'s resume, skills, experience and projects.</div>',
            unsafe_allow_html=True,
        )
        history_key = "fri_personal_history"
        instructions = PERSONAL_SYSTEM_PROMPT
        model = PERSONAL_MODEL
        use_web_search = False
        suggestions = SUGGESTED_QUESTIONS_PERSONAL
    else:
        st.markdown(
            '<div class="fri-mode-box">🌐 <b>Web Search mode</b> — a general OpenAI-powered '
            'assistant with live web search, not limited to this portfolio.</div>',
            unsafe_allow_html=True,
        )
        history_key = "fri_web_history"
        instructions = WEB_SYSTEM_PROMPT
        model = WEB_MODEL
        use_web_search = True
        suggestions = SUGGESTED_QUESTIONS_WEB

    history = st.session_state[history_key]

    if not history:
        st.caption("Try asking:")
        cols = st.columns(len(suggestions))
        for col, question in zip(cols, suggestions):
            if col.button(question, key=f"chip_{history_key}_{question}", width='stretch'):
                st.session_state[f"{history_key}_pending"] = question
                st.rerun()

    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pending_prompt = st.session_state.pop(f"{history_key}_pending", None)
    typed_prompt = st.chat_input("Ask F.R.I.D.A.Y. anything...")
    prompt = pending_prompt or typed_prompt

    if prompt:
        history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            client = get_client()
            if client is None:
                answer = (
                    "F.R.I.D.A.Y. isn't connected yet — add `OPENAI_API_KEY` to "
                    "`.streamlit/secrets.toml` (see README.md) to turn it on."
                )
                st.warning(answer)
            else:
                try:
                    stream = stream_reply(client, model, instructions, history, use_web_search=use_web_search)
                    answer = st.write_stream(stream)
                except Exception as exc:
                    answer = friendly_error(exc)
                    st.error(answer)

        history.append({"role": "assistant", "content": answer})

    if history:
        if st.button("🧹 Clear this chat", key=f"clear_{history_key}"):
            st.session_state[history_key] = []
            st.rerun()

# ------------------------------------------------------------
# TAB 2 — PROJECTS
# ------------------------------------------------------------

with tab2:
    st.markdown("### Projects")
    st.write("Four projects from Sameer's resume, plus a couple of side builds below.")

    for p in PROJECTS:
        st.markdown(f"""
        <div class="fri-card">
            <div class="fri-eyebrow">{p['id']}</div>
            <div class="fri-card-title">{p['title']}</div>
            <div class="fri-card-sub">{p['one_liner']}</div>
            {''.join(f'<span class="fri-tech-pill">{t}</span>' for t in p['tags'])}
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Details"):
            st.write(p["description"])
            if p["link"]:
                st.link_button(p["link_label"], p["link"])

    st.divider()
    st.markdown("#### Additional / side projects")
    for p in ADDITIONAL_PROJECTS:
        with st.expander(p["title"]):
            st.write(p["description"])

# ------------------------------------------------------------
# TAB 3 — ABOUT ME
# ------------------------------------------------------------

with tab3:
    col1, col2 = st.columns([1, 2])
    with col1:
        safe_image(PROFILE["photo_path"], width='stretch')
    with col2:
        st.markdown(f"### {PROFILE['name']}")
        kv_row("role", PROFILE["tagline"])
        kv_row("based", f"{PROFILE['based_in']} ({PROFILE['work_location_note']})")
        kv_row("education", f"{EDUCATION['degree']}<br>{EDUCATION['institution']} — {EDUCATION['completed']}")
        kv_row("status", PROFILE["status"])

    st.divider()
    st.markdown("#### Experience")
    for job in EXPERIENCE:
        st.markdown(f"**{job['role']}, {job['company']}** &nbsp;·&nbsp; {job['location']} &nbsp;·&nbsp; *{job['dates']}*")
        for b in job["bullets"]:
            st.markdown(f"- {b}")
        st.write("")

    st.divider()
    st.markdown("#### Skills")
    skill_cols = st.columns(2)
    for i, (category, items) in enumerate(SKILLS.items()):
        with skill_cols[i % 2]:
            st.markdown(f"**{category}**")
            st.markdown("".join(f'<span class="fri-tech-pill">{s}</span>' for s in items), unsafe_allow_html=True)
            st.write("")

    st.divider()
    st.markdown("#### Certifications")
    for c in CERTIFICATIONS:
        st.markdown(f"✓ {c}")

    st.divider()
    st.markdown("#### A few photos")
    gallery_cols = st.columns(3)
    for i, item in enumerate(GALLERY):
        with gallery_cols[i % 3]:
            safe_image(item["path"], caption=item["caption"], width='stretch')

    st.divider()
    st.markdown("#### Outside of work")
    st.write(f"**Hobbies:** {', '.join(HOBBIES)}")
    st.markdown("**Currently/recently reading:**")
    for b in BOOKS:
        st.markdown(f"- {b}")
    st.link_button("📸 Instagram", PROFILE["instagram_url"])

# ------------------------------------------------------------
# TAB 4 — NOTABLE ACHIEVEMENTS
# ------------------------------------------------------------

with tab4:
    st.markdown("### Notable Achievements")
    for a in ACHIEVEMENTS:
        st.markdown(f"""
        <div class="fri-card">
            <div class="fri-eyebrow">{a['id']}</div>
            <div class="fri-card-title">{a['title']}</div>
            <div class="fri-card-sub">{a['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        img_cols = st.columns(len(a["images"]))
        for col, img_path in zip(img_cols, a["images"]):
            with col:
                safe_image(img_path, width='stretch')
        st.write("")

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    f'<div style="text-align:center; color: var(--fri-slate); font-size: 0.85rem; padding: 1rem 0;">'
    f'Built with Streamlit + OpenAI &nbsp;·&nbsp; F.R.I.D.A.Y. — {PROFILE["name"]}\'s portfolio assistant</div>',
    unsafe_allow_html=True,
)
