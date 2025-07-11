from PIL import Image, ImageEnhance
import numpy as np

def rotate_image(image: Image.Image, angle: int) -> Image.Image:
    """Rotate image by a specified angle in degrees."""
    return image.rotate(angle)

def flip_horizontal(image: Image.Image) -> Image.Image:
    """Flip image horizontally (left to right)."""
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def flip_vertical(image: Image.Image) -> Image.Image:
    """Flip image vertically (top to bottom)."""
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust brightness.
    Factor < 1.0 makes it darker, > 1.0 makes it brighter.
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjust contrast.
    Factor < 1.0 lowers contrast, > 1.0 increases contrast.
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def add_gaussian_noise(image: Image.Image, std_dev: float = 10.0) -> Image.Image:
    """
    Add Gaussian noise to image.
    std_dev controls the intensity of the noise.
    """
    arr = np.array(image).astype(np.float32)
    noise = np.random.normal(0, std_dev, arr.shape)
    noisy_arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_arr)
