import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_content(topic, content_type, retrieved_information):

    # Limit retrieved text so we do not waste Groq tokens
    retrieved_information = str(retrieved_information)[:10000]

    prompt = f"""
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
- Do NOT return nested objects.
- Do NOT return title/content objects.
- Do NOT return arrays or lists.

EXACT FORMAT:
{{
  "version_1": "Paragraph 1.\\n\\nParagraph 2.\\n\\nParagraph 3.",
  "version_2": "Paragraph 1.\\n\\nParagraph 2."
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Return valid JSON with exactly two string fields: version_1 and version_2."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1800,
            response_format={"type": "json_object"}
        )

        result = json.loads(
            response.choices[0].message.content
        )

        version_1 = result["version_1"]
        version_2 = result["version_2"]

        # Emergency handling if model still returns dictionary
        if isinstance(version_1, dict):
            content = version_1.get("content", "")
            if isinstance(content, list):
                version_1 = "\n\n".join(content)
            else:
                version_1 = str(content)

        if isinstance(version_2, dict):
            content = version_2.get("content", "")
            if isinstance(content, list):
                version_2 = "\n\n".join(content)
            else:
                version_2 = str(content)

        return str(version_1), str(version_2)

    except Exception as error:
        print("OPTIMIZER ERROR:", error)

        return (
            "Content generation temporarily unavailable.",
            "Content generation temporarily unavailable."
        )