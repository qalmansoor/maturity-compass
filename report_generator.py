# report_generator.py
# Consulting-grade AI maturity report generator
# Uses context layer, consistency flags, and self-perception gap
# as additional diagnostic inputs beyond dimension scores

import anthropic
import os
from assessor import get_score_label

# ── GCC ENERGY SECTOR BENCHMARKS ──
# Based on published sources: Gartner 2025, KPMG GCC Digital Maturity 2024,
# McKinsey Middle East Digital Report 2024, Aramco AI disclosures 2025,
# ACWA Power AR 2023, DEWA Annual Report 2025
# NOTE: These are indicative benchmarks from public disclosures,
# not a proprietary survey dataset. Stated as such in all outputs.

SECTOR_BENCHMARKS = {
    "Power Generation": {
        "gcc_median": 2.3,
        "gcc_leaders": ["Saudi Electricity Company (SEC)", "ACWA Power", "DEWA"],
        "leader_score_estimate": "3.8–4.2",
        "primary_kpis": [
            "Availability Factor (%)",
            "Heat Rate (BTU/kWh)",
            "Forced Outage Rate (%)",
            "O&M Cost per MWh (SAR)",
            "Predictive Maintenance Coverage (%)",
        ],
        "key_use_cases": [
            "Predictive maintenance on gas turbines",
            "Heat rate optimisation",
            "Outage risk scoring",
            "LTSA performance compliance monitoring",
            "Shift handover AI summaries",
        ],
        "gcc_context": (
            "ACWA Power deployed Azure AI and Power BI predictive maintenance "
            "across 90 assets in 14 countries by 2023. SEC is actively deploying "
            "AI under the national digital infrastructure mandate. DEWA deployed "
            "Microsoft 365 Copilot Cowork across all operations in 2026, becoming "
            "the first UAE government entity with full agentic AI deployment."
        ),
        "transformation_risk": (
            "The most common failure in Saudi power generation AI programmes: "
            "digital teams that cannot speak LTSA contractual language or interpret "
            "DCS historian data are unable to build trust with plant operations teams. "
            "Field adoption stalls not because the technology is wrong but because "
            "the people deploying it have no operational credibility."
        ),
    },
    "Oil & Gas Upstream": {
        "gcc_median": 3.1,
        "gcc_leaders": ["Saudi Aramco", "ADNOC"],
        "leader_score_estimate": "4.5–5.0",
        "primary_kpis": [
            "Production Efficiency (%)",
            "Drilling Cost per Well ($)",
            "Unplanned Downtime (hours)",
            "HSE Incident Rate",
            "Reservoir Recovery Factor (%)",
        ],
        "key_use_cases": [
            "Drilling parameter optimisation",
            "Reservoir simulation augmentation",
            "Predictive equipment failure on wellheads",
            "HSE anomaly detection",
            "Production forecasting",
        ],
        "gcc_context": (
            "Saudi Aramco achieved $1.8Bn in AI-driven technology value in 2024 "
            "with 442 use cases identified and 200+ deployed. ADNOC has embedded "
            "AI across upstream operations with a dedicated AI Centre of Excellence. "
            "Upstream AI maturity in the GCC is the highest of any energy sub-sector "
            "due to the scale of national champion investment."
        ),
        "transformation_risk": (
            "Data sovereignty is the defining constraint in GCC upstream AI. "
            "Reservoir and production data is classified at the national level in "
            "Saudi Arabia and the UAE. Any AI programme that requires sending "
            "operational data to cloud platforms outside the region faces regulatory "
            "and security blockers that generic global frameworks do not anticipate."
        ),
    },
    "Oil & Gas Downstream": {
        "gcc_median": 2.7,
        "gcc_leaders": ["SABIC", "ADNOC Refining"],
        "leader_score_estimate": "3.5–4.0",
        "primary_kpis": [
            "Refinery Utilisation Rate (%)",
            "Energy Intensity (GJ/tonne)",
            "Product Quality Compliance (%)",
            "Unplanned Shutdown Frequency",
            "Margin per Barrel ($)",
        ],
        "key_use_cases": [
            "Process optimisation in refining units",
            "Energy consumption forecasting",
            "Quality prediction in product streams",
            "Rotating equipment health monitoring",
            "Supply chain and logistics optimisation",
        ],
        "gcc_context": (
            "SABIC and ADNOC Refining have both invested in process AI through "
            "partnerships with AspenTech and Honeywell. Downstream AI maturity "
            "is driven by energy efficiency mandates — Saudi Arabia's National "
            "Energy Efficiency Programme creates regulatory pressure to prove "
            "AI-driven consumption reduction."
        ),
        "transformation_risk": (
            "Downstream AI programmes frequently stall at the process engineer level. "
            "Operators who have run the same process configuration for 15 years "
            "treat AI recommendations as interference, not assistance. "
            "Change management in refinery environments requires a fundamentally "
            "different approach to field adoption than office-based digital programmes."
        ),
    },
    "Renewables": {
        "gcc_median": 2.5,
        "gcc_leaders": ["ACWA Power", "Masdar", "NEOM Energy"],
        "leader_score_estimate": "3.5–4.2",
        "primary_kpis": [
            "Capacity Factor (%)",
            "Levelised Cost of Energy (LCOE)",
            "Grid Availability (%)",
            "O&M Cost per MWh",
            "CO2 Avoided (tonnes/year)",
        ],
        "key_use_cases": [
            "Solar irradiance forecasting",
            "Wind power production optimisation",
            "Battery storage dispatch optimisation",
            "Drone-based panel inspection with AI defect detection",
            "Grid integration and curtailment management",
        ],
        "gcc_context": (
            "The GCC renewables sector is nascent compared to upstream oil and gas "
            "but growing rapidly. NEOM's energy system is designed AI-native from "
            "the outset. ACWA Power's renewables portfolio is the most advanced in "
            "terms of AI-assisted O&M. Saudi Arabia's target of 50% renewables "
            "by 2030 creates urgency to build AI capability fast."
        ),
        "transformation_risk": (
            "Renewables AI programmes in the GCC face a talent gap that is more "
            "acute than in thermal generation. The combination of grid integration "
            "expertise, solar irradiance modelling, and AI engineering is rare. "
            "Organisations that outsource all three to a single EPC or O&M contractor "
            "are building zero internal capability — a liability as the portfolio scales."
        ),
    },
    "Water & Desalination": {
        "gcc_median": 2.2,
        "gcc_leaders": ["ACWA Power Water", "DEWA Water", "SWCC"],
        "leader_score_estimate": "3.2–3.8",
        "primary_kpis": [
            "Specific Energy Consumption (kWh/m³)",
            "Plant Availability (%)",
            "Water Quality Compliance (%)",
            "Chemical Consumption (kg/m³)",
            "Brine Disposal Cost",
        ],
        "key_use_cases": [
            "Membrane fouling prediction",
            "Energy optimisation in RO and MSF processes",
            "Chemical dosing optimisation",
            "Plant availability forecasting",
            "Brine management AI",
        ],
        "gcc_context": (
            "Water security is a strategic priority across all GCC nations. "
            "SWCC in Saudi Arabia and DEWA in the UAE are both under government "
            "mandate to reduce specific energy consumption in desalination. "
            "AI adoption in water is earlier-stage than power but investment "
            "is accelerating given the national security dimension of water supply."
        ),
        "transformation_risk": (
            "Water and desalination AI programmes face the most acute OT/IT "
            "integration challenge in the GCC energy sector. Process control "
            "systems in desalination plants are often proprietary, with vendors "
            "restricting data access for competitive reasons. "
            "Programmes that do not resolve the data access question before "
            "building AI capability will consistently fail to deploy at scale."
        ),
    },
    "Transmission & Distribution": {
        "gcc_median": 2.4,
        "gcc_leaders": ["SEC T&D Division", "TRANSCO UAE", "Kahramaa"],
        "leader_score_estimate": "3.4–3.9",
        "primary_kpis": [
            "System Average Interruption Duration Index (SAIDI)",
            "System Average Interruption Frequency Index (SAIFI)",
            "Technical Losses (%)",
            "Asset Utilisation (%)",
            "Fault Detection Response Time (minutes)",
        ],
        "key_use_cases": [
            "Predictive fault detection on HV assets",
            "Load forecasting for grid balancing",
            "Asset health indexing for capex prioritisation",
            "Vegetation management AI with satellite imagery",
            "Customer interruption prediction and pre-emptive response",
        ],
        "gcc_context": (
            "SEC's T&D division is the largest grid operator in the GCC and is "
            "actively deploying AI for fault prediction and load management. "
            "UAE grid operators benefit from smaller, more integrated networks "
            "that are easier to instrument. The GCC grid interconnection project "
            "is creating new requirements for cross-border AI-assisted dispatch."
        ),
        "transformation_risk": (
            "T&D AI programmes face a unique governance challenge: grid reliability "
            "is a public safety obligation. Any AI recommendation that affects "
            "switching decisions or load shedding requires a level of regulatory "
            "validation that slows deployment significantly. Programmes that treat "
            "T&D the same as industrial AI consistently underestimate the approval "
            "cycles required before field deployment."
        ),
    },
    "Energy Holding / Conglomerate": {
        "gcc_median": 2.8,
        "gcc_leaders": ["Saudi Aramco", "ADNOC Group", "ACWA Power"],
        "leader_score_estimate": "3.8–4.5",
        "primary_kpis": [
            "Portfolio AI Use Case Coverage (%)",
            "Cross-subsidiary Data Integration (%)",
            "AI Programme ROI ($M)",
            "Digital Capability Index (internal)",
            "National AI Programme Contribution",
        ],
        "key_use_cases": [
            "Group-wide AI use case prioritisation and governance",
            "Cross-subsidiary data platform",
            "Portfolio performance AI dashboards",
            "Shared AI services for operating companies",
            "National programme reporting and compliance",
        ],
        "gcc_context": (
            "GCC energy conglomerates face a unique challenge: building group-level "
            "AI capability while managing operating companies at different maturity "
            "levels. Aramco's model — 442 identified use cases, 200+ deployed, "
            "shared digital services through Aramco Digital — is the reference case "
            "for how a GCC conglomerate can systematise AI at scale."
        ),
        "transformation_risk": (
            "Conglomerate AI programmes that are managed centrally without "
            "operating company buy-in consistently fail. The most dangerous pattern: "
            "a group CDO builds a strategy, creates a centre of excellence, and "
            "mandates adoption — but operating company CEOs see it as overhead, "
            "not value. The translation layer between group strategy and subsidiary "
            "execution is where GCC conglomerate digital programmes most commonly stall."
        ),
    },
    "Other Energy": {
        "gcc_median": 2.4,
        "gcc_leaders": ["Sector leaders vary"],
        "leader_score_estimate": "3.2–4.0",
        "primary_kpis": [
            "Operational Efficiency KPIs",
            "AI Use Cases in Production",
            "Internal Capability Index",
            "Value Realisation ($ or SAR impact)",
        ],
        "key_use_cases": [
            "Asset performance management",
            "Predictive maintenance",
            "Operational data analytics",
            "Process optimisation",
            "Workforce productivity tools",
        ],
        "gcc_context": (
            "GCC energy organisations across all sub-sectors are under increasing "
            "pressure to demonstrate AI value as Vision 2030 and equivalent national "
            "programmes enter their execution phase. The window for building "
            "internal capability before being locked into vendor dependency is narrowing."
        ),
        "transformation_risk": (
            "Organisations without a clearly defined sector benchmark risk "
            "benchmarking themselves against global averages that do not reflect "
            "GCC operational realities. The translation gap between global AI "
            "frameworks and GCC execution context is the primary risk to "
            "value realisation across all energy sub-sectors."
        ),
    },
}


