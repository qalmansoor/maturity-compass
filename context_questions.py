# context_questions.py
# Pre-assessment context layer
# Feeds organisational constraints into the report for a contextualised roadmap
# Addresses the "generic 90-day roadmap" criticism

CONTEXT_QUESTIONS = [
    {
        "id": "ctx_budget",
        "text": "What best describes your organisation's current digital transformation budget allocation?",
        "help": "This helps calibrate what is realistic in a 90-day roadmap given your resource constraints.",
        "options": [
            "No dedicated budget — digital initiatives compete with operational spend",
            "Limited budget — under $1M USD allocated to digital/AI annually",
            "Moderate budget — $1M–$10M USD allocated to digital/AI annually",
            "Significant budget — $10M–$50M USD allocated to digital/AI annually",
            "Major programme — over $50M USD committed to digital transformation",
        ],
    },
    {
        "id": "ctx_leadership",
        "text": "Does your organisation currently have a dedicated digital or AI leadership role?",
        "help": "Ownership at the top is the single biggest predictor of transformation success.",
        "options": [
            "No — digital responsibility sits with the CTO or IT Director as a secondary function",
            "A digital champion exists but without a formal mandate or dedicated team",
            "A Chief Digital Officer or equivalent has been appointed but the role is less than 12 months old",
            "A CDO or equivalent has been in post for over 12 months with a funded team",
            "Digital leadership is at C-suite level with board accountability and cross-functional authority",
        ],
    },
    {
        "id": "ctx_barrier",
        "text": "What is the single biggest internal barrier to AI adoption in your organisation right now?",
        "help": "The roadmap will prioritise actions that directly address your stated barrier.",
        "options": [
            "Data quality and availability — our data is not ready for AI",
            "Talent and skills — we do not have the internal capability to build or run AI",
            "Leadership and governance — there is no clear owner or mandate",
            "Change resistance — operational teams do not trust or adopt new tools",
            "Vendor dependency — we are locked into external systems we cannot control",
        ],
    },
    {
        "id": "ctx_timeline",
        "text": "Is there an upcoming milestone that your AI programme needs to align to?",
        "help": "This shapes the urgency and sequencing of the 90-day roadmap.",
        "options": [
            "No specific milestone — we are building at our own pace",
            "Board or leadership review within the next 3 months",
            "Regulatory filing or compliance deadline within the next 6 months",
            "Major contract renewal or vendor negotiation within the next 12 months",
            "Public commitment or national programme reporting deadline (e.g. Vision 2030 KPI)",
        ],
    },
    {
        "id": "ctx_maturity_self",
        "text": "Before completing this assessment, how would you rate your organisation's AI maturity?",
        "help": "We compare your self-perception with your assessed score — the gap is itself a finding.",
        "options": [
            "Early stage — we are just beginning to explore AI",
            "Developing — we have pilots running but nothing at scale",
            "Intermediate — AI is operational in some areas",
            "Advanced — AI is embedded across multiple functions",
            "Leading — AI is core to how we operate and compete",
        ],
        "score_map": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
    },
]

BARRIER_DIMENSION_MAP = {
    "Data quality and availability — our data is not ready for AI":
        "Data & OT Infrastructure Readiness",
    "Talent and skills — we do not have the internal capability to build or run AI":
        "Internal Capability & Ownership",
    "Leadership and governance — there is no clear owner or mandate":
        "Strategic Mandate & Executive Accountability",
    "Change resistance — operational teams do not trust or adopt new tools":
        "Operational Credibility of the AI Programme",
    "Vendor dependency — we are locked into external systems we cannot control":
        "Internal Capability & Ownership",
}
