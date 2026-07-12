import streamlit as st

from web_search import search_web
from content_optimizer import generate_content
from content_auditor import audit_content
from content_verifier import verify_content


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="AI Content Optimizer & Auditor",
    page_icon="🤖",
    layout="wide"
)


# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: white;
    }

    .stButton > button {
        width: 100%;
        height: 3.2em;
        border-radius: 12px;
        border: none;
        background: linear-gradient(90deg, #2563eb, #9333ea);
        color: white;
        font-size: 18px;
        font-weight: bold;
    }

    .stButton > button:hover {
        transform: scale(1.02);
    }

    .metric-card {
        background: #1a1f2e;
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #2b3245;
    }

    .result-card {
        background: #171c28;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #2d3748;
        margin-bottom: 20px;
    }

    .success-card {
        background: #11281b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #2e8b57;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
        width=90
    )

    st.title("AI Pipeline")

    st.markdown(
        """
✔ Web Retrieval

✔ Content Generation

✔ AI Optimization

✔ Content Audit

✔ Claim Verification

✔ Final Decision
"""
    )

    st.divider()

    st.info(
        "This application generates content using real-time "
        "web information, optimizes it, audits quality, "
        "and verifies factual claims."
    )


# ======================================================
# HEADER
# ======================================================

st.markdown(
    """
# 🤖 AI Content Optimizer & Auditor

Generate **high-quality AI content** using real-time web information,
automatically optimize it, audit content quality, and verify factual claims.
"""
)

st.divider()


# ======================================================
# INPUT SECTION
# ======================================================

col1, col2 = st.columns([3, 1])

with col1:

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Latest FIFA Club World Cup News"
    )

with col2:

    content_type = st.selectbox(
        "Content Type",
        [
            "News Article",
            "Blog Post",
            "Social Media Post",
            "Product Description"
        ]
    )


st.write("")


generate = st.button("🚀 Generate AI Content")


# ======================================================
# START PIPELINE
# ======================================================

