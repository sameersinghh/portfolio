"""
Portfolio content for Sameer Singh.

Everything the site displays — and everything F.R.I.D.A.Y. (personal mode)
is allowed to know — is defined ONCE here as plain data. app.py renders it,
and build_personal_system_prompt() turns it into the assistant's system
prompt. Update a bullet point here and both the page and the assistant
stay in sync automatically.

To update the site: edit the structures below. Nothing else needs to change.
"""

PROFILE = {
    "name": "Sameer Singh",
    "tagline": "Data & BI Analyst",
    "years_experience": "2 years",
    "based_in": "Amritsar, Punjab",
    "work_location_note": "Worked in Bengaluru, Karnataka",
    "status": "Open to Data / BI Analyst roles",
    "email": "sameersingh.general@gmail.com",
    "github": "github.com/sameersinghh",
    "linkedin": "linkedin.com/in/sameer-singhh",
    "portfolio": "sameersinghh.com",
    "instagram_url": "https://www.instagram.com/sameersinghh/",
    "resume_path": "assets/resume.pdf",
    "photo_path": "assets/me.jpg",
    "summary": (
        "Data Analyst / Data Science professional with 2 years of experience "
        "delivering business intelligence and analytical solutions. Experienced "
        "in transforming large datasets into actionable insights through "
        "exploratory data analysis, customer segmentation, A/B testing, "
        "statistical modelling and KPI analysis. Hands-on experience applying "
        "Generative AI, MLOps and NLP to build analytical applications."
    ),
}

SKILLS = {
    "Programming & Data": ["Python", "Pandas", "NumPy", "Scikit-learn", "SQL", "Jupyter Notebook"],
    "SQL": ["Advanced queries", "Joins", "CTEs", "Window functions"],
    "Data Engineering": ["Extraction", "Cleaning", "Transformation", "ETL", "Processing"],
    "Visualisation & BI": ["Tableau", "Power BI", "Matplotlib", "Seaborn", "Dashboard development"],
    "Statistics": ["Hypothesis testing", "Regression analysis", "A/B testing", "Forecasting", "Quantitative analysis"],
    "AI / GenAI": ["Machine Learning", "Generative AI", "Google Gemini Pro", "LangChain", "Streamlit", "LLM-powered apps"],
    "Professional": ["Strategic thinking", "Communication", "Presentation skills"],
}

EXPERIENCE = [
    {
        "role": "Analyst",
        "company": "KPMG",
        "location": "Bengaluru, Karnataka",
        "dates": "Sep 2024 – Jun 2026",
        "bullets": [
            "Built and maintained 5 dashboards across Tableau and Power BI for "
            "banking-sector and mobile-tower-operator engagements.",
            "Wrote and optimised SQL queries to work with 400K+ row datasets.",
            "Used Python, SQL and statistical techniques to analyse operational "
            "and business data, identifying KPI trends and reporting inconsistencies.",
            "Translated stakeholder requirements into scalable analytical and "
            "reporting solutions, then automated the recurring reporting "
            "workflows and dashboard pipelines.",
            "Communicated findings through dashboards and business "
            "presentations, and supported data quality and validation processes.",
        ],
    },
    {
        "role": "Academic Intern",
        "company": "KPMG",
        "location": "Bengaluru, Karnataka",
        "dates": "Apr 2024 – Sep 2024",
        "bullets": [
            "Supported dashboard development and maintenance using Tableau, "
            "Power BI and SQL.",
            "Prepared and validated telecom datasets and performed data QA, "
            "resolving reporting inconsistencies.",
            "Performed ad hoc analytical reporting.",
        ],
    },
]

