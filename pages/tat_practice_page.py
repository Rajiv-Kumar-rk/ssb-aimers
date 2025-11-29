import os
import random
import streamlit as st
from story_checker import examine_candidate_written_story
from story_generator import generate_image_story
from utils.tat_story_report_dialog import tat_story_report_dialog


st.set_page_config(page_title="SSB Prep", page_icon="🎯")


st.title("TAT Practice")

IMAGES_DIR = os.path.join('.', 'tat_images')
image_files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.jfif', '.gif', '.bmp'))]

# Inline uploader and random-image button: uploader on the left, random button on the right
col_upload, col_random = st.columns([4, 1])

# Max upload size constant
MAX_UPLOAD_BYTES = 5 * 1024 * 1024

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload an image (optional) — Max 5 MB", 
        type=["png", "jpg", "jpeg", "webp"], 
        accept_multiple_files=False,
        )
    st.caption("Supported: PNG, JPG, JPEG, WEBP — Max 5 MB")
    # Enforce max upload size (5 MB)
    if uploaded_file is not None:
        try:
            size = getattr(uploaded_file, 'size', None)
            if size is not None and size > MAX_UPLOAD_BYTES:
                st.toast("Uploaded file is too large. Maximum allowed size is 5 MB.", icon="❌")
                uploaded_file = None
        except Exception:
            # If for some reason size can't be read, don't block; allow downstream code to handle errors
            pass

def pick_random_image():
    if not image_files:
        return
    current = st.session_state.get('current_image_name')
    choices = [f for f in image_files if f != current]
    # If only one image exists, keep it; otherwise pick a different one
    st.session_state.current_image_name = random.choice(choices) if choices else current

with col_random:
    st.button("🎲 Random Image", on_click=pick_random_image, key="random_img_btn", use_container_width=True)

if 'current_image_name' not in st.session_state:
    st.session_state.current_image_name = random.choice(image_files) if image_files else None



# Determine which image to show/use: uploaded file takes precedence
if uploaded_file is not None:
    image_source = uploaded_file
else:
    sel = st.session_state.get('current_image_name')
    image_source = os.path.join(IMAGES_DIR, sel) if sel else None

# Preview the selected image (use container width so it stretches responsively)
st.image(image=image_source, use_column_width=True)

# Text area for user story input
story_input = st.text_area(label="Write your story", placeholder="Write your story here...", label_visibility="hidden")

actionButtonsContainer = st.empty()
with actionButtonsContainer:
    # 3 columns: left spacer, button row, right spacer
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:  # Center column
        b1, b2 = st.columns([1, 1])

        with b1:
            examine_btn = st.button("🔍 Examine Story", type="secondary", use_container_width=True, key="examine_btn")
        with b2:
            suggest_btn = st.button("💡 Suggest Story", type="secondary", use_container_width=True, key="suggest_btn")


if examine_btn:
    if story_input.strip() == "":
        st.toast("Provide us with your story written above displayed picture.", icon="ℹ️")
    else:
        with st.spinner("⏳ Wait, we're analyzing your submission..."):
            response = examine_candidate_written_story(
                    image_path=image_source,
                    story_content=story_input.strip()
                )

        # After spinner completes
        if not response:
            st.toast("Something went wrong.", icon="❌")
        else:
            st.toast("Report generated successfully.", icon="✅")
            tat_story_report_dialog(response, False)

elif suggest_btn:

    with st.spinner("⏳ Wait, we're generating story based on above displayed picture..."): 
        response = generate_image_story(
            image_path=image_source
        )
    
    if not response:
        st.toast("Something went wrong.", icon="❌")
    else: 
        st.toast("Story generated successfully.", icon="✅")
        tat_story_report_dialog(response, True)
