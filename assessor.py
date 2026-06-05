# assessor.py
# Scoring logic with consistency detection and self-perception gap analysis

from questions import QUESTIONS, DIMENSIONS, get_maturity_level


def compute_scores(responses: dict) -> dict:
    dimension_scores = {}
    question_detail = {}

    for dimension in DIMENSIONS:
        questions = QUESTIONS[dimension]
        scores = []
        for q in questions:
            qid = q["id"]
            if qid in responses:
                score = responses[qid]
                scores.append(score)
                question_detail[qid] = {
                    "dimension": dimension,
                    "type": q["type"],
                    "score": score,
                    "text": q["text"],
                }
        if scores:
            dimension_scores[dimension] = round(sum(scores) / len(scores), 2)
        else:
            dimension_scores[dimension] = 0.0

    overall = round(sum(dimension_scores.values()) / len(dimension_scores), 2)
    maturity = get_maturity_level(overall)

    # Question type averages across all dimensions
    type_scores = {}
    for qid, detail in question_detail.items():
        qtype = detail["type"]
        if qtype not in type_scores:
            type_scores[qtype] = []
        type_scores[qtype].append(detail["score"])

    type_averages = {
        t: round(sum(s) / len(s), 2)
        for t, s in type_scores.items()
    }

    # ── CONSISTENCY ANALYSIS ──
    # Flags dimensions where answers are internally contradictory
    # High variance within a dimension = self-reporting inconsistency
    # This is itself a diagnostic finding
    consistency_flags = {}
    for dimension in DIMENSIONS:
        questions = QUESTIONS[dimension]
        scores = [
            responses[q["id"]]
            for q in questions
            if q["id"] in responses
        ]
        if len(scores) >= 3:
            mean = sum(scores) / len(scores)
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            std_dev = variance ** 0.5
            max_score = max(scores)
            min_score = min(scores)
            spread = max_score - min_score

            # Flag if std deviation > 1.2 or spread >= 3
            # This means answers within the dimension are inconsistent
            # e.g. scoring 5 on Current State but 1 on Evidence
            if std_dev > 1.2 or spread >= 3:
                consistency_flags[dimension] = {
                    "flagged": True,
                    "std_dev": round(std_dev, 2),
                    "spread": spread,
                    "max": max_score,
                    "min": min_score,
                    "interpretation": _interpret_inconsistency(
                        dimension, scores, questions, responses
                    ),
                }
            else:
                consistency_flags[dimension] = {"flagged": False}
        else:
            consistency_flags[dimension] = {"flagged": False}

    return {
        "dimension_scores": dimension_scores,
        "overall_score": overall,
        "maturity_level": maturity,
        "question_detail": question_detail,
        "type_averages": type_averages,
        "consistency_flags": consistency_flags,
    }


def _interpret_inconsistency(dimension, scores, questions, responses):
    """
    Generate a human-readable interpretation of the inconsistency.
    Identifies which question types have the largest gap.
    """
    type_scores = {}
    for q in questions:
        if q["id"] in responses:
            qtype = q["type"]
            type_scores[qtype] = responses[q["id"]]

    if not type_scores:
        return "Inconsistent answers detected within this dimension."

    max_type = max(type_scores.items(), key=lambda x: x[1])
    min_type = min(type_scores.items(), key=lambda x: x[1])

    if max_type[1] - min_type[1] >= 3:
        return (
            f"Your '{max_type[0]}' score ({max_type[1]}/5) is significantly higher "
            f"than your '{min_type[0]}' score ({min_type[1]}/5). "
            f"This suggests the organisation has stronger aspirations or stated positions "
            f"than its evidence base can support. This gap is itself a risk."
        )
    return (
        f"Answer spread of {max(scores) - min(scores)} points detected. "
        f"Verify responses with operational stakeholders before acting on this dimension's score."
    )


def identify_gaps(dimension_scores: dict) -> list:
    return sorted(dimension_scores.items(), key=lambda x: x[1])


def get_score_label(score: float) -> str:
    if score < 1.8:
        return "Critical Gap"
    elif score < 2.6:
        return "Needs Attention"
    elif score < 3.4:
        return "Developing"
    elif score < 4.2:
        return "Advanced"
    else:
        return "Leading"


def compute_self_perception_gap(
    self_perception_option: str,
    overall_score: float
) -> dict:
    """
    Compares self-declared maturity level with assessed score.
    The gap between perception and reality is a diagnostic finding.
    """
    perception_map = {
        "Early stage — we are just beginning to explore AI": 1.0,
        "Developing — we have pilots running but nothing at scale": 2.0,
        "Intermediate — AI is operational in some areas": 3.0,
        "Advanced — AI is embedded across multiple functions": 4.0,
        "Leading — AI is core to how we operate and compete": 5.0,
    }

    perceived = perception_map.get(self_perception_option, None)
    if perceived is None:
        return {"gap": None, "direction": None, "interpretation": None}

    gap = round(overall_score - perceived, 2)

    if abs(gap) <= 0.4:
        direction = "aligned"
        interpretation = (
            "Your self-perception closely matches your assessed score. "
            "This suggests organisational self-awareness — a positive signal for "
            "structured transformation."
        )
    elif gap > 0.4:
        direction = "underestimate"
        interpretation = (
            f"You rated yourself lower than your assessment result by {abs(gap)} points. "
            f"This may indicate excessive caution or a lack of visibility into existing "
            f"capability. There may be more to build on than leadership realises."
        )
    else:
        direction = "overestimate"
        interpretation = (
            f"You rated yourself higher than your assessment result by {abs(gap)} points. "
            f"This is the most common pattern in GCC energy organisations and the most "
            f"dangerous: executive confidence outpacing operational reality. "
            f"Transformation programmes built on overestimated baselines consistently "
            f"underdeliver."
        )

    return {
        "gap": gap,
        "perceived_score": perceived,
        "direction": direction,
        "interpretation": interpretation,
    }
