import base64
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_visual_signals(image_bytes: bytes) -> str:
    """
    Extracts visible plant symptoms from an image.
    Does NOT diagnose disease or recommend treatment.
    """

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a plant observation assistant. "
                    "Describe only visible symptoms such as discoloration, "
                    "spots, wilting, dryness, or damage. "
                    "Do NOT diagnose disease or suggest treatment."
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe visible plant symptoms."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()