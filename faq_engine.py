"""
Fully local Q&A engine for F.R.I.D.A.Y.'s Personal mode.

No network calls, no API key, no third-party package — this only reads
data.py using the standard library. That means Personal mode works even
if OpenAI is down, misconfigured, or the openai package itself fails to
install on a given host (which is exactly what happened on first deploy).

How it works: every answerable topic (each project, each skill category,
KPMG experience, education, ...) gets a set of keywords pulled straight
out of data.py. A question is matched to whichever topic shares the most
keywords with it. It's a bag-of-words lookup, not an LLM — good enough
for a bounded portfolio FAQ, and it can never be "down".
"""

import re

from data import (
    PROFILE, SKILLS, EXPERIENCE, PROJECTS, ADDITIONAL_PROJECTS,
    EDUCATION, CERTIFICATIONS, ACHIEVEMENTS, BOOKS, HOBBIES,
)

_STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with",
    "this", "that", "these", "those", "from", "using", "use", "used", "is",
    "are", "was", "were", "by", "at", "as", "it", "its", "into", "across",
    "over", "via", "based", "technology", "technologies",
    # Question/grammar words: excluded everywhere, mainly so they can't leak
    # from a project's own description prose into its keyword set (e.g. "...
    # exploring HOW review text..." was making every "how" question match
    # that project instead of the topic it was actually about).
    "how", "what", "why", "when", "who", "which", "can", "could", "does",
    "do", "did", "will", "would", "should", "has", "have", "had",
    "he", "his", "him", "she", "her", "they", "them", "their",
    "tell", "me", "you", "your", "about", "any", "some", "all", "just",
    "also", "more", "most", "than", "then", "so", "if", "out", "up", "down",
    "not", "no", "yes",
}

# Only stripped out of AUTO-GENERATED project keywords (title/description/tags),
# so an individual project's blurb saying "...this project uses..." doesn't
# make it match every generic "what projects...ʺ / "...built?" question. The
# query itself, and the hand-written overview topic below, keep these words —
# that's specifically how generic questions route to the overview instead.
_PROJECT_GENERIC_WORDS = {"project", "projects", "portfolio", "built", "build", "made"}


def _words(text, exclude_extra=None):
    exclude = _STOPWORDS | (exclude_extra or set())
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in exclude and len(w) > 1}


def _project_topics():
    """One topic per project, keywords drawn from title + description + tags."""
    topics = []
    for p in PROJECTS:
        keywords = _words(p["title"], _PROJECT_GENERIC_WORDS) | _words(p["description"], _PROJECT_GENERIC_WORDS)
        for t in p.get("tags", []):
            keywords |= _words(t, _PROJECT_GENERIC_WORDS)
        lines = [f"**{p['title']}**", "", p["description"]]
        if p.get("tags"):
            lines += ["", "Technologies: " + ", ".join(p["tags"])]
        if p.get("link"):
            lines += ["", f"🔗 {p['link_label']}: {p['link']}"]
        topics.append({"keywords": keywords, "answer": "\n".join(lines)})
    for p in ADDITIONAL_PROJECTS:
        keywords = _words(p["title"], _PROJECT_GENERIC_WORDS) | _words(p["description"], _PROJECT_GENERIC_WORDS)
        topics.append({"keywords": keywords, "answer": f"**{p['title']}**\n\n{p['description']}"})
    return topics


def _skill_topics():
    """One topic per skill category, so 'his Python experience' etc. resolve directly."""
    topics = []
    for category, items in SKILLS.items():
        keywords = _words(category)
        for item in items:
            keywords |= _words(item)
        topics.append({"keywords": keywords, "answer": f"**{category}:** {', '.join(items)}"})
    return topics


