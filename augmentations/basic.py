from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import random

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

def apply_augmentations(
    image: Image.Image,
    rotate_angle: int = 0,
    flip_h: bool = False,
    flip_v: bool = False,
    brightness: float = 1.0,
    contrast: float = 1.0,
    noise_std: float = 0.0
) -> Image.Image:
    """Applies a series of augmentations to an image based on input parameters."""
    aug_image = image

    if rotate_angle != 0:
        aug_image = rotate_image(aug_image, rotate_angle)
    if flip_h:
        aug_image = flip_horizontal(aug_image)
    if flip_v:
        aug_image = flip_vertical(aug_image)
    if brightness != 1.0:
        aug_image = adjust_brightness(aug_image, brightness)
    if contrast != 1.0:
        aug_image = adjust_contrast(aug_image, contrast)
    if noise_std != 0.0:
        aug_image = add_gaussian_noise(aug_image, noise_std)

    return aug_image

def random_augmentations(image):
    """Applies a random sequence of strong augmentations to the input image."""
    if not isinstance(image, Image.Image):
        image = Image.fromarray(np.array(image).astype("uint8"))

    # Define a list of available augmentation operations
    operations = [
        lambda img: img.rotate(random.randint(-25, 25)),
        lambda img: ImageOps.mirror(img),
        lambda img: ImageOps.flip(img),
        lambda img: ImageEnhance.Brightness(img).enhance(random.uniform(0.7, 1.5)),
        lambda img: ImageEnhance.Contrast(img).enhance(random.uniform(0.7, 1.5)),
        lambda img: img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.5))),
        lambda img: add_random_noise(img, std=random.uniform(5, 20)),
    ]

    # Randomly select 3 to 5 operations to apply
    num_ops = random.randint(3, 5)
    selected_ops = random.sample(operations, num_ops)

    for op in selected_ops:
        image = op(image)

    return image

def add_random_noise(image, std=10):
    """Adds Gaussian noise to a PIL image."""
    arr = np.array(image).astype(np.float32)
    noise = np.random.normal(0, std, arr.shape)
    noisy_arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_arr)

