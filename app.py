import streamlit as st
from PIL import Image
from io import BytesIO
from augmentations import basic
from utils.ui_elements import get_augmentation_controls
import io
from datetime import datetime
import zipfile
import pandas as pd
from suggestions import get_suggestions
from logger import log_augmentation
from augmentations.basic import random_augmentations




st.set_page_config(page_title="Medical Image Augmentor", layout="centered")

with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. **Upload** a medical image (PNG or JPG).
    2. **Select augmentations** from the panel.
    3. Click **Apply** to view results.
    4. Click **Download** to save the augmented image.

    ⚠️ *Avoid excessive noise or rotation on small images.*
    """)

st.image("assets/logo.png", width=150)
st.title("🧠 Cardinal MedAug - Medical Image Augmentor")
st.markdown("""
Welcome to **Cardinal MedAug** — a free tool to safely augment medical images for use in research and AI training.

Upload your medical images, preview your augmentations in real-time, and download the enhanced dataset in one click.

---

**Why use this?**
- Quick augmentation for training datasets
- No coding required
- Built for researchers, data scientists, and medical imaging teams

---
""")

# --- File Upload ---
uploaded_files = st.file_uploader(
   "Upload PNG or JPG image",
   type=["png", "jpg", "jpeg"],
   accept_multiple_files=True)

st.markdown("### Select Augmentations")
mode = st.radio("Choose Mode:", ["Custom", "Power"])
if mode == "Power":
    st.info("🚀 Power Mode applies a random combination of augmentations. Upload multiple images to see diverse results!")


    # --- Augmentation Inputs ---
rotate_angle, flip_h, flip_v, brightness, contrast, noise_std = get_augmentation_controls()


augmented_images = []

if 'augment_count' not in st.session_state:
    st.session_state['augment_count'] = 0


if uploaded_files and st.button("Apply Augmentations"):
    st.session_state['augment_count'] += 1
    log_augmentation(rotate_angle, flip_h, flip_v, brightness, contrast, noise_std)

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Original Image", use_container_width=True)

        if mode == "Power (Random Strong Augmentations)":
            aug_image = basic.random_augmentations(image)
        else:

            aug_image = basic.apply_augmentations(
            image,
            rotate_angle=rotate_angle,
            flip_h=flip_h,
            flip_v=flip_v,
            brightness=brightness,
            contrast=contrast,
            noise_std=noise_std
    )

        augmented_images.append((uploaded_file.name, aug_image))
        st.image(aug_image, caption=f"Augmented - {uploaded_file.name}", use_container_width=True)

    image = Image.open(uploaded_file).convert("RGB")

    st.success("✅ Augmentation applied successfully.")

    suggestions = get_suggestions(rotate_angle, flip_h, flip_v, brightness, contrast, noise_std)

with st.expander("💡 Smart Suggestions"):
    suggestions = get_suggestions(rotate_angle, flip_h, flip_v, brightness, contrast, noise_std)
    st.sidebar.markdown("### 💡 Suggestions")
    st.sidebar.write(suggestions)
    for tip in suggestions:
        st.sidebar.write("- " + tip)



    with st.spinner("Applying augmentations..."):


    # --- Download Button ---
            if augmented_images:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
                    for filename, image in augmented_images:
                        img_buffer = io.BytesIO()
                        image.save(img_buffer, format="PNG")
                        zip_file.writestr(f"aug_{filename}", img_buffer.getvalue())
                zip_buffer.seek(0)

                file_name = f"aug_image_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"

                st.download_button(
                    label="📦 Download All Augmented Images (ZIP)",
                    data=zip_buffer,
                    file_name="augmented_images.zip",
                    mime="application/zip"
                )

    with st.expander("🗣️ Give Feedback"):
         st.markdown(
        "[Fill out our feedback form here](https://forms.gle/4YgG1EkKYzi7jiWH6)",
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("### 📊 Analytics")
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQXG_NBp7YYJQIp4cJSpyofLS3V_GJSJUEXt1aqZ16HU6Wz9uzF1lcW54rWgCWW_RKDeH5pdFaxBUjU/pub?output=csv/export?format=csv"
        df = pd.read_csv(sheet_url)
        st.dataframe(df.tail(5))  # Show latest 5 feedbacks
    except Exception as e:
        st.error(f"Failed to load feedback data: {e}")
        st.metric(label="Total Augmentations", value=st.session_state['augment_count'])


