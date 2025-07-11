import streamlit as st

def get_augmentation_controls():
    st.markdown("### Select Augmentations")
    rotate_angle = st.slider("Rotate Angle (°)", -30, 30, 0)
    flip_h = st.checkbox("Flip Horizontally")
    flip_v = st.checkbox("Flip Vertically")
    brightness = st.slider("Brightness", 0.5, 1.5, 1.0)
    contrast = st.slider("Contrast", 0.5, 1.5, 1.0)
    noise_std = st.slider("Gaussian Noise Std Dev", 0.0, 50.0, 0.0)

    return rotate_angle, flip_h, flip_v, brightness, contrast, noise_std