def _specific_topics():
    exp_lines = []
    for job in EXPERIENCE:
        exp_lines.append(f"**{job['role']}, {job['company']}** — {job['dates']} ({job['location']})")
        exp_lines.extend(f"- {b}" for b in job["bullets"])
        exp_lines.append("")

    ach_lines = [f"- **{a['title']}** — {a['description']}" for a in ACHIEVEMENTS]

    return [
        {
            "keywords": {"kpmg", "experience", "work", "career", "job", "analyst",
                         "employment", "worked", "intern", "internship", "academic"},
            "answer": "\n".join(exp_lines).strip(),
        },
        {
            "keywords": {"education", "degree", "college", "university", "btech",
                         "bachelor", "academic", "study", "studied", "school"},
            "answer": f"**{EDUCATION['degree']}**\n{EDUCATION['institution']} — completed {EDUCATION['completed']}",
        },
        {
            "keywords": {"certification", "certifications", "certificate",
                         "certificates", "certified", "course", "courses"},
            "answer": "Certifications:\n\n" + "\n".join(f"- {c}" for c in CERTIFICATIONS),
        },
        {
            "keywords": {"achievement", "achievements", "award", "awards",
                         "accomplishment", "accomplishments", "recognition",
                         "spot", "ubisoft", "ncc"},
            "answer": "Notable achievements:\n\n" + "\n".join(ach_lines),
        },
        {
            "keywords": {"contact", "email", "github", "linkedin", "reach",
                         "connect", "portfolio", "website", "link", "links"},
            "answer": (
                f"**Email:** {PROFILE['email']}\n"
                f"**GitHub:** {PROFILE['github']}\n"
                f"**LinkedIn:** {PROFILE['linkedin']}\n"
                f"**Portfolio:** {PROFILE['portfolio']}"
            ),
        },
        {
            "keywords": {"hobby", "hobbies", "outside", "free", "book", "books",
                         "read", "reading", "interest", "interests", "fun", "personal"},
            "answer": (
                f"Outside work: {', '.join(HOBBIES)}.\n\n"
                "A few books he's enjoyed recently:\n" + "\n".join(f"- {b}" for b in BOOKS[:5])
            ),
        },
    ]


def _general_topics():
    proj_lines = [f"- **{p['title']}** — {p['one_liner']}" for p in PROJECTS]
    proj_lines += [f"- **{p['title']}**" for p in ADDITIONAL_PROJECTS]
    skills_lines = [f"**{cat}:** {', '.join(items)}" for cat, items in SKILLS.items()]

    return [
        {
            "keywords": {"hi", "hello", "hey", "yo", "namaste", "greetings"},
            "answer": (
                "Hello! I'm F.R.I.D.A.Y., Sameer's portfolio assistant. Ask me about his "
                "experience, projects, skills, education, certifications or achievements — "
                "or tap one of the suggestions above."
            ),
        },
        {
            "keywords": {"who", "about", "introduce", "introduction", "summary",
                         "profile", "yourself", "sameer"},
            "answer": (
                f"**{PROFILE['name']}** — {PROFILE['tagline']}, {PROFILE['years_experience']} of experience.\n\n"
                f"{PROFILE['summary']}\n\n"
                f"Based in {PROFILE['based_in']}. {PROFILE['status']}."
            ),
        },
        {
            "keywords": {"skill", "skills", "technical", "capable", "good", "stack", "toolkit"},
            "answer": "Sameer's technical skill set:\n\n" + "\n".join(skills_lines),
        },
        {
            "keywords": {"project", "projects", "portfolio", "built", "build", "made"},
            "answer": "Sameer's projects:\n\n" + "\n".join(proj_lines),
        },
    ]


_TOPICS = _project_topics() + _skill_topics() + _specific_topics() + _general_topics()

_FALLBACK = (
    "I don't have a good answer for that from Sameer's portfolio. I can tell you about his:\n\n"
    "- Experience at KPMG (Analyst + Academic Intern)\n"
    "- Projects — churn prediction, network security, YouTube analytics, and more\n"
    "- Technical skills — Python, SQL, ML, GenAI, Tableau/Power BI\n"
    "- Education & certifications\n"
    "- Achievements\n"
    "- Contact details\n\n"
    "Try something like *\"What did Sameer build with deep learning?\"*"
)


def answer(question):
    """Return the best-matching local answer for a question, or a helpful fallback."""
    if not question or not question.strip():
        return _FALLBACK
    q_words = _words(question)
    if not q_words:
        return _FALLBACK

    best_topic, best_score = None, 0
    for topic in _TOPICS:
        score = len(q_words & topic["keywords"])
        if score > best_score:
            best_score, best_topic = score, topic

    return best_topic["answer"] if best_topic else _FALLBACK
