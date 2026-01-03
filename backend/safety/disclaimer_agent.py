from typing import Optional


def inject_disclaimer(
    answer: str,
    input_mode: str,
    used_vision: bool,
    used_environment: bool,
) -> str:
    """
    Injects a deterministic safety disclaimer.
    This function NEVER changes the answer content.
    """

    disclaimers = []

    # Generic disclaimer (always safe)
    disclaimers.append(
        "⚠️ This guidance is for informational purposes only and should not be considered professional advice."
    )

    # Vision-based disclaimer
    if used_vision:
        disclaimers.append(
            "📷 Image-based assessment may be limited by image quality, lighting, or angle."
        )

    # Environment-based disclaimer
    if used_environment:
        disclaimers.append(
            "🌦️ Local micro-climate conditions may vary and can influence plant health differently."
        )

    # Join disclaimers
    disclaimer_text = "\n\n" + "\n".join(disclaimers)

    return answer.strip() + disclaimer_text