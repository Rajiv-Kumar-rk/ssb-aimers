import streamlit as st
import pandas as pd

@st.dialog("Story Report Analysis", width="large", dismissible=True)
def tat_story_report_dialog(response, is_suggested_story=False):
    st.title("🪖 SSB Story Evaluation Report")

    if is_suggested_story:
        st.header(f"Suggested Story: {response['generated_story']['title']}")
        st.text(f"{response['generated_story']['story_text']}")

    # ========== IMAGE ANALYSIS ==========
    st.header("🖼️ Image–Story Relevance")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Relevance Score", f"{response['image_analysis']['relevance_score']}/10")
        verdict = response['image_analysis']['verdict']
        if verdict.lower() == "not relevant":
            st.error(f"Verdict: {verdict}")
        else:
            st.success(f"Verdict: {verdict}")
    with col2:
        st.write(f"**Justification:** {response['image_analysis']['justification']}")

    st.markdown("**Identified Elements:**")
    st.write(", ".join(response['image_analysis']['identified_elements']))

    # --- Object Utilization Table ---
    st.markdown("### 📋 Object Utilization Mapping")
    util_data = [
        {
            "Element": obj["element"],
            "Present in Story": "✅ Yes" if obj["present_in_story"] else "❌ No",
            "Representation in Story": obj["representation"] or "—"
        }
        for obj in response["image_analysis"]["object_utilization_table"]
    ]

    st.dataframe(
    pd.DataFrame(util_data),
    width="stretch",
    hide_index=True  # 👈 This hides the sequence number column
)
    # ========== STORY COMPLIANCE ==========
    st.header("✅ Story Rule Compliance")
    if response["story_compliance"]["passed"]:
        st.success("Pass – Story meets SSB structure and positivity standards.")
    else:
        st.error("Fail – Story deviates from required structure.")
    st.caption(response["story_compliance"]["justification"])

    # ========== OLQ SCORES ==========
    st.header("🧩 OLQ Scoring Breakdown")

    cols = st.columns(3)
    for i, olq in enumerate(response["olq_scores_summary"]):
        col = cols[i % 3]
        with col:
            with st.expander(f"{olq['name']} — {olq['score']}/10"):
                st.progress(olq["score"] / 10)
                st.caption(olq["justification"])

    if not is_suggested_story:
        # ========== PSYCHOLOGICAL SUMMARY ==========
        st.header("🧠 Psychological Summary")
        st.info(response["psychological_summary"]["mindset_summary"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💪 Strengths")
            for s in response["psychological_summary"]["strengths"]:
                st.markdown(f"- {s}")
        with col2:
            st.subheader("⚙️ Weaknesses")
            for w in response["psychological_summary"]["weaknesses"]:
                st.markdown(f"- {w}")

        # --- Areas of Improvement ---
        st.subheader("🔍 Areas of Improvement")
        for area in response["psychological_summary"]["areas_of_improvement"]:
            st.markdown(f"- {area}")

        # --- Key Inference & Final Verdict ---
        st.subheader("🧭 Key Personality Inference")
        st.write(response["psychological_summary"]["key_personality_inference"])

        verdict = response["psychological_summary"]["final_verdict"]
        if verdict.lower() == "recommended":
            st.success(f"🏅 Final Verdict: {verdict}")
        else:
            st.error(f"🏅 Final Verdict: {verdict}")
