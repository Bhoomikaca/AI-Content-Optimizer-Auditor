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

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1,h2,h3{
    color:white;
}

.stButton>button{
    width:100%;
    height:3.2em;
    border-radius:12px;
    border:none;
    background:linear-gradient(90deg,#2563eb,#9333ea);
    color:white;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    transform:scale(1.02);
}

.metric-card{
    background:#1a1f2e;
    padding:18px;
    border-radius:15px;
    border:1px solid #2b3245;
}

.result-card{
    background:#171c28;
    padding:25px;
    border-radius:18px;
    border:1px solid #2d3748;
    margin-bottom:20px;
}

.success-card{
    background:#11281b;
    padding:20px;
    border-radius:15px;
    border:1px solid #2e8b57;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
        width=90
    )

    st.title("AI Pipeline")

    st.markdown("""
✔ Web Retrieval

✔ Content Generation

✔ AI Optimization

✔ Content Audit

✔ Fact Verification
""")

    st.divider()

    st.info(
        "This application generates content using real-time web information, "
        "optimizes it, audits quality, and verifies factual consistency."
    )

# ======================================================
# HEADER
# ======================================================

st.markdown("""
# 🤖 AI Content Optimizer & Auditor

Generate **high-quality AI content** using real-time web information,
automatically optimize it, audit quality, and verify factual accuracy.
""")

st.divider()

# ======================================================
# INPUT SECTION
# ======================================================

col1,col2=st.columns([3,1])

with col1:

    topic=st.text_input(
        "Enter Topic",
        placeholder="Example: FIFA Club World Cup"
    )

with col2:

    content_type=st.selectbox(
        "Content Type",
        [
            "News Article",
            "Blog Post",
            "Social Media Post",
            "Product Description"
        ]
    )

st.write("")

generate=st.button("🚀 Generate AI Content")

if generate:

    if not topic:
        st.warning("Please enter a topic.")

    else:

        try:

            status = st.status(
                "🚀 Running AI Pipeline...",
                expanded=True
            )

            # ============================================
            # STEP 1 : WEB SEARCH
            # ============================================

            status.write("🔍 Searching latest information...")

            retrieved_information, sources = search_web(topic)

            status.write("✅ Web search completed.")

            status.write(
                "📚 Found {} trusted sources.".format(len(sources))
            )

            st.divider()

            st.header("🌐 Retrieved Sources")

            st.info(
                f"Total Sources Retrieved: **{len(sources)}**"
            )

            with st.expander("📖 View Sources", expanded=True):

                for i, source in enumerate(sources, start=1):

                    st.markdown(
                        f"""
**{i}. {source['title']}**

🔗 {source['url']}
"""
                    )

            # ============================================
            # STEP 2 : GENERATE + OPTIMIZE
            # ============================================

            status.write("✍ Generating two AI content drafts...")

            version1, version2, optimized_version = generate_content(
                topic,
                content_type,
                retrieved_information
            )

            status.write(
                "✨ Merging and optimizing the best content..."
            )

            # ============================================
            # STEP 3 : AUDIT
            # ============================================

            status.write(
                "📊 Evaluating quality, grammar and hallucination risk..."
            )

            audit = audit_content(
                optimized_version,
                retrieved_information
            )

            status.write("✅ Audit completed.")

            # ============================================
            # STEP 4 : VERIFY
            # ============================================

            status.write(
                "🔬 Cross-checking claims with retrieved sources..."
            )

            verification = verify_content(
                optimized_version,
                retrieved_information
            )

            status.write("✅ Verification completed.")

            # ============================================
            # PIPELINE COMPLETE
            # ============================================

            status.update(
                label="🎉 Pipeline Completed Successfully!",
                state="complete"
            )

            st.success(
                "AI pipeline executed successfully."
            )

            st.divider()

                        # ============================================
            # CONTENT OPTIMIZER - DRAFT VERSIONS
            # ============================================

            st.header("✍️ Content Optimizer")

            st.write(
                "Two content versions were generated using the "
                "retrieved web information."
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("📝 Version 1")

                st.markdown(
                    f"""
<div class="result-card">
{version1}
</div>
""",
                    unsafe_allow_html=True
                )

            with col2:

                st.subheader("📝 Version 2")

                st.markdown(
                    f"""
<div class="result-card">
{version2}
</div>
""",
                    unsafe_allow_html=True
                )

            st.divider()

                        # ============================================
            # DISPLAY OPTIMIZED FINAL CONTENT
            # ============================================

            st.header("✨ Final Optimized Content")

            st.markdown(
                f"""
<div class="result-card">
{optimized_version}
</div>
""",
                unsafe_allow_html=True
            )

            # ============================================
            # DISPLAY AUDIT REPORT
            # ============================================

            st.divider()

            st.header("📊 Content Auditor Analysis")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Accuracy Score",
                    f"{audit.get('accuracy_score', 0)}/100"
                )

            with col2:
                st.metric(
                    "Grammar Score",
                    f"{audit.get('grammar_score', 0)}/100"
                )

            with col3:
                st.metric(
                    "Clarity Score",
                    f"{audit.get('clarity_score', 0)}/100"
                )

            # ============================================
            # HALLUCINATION RISK
            # ============================================

            st.subheader("🧠 Hallucination Risk")

            hallucination_risk = audit.get(
                "hallucination_risk",
                "UNKNOWN"
            )

            if hallucination_risk == "LOW":
                st.success("✅ LOW RISK")

            elif hallucination_risk == "MEDIUM":
                st.warning("⚠️ MEDIUM RISK")

            else:
                st.error(
                    f"❌ {hallucination_risk} RISK"
                )

            # ============================================
            # AUDITOR FEEDBACK
            # ============================================

            with st.expander("📝 View Detailed Auditor Feedback"):

                st.write(
                    audit.get(
                        "feedback",
                        "No feedback available."
                    )
                )

            # ============================================
            # DISPLAY VERIFICATION RESULTS
            # ============================================

            st.divider()

            st.header("🔬 Fact Verification Results")

            st.write(verification)

            # ============================================
            # FINAL DECISION
            # ============================================

            st.divider()

            st.header("🏆 Final Decision")

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

            average_score = (
                accuracy_score
                + grammar_score
                + clarity_score
            ) / 3

            if (
                average_score >= 80
                and hallucination_risk == "LOW"
            ):

                st.success(
                    f"""
🏆 READY TO PUBLISH

Overall Quality Score: {average_score:.1f}/100

The content has successfully completed generation,
optimization, auditing, and fact verification.
"""
                )

            elif average_score >= 60:

                st.warning(
                    f"""
⚠️ REVIEW RECOMMENDED

Overall Quality Score: {average_score:.1f}/100

The content may require minor improvements before publishing.
"""
                )

            else:

                st.error(
                    f"""
❌ NEEDS IMPROVEMENT

Overall Quality Score: {average_score:.1f}/100

The content requires further optimization before publishing.
"""
                )

           

        except Exception as error:

            error_message = str(error).lower()

            if (
                "rate_limit" in error_message
                or "rate limit" in error_message
                or "429" in error_message
            ):
                st.error(
                    "⚠️ AI service usage limit has been reached. "
                    "Please wait for the API limit to reset and try again later."
                )

            elif "api key" in error_message or "authentication" in error_message:
                st.error(
                    "🔑 AI service authentication failed. "
                    "Please check the API configuration."
                )

            elif "connection" in error_message or "timeout" in error_message:
                st.error(
                    "🌐 Unable to connect to the AI service. "
                    "Please check your internet connection and try again."
                )

            else:
                st.error(
                    "❌ Something went wrong while processing the content. "
                    "Please try again later."
                )

            with st.expander("🔧 Technical Error Details"):
                st.code(str(error))