import streamlit as st
import os

st.set_page_config(page_title="SSB Prep", page_icon="🎯")

st.title("🎯 TAT Practice — Prepare for SSB with Confidence")

hero_path = os.path.join('.', 'tat_images', 'tat_pic.jpg')

cols = st.columns([2, 1])
with cols[0]:
    st.markdown("### Ace the Thematic Apperception Test (TAT)")
    st.markdown(
        "Practice writing clear, positive, and SSB-aligned stories based on images — get instant evaluation and feedback on Officer-Like Qualities (OLQs)."
    )

    st.markdown("**What you get:**")
    st.markdown("- Realistic, Indian-context TAT prompts and sample images")
    st.markdown("- Automated story generation from images (practice mode)")
    st.markdown("- Detailed evaluation across 15 OLQs with short justifications")
    st.markdown("- Quick tips to improve structure, positivity, and relevance")

    if st.button("🚀 Start Practice", use_container_width=True, key="start_tat"):
        st.switch_page("pages/tat_practice_page.py")

with cols[1]:
    # Show a hero image if available
    try:
        st.image(hero_path, caption="TAT Practice — Visual Prompt Example", width="stretch")
    except Exception:
        # image optional; ignore if missing
        pass

st.markdown("---")

features = st.columns(3)
with features[0]:
    st.markdown("**⏱️ Timed Practice**\n\nSimulate real TAT timing and constraints.")
with features[1]:
    st.markdown("**🧠 OLQ Feedback**\n\nReceive structured scoring and short psychological summary.")
with features[2]:
    st.markdown("**💡 Tips & Examples**\n\nQuick actionable tips to refine your stories.")

with st.expander("How to use this tool", expanded=False):
    st.markdown("1. Choose or upload an image on the Practice page.\n2. Write your story or request a suggested story.\n3. Get an evaluation and OLQ scores.\n4. Improve and repeat.")

st.markdown("---")
st.caption("Created to help aspirants practice TAT with fast, guided feedback. Use responsibly — for practice only.")