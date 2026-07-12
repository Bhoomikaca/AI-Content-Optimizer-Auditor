import os
import json
import re
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def audit_content(optimized_content, retrieved_information):

    # Limit source information to reduce token usage
    retrieved_information = str(retrieved_information)[:5000]

    prompt = f"""
You are an AI Content Auditor and Claim Verification Agent.

Analyze the optimized content using ONLY the provided source information.

SOURCE INFORMATION:
{retrieved_information}

OPTIMIZED CONTENT:
{optimized_content}

Perform TWO tasks.

TASK 1: CONTENT AUDIT

Evaluate:

1. Accuracy score from 0 to 100.
2. Grammar score from 0 to 100.
3. Clarity score from 0 to 100.
4. Hallucination risk as LOW, MEDIUM, or HIGH.
5. Give brief feedback.

TASK 2: CLAIM VERIFICATION

Identify the important factual claims.

For each claim, classify it as:

SUPPORTED:
The source information supports the claim.

UNSUPPORTED:
There is not enough source evidence.

CONTRADICTED:
The source information conflicts with the claim.

Count:

- Supported claims
- Unsupported claims
- Contradicted claims

Keep verification details concise.

IMPORTANT RULES:

- Use ONLY the provided source information.
- Do not use outside knowledge.
- Be strict.
- Do not invent evidence.
- Check only important factual claims.
- Maximum 8 claims.
- Keep reasons short.
- Return ONLY valid JSON.
- Do not use markdown.

Return exactly this structure:

{{
    "audit": {{
        "accuracy_score": 0,
        "grammar_score": 0,
        "clarity_score": 0,
        "hallucination_risk": "LOW",
        "feedback": "Short feedback"
    }},
    "verification": {{
        "supported_claims": 0,
        "unsupported_claims": 0,
        "contradicted_claims": 0,
        "verification_details": [
            {{
                "claim": "Factual claim",
                "status": "SUPPORTED",
                "reason": "Short reason"
            }}
        ]
    }}
}}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI Content Auditor and "
                        "Claim Verification Agent. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=800,
            response_format={"type": "json_object"}
        )

        response_text = (
            response.choices[0]
            .message.content
            .strip()
        )

        response_text = response_text.replace(
            "```json",
            ""
        )

        response_text = response_text.replace(
            "```",
            ""
        ).strip()

        try:

            return json.loads(response_text)

        except json.JSONDecodeError:

            match = re.search(
                r"\{.*\}",
                response_text,
                re.DOTALL
            )

            if match:

                try:

                    return json.loads(match.group())

                except json.JSONDecodeError:

                    pass

            return {
                "audit": {
                    "accuracy_score": 0,
                    "grammar_score": 0,
                    "clarity_score": 0,
                    "hallucination_risk": "UNKNOWN",
                    "feedback": "Invalid auditor response."
                },
                "verification": {
                    "supported_claims": 0,
                    "unsupported_claims": 0,
                    "contradicted_claims": 0,
                    "verification_details": []
                }
            }

    except Exception as error:

        print("AUDITOR AND VERIFIER ERROR:", error)

        return {
            "audit": {
                "accuracy_score": 0,
                "grammar_score": 0,
                "clarity_score": 0,
                "hallucination_risk": "ERROR",
                "feedback": "Analysis temporarily unavailable."
            },
            "verification": {
                "supported_claims": 0,
                "unsupported_claims": 0,
                "contradicted_claims": 0,
                "verification_details": []
            }
        }


# ---------------------------------------
# TEMPORARY TEST
# ---------------------------------------

if __name__ == "__main__":

    from web_search import search_web
    from content_optimizer import generate_content
    from content_verifier import verify_content

    topic = "Latest FIFA Club World Cup news"

    content_type = "News Article"

    print("Step 1: Retrieving information...")

    retrieved_information, sources = search_web(topic)

    print("Step 2: Generating content...")

    version_1, version_2, optimized_content = generate_content(
        topic,
        content_type,
        retrieved_information
    )

    print("Step 3: Auditing and verifying...")

    analysis_result = audit_content(
        optimized_content,
        retrieved_information
    )

    audit_result = analysis_result["audit"]

    verification_result = verify_content(
        analysis_result
    )

    print("\n--- AUDIT RESULTS ---\n")

    print(audit_result)

    print("\n--- VERIFICATION RESULTS ---\n")

    print(verification_result)