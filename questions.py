# questions.py
# AI Maturity Compass — Assessment Questions
#
# Framework: Gartner AI Maturity Model (7 pillars), consolidated and
# reframed around GCC energy execution reality across 5 dimensions.
#
# Each dimension uses a consistent 5-question logic:
#   Q1 — Current State: Where are you today
#   Q2 — Accountability: Who owns this and what happens if it fails
#   Q3 — Dependency: Internal capability vs external reliance
#   Q4 — Translation: Does it connect to operational reality on the ground
#   Q5 — Evidence: Can you point to a specific proof point

DIMENSIONS = [
    "Strategic Mandate & Executive Accountability",
    "Data & OT Infrastructure Readiness",
    "Operational Credibility of the AI Programme",
    "Internal Capability & Ownership",
    "Value Realisation Discipline",
]

DIMENSION_SUBTITLES = {
    "Strategic Mandate & Executive Accountability":
        "Is there someone whose career depends on AI delivering value — or is this a strategy exercise?",
    "Data & OT Infrastructure Readiness":
        "Can you actually feed an AI system with the operational data it needs from your plant floor?",
    "Operational Credibility of the AI Programme":
        "Do the people leading AI understand the domain well enough that field teams will trust and adopt it?",
    "Internal Capability & Ownership":
        "When the external consultant leaves, does the capability stay — or does it leave with them?",
    "Value Realisation Discipline":
        "Can you point to a specific operational outcome that changed because of AI — not a pilot, an outcome?",
}

DIMENSION_ICONS = {
    "Strategic Mandate & Executive Accountability": "🎯",
    "Data & OT Infrastructure Readiness": "🏭",
    "Operational Credibility of the AI Programme": "⚙️",
    "Internal Capability & Ownership": "🧠",
    "Value Realisation Discipline": "📊",
}

