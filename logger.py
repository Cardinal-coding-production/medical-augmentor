from datetime import datetime
import os

def log_augmentation(rotate, flip_h, flip_v, brightness, contrast, noise):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log = {
        "time": timestamp,
        "rotate": rotate,
        "flip_h": flip_h,
        "flip_v": flip_v,
        "brightness": brightness,
        "contrast": contrast,
        "noise": noise
    }

    log_dir = "data/synthetic"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "logs.txt"), "a") as f:
        f.write(str(log) + "\n")