if generate:

    if not topic:

        st.warning("Please enter a topic.")

    else:

        try:

            status = st.status(
                "🚀 Running AI Pipeline...",
                expanded=True
            )


            # ==================================================
            # STEP 1: WEB SEARCH
            # ==================================================

            status.write(
                "🔍 Searching for the latest information..."
            )

            retrieved_information, sources = search_web(topic)

            status.write("✅ Web search completed.")

            status.write(
                f"📚 Found {len(sources)} sources."
            )


            # ==================================================
            # DISPLAY RETRIEVED SOURCES
            # ==================================================

            st.divider()

            st.header("🌐 Retrieved Sources")

            st.info(
                f"Total Sources Retrieved: **{len(sources)}**"
            )

            with st.expander(
                "📖 View Retrieved Sources",
                expanded=True
            ):

                for i, source in enumerate(
                    sources,
                    start=1
                ):

                    st.markdown(
                        f"""
**{i}. {source.get('title', 'Unknown Source')}**

🔗 {source.get('url', 'URL unavailable')}
"""
                    )


            # ==================================================
            # STEP 2: CONTENT GENERATION + OPTIMIZATION
            # ==================================================

            status.write(
                "✍️ Generating two AI content versions..."
            )

            version_1, version_2, optimized_content = generate_content(
                topic,
                content_type,
                retrieved_information
            )

            status.write(
                "✨ Final optimized content generated."
            )


            # ==================================================
            # STEP 3: AUDIT + CLAIM VERIFICATION
            # ONE GROQ CALL
            # ==================================================

            status.write(
                "📊 Auditing content and verifying factual claims..."
            )

            analysis_result = audit_content(
                optimized_content,
                retrieved_information
            )


            # ==================================================
            # EXTRACT AUDIT RESULT
            # ==================================================

            audit = analysis_result.get(
                "audit",
                {}
            )


            # ==================================================
            # EXTRACT VERIFICATION RESULT
            # ZERO EXTRA GROQ CALLS
            # ==================================================

            verification = verify_content(
                analysis_result
            )


            status.write("✅ Content audit completed.")

            status.write("✅ Claim verification completed.")


            # ==================================================
            # PIPELINE COMPLETE
            # ==================================================

            status.update(
                label="🎉 Pipeline Completed Successfully!",
                state="complete",
                expanded=False
            )

            st.success(
                "AI pipeline executed successfully."
            )


            # ==================================================
            # CONTENT OPTIMIZER OUTPUT
            # ==================================================

            st.divider()

            st.header("✍️ Content Optimizer")

            st.write(
                "Two content versions were generated from "
                "the retrieved web information."
            )


            # ==================================================
            # DISPLAY VERSION 1 AND VERSION 2
            # ==================================================

            col1, col2 = st.columns(2)


            with col1:

                st.subheader("📝 Version 1")

                st.markdown(
                    f"""
<div class="result-card">
{version_1}
</div>
""",
                    unsafe_allow_html=True
                )


            with col2:

                st.subheader("📝 Version 2")

                st.markdown(
                    f"""
<div class="result-card">
{version_2}
</div>
""",
                    unsafe_allow_html=True
                )


            # ==================================================
            # FINAL OPTIMIZED CONTENT
            # ==================================================

            st.divider()

            st.header("✨ Final Optimized Content")

            st.write(
                "The strongest information from both versions "
                "has been combined, refined, and simplified."
            )

            st.markdown(
                f"""
<div class="result-card">
{optimized_content}
</div>
""",
                unsafe_allow_html=True
            )


            # ==================================================
            # CONTENT AUDITOR ANALYSIS
            # ==================================================

            st.divider()

            st.header("📊 Content Auditor Analysis")


            accuracy_score = audit.get(
                "accuracy_score",
                0
            )

            grammar_score = audit.get(
                "grammar_score",
                0
            )

            clarity_score = audit.get(
                "clarity_score",
                0
            )

            hallucination_risk = audit.get(
                "hallucination_risk",
                "UNKNOWN"
            )


            # ==================================================
            # DISPLAY AUDIT SCORES
            # ==================================================

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Accuracy Score",
                    f"{accuracy_score}/100"
                )


            with col2:

                st.metric(
                    "Grammar Score",
                    f"{grammar_score}/100"
                )


            with col3:

                st.metric(
                    "Clarity Score",
                    f"{clarity_score}/100"
                )


            # ==================================================
            # HALLUCINATION RISK
            # ==================================================

            st.subheader("🧠 Hallucination Risk")


            if hallucination_risk == "LOW":

                st.success("✅ LOW RISK")


            elif hallucination_risk == "MEDIUM":

                st.warning("⚠️ MEDIUM RISK")


            elif hallucination_risk == "HIGH":

                st.error("❌ HIGH RISK")


            else:

                st.warning(
                    f"⚠️ {hallucination_risk}"
                )


            # ==================================================
            # AUDITOR FEEDBACK
            # ==================================================

            with st.expander(
                "📝 View Detailed Auditor Feedback"
            ):

                st.write(
                    audit.get(
                        "feedback",
                        "No auditor feedback available."
                    )
                )


            # ==================================================
            # CLAIM VERIFICATION RESULTS
            # ==================================================

            st.divider()

            st.header("🔬 Claim Verification Results")


            supported_claims = verification.get(
                "supported_claims",
                0
            )

            unsupported_claims = verification.get(
                "unsupported_claims",
                0
            )

            contradicted_claims = verification.get(
                "contradicted_claims",
                0
            )


            # ==================================================
            # CLAIM METRICS
            # ==================================================

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Supported Claims",
                    supported_claims
                )


            with col2:

                st.metric(
                    "Unsupported Claims",
                    unsupported_claims
                )


            with col3:

                st.metric(
                    "Contradicted Claims",
                    contradicted_claims
                )


            # ==================================================
            # VERIFICATION DETAILS
            # ==================================================

            verification_details = verification.get(
                "verification_details",
                []
            )


            with st.expander(
                "📋 View Claim Verification Details"
            ):

                if verification_details:

                    for i, detail in enumerate(
                        verification_details,
                        start=1
                    ):

                        st.markdown(
                            f"### Claim {i}"
                        )


                        st.write(
                            "**Claim:**",
                            detail.get(
                                "claim",
                                "Claim unavailable"
                            )
                        )


                        claim_status = detail.get(
                            "status",
                            "UNKNOWN"
                        )


                        if claim_status == "SUPPORTED":

                            st.success(
                                "✅ SUPPORTED"
                            )


                        elif claim_status == "UNSUPPORTED":

                            st.warning(
                                "⚠️ UNSUPPORTED"
                            )


                        elif claim_status == "CONTRADICTED":

                            st.error(
                                "❌ CONTRADICTED"
                            )


                        else:

                            st.info(
                                claim_status
                            )


                        st.write(
                            "**Reason:**",
                            detail.get(
                                "reason",
                                "Reason unavailable"
                            )
                        )


                        st.divider()


                else:

                    st.info(
                        "No verification details available."
                    )


            # ==================================================
            # FINAL DECISION
            # ==================================================

            st.divider()

            st.header("🏆 Final Decision")


            average_score = (
                accuracy_score
                + grammar_score
                + clarity_score
            ) / 3


            # ==================================================
            # READY TO PUBLISH
            # ==================================================

            if (
                average_score >= 80
                and hallucination_risk == "LOW"
                and unsupported_claims == 0
                and contradicted_claims == 0
            ):

                st.success(
                    f"""
🏆 READY TO PUBLISH

Overall Quality Score: {average_score:.1f}/100

Supported Claims: {supported_claims}

Unsupported Claims: {unsupported_claims}

Contradicted Claims: {contradicted_claims}

The content successfully completed generation,
optimization, auditing, and claim verification.
"""
                )


            # ==================================================
            # REVIEW RECOMMENDED
            # ==================================================

            elif (
                average_score >= 60
                and contradicted_claims == 0
            ):

                st.warning(
                    f"""
⚠️ REVIEW RECOMMENDED

Overall Quality Score: {average_score:.1f}/100

Supported Claims: {supported_claims}

Unsupported Claims: {unsupported_claims}

Contradicted Claims: {contradicted_claims}

The content may require minor improvements
before publishing.
"""
                )


            # ==================================================
            # NEEDS IMPROVEMENT
            # ==================================================

            else:

                st.error(
                    f"""
❌ NEEDS IMPROVEMENT

Overall Quality Score: {average_score:.1f}/100

Supported Claims: {supported_claims}

Unsupported Claims: {unsupported_claims}

Contradicted Claims: {contradicted_claims}

The content requires further improvement
before publishing.
"""
                )


            # ==================================================
            # DISPLAY FINAL PUBLISHABLE CONTENT
            # ==================================================

            st.divider()

            st.header("📄 Final Content")

            st.write(
                optimized_content
            )


        # ======================================================
        # ERROR HANDLING
        # ======================================================

        except Exception as error:

            error_message = str(error).lower()


            # ==================================================
            # RATE LIMIT ERROR
            # ==================================================

            if (
                "rate_limit" in error_message
                or "rate limit" in error_message
                or "429" in error_message
            ):

                st.error(
                    "⚠️ AI service usage limit has been reached. "
                    "Please wait for the API limit to reset "
                    "and try again later."
                )


            # ==================================================
            # API KEY ERROR
            # ==================================================

            elif (
                "api key" in error_message
                or "authentication" in error_message
                or "401" in error_message
            ):

                st.error(
                    "🔑 AI service authentication failed. "
                    "Please check the API configuration."
                )


            # ==================================================
            # CONNECTION ERROR
            # ==================================================

            elif (
                "connection" in error_message
                or "timeout" in error_message
            ):

                st.error(
                    "🌐 Unable to connect to the AI service. "
                    "Please check your internet connection "
                    "and try again."
                )


            # ==================================================
            # GENERAL ERROR
            # ==================================================

            else:

                st.error(
                    "❌ Something went wrong while processing "
                    "the content. Please try again."
                )


            # ==================================================
            # TECHNICAL ERROR DETAILS
            # ==================================================

            with st.expander(
                "🔧 Technical Error Details"
            ):

                st.code(
                    str(error)
                )