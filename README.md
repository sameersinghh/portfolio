# Sameer Singh — Portfolio

## Project structure

```
sameer-portfolio/
├── app.py                       # UI: page config, styling, sidebar, 4 tabs
├── data.py                      # ALL content lives here — edit this to update the site
├── chat_engine.py                # OpenAI client + streaming
├── requirements.txt
├── .gitignore                   # already excludes secrets.toml
├── .streamlit/
│   ├── config.toml              # theme (already set up)
│   └── secrets.toml.example     # copy → secrets.toml, add your key
└── assets/                      # add your own files here (see list below)
```

## Setup

```bash
cd sameer-portfolio
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# now edit .streamlit/secrets.toml and paste your NEW key
```

Run it:

```bash
streamlit run app.py
```

## Deploying (Streamlit Community Cloud)

1. Push this folder to a GitHub repo — `.gitignore` already keeps
   `secrets.toml` out of it.
2. On [share.streamlit.io](https://share.streamlit.io), point a new app
   at the repo, main file `app.py`.
3. In the app's **Settings → Secrets**, paste the same
   `OPENAI_API_KEY = "sk-..."` line — this is the cloud equivalent of
   your local `secrets.toml`.

## What changed from the previous version

- **The exposed API key isn't in any file.** Both the code and this
  README point you to secrets/env vars instead.
- **Streaming was actually broken.** The Responses API streams typed
  *events* (`response.output_text.delta`, `response.completed`, …), not
  plain text — piping that stream straight into `st.write_stream()`
  wouldn't have rendered correctly. `chat_engine.py` now filters to just
  the text deltas.
- **The model name didn't exist.** `gpt-5.6-mini` isn't a real model —
  swapped in `gpt-5.6-luna` (cheap, plenty for grounded Q&A) for
  Personal mode and `gpt-5.6-terra` for Web Search mode. Check
  [OpenAI's pricing page](https://platform.openai.com/docs/pricing) if
  these are ever retired and swap the two constants at the top of
  `chat_engine.py`.
- **The mode switch moved out of the sidebar.** On a phone, Streamlit's
  sidebar starts collapsed, so the Personal/Web Search toggle — the
  actual core feature you asked for — could go unnoticed. It's now at
  the top of the F.R.I.D.A.Y. tab itself.
- **One content section was dropped in the earlier rewrite and is
  restored:** the About Me travel-photo gallery (Moon/birds/hallway/
  Red Fort/beach/decor).
- **All content is now in one place (`data.py`)** instead of being
  duplicated between the visible UI and F.R.I.D.A.Y.'s system prompt —
  edit a bullet once and both stay in sync.
- **Filenames are now lowercase with no spaces** (e.g. `ncc_camp_
  certificate.jpeg` instead of `NCC camp certificate.jpeg`) — mixed
  case and spaces are a common source of "works on my machine, breaks
  once deployed" bugs on Linux hosts.
- Dropped the non-functional star-rating widget (it wasn't wired to
  any storage, so feedback vanished on every rerun). Easy to re-add
  properly with Streamlit's persistent storage if you want it back.
- Suggested-question chips were added so a first-time visitor has
  something to tap instead of a blank input box.