QUESTIONS = {
    "Strategic Mandate & Executive Accountability": [
        {
            "id": "sv1",
            "type": "Current State",
            "text": "How would you describe the current status of your organisation's AI strategy?",
            "options": [
                ("No formal AI strategy exists — discussions are informal and ad hoc", 1),
                ("An AI strategy has been drafted but not formally approved or funded", 2),
                ("A board-approved AI strategy exists with defined priorities and budget allocation", 3),
                ("Our AI strategy is reviewed quarterly with executive accountability for delivery", 4),
                ("AI investment decisions are made at board level with measurable ROI targets and personal accountability", 5),
            ],
        },
        {
            "id": "sv2",
            "type": "Accountability",
            "text": "If your AI programme failed to deliver value this year, who would be held accountable?",
            "options": [
                ("No one — there is no named owner for AI outcomes", 1),
                ("The IT department would likely take responsibility", 2),
                ("A Chief Digital Officer or equivalent holds nominal accountability", 3),
                ("A named executive has AI delivery targets embedded in their performance review", 4),
                ("Multiple executives across business units have AI value targets — failure has career consequences", 5),
            ],
        },
        {
            "id": "sv3",
            "type": "Dependency",
            "text": "Who is primarily driving your AI agenda?",
            "options": [
                ("External consultants or vendors are setting our AI direction", 1),
                ("A mix of external advisors and internal staff — but external firms lead", 2),
                ("Internal team leads with occasional external advisory support", 3),
                ("Fully internal leadership — external firms execute, not advise", 4),
                ("Internal capability is the default; external partners are used for specialist execution only", 5),
            ],
        },
        {
            "id": "sv4",
            "type": "Translation",
            "text": "How connected is your AI strategy to the specific operational challenges of your assets and business units?",
            "options": [
                ("AI strategy is high-level — no connection to specific asset or operational problems", 1),
                ("Some use cases are identified but not tied to operational KPIs", 2),
                ("Priority use cases are mapped to specific operational problems with defined owners", 3),
                ("Every AI initiative has a named operational sponsor who defines the problem and validates the outcome", 4),
                ("AI roadmap is co-created with operations, finance, and engineering — not handed down from strategy", 5),
            ],
        },
        {
            "id": "sv5",
            "type": "Evidence",
            "text": "Can your organisation point to a specific AI initiative that changed a board-level decision in the last 24 months?",
            "options": [
                ("No — AI has not influenced board-level decisions", 1),
                ("AI has informed some management decisions but not at board level", 2),
                ("One or two instances where AI analysis influenced a significant business decision", 3),
                ("AI-generated insights are regularly presented at board level and influence capital allocation", 4),
                ("AI is a standard input to board decisions — investment, operations, and risk discussions are AI-informed", 5),
            ],
        },
    ],

    "Data & OT Infrastructure Readiness": [
        {
            "id": "de1",
            "type": "Current State",
            "text": "How would you describe the availability and quality of operational data across your assets?",
            "options": [
                ("Data is siloed by site and system — no central access or consistent quality", 1),
                ("Some data is centralised but completeness and quality vary significantly by site", 2),
                ("Key operational datasets are centralised, documented, and accessible to analytics teams", 3),
                ("OT and IT data streams are integrated with near real-time access and governed quality standards", 4),
                ("A unified industrial data platform operates across all assets with automated quality monitoring", 5),
            ],
        },
        {
            "id": "de2",
            "type": "Accountability",
            "text": "Who owns data quality in your organisation?",
            "options": [
                ("No one — data quality is not formally owned", 1),
                ("IT manages data infrastructure but business teams own quality inconsistently", 2),
                ("A data governance committee exists but enforcement is inconsistent", 3),
                ("Named data owners exist per domain with accountability for quality and completeness", 4),
                ("Data ownership is embedded in operational roles — plant managers are accountable for OT data quality", 5),
            ],
        },
        {
            "id": "de3",
            "type": "Dependency",
            "text": "If your primary technology vendor was replaced tomorrow, how much of your data infrastructure would remain intact?",
            "options": [
                ("Most of our data capability is vendor-dependent — switching would cause significant disruption", 1),
                ("Core systems are vendor-dependent but some internal capability exists", 2),
                ("Internal data pipelines exist alongside vendor systems — transition would be manageable", 3),
                ("Data architecture is vendor-agnostic by design — internal teams own the pipelines", 4),
                ("Fully portable data infrastructure — vendor independence is a governance requirement", 5),
            ],
        },
        {
            "id": "de4",
            "type": "Translation",
            "text": "How well does your data infrastructure reflect the operational reality of your assets — shift patterns, maintenance cycles, OT sensor data?",
            "options": [
                ("OT data is largely uncaptured or inaccessible for analytics purposes", 1),
                ("Some OT data is captured but not integrated with IT systems or analytics platforms", 2),
                ("OT data is integrated into analytics for specific use cases — not enterprise-wide", 3),
                ("OT/IT convergence is complete for priority asset classes with real-time feeds to analytics", 4),
                ("Comprehensive OT data integration including edge computing at site level — no data blind spots", 5),
            ],
        },
        {
            "id": "de5",
            "type": "Evidence",
            "text": "Can you point to a specific operational decision in the last 12 months that was made better because of data your organisation collected and analysed internally?",
            "options": [
                ("No — we cannot point to a specific data-driven operational decision", 1),
                ("Informal examples exist but they are not documented or repeatable", 2),
                ("One or two documented cases where internal data analysis improved an operational decision", 3),
                ("Multiple documented cases across different asset types and business functions", 4),
                ("Data-driven decision making is standard operating procedure — exceptions are documented and reviewed", 5),
            ],
        },
    ],

    "Operational Credibility of the AI Programme": [
        {
            "id": "oc1",
            "type": "Current State",
            "text": "What is the primary background of the people leading your AI and digital transformation programme?",
            "options": [
                ("Primarily external technology consultants with limited energy sector experience", 1),
                ("Mix of technology specialists and some energy professionals — technology leads", 2),
                ("Energy professionals with digital upskilling — domain knowledge is the foundation", 3),
                ("Dedicated digital transformation roles filled by people with both energy and AI credentials", 4),
                ("AI programme is led by energy operators who have built digital capability — not the reverse", 5),
            ],
        },
        {
            "id": "oc2",
            "type": "Accountability",
            "text": "When an AI recommendation conflicts with the judgment of an experienced field engineer or plant manager, what happens?",
            "options": [
                ("The AI recommendation is ignored — field judgment always overrides by default", 1),
                ("Conflict is escalated to management with no structured resolution process", 2),
                ("A review process exists but resolution depends on individual relationships", 3),
                ("Structured escalation with documented outcomes — learnings feed back into model improvement", 4),
                ("Conflicts are treated as model improvement opportunities — field engineers are formal contributors to AI validation", 5),
            ],
        },
        {
            "id": "oc3",
            "type": "Dependency",
            "text": "How reliant is your AI programme on individuals with specific technical expertise that the organisation does not formally own?",
            "options": [
                ("Highly reliant — if 2–3 people left, the programme would stall", 1),
                ("Moderate reliance on key individuals — some knowledge transfer has occurred", 2),
                ("Knowledge is documented and partially distributed — key person risk is reducing", 3),
                ("Structured knowledge transfer programme in place — no single point of failure in the AI team", 4),
                ("AI capability is institutionalised — no individual dependency; processes and tools carry the knowledge", 5),
            ],
        },
        {
            "id": "oc4",
            "type": "Translation",
            "text": "How often do your AI and digital teams spend time on-site at operating assets — plant floors, control rooms, field operations?",
            "options": [
                ("Rarely or never — digital teams work remotely or from headquarters", 1),
                ("Occasional site visits for specific project milestones only", 2),
                ("Regular site engagement for active projects — but not systematic across the portfolio", 3),
                ("Structured site engagement programme — digital team members have scheduled operational rotations", 4),
                ("Digital and operations teams are co-located for active programmes — no separation between digital and field", 5),
            ],
        },
        {
            "id": "oc5",
            "type": "Evidence",
            "text": "Can you point to an AI initiative that was adopted and sustained by field operations teams — not just piloted and handed over?",
            "options": [
                ("No sustained field adoption — pilots have not converted to operational use", 1),
                ("One example of field adoption but it required significant ongoing external support", 2),
                ("Two or three examples of field adoption with partial self-sufficiency", 3),
                ("Multiple examples of field-led AI adoption where operations teams own the tool", 4),
                ("Field teams independently request, configure, and iterate on AI tools — adoption is pull, not push", 5),
            ],
        },
    ],

    "Internal Capability & Ownership": [
        {
            "id": "ic1",
            "type": "Current State",
            "text": "How would you describe your organisation's internal AI and data science capability?",
            "options": [
                ("No internal AI capability — all digital work is done by external vendors or consultants", 1),
                ("Small internal team exists but relies heavily on external support for delivery", 2),
                ("Internal team can deliver defined use cases independently but depends on vendors for new capability", 3),
                ("Strong internal team with full-cycle capability — ideation, build, deploy, and maintain", 4),
                ("Internal AI capability is a competitive asset — we build for our own operations and could advise others", 5),
            ],
        },
        {
            "id": "ic2",
            "type": "Accountability",
            "text": "When an externally-built AI solution requires maintenance, updates, or troubleshooting, who handles it?",
            "options": [
                ("The external vendor entirely — we have no internal capability to maintain AI systems", 1),
                ("Primarily the vendor with limited internal involvement", 2),
                ("Shared maintenance — internal and external teams co-maintain", 3),
                ("Primarily internal — vendor is on standby for major issues only", 4),
                ("Fully internal — vendor dependency has been deliberately eliminated post-deployment", 5),
            ],
        },
        {
            "id": "ic3",
            "type": "Dependency",
            "text": "What proportion of your active AI use cases could your internal team maintain and improve without external support?",
            "options": [
                ("Less than 20% — we are heavily vendor-dependent across our portfolio", 1),
                ("20–40% — significant external dependency remains", 2),
                ("40–60% — roughly equal internal and external capability", 3),
                ("60–80% — internal capability is the default; external used for frontier work only", 4),
                ("More than 80% — internal ownership is a strategic requirement, not just an aspiration", 5),
            ],
        },
        {
            "id": "ic4",
            "type": "Translation",
            "text": "How effectively does your AI capability development programme build skills in local national talent specifically?",
            "options": [
                ("No structured capability development programme for national talent in AI roles", 1),
                ("Ad hoc training exists — no structured pipeline or localisation target for digital roles", 2),
                ("Localisation targets exist for digital roles but are not consistently met", 3),
                ("Active programme with measurable progress in placing nationals in AI and data roles", 4),
                ("National talent leads the AI programme at all levels — localisation in digital is a board KPI", 5),
            ],
        },
        {
            "id": "ic5",
            "type": "Evidence",
            "text": "Can you point to an AI solution that was built entirely by your internal team — from problem definition to production deployment?",
            "options": [
                ("No — all production AI solutions have been built by external parties", 1),
                ("One partial example — internal team contributed but external vendor led", 2),
                ("Two or three examples of internally-built solutions in limited production", 3),
                ("Multiple examples of fully internal builds across different operational domains", 4),
                ("Internal builds are the standard — external vendors are the exception, not the rule", 5),
            ],
        },
    ],

    "Value Realisation Discipline": [
        {
            "id": "vr1",
            "type": "Current State",
            "text": "How many AI use cases are currently in sustained production — not pilots, not proofs of concept?",
            "options": [
                ("Zero — we have no AI in sustained production", 1),
                ("1–5 use cases in production with inconsistent performance tracking", 2),
                ("6–15 use cases in production with basic performance monitoring", 3),
                ("16–40 use cases in production with structured value tracking", 4),
                ("40+ use cases in production — AI is a normal part of operational infrastructure", 5),
            ],
        },
        {
            "id": "vr2",
            "type": "Accountability",
            "text": "Who is responsible for proving that an AI initiative delivered the value it promised?",
            "options": [
                ("No one — value measurement is not formally owned", 1),
                ("The technology or digital team tracks usage metrics but not business outcomes", 2),
                ("Project managers track delivery milestones — business value is assessed informally", 3),
                ("Named business owners are accountable for value realisation with defined KPIs", 4),
                ("A formal value realisation function tracks every AI initiative against promised outcomes — underperformance triggers review", 5),
            ],
        },
        {
            "id": "vr3",
            "type": "Dependency",
            "text": "How dependent is your value measurement on the continued involvement of the team that built the AI solution?",
            "options": [
                ("Entirely dependent — only the build team knows how to interpret the outputs", 1),
                ("Mostly dependent — some documentation exists but understanding is concentrated", 2),
                ("Partial dependency — operational teams understand the tool but rely on build team for analysis", 3),
                ("Operational teams own value measurement — build team involvement is optional", 4),
                ("Value measurement is fully embedded in operational KPIs — no dependency on the AI build team", 5),
            ],
        },
        {
            "id": "vr4",
            "type": "Translation",
            "text": "How well do your AI value metrics connect to outcomes that operational and financial leadership actually care about — availability, heat rate, cost per MWh, revenue?",
            "options": [
                ("AI metrics are technical — model uptime, prediction accuracy — not operational outcomes", 1),
                ("Some connection to operational metrics but financial impact is not calculated", 2),
                ("Operational and financial impact is estimated for major use cases", 3),
                ("Every production AI use case has a defined operational and financial KPI reviewed by leadership", 4),
                ("AI value is reported in the same language as financial results — cost per MWh, availability %, SAR impact", 5),
            ],
        },
        {
            "id": "vr5",
            "type": "Evidence",
            "text": "Can your organisation point to a specific, quantified operational improvement — with a number attached — that AI delivered in the last 24 months?",
            "options": [
                ("No — we cannot quantify AI's operational impact", 1),
                ("Qualitative improvements are described but no numbers are attached", 2),
                ("One or two quantified examples exist but they are not regularly reported", 3),
                ("Multiple quantified examples are documented and shared with leadership quarterly", 4),
                ("AI value is reported at board level with SAR or operational metric impact — comparable to capex reporting", 5),
            ],
        },
    ],
}

