import streamlit as st

st.set_page_config(page_title="SSB Prep", page_icon="🎯")

st.markdown("# SSB Preparation Hub")
st.markdown("Welcome, Buddy ! Prepare effectively for your upcoming SSB with this amazing suite of tools focused on Indian context and SSB standards.")

modules = [
    {
        "id": "intro",
        "title": "Intro",
        "path": "pages/tat_intro_page.py",
        "desc": "Guidelines, tips, and an overview of the Thematic Apperception Test.",
        "icon": "📘",
    },
    {
        "id": "practice",
        "title": "Practice",
        "path": "pages/tat_practice_page.py",
        "desc": "Hands-on image-based practice with generation and evaluation tools.",
        "icon": "🎯",
    },
]

# Render modules as cards in a responsive row
cols = st.columns(len(modules))
for i, m in enumerate(modules):
    with cols[i]:
        st.markdown(f"### {m['icon']} {m['title']}")
        st.caption(m['desc'])
        if st.button(f"Open {m['title']}", key=f"open_{m['id']}", use_container_width=True):
            st.switch_page(m['path'])

st.markdown("---")