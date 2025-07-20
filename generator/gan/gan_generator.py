import numpy as np
from PIL import Image
import os
import uuid

def generate_gan_images(num_images=1, output_dir="data/synthetic", image_size=(64, 64)):
    os.makedirs(output_dir, exist_ok=True)
    images = []

    for _ in range(num_images):
        # Dummy GAN output: generate random noise image
        array = np.random.randint(0, 256, (image_size[0], image_size[1], 3), dtype=np.uint8)
        img = Image.fromarray(array)
        filename = f"gan_{uuid.uuid4().hex}.png"
        path = os.path.join(output_dir, filename)
        img.save(path)
        images.append((filename, img))

    return images