PROJECTS = [
    {
        "id": "PROJ-01",
        "title": "Customer Churn Prediction (ANN)",
        "one_liner": "Predicting which bank customers are likely to leave, from behavioural data.",
        "tags": ["Python", "Keras", "TensorFlow", "ANN", "Streamlit"],
        "description": (
            "Analysed 10K+ bank customer records across 11 behavioural attributes "
            "to forecast retention. Covered data cleaning and preprocessing, "
            "building and optimising an Artificial Neural Network in Keras/"
            "TensorFlow, and deploying the final predictive pipeline as a "
            "Streamlit web app."
        ),
        "link": "https://customerchurnprediction-sameersingh.streamlit.app/",
        "link_label": "Launch project",
    },
    {
        "id": "PROJ-02",
        "title": "Merchant Sales Analytics Dashboard",
        "one_liner": "A Power BI dashboard answering 8 defined merchant sales questions.",
        "tags": ["Power BI", "DAX", "Data Modelling", "Business Analytics"],
        "description": (
            "Built against 8 business requirements covering top/bottom product "
            "performance, time trends, period comparisons, discount analysis "
            "and city-level sales. The dimensional model uses 1 fact table and "
            "3 dimension tables, with map, bar, scatter, line and column "
            "visualisations supporting measure-level and cross-visual filtering."
        ),
        "link": (
            "https://app.powerbi.com/groups/me/reports/695c298a-84a8-4571-b8cb-"
            "d96678b615fa?ctid=8cb6efdc-e967-4f25-b141-f1002ca257dd&pbi_source="
            "linkShare&bookmarkGuid=9714f8f5-199b-475e-908d-5e8c52bde149"
        ),
        "link_label": "Open dashboard",
    },
    {
        "id": "PROJ-03",
        "title": "Network Security System",
        "one_liner": "An end-to-end ML pipeline for network security, shipped with CI/CD.",
        "tags": ["Python", "MongoDB", "Scikit-learn", "Docker", "AWS", "GitHub Actions"],
        "description": (
            "An end-to-end pipeline covering data ingestion, schema and "
            "data-drift validation, preprocessing (imputation, RobustScaler, "
            "SMOTETomek), automated model training and evaluation, artifact "
            "tracking, containerisation and AWS deployment through a GitHub "
            "Actions CI/CD workflow."
        ),
        "link": None,
        "link_label": None,
    },
    {
        "id": "PROJ-04",
        "title": "YouTube Creator Growth & Ecosystem Analytics",
        "one_liner": "Benchmarking models to predict subscriber count from channel engagement.",
        "tags": ["Python", "Regression", "Random Forest", "NLTK", "TextBlob"],
        "description": (
            "Analysed 995 top YouTube channels from the Global YouTube "
            "Statistics dataset (28 attributes, cleaned to 554 records / 23 "
            "features). Benchmarked Linear, Ridge, Lasso and Elastic Net "
            "regression against Decision Tree and Random Forest models, and "
            "applied NLTK/TextBlob for NLP, to predict subscriber count from "
            "engagement data."
        ),
        "link": None,
        "link_label": None,
    },
]

ADDITIONAL_PROJECTS = [
    {
        "title": "Movie Review Sentiment Analysis (RNN)",
        "description": (
            "A sentiment-analysis project exploring how review text is turned "
            "into representations suitable for sequence-based deep learning, "
            "using a Recurrent Neural Network to classify reviews as positive "
            "or negative."
        ),
    },
    {
        "title": "Next-Word Prediction (LSTM)",
        "description": (
            "A sequence-modelling project predicting the next word from "
            "preceding context using an LSTM network, with early stopping "
            "used to halt training once validation performance stops improving."
        ),
    },
    {
        "title": "F.R.I.D.A.Y. — this assistant",
        "description": (
            "The chat assistant on this page. Personal mode answers only from "
            "this portfolio's content; Web Search mode is a general "
            "OpenAI-powered assistant with live web search."
        ),
    },
]

EDUCATION = {
    "degree": "B.Tech, Computer Science — Artificial Intelligence & Machine Learning",
    "institution": "SRMIST University",
    "completed": "November 2024",
}

CERTIFICATIONS = [
    "Google Advanced Data Analytics",
    "IBM Data Science",
    "GenAI Apps using Gemini Pro",
    "Stanford Supervised Machine Learning",
    "Meta Version Control",
]

ACHIEVEMENTS = [
    {
        "id": "REC-01",
        "title": "Two SPOT Awards — KPMG India",
        "description": (
            "Recognised twice with KPMG India's SPOT award for contributions "
            "to the team and to client projects."
        ),
        "images": ["assets/spot1.jpeg", "assets/spot2.jpeg"],
    },
    {
        "id": "REC-02",
        "title": "3rd Place — Ubisoft India FindTheLag Contest",
        "description": "Placed third at the Ubisoft India FindTheLag contest, held at IIT Bombay.",
        "images": ["assets/iitbombay.jpg"],
    },
    {
        "id": "REC-03",
        "title": "NCC Airwing Cadet Captain",
        "description": "Served as Cadet Captain in the NCC Airwing.",
        "images": ["assets/ncc.jpg", "assets/ncc_camp_certificate.jpeg"],
    },
]

BOOKS = [
    "The Alchemist — Paulo Coelho",
    "Man's Search for Meaning — Viktor Frankl",
    "The Power of Habit — Charles Duhigg",
    "The 80/20 Principle — Richard Koch",
    "How to Win Friends and Influence People — Dale Carnegie",
    "The 7 Habits of Highly Effective People — Stephen R. Covey",
    "Rework — Jason Fried & David Heinemeier Hansson",
    "The Psychology of Money — Morgan Housel",
]

HOBBIES = ["Cricket", "Football", "Badminton", "Movies", "Music", "Photography", "Travelling"]