def generate_report(
    org_name: str,
    org_sector: str,
    org_country: str,
    dimension_scores: dict,
    overall_score: float,
    maturity_level: dict,
    type_averages: dict,
    consistency_flags: dict = None,
    self_perception_gap: dict = None,
    context_responses: dict = None,
) -> str:

    # Get sector benchmark data
    benchmark = SECTOR_BENCHMARKS.get(org_sector, SECTOR_BENCHMARKS["Other Energy"])
    gcc_median = benchmark["gcc_median"]
    gap_to_median = round(overall_score - gcc_median, 2)
    gap_to_leaders = benchmark["leader_score_estimate"]

    dim_summary = "\n".join([
        f"- {dim}: {score}/5.0 ({get_score_label(score)})"
        for dim, score in dimension_scores.items()
    ])

    sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1])
    weakest_type = min(type_averages.items(), key=lambda x: x[1]) if type_averages else ("Unknown", 0)
    strongest_type = max(type_averages.items(), key=lambda x: x[1]) if type_averages else ("Unknown", 0)

    # Build consistency flags summary
    consistency_summary = ""
    if consistency_flags:
        flagged = [
            f"- {dim}: {data['interpretation']}"
            for dim, data in consistency_flags.items()
            if data.get("flagged")
        ]
        if flagged:
            consistency_summary = (
                "CONSISTENCY FLAGS — ANSWERS INTERNALLY CONTRADICTORY IN THESE DIMENSIONS:\n"
                + "\n".join(flagged)
                + "\nThese flags indicate the self-reported score may not reflect operational "
                "reality. Surface these specifically in Section 2."
            )
        else:
            consistency_summary = "No significant answer inconsistencies detected across dimensions."

    # Build self-perception gap summary
    perception_summary = ""
    if self_perception_gap and self_perception_gap.get("gap") is not None:
        direction = self_perception_gap["direction"]
        gap_val = abs(self_perception_gap["gap"])
        perceived = self_perception_gap["perceived_score"]
        perception_summary = (
            f"SELF-PERCEPTION GAP:\n"
            f"Respondent self-rated at {perceived}/5.0 before assessment. "
            f"Assessed score: {overall_score}/5.0. "
            f"Gap: {self_perception_gap['gap']} ({direction}). "
            f"{self_perception_gap['interpretation']}"
        )

    # Build context summary
    context_summary = ""
    if context_responses:
        budget = context_responses.get("ctx_budget", "Not provided")
        leadership = context_responses.get("ctx_leadership", "Not provided")
        barrier = context_responses.get("ctx_barrier", "Not provided")
        timeline = context_responses.get("ctx_timeline", "Not provided")
        context_summary = f"""
ORGANISATIONAL CONTEXT (use to personalise the 90-day roadmap):
- Budget level: {budget}
- Digital leadership: {leadership}
- Stated primary barrier: {barrier}
- Upcoming milestone: {timeline}

The 90-day roadmap MUST be calibrated to these constraints.
If budget is limited, prioritise zero or low-cost actions.
If no CDO exists, the first recommendation must address leadership accountability.
If the stated barrier is data quality, Phase 1 must start there.
If there is an upcoming board review or Vision 2030 milestone, sequence the roadmap
so Phase 1 produces something presentable by that date.
"""

    prompt = f"""You are a senior digital transformation consultant at Aramco Digital's consulting practice.
You have just completed a structured AI maturity assessment with a client executive.

CRITICAL FRAMING:
The biggest failure of global consulting firms in GCC AI transformation is the translation gap:
producing strategy documents that ignore how decisions get made on the ground, building capability
in external consultants rather than internal teams, and declaring success at pilot stage before
value has been realised at operational scale.

Your report must NOT read like a generic McKinsey or BCG output.
Every paragraph must reflect GCC energy execution reality.
Every recommendation must be specific enough to assign to a named role on Monday morning.
If you write something that could apply to any company in any country, rewrite it.

═══════════════════════════════════════════════════
CLIENT PROFILE
═══════════════════════════════════════════════════
Organisation: {org_name}
Sector: {org_sector}
Country / Region: {org_country}

═══════════════════════════════════════════════════
ASSESSMENT RESULTS
═══════════════════════════════════════════════════
Overall Score: {overall_score}/5.0
Maturity Level: {maturity_level['label']} (Level {maturity_level['level']} of 5)
Gartner Equivalent: {maturity_level['gartner']}

DIMENSION SCORES:
{dim_summary}

QUESTION-TYPE PATTERN:
Weakest type: {weakest_type[0]} (avg {weakest_type[1]}/5.0)
Strongest type: {strongest_type[0]} (avg {strongest_type[1]}/5.0)

{consistency_summary}

{perception_summary}

═══════════════════════════════════════════════════
SECTOR BENCHMARK DATA
═══════════════════════════════════════════════════
Sector: {org_sector}
GCC Sector Median (indicative, based on public disclosures): {gcc_median}/5.0
Gap to GCC median: {gap_to_median:+.2f} points
GCC sector leaders: {", ".join(benchmark["gcc_leaders"])}
Estimated leader score range: {gap_to_leaders}/5.0

Sector-specific KPIs to reference in roadmap:
{chr(10).join("- " + kpi for kpi in benchmark["primary_kpis"])}

High-value use cases for this sector:
{chr(10).join("- " + uc for uc in benchmark["key_use_cases"])}

GCC sector context:
{benchmark["gcc_context"]}

Sector-specific transformation risk:
{benchmark["transformation_risk"]}

BENCHMARK TRANSPARENCY NOTE:
These benchmarks are indicative, derived from publicly available disclosures
(Gartner 2025, KPMG GCC Digital Maturity 2024, company annual reports and press releases).
They are not based on a proprietary survey dataset. Present them as directional context,
not precise measurements. State this explicitly in the report.

{context_summary}

═══════════════════════════════════════════════════
REPORT STRUCTURE
═══════════════════════════════════════════════════

---
## AI MATURITY ASSESSMENT REPORT

**Client:** {org_name} | **Sector:** {org_sector} | **Region:** {org_country} | **Overall Score:** {overall_score} / 5.0 — {maturity_level['label']}

---

### 1. EXECUTIVE SUMMARY
3–4 sentences maximum. Direct and specific.
- State the maturity level and what it means operationally for this sector
- Name the one strength and one critical gap
- If a self-perception gap exists, reference it directly — this is important signal
- End with the 90-day strategic imperative and why the timing matters now

### 2. WHAT YOUR SCORES REVEAL
2–3 paragraphs. Interpret, do not describe.
- Use the question-type pattern to diagnose the underlying dynamic
- If consistency flags exist, name them directly: "Your answers in [dimension] are
  internally contradictory — this itself is a finding that warrants attention"
- Reference the sector transformation risk specific to {org_sector}
- Name where this organisation is most likely to stall between strategy and execution
- Do not simply restate the scores — tell the reader what the pattern means

### 3. THE THREE GAPS THAT MATTER MOST
Ranked by urgency. For each:
**Gap [N] — [Dimension Name]**
**The real problem:** One sentence naming the underlying organisational issue
**Why it stalls here:** The specific GCC {org_sector} execution reason — not generic
**The action:** One specific, owner-assignable action that can begin this week

### 4. PRIORITISED 90-DAY ROADMAP
CRITICAL: This roadmap must be calibrated to the organisational context provided.
Honour the budget level, leadership situation, stated barrier, and any upcoming milestone.

**Phase 1 — Days 1–30: [Name this phase based on what's most urgent]**
2–3 specific actions. If there is no CDO, action 1 must be leadership accountability.
If data is the stated barrier, action 1 must be a data diagnostic.

**Phase 2 — Days 31–60: [Name this phase]**
Deploy one use case that produces a measurable outcome in {org_sector} operational terms.
Name the specific use case from the sector list above. Name the KPI it moves.

**Phase 3 — Days 61–90: [Name this phase]**
Institutionalise. Build internal ownership. Define the value measurement framework.
Name the specific {org_sector} KPI that will be reported to leadership at Day 90.

### 5. BENCHMARK: WHERE YOU STAND IN THE GCC
One honest paragraph.
- State the gap to GCC median ({gcc_median}/5.0) and what it means in execution terms
- Reference what {", ".join(benchmark["gcc_leaders"][:2])} have achieved specifically
- Be honest about the recovery timeline — do not be vague
- Close with one sentence on the window of opportunity before the gap becomes structural

---
*Benchmarks are indicative, derived from publicly available GCC energy AI disclosures
(Gartner 2025, KPMG GCC Digital Maturity 2024, company annual reports).
Not based on a proprietary survey dataset.*
*Assessment conducted via AI Maturity Compass · Built by Qasim Almansoor*

---

TONE:
- Senior consulting register — not academic, not motivational, not generic
- Every paragraph earns its place — cut anything that does not add specific insight
- Recommendations are owner-specific and time-bound
- Do not use: "it is important to note", "it is worth mentioning", "in conclusion", "leverage"
- Do not use bullet points inside paragraphs
- Do not use backticks, code formatting, or monospace text anywhere in the report
- Numbers like dollar amounts, SAR values, or percentages must be written as plain text, never in code blocks
- Total body length: 700–850 words"""

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
