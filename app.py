import streamlit as st

from web_search import search_web
from content_optimizer import generate_content
from content_auditor import audit_content
from content_verifier import verify_content

st.set_page_config(
    page_title="AI Content Optimizer & Auditor",
    page_icon="🤖",
    layout="wide"
)

st.title(" AI Content Optimizer & Auditor")

st.write(
    "Generate, audit and verify AI-generated content using real-time web information."
)

topic = st.text_input(
    "Enter Topic:",
    placeholder="Example: Latest FIFA Club World Cup News"
)

content_type = st.selectbox(
    "Select Content Type:",
    [
        "News Article",
        "Blog Post",
        "Social Media Post",
        "Product Description"
    ]
)

if st.button(" GENERATE CONTENT"):

    if not topic:
        st.warning("Please enter a topic.")

    else:

        try:

            # -----------------------------
            # STEP 1 : WEB SEARCH
            # -----------------------------
            with st.spinner("🔍 Retrieving latest information..."):

                retrieved_information, sources = search_web(topic)

            st.success("Information Retrieved Successfully!")

            st.divider()

            st.header("🌐 RETRIEVED INFORMATION")

            st.write(f"Sources Found : {len(sources)}")

            for source in sources:
                st.markdown(f"- [{source['title']}]({source['url']})")

            # -----------------------------
            # STEP 2 : CONTENT GENERATION
            # -----------------------------
            with st.spinner("✍️ Generating Content..."):

                version_1, version_2 = generate_content(
                    topic,
                    content_type,
                    retrieved_information
                )

            st.divider()

            st.header("📝 CONTENT VERSION 1")
            st.write(version_1)

            st.divider()

            st.header("📝 CONTENT VERSION 2")
            st.write(version_2)

            # -----------------------------
            # STEP 3 : CONTENT AUDIT
            # -----------------------------
            with st.spinner("🔎 Auditing Version 1..."):

                audit_v1 = audit_content(
                    version_1,
                    retrieved_information
                )

            with st.spinner("🔎 Auditing Version 2..."):

                audit_v2 = audit_content(
                    version_2,
                    retrieved_information
                )

            st.divider()

            st.header("📊 AUDIT REPORT - VERSION 1")
            st.json(audit_v1)

            st.divider()

            st.header("📊 AUDIT REPORT - VERSION 2")
            st.json(audit_v2)

            # -----------------------------
            # STEP 4 : CLAIM VERIFICATION
            # -----------------------------
            with st.spinner("✅ Verifying Version 1..."):

                verification_v1 = verify_content(
                    version_1,
                    retrieved_information
                )

            with st.spinner("✅ Verifying Version 2..."):

                verification_v2 = verify_content(
                    version_2,
                    retrieved_information
                )

            st.divider()

            st.header("🔬 VERIFICATION RESULTS - VERSION 1")
            st.write(verification_v1)

            st.divider()

            st.header("🔬 VERIFICATION RESULTS - VERSION 2")
            st.write(verification_v2)

            # -----------------------------
            # STEP 5 : FINAL OUTPUT
            # -----------------------------
            st.divider()

            st.header(" FINAL DECISION")

            st.info("Content generation pipeline completed.")

            st.info(
                "This MVP displays both generated versions. "
                "Automatic best-version selection will be added later."
            )

            st.divider()

            st.header("🏆 FINAL CONTENT")

            st.subheader("Version 1")
            st.write(version_1)

            st.subheader("Version 2")
            st.write(version_2)

        except Exception as error:

            st.error(f"An error occurred:\n\n{error}")