GALLERY = [
    {"path": "assets/moon.jpg", "caption": "Moon"},
    {"path": "assets/birds.jpg", "caption": "Birds"},
    {"path": "assets/hallway.jpg", "caption": "Hallway"},
    {"path": "assets/redfort.jpg", "caption": "Red Fort"},
    {"path": "assets/beach.jpg", "caption": "Beach"},
    {"path": "assets/decor.jpg", "caption": "Decor"},
]

SUGGESTED_QUESTIONS_PERSONAL = [
    "What did Sameer do at KPMG?",
    "Tell me about the Network Security project",
    "What's his experience with SQL?",
    "Which project used deep learning?",
]

SUGGESTED_QUESTIONS_WEB = [
    "What does a Data/BI Analyst interview usually cover?",
    "Power BI vs Tableau — what's the real difference?",
    "What's new in data analytics this month?",
]


def _bullets(items):
    return "\n".join(f"- {item}" for item in items)


def build_personal_system_prompt():
    """Assemble F.R.I.D.A.Y.'s (personal-mode) system prompt from the data above."""
    lines = [
        "You are F.R.I.D.A.Y., the personal AI assistant on Sameer Singh's "
        "portfolio site. You represent Sameer to recruiters, hiring managers "
        "and other visitors.",
        "",
        "Rules:",
        "1. Answer ONLY using the portfolio information below. Never invent "
        "employers, titles, results, technologies, certifications, education "
        "or numbers that aren't stated here.",
        "2. If the answer isn't in this context, say so plainly: \"I don't "
        "have that in Sameer's portfolio — you could ask him directly.\"",
        "3. Speak about Sameer in the third person, as his assistant — not as "
        "if you are Sameer.",
        "4. Be concise. Prefer short paragraphs or bullet points over long essays.",
        "",
        "=== PROFILE ===",
        f"Name: {PROFILE['name']}",
        f"Role: {PROFILE['tagline']}",
        f"Experience: {PROFILE['years_experience']}",
        f"Based in: {PROFILE['based_in']}",
        f"{PROFILE['work_location_note']}",
        f"Status: {PROFILE['status']}",
        f"Summary: {PROFILE['summary']}",
        "",
        "=== SKILLS ===",
    ]
    for category, items in SKILLS.items():
        lines.append(f"{category}: {', '.join(items)}")

    lines += ["", "=== EXPERIENCE ==="]
    for job in EXPERIENCE:
        lines.append(f"{job['role']}, {job['company']} ({job['location']}) — {job['dates']}")
        lines.append(_bullets(job["bullets"]))
        lines.append("")

    lines.append("=== PROJECTS ===")
    for p in PROJECTS:
        lines.append(f"{p['title']}: {p['description']}")
        lines.append(f"Technologies: {', '.join(p['tags'])}")
        lines.append("")

    lines.append("=== ADDITIONAL / SIDE PROJECTS ===")
    for p in ADDITIONAL_PROJECTS:
        lines.append(f"{p['title']}: {p['description']}")
    lines.append("")

    lines.append("=== EDUCATION ===")
    lines.append(f"{EDUCATION['degree']}, {EDUCATION['institution']} — completed {EDUCATION['completed']}")
    lines.append("")

    lines.append("=== CERTIFICATIONS ===")
    lines.append(_bullets(CERTIFICATIONS))
    lines.append("")

    lines.append("=== ACHIEVEMENTS ===")
    for a in ACHIEVEMENTS:
        lines.append(f"- {a['title']}: {a['description']}")
    lines.append("")

    lines.append("=== INTERESTS ===")
    lines.append(f"Hobbies: {', '.join(HOBBIES)}")
    lines.append(f"Favourite books: {', '.join(BOOKS)}")
    lines.append("")

    lines.append("=== CONTACT ===")
    lines.append(f"Email: {PROFILE['email']}")
    lines.append(f"GitHub: {PROFILE['github']}")
    lines.append(f"LinkedIn: {PROFILE['linkedin']}")
    lines.append(f"Portfolio: {PROFILE['portfolio']}")

    return "\n".join(lines)


def build_web_system_prompt():
    """Assemble the system prompt for Web Search mode."""
    return (
        "You are F.R.I.D.A.Y. in Web Search mode, on Sameer Singh's portfolio "
        "site. You are a general-purpose assistant with live web search. "
        "Answer accurately and search the web when a question needs current "
        "or factual information you're not certain of. Never pretend to have "
        "searched if you haven't.\n\n"
        "If asked about Sameer specifically, you may draw on the portfolio "
        "context below — but clearly distinguish it from anything found via "
        "web search:\n\n" + build_personal_system_prompt()
    )


PERSONAL_SYSTEM_PROMPT = build_personal_system_prompt()
WEB_SYSTEM_PROMPT = build_web_system_prompt()
