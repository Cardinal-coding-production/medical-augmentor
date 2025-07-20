# generator/procedural/generator.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import os
import cv2
import numpy as np
from datetime import datetime
from database.db_init import SessionLocal
from database.models import SyntheticImage

# Directory to save generated images
SAVE_DIR = "data/synthetic"
os.makedirs(SAVE_DIR, exist_ok=True)

def generate_lung_blob_image(image_size=(256, 256)):
    """
    Creates a synthetic lung-like blob image.
    """
    img = np.zeros(image_size, dtype=np.uint8)

    # Simulate two lung-shaped ellipses
    center1 = (int(image_size[1] * 0.35), int(image_size[0] / 2))
    center2 = (int(image_size[1] * 0.65), int(image_size[0] / 2))
    axes = (50, 80)

    cv2.ellipse(img, center1, axes, angle=0, startAngle=0, endAngle=360, color=255, thickness=-1)
    cv2.ellipse(img, center2, axes, angle=0, startAngle=0, endAngle=360, color=255, thickness=-1)

    # Add Gaussian blur
    img = cv2.GaussianBlur(img, (21, 21), 0)

    return img

def save_image_and_log(img: np.ndarray, generator_type: str = "procedural", resolution: str = "256x256", notes: str = "synthetic lung blob"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"synthetic_{generator_type}_{timestamp}.png"
    filepath = os.path.join(SAVE_DIR, filename)

    cv2.imwrite(filepath, img)

    # Store metadata in DB
    session = SessionLocal()
    image_record = SyntheticImage(
        filename=filename,
        generator_type=generator_type,
        resolution=resolution,
        notes=notes
    )
    session.add(image_record)
    session.commit()
    session.close()

    print(f"Saved: {filename} -> DB updated")
    return filepath

def generate_procedural_images(num_images=5, output_dir="data/synthetic"):
    """
    Main function used in Streamlit app to generate and return image paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []

    for _ in range(num_images):
        img = generate_lung_blob_image()
        path = save_image_and_log(img, generator_type="procedural", resolution="256x256", notes="synthetic lung blob")
        image_paths.append(path)

    return image_paths

# Optional CLI entry point
if __name__ == "__main__":
    generate_procedural_images(num_images=5)

