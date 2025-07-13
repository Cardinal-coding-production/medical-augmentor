from datetime import datetime

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

    with open("logs.txt", "a") as f:
        f.write(str(log) + "\n")
