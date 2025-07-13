def get_suggestions(rotate, flip_h, flip_v, brightness, contrast, noise):
    suggestions = []

    if rotate != 0:
        suggestions.append("📐 Rotation is great for orientation invariance (e.g. X-ray angles).")

    if flip_h:
        suggestions.append("↔ Horizontal flipping helps in symmetry-heavy scans like MRIs.")

    if flip_v:
        suggestions.append("↕ Vertical flipping is rare but can be useful in dermatology datasets.")

    if brightness != 1.0:
        suggestions.append("💡 Brightness adjustment helps model learn across exposure variations.")

    if contrast != 1.0:
        suggestions.append("🎚️ Contrast tuning is useful for better visibility of fine details.")

    if noise != 0:
        suggestions.append("🎛️ Adding Gaussian noise helps with robustness in real-world data.")

    if not suggestions:
        suggestions.append("✅ Tip: Try combining multiple augmentations for stronger results!")

    return suggestions
