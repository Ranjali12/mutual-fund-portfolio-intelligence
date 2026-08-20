import json
import os

from google import genai
from google.genai import errors


def generate_insights(analysis: dict) -> dict:
    """Generate personalised portfolio insights using Gemini."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a mutual-fund portfolio intelligence assistant.

Your job is to interpret VERIFIED portfolio analytics and produce
a small set of useful, prioritised insights for the investor.

IMPORTANT RULES:
1. Do not recalculate financial numbers.
2. Do not invent fund facts, returns, risks, or categories.
3. Use only the evidence provided in the portfolio analysis.
4. If evidence is insufficient, explicitly say so.
5. Distinguish facts from interpretation.
6. Do not give a direct buy/sell instruction.
7. Focus on what is most useful to the investor.

Return ONLY valid JSON in this structure:

{{
  "overall_assessment": "short summary",
  "insights": [
    {{
      "priority": "high|medium|low",
      "type": "concentration|performance|suitability|diversification|data_quality|other",
      "finding": "what the data shows",
      "why_it_matters": "why this may matter for this investor",
      "evidence": ["specific verified values from the input"],
      "action": "reasonable next step"
    }}
  ]
}}

Investor and verified portfolio analysis:

{json.dumps(analysis, indent=2, default=str)}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            },
        )
    except errors.ServerError as exc:
        raise RuntimeError(
            "Gemini is temporarily unavailable. "
            "Please try again in a few minutes."
        ) from exc

    text = response.text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid JSON."
        ) from exc