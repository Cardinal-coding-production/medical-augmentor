import streamlit as st
import traceback

try:
    import os
    import io
    import zipfile
    import uuid
    from PIL import Image
    from datetime import datetime
    import pandas as pd

    from augmentations import basic
    from utils.ui_elements import get_augmentation_controls
    from suggestions import get_suggestions
    from logger import log_augmentation
    from database.models import SyntheticImage
    from database.db_init import SessionLocal, save_to_database, init_db
    from generator.procedural.generator import generate_procedural_images
    from generator.gan.gan_generator import generate_gan_images

    SAVE_DIR = "/tmp/synthetic"
    os.makedirs("/tmp/synthetic", exist_ok=True)

    init_db()

    st.set_page_config(page_title="Medical Image Augmentor", layout="centered")
    st.success("✅ App booted successfully")

except Exception as e:
    st.title("🚨 App Startup Failed")
    st.error("The app failed to start. Here's the traceback:")
    st.exception(e)
    st.stop()

# --- Ensure augment_count is always initialized ---
if 'augment_count' not in st.session_state:
    st.session_state['augment_count'] = 0

with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. Choose a mode below.
    2. Upload image(s) or click generate.
    3. Preview results and download outputs.
    """)

st.image("assets/logo.jpg", width=150)
st.title("🧠 Cardinal MedAug")

# -------------------------
# 🔄 Mode Switch UI
# -------------------------
mode = st.radio("Choose Mode", ["Procedural Generator", "AI Generator", "Image Augmentation"])

# Session connection
session = SessionLocal()

# -------------------------
# 🔬 Procedural Generator
# -------------------------
if mode == "Procedural Generator":
    st.subheader("🧬 Generate Synthetic Medical Images")
    num_images = st.slider("Number of images to generate", 1, 10, 3)

    if st.button("🚀 Generate Images"):
        image_paths = generate_procedural_images(n=num_images)

        for path in image_paths:
            st.image(path, use_container_width=True)

            filename = os.path.basename(path)
            new_entry = SyntheticImage(
                id=str(uuid.uuid4()),
                filename=filename,
                generator_type="procedural",
                resolution="256x256",
                notes="synthetic lung blob",
                created_at=datetime.now()
            )
            session.add(new_entry)
        session.commit()
        st.success(f"✅ Generated and saved {num_images} synthetic images.")

# -------------------------
# 🧪 Image Augmentation
# -------------------------
elif mode == "Image Augmentation":
    uploaded_files = st.file_uploader(
       "Upload PNG or JPG image",
       type=["png", "jpg", "jpeg"],
       accept_multiple_files=True)

    st.markdown("### Select Augmentations")
    aug_mode = st.radio("Choose Augmentation Mode:", ["Custom", "Power"])
    if aug_mode == "Power":
        st.info("🚀 Power Mode applies a random combination of augmentations.")

    rotate_angle, flip_h, flip_v, brightness, contrast, noise_std = get_augmentation_controls()

    augmented_images = []

    if uploaded_files and st.button("Apply Augmentations"):
        st.session_state['augment_count'] += 1
        log_augmentation(rotate_angle, flip_h, flip_v, brightness, contrast, noise_std)

        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Original Image", use_container_width=True)

            if aug_mode == "Power":
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

            filename = f"augmented_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.png"
            save_path = os.path.join(SAVE_DIR, filename)
            aug_image.save(save_path)
            augmented_images.append((uploaded_file.name, aug_image))
            st.image(aug_image, caption=f"Augmented - {uploaded_file.name}", use_container_width=True)

            entry = SyntheticImage(
                id=str(uuid.uuid4()),
                filename=filename,
                generator_type="augmentation",
                resolution=f"{aug_image.width}x{aug_image.height}",
                notes="user uploaded augmentation",
                created_at=datetime.now()
            )
            session.add(entry)

        session.commit()
        st.success("✅ Augmentation applied and saved.")

        suggestions = get_suggestions(rotate_angle, flip_h, flip_v, brightness, contrast, noise_std)
        with st.expander("💡 Smart Suggestions"):
            for tip in suggestions:
                st.write("- " + tip)

        if augmented_images:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
                for filename, image in augmented_images:
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format="PNG")
                    zip_file.writestr(f"aug_{filename}", img_buffer.getvalue())
            zip_buffer.seek(0)

            st.download_button(
                label="📦 Download All Augmented Images (ZIP)",
                data=zip_buffer,
                file_name="augmented_images.zip",
                mime="application/zip"
            )

# -------------------------
# 🤖 AI Generator (GAN)
# -------------------------
elif mode == "AI Generator":
    st.subheader("🧠 Generate GAN-based Synthetic Medical Images")
    num_images = st.slider("Number of GAN images to generate", 1, 10, 1)

    if st.button("🎨 Generate GAN Images"):
        generated = generate_gan_images(num_images)

        for filename, image in generated:
            st.image(image, caption=filename, use_container_width=True)
            save_to_database(
                filename=filename,
                generator_type="GAN",
                resolution=f"{image.size[0]}x{image.size[1]}",
                notes="Generated using GAN"
            )

# -------------------------
# 🖼 Show Recent Images
# -------------------------
st.subheader("🖼 Recently Generated or Augmented Images")
recent = session.query(SyntheticImage).order_by(SyntheticImage.created_at.desc()).limit(5).all()
for r in recent:
    image_path = os.path.join(SAVE_DIR, r.filename)
    if os.path.exists(image_path):
        st.image(image_path, caption=f"{r.generator_type.capitalize()} @ {r.created_at.strftime('%Y-%m-%d %H:%M')}", use_container_width=True)

# -------------------------
# Feedback + Analytics
# -------------------------
with st.expander("🗣️ Give Feedback"):
    st.markdown("[Fill out our feedback form here](https://forms.gle/4YgG1EkKYzi7jiWH6)", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📊 Analytics")
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRHXpKAMaLKLSGiK35cvfVpm_6Me_sN5ErzygL-xcMLH5zfhKg0JPb-VZv_PNXR9dA_vt0dQgXbgtxz/pub?output=csv"
        df = pd.read_csv(sheet_url)
        st.dataframe(df.tail(5))
    except Exception as e:
        st.warning("Feedback sheet failed to load.")
        st.metric(label="Total Augmentations", value=st.session_state.get('augment_count', 0))

