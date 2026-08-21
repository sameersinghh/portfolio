"""
OpenAI client + streaming helpers for F.R.I.D.A.Y.

Uses the OpenAI Responses API (client.responses.create), which is the
current recommended API for new OpenAI integrations. Two models are used
so Personal mode stays cheap even under heavy traffic, while Web Search
mode gets a slightly stronger model for open-ended reasoning.

Model names change as OpenAI ships new tiers — if these ever 404, check
the current lineup at https://platform.openai.com/docs/pricing and swap
the constants below.
"""

import os

import streamlit as st
from openai import (
    OpenAI,
    APIConnectionError,
    APIError,
    AuthenticationError,
    RateLimitError,
)

PERSONAL_MODEL = "gpt-5.6-luna"   # cheap + fast — plenty for Q&A grounded in a fixed context
WEB_MODEL = "gpt-5.6-terra"       # a step up, for open-ended web-search reasoning


def _read_api_key():
    """Read the key from Streamlit secrets first, then environment variables."""
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("OPENAI_API_KEY")


@st.cache_resource(show_spinner=False)
def get_client():
    """Return a cached OpenAI client, or None if no key is configured."""
    api_key = _read_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _stream_text(response_stream):
    """
    Turn a Responses API event stream into plain text chunks that
    st.write_stream() can render. The raw stream yields typed events
    (response.created, response.output_text.delta, response.completed, ...)
    — only the text-delta events carry the tokens visitors should see.
    """
    for event in response_stream:
        event_type = getattr(event, "type", "")
        if event_type == "response.output_text.delta":
            yield event.delta
        elif event_type in ("response.failed", "response.error", "error"):
            error_obj = getattr(event, "error", None)
            message = getattr(error_obj, "message", None) or str(error_obj) if error_obj else None
            raise RuntimeError(message or "The model reported an error while responding.")


def stream_reply(client, model, instructions, history, use_web_search=False):
    """
    Start a Responses API stream and return a generator of text chunks.

    `history` is a list of {"role": "user"|"assistant", "content": str}
    dicts — no "system" entry, since `instructions` carries the system
    prompt as its own top-level parameter.
    """
    tools = [{"type": "web_search"}] if use_web_search else None
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=history,
        tools=tools,
        stream=True,
    )
    return _stream_text(response)


def friendly_error(exc):
    """Turn OpenAI/network exceptions into a short message safe to show visitors."""
    if isinstance(exc, AuthenticationError):
        return "F.R.I.D.A.Y. can't authenticate with OpenAI right now — the API key may be missing or invalid."
    if isinstance(exc, RateLimitError):
        return "F.R.I.D.A.Y. is getting a lot of questions right now — please try again in a moment."
    if isinstance(exc, APIConnectionError):
        return "F.R.I.D.A.Y. couldn't reach OpenAI — check your connection and try again."
    if isinstance(exc, APIError):
        return "OpenAI returned an error while F.R.I.D.A.Y. was responding. Please try again."
    return "Something went wrong while F.R.I.D.A.Y. was responding. Please try again."
