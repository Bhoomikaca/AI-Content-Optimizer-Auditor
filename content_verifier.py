import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def verify_content(generated_content, retrieved_information):

    prompt = f"""
You are an expert AI Fact-Checking and Claim Verification Agent.

Your job is to identify factual claims in the generated content and
verify each claim using ONLY the retrieved information provided.

RETRIEVED INFORMATION:
{retrieved_information}

GENERATED CONTENT:
{generated_content}

INSTRUCTIONS:

1. Identify the factual claims in the generated content.

2. Compare every factual claim against the retrieved information.

3. Classify each claim as:

SUPPORTED
- The retrieved information clearly supports the claim.

UNSUPPORTED
- The retrieved information does not provide enough evidence.

CONTRADICTED
- The retrieved information directly conflicts with the claim.

4. Count the total number of:
- Supported claims
- Unsupported claims
- Contradicted claims

5. Do not use outside knowledge.

6. Be strict. Do not mark a claim as supported unless evidence exists
in the retrieved information.

Return the response EXACTLY in this format:

SUPPORTED_CLAIMS: [number]

UNSUPPORTED_CLAIMS: [number]

CONTRADICTED_CLAIMS: [number]

VERIFICATION_DETAILS:

CLAIM: [claim]
STATUS: [SUPPORTED/UNSUPPORTED/CONTRADICTED]
REASON: [brief explanation]

CLAIM: [claim]
STATUS: [SUPPORTED/UNSUPPORTED/CONTRADICTED]
REASON: [brief explanation]
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
            temperature=0.1,
            max_tokens=2000
        )

        response_text = response.choices[0].message.content.strip()

        print("\n========== GROQ VERIFIER RAW RESPONSE ==========\n")
        print(response_text)
        print("\n===============================================\n")

        return response_text

    except Exception as error:

        print("\nGROQ VERIFIER ERROR:\n")
        print(error)

        return f"""
SUPPORTED_CLAIMS: 0

UNSUPPORTED_CLAIMS: 0

CONTRADICTED_CLAIMS: 0

VERIFICATION_DETAILS:

ERROR: {error}
"""


# ============================================================
# TEMPORARY TEST
# ============================================================

if __name__ == "__main__":

    from web_search import search_web
    from content_optimizer import generate_content

    topic = "Latest FIFA Club World Cup news"

    content_type = "News Article"

    print("Step 1: Retrieving information...")

    retrieved_information, sources = search_web(topic)

    print("Step 2: Generating content...")

    version_1, version_2 = generate_content(
        topic,
        content_type,
        retrieved_information
    )

    print("Step 3: Verifying claims...")

    verification_report = verify_content(
        version_1,
        retrieved_information
    )

    print("\n--- VERIFICATION RESULTS ---\n")

    print(verification_report)