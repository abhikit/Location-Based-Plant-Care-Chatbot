RISK_KEYWORDS = {
    "toxic_chemical": [
        "pesticide overdose",
        "chemical concentrate",
        "toxic spray",
    ],
    "medical_advice": [
        "safe for humans",
        "consume leaves",
        "eat plant",
    ],
    "environmental_harm": [
        "excess fertilizer",
        "dump chemicals",
        "overuse pesticide",
    ],
}


def apply_policy_rules(answer: str) -> list[str]:
    flags = []

    text = answer.lower()
    for category, keywords in RISK_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                flags.append(category)
                break

    return flags