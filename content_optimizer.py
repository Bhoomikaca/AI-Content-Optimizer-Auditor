import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def generate_content(topic, content_type, retrieved_information):

    # Limit source information to reduce token usage
    retrieved_information = str(retrieved_information)[:5000]

    prompt = f"""
You are an AI Content Optimizer.

Using ONLY the provided source information, create:

1. VERSION 1
2. VERSION 2
3. FINAL OPTIMIZED CONTENT

TOPIC:
{topic}

CONTENT TYPE:
{content_type}

SOURCE INFORMATION:
{retrieved_information}

INSTRUCTIONS:

VERSION 1:
- Professional and informative.
- Maximum 3 short paragraphs.
- Include only important facts.
- Use simple and clear language.

VERSION 2:
- Concise and engaging.
- Maximum 2 short paragraphs.
- Include only important facts.
- Use simple and clear language.

FINAL OPTIMIZED CONTENT:
- Combine the strongest information from Version 1 and Version 2.
- Remove duplicate information.
- Do not simply copy both versions together.
- Improve clarity and readability.
- Use simple language.
- Maximum 3 short paragraphs.
- Preserve factual accuracy.

IMPORTANT RULES:

- Use ONLY the provided source information.
- Do not use outside knowledge.
- Do not invent facts.
- Do not add unsupported claims.
- Avoid unnecessary details.
- Avoid repeating information.
- Keep the output concise to reduce token usage.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "version_1": "Version 1 content",
    "version_2": "Version 2 content",
    "optimized_content": "Final combined and optimized content"
}}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI Content Optimizer. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1200,
            response_format={"type": "json_object"}
        )

        response_text = response.choices[0].message.content.strip()

        result = json.loads(response_text)

        version_1 = str(
            result.get("version_1", "")
        ).strip()

        version_2 = str(
            result.get("version_2", "")
        ).strip()

        optimized_content = str(
            result.get("optimized_content", "")
        ).strip()

        return (
            version_1,
            version_2,
            optimized_content
        )

    except Exception as error:

        print("CONTENT OPTIMIZER ERROR:", error)

        return (
            "Content Version 1 is temporarily unavailable.",
            "Content Version 2 is temporarily unavailable.",
            "Final optimized content is temporarily unavailable."
        )


# ---------------------------------------
# TEMPORARY TEST
# ---------------------------------------

if __name__ == "__main__":

    from web_search import search_web

    topic = "Latest FIFA Club World Cup news"

    content_type = "News Article"

    print("Step 1: Retrieving information...")

    retrieved_information, sources = search_web(topic)

    print("Step 2: Generating and optimizing content...")

    version_1, version_2, optimized_content = generate_content(
        topic,
        content_type,
        retrieved_information
    )

    print("\n--- VERSION 1 ---\n")
    print(version_1)

    print("\n--- VERSION 2 ---\n")
    print(version_2)

    print("\n--- FINAL OPTIMIZED CONTENT ---\n")
    print(optimized_content)