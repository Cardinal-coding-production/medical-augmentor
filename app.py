import streamlit as st
from PIL import Image
from io import BytesIO
from augmentations import basic
from utils.ui_elements import get_augmentation_controls


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


st.title("🧠 Medical Image Augmentor")
st.markdown("Upload your medical image and apply safe augmentations.")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload PNG or JPG image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)


    st.markdown("### Select Augmentations")

    # --- Augmentation Inputs ---
    rotate_angle, flip_h, flip_v, brightness, contrast, noise_std = get_augmentation_controls()


    if st.button("Apply Augmentations"):
        aug_image = image.copy()

        if rotate_angle != 0:
            aug_image = basic.rotate_image(aug_image, rotate_angle)
        if flip_h:
            aug_image = basic.flip_horizontal(aug_image)
        if flip_v:
            aug_image = basic.flip_vertical(aug_image)
        if brightness != 1.0:
            aug_image = basic.adjust_brightness(aug_image, brightness)
        if contrast != 1.0:
            aug_image = basic.adjust_contrast(aug_image, contrast)
        if noise_std > 0.0:
            aug_image = basic.add_gaussian_noise(aug_image, noise_std)

        st.image(aug_image, caption="Augmented Image", use_container_width=True)

        st.success("✅ Augmentation applied successfully.")

        with st.spinner("Applying augmentations..."):
    # image processing code here
            ...
        st.success("✅ Done!")





        # --- Download Button ---
        buf = BytesIO()
        aug_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Download Augmented Image",
            data=byte_im,
            file_name="augmented_image.png",
            mime="image/png"
        )
