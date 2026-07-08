import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def get_tavily_key():
    """
    Gets Tavily API key from:
    1. Environment variables locally
    2. Streamlit Cloud secrets when deployed
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st
        return st.secrets["TAVILY_API_KEY"]
    except Exception:
        return None


TAVILY_API_KEY = get_tavily_key()

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY was not found. "
        "Check your .env file or Streamlit secrets."
    )


tavily_client = TavilyClient(
    api_key=TAVILY_API_KEY
)


def search_web(topic):

    response = tavily_client.search(
        query=topic,
        search_depth="advanced",
        max_results=5
    )

    results = response.get("results", [])

    retrieved_information = []
    sources = []

    for result in results:

        title = result.get("title", "No title")

        content = result.get(
            "content",
            "No content"
        )

        url = result.get("url", "")

        retrieved_information.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"Source: {url}\n"
        )

        sources.append({
            "title": title,
            "url": url
        })

    combined_information = "\n\n".join(
        retrieved_information
    )

    return combined_information, sources