import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_content(topic, content_type, retrieved_information):

    # Limit retrieved text
    retrieved_information = str(retrieved_information)[:10000]

    generation_prompt = f"""
Create TWO publish-ready content versions using ONLY the source information.

TOPIC:
{topic}

CONTENT TYPE:
{content_type}

SOURCE INFORMATION:
{retrieved_information}

RULES:
- Do not invent facts.
- Version 1: professional, detailed, exactly 3 paragraphs.
- Version 2: engaging, concise, exactly 2 paragraphs.
- Return ONLY JSON.
- version_1 MUST be one plain string.
- version_2 MUST be one plain string.

EXACT FORMAT:
{{
  "version_1": "Paragraph 1.\\n\\nParagraph 2.\\n\\nParagraph 3.",
  "version_2": "Paragraph 1.\\n\\nParagraph 2."
}}
"""

    try:

        # -----------------------------
        # Generate Version 1 & Version 2
        # -----------------------------
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Return valid JSON with exactly two string fields: version_1 and version_2."
                },
                {
                    "role": "user",
                    "content": generation_prompt
                }
            ],
            temperature=0.3,
            max_tokens=1800,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        version_1 = str(result.get("version_1", "")).strip()
        version_2 = str(result.get("version_2", "")).strip()

        # -----------------------------
        # Optimization Step
        # -----------------------------
        optimization_prompt = f"""
You are an expert AI Content Optimizer.

You are given two versions of the same content.

Version 1:
{version_1}

Version 2:
{version_2}

Your task is to:

1. Compare both versions.
2. Keep only the strongest points.
3. Remove duplicate information.
4. Improve readability.
5. Improve grammar.
6. Improve clarity.
7. Preserve factual accuracy.
8. Produce ONE polished version.

Return ONLY the final optimized content.
"""

        optimized_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI content editor."
                },
                {
                    "role": "user",
                    "content": optimization_prompt
                }
            ],
            temperature=0.2,
            max_tokens=1200
        )

        optimized_version = (
            optimized_response.choices[0]
            .message.content
            .strip()
        )

        return version_1, version_2, optimized_version

    except Exception as error:

        print("OPTIMIZER ERROR:", error)

        return (
            "Content generation temporarily unavailable.",
            "Content generation temporarily unavailable.",
            "Content optimization temporarily unavailable."
        )