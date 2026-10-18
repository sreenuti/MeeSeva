from __future__ import annotations

from dataclasses import dataclass


CATEGORIES = ("identity_proof", "address_proof", "income_proof", "unknown")


@dataclass
class ClassificationResult:
    category: str
    certainty: str  # high | medium | low | unknown — rule-based certainty, not calibrated probability
    matched_signals: list[str]


def classify_document(text: str) -> ClassificationResult:
    lowered = text.lower()
    scores = {
        "identity_proof": 0,
        "address_proof": 0,
        "income_proof": 0,
    }
    signals: dict[str, list[str]] = {k: [] for k in scores}

    identity_terms = [
        "synthetic identity",
        "identity proof",
        "date of birth",
        "synthetic id",
        "synth-id-",
    ]
    address_terms = [
        "synthetic address",
        "address proof",
        "residence",
        "postal code",
        "district",
        "village",
    ]
    income_terms = [
        "synthetic income",
        "income proof",
        "gross annual income",
        "salary",
        "payslip",
        "income amount",
        "inr",
    ]

    for term in identity_terms:
        if term in lowered:
            scores["identity_proof"] += 1
            signals["identity_proof"].append(term)
    for term in address_terms:
        if term in lowered:
            scores["address_proof"] += 1
            signals["address_proof"].append(term)
    for term in income_terms:
        if term in lowered:
            scores["income_proof"] += 1
            signals["income_proof"].append(term)

    best = max(scores, key=lambda k: scores[k])
    best_score = scores[best]
    if best_score == 0:
        return ClassificationResult(category="unknown", certainty="unknown", matched_signals=[])

    second = sorted(scores.values(), reverse=True)[1]
    if best_score >= 3 and best_score > second:
        certainty = "high"
    elif best_score >= 2:
        certainty = "medium"
    else:
        certainty = "low"
    return ClassificationResult(category=best, certainty=certainty, matched_signals=signals[best])
