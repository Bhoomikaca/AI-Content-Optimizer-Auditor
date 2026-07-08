import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def audit_content(content, retrieved_information):

    prompt = f"""
You are an AI Content Auditor.

Compare the generated content ONLY with the retrieved information.

Retrieved Information:
{retrieved_information}

Generated Content:
{content}

Your task is to audit the content based on:

1. Factual accuracy
2. Grammar quality
3. Clarity
4. Hallucination risk

Return ONLY valid JSON.

Use exactly this structure:

{{
    "accuracy_score": 95,
    "grammar_score": 98,
    "clarity_score": 94,
    "hallucination_risk": "LOW",
    "feedback": "Brief explanation."
}}

IMPORTANT RULES:

Do not write explanations outside the JSON.
Do not use markdown.
Do not use ```json.
Return JSON only.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1000
        )

        response_text = response.choices[0].message.content.strip()

        # ---------- DEBUG ----------
        print("\n========== GROQ RAW RESPONSE ==========\n")
        print(response_text)
        print("\n=======================================\n")
        # ---------------------------

        # Remove markdown formatting if Groq adds it
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "").strip()

        try:

            result = json.loads(response_text)

            return result

        except Exception:

            # Try extracting JSON from response
            match = re.search(
                r"\{.*\}",
                response_text,
                re.DOTALL
            )

            if match:

                try:

                    result = json.loads(match.group())

                    return result

                except Exception:

                    pass

            # Return fallback result
            return {
                "accuracy_score": 0,
                "grammar_score": 0,
                "clarity_score": 0,
                "hallucination_risk": "UNKNOWN",
                "feedback": response_text
            }

    except Exception as error:

        print("GROQ ERROR:", error)

        return {
            "accuracy_score": 0,
            "grammar_score": 0,
            "clarity_score": 0,
            "hallucination_risk": "ERROR",
            "feedback": str(error)
        }


# ============================================================
# TEST THE CONTENT AUDITOR
# ============================================================

if __name__ == "__main__":

    from web_search import search_web
    from content_optimizer import generate_content

    topic = "Latest FIFA Club World Cup news"

    content_type = "News Article"

    retrieved_information, _ = search_web(topic)

    version_1, version_2 = generate_content(
        topic,
        content_type,
        retrieved_information
    )

    print("\n========== AUDITING VERSION 1 ==========\n")

    audit_result = audit_content(
        version_1,
        retrieved_information
    )

    print(audit_result)