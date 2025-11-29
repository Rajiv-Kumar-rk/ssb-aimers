import streamlit as st

pages = {
    "Introduction": [st.Page("pages/main_page.py", title="Home")],
    "TAT TEST": [
        st.Page("pages/tat_intro_page.py", title="TAT Introduction"),
        st.Page("pages/tat_practice_page.py", title="TAT Practice"),
    ],
}

pg = st.navigation(pages)
pg.run()

