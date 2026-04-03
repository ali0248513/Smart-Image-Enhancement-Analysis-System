"""
Phase 4 – Intensity Transformations  (Lab 04)
Negative, Log, Gamma correction (γ=0.5 and γ=1.5).
Identifies best method for brightening and highlighting detail.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def _negative(img: np.ndarray) -> np.ndarray:
    return 255 - img


def _log_transform(img: np.ndarray) -> np.ndarray:
    img_float = img.astype(np.float64) + 1.0
    c = 255.0 / np.log(1 + img_float.max())
    log_img = c * np.log(img_float)
    return np.clip(log_img, 0, 255).astype(np.uint8)


def _gamma_correction(img: np.ndarray, gamma: float) -> np.ndarray:
    img_norm = img / 255.0
    corrected = np.power(img_norm, gamma) * 255.0
    return np.clip(corrected, 0, 255).astype(np.uint8)


def intensity_transformations(img_gray: np.ndarray, results_dir: str) -> None:
    negative   = _negative(img_gray)
    log_img    = _log_transform(img_gray)
    gamma_05   = _gamma_correction(img_gray, 0.5)
    gamma_15   = _gamma_correction(img_gray, 1.5)

    images = [img_gray, negative, log_img, gamma_05, gamma_15]
    titles = [
        "Original",
        "Negative\n(s = 255 − r)",
        "Log Transform\n(s = c·log(1+r))",
        "Gamma γ=0.5\n(brightening)",
        "Gamma γ=1.5\n(darkening)"
    ]
    means  = [f"Mean: {im.mean():.1f}" for im in images]

    # ── comparison figure ────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    fig.suptitle("Phase 4 – Intensity Transformations", fontsize=13, fontweight="bold")

    for col, (img, title, mean) in enumerate(zip(images, titles, means)):
        axes[0, col].imshow(img, cmap="gray", vmin=0, vmax=255)
        axes[0, col].set_title(title, fontsize=9)
        axes[0, col].axis("off")
        axes[0, col].text(0.5, -0.05, mean, transform=axes[0, col].transAxes,
                          ha="center", fontsize=8, color="gray")

        axes[1, col].hist(img.ravel(), bins=64, range=(0, 255), color="steelblue", alpha=0.7)
        axes[1, col].set_xlim(0, 255)
        axes[1, col].set_xlabel("Pixel value", fontsize=8)
        axes[1, col].set_ylabel("Count", fontsize=8)
        axes[1, col].tick_params(labelsize=7)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "phase4_intensity.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── analysis ─────────────────────────────────────────────────────────────
    print("  Intensity transformation analysis:")
    for title, img in zip(titles, images):
        label = title.replace("\n", " ")
        print(f"    {label:<35} mean={img.mean():.1f}  std={img.std():.1f}")

    print("\n  Best method for BRIGHTENING     : Gamma γ=0.5  (raises dark pixels non-linearly)")
    print("  Best method for HIGHLIGHTING DETAIL: Log Transform  (compresses highlights, expands shadows)")
    print(f"  Saved → {results_dir}/phase4_intensity.png")