MATURITY_LEVELS = {
    1: {
        "label": "Digital Laggard",
        "gartner": "Foundational",
        "range": (1.0, 1.8),
        "description": "AI activity is largely absent or exploratory. No formal strategy, fragmented data, and limited executive engagement. The organisation is at significant risk of falling behind GCC peers as the region accelerates toward AI-native operations.",
        "colour": "#EF4444",
        "icon": "🔴",
    },
    2: {
        "label": "Pilot Stage",
        "gartner": "Emerging",
        "range": (1.8, 2.6),
        "description": "Early experiments exist but results are inconsistent. AI sits in pockets rather than the enterprise. The common trap at this level: deploying technology without fixing the underlying accountability, data, and capability gaps first.",
        "colour": "#F97316",
        "icon": "🟠",
    },
    3: {
        "label": "Emerging Operator",
        "gartner": "Operational",
        "range": (2.6, 3.4),
        "description": "AI is operational in defined areas with structured ownership and measurable outcomes. Foundational capability is in place but the organisation has not yet scaled across functions or achieved enterprise-wide value realisation.",
        "colour": "#EAB308",
        "icon": "🟡",
    },
    4: {
        "label": "Scaling Practitioner",
        "gartner": "Scaled",
        "range": (3.4, 4.2),
        "description": "AI is embedded across multiple functions with board-level visibility and measurable ROI. The organisation is deploying at scale and building genuine competitive differentiation through operational intelligence.",
        "colour": "#22C55E",
        "icon": "🟢",
    },
    5: {
        "label": "AI-Native Enterprise",
        "gartner": "Transformational",
        "range": (4.2, 5.01),
        "description": "AI is business DNA. Decisions across operations, finance, and strategy are AI-augmented by default. The organisation serves as a regional benchmark and actively shapes the GCC AI ecosystem.",
        "colour": "#06B6D4",
        "icon": "🔵",
    },
}


def get_maturity_level(score: float) -> dict:
    for level, data in MATURITY_LEVELS.items():
        low, high = data["range"]
        if low <= score < high:
            return {**data, "level": level}
    return {**MATURITY_LEVELS[5], "level": 5}